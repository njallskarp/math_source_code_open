"""Independent structural verifier; imports no producer or literal checker.

Proves the Ramsey property from the Paley core and the three complete classes
of mixed forbidden-set constraints. Uses bit rows and recursive clique search.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys


def clique(rows, candidates, size):
    if size==0:
        return True
    while candidates.bit_count()>=size:
        bit=candidates & -candidates
        candidates^=bit
        v=bit.bit_length()-1
        if clique(rows,candidates & rows[v],size-1):
            return True
    return False


def audit(path):
    data=path.read_bytes()
    cert=json.loads(data)
    if sorted(cert)!=['blocked_cross_additions','columns']:
        raise ValueError('schema')
    columns=cert['columns']
    if type(columns) is not list or len(columns)!=4:
        raise ValueError('column count')
    masks=[]
    for col in columns:
        if type(col) is not list or len(col)!=7:
            raise ValueError('column size')
        mask=0
        for v in col:
            if type(v) is not int or not 0<=v<17 or mask>>v&1:
                raise ValueError('column member')
            mask |= 1<<v
        if col != sorted(col):
            raise ValueError('column order')
        masks.append(mask)
    universe=(1<<17)-1
    residues={x*x%17 for x in range(1,17)}
    rows=[sum(1<<v for v in range(17) if (v-u)%17 in residues) for u in range(17)]
    blue=[universe ^ (1<<u) ^ rows[u] for u in range(17)]
    if clique(rows,universe,4) or clique(blue,universe,4):
        raise ValueError('Paley Ramsey core')
    for i in range(4):
        if clique(rows,masks[i],3):
            raise ValueError('one S vertex plus red A triangle')
        if clique(rows,masks[i]&masks[(i+1)%4],2):
            raise ValueError('adjacent S pair plus red A edge')
    for i in range(2):
        if clique(blue,universe ^ (masks[i]|masks[i+2]),3):
            raise ValueError('opposite S pair plus blue A triangle')
    full=rows+[0]*5
    for i,mask in enumerate(masks):
        s=17+i
        full[s]=mask | (1<<21) | (1<<(17+(i+1)%4)) | (1<<(17+(i-1)%4))
        for a in range(17):
            if mask>>a&1:
                full[a] |= 1<<s
    full[21]=sum(1<<v for v in range(17,21))
    # A missing edge uv creates a red K4 iff the common neighborhood has an edge.
    missing=[(a,17+i) for i,m in enumerate(masks) for a in range(17) if not m>>a&1]
    if any(not clique(full,full[u]&full[v],2) for u,v in missing):
        raise ValueError('cross addition still possible')
    certificates={}
    for row in cert['blocked_cross_additions']:
        if set(row)!={'edge','clique'}:
            raise ValueError('obstruction schema')
        e=tuple(row['edge']);q=row['clique']
        if len(e)!=2 or any(type(v) is not int for v in e) or e in certificates:
            raise ValueError('obstruction edge')
        if len(q)!=4 or any(type(v) is not int or not 0<=v<22 for v in q) or q!=sorted(set(q)):
            raise ValueError('obstruction clique')
        absent=[]
        for u in q:
            for v in q:
                if u<v and not full[u]>>v&1:
                    absent.append((u,v))
        if absent!=[e]:
            raise ValueError('obstruction does not prove K4')
        certificates[e]=q
    if set(certificates)!=set(missing) or len(missing)!=40:
        raise ValueError('incomplete obstruction list')
    safe=[[u,v] for u in range(22) for v in range(u+1,22)
          if not full[u]>>v&1 and not clique(full,full[u]&full[v],2)]
    if safe!=[[0,21],[2,21],[3,21],[5,21],[9,21],[13,21]]:
        raise ValueError('unrestricted boundary')
    edges=[(u,v) for u in range(22) for v in range(u+1,22) if full[u]>>v&1]
    if len(edges)!=104:
        raise ValueError('edge count')
    edge_bytes=''.join(f'{u} {v}\n' for u,v in edges).encode()
    return {'status':'VERIFIED_CROSS_MAXIMAL_PALEY_C4_COUNTEREXAMPLE',
        'vertices':22,'red_edges':104,'column_sizes':[7,7,7,7],
        'degree_histogram':dict(sorted(Counter(row.bit_count() for row in full).items())),
        'blocked_cross_additions':len(missing),'safe_unrestricted_additions':safe,
        'edge_sha256':sha256(edge_bytes).hexdigest(),
        'certificate_sha256':sha256(data).hexdigest()}


if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('certificate.json')
    print(json.dumps(audit(path),indent=2,sort_keys=True))
