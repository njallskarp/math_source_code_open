"""Complete 144-case type-62 extremal consumer, with physical CNF and DRAT audits."""
from itertools import combinations,permutations
from pathlib import Path
import argparse,json,subprocess,time
from hashlib import sha256
import audit

PAIRS=list(combinations(range(43),2))
def decode(record):
    n=ord(record[0])-63;bits=''.join(format(ord(ch)-63,'06b') for ch in record[1:]);k=0;E=set()
    for v in range(n):
        for u in range(v):
            if bits[k]=='1':E.add((u,v))
            k+=1
    return E

def cases(inputs,certificate):
    family=next(f for f in certificate['families'] if f['type']==62)
    F={(0,2),(0,3),(0,4),(1,2),(1,3)}
    for h in (6,7,8):
        E=decode(inputs['interfaces'][h]);S=[v for v in range(21) if (v,21) in E]
        marks=[p for p in permutations(S) if {tuple(sorted((p[u],p[v]))) for u,v in F}=={e for e in E if e[0] in S and e[1] in S}]
        if len(marks)!=2:raise ValueError('complete S marking count')
        for j,rep in enumerate(family['representatives']):
            for k,p in enumerate(marks):yield (h,62,j,k),E,p,rep['columns']

def specification(E,mark,columns):
    lookup={v:i for i,v in enumerate(mark)};fixed={}
    for u,v in PAIRS:
        if v<22:fixed[u,v]=(u,v) in E
        elif u==22 or v==22:fixed[u,v]=(u if v==22 else v)<22
        elif u==21:fixed[u,v]=v<40
        elif 23<=u<v<40:fixed[u,v]=(v-u)%17 in {1,2,4,8,9,13,15,16}
        elif u in lookup and 23<=v<40:fixed[u,v]=bool(columns[lookup[u]]>>(v-23)&1)
    return fixed

def independent_specification(inputs,certificate,key):
    h,kind,j,k=key;n,E=audit.graph6(inputs['interfaces'][h]);audit.require(n==22,'order')
    S=sorted(v for v in range(22) if tuple(sorted((v,21))) in E)
    marks=[p for p in permutations(S) if all((tuple(sorted((p[u],p[v]))) in E)==((u,v) in audit.s_edges(kind)) for u,v in combinations(range(5),2))]
    columns=next(f for f in certificate['families'] if f['type']==kind)['representatives'][j]['columns']
    A=[[2]*43 for _ in range(43)]
    def put(u,v,c):A[u][v]=A[v][u]=int(c)
    for u,v in combinations(range(22),2):put(u,v,(u,v) in E)
    for v in range(43):
        if v!=22:put(22,v,v<22)
    for v in range(23,43):put(21,v,v<=39)
    P=audit.paley()
    for u,v in combinations(range(17),2):put(u+23,v+23,P[u][v])
    for s,v in enumerate(marks[k]):
        for t in range(17):put(v,t+23,columns[s]>>t&1)
    return bytes(48+A[u][v] for u,v in PAIRS)

def encode(fixed):
    variables={e:i+1 for i,e in enumerate(e for e in PAIRS if e not in fixed)};clauses=set()
    for color in (False,True):
        allowed=[sum(1<<v for v in range(u+1,43) if fixed.get((u,v),color)==color) for u in range(43)]
        def visit(chosen,candidates):
            if len(chosen)==5:
                clause=tuple((-1 if color else 1)*variables[e] for e in combinations(chosen,2) if e in variables)
                clauses.add(clause);return
            while candidates.bit_count()>=5-len(chosen):
                bit=candidates&-candidates;candidates^=bit;v=bit.bit_length()-1
                visit(chosen+[v],candidates&allowed[v])
        visit([], (1<<43)-1)
    data=(f'p cnf {len(variables)} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in sorted(clauses))).encode()
    return data,len(variables),len(clauses)

def main():
    p=argparse.ArgumentParser();p.add_argument('scratch',type=Path);p.add_argument('--kissat',required=True)
    p.add_argument('--drat-trim',required=True);p.add_argument('--audit-cnf',required=True);p.add_argument('--seconds',type=int)
    args=p.parse_args();source=Path(__file__).parent;scratch=args.scratch.resolve()
    if scratch.exists() or source.resolve() in scratch.parents:raise ValueError('new external scratch required')
    scratch.mkdir(parents=True);inputs=json.loads((source/'inputs.json').read_text());certificate=json.loads((source/'certificate.json').read_text())
    allcases=list(cases(inputs,certificate));audit.require(len(allcases)==144,'complete case count')
    manifest=[];runs=[]
    for key,E,mark,columns in allcases:
        stem='-'.join(map(str,key));fixed=specification(E,mark,columns)
        raw=bytes(48+int(fixed[e]) if e in fixed else 50 for e in PAIRS)
        independently_fixed=independent_specification(inputs,certificate,key)
        audit.require(raw==independently_fixed,'independent physical specification differs')
        matrix=scratch/(stem+'.matrix');matrix.write_bytes(independently_fixed)
        data,nv,nc=encode(fixed);audit.require(nv==389,'all remaining physical edges')
        cnf=scratch/(stem+'.cnf');cnf.write_bytes(data);other=scratch/(stem+'.independent.cnf')
        subprocess.run([args.audit_cnf,str(matrix),str(other)],check=True)
        audit.require(other.read_bytes()==data,'literal five-set CNF differs entry by entry')
        proof=scratch/(stem+'.drat');command=[args.kissat]
        if args.seconds is not None:command.append('--time='+str(args.seconds))
        command.extend([str(cnf),str(proof)]);start=time.monotonic()
        with (scratch/(stem+'.solver.log')).open('w') as f:r=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT)
        audit.require(r.returncode==20,'UNSAT not established; incomplete family')
        solver_seconds=time.monotonic()-start;start=time.monotonic()
        checked=subprocess.run([args.drat_trim,str(cnf),str(proof)],text=True,capture_output=True)
        (scratch/(stem+'.check.log')).write_text(checked.stdout+checked.stderr)
        audit.require(checked.returncode==0 and 's VERIFIED' in checked.stdout,'proof not verified')
        row={'key':list(key),'variables':nv,'clauses':nc,'cnf_sha256':sha256(data).hexdigest()};manifest.append(row)
        runs.append({**row,'solver_seconds':solver_seconds,'checker_seconds':time.monotonic()-start,'proof_bytes':proof.stat().st_size,'proof_sha256':sha256(proof.read_bytes()).hexdigest()})
        (scratch/'runs.json').write_text(json.dumps(runs,indent=2)+'\n')
        if len(runs)%12==0:print(len(runs),'of 144 complete cases VERIFIED',flush=True)
    raw=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode();(scratch/'manifest.json').write_bytes(raw)
    expected=source/'GLUING_MANIFEST.json'
    if expected.exists():audit.require(expected.read_bytes()==raw,'complete gluing manifest mismatch')
    result={'status':'VERIFIED_COMPLETE_TYPE62_DENSITY115_EXCLUSION','complete_cases':144,
            'interfaces':[6,7,8],'free_edges_per_case':389,'manifest_sha256':sha256(raw).hexdigest(),
            'new_global_hub_deficiency_lower_bound':8}
    (scratch/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True),flush=True)

if __name__=='__main__':main()
