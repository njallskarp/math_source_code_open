"""Literal definition-level verifier; Python 3.10+, standard library only."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    obj=json.loads(path.read_text())
    need(set(obj)=={'columns','blocked_cross_additions'}, 'certificate keys')
    columns=obj['columns']
    need(isinstance(columns,list) and len(columns)==4, 'four columns required')
    for col in columns:
        need(isinstance(col,list) and all(type(a) is int and 0<=a<17 for a in col), 'column vertices')
        need(col==sorted(set(col)), 'sorted distinct column vertices')
    return obj


def check(path):
    cert=load(path)
    red={e for e in combinations(range(17),2) if (e[1]-e[0])%17 in {1,2,4,8,9,13,15,16}}
    red.update([(17,18),(18,19),(19,20),(17,20)])
    red.update((s,21) for s in range(17,21))
    red.update((a,17+i) for i,col in enumerate(cert['columns']) for a in col)
    need(len(red)==104, '104 red edges required')
    need(all(len(c)==7 for c in cert['columns']), 'four size-seven columns')
    for vertices in combinations(range(22),4):
        need(not set(combinations(vertices,2)) <= red, 'red K4')
    for vertices in combinations(range(22),5):
        need(bool(set(combinations(vertices,2)) & red), 'blue K5')
    missing={(a,s) for a in range(17) for s in range(17,21)}-red
    seen=set()
    for row in cert['blocked_cross_additions']:
        need(set(row)=={'edge','clique'}, 'obstruction keys')
        e=tuple(row['edge']); q=row['clique']
        need(len(e)==2 and all(type(v) is int for v in e), 'edge encoding')
        need(e in missing and e not in seen, 'obstruction coverage')
        need(len(q)==4 and all(type(v) is int and 0<=v<22 for v in q), 'clique vertices')
        need(q==sorted(set(q)) and set(e)<=set(q), 'clique encoding')
        need(set(combinations(q,2))-red=={e}, 'single missing edge of red K4')
        seen.add(e)
    need(seen==missing and len(seen)==40, 'complete forty-edge obstruction certificate')
    # Deliberately do not call the graph red-maximal without its marked core.
    safe=[]
    fours=[set(combinations(q,2)) for q in combinations(range(22),4)]
    for e in combinations(range(22),2):
        if e not in red and not any(es <= red|{e} for es in fours):
            safe.append(list(e))
    need(safe==[[0,21],[2,21],[3,21],[5,21],[9,21],[13,21]], 'unrestricted addition boundary')
    edge_bytes=''.join(f'{u} {v}\n' for u,v in sorted(red)).encode()
    return {'status':'VERIFIED_CROSS_MAXIMAL_PALEY_C4_COUNTEREXAMPLE',
        'vertices':22,'red_edges':104,'column_sizes':[7,7,7,7],
        'degree_histogram':dict(sorted(Counter(sum(v in e for e in red) for v in range(22)).items())),
        'blocked_cross_additions':40, 'safe_unrestricted_additions':safe,
        'edge_sha256':sha256(edge_bytes).hexdigest(),
        'certificate_sha256':sha256(path.read_bytes()).hexdigest()}


if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('certificate.json')
    print(json.dumps(check(path),indent=2,sort_keys=True))
