"""Definition-level finite controls and damaged-certificate rejection."""
from itertools import combinations
from copy import deepcopy
import json
from pathlib import Path
import audit

def independent(matrix,vertices):
    return all(not matrix[u][v] for u,v in combinations(vertices,2))

def reduced(P,S,columns):
    n=len(P);m=len(S)
    if any(all(S[u][v] for u,v in combinations(q,2)) for q in combinations(range(m),3)):return False
    for X in columns:
        if any(all(P[u][v] for u,v in combinations(q,2)) for q in combinations(X,3)):return False
    for i,j in combinations(range(m),2):
        if S[i][j]:
            if not independent(P,sorted(columns[i]&columns[j])):return False
        else:
            missed=[v for v in range(n) if v not in columns[i]|columns[j]]
            if any(independent(P,q) for q in combinations(missed,3)):return False
    for i,j,k in combinations(range(m),3):
        if independent(S,[i,j,k]):
            missed=[v for v in range(n) if v not in columns[i]|columns[j]|columns[k]]
            if not all(P[u][v] for u,v in combinations(missed,2)):return False
    return True

def matrix(n,mask):
    A=[[False]*n for _ in range(n)]
    for i,(u,v) in enumerate(combinations(range(n),2)):A[u][v]=A[v][u]=bool(mask>>i&1)
    return A

def controls():
    count=valid=0
    for n in range(4):
        for m in range(4):
            for a in range(1<<(n*(n-1)//2)):
                P=matrix(n,a)
                for b in range(1<<(m*(m-1)//2)):
                    S=matrix(m,b)
                    for cross in range(1<<(n*m)):
                        columns=[{v for v in range(n) if cross>>(s*n+v)&1} for s in range(m)]
                        A=[[False]*(n+m+1) for _ in range(n+m+1)]
                        for u,v in combinations(range(n),2):A[u][v]=A[v][u]=P[u][v]
                        for u,v in combinations(range(m),2):A[n+u][n+v]=A[n+v][n+u]=S[u][v]
                        for s,X in enumerate(columns):
                            A[n+s][n+m]=A[n+m][n+s]=True
                            for v in X:A[v][n+s]=A[n+s][v]=True
                        forbidden=any(all(A[u][v] for u,v in combinations(q,2)) for q in combinations(range(n+m+1),4))
                        forbidden|=any(independent(A,q) for q in combinations(range(n+m+1),5))
                        got=reduced(P,S,columns)
                        audit.require(got== (not forbidden),'physical reduction mismatch')
                        count+=1;valid+=got
    return count,valid

def main():
    directory=Path(__file__).parent;certificate=json.loads((directory/'certificate.json').read_text())
    changes=[]
    c=deepcopy(certificate);c['families'][0]['representatives'].pop();changes.append(c)
    c=deepcopy(certificate);c['families'][0]['representatives'][0]['columns'][0]^=1;changes.append(c)
    c=deepcopy(certificate);c['families'][1]['representatives'][0]['orbit_size']-=1;changes.append(c)
    c=deepcopy(certificate);c['families'][1]['full_tuple_sha256']='0'*64;changes.append(c)
    for c in changes:
        try:audit.check_certificate(c)
        except ValueError:pass
        else:raise ValueError('damaged certificate accepted')
    inputs=json.loads((directory/'inputs.json').read_text())
    damaged=deepcopy(inputs);damaged['interfaces'].pop()
    try:audit.consumer(damaged,certificate)
    except ValueError:pass
    else:raise ValueError('missing interface accepted')
    for bad in ['', 'U', '?@', '\n', '~~~']:
        try:audit.graph6(bad)
        except ValueError:pass
        else:raise ValueError('malformed graph6 accepted')
    total,valid=controls()
    print(json.dumps({'status':'DENSE_HUB_DEFINITION_CONTROLS_PASS','physical_assignments':total,
                     'valid_local_graphs':valid,'certificate_mutations_rejected':len(changes),
                     'missing_interface_rejected':True,'malformed_graph6_rejected':5},indent=2,sort_keys=True))

if __name__=='__main__':main()
