"""Exact orbit verification for fully visible mixed three-anchor five-sets."""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bits(vertex, dimension=3):
    return tuple((vertex >> (dimension - 1 - index)) & 1 for index in range(dimension))


def encode(values):
    return [format(value, "03b") for value in values]


def transform(vertex, permutation, flips):
    source = bits(vertex)
    target = tuple(source[permutation[index]] ^ flips[index] for index in range(3))
    return 4 * target[0] + 2 * target[1] + target[2]


def valid(multiset, dimension=3):
    support = set(multiset)
    return (
        all({bits(vertex, dimension)[index] for vertex in support} == {0, 1} for index in range(dimension))
        and not any((vertex ^ ((1 << dimension) - 1)) in support for vertex in support)
    )


def category(multiset):
    support = set(multiset)
    multiplicity = Counter(multiset)
    partition = sorted(multiplicity.values(), reverse=True)
    cube_degree = {
        vertex: sum((vertex ^ other).bit_count() == 1 for other in support)
        for vertex in support
    }
    edge_count = sum(cube_degree.values()) // 2
    if len(support) == 3:
        require(edge_count == 0, "three-support geometry")
        if partition == [3, 1, 1]:
            return "triangle_heavy"
        require(partition == [2, 2, 1], "three-support partition")
        return "triangle_double"
    require(len(support) == 4 and partition == [2, 1, 1, 1], "four-support partition")
    doubled = next(vertex for vertex, count in multiplicity.items() if count == 2)
    if edge_count == 0:
        require(set(cube_degree.values()) == {0}, "tetrahedron geometry")
        return "parity_tetrahedron"
    require(edge_count == 3 and sorted(cube_degree.values()) == [1, 1, 1, 3], "star geometry")
    return "star_center" if cube_degree[doubled] == 3 else "star_leaf"


def audit(certificate):
    require(certificate["format"] == "r55-three-cube-mixed-orbits-v1", "format")
    group = [
        (permutation, flips)
        for permutation in permutations(range(3))
        for flips in product((0, 1), repeat=3)
    ]
    actions = {
        tuple(transform(vertex, permutation, flips) for vertex in range(8))
        for permutation, flips in group
    }
    require(len(group) == len(actions) == certificate["group_order"] == 48, "cube group")

    all_multisets = list(combinations_with_replacement(range(8), 5))
    qualifying = {multiset for multiset in all_multisets if valid(multiset)}
    require(len(all_multisets) == 792 and len(qualifying) == 88, "multiset counts")
    require(not any(valid(multiset, 2) for multiset in combinations_with_replacement(range(4), 5)), "two-bit contrast")

    computed = {}
    union = set()
    orbit_rows = []
    for record in certificate["orbits"]:
        representative = tuple(int(value, 2) for value in record["representative"])
        require(tuple(sorted(representative)) == representative, "sorted representative")
        require(valid(representative), "valid representative")
        orbit = {
            tuple(sorted(transform(vertex, permutation, flips) for vertex in representative))
            for permutation, flips in group
        }
        stabilizer = sum(
            tuple(sorted(transform(vertex, permutation, flips) for vertex in representative)) == representative
            for permutation, flips in group
        )
        require(48 == stabilizer * len(orbit), "orbit-stabilizer")
        require(stabilizer == record["stabilizer_order"], "stabilizer order")
        require(len(orbit) == record["orbit_size"], "orbit size")
        require(len(set(representative)) == record["support_size"], "support size")
        require(sorted(Counter(representative).values(), reverse=True) == record["multiplicities"], "multiplicities")
        require(category(representative) == record["name"], "orbit name")
        canonical = min(orbit)
        require(canonical == representative, "canonical representative")
        require(record["name"] not in computed and union.isdisjoint(orbit), "distinct orbit")
        computed[record["name"]] = orbit
        union.update(orbit)
        orbit_rows.append([
            record["name"],
            record["representative"],
            stabilizer,
            len(orbit),
        ])
    require(union == qualifying, "orbit-complete classification")

    categories = Counter(category(multiset) for multiset in qualifying)
    require(categories == Counter({
        "triangle_heavy": 24,
        "triangle_double": 24,
        "star_center": 8,
        "star_leaf": 24,
        "parity_tetrahedron": 8,
    }), "category counts")
    supports = {frozenset(multiset) for multiset in qualifying}
    support_geometries = Counter()
    for support in supports:
        edge_count = sum((left ^ right).bit_count() == 1 for left, right in combinations(support, 2))
        support_geometries[(len(support), edge_count)] += 1
    require(support_geometries == Counter({(3, 0): 8, (4, 3): 8, (4, 0): 2}), "support geometries")

    rows = [",".join(encode(multiset)) for multiset in sorted(qualifying)]
    return {
        "complete_cut_templates": 2 * len(computed),
        "cube_group_order": len(actions),
        "orbit_rows": orbit_rows,
        "qualifying_multiset_sha256": sha256(("\n".join(rows) + "\n").encode()).hexdigest(),
        "qualifying_multisets": len(qualifying),
        "support_geometries": [[size, edges, count] for (size, edges), count in sorted(support_geometries.items())],
        "three_bit_orbits": len(computed),
        "total_five_multisets": len(all_multisets),
        "two_bit_qualifying_multisets": 0,
    }


def main():
    certificate = json.loads((HERE / "ORBIT_CERTIFICATE.json").read_text())
    print(json.dumps(audit(certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
