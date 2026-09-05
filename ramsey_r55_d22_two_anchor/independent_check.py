"""NetworkX decoder and maximal-clique verification, importing no target code."""
import base64
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import networkx as nx


def require(ok, label):
    if not ok:
        raise ValueError(label)


def main():
    data=json.loads((Path(__file__).resolve().parent/'WITNESS.json').read_text())
    h=nx.from_graph6_bytes(base64.b64decode(data['red_core_parent_graph6_base64'],validate=True))
    h.remove_edges_from(data['red_core_delete_edges'])
    j=nx.from_graph6_bytes(base64.b64decode(data['blue_core_graph6_base64'],validate=True))
    g=nx.Graph()
    g.add_nodes_from(range(43))
    g.add_edges_from((0,a) for a in range(1,23))
    g.add_edges_from((a+1,b+1) for a,b in h.edges)
    g.add_edges_from((a+23,b+23) for a,b in nx.complement(j).edges)
    for a,row in enumerate(data['cross_rows'],1):
        for b,bit in enumerate(row,23):
            if bit=='1':
                g.add_edge(a,b)
    gb=nx.complement(g)
    require(Counter(dict(g.degree()).values())==Counter({20:8,21:26,22:9}), 'degree profile')
    local=[]
    for v in data['anchors']:
        for color,graph in (('R',g),('B',gb)):
            core=graph.subgraph(list(graph.neighbors(v)))
            require(max(map(len,nx.find_cliques(core)))==3, 'local clique number')
            require(max(map(len,nx.find_cliques(nx.complement(core))))==4, 'local independence number')
            local.append((v,color,len(core),core.number_of_edges()))
    require(local==[(0,'R',22,108),(0,'B',20,100),(3,'R',21,99),(3,'B',21,97)], 'four exact neighborhoods')
    cells={bits:{x for x in range(43) if x not in data['anchors'] and tuple(int(g.has_edge(v,x)) for v in data['anchors'])==bits} for bits in ((1,1),(1,0),(0,1),(0,0))}
    require([len(x) for x in cells.values()]==[10,11,10,10], 'four cells')
    free=set()
    for sa,sb in (((1,1),(0,0)),((1,0),(0,1))):
        free.update(tuple(sorted((a,b))) for a in cells[sa] for b in cells[sb])
    require(len(free)==210, 'free diagonal edge count')
    hole=tuple(data['forced_diagonal_edge'])
    require(hole in free,'free forcing hole')
    for name,graph in (('red_five_minus_edge',g),('blue_five_minus_edge',gb)):
        chosen=data[name]
        fixed_pairs=set(combinations(chosen,2))-{hole}
        require(len(fixed_pairs)==9 and not fixed_pairs&free, 'nine protected pairs')
        require(all(graph.has_edge(a,b) for a,b in fixed_pairs),'forcing colors')
    require(len(set(data['red_five_minus_edge'])|set(data['blue_five_minus_edge']))==8,'eight-vertex forcing support')
    defects={}
    merged=[]
    for color,graph in (('R',g),('B',gb)):
        # Bron--Kerbosch maximal cliques followed by subset generation; duplicates removed.
        fives={tuple(sorted(s)) for c in nx.find_cliques(graph) for s in combinations(c,5)}
        defects[color]=len(fives)
        for subset in fives:
            require(not set(data['anchors'])&set(subset),'defect avoids anchors')
            require(any(e in free for e in combinations(subset,2)),'defect crosses diagonal')
            merged.append((subset,color))
    require(defects=={'R':273,'B':280}, 'full monochromatic sets')
    rows=[c+':'+','.join(map(str,s)) for s,c in sorted(merged)]
    digest=sha256(('\n'.join(rows)+'\n').encode()).hexdigest()
    print('PASS independent graph6 decoding and four full (4,5) neighborhoods')
    print('PASS red_degree_profile=20^8,21^26,22^9 red_edges=452')
    print('PASS cells=10,11,10,10 diagonal_edges=210')
    print('PASS fixed red and blue K5-minus-edge force opposite colors on (5,25)')
    print('PASS every one of 2^210 fixed-neighborhood completions is excluded')
    print('PASS monochromatic_K5 red=273 blue=280')
    print('MONOCHROMATIC_LIST_SHA256',digest)


if __name__=='__main__':
    main()
