#!/usr/bin/env python3
"""Independent physical edge-set decoder and full invariant-basis action check.

Imports no target checker, decomposition or producer. Matrix positivity is
proved by exact actions on a complete independent basis, with positive
rank-one decompositions of the small coefficient blocks.
"""
import argparse,hashlib,json,math
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement,permutations
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def decode(path):
    raw=json.loads(path.read_text());D=raw['denominator'];cells=raw['cells']
    require(type(D)==int and D>0,'positive integer denominator')
    require(sorted(sum(cells,[]))==list(range(43)),'vertex partition')
    cls={v:t for t,cell in enumerate(cells) for v in cell};pairs=list(combinations(range(4),2));tables={}
    for record in raw['four_tables']:
        types=tuple(record['types']);require(types not in tables,'unique table');distribution={}
        for text,mass in record['orbits'].items():
            require(type(mass)==int and 0<mass<=D,'positive mass')
            edges=frozenset(e for j,e in enumerate(pairs) if int(text)&(1<<j))
            orbit=set()
            for permutation in permutations(range(4)):
                if any(types[j]!=types[permutation[j]] for j in range(4)):continue
                orbit.add(frozenset(tuple(sorted((permutation[u],permutation[v]))) for u,v in edges))
            require(not(set(distribution)&orbit),'disjoint orbits')
            distribution.update({e:mass for e in orbit})
        require(sum(distribution.values())==D,'normalized edge-set distribution');tables[types]=distribution
    expected={ts for ts in combinations_with_replacement(range(len(cells)),4) if all(ts.count(t)<=len(cells[t]) for t in ts)}
    require(set(tables)==expected,'complete feasible table support')
    cache={}
    def red_event(vertices,edges):
        vertices=set(vertices)
        for v in range(43):
            if len(vertices)==4:break
            vertices.add(v)
        ordered=sorted(vertices,key=lambda v:(cls[v],v));types=tuple(cls[v] for v in ordered)
        required=frozenset(tuple(sorted((ordered.index(u),ordered.index(v)))) for u,v in edges)
        key=(types,required)
        if key not in cache:cache[key]=sum(m for e,m in tables[types].items() if required<=e)
        return cache[key]
    return D,cells,red_event


def positive_rank(matrix):
    """Subtract positive rank-one columns; verify the full sum explicitly."""
    n=len(matrix);a=[[F(x) for x in row] for row in matrix];original=[r[:] for r in a];factors=[]
    require(all(len(r)==n for r in a),'square coefficient block')
    require(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)),'symmetric coefficient block')
    while any(x for row in a for x in row):
        require(all(a[i][i]>=0 for i in range(n)),'negative diagonal residual')
        pivots=[i for i in range(n) if a[i][i]>0]
        require(pivots,'nonzero residual with zero diagonal');k=pivots[0];d=a[k][k];c=[r[k] for r in a]
        factors.append((c,d))
        for i in range(n):
            for j in range(n):a[i][j]-=c[i]*c[j]/d
    require(all(original[i][j]==sum(c[i]*c[j]/d for c,d in factors) for i in range(n) for j in range(n)),'explicit positive factor sum')
    return len(factors)


def kernel_basis(rows):
    a=[[F(x) for x in r] for r in rows];n=len(a);m=len(a[0]);pivots=[];r=0
    for j in range(m):
        found=next((k for k in range(r,n) if a[k][j]),None)
        if found is None:continue
        a[r],a[found]=a[found],a[r];pivot=a[r][j];a[r]=[x/pivot for x in a[r]]
        for k in range(n):
            if k!=r:
                c=a[k][j];a[k]=[x-c*y for x,y in zip(a[k],a[r])]
        pivots.append(j);r+=1
        if r==n:break
    free=[j for j in range(m) if j not in pivots];basis=[]
    for j in free:
        v={j:F(1)}
        for k,pivot in enumerate(pivots):
            if a[k][j]:v[pivot]=-a[k][j]
        scale=math.lcm(*(x.denominator for x in v.values()));v={k:int(x*scale) for k,x in v.items()}
        require(all(sum(row[k]*x for k,x in v.items())==0 for row in rows),'literal incidence kernel')
        require(v[j]==scale and all(k==j or k not in free for k in v),'free-coordinate independence')
        basis.append(v)
    return pivots,basis


