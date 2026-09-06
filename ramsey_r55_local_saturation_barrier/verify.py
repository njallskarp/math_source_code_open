"""Exact definition-level verification of the minimal saturation obstruction."""
from collections import Counter
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def decode(s):
    need(type(s) is str and len(s) == 40 and ord(s[0])-63 == 22, 'graph6 domain')
    bits = []
    for c in s[1:]:
        n = ord(c)-63
        need(0 <= n < 64, 'graph6 alphabet')
        bits += [(n >> k) & 1 for k in range(5, -1, -1)]
    need(not any(bits[231:]), 'zero graph6 padding')
    return {p for p, b in zip(((i,j) for j in range(1,22) for i in range(j)), bits) if b}


def counts(n, edges, size, color):
    return sum(all((p in edges) == color for p in combinations(S,2))
               for S in combinations(range(n),size))


def digest(edges):
    return sha256((json.dumps(sorted(edges),separators=(',',':'))+'\n').encode()).hexdigest()


def neighbors(n, edges):
    return [{w for w in range(n) if tuple(sorted((v,w))) in edges} for v in range(n)]


def connected_masks(adj, removed):
    alive = ((1 << len(adj))-1) ^ removed
    if not alive:
        return True
    seen = front = alive & -alive
    while front:
        reached = 0
        while front:
            bit = front & -front; front ^= bit
            reached |= adj[bit.bit_length()-1]
        front = reached & alive & ~seen
        seen |= front
    return seen == alive


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--witness',type=Path,default=HERE/'WITNESS.json')
    args=parser.parse_args()
    w = json.loads(args.witness.read_text())
    parent = decode(w['parent_graph6'])
    need(len(parent)==114 and counts(22,parent,4,True)==0 and counts(22,parent,5,False)==0,'parent Ramsey')
    deleted = [tuple(p) for p in w['deleted_edges']]
    need(len(deleted)==len(set(deleted))==6 and all(0<=a<b<22 and (a,b) in parent for a,b in deleted),'six deletions')
    H = parent-set(deleted); N=neighbors(22,H)
    need([sorted(a) for a in N]==w['core_adjacency'],'independent adjacency representation')
    need(len(H)==108 and counts(22,H,4,True)==0 and counts(22,H,5,False)==0,'core Ramsey')
    a,b=w['distant_pair']; need((a,b)==(4,5) and (a,b) not in H and not N[a]&N[b],'distant pair')
    path=w['distance_three_path']
    need(path[0]==a and path[-1]==b and len(path)==len(set(path))==4 and all(tuple(sorted(p)) in H for p in zip(path,path[1:])),'distance-three path')
    distant=[]
    for u,v in combinations(range(22),2):
        if (u,v) not in H and not N[u]&N[v]: distant.append([u,v])
    need(distant==[[4,5]],'unique distant pair')
    mask_adj=[sum(1<<v for v in row) for row in N]
    tested=0
    for k in range(7):
        for cut in combinations(range(22),k):
            need(connected_masks(mask_adj,sum(1<<v for v in cut)),'connectivity lower bound')
            tested+=1
    cut=w['seven_cut']
    need(len(cut)==len(set(cut))==7 and sorted(N[4])==cut and not connected_masks(mask_adj,sum(1<<v for v in cut)),'seven-cut upper bound')
    # Exact six-bit deletion kernel, checked against all literal five-sets.
    PN=neighbors(22,parent); C=sorted(PN[a]&PN[b]); need(C==list(range(12,18)),'common domain')
    constraints=set()
    for S in combinations([v for v in range(22) if v not in (a,b)],4):
        if any(p in parent for p in combinations(S,2)): continue
        for v,sign in ((a,1),(b,-1)):
            touched=PN[v]&set(S)
            if touched <= set(C):
                need(bool(touched),'parent independent five-set')
                constraints.add(tuple(sign*(C.index(x)+1) for x in sorted(touched)))
    valid=[]
    for word in product((0,1),repeat=len(C)):
        removed={tuple(sorted((b if bit else a,x))) for x,bit in zip(C,word)}
        predicted=all(any((lit>0)==bool(word[abs(lit)-1]) for lit in clause) for clause in constraints)
        literal=counts(22,parent-removed,5,False)==0
        need(predicted==literal,'whole deletion kernel equivalence')
        if literal: valid.append(list(word))
    need([0,1,1,0,0,1] in valid,'chosen deletion word')
    # Three outside vertices form a red triangle; the root is blue to them.
    signatures=w['outside_signatures'];need(len(signatures)==3,'three signatures')
    G=H | {(v,22) for v in range(22)} | set(combinations(range(23,26),2))
    for outside,signature in enumerate(signatures,23):
        need(signature==sorted(set(signature)) and all(type(v) is int and 0<=v<22 for v in signature),'signature domain')
        G |= {(v,outside) for v in signature}
    need(len(G)==178 and counts(26,G,5,True)==counts(26,G,5,False)==0,'full 26-vertex Ramsey witness')
    plus=H|{(4,5)};need(counts(22,plus,4,True)==counts(22,plus,5,False)==0,'locally safe addition')
    forbidden=(4,5,23,24,25)
    need(all(p in G|{(4,5)} for p in combinations(forbidden,2)),'global red obstruction')
    need(counts(26,G|{(4,5)},5,True)==1,'exactly one new red K5')
    for outside_subset in combinations(range(23,26),2):
        V=list(range(23))+list(outside_subset)
        need(all(not all(p in G|{(4,5)} for p in combinations(S,2)) for S in combinations(V,5)),'two-outside boundary control')
    print(json.dumps({'vertices':26,'red_edges':178,'core_edges':108,'core_degree_histogram':dict(sorted(Counter(map(len,N)).items())),
                      'core_connectivity':7,'cut_subsets_checked':tested,'core_diameter':3,'distant_pairs':distant,
                      'kernel_variables':len(C),'kernel_clauses':len(constraints),'kernel_assignments_checked':2**len(C),'kernel_solutions':valid,
                      'full_five_sets_per_color':comb(26,5),'new_red_K5_count':1,'core_edge_sha256':digest(H),'extension_edge_sha256':digest(G)},sort_keys=True))


if __name__=='__main__':
    main()
