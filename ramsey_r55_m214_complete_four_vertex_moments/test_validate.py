#!/usr/bin/env python3
"""Definition-level controls for six-edge marginals, transport and parsing."""
import itertools as it
import json
import random
import validate as check
import witness as producer


def require(ok,message):
    if not ok:raise ValueError(message)


def main():
    vertices=(2,9,16,30);pairs=list(it.combinations(vertices,2));rng=random.Random(2143401)
    distributions=[{mask:1} for mask in range(64)]
    for _ in range(128):
        masses=[rng.randrange(8) for _ in range(64)];distributions.append({i:m for i,m in enumerate(masses) if m})
    projections=events=transports=0
    for atoms in distributions:
        _,observed=check.physical_projections(vertices,atoms)
        for triple,dist in observed.items():
            expected=[0]*8
            for mask,mass in atoms.items():
                red={edge for k,edge in enumerate(pairs) if mask&(1<<k)}
                bits=tuple(int(p in red) for p in it.combinations(triple,2));expected[sum(bit*2**i for i,bit in enumerate(bits))]+=mass
            require(dist==tuple(expected),'literal triangle projection');projections+=1
        for i,j in pairs:
            a,b=sorted(set(vertices)-{i,j});expected=0
            for mask,mass in atoms.items():
                red={edge for k,edge in enumerate(pairs) if mask&(1<<k)}
                if (i,j) in red and all(tuple(sorted((v,h))) not in red for v in (a,b) for h in (i,j)):expected+=mass
            require(check.footprint_mass(pairs,atoms,(a,b,i,j))==expected,'literal footprint event');events+=1
        for order in it.permutations(vertices):
            moved=producer.transport(atoms,order,vertices);literal={}
            oldpairs=list(it.combinations(order,2))
            for mask,mass in atoms.items():
                red={frozenset(p) for k,p in enumerate(oldpairs) if mask>>k&1}
                key=sum(2**k for k,p in enumerate(pairs) if frozenset(p) in red);literal[key]=mass
            require(moved==literal,'physical six-edge transport');transports+=1
        D=sum(atoms.values());line='\t'.join(map(str,vertices))+'\t'+'\t'.join(f'{k}:{v}' for k,v in sorted(atoms.items()))+'\n'
        require(check.parse_four_line(line,vertices,D)==atoms,'valid sparse stream')
    malformed=['2 9 16 30 0:1 0:1','2 9 16 30 64:2','2 9 16 30 0:-1 1:3','2 9 16 30 0:0 1:2','2 9 16 30 0:1','2 9 16 31 0:2','2 9 16 30 1:1 0:1','2 9 16 30 0:2:3','2 9 16 30','']
    rejected=0
    for line in malformed:
        try:check.parse_four_line(line,vertices,2)
        except ValueError:rejected+=1
        else:raise ValueError('accepted damaged stream')
    # Complete truth table for the projected separator inequality.
    for mask in range(64):
        atoms={mask:1};_,dist=check.physical_projections(vertices,atoms)
        for i,j in pairs:
            a,b=sorted(set(vertices)-{i,j});q=check.footprint_mass(pairs,atoms,(a,b,i,j))
            bounds=[]
            for v in (a,b):
                tri=tuple(sorted((v,i,j)));bit=list(it.combinations(tri,2)).index((i,j));bounds.append(dist[tri][1<<bit])
            edge=(mask>>pairs.index((i,j)))&1
            require(max(0,sum(bounds)-edge)<=q<=min(bounds),'projected Frechet truth table')
    print(json.dumps({'status':'PASS','distributions':len(distributions),'triangle_projections':projections,'footprint_events':events,'transports':transports,'separator_boolean_instances':384,'malformed_streams_rejected':rejected},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
