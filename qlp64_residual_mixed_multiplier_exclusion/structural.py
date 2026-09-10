"""Direct Gaussian root checks and witnesses for the quotient maps."""
from functools import lru_cache
from itertools import product
import json
import quotient


@lru_cache(None)
def paf(row):
    n=len(row)
    return tuple(sum(row[j]*row[(j+k)%n] for j in range(n)) for k in range(n))


def gaussian_imaginary(r,s):
    n=len(r);x=[a+b for a,b in zip(s,r)];y=[a-b for a,b in zip(s,r)]
    return tuple(sum(y[j]*x[(j+k)%n]-x[j]*y[(j+k)%n] for j in range(n)) for k in range(n))


def valid(q):
    p,r,s=q;n=len(p);bound=32//n
    assert list(map(sum,q))==[0,0,1]
    assert all(abs(v)<=bound for row in q for v in row)
    assert all((v-bound)%2==0 for row in (r,s) for v in row[1::2])
    assert all(2*a+b+c==(65-64//n if k==0 else -64//n)
               for k,(a,b,c) in enumerate(zip(paf(p),paf(r),paf(s))))
    assert not any(gaussian_imaginary(r,s))


def direct_roots(expected):
    rows=[[],[],[]]
    for row in product(range(-8,9),repeat=4):
        energy=sum(v*v for v in row);total=sum(row)
        if total==0 and energy<=24:rows[0].append(row)
        if energy<=49 and all(v%2==0 for v in row[1::2]):
            if total==0:rows[1].append(row)
            if total==1:rows[2].append(row)
    found=[]
    for p,r,s in product(*rows):
        a,b,c=paf(p),paf(r),paf(s)
        if 2*a[0]+b[0]+c[0]!=49:continue
        if any(2*a[k]+b[k]+c[k]!=-16 for k in (1,2,3)):continue
        if any(gaussian_imaginary(r,s)):continue
        found.append((p,r,s))
    assert sorted(found)==expected
    return dict(row_counts=list(map(len,rows)),direct_triples=len(found))


@lru_cache(None)
def p_images(p,h):
    n=len(p)
    return frozenset(tuple(sign*p[(h*eps*j+b)%n] for j in range(n))
                     for eps in (1,-1) for sign in (1,-1) for b in range(n))


def related(q,target):
    p,r,s=q;n=len(p)
    for h in range(1,n,2):
        if target[0] not in p_images(p,h):continue
        for eps,sign,b in product((1,-1),(1,-1),range(0,n,2)):
            rr=tuple(sign*r[(h*eps*j+b)%n] for j in range(n))
            if rr!=target[1]:continue
            ss=tuple(s[(h*eps*j+b)%n] for j in range(n))
            if ss==target[2]:return True
    return False


def actions(q):
    p,r,s=q;n=len(p)
    def perm(row,h,b):return tuple(row[(h*j+b)%n] for j in range(n))
    return [(perm(p,1,1),r,s),(tuple(-v for v in p),r,s),(perm(p,-1,0),r,s),
            (p,perm(r,1,2),perm(s,1,2)),(p,tuple(-v for v in r),s),
            (p,perm(r,-1,0),perm(s,-1,0)),tuple(perm(row,3,0) for row in q)]


def fold(q):
    d=len(q[0])//2
    return tuple(tuple(row[j]+row[j+d] for j in range(d)) for row in q)


def halfperiod_control():
    # A single row: no companion pair is claimed. It refutes transferring the
    # ordinary half-period positivity lemma to a conjugating action.
    codes=(0,1,0,1,0,1,2,3,2,3,0,3,2,3,2,1)
    real=(1,0,-1,0);imag=(0,1,0,-1)
    assert sum(real[z] for z in codes)==sum(imag[z] for z in codes)==0
    assert all(codes[9*j%16]==(-codes[j])%4 for j in range(16))
    correlations=[]
    for k in range(16):
        ds=[(codes[j]-codes[(j+k)%16])%4 for j in range(16)]
        assert sum(imag[z] for z in ds)==0
        correlations.append(sum(real[z] for z in ds))
    assert correlations[8]==-8
    return dict(length=16,codes=list(codes),all_correlations=correlations)


def run(work):
    def read(name):return [tuple(tuple(r) for r in q) for q in json.loads((work/name).read_text())]
    roots=read('cover4.json');result=dict(roots=direct_roots(roots))
    checks=[]
    for n,file in ((8,'cover8.json'),(16,'selected-cover16.json')):
        source=read(file);representatives=set(read(f'quotient{n}.json'))
        for q in source:
            valid(q);c=quotient.canonical(q)
            assert c in representatives and related(q,c)
        assert {quotient.canonical(q) for q in source}==representatives
        checks.append(dict(length=n,tuples=len(source),valid_orbit_images=len(source),representatives=len(representatives)))
    transformations=0
    for q in read('quotient8.json'):
        for transformed,folded_transformed in zip(actions(q),actions(fold(q))):
            valid(transformed);assert fold(transformed)==folded_transformed;transformations+=1
    result.update(quotients=checks,generator_and_folding_checks=transformations,
                  halfperiod_negative_control=halfperiod_control())
    return result
