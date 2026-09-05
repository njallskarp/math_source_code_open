"""Exact aggregate central-edge model for the fixed M=216 signature witness."""

from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product


EXTREMA = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}


@lru_cache(None)
def upper(red, blue):
    """Elementary Ramsey upper bound with the even/even improvement."""
    if min(red, blue) == 1:
        return 1
    left, right = upper(red - 1, blue), upper(red, blue - 1)
    return left + right - int(left % 2 == right % 2 == 0)


def decode_core(order, mask):
    pairs = tuple(combinations(range(order), 2))
    adjacency = [set() for _ in range(order)]
    for bit, (left, right) in enumerate(pairs):
        if mask >> bit & 1:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return tuple(frozenset(row) for row in adjacency)


def roots(adjacency):
    """All nonempty disjoint red/blue exceptional root pairs."""
    order = len(adjacency)
    for word in product(range(3), repeat=order):
        red = frozenset(i for i, value in enumerate(word) if value == 1)
        blue = frozenset(i for i, value in enumerate(word) if value == 2)
        if not red | blue:
            continue
        if any(right not in adjacency[left] for left, right in combinations(red, 2)):
            continue
        if any(right in adjacency[left] for left, right in combinations(blue, 2)):
            continue
        fixed = frozenset(
            i for i in range(order) if i not in red | blue
            and red <= adjacency[i] and not blue & adjacency[i]
        )
        yield red, blue, fixed, 5 - len(red), 5 - len(blue)


def build(record, stage=2):
    """Return variables, boxes, and exact two-sided rows.

    stage 0 is the internal-root baseline, stage 1 adds order-15/16 density,
    and stage 2 adds the external-root lifting inequalities.
    """
    degrees = tuple(record["exceptional_degrees"])
    adjacency = decode_core(len(degrees), record["core_mask"])
    values = {mask: value for mask, value in record["cells"]}
    cells = tuple(sorted(values))
    pairs = tuple(
        (left, right)
        for left, right in combinations_with_replacement(cells, 2)
        if left != right or values[left] >= 2
    )
    boxes = tuple(
        values[left] * values[right] if left != right
        else values[left] * (values[left] - 1) // 2
        for left, right in pairs
    )
    rows = []

    def add(name, row, lower, upper_bound):
        rows.append((name, tuple(row), int(lower), int(upper_bound)))

    # Sum of red central degrees over every signature cell.
    for cell in cells:
        row = [int(left == cell) + int(right == cell) for left, right in pairs]
        target = (21 - cell.bit_count()) * values[cell]
        add(("degree", cell), row, target, target)

    # The hard branch improves each local Ramsey extremum by seven.
    # t_R + t_B is reconstructed from the global edge identity.
    edge_total = 231 + record["M"]
    for vertex, degree in enumerate(degrees):
        fixed = sum(right in adjacency[left] for left, right in combinations(adjacency[vertex], 2))
        fixed += sum(
            values[cell] * sum(cell >> neighbor & 1 for neighbor in adjacency[vertex])
            for cell in cells if cell >> vertex & 1
        )
        row = [int(bool(left & right & (1 << vertex))) for left, right in pairs]
        neighbor_degree_sum = sum(degrees[j] for j in adjacency[vertex])
        neighbor_degree_sum += 21 * (degree - len(adjacency[vertex]))
        local_sum = (42 - degree) * (41 - degree) // 2 - edge_total + neighbor_degree_sum
        red_cap = EXTREMA[degree] - 7
        blue_cap = EXTREMA[42 - degree] - 7
        add(("local", vertex), row, local_sum - blue_cap - fixed, red_cap - fixed)

    for red, blue, fixed_vertices, p, q in roots(adjacency):
        red_mask = sum(1 << i for i in red)
        blue_mask = sum(1 << i for i in blue)
        selected = frozenset(
            cell for cell in cells
            if cell & red_mask == red_mask and not cell & blue_mask
        )
        size = len(fixed_vertices) + sum(values[cell] for cell in selected)
        if not selected:
            continue

        for cell in cells:
            if stage < 2 and cell not in selected:
                continue
            row = [
                int(left == cell and right in selected)
                + int(right == cell and left in selected)
                for left, right in pairs
            ]
            capacity = sum(coefficient * box for coefficient, box in zip(row, boxes))
            if cell & red_mask == red_mask:
                fixed_red = values[cell] * sum(cell >> i & 1 for i in fixed_vertices)
                add(
                    ("root-red", red_mask, blue_mask, cell), row, 0,
                    (upper(p - 1, q) - 1) * values[cell] - fixed_red,
                )
            if not cell & blue_mask:
                fixed_blue = values[cell] * sum(not (cell >> i & 1) for i in fixed_vertices)
                add(
                    ("root-blue", red_mask, blue_mask, cell), row,
                    capacity - (upper(p, q - 1) - 1) * values[cell] + fixed_blue,
                    capacity,
                )

        for vertex in fixed_vertices:
            red_degree = sum(neighbor in fixed_vertices for neighbor in adjacency[vertex])
            red_degree += sum(values[cell] for cell in selected if cell >> vertex & 1)
            add(
                ("fixed-root", red_mask, blue_mask, vertex), [0] * len(pairs),
                max(0, size - upper(p, q - 1)) - red_degree,
                upper(p - 1, q) - 1 - red_degree,
            )

        if stage >= 1 and p == q == 4 and size in (15, 16):
            low, high = (50, 55) if size == 15 else (58, 62)
            fixed_edges = sum(
                right in adjacency[left] for left, right in combinations(fixed_vertices, 2)
            )
            fixed_edges += sum(
                values[cell] * sum(cell >> vertex & 1 for vertex in fixed_vertices)
                for cell in selected
            )
            row = [int(left in selected and right in selected) for left, right in pairs]
            add(("density", red_mask, blue_mask, size), row, low - fixed_edges, high - fixed_edges)

    return pairs, boxes, tuple(rows)


def canonical_inequalities(record, stage=2):
    """Deduplicate rows as A z <= b, including variable boxes."""
    pairs, boxes, rows = build(record, stage)
    bounds = {}
    labels = {}
    for name, row, lower, upper_bound in rows:
        for coefficients, bound, sense in (
            (row, upper_bound, "upper"),
            (tuple(-value for value in row), -lower, "lower"),
        ):
            if coefficients not in bounds or bound < bounds[coefficients]:
                bounds[coefficients] = bound
                labels[coefficients] = (name, sense)
    for index, box in enumerate(boxes):
        positive = tuple(int(i == index) for i in range(len(pairs)))
        negative = tuple(-value for value in positive)
        if positive not in bounds or box < bounds[positive]:
            bounds[positive] = box
            labels[positive] = (("box", index), "upper")
        if negative not in bounds or 0 < bounds[negative]:
            bounds[negative] = 0
            labels[negative] = (("box", index), "lower")
    ordered = sorted(bounds)
    return pairs, boxes, tuple((row, bounds[row], labels[row]) for row in ordered)
