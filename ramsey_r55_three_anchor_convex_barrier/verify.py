"""Exact primal certificate: cell averages and complete linear K5 constraints."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from math import comb, factorial, prod
from pathlib import Path

from seed import audit, construct, require

HERE = Path(__file__).resolve().parent


def certificate(data):
    adjacency, local, edge_digest = audit(construct(data))
    roots = (0,3,9)
    cells = [[v for v in range(43) if v not in roots and
              sum(int(adjacency[r][v]) << (2-i) for i,r in enumerate(roots)) == s]
             for s in range(8)] + [[r] for r in roots]
    sizes = [len(c) for c in cells]
    require(sizes == [6,4,4,6,5,6,6,3,1,1,1], "cell sizes")
    counts, density = {}, {}
    for s in range(11):
        for t in range(s,11):
            pairs = list(combinations(cells[s],2)) if s == t else [(u,v) for u in cells[s] for v in cells[t]]
            counts[s,t] = sum(adjacency[u][v] for u,v in pairs)
            density[s,t] = Fraction(counts[s,t],len(pairs)) if pairs else Fraction(0)
    require(sum(counts.values()) == 452, "edge average")
    central = {p:q for p,q in density.items() if p[1] < 8}
    require({p for p,q in central.items() if q == 0} == {(7,7)}, "unique zero block")
    require(all(Fraction(1,6) <= q <= Fraction(3,4) for q in central.values() if q), "uniform density bounds")
    # At most choose(3,2) zero edges occur in any central five-set.
    require((10-comb(sizes[7],2))*Fraction(1,6) == Fraction(7,6), "uniform lower bound")
    records, mixed, outside = [], [], []
    for pattern in combinations_with_replacement(range(11),5):
        m = Counter(pattern)
        if any(m[s] > sizes[s] for s in m):
            continue
        number = prod(comb(sizes[s],m[s]) for s in m)
        value = sum((density[s,t] for s,t in combinations(pattern,2)), Fraction(0))
        total = number * value
        require(total.denominator == 1, "double-count integrality")
        require(1 <= value <= 9, "all global K5 clauses")
        records.append((pattern,number,total.numerator))
        if max(pattern) < 8:
            outside.append((value,pattern))
            if all({(s>>i)&1 for s in pattern} == {0,1} for i in range(3)) and not any((s^7) in pattern for s in pattern):
                mixed.append((value,pattern))
    require(sum(n for _p,n,_e in records) == comb(43,5), "all five-sets covered")
    require(len(mixed) == 88, "mixed complement-free patterns")
    text = "".join(f"{','.join(map(str,p))}|{n}|{e}\n" for p,n,e in records)
    point_text = "".join(f"{s},{t}|{density[s,t]}\n" for s,t in sorted(density))
    return {
        "status": "PASS_EXACT_CONVEX_BARRIER",
        "cell_sizes": sizes[:8],
        "central_edge_counts_upper_triangle": [[counts[s,t] for t in range(s,8)] for s in range(8)],
        "local_profiles": local,
        "seed_edge_sha256": edge_digest,
        "cell_permutation_group_order": prod(factorial(n) for n in sizes),
        "five_set_patterns": len(records),
        "five_sets": sum(n for _p,n,_e in records),
        "pattern_average_sha256": sha256(text.encode()).hexdigest(),
        "density_sha256": sha256(point_text.encode()).hexdigest(),
        "outside_patterns": len(outside),
        "outside_exact_range": [str(min(outside)[0]), str(max(outside)[0])],
        "outside_uniform_bound": ["7/6", "15/2"],
        "mixed_patterns": len(mixed),
        "mixed_exact_range": [str(min(mixed)[0]), str(max(mixed)[0])],
    }


if __name__ == "__main__":
    print(json.dumps(certificate(json.loads((HERE / "SEED.json").read_text())), indent=2, sort_keys=True))
