"""Standard-library exact verification of the three-anchor survivor."""
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


def edge(left, right):
    return tuple(sorted((left, right)))


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
    require(data["format"] == "r55-d22-three-anchor-survivor-v1", "format")
    require(data["anchors"] == [0, 3, 9], "anchors")
    order, red_core = decode_graph6(data["red_core_parent_graph6_base64"])
    require(order == 22 and len(red_core) == 114, "red parent core")
    for raw_edge in data["red_core_delete_edges"]:
        deleted = tuple(raw_edge)
        require(deleted in red_core, "red deletion")
        red_core.remove(deleted)
    order, blue_core = decode_graph6(data["blue_core_graph6_base64"])
    require(order == 20 and len(blue_core) == 100, "blue core")
    rows = data["cross_rows"]
    require(
        len(rows) == 22 and all(len(row) == 20 and set(row) <= {"0", "1"} for row in rows),
        "cross rows",
    )
    red = {(0, vertex) for vertex in range(1, 23)}
    red.update((left + 1, right + 1) for left, right in red_core)
    red.update(
        (left + 23, right + 23)
        for left, right in combinations(range(20), 2)
        if (left, right) not in blue_core
    )
    red.update(
        (left + 1, right + 23)
        for left, row in enumerate(rows)
        for right, bit in enumerate(row)
        if bit == "1"
    )
    return red


def audit(red, data):
    require(all(0 <= left < right < 43 for left, right in red), "canonical edges")
    adjacency = [[False] * 43 for _ in range(43)]
    for left, right in red:
        adjacency[left][right] = adjacency[right][left] = True
    degrees = [sum(row) for row in adjacency]
    require(len(red) == 452, "red edge count")
    require(Counter(degrees) == Counter({20: 8, 21: 26, 22: 9}), "degree profile")
    require(set(vertex for vertex in range(43) if adjacency[0][vertex]) == set(range(1, 23)), "root split")

    local = []
    neighborhoods = {}
    for root in data["anchors"]:
        for root_color in (True, False):
            vertices = [
                vertex for vertex in range(43)
                if vertex != root and adjacency[root][vertex] == root_color
            ]
            neighborhoods[(root, root_color)] = set(vertices)
            same_edges = sum(adjacency[left][right] == root_color for left, right in combinations(vertices, 2))
            for size, forbidden_color in ((4, root_color), (5, not root_color)):
                require(
                    not any(
                        all(adjacency[left][right] == forbidden_color for left, right in combinations(subset, 2))
                        for subset in combinations(vertices, size)
                    ),
                    f"local condition root={root},color={int(root_color)}",
                )
            local.append([
                root,
                "R" if root_color else "B",
                len(vertices),
                same_edges,
                LOCAL_UPPER[len(vertices)] - same_edges,
            ])

    anchors = tuple(data["anchors"])
    require(all(adjacency[left][right] for left, right in combinations(anchors, 2)), "red anchor triangle")
    anchor_core_degrees = [
        sum(adjacency[root][vertex] for vertex in range(1, 23) if vertex != root)
        for root in anchors[1:]
    ]
    require(anchor_core_degrees == [10, 10], "eligible high partners")
    triple_common = [
        vertex for vertex in range(43) if vertex not in anchors
        and all(adjacency[root][vertex] for root in anchors)
    ]

    outside = [vertex for vertex in range(43) if vertex not in anchors]
    signature = {
        vertex: tuple(int(adjacency[root][vertex]) for root in anchors)
        for vertex in outside
    }
    cells = Counter(signature.values())
    omitted = {
        pair for pair in combinations(outside, 2)
        if all(signature[pair[0]][index] != signature[pair[1]][index] for index in range(3))
    }
    for pair in combinations(outside, 2):
        unseen = all(not ({pair[0], pair[1]} <= neighborhood) for neighborhood in neighborhoods.values())
        require(unseen == (pair in omitted), "unseen equals complementary signatures")

    defects = Counter()
    first = {}
    rows = []
    supports = Counter()
    for subset in combinations(outside, 5):
        pairs = tuple(combinations(subset, 2))
        colors = {adjacency[left][right] for left, right in pairs}
        if len(colors) == 1:
            label = "R" if colors.pop() else "B"
            width = sum(pair in omitted for pair in pairs)
            support = tuple(sorted(set(signature[vertex] for vertex in subset)))
            defects[(label, width)] += 1
            supports[(label, width, support)] += 1
            first.setdefault((label, width), list(subset))
            rows.append(label + ":" + ",".join(map(str, subset)))
    require(defects, "witness is not Ramsey")

    edge_text = "".join(f"{left} {right}\n" for left, right in sorted(red))
    defect_text = "\n".join(rows) + "\n"
    first_minimum = {
        label: first[(label, min(width for color, width in defects if color == label))]
        for label in ("R", "B")
    }
    first_support = {
        label: ["".join(map(str, signature[vertex])) for vertex in first_minimum[label]]
        for label in ("R", "B")
    }
    for label, subset in first_minimum.items():
        support = {signature[vertex] for vertex in subset}
        require(all({bits[index] for bits in support} == {0, 1} for index in range(3)), "mixed in every anchor coordinate")
        require(
            not any(all(left[index] != right[index] for index in range(3)) for left, right in combinations(support, 2)),
            "complement-free signature support",
        )
    return {
        "anchor_core_degrees": anchor_core_degrees,
        "anchor_triangle": "R",
        "anchors": list(anchors),
        "cell_sizes": [["".join(map(str, bits)), cells[bits]] for bits in sorted(cells)],
        "degree_deviation_square_sum": sum((degree - 21) ** 2 for degree in degrees),
        "degrees": sorted(Counter(degrees).items()),
        "edge_sha256": sha256(edge_text.encode()).hexdigest(),
        "edges": len(red),
        "first_minimum_defects": first_minimum,
        "first_minimum_signatures": first_support,
        "local": local,
        "minimum_defect_width": min(width for _label, width in defects),
        "monochromatic_defect_list_sha256": sha256(defect_text.encode()).hexdigest(),
        "monochromatic_defects": [[label, width, defects[(label, width)]] for label, width in sorted(defects)],
        "omitted_edges": len(omitted),
        "triple_common_red_neighbors": triple_common,
    }


def main():
    data = json.loads((HERE / "WITNESS.json").read_text())
    print(json.dumps(audit(construct(data), data), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
