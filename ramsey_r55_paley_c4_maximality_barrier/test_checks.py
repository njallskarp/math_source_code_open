"""Definition-level controls for recursive clique and edge-addition checks."""
import copy
from itertools import combinations
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import audit
import verify


def literal(red, n, k):
    return any(set(combinations(q,2))<=red for q in combinations(range(n),k))


def main():
    graphs=clique_checks=addition_checks=0
    for n in range(6):
        pairs=list(combinations(range(n),2))
        for bits in range(1<<len(pairs)):
            red={e for i,e in enumerate(pairs) if bits>>i&1}
            rows=[sum(1<<v for v in range(n) if tuple(sorted((u,v))) in red) for u in range(n)]
            graphs+=1
            for k in range(2,6):
                if audit.clique(rows,(1<<n)-1,k)!=literal(red,n,k):
                    raise ValueError('clique engine mismatch')
                clique_checks+=1
            if not literal(red,n,4):
                for u,v in pairs:
                    if (u,v) not in red:
                        expected=literal(red|{(u,v)},n,4)
                        actual=audit.clique(rows,rows[u]&rows[v],2)
                        if actual!=expected:
                            raise ValueError('edge-addition characterization mismatch')
                        addition_checks+=1
    cert_path=Path(__file__).with_name('certificate.json')
    cert=json.loads(cert_path.read_text())
    if verify.check(cert_path)!=audit.audit(cert_path):
        raise ValueError('independent witness results disagree')
    bad=[]
    x=copy.deepcopy(cert);x['columns'][0][0]=False;bad.append(x)
    x=copy.deepcopy(cert);x['columns'][0][0]=17;bad.append(x)
    x=copy.deepcopy(cert);x['columns'][0][1]=x['columns'][0][0];bad.append(x)
    x=copy.deepcopy(cert);x['columns'][0].reverse();bad.append(x)
    x=copy.deepcopy(cert);x['columns'].pop();bad.append(x)
    x=copy.deepcopy(cert);x['blocked_cross_additions'].pop();bad.append(x)
    x=copy.deepcopy(cert);x['blocked_cross_additions'].append(x['blocked_cross_additions'][0]);bad.append(x)
    x=copy.deepcopy(cert);x['blocked_cross_additions'][0]['clique']=[0,1,2,3];bad.append(x)
    x=copy.deepcopy(cert);x['blocked_cross_additions'][0]['edge']=[0,1];bad.append(x)
    x=copy.deepcopy(cert);x['unexpected']=True;bad.append(x)
    rejected=0
    with TemporaryDirectory() as temp:
        path=Path(temp)/'bad.json'
        for obj in bad:
            path.write_text(json.dumps(obj))
            for checker in (verify.check,audit.audit):
                try:
                    checker(path)
                except ValueError:
                    rejected+=1
                else:
                    raise ValueError('malformed certificate accepted')
    print(json.dumps({'status':'CHECKER_CONTROLS_PASS','small_graphs':graphs,
        'literal_clique_comparisons':clique_checks,
        'literal_edge_addition_comparisons':addition_checks,
        'malformed_certificates_rejected_by_both':len(bad),
        'individual_rejections':rejected},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
