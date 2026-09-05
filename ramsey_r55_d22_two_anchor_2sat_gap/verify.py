"""Solver-free definition-level verification of the width-two survivor."""
from __future__ import annotations

import base64
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LOCAL_UPPER = {20: 100, 21: 107, 22: 114}


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
    require(not any(bits[bit_count:]), "graph6 padding")
    edges = set()
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.add((left, right))
            cursor += 1
    return order, edges


def construct(data):
    require(data["format"] == "r55-d22-two-anchor-width2-gap-v1", "witness format")
    require(data["anchors"] == [0, 3], "anchor labels")
    order, red_core = decode_graph6(data["red_core_parent_graph6_base64"])
    require(order == 22 and len(red_core) == 114, "red parent core")
    for raw_edge in data["red_core_delete_edges"]:
        edge = tuple(raw_edge)
        require(edge in red_core, "core deletion exists once")
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
    require(all(0 <= a < b < 43 for a, b in red), "simple canonical edges")
    adjacency = [[False] * 43 for _ in range(43)]
    for a, b in red:
        adjacency[a][b] = adjacency[b][a] = True
    degrees = [sum(row) for row in adjacency]
    require(len(red) == 452, "red edge count")
    require(Counter(degrees) == Counter({20: 8, 21: 26, 22: 9}), "degree profile")
    require(set(x for x in range(43) if adjacency[0][x]) == set(range(1, 23)), "root split")

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
                    f"forbidden subset at root {root}, color {int(color)}",
                )
            local.append(
                [root, "R" if color else "B", len(vertices), same_edges, LOCAL_UPPER[len(vertices)] - same_edges]
            )
    require(
        local == [[0, "R", 22, 108, 6], [0, "B", 20, 100, 0], [3, "R", 21, 99, 8], [3, "B", 21, 98, 9]],
        "two-anchor profiles",
    )

    outside = [x for x in range(43) if x not in (0, 3)]
    signature = {x: (int(adjacency[0][x]), int(adjacency[3][x])) for x in outside}
    cells = Counter(signature.values())
    require(
        [cells[sig] for sig in ((1, 1), (1, 0), (0, 1), (0, 0))] == [10, 11, 10, 10],
        "signature cells",
    )
    diagonal = []
    for a, b in combinations(outside, 2):
        unseen = all(not ({a, b} <= neighborhood) for neighborhood in neighborhoods.values())
        antipodal = signature[a][0] != signature[b][0] and signature[a][1] != signature[b][1]
        require(unseen == antipodal, "diagonal equals unseen")
        if unseen:
            diagonal.append((a, b))
    require(len(diagonal) == 210, "diagonal edge count")
    diagonal_set = set(diagonal)
    variable = {edge: index + 1 for index, edge in enumerate(diagonal)}

    raw_counts = Counter()
    origins = {}
    defects = Counter()
    first_defects = {}
    monochromatic_rows = []
    for subset in combinations(outside, 5):
        pairs = list(combinations(subset, 2))
        holes = tuple(edge for edge in pairs if edge in diagonal_set)
        exposed = [edge for edge in pairs if edge not in diagonal_set]
        if holes and all(adjacency[a][b] for a, b in exposed):
            clause = tuple(sorted(-variable[edge] for edge in holes))
            raw_counts[("R", len(clause))] += 1
            origins.setdefault(clause, ("R", subset, holes))
        if holes and all(not adjacency[a][b] for a, b in exposed):
            clause = tuple(sorted(variable[edge] for edge in holes))
            raw_counts[("B", len(clause))] += 1
            origins.setdefault(clause, ("B", subset, holes))
        if all(adjacency[a][b] for a, b in pairs):
            defects[("R", len(holes))] += 1
            first_defects.setdefault(("R", len(holes)), list(subset))
            monochromatic_rows.append("R:" + ",".join(map(str, subset)))
        if all(not adjacency[a][b] for a, b in pairs):
            defects[("B", len(holes))] += 1
            first_defects.setdefault(("B", len(holes)), list(subset))
            monochromatic_rows.append("B:" + ",".join(map(str, subset)))

    expected_raw = {
        ("B", 1): 13, ("B", 2): 205, ("B", 3): 1151, ("B", 4): 1104, ("B", 6): 2422,
        ("R", 1): 19, ("R", 2): 326, ("R", 3): 2384, ("R", 4): 1241, ("R", 6): 544,
    }
    expected_unique = {
        ("B", 1): 10, ("B", 2): 161, ("B", 3): 1109, ("B", 4): 867, ("B", 6): 2422,
        ("R", 1): 13, ("R", 2): 229, ("R", 3): 2249, ("R", 4): 645, ("R", 6): 544,
    }
    unique_counts = Counter((origin[0], len(clause)) for clause, origin in origins.items())
    require(dict(raw_counts) == expected_raw, "raw residual census")
    require(dict(unique_counts) == expected_unique, "unique residual census")

    violated = Counter()
    for clause, origin in origins.items():
        satisfied = any(
            (diagonal[abs(literal) - 1] in red) == (literal > 0)
            for literal in clause
        )
        if not satisfied:
            violated[(origin[0], len(clause))] += 1
    expected_violated = {
        ("B", 3): 92, ("B", 4): 45, ("B", 6): 58,
        ("R", 3): 140, ("R", 4): 12, ("R", 6): 1,
    }
    require(dict(violated) == expected_violated, "violated residual clauses")
    require(not any(width <= 2 for _color, width in violated), "width-two subsystem satisfied")
    require(
        defects == Counter({("R", 3): 141, ("B", 3): 93, ("B", 6): 58, ("B", 4): 53, ("R", 4): 20, ("R", 6): 1}),
        "full defect census",
    )
    require(first_defects[("R", 3)] == data["first_red_width3_k5"], "first red width-three defect")
    require(first_defects[("B", 3)] == data["first_blue_width3_k5"], "first blue width-three defect")
    for label, subset in (("R", data["first_red_width3_k5"]), ("B", data["first_blue_width3_k5"])):
        pairs = list(combinations(subset, 2))
        require(sum(edge in diagonal_set for edge in pairs) == 3, "three diagonal holes")
        color = label == "R"
        require(all(adjacency[a][b] == color for a, b in pairs), "advertised monochromatic defect")

    clause_rows = []
    for clause in sorted(origins, key=lambda item: (len(item), item)):
        label, subset, holes = origins[clause]
        clause_rows.append(
            label + ":" + ",".join(map(str, subset)) + ":" + ";".join(f"{a}-{b}" for a, b in holes)
        )
    edge_text = "".join(f"{a} {b}\n" for a, b in sorted(red))
    defect_output = [[color, width, defects[(color, width)]] for color, width in sorted(defects)]
    violated_output = [[color, width, expected_violated[(color, width)]] for color, width in sorted(expected_violated)]
    return {
        "anchors": [0, 3],
        "cell_sizes": [cells[sig] for sig in ((1, 1), (1, 0), (0, 1), (0, 0))],
        "degree_deviation_square_sum": sum((degree - 21) ** 2 for degree in degrees),
        "degrees": sorted(Counter(degrees).items()),
        "diagonal_edges": len(diagonal),
        "edge_sha256": sha256(edge_text.encode()).hexdigest(),
        "edges": len(red),
        "first_blue_width3_k5": data["first_blue_width3_k5"],
        "first_red_width3_k5": data["first_red_width3_k5"],
        "local": local,
        "minimum_defect_width": min(width for _color, width in defects),
        "monochromatic_defects": defect_output,
        "monochromatic_list_sha256": sha256(("\n".join(monochromatic_rows) + "\n").encode()).hexdigest(),
        "residual_clause_sha256": sha256(("\n".join(clause_rows) + "\n").encode()).hexdigest(),
        "residual_clauses": len(origins),
        "violated_residual_clauses": violated_output,
        "width_at_most_two_clauses": sum(count for (label, width), count in expected_unique.items() if width <= 2),
        "width_at_most_two_status": "SAT_BY_STORED_DEGREE_COMPATIBLE_ASSIGNMENT",
    }


def main():
    data = json.loads((HERE / "WITNESS.json").read_text())
    print(json.dumps(audit(construct(data), data), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
