"""Solver-free definition-level verification of the two-anchor gap witness."""
from __future__ import annotations

import base64
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LOCAL_UPPER = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode_graph6(encoded):
    raw = base64.b64decode(encoded, validate=True)
    require(bool(raw), "empty graph6")
    order = raw[0] - 63
    require(0 <= order <= 62, "small graph6 order")
    bit_count = order * (order - 1) // 2
    require(len(raw) == 1 + (bit_count + 5) // 6, "graph6 length")
    bits = []
    for value in raw[1:]:
        require(63 <= value <= 126, "graph6 alphabet")
        bits.extend(((value - 63) >> bit) & 1 for bit in range(5, -1, -1))
    require(not any(bits[bit_count:]), "zero graph6 padding")
    edges = set()
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.add((left, right))
            cursor += 1
    return order, edges


def construct(data):
    require(data["format"] == "r55-d22-two-anchor-binary-gap-v1", "witness format")
    require(data["anchors"] == [0, 3], "anchor labels")
    order, red_core = decode_graph6(data["red_core_parent_graph6_base64"])
    require(order == 22 and len(red_core) == 114, "red parent core")
    for raw_edge in data["red_core_delete_edges"]:
        edge = tuple(raw_edge)
        require(edge in red_core, "core deletion exists exactly once")
        red_core.remove(edge)
    order, blue_core = decode_graph6(data["blue_core_graph6_base64"])
    require(order == 20 and len(blue_core) == 100, "blue core")
    rows = data["cross_rows"]
    require(
        len(rows) == 22 and all(len(row) == 20 and set(row) <= {"0", "1"} for row in rows),
        "cross-matrix format",
    )
    red = {(0, vertex) for vertex in range(1, 23)}
    red.update((a + 1, b + 1) for a, b in red_core)
    red.update(
        (a + 23, b + 23)
        for a, b in combinations(range(20), 2)
        if (a, b) not in blue_core
    )
    red.update(
        (i + 1, j + 23)
        for i, row in enumerate(rows)
        for j, bit in enumerate(row)
        if bit == "1"
    )
    return red


def audit(red, data):
    require(
        all(type(a) is int and type(b) is int and 0 <= a < b < 43 for a, b in red),
        "simple canonical red edges",
    )
    adjacency = [[False] * 43 for _ in range(43)]
    for a, b in red:
        adjacency[a][b] = adjacency[b][a] = True

    degrees = [sum(row) for row in adjacency]
    require(len(red) == 452, "M=452 red edges")
    require(Counter(degrees) == Counter({20: 8, 21: 26, 22: 9}), "tight degree profile")
    require(degrees[0] == 22, "d=22 anchor")
    require(set(x for x in range(43) if adjacency[0][x]) == set(range(1, 23)), "anchor split")

    neighborhoods = {}
    local = []
    for root in (0, 3):
        for color in (True, False):
            vertices = [x for x in range(43) if x != root and adjacency[root][x] == color]
            neighborhoods[(root, color)] = set(vertices)
            same_edges = sum(adjacency[a][b] == color for a, b in combinations(vertices, 2))
            for size, target in ((4, color), (5, not color)):
                require(
                    not any(
                        all(adjacency[a][b] == target for a, b in combinations(subset, 2))
                        for subset in combinations(vertices, size)
                    ),
                    f"forbidden monochromatic subset in root {root} color {int(color)}",
                )
            local.append(
                [root, "R" if color else "B", len(vertices), same_edges, LOCAL_UPPER[len(vertices)] - same_edges]
            )
    require(
        local == [[0, "R", 22, 108, 6], [0, "B", 20, 100, 0], [3, "R", 21, 95, 12], [3, "B", 21, 101, 6]],
        "exact two-anchor local profiles",
    )

    outside = [x for x in range(43) if x not in (0, 3)]
    signature = {x: (int(adjacency[0][x]), int(adjacency[3][x])) for x in outside}
    cells = Counter(signature.values())
    require(
        [cells[sig] for sig in ((1, 1), (1, 0), (0, 1), (0, 0))] == [10, 11, 10, 10],
        "two-anchor cell sizes",
    )
    diagonal = []
    for a, b in combinations(outside, 2):
        unseen = all(not ({a, b} <= neighborhood) for neighborhood in neighborhoods.values())
        antipodal = signature[a][0] != signature[b][0] and signature[a][1] != signature[b][1]
        require(unseen == antipodal, "exact omitted-edge interface")
        if unseen:
            diagonal.append((a, b))
    require(len(diagonal) == 210, "diagonal-edge count")
    diagonal_set = set(diagonal)
    variable = {edge: index + 1 for index, edge in enumerate(diagonal)}

    raw_counts = Counter()
    clause_origins = {}
    full_defects = Counter()
    full_rows = []
    first_defect = {}
    for subset in combinations(outside, 5):
        pairs = list(combinations(subset, 2))
        holes = [edge for edge in pairs if edge in diagonal_set]
        fixed_pairs = [edge for edge in pairs if edge not in diagonal_set]
        for color, label in ((True, "R"), (False, "B")):
            if holes and all(adjacency[a][b] == color for a, b in fixed_pairs):
                clause = tuple(sorted((-variable[edge] if color else variable[edge]) for edge in holes))
                raw_counts[(label, len(clause))] += 1
                clause_origins.setdefault(clause, (label, subset, tuple(holes)))
        first_color = adjacency[subset[0]][subset[1]]
        if all(adjacency[a][b] == first_color for a, b in pairs):
            label = "R" if first_color else "B"
            full_defects[label] += 1
            first_defect.setdefault(label, list(subset))
            full_rows.append(label + ":" + ",".join(map(str, subset)))

    unique_counts = Counter((origin[0], len(clause)) for clause, origin in clause_origins.items())
    expected_raw = {
        ("B", 1): 16, ("B", 2): 271, ("B", 3): 1414, ("B", 4): 1292, ("B", 6): 2217,
        ("R", 1): 8, ("R", 2): 364, ("R", 3): 1827, ("R", 4): 1106, ("R", 6): 494,
    }
    expected_unique = {
        ("B", 1): 13, ("B", 2): 215, ("B", 3): 1359, ("B", 4): 983, ("B", 6): 2217,
        ("R", 1): 7, ("R", 2): 263, ("R", 3): 1765, ("R", 4): 630, ("R", 6): 494,
    }
    require(dict(raw_counts) == expected_raw, "raw residual-clause census")
    require(dict(unique_counts) == expected_unique, "unique residual-clause census")

    unit_values = {}
    for clause, (label, _subset, _holes) in clause_origins.items():
        if len(clause) != 1:
            continue
        literal = clause[0]
        edge = diagonal[abs(literal) - 1]
        value = literal > 0
        require(edge not in unit_values or unit_values[edge] == value, "opposite one-edge forcing")
        unit_values[edge] = value
    require(Counter(unit_values.values()) == Counter({True: 13, False: 7}), "unit-force colors")

    coupled = [tuple(edge) for edge in data["coupled_diagonal_edges"]]
    require(len(coupled) == 2 and len(set(coupled)) == 2, "two coupled edges")
    require(all(edge in diagonal_set for edge in coupled), "coupled edges are omitted")
    for subset, edge in zip(data["blue_unit_five_sets"], coupled):
        require(len(subset) == 5 and list(subset) == sorted(set(subset)), "canonical blue five-set")
        pairs = list(combinations(subset, 2))
        require([candidate for candidate in pairs if candidate in diagonal_set] == [edge], "blue unit hole")
        require(all(not adjacency[a][b] for a, b in pairs if (a, b) != edge), "nine fixed blue edges")
        require(unit_values[edge] is True, "blue unit forces red hole")
    red_subset = data["red_binary_five_set"]
    require(len(red_subset) == 5 and list(red_subset) == sorted(set(red_subset)), "canonical red five-set")
    red_pairs = list(combinations(red_subset, 2))
    require([edge for edge in red_pairs if edge in diagonal_set] == coupled, "red binary holes")
    require(all(adjacency[a][b] for a, b in red_pairs if (a, b) not in set(coupled)), "eight fixed red edges")
    require(len(set().union(*map(set, data["blue_unit_five_sets"]), set(red_subset))) == 8, "eight-vertex certificate")

    # The width-one system sets both coupled indicators to one.  The red
    # two-hole clause says their sum is at most one, so width two is impossible.
    require(sum(int(unit_values[edge]) for edge in coupled) == 2, "two blue unit lower bounds")
    require(2 > 1, "binary red upper bound contradiction")

    clause_lines = []
    for clause in sorted(clause_origins, key=lambda item: (len(item), item)):
        label, subset, holes = clause_origins[clause]
        clause_lines.append(
            label + ":" + ",".join(map(str, subset)) + ":" + ";".join(f"{a}-{b}" for a, b in holes)
        )
    edge_text = "".join(f"{a} {b}\n" for a, b in sorted(red))
    return {
        "anchors": [0, 3],
        "cell_sizes": [cells[sig] for sig in ((1, 1), (1, 0), (0, 1), (0, 0))],
        "coupled_diagonal_edges": [list(edge) for edge in coupled],
        "degree_deviation_square_sum": sum((degree - 21) ** 2 for degree in degrees),
        "degrees": sorted(Counter(degrees).items()),
        "diagonal_edges": len(diagonal),
        "edge_sha256": sha256(edge_text.encode()).hexdigest(),
        "edges": len(red),
        "first_defects": dict(sorted(first_defect.items())),
        "full_coloring_defects": dict(sorted(full_defects.items())),
        "local": local,
        "monochromatic_list_sha256": sha256(("\n".join(full_rows) + "\n").encode()).hexdigest(),
        "residual_clause_sha256": sha256(("\n".join(clause_lines) + "\n").encode()).hexdigest(),
        "residual_clauses": len(clause_origins),
        "residual_raw_counts": [[label, width, expected_raw[(label, width)]] for label, width in sorted(expected_raw)],
        "residual_unique_counts": [[label, width, expected_unique[(label, width)]] for label, width in sorted(expected_unique)],
        "unit_forced_blue": sum(not value for value in unit_values.values()),
        "unit_forced_red": sum(value for value in unit_values.values()),
        "unit_subsystem": "SAT",
        "width_two_certificate": {
            "blue_lower_bounds": ["x_4_32 >= 1", "x_4_35 >= 1"],
            "red_upper_bound": "x_4_32 + x_4_35 <= 1",
            "status": "UNSAT",
            "vertices": [4, 8, 9, 11, 23, 32, 35, 38],
        },
    }


def main():
    data = json.loads((HERE / "WITNESS.json").read_text())
    print(json.dumps(audit(construct(data), data), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
