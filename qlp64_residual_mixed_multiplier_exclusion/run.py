"""Rebuild and audit the complete necessary cover for mixed multiplier 33."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shlex
import subprocess
import time
import cover
import quotient
import audit_fibers
import replay32
import structural

ROOT=Path(__file__).resolve().parent


def write_json(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def strip_seconds(value):return {k:v for k,v in value.items() if k!='seconds'}
def canonical_json(qs):return json.dumps(qs,separators=(',',':'))+'\n'


def save_cover(work,name,qs):
    qs=sorted(qs);data=canonical_json(qs);(work/name).write_text(data)
    return dict(states=len(qs),sha256=hashlib.sha256(data.encode()).hexdigest())


def parent_file(work,name,qs):
    n=len(qs[0][0]);path=work/name
    path.write_text(f'{n} {len(qs)}\n'+'\n'.join(' '.join(str(v) for row in q for v in row) for q in qs)+'\n')
    return path


def parse_children(path,n):
    out=[]
    for line in path.read_text().splitlines():
        vals=list(map(int,line.split()));assert len(vals)==3*n
        out.append(tuple(tuple(vals[j:j+n]) for j in range(0,3*n,n)))
    assert len(out)==len(set(out))
    return sorted(out)


def compile_sources(work,cxx,flags):
    args=[cxx,'-std=c++20','-O3','-Wall','-Wextra','-Wpedantic','-Wshadow','-Werror']
    if platform.system()=='Darwin':
        sdk=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip()
        args+=['-isysroot',sdk,'-isystem',str(Path(sdk)/'usr/include/c++/v1')]
    args+=shlex.split(flags);commands=[]
    for name in ('lift_match','fiber_export','replay16'):
        cmd=[*args,str(ROOT/(name+'.cpp')),'-o',str(work/name)]
        subprocess.run(cmd,check=True);commands.append(cmd)
    return commands


def native_stage(work,n,parents):
    path=parent_file(work,f'parents{n//2}.txt',parents)
    tick=time.monotonic()
    with (work/f'lift{n}.log').open('w') as log:
        result=json.loads(subprocess.check_output([str(work/'lift_match'),str(path),str(work/f'children{n}.txt')],text=True,stderr=log))
    assert result['complete'] and result['parents']==len(parents)
    out=parse_children(work/f'children{n}.txt',n);assert len(out)==result['children']
    print(json.dumps(result),flush=True)
    return out,result,time.monotonic()-tick


def empty_controls(work):
    cases=[(8,0,0,(1,0,-1,0)),(8,1,1,(0,2,0,-2)),
           (8,0,0,(0,0,0,0)),(8,1,0,(0,0,0,0)),
           (32,0,15,(1,-1)*8),(32,1,15,tuple(2 if j%4==1 else -2 if j%4==3 else 0 for j in range(16)))]
    ip=work/'control-input.txt';op=work/'control-output.txt'
    ip.write_text(str(len(cases))+'\n'+'\n'.join(' '.join(map(str,(n,k,cap,*p))) for n,k,cap,p in cases)+'\n')
    subprocess.run([str(work/'fiber_export'),str(ip),str(op)],check=True)
    counts=[]
    for (n,k,cap,p),line in zip(cases,op.read_text().splitlines(),strict=True):
        data=list(map(int,line.split()));ref,_=audit_fibers.reference(p,k,cap)
        assert data==[len(ref),*ref];counts.append(len(ref))
    assert counts==[0,0,1,1,0,0]
    return dict(cases=len(cases),children=counts)


def main():
    if not __debug__:raise RuntimeError('Run Python without -O.')
    parser=argparse.ArgumentParser();parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--cxx',default='c++');parser.add_argument('--cxxflags',default='')
    args=parser.parse_args();work=args.workdir.resolve()
    if work==ROOT or ROOT in work.parents:raise RuntimeError('Work directory must be outside source package.')
    work.mkdir(parents=True,exist_ok=True);(work/'verified.json').unlink(missing_ok=True)
    started=time.monotonic();commands=compile_sources(work,args.cxx,args.cxxflags)
    audit_fibers.W=work;replay32.W=work
    expected=json.loads((ROOT/'expected.json').read_text());result={};timings={}
    roots={}
    for n in (2,4):
        rows=[cover.rows(n,0,None),cover.rows(n,0,True),cover.rows(n,1,True)]
        qs=cover.match(*rows,n);roots[n]=qs
        result[f'root{n}']={**save_cover(work,f'cover{n}.json',qs),'row_counts':list(map(len,rows))}
    q8,result['native8'],timings['native8']=native_stage(work,8,roots[4])
    result['cover8']=save_cover(work,'cover8.json',q8)
    u8=sorted({quotient.canonical(q) for q in q8});result['quotient8']=save_cover(work,'quotient8.json',u8)
    parent_file(work,'quotient8.txt',u8)
    q16,result['native16'],timings['native16']=native_stage(work,16,u8)
    result['selected_cover16']=save_cover(work,'selected-cover16.json',q16)
    u16=sorted({quotient.canonical(q) for q in q16});result['quotient16']=save_cover(work,'quotient16.json',u16)
    q32,result['native32'],timings['native32']=native_stage(work,32,u16)
    result['cover32']=save_cover(work,'cover32.json',q32);assert not q32
    result['structural']=structural.run(work)
    fa=audit_fibers.main();timings['fiber_audit']=fa['seconds'];result['fiber_audit']=strip_seconds(fa)
    result['empty_controls']=empty_controls(work)
    tick=time.monotonic();independent=[]
    for index,q in enumerate(roots[4]):
        independent.extend(cover.match(*(cover.lifts(row,k) for k,row in enumerate(q)),8))
        if (index+1)%32==0:print('Python length-8 parents',index+1,'of',len(roots[4]),flush=True)
    assert sorted(independent)==q8
    result['independent8']=dict(complete_parents=len(roots[4]),complete_children=len(independent),native_and_python_equal=True,sha256=result['cover8']['sha256'])
    timings['independent8']=time.monotonic()-tick
    tick=time.monotonic()
    ir=json.loads(subprocess.check_output([str(work/'replay16'),str(work/'fiber-input.txt'),str(work/'fiber-output.txt'),str(work/'quotient8.txt'),str(work/'replay16-children.txt')],text=True))
    assert ir['complete'] and parse_children(work/'replay16-children.txt',16)==q16
    result['independent16']={**ir,'complete_lists_equal':True};timings['independent16']=time.monotonic()-tick
    ir=replay32.main();result['independent32']=strip_seconds(ir);timings['independent32']=ir['seconds']
    # JSON normalization also converts integer dictionary keys consistently.
    result=json.loads(json.dumps(result));write_json(work/'result.json',result)
    assert result==expected,'Exact result mismatch; inspect result.json and expected.json.'
    write_json(work/'execution.json',dict(commands=commands,python=platform.python_version(),platform=platform.platform(),
        compiler=subprocess.check_output([args.cxx,'--version'],text=True).splitlines()[0],timings=timings,
        total_seconds=time.monotonic()-started,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(ROOT.iterdir()) if p.suffix in ('.py','.cpp')}))
    final=dict(verified=True,mixed_multiplier=33,final_compressed_states=0,final_sha256=result['cover32']['sha256'],
               earlier_exclusions_replayed=False,affine_corollary_conditional_on_earlier_exclusions=True)
    write_json(work/'verified.json',final);print(json.dumps(final,sort_keys=True),flush=True)


if __name__=='__main__':main()
