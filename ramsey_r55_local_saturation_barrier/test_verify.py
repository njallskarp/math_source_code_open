"""Small exhaustive semantics, path controls and corrupt-certificate rejection."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import audit
import verify


def main():
    checks=0
    for n in range(6):
        pairs=list(combinations(range(n),2))
        for word in range(1<<len(pairs)):
            E={p for i,p in enumerate(pairs) if word>>i&1}
            N=verify.neighbors(n,E);A=[sum(1<<v for v in row) for row in N]
            for size in (3,4,5):
                for color in (False,True):
                    verify.need(verify.counts(n,E,size,color)==audit.clique_count(A if color else audit.complement(A),size),'definition comparison')
                    checks+=1
    paths=[[v for v in range(2,9)],[v for v in range(2,9)]]+[[0,1] for _ in range(7)]
    verify.need(len(audit.certify_paths(paths,0,1))==7,'seven-path positive control')
    paths[0].remove(8);paths[8].remove(0)
    try:audit.certify_paths(paths,0,1)
    except ValueError:pass
    else:raise ValueError('six-path negative control accepted')
    w=json.loads((verify.HERE/'WITNESS.json').read_text())
    bad=[]
    x=deepcopy(w);x['deleted_edges'][1]=x['deleted_edges'][0];bad.append((x,'six deletions'))
    x=deepcopy(w);x['core_adjacency'][0].append(0);bad.append((x,'independent adjacency representation'))
    x=deepcopy(w);x['distant_pair']=[4,6];bad.append((x,'distant pair'))
    x=deepcopy(w);x['distance_three_path']=[4,6,8,5];bad.append((x,'distance-three path'))
    rejected=0
    with tempfile.TemporaryDirectory(prefix='r55-saturation-controls-') as d:
        p=Path(d)/'bad.json'
        for x,reason in bad:
            p.write_text(json.dumps(x))
            proc=subprocess.run([sys.executable,'-B',str(verify.HERE/'verify.py'),'--witness',str(p)],capture_output=True,text=True,timeout=15)
            verify.need(proc.returncode!=0 and reason in proc.stderr,'corrupted witness rejected')
            rejected+=1
    for s in (w['parent_graph6'][:-1],w['parent_graph6'][:-1]+'X','?'+w['parent_graph6'][1:]):
        try:verify.decode(s)
        except ValueError:rejected+=1
        else:raise ValueError('malformed graph6 accepted')
    print(json.dumps({'literal_clique_comparisons':checks,'certificate_corruptions_rejected':rejected,
                      'seven_path_control':True,'six_path_control_rejected':True},sort_keys=True))


if __name__=='__main__':main()
