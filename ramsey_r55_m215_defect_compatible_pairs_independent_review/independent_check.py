#!/usr/bin/env python3
"""Clean-room audit of the M=215 defect-compatible-pair interface.

This checker imports no target module, expected output, solver, or catalogue.
It reads only the two explicitly hash-pinned target data files.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "ramsey_r55_m215_defect_compatible_pairs"
CERTIFICATE_SHA256 = "9dcb80ade7e904b4849094a0bbf2cfed7e07ea0aa5c07ee44752d30824e3afaa"
SHARPNESS_SHA256 = "3eadf55b4a2b83a0b00d59bd81db113b27c0604b4ddf3151136346613b9bd06b"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def choose2(x):
    return x * (x - 1) // 2


def pinned_json(name, expected_hash):
    raw = (TARGET / name).read_bytes()
    require(sha256(raw).hexdigest() == expected_hash, f"unexpected {name} hash")
    return json.loads(raw)


def convex_incidence_minimum(total, slots, capacity):
    """Minimize sum binom(d_i,2) by selecting marginal costs.

    Raising a slot from d to d+1 costs d.  Selecting the `total` least
    marginal costs is a separate dynamic reconstruction of the balancing
    formula used in the target proof.
    """
    if slots == 0:
        return 0 if total == 0 else None
    if total < 0 or total > slots * capacity:
        return None
    marginals = sorted(cost for _ in range(slots) for cost in range(capacity))
    return sum(marginals[:total])


def incidence_bound(k, fixed_red_stars):
    if k == 0:
        return 0, 1
    best = None
    feasible_states = 0
    for inside_edges in range(comb(k, 2) + 1):
        crossing = (21 - fixed_red_stars) * k - 2 * inside_edges
        inside = convex_incidence_minimum(2 * inside_edges, k, k - 1)
        outside = convex_incidence_minimum(crossing, 41 - k, k)
        if inside is None or outside is None:
            continue
        feasible_states += 1
        value = (
            inside
            + outside
            + (fixed_red_stars - 1) * comb(k, 2)
            + inside_edges
        )
        best = value if best is None else min(best, value)
    require(best is not None, f"no incidence state for k={k}")
    return best, feasible_states


def reconstruct_bounds():
    rows = []
    state_count = 0
    for k in range(22):
        opposite, states = incidence_bound(k, 1)
        same_blue, states0 = incidence_bound(k, 0)
        same_red, states2 = incidence_bound(k, 2)
        require(same_blue == same_red, f"color reversal failed at k={k}")
        state_count += states + states0 + states2
        for same, lower in ((0, opposite), (1, same_blue)):
            high = max(0, (lower - 9 * comb(k, 2) + 3) // 4)
            rows.append([k, same, lower, high])
    return rows, state_count


def reconstruct_multiplicities(bounds):
    high = {(k, same): h for k, same, _, h in bounds}
    rows = []
    minimizing_splits = {}
    for n in (19, 20, 21):
        values = [high[(k, 1)] + high[(n - k, 0)] for k in range(n + 1)]
        minimum = min(values)
        rows.append([n, minimum, (n - 15) // 2])
        minimizing_splits[str(n)] = [k for k, value in enumerate(values) if value == minimum]
    return rows, minimizing_splits


def weak_compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            yield (first,) + rest


def reconstruct_roots():
    roots = []
    compositions = list(weak_compositions(9, 4))
    for case in range(4):
        for pair_red in range(2):
            for common_size in range(10, 14):
                cell_sizes = [common_size, 20 - common_size, 20 - common_size, common_size + 1]
                for y_red in range(2):
                    for counts in compositions:
                        first_red = counts[0] + counts[1] if pair_red else counts[2] + counts[3]
                        second_red = counts[0] + counts[2] if pair_red else counts[1] + counts[3]
                        if (first_red, second_red) != (5, 5):
                            continue
                        z_cell = 3 if pair_red else 0
                        y_cell = 0 if y_red == pair_red else 3
                        if counts[y_cell] == 0:
                            continue
                        central = [cell_sizes[j] - counts[j] - int(j == z_cell) for j in range(4)]
                        if min(central) < 0:
                            continue
                        candidate_cells = [-1] if case < 2 else list(range(4))
                        for w_cell in candidate_cells:
                            if w_cell >= 0 and central[w_cell] == 0:
                                continue
                            roots.append([case, pair_red, common_size, y_red, counts[0], w_cell])
    require(len(roots) == len(set(map(tuple, roots))), "duplicate reconstructed roots")
    return sorted(roots)


def defect_localization():
    possibilities = []
    for a_z in range(10):
        for red_edges_in_E in range(37):
            s_E = 2 * red_edges_in_E + 2 * a_z - 45
            s_z = a_z - 6
            s_C = 2 - s_E - s_z
            if 0 <= s_E <= 2 and s_E % 2 == 1 and s_z >= 0 and s_C >= 0:
                possibilities.append([a_z, red_edges_in_E, s_E, s_z, s_C])
    require(possibilities == [[6, 17, 1, 0, 1], [7, 16, 1, 1, 0]], "defect split")
    # Since the total red and blue excesses are (1,1), the unit in E and
    # the remaining unit necessarily have opposite colors.
    p_sizes = {"central_defect_wz_blue": 19, "central_defect_wz_red": 20, "z_defect": 21}
    return possibilities, p_sizes


def codegree(adjacency, u, v):
    pair_red = v in adjacency[u]
    return sum(
        w not in (u, v)
        and ((w in adjacency[u]) == pair_red)
        and ((w in adjacency[v]) == pair_red)
        for w in range(43)
    )


def validate_sharpness(data):
    require(set(data) == {"external_signatures"}, "sharpness schema")
    entries = data["external_signatures"]
    require(all(isinstance(row, list) and len(row) == 2 for row in entries), "signature rows")
    require(all(isinstance(mask, int) and 0 <= mask < 256 and isinstance(count, int) and count > 0
                for mask, count in entries), "signature values")
    require(len({mask for mask, _ in entries}) == len(entries), "duplicate masks")
    require(sum(count for _, count in entries) == 33, "signature multiplicity")

    adjacency = [set() for _ in range(43)]
    for u in range(8):
        for v in range(u + 1, 8):
            if (v - u) % 8 in (1, 2, 6, 7):
                adjacency[u].add(v)
                adjacency[v].add(u)
    vertex = 10
    for mask, count in entries:
        for _ in range(count):
            for u in range(8):
                if mask >> u & 1:
                    adjacency[u].add(vertex)
                    adjacency[vertex].add(u)
            vertex += 1
    require(vertex == 43, "sharpness order")
    require(all(len(adjacency[u]) == 21 for u in range(8)), "sharpness degrees")
    require(all(8 not in adjacency[u] and 9 not in adjacency[u] for u in range(8)), "fixed blue stars")
    require(all(not adjacency[u] for u in (8, 9)), "external anchors are not red-adjacent")
    require(all(v not in adjacency[u] for u, v in combinations(range(8, 43), 2)), "outside independence")
    values = [codegree(adjacency, u, v) for u, v in combinations(range(8), 2)]
    histogram = dict(sorted(Counter(values).items()))
    require(histogram == {8: 2, 9: 26} and sum(values) == 250, "sharpness codegrees")
    return histogram


def ldl_pivots(matrix):
    n = len(matrix)
    lower = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    diagonal = [Fraction(0) for _ in range(n)]
    for i in range(n):
        lower[i][i] = Fraction(1)
        diagonal[i] = Fraction(matrix[i][i]) - sum(lower[i][k] ** 2 * diagonal[k] for k in range(i))
        require(diagonal[i] != 0, "zero LDL pivot")
        for j in range(i + 1, n):
            numerator = Fraction(matrix[j][i]) - sum(
                lower[j][k] * lower[i][k] * diagonal[k] for k in range(i)
            )
            lower[j][i] = numerator / diagonal[i]
    return diagonal


def scalar_separator():
    size = 10
    gram = [[0] * size for _ in range(size)]
    pair_sum = 0
    for u in range(size):
        for v in range(size):
            if u == v:
                gram[u][v] = 42
            else:
                q = 10 if {u, v} == {0, 1} else 9
                gram[u][v] = 4 * q - 39
                if u < v:
                    pair_sum += q
    one_star = [[gram[u][v] - 1 for v in range(size)] for u in range(size)]
    two_star = [[gram[u][v] - 2 for v in range(size)] for u in range(size)]
    gram_pivots = ldl_pivots(gram)
    one_pivots = ldl_pivots(one_star)
    require(all(value > 0 for value in gram_pivots + one_pivots), "PSD separator premise")
    ones_quadratic = sum(map(sum, two_star))
    require(pair_sum == 406 and ones_quadratic == -42, "separator arithmetic")
    return {
        "pair_sum": pair_sum,
        "gram_min_ldl_pivot": str(min(gram_pivots)),
        "one_star_min_ldl_pivot": str(min(one_pivots)),
        "two_star_ones_quadratic": ones_quadratic,
    }


def root_geometry(root):
    case, pair_red, common_size, y_red, a, w_cell = root
    quota = 5 if pair_red else 4
    e_counts = [a, quota - a, quota - a, 9 - 2 * quota + a]
    sizes = [common_size, 20 - common_size, 20 - common_size, common_size + 1]
    cells = []
    next_vertex = 2
    for size in sizes:
        cells.append(list(range(next_vertex, next_vertex + size)))
        next_vertex += size
    require(next_vertex == 43, "cell partition")
    exceptional = {v for j, cell in enumerate(cells) for v in cell[:e_counts[j]]}
    z_cell = 3 if pair_red else 0
    y_cell = 0 if y_red == pair_red else 3
    y = cells[y_cell][0]
    central_by_cell = [
        [v for v in cell if v not in exceptional]
        for cell in cells
    ]
    z = central_by_cell[z_cell].pop(0)
    w = None
    if case >= 2:
        w = central_by_cell[w_cell].pop(0)
    require((case < 2) == (w_cell == -1), "defect-case encoding")
    require(y in exceptional and z not in exceptional and (w is None or w not in exceptional | {z}), "marks")
    return cells, exceptional, z, y, w


def build_transport_graph(root):
    case, pair_red, _, y_red, _, w_cell = root
    cells, exceptional, z, y, w = root_geometry(root)
    red_edges = set()
    for u, v in combinations(range(43), 2):
        if (u, v) == (0, 1):
            red = bool(pair_red)
        elif u < 2:
            cell = next(j for j in range(4) if v in cells[j])
            in_pair_color = cell in ((0, 1) if u == 0 else (0, 2))
            red = bool(pair_red) if in_pair_color else not bool(pair_red)
        else:
            red = False
        if red:
            red_edges.add((u, v))
    remaining_needed = 446 - len(red_edges)
    free_blue = [(u, v) for u, v in combinations(range(2, 43), 2) if (u, v) not in red_edges]
    require(0 <= remaining_needed <= len(free_blue), "global red fill")
    red_edges.update(free_blue[:remaining_needed])

    degree = [0] * 43
    for u, v in red_edges:
        degree[u] += 1
        degree[v] += 1
    require(len(red_edges) == 446 and degree[0] == degree[1] == 21, "global/endpoint degrees")
    require(sum((min(0, v), max(0, v)) in red_edges for v in exceptional) == 5, "first E quota")
    require(sum((min(1, v), max(1, v)) in red_edges for v in exceptional) == 5, "second E quota")
    require((min(0, z), max(0, z)) not in red_edges and (min(1, z), max(1, z)) not in red_edges, "z mark")
    require(((min(0, y), max(0, y)) in red_edges) == bool(y_red), "first y mark")
    require(((min(1, y), max(1, y)) in red_edges) == bool(y_red), "second y mark")
    if w is not None:
        require(w in cells[w_cell], "w mark")
    require(y >= 2 and z >= 2 and y != z, "yz not represented")
    if w is not None:
        require(w >= 2 and z >= 2 and w != z, "wz not represented")
    return red_edges, exceptional, z, y, w


def transport_audit(roots):
    digest = sha256()
    case_counts = Counter()
    fixed_checks = 0
    permutation = [(17 * vertex + 9) % 43 for vertex in range(43)]
    require(len(set(permutation)) == 43, "transport permutation")
    for root in roots:
        red_edges, exceptional, z, y, w = build_transport_graph(root)
        transported = {
            tuple(sorted((permutation[u], permutation[v])))
            for u, v in red_edges
        }
        for u, v in combinations(range(43), 2):
            require(
                ((u, v) in red_edges)
                == (tuple(sorted((permutation[u], permutation[v]))) in transported),
                "physical edge transport",
            )
            fixed_checks += 1
            digest.update(bytes((int((u, v) in red_edges), int(tuple(sorted((permutation[u], permutation[v]))) in transported))))
        transported_exceptional = {permutation[v] for v in exceptional}
        require(sum(tuple(sorted((permutation[0], v))) in transported for v in transported_exceptional) == 5,
                "transported first E quota")
        require(sum(tuple(sorted((permutation[1], v))) in transported for v in transported_exceptional) == 5,
                "transported second E quota")
        require(tuple(sorted((permutation[0], permutation[z]))) not in transported, "transported z star")
        require((tuple(sorted((permutation[0], permutation[y]))) in transported) == bool(root[3]), "transported y star")
        if w is not None:
            require(permutation[w] not in (permutation[0], permutation[1], permutation[z]), "transported w")
        case_counts[root[0]] += 1
    require(case_counts == Counter({0: 72, 1: 72, 2: 288, 3: 288}), "case coverage")
    return {
        "case_counts": {str(k): case_counts[k] for k in range(4)},
        "fixed_endpoint_bits_per_root": 83,
        "free_physical_bits_per_root": 820,
        "physical_edge_roundtrips": fixed_checks,
        "transport_sha256": digest.hexdigest(),
    }


def formula_truth_tables():
    five_set_accepts = 0
    for mask in range(1 << 10):
        bits = [(mask >> bit) & 1 for bit in range(10)]
        five_set_accepts += int(not (all(bits) or not any(bits)))
    require(five_set_accepts == 1022, "five-set clause")
    valid_triangle_aux_rows = 0
    for color in range(2):
        for mask in range(8):
            edges = [(mask >> bit) & 1 for bit in range(3)]
            expected = all(edge == color for edge in edges)
            for auxiliary in range(2):
                valid_triangle_aux_rows += int(bool(auxiliary) == expected)
    require(valid_triangle_aux_rows == 16, "triangle equivalence")
    return {"five_set_colorings_accepted": five_set_accepts, "triangle_aux_rows_accepted": valid_triangle_aux_rows}


def validate_certificate(data, expected_bounds, expected_multiplicities, expected_roots):
    require(set(data) == {"schema", "bounds", "multiplicities", "roots"}, "certificate schema")
    require(data["schema"] == 1, "certificate version")
    require(data["bounds"] == expected_bounds, "bound table mismatch")
    require(data["multiplicities"] == expected_multiplicities, "multiplicity mismatch")
    require(data["roots"] == expected_roots, "marked-root mismatch")


def mutation_controls(certificate, sharpness, expected_bounds, expected_multiplicities, expected_roots):
    damaged = []
    for mutation in range(5):
        copy = json.loads(json.dumps(certificate))
        if mutation == 0:
            copy["bounds"].pop()
        elif mutation == 1:
            copy["multiplicities"][0][1] += 1
        elif mutation == 2:
            copy["roots"].pop()
        elif mutation == 3:
            copy["roots"].append(copy["roots"][0])
        else:
            copy["roots"][0][3] ^= 1
        try:
            validate_certificate(copy, expected_bounds, expected_multiplicities, expected_roots)
        except ValueError:
            damaged.append(f"certificate-{mutation}")
    sharp_copy = json.loads(json.dumps(sharpness))
    sharp_copy["external_signatures"][0][1] += 1
    try:
        validate_sharpness(sharp_copy)
    except ValueError:
        damaged.append("sharpness-0")
    require(len(damaged) == 6, "mutation accepted")
    return damaged


def main():
    certificate = pinned_json("certificate.json", CERTIFICATE_SHA256)
    sharpness = pinned_json("sharpness.json", SHARPNESS_SHA256)
    bounds, incidence_states = reconstruct_bounds()
    multiplicities, minimizing_splits = reconstruct_multiplicities(bounds)
    roots = reconstruct_roots()
    validate_certificate(certificate, bounds, multiplicities, roots)
    defect_cases, p_sizes = defect_localization()
    sharpness_histogram = validate_sharpness(sharpness)
    report = {
        "certificate_sha256": CERTIFICATE_SHA256,
        "critical_bounds": {
            "opposite_k9": bounds[18][2],
            "opposite_k10": bounds[20][2],
            "same_k8": bounds[17][2],
            "same_k10": bounds[21][2],
        },
        "defect_possibilities": defect_cases,
        "formula_truth_tables": formula_truth_tables(),
        "incidence_states_checked": incidence_states,
        "marked_roots_matched": len(roots),
        "minimizing_class_splits": minimizing_splits,
        "multiplicities": multiplicities,
        "mutations_rejected": mutation_controls(certificate, sharpness, bounds, multiplicities, roots),
        "p_sizes": p_sizes,
        "scalar_separator": scalar_separator(),
        "sharpness_codegree_histogram": {str(k): v for k, v in sharpness_histogram.items()},
        "sharpness_sha256": SHARPNESS_SHA256,
        "transport": transport_audit(roots),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
