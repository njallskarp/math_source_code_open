"""Independent antipodal-pair enumeration of the five signature types."""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json


PAIRS = ((0, 7), (1, 6), (2, 5), (3, 4))


def bits(vertex):
    return tuple(map(int, format(vertex, "03b")))


def positive_compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(1, total - parts + 2):
        for tail in positive_compositions(total - first, parts - 1):
            yield (first,) + tail


def classify(multiset):
    support = set(multiset)
    counts = Counter(multiset)
    edge_degrees = {
        vertex: sum((vertex ^ other).bit_count() == 1 for other in support)
        for vertex in support
    }
    if len(support) == 3:
        return "triangle_heavy" if max(counts.values()) == 3 else "triangle_double"
    doubled = next(vertex for vertex, count in counts.items() if count == 2)
    if not any(edge_degrees.values()):
        return "parity_tetrahedron"
    return "star_center" if edge_degrees[doubled] == 3 else "star_leaf"


def main():
    qualifying = set()
    support_counts = Counter()
    for size in (3, 4):
        for chosen_pairs in combinations(range(4), size):
            for orientations in product((0, 1), repeat=size):
                support = tuple(sorted(PAIRS[index][orientation] for index, orientation in zip(chosen_pairs, orientations)))
                if not all({bits(vertex)[coordinate] for vertex in support} == {0, 1} for coordinate in range(3)):
                    continue
                edge_count = sum((left ^ right).bit_count() == 1 for left, right in combinations(support, 2))
                support_counts[(size, edge_count)] += 1
                for composition in positive_compositions(5, size):
                    multiset = tuple(
                        vertex
                        for vertex, count in zip(support, composition)
                        for _ in range(count)
                    )
                    qualifying.add(multiset)
    categories = Counter(classify(multiset) for multiset in qualifying)
    assert len(qualifying) == 88
    assert categories == Counter({
        "triangle_heavy": 24,
        "triangle_double": 24,
        "star_center": 8,
        "star_leaf": 24,
        "parity_tetrahedron": 8,
    })
    assert support_counts == Counter({(3, 0): 8, (4, 3): 8, (4, 0): 2})
    rows = [",".join(format(vertex, "03b") for vertex in multiset) for multiset in sorted(qualifying)]
    print(json.dumps({
        "category_counts": sorted(categories.items()),
        "qualifying_multiset_sha256": sha256(("\n".join(rows) + "\n").encode()).hexdigest(),
        "qualifying_multisets": len(qualifying),
        "status": "PASS_ANTIPODAL_PAIR_DECOMPOSITION",
        "support_counts": [[size, edges, count] for (size, edges), count in sorted(support_counts.items())],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