def check_basis(cells,edges,matrix):
    flat=sum(cells,[]);require(sorted(flat)==list(range(len(flat))) and all(cells),'complete cell partition')
    require(edges==[()]+list(combinations(range(len(flat)),2)),'complete coordinate roster')
    n=len(edges);require(len(matrix)==n and all(len(row)==n for row in matrix),'full square matrix')
    require(all(matrix[i][j]==matrix[j][i] for i in range(n) for j in range(n)),'full matrix symmetry')
    lookup={e:i for i,e in enumerate(edges)};cls={v:i for i,c in enumerate(cells) for v in c}
    groups={}
    for index,e in enumerate(edges):groups.setdefault(tuple(sorted(cls[v] for v in e)),[]).append(index)
    keys=list(groups);key_index={k:i for i,k in enumerate(keys)};orbit=[tuple(sorted(cls[v] for v in e)) for e in edges]
    basis=[];checks=0;rank=0
    def add(family,vector):basis.append((family,vector))
    def action(vector):return [sum(row[j]*c for j,c in vector.items()) for row in matrix]
    # Cell-constant basis, including the physical constant coordinate.
    B=[];images=[]
    for o in keys:
        vec={j:1 for j in groups[o]};im=action(vec);images.append(im);add(('constant',),vec)
        B.append([sum(im[j] for j in groups[p]) for p in keys])
    for k,o in enumerate(keys):
        for j,p in enumerate(orbit):require(images[k][j]*len(groups[p])==B[k][key_index[p]],'constant-basis action');checks+=1
    r0=positive_rank(B);rank+=r0
    standard_records=[]
    # All vertex differences, not only one representative, are checked.
    for i,cell in enumerate(cells):
        ni=len(cell)
        if ni<2:continue
        labels=[j for j in range(len(cells)) if j!=i or ni>=3]
        scales={j:(ni-2 if j==i else len(cells[j])) for j in labels}
        vectors={};images={}
        for t,b in enumerate(cell[1:],1):
            a=cell[0]
            for j in labels:
                v=Counter()
                for u,sgn in ((a,1),(b,-1)):
                    for w in cells[j]:
                        if w!=u:v[lookup[tuple(sorted((u,w)))]]+=sgn
                v={e:c for e,c in v.items() if c};vectors[t,j]=v;images[t,j]=action(v);add(('standard',i),v)
        B={}
        for j in labels:
            for k in labels:
                twice=sum(c*images[1,j][e] for e,c in vectors[1,k].items())
                require(twice%2==0,'standard coefficient parity');B[k,j]=twice//2
        for (t,j),im in images.items():
            for e in range(n):
                terms=[(k,vectors[t,k].get(e,0)) for k in labels if vectors[t,k].get(e,0)]
                require(len(terms)<=1,'disjoint standard copies')
                if terms:
                    k,c=terms[0];require(im[e]*scales[k]==B[k,j]*c,'every standard-basis action')
                else:require(im[e]==0,'zero standard-basis action')
                checks+=1
        r=positive_rank([[B[j,k] for k in labels] for j in labels]);rank+=(ni-1)*r
        standard_records.append({'cell':i,'block_rank':r,'multiplicity':ni-1})
    residual=[]
    def scalar_family(family,vectors):
        nonlocal checks,rank
        require(bool(vectors),'nonempty residual family')
        first=vectors[0];im=action(first);pivot=next(iter(first));lam=F(im[pivot],first[pivot]);require(lam>=0,'negative residual eigenvalue')
        for v in vectors:
            im=action(v);add(family,v)
            for j,x in enumerate(im):require(x==lam*v.get(j,0),'every residual-basis action');checks+=1
        if lam>0:rank+=len(vectors)
        residual.append((family,len(vectors),lam))
    for i,cell in enumerate(cells):
        if len(cell)<4:continue
        es=list(combinations(cell,2));rows=[[int(u in e) for e in es] for u in cell];pivots,local=kernel_basis(rows)
        require(len(pivots)==len(cell) and len(local)==len(cell)*(len(cell)-3)//2,'full internal incidence kernel')
        vectors=[{lookup[es[j]]:c for j,c in v.items()} for v in local];scalar_family(('internal',i),vectors)
    for i,j in combinations(range(len(cells)),2):
        if min(len(cells[i]),len(cells[j]))<2:continue
        a=cells[i][0];b=cells[j][0];vectors=[]
        for u in cells[i][1:]:
            for v in cells[j][1:]:
                vector={lookup[tuple(sorted(e))]:c for e,c in (((a,b),1),((a,v),-1),((u,b),-1),((u,v),1))}
                vectors.append(vector)
        scalar_family(('tensor',i,j),vectors)
    # Distinct families are orthogonal. Within each, the displayed independent
    # bases (indicators, vertex differences, free-coordinate kernels, rectangles)
    # have their proved full dimension. Hence these 904 vectors span.
    require(len(basis)==n,'complete basis dimension');orthogonal=0
    for a,(family,v) in enumerate(basis):
        for other,w in basis[a+1:]:
            if family==other:continue
            if len(v)>len(w):small,large=w,v
            else:small,large=v,w
            require(sum(c*large.get(j,0) for j,c in small.items())==0,'different basis families orthogonal');orthogonal+=1
    require(checks==n*n,'every basis image coordinate')
    return {'order':n,'rank':rank,'basis_vectors':len(basis),'basis_image_coordinates':checks,
            'cross_family_orthogonality_checks':orthogonal,'trivial_rank':r0,'standard_blocks':standard_records,
            'residual_dimensions':[{'family':f,'dimension':d,'positive':lam>0} for f,d,lam in residual]}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path);a=p.parse_args();D,cells,event=decode(a.certificate)
    edges=[()]+list(combinations(range(43),2));matrix=[]
    for e in edges:
        row=[]
        for f in edges:
            row.append(D if not e and not f else event(e+f,tuple(z for z in (e,f) if z)))
        matrix.append(row)
    require(all(matrix[i][j]==matrix[j][i] for i in range(904) for j in range(904)),'physical matrix symmetry')
    result=check_basis(cells,edges,matrix)
    digest=hashlib.sha256(f'904 {D}\n'.encode())
    for row in matrix:digest.update((' '.join(map(str,row))+'\n').encode())
    result['matrix_sha256']=digest.hexdigest()
    weighted=[(tuple(sorted((29,u))),2) for u in range(2,15)]+[((2,8),1)]
    first=sum(c*event(e,(e,)) for e,c in weighted);second=sum(c*d*event(e+f,(e,f)) for e,c in weighted for f,d in weighted)
    square=second-28*first+196*D;require(square>=0,'mixed square repaired independently')
    result.update(status='INDEPENDENT_FULL_GLOBAL_PSD_BASIS_PASS',physical_entries=904**2,certificate_sha256=hashlib.sha256(a.certificate.read_bytes()).hexdigest(),former_mixed_square=str(F(square,D)))
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
