"""Exact definition-level checker; no solver or catalog is needed at replay."""
from __future__ import annotations

import base64
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = {18:85,19:92,20:100,21:107,22:114,23:122,24:132}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode_graph6(encoded):
    raw = base64.b64decode(encoded, validate=True)
    require(bool(raw), 'empty graph6')
    n = raw[0]-63
    require(0 <= n <= 62, 'graph6 small order')
    bit_count = n*(n-1)//2
    require(len(raw) == 1+(bit_count+5)//6, 'graph6 length')
    bits = []
    for value in raw[1:]:
        require(63 <= value <= 126, 'graph6 alphabet')
        bits.extend(((value-63) >> k) & 1 for k in range(5,-1,-1))
    require(not any(bits[bit_count:]), 'nonzero graph6 padding')
    edges = set()
    index = 0
    for right in range(1,n):
        for left in range(right):
            if bits[index]:
                edges.add((left,right))
            index += 1
    return n,edges


def construct(data):
    require(data['format']=='r55-d22-two-anchor-v1', 'witness format')
    require(data['anchors']==[0,3], 'anchor labels')
    n,h = decode_graph6(data['red_core_parent_graph6_base64'])
    require(n==22 and len(h)==114, 'red core parent')
    for raw_edge in data['red_core_delete_edges']:
        e=tuple(raw_edge)
        require(e in h, 'deletion exists exactly once')
        h.remove(e)
    n,j = decode_graph6(data['blue_core_graph6_base64'])
    require(n==20 and len(j)==100, 'blue core')
    rows=data['cross_rows']
    require(len(rows)==22 and all(len(row)==20 and set(row)<={'0','1'} for row in rows), 'cross matrix format')
    red={(0,x) for x in range(1,23)}
    red.update((a+1,b+1) for a,b in h)
    red.update((a+23,b+23) for a,b in combinations(range(20),2) if (a,b) not in j)
    red.update((i+1,j+23) for i,row in enumerate(rows) for j,bit in enumerate(row) if bit=='1')
    return red


def audit(red, data):
    require(all(type(a) is int and type(b) is int and 0<=a<b<43 for a,b in red), 'simple canonical edges')
    adj=[[False]*43 for _ in range(43)]
    for a,b in red:
        adj[a][b]=adj[b][a]=True
    degrees=[sum(row) for row in adj]
    require(Counter(degrees)==Counter({20:8,21:26,22:9}), 'exact red degree profile')
    require(degrees[0]==22 and set(x for x in range(43) if adj[0][x])==set(range(1,23)), 'anchor split')
    require(adj[0][3], 'red root edge')
    common=[x for x in range(43) if adj[0][x] and adj[3][x]]
    require(len(common)>=10, 'eligible high partner')
    local=[]
    neighborhoods={}
    for root in (0,3):
        for color in (True,False):
            vs=[x for x in range(43) if x!=root and adj[root][x]==color]
            neighborhoods[(root,color)]=set(vs)
            e=sum(adj[a][b]==color for a,b in combinations(vs,2))
            for size,target in ((4,color),(5,not color)):
                require(not any(all(adj[a][b]==target for a,b in combinations(s,2)) for s in combinations(vs,size)), f'forbidden set in root {root} color {color}')
            local.append((root,'R' if color else 'B',len(vs),e,U[len(vs)]-e))
    require(local[0]==(0,'R',22,108,6), 'd22 deficiency six')
    signatures={x:(int(adj[0][x]),int(adj[3][x])) for x in range(43) if x not in (0,3)}
    cells=Counter(signatures.values())
    diagonal=[]
    for a,b in combinations(signatures,2):
        sa,sb=signatures[a],signatures[b]
        unseen=all(not ({a,b}<=ns) for ns in neighborhoods.values())
        antipodal=sa[0]!=sb[0] and sa[1]!=sb[1]
        require(unseen==antipodal, 'exact omitted edge interface')
        if unseen:
            diagonal.append((a,b))
    hole=tuple(data['forced_diagonal_edge'])
    require(hole in diagonal, 'forcing hole is an omitted diagonal edge')
    require(signatures[hole[0]]==(1,0) and signatures[hole[1]]==(0,1), 'forcing hole cell types')
    for name,color in (('red_five_minus_edge',True),('blue_five_minus_edge',False)):
        subset=data[name]
        require(len(subset)==5 and len(set(subset))==5 and list(subset)==sorted(subset), 'canonical forcing five-set')
        require(set(hole)<=set(subset), 'forcing set contains hole')
        require(not {0,3}&set(subset), 'forcing set avoids anchors')
        for e in combinations(subset,2):
            if e==hole:
                continue
            require(e not in diagonal and adj[e[0]][e[1]]==color, 'nine fixed forcing edges')
    require(set(data['red_five_minus_edge']) & set(data['blue_five_minus_edge'])==set(hole), 'eight-vertex obstruction')
    # Unit-multiplier sum of the two standard monochromatic-K5 inequalities.
    red_pairs=set(combinations(data['red_five_minus_edge'],2))
    blue_pairs=set(combinations(data['blue_five_minus_edge'],2))
    coefficients=Counter({e:1 for e in red_pairs})
    coefficients.subtract({e:1 for e in blue_pairs})
    require(coefficients[hole]==0 and sum(c!=0 for c in coefficients.values())==18, 'exact elimination of hole')
    cut_lhs=sum(c*int(e in red) for e,c in coefficients.items())
    require(cut_lhs==9 and 9+(-1)==8, 'unit-multiplier cut violated by one')
    counts=Counter()
    patterns=Counter()
    first={}
    monochromatic_rows=[]
    for s in combinations(range(43),5):
        first_color=adj[s[0]][s[1]]
        if not all(adj[a][b]==first_color for a,b in combinations(s,2)):
            continue
        color='R' if first_color else 'B'
        require(0 not in s and 3 not in s, 'defect meets anchor')
        require(all(not set(s)<=ns for ns in neighborhoods.values()), 'defect inside checked neighborhood')
        require(any(a in s and b in s for a,b in diagonal), 'defect avoids both omitted interfaces')
        counts[color]+=1
        monochromatic_rows.append(color+':'+','.join(map(str,s)))
        first.setdefault(color,list(s))
        pattern=tuple(sum(signatures[x]==sig for x in s) for sig in ((1,1),(1,0),(0,1),(0,0)))
        patterns[(color,pattern)]+=1
    require(counts['R']>0 and counts['B']>0, 'explicit non-Ramsey witness')
    edge_text=''.join(f'{a} {b}\n' for a,b in sorted(red))
    return {'edges':len(red),'degrees':sorted(Counter(degrees).items()),'local':local,'common':len(common),
            'cell_sizes':[cells[sig] for sig in ((1,1),(1,0),(0,1),(0,0))],
            'diagonal_edges':len(diagonal),'defects':dict(sorted(counts.items())),
            'first_defects':dict(sorted(first.items())),
            'monochromatic_list_sha256':sha256(('\n'.join(monochromatic_rows)+'\n').encode()).hexdigest(),
            'forced_diagonal_edge':list(hole),
            'red_five_minus_edge':data['red_five_minus_edge'],
            'blue_five_minus_edge':data['blue_five_minus_edge'],
            'excluded_fixed_neighborhood_completions':'2^'+str(len(diagonal)),
            'guarded_incidence_cut':{'lhs':cut_lhs,'rhs':8,'multipliers':[1,1]},
            'pattern_digest':sha256(json.dumps([(c,list(p),n) for (c,p),n in sorted(patterns.items())],separators=(',',':')).encode()).hexdigest(),
            'degree_deviation_square_sum':sum((d-21)**2 for d in degrees),
            'edge_sha256':sha256(edge_text.encode()).hexdigest()}


def main():
    data=json.loads((HERE/'WITNESS.json').read_text())
    result=audit(construct(data), data)
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
