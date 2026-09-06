"""Clean-room checker for the Paley-17 independent-four obstruction.

This program uses only the theorem statement.  It does not read the reviewed
artifact, its implementations, its certificate, or its catalogue inputs.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json


ORDER = 17
ALL = (1 << ORDER) - 1
RESIDUES = frozenset({1, 2, 4, 8, 9, 13, 15, 16})


def red_edge(u, v):
    return u != v and (u - v) % ORDER in RESIDUES


def vertices(value):
    return [vertex for vertex in range(ORDER) if value >> vertex & 1]


def monochromatic_cliques(size, color):
    return [
        group
        for group in combinations(range(ORDER), size)
        if all(red_edge(u, v) == color for u, v in combinations(group, 2))
    ]


def is_triangle_free(value):
    chosen = vertices(value)
    return not any(
        all(red_edge(u, v) for u, v in combinations(group, 2))
        for group in combinations(chosen, 3)
    )


def has_independent_triple(value):
    chosen = vertices(value)
    return any(
        all(not red_edge(u, v) for u, v in combinations(group, 2))
        for group in combinations(chosen, 3)
    )


def is_red_clique(value):
    chosen = vertices(value)
    return all(red_edge(u, v) for u, v in combinations(chosen, 2))


def add_edge(adjacency, u, v):
    adjacency[u] |= 1 << v
    adjacency[v] |= 1 << u


def increasing_bits(value, lower_bound):
    value &= ~((1 << lower_bound) - 1)
    while value:
        bit = value & -value
        value ^= bit
        yield bit.bit_length() - 1


def enumerate_cliques(adjacency):
    triangle_count = 0
    four_clique_count = 0
    triangle_rows = []
    for i in range(len(adjacency)):
        for j in increasing_bits(adjacency[i], i + 1):
            common = adjacency[i] & adjacency[j]
            for k in increasing_bits(common, j + 1):
                triangle_count += 1
                triangle_rows.append((i, j, k))
                four_clique_count += (
                    common & adjacency[k] & ~((1 << (k + 1)) - 1)
                ).bit_count()
    return triangle_count, four_clique_count, triangle_rows


def extension_clique_count(columns, size, color):
    def edge(u, v):
        if u < ORDER and v < ORDER:
            return red_edge(u, v)
        if u >= ORDER and v >= ORDER:
            return False
        core, exterior = (u, v - ORDER) if u < ORDER else (v, u - ORDER)
        return columns[exterior] >> core & 1 == 1

    return sum(
        all(edge(u, v) == color for u, v in combinations(group, 2))
        for group in combinations(range(ORDER + len(columns)), size)
    )


def main():
    red_four = monochromatic_cliques(4, True)
    blue_four = monochromatic_cliques(4, False)
    if red_four or blue_four:
        raise AssertionError("the generated core is not a (4,4)-graph")

    triangle_free = [value for value in range(1 << ORDER) if is_triangle_free(value)]
    triangle_free_set = set(triangle_free)
    maximal = sorted(
        value
        for value in triangle_free
        if all(
            value >> vertex & 1 or value | (1 << vertex) not in triangle_free_set
            for vertex in range(ORDER)
        )
    )

    adjacency = [0] * len(maximal)
    edges = []
    loops = []
    omissions = [ALL ^ value for value in maximal]
    for i in range(len(maximal)):
        if not has_independent_triple(omissions[i]):
            loops.append(i)
        for j in range(i + 1, len(maximal)):
            if not has_independent_triple(omissions[i] & omissions[j]):
                add_edge(adjacency, i, j)
                edges.append((i, j))

    triangle_count, four_clique_count, triangle_rows = enumerate_cliques(adjacency)
    if loops or four_clique_count:
        raise AssertionError("four independent exterior vertices were not excluded")

    full_three = []
    for i, j, k in triangle_rows:
        common_omission = omissions[i] & omissions[j] & omissions[k]
        if is_red_clique(common_omission):
            full_three.append((i, j, k))
    if not full_three:
        raise AssertionError("the asserted sharp boundary at three was not witnessed")

    first = full_three[0]
    first_columns = [maximal[i] for i in first]
    witness_red_four = extension_clique_count(first_columns, 4, True)
    witness_blue_five = extension_clique_count(first_columns, 5, False)
    if witness_red_four or witness_blue_five:
        raise AssertionError("the sharpness witness failed literal clique checks")
    mask_bytes = "".join(f"{value}\n" for value in maximal).encode()
    edge_bytes = "".join(f"{i} {j}\n" for i, j in edges).encode()
    result = {
        "status": "INDEPENDENT_PALEY17_OBSTRUCTION_VERIFIED",
        "paley_red_edges": sum(
            red_edge(u, v) for u, v in combinations(range(ORDER), 2)
        ),
        "paley_red_k4": len(red_four),
        "paley_blue_k4": len(blue_four),
        "triangle_free_subsets": len(triangle_free),
        "maximal_columns": len(maximal),
        "maximal_column_size_histogram": dict(
            sorted(Counter(value.bit_count() for value in maximal).items())
        ),
        "maximal_columns_sha256": sha256(mask_bytes).hexdigest(),
        "compatible_self_pairs": len(loops),
        "compatibility_edges": len(edges),
        "compatibility_triangles": triangle_count,
        "compatibility_four_cliques": four_clique_count,
        "compatibility_edges_sha256": sha256(edge_bytes).hexdigest(),
        "valid_unordered_maximal_column_triples_for_three_extension": len(full_three),
        "first_independent_three_extension": [vertices(value) for value in first_columns],
        "sharpness_witness_red_k4": witness_red_four,
        "sharpness_witness_blue_k5": witness_blue_five,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
