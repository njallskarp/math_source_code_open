"""Small literal controls, complete set comparison, and scope mutations."""
import copy
from itertools import combinations
import json
from pathlib import Path
import audit
import derive


def literal_clique(red,n,k,color=True):
    return any(all((e in red)==color for e in combinations(q,2)) for q in combinations(range(n),k))


def ramsey(red,n):
    return not literal_clique(red,n,4) and not literal_clique(red,n,5,False)


def main():
    directory=Path(__file__).parent;inputs=json.loads((directory/'inputs.json').read_text())
    cert=json.loads((directory/'certificate.json').read_text())
    left=derive.calculate(inputs);right=audit.calculate(inputs,cert)
    if left!=right:raise ValueError('complete entry-level sets disagree')
    small_graphs=domain_checks=clique_checks=0
    for n in range(6):
        pairs=list(combinations(range(n),2))
        for word in range(1<<len(pairs)):
            red={e for i,e in enumerate(pairs) if word>>i&1}
            matrix=[[tuple(sorted((u,v))) in red for v in range(n)] for u in range(n)]
            rows=[sum(1<<v for v in range(n) if matrix[u][v]) for u in range(n)]
            a=derive.domains(rows);b=audit.domains(matrix)
            direct=[]
            for mask in range(1<<n):
                vertices=[v for v in range(n) if mask>>v&1]
                if not any(all(e in red for e in combinations(q,2)) for q in combinations(vertices,3)):direct.append(mask)
            maximal=sorted(x for x in direct if all(x>>v&1 or x|1<<v not in direct for v in range(n)))
            if a!=b or a!=(len(direct),maximal):raise ValueError('domain controls')
            domain_checks+=1;small_graphs+=1
            if derive.graph_counts(n,sorted(red))!=audit.graph_counts(n,sorted(red)):raise ValueError('graph clique counters')
            for k in [3,4]:
                expected=sum(all(e in red for e in combinations(q,2)) for q in combinations(range(n),k))
                if derive.graph_counts(n,sorted(red))[k]!=expected:raise ValueError('literal clique count')
                clique_checks+=1
    # Every possible cross-assignment for all cores n<=3 and independent
    # outside sets k<=4. This checks the sound local saturation transport,
    # allowing repeated maximal columns in small cases where loops exist.
    physical=saturated=0
    for n in range(4):
        pairs=list(combinations(range(n),2))
        for word in range(1<<len(pairs)):
            core={e for i,e in enumerate(pairs) if word>>i&1}
            rows=[sum(1<<v for v in range(n) if tuple(sorted((u,v))) in core) for u in range(n)]
            _,maximal=derive.domains(rows)
            for k in range(5):
                cross=[(a,n+s) for s in range(k) for a in range(n)]
                for assignment in range(1<<len(cross)):
                    red=core|{e for i,e in enumerate(cross) if assignment>>i&1};physical+=1
                    if not ramsey(red,n+k):continue
                    enlarged=set(red)
                    for s in range(k):
                        column=sum(1<<a for a in range(n) if (a,n+s) in red)
                        extension=next(x for x in maximal if column&x==column)
                        enlarged.update((a,n+s) for a in range(n) if extension>>a&1)
                    if not ramsey(enlarged,n+k):raise ValueError('local saturation failed')
                    saturated+=1
    bad_certs=[]
    x=copy.deepcopy(cert);x['maximal_columns'].pop();bad_certs.append(x)
    x=copy.deepcopy(cert);x['maximal_columns'].append(x['maximal_columns'][0]);bad_certs.append(x)
    x=copy.deepcopy(cert);x['compatibility_clique_counts'][4]=1;bad_certs.append(x)
    x=copy.deepcopy(cert);x['pair_graph_sha256']='0'*64;bad_certs.append(x)
    for x in bad_certs:
        try:audit.calculate(inputs,x)
        except ValueError:pass
        else:raise ValueError('damaged certificate accepted')
    bad_inputs=[]
    x=copy.deepcopy(inputs);x['interfaces'].pop();bad_inputs.append(x)
    x=copy.deepcopy(inputs);x['interfaces'][1]=x['interfaces'][0];bad_inputs.append(x)
    x=copy.deepcopy(inputs);x['r44_17']['catalogue_to_paley'][0]=1;bad_inputs.append(x)
    x=copy.deepcopy(inputs);x['local_survivors'][0]['columns'][0]=[];bad_inputs.append(x)
    for x in bad_inputs:
        for check in [derive.consumer,audit.consumer]:
            try:check(x)
            except ValueError:pass
            else:raise ValueError('scope mutation accepted')
    rec=inputs['interfaces'][0]
    bad_g6=['','!',rec[:-1],rec+'?',rec[:-1]+chr(ord(rec[-1])+1)]
    for x in bad_g6:
        for decoder in [derive.graph6,audit.decode]:
            try:decoder(x)
            except ValueError:pass
            else:raise ValueError('bad graph6 accepted')
    print(json.dumps({'status':'INDEPENDENT_COLUMN_AND_TRANSPORT_CONTROLS_PASS',
        'complete_columns_compared':len(cert['maximal_columns']),
        'complete_pairs_compared':len(left[2]),'small_graphs':small_graphs,
        'literal_domain_comparisons':domain_checks,'literal_clique_counts':clique_checks,
        'physical_extension_assignments':physical,'valid_saturated_extensions':saturated,
        'certificate_mutations_rejected':len(bad_certs),
        'scope_mutations_rejected_by_both':len(bad_inputs),
        'malformed_graph6_rejected_by_both':len(bad_g6)},indent=2,sort_keys=True))


if __name__=='__main__':main()
