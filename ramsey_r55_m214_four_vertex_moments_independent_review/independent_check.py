#!/usr/bin/env python3
"""Clean-room exact checker for the complete-four-support M214 witness.

Run this after the target's reproduce.py.  This module imports no target or
predecessor Python code and uses no solver or floating-point arithmetic.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
import argparse
import json
import math
from pathlib import Path


N = 43
TARGET_DIR = Path(__file__).resolve().parent.parent / "ramsey_r55_m214_complete_four_vertex_moments"
CERTIFICATE_SHA256 = "3f3fe88ace02db3797d352e4766f807fd82adb3e72658e37e6d9e532e786ef0f"
POINTS_SHA256 = "7bb543141b8ed264f95fac33954d681268e876fd0ddeed11e29afad3f56ab4e7"
MOMENTS_SHA256 = "a5fa2ed62dec1491eacaad12b1877b98478631bcbf342d7bda80af8ddd0b9912"
FOUR_SHA256 = "418f4459e227c232ecabfdb9e7b47461b4c938e2d1065493f874ecd266eaab13"
OLD_POINTS_SHA256 = "c4bb5b1ccf67291ebf430a0cc5ea1e2a0dcf5d95998c4fc4b993418f484b78e4"
OLD_MOMENTS_SHA256 = "99f9385f47f98d46093d973e3b6ccc2b84fac37b6f1d7738f9c10dac65a68210"
OPB_SHA256 = "9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609"
OPB_HEADER = b"* #variable= 98758 #constraint= 2983003 #equal= 87 intsize= 64\n"

TYPE_ORDER = ("u", "v", "p", "a", "b", "o", "h", "ca", "cb", "co")
TYPE_INDEX = {name: index for index, name in enumerate(TYPE_ORDER)}
VERTEX_TYPE = {0: "u", 1: "v", 2: "p", 14: "o", 28: "ca", 29: "cb"}
VERTEX_TYPE.update({v: "a" for v in range(3, 8)})
VERTEX_TYPE.update({v: "b" for v in range(8, 14)})
VERTEX_TYPE.update({v: "h" for v in range(15, 28)})
VERTEX_TYPE.update({v: "co" for v in range(30, 43)})
E = frozenset(range(2, 15))
H = frozenset(range(15, 28))
EA = frozenset(range(2, 8))
EB = frozenset(range(8, 14))
X = frozenset(range(2, 43)) - H

EDGE_PARAMETERS = {
    "pA": F(5, 6), "pB": F(23, 36), "pO": F(0),
    "AA": F(5, 6), "AB": F(17, 90), "AO": F(7, 10),
    "BB": F(4, 5), "BO": F(5, 12),
    "upA": F(8, 15), "upB": F(0), "upO": F(67, 195),
    "aA": F(5, 6), "aB": F(4, 25), "aO": F(901, 1950),
    "bA": F(13, 60), "bB": F(13, 15), "bO": F(71, 156),
    "oA": F(0), "oB": F(0), "oO": F(8, 13),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def red13(left, right):
    return ((left - 15) - (right - 15)) % 13 in {1, 5, 8, 12}


def edge_value(left, right):
    if left > right:
        left, right = right, left
    require(0 <= left < right < N, "edge domain")
    if (left, right) == (0, 1):
        return F(1)
    if left in (0, 1):
        if left == 0:
            return F(int(right in H or right in EA or right == 28))
        return F(int(right in H or right in EB or right == 29))
    if left in H and right in H:
        return F(int(red13(left, right)))
    if (left in H) != (right in H):
        exterior = right if left in H else left
        return F(6, 13) if exterior in E else F(3, 5)
    if left in E and right in E:
        lt, rt = VERTEX_TYPE[left], VERTEX_TYPE[right]
        if "p" in (lt, rt):
            other = rt if lt == "p" else lt
            return EDGE_PARAMETERS[{"a": "pA", "b": "pB", "o": "pO"}[other]]
        key = {
            ("a", "a"): "AA", ("a", "b"): "AB", ("a", "o"): "AO",
            ("b", "b"): "BB", ("b", "o"): "BO",
        }[tuple(sorted((lt, rt)))]
        return EDGE_PARAMETERS[key]
    if (left in E) != (right in E):
        exceptional = left if left in E else right
        central = right if left in E else left
        row = {"p": "up", "a": "a", "b": "b", "o": "o"}[VERTEX_TYPE[exceptional]]
        column = {"ca": "A", "cb": "B", "co": "O"}[VERTEX_TYPE[central]]
        return EDGE_PARAMETERS[row + column]
    lt, rt = VERTEX_TYPE[left], VERTEX_TYPE[right]
    special_left, special_right = lt in {"ca", "cb"}, rt in {"ca", "cb"}
    if special_left and special_right:
        return F(1)
    if special_left != special_right:
        return F(2, 5)
    return F(8, 15)


def physical_maps():
    edge = {pair: index for index, pair in enumerate(combinations(range(N), 2), 1)}
    roots = []
    patterns = (("H", "A"), ("BB", "BO", "OO"), ("B", "O"),
                ("BB", "BO", "OO"), ("HO", "AB"))
    for family in range(5):
        for common in range(9, 14):
            for k in range(7):
                sizes = (k, 6-k, 6-k, 1+k, common-k, 14-common+k,
                         14-common+k, common-k)
                cells, first = [], 2
                for size in sizes:
                    cells.append(tuple(range(first, first + size)))
                    first += size
                require(first == N, "root partition")
                for pattern in patterns[family]:
                    offset = 0 if family < 2 else 4
                    if any(pattern.count(label) > sizes[offset + i]
                           for i, label in enumerate("HABO")):
                        continue
                    core = tuple(sorted(cells[0] + cells[4]))
                    exterior = tuple(v for v in range(2, N) if v not in core)
                    roots.append(((family, common, k, pattern), core, exterior))
    require(len(roots) == 389 and roots[48][0] == (0, 13, 0, "A"), "root order")
    missed_support, q_support = set(), set()
    for _, core, exterior in roots:
        for a, b in combinations(exterior, 2):
            missed_support.update((a, b, h) for h in core)
            q_support.update((a, b, i, j) for i, j in combinations(core, 2))
    require((len(missed_support), len(q_support)) == (10612, 74513), "coordinate support")
    missed = {key: 13634 + index for index, key in enumerate(sorted(missed_support))}
    q = {key: 24246 + index for index, key in enumerate(sorted(q_support))}
    return edge, roots, missed, q


def read_certificate(path):
    require(file_hash(path) == CERTIFICATE_SHA256, "certificate hash")
    data = json.loads(path.read_text(encoding="ascii"))
    require(set(data) == {"denominator", "templates"}, "certificate schema")
    denominator = int(data["denominator"])
    require(denominator > 0, "certificate denominator")
    templates, entries = {}, 0
    for row in data["templates"]:
        require(set(row) == {"types", "edges", "atoms"}, "template schema")
        types = tuple(row["types"])
        edges = tuple(map(F, row["edges"]))
        require(len(types) == 4 and tuple(sorted(types)) == types and all(0 <= t < 10 for t in types),
                "template types")
        require(len(edges) == 6 and all(0 <= x <= 1 for x in edges), "template edges")
        atoms = {int(mask): int(mass) for mask, mass in row["atoms"].items()}
        require(len(atoms) == len(row["atoms"]) and atoms and
                all(0 <= mask < 64 and mass > 0 for mask, mass in atoms.items()), "template atoms")
        require(sum(atoms.values()) == denominator, "template normalization")
        key = (types, edges)
        require(key not in templates, "duplicate template")
        templates[key] = atoms
        entries += len(atoms)
    require((len(templates), entries) == (463, 4371), "template coverage")
    return denominator, templates


def canonical_template(vertices, edge_values):
    def key(order):
        return (
            tuple(TYPE_INDEX[VERTEX_TYPE[v]] for v in order),
            tuple(edge_values[tuple(sorted(pair))] for pair in combinations(order, 2)),
            order,
        )
    order = min(permutations(vertices), key=key)
    full = key(order)
    return (full[0], full[1]), order


def transport_atoms(atoms, order, vertices):
    canonical_pairs = tuple(combinations(range(4), 2))
    physical_pairs = tuple(combinations(vertices, 2))
    result = {}
    for mask, mass in atoms.items():
        physical_mask = 0
        for bit, (i, j) in enumerate(canonical_pairs):
            if mask >> bit & 1:
                actual = tuple(sorted((order[i], order[j])))
                physical_mask |= 1 << physical_pairs.index(actual)
        require(physical_mask not in result, "transport collision")
        result[physical_mask] = mass
    return result


def read_point(path, denominator):
    require(file_hash(path) == POINTS_SHA256, "new point hash")
    values = [0]
    with path.open(encoding="ascii") as handle:
        require(next(handle, "") == "variable\tvalue\n", "point header")
        for index in range(1, 98759):
            fields = next(handle, "").split()
            require(len(fields) == 2 and fields[0] == str(index), "point coordinate order")
            value = F(fields[1])
            require(0 <= value <= 1 and (value * denominator).denominator == 1, "point box/scale")
            values.append(int(value * denominator))
        require(handle.read() == "", "extra point coordinates")
    return values


def read_moments(path, denominator=None, expected_hash=None):
    if expected_hash is not None:
        require(file_hash(path) == expected_hash, "moment hash")
    values = {}
    with path.open(encoding="ascii") as handle:
        require(next(handle, "") == "a\tb\tc\tm_a\tm_b\tm_c\n", "moment header")
        for triple in combinations(range(N), 3):
            fields = next(handle, "").split()
            require(len(fields) == 6 and tuple(map(int, fields[:3])) == triple, "moment order")
            row = tuple(map(F, fields[3:]))
            require(all(0 <= x <= 1 for x in row), "moment box")
            for h, value in zip(triple, row):
                key = tuple(v for v in triple if v != h) + (h,)
                if denominator is None:
                    values[key] = value
                else:
                    require((value * denominator).denominator == 1, "moment scale")
                    values[key] = int(value * denominator)
        require(handle.read() == "", "extra moment rows")
    require(len(values) == 37023, "moment support")
    return values


def atom_values(triple, point, moments, denominator, edge, triangle_index):
    a, b, c = triple
    A, B, C = (point[edge[pair]] for pair in combinations(triple, 2))
    ma = moments[(b, c, a)]
    mb = moments[(a, c, b)]
    mc = moments[(a, b, c)]
    u = ma + A + B - denominator
    v = mb + A + C - denominator
    w = mc + B + C - denominator
    z = point[triangle_index[triple]]
    atoms = (
        denominator-A-B-C+u+v+w-z, A-u-v+z, B-u-w+z, u-z,
        C-v-w+z, v-z, w-z, z,
    )
    require(min(atoms) >= 0 and sum(atoms) == denominator, "triangle probability")
    return atoms


def evaluate_base_opb(path, point, denominator):
    digest = sha256()
    rows = equalities = size = 0
    with path.open("rb") as handle:
        header = handle.readline()
        require(header == OPB_HEADER, "OPB header")
        digest.update(header)
        size += len(header)
        for raw in handle:
            digest.update(raw)
            size += len(raw)
            fields = raw.split()
            require(len(fields) >= 5 and len(fields) % 2 == 1 and fields[-1] == b";", "OPB syntax")
            relation = fields[-3]
            require(relation in (b"=", b">="), "OPB relation")
            slack = -int(fields[-2]) * denominator
            for pos in range(0, len(fields)-3, 2):
                token = fields[pos+1]
                require(token.startswith(b"x"), "OPB variable token")
                index = int(token[1:])
                require(0 < index < len(point), "OPB variable index")
                slack += int(fields[pos]) * point[index]
            require(slack == 0 if relation == b"=" else slack >= 0, f"OPB row {rows+1}")
            rows += 1
            equalities += relation == b"="
    require((rows, equalities, size) == (2983003, 87, 511537255), "OPB coverage")
    require(digest.hexdigest() == OPB_SHA256, "OPB hash")
    return rows, equalities


def global_triangle_checks(point, moments, denominator, edge, missed):
    triangle_index = {triple: 904 + index for index, triple in enumerate(combinations(range(N), 3))}
    triangle_atoms = {}
    red_codegree = {pair: 0 for pair in edge}
    blue_codegree = {pair: 0 for pair in edge}
    red_local = [0] * N
    blue_local = [0] * N
    for triple in combinations(range(N), 3):
        atoms = atom_values(triple, point, moments, denominator, edge, triangle_index)
        triangle_atoms[triple] = atoms
        for pair in combinations(triple, 2):
            red_codegree[pair] += atoms[7]
            blue_codegree[pair] += atoms[0]
        for vertex in triple:
            red_local[vertex] += atoms[7]
            blue_local[vertex] += atoms[0]
    require(len(triangle_atoms) * 8 == 98728, "triangle atom rows")

    degree = []
    for vertex in range(N):
        observed = sum(point[edge[tuple(sorted((vertex, other)))]] for other in range(N) if other != vertex)
        expected = (20 if vertex in E else 21) * denominator
        require(observed == expected, "degree equality")
        degree.append(expected // denominator)
    # The campaign label M=214 is not an edge count.  The explicit degree
    # profile 20^13 21^30 has red-edge expectation 445.
    require(sum(point[index] for index in edge.values()) == 445 * denominator, "red edge total")
    for pair, index in edge.items():
        require(red_codegree[pair] <= 13 * point[index], "red codegree")
        require(blue_codegree[pair] <= 13 * (denominator-point[index]), "blue codegree")

    for key, index in missed.items():
        require(point[index] == moments[key], "shared wedge coordinate")
    star_rows = 0
    for h in range(N):
        for a in range(N):
            if a == h:
                continue
            xa = point[edge[tuple(sorted((a, h)))]]
            red = blue = 0
            for b in range(N):
                if b in (a, h):
                    continue
                m = moments[tuple(sorted((a, b))) + (h,)]
                xb = point[edge[tuple(sorted((b, h)))]]
                blue += m
                red += m + xa + xb - denominator
            require(red == (degree[h]-1) * xa, "red star equality")
            require(blue == (41-degree[h]) * (denominator-xa), "blue star equality")
            star_rows += 1
    require(star_rows == 1806, "star row count")

    upper = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
    red_deficiency = sum(upper[degree[v]] * denominator - red_local[v] for v in range(N))
    blue_deficiency = sum(upper[42-degree[v]] * denominator - blue_local[v] for v in range(N))
    require((red_deficiency, blue_deficiency) == (301*denominator, 303*denominator), "deficiency totals")
    return triangle_index, triangle_atoms, {
        "triangle_atom_rows": 98728,
        "global_star_equalities": star_rows,
        "red_codegree_rows": 903,
        "blue_codegree_rows": 903,
        "red_edge_expectation": 445,
        "red_deficiency_sum": 301,
        "blue_deficiency_sum": 303,
    }


def moment_hull_slacks(common, degree_sum, pair_count, S, Q, selector, edge_value_scaled, denominator):
    constant = 45 - common - degree_sum
    maximum = 64 - common - degree_sum
    inactive = 2*denominator - selector - edge_value_scaled
    for tangent in range(maximum):
        rhs = tangent*constant - math.comb(tangent+1, 2)
        guard = rhs + tangent*(common+39)
        require(guard >= 0, "valid lower guard")
        yield Q - tangent*S + math.comb(tangent+1, 2)*denominator + guard*inactive
    guard = -(maximum-1)*constant + 2*pair_count
    yield (maximum-1)*S - 2*Q + guard*inactive


def check_predecessor_suffix(point, denominator, edge, roots, missed, q, triangle_index):
    require([point[13245+r] for r in range(389)] ==
            [denominator if r == 48 else 0 for r in range(389)], "selected root")
    coupled_rows = hull_rows = active_relations = 0
    active_S, active_Q = set(), set()
    for root_index, (_, core, exterior) in enumerate(roots):
        common = len(core)
        pairs = tuple(combinations(exterior, 2))
        pair_count = len(pairs)
        selector = point[13245+root_index]
        for i, j in combinations(core, 2):
            degree_sum = (20 if i in E else 21) + (20 if j in E else 21)
            maximum = 64-common-degree_sum
            xij = point[edge[i, j]]
            Q = sum(point[q[a, b, i, j]] for a, b in pairs)
            adjacent = sum(point[edge[tuple(sorted((h, v)))]]
                           for h in (i, j) for v in core if h != v)
            triangles = sum(point[triangle_index[tuple(sorted((i, j, v)))]] for v in exterior)
            S = (45-common-degree_sum)*denominator + adjacent + triangles
            coupled = (math.comb(maximum, 2)*xij +
                       (pair_count-math.comb(maximum, 2))*(denominator-selector) - Q)
            require(coupled >= 0, "coupled-column row")
            slacks = tuple(moment_hull_slacks(common, degree_sum, pair_count, S, Q,
                                              selector, xij, denominator))
            require(min(slacks) >= 0, "reanchored moment hull")
            coupled_rows += 1
            hull_rows += len(slacks)
            if selector == denominator and xij == denominator:
                active_S.add(F(S, denominator))
                active_Q.add(F(Q, denominator))
                for a, b in pairs:
                    require(point[missed[a, b, i]] == point[missed[a, b, j]], "active equal wedges")
                    require(14*point[q[a, b,i,j]] == 3*point[missed[a,b,i]], "active rho relation")
                    active_relations += 1
    require((coupled_rows, hull_rows) == (21762, 264560), "suffix row coverage")
    require((active_S, active_Q) == ({F(5)}, {F(117, 7)}), "active aggregates")
    require(active_relations == 9828, "active rho support")
    return {
        "coupled_column_rows": coupled_rows,
        "reanchored_hull_rows": hull_rows,
        "active_rho_relations": active_relations,
        "active_S": "5",
        "active_Q": "117/7",
    }


def parse_four_line(raw, vertices, denominator):
    fields = raw.split()
    require(len(fields) >= 5 and tuple(map(int, fields[:4])) == vertices, "four-set order")
    atoms, previous = {}, -1
    for field in fields[4:]:
        parts = field.split(b":")
        require(len(parts) == 2, "four-set atom syntax")
        mask, mass = map(int, parts)
        require(previous < mask < 64 and mass > 0, "four-set atom order/value")
        atoms[mask] = mass
        previous = mask
    require(sum(atoms.values()) == denominator, "four-set normalization")
    return atoms


def marginal(atoms, selected_bits):
    result = [0] * (1 << len(selected_bits))
    for mask, mass in atoms.items():
        state = sum(((mask >> bit) & 1) << position
                    for position, bit in enumerate(selected_bits))
        result[state] += mass
    return tuple(result)


def footprint(atoms, pairs, a, b, i, j):
    red = pairs.index((i, j))
    blue = [pairs.index(tuple(sorted((v, h)))) for v in (a, b) for h in (i, j)]
    return sum(mass for mask, mass in atoms.items()
               if mask >> red & 1 and all(not (mask >> bit & 1) for bit in blue))


def one_anchor_event(atoms, pairs, anchor, i, j):
    red = pairs.index((i, j))
    blue = [pairs.index(tuple(sorted((anchor, h)))) for h in (i, j)]
    return sum(mass for mask, mass in atoms.items()
               if mask >> red & 1 and all(not (mask >> bit & 1) for bit in blue))


def check_four_stream(path, point, denominator, edge, q, triangle_atoms, templates):
    by_four = defaultdict(list)
    for key, index in q.items():
        by_four[tuple(sorted(key))].append((key, index))
    edge_values = {pair: F(point[index], denominator) for pair, index in edge.items()}
    require(all(edge_values[pair] == edge_value(*pair) for pair in edge), "explicit edge pattern")
    digest = sha256()
    sets = marginal_rows = footprint_rows = nonzeros = frechet_checks = edge_checks = 0
    used_templates = set()
    with path.open("rb") as handle:
        header = handle.readline()
        digest.update(header)
        require(header == f"four-vertex-atoms\t43\t{denominator}\n".encode(), "four-set header")
        for vertices in combinations(range(N), 4):
            raw = handle.readline()
            require(raw, "missing four-set")
            digest.update(raw)
            atoms = parse_four_line(raw, vertices, denominator)
            pairs = tuple(combinations(vertices, 2))
            template_key, order = canonical_template(vertices, edge_values)
            require(template_key in templates, "missing compact template")
            require(atoms == transport_atoms(templates[template_key], order, vertices), "template transport")
            used_templates.add(template_key)
            for bit, pair in enumerate(pairs):
                observed = sum(mass for mask, mass in atoms.items() if mask >> bit & 1)
                require(observed == point[edge[pair]], "physical edge marginal")
                edge_checks += 1
            for triple in combinations(vertices, 3):
                bits = [pairs.index(pair) for pair in combinations(triple, 2)]
                require(marginal(atoms, bits) == triangle_atoms[triple], "physical triangle marginal")
                marginal_rows += 8
            for (a, b, i, j), index in by_four[vertices]:
                require(footprint(atoms, pairs, a, b, i, j) == point[index], "physical footprint")
                footprint_rows += 1
            for i, j in pairs:
                a, b = sorted(set(vertices) - {i, j})
                ta = one_anchor_event(atoms, pairs, a, i, j)
                tb = one_anchor_event(atoms, pairs, b, i, j)
                xij = sum(mass for mask, mass in atoms.items() if mask >> pairs.index((i, j)) & 1)
                both = footprint(atoms, pairs, a, b, i, j)
                require(max(0, ta+tb-xij) <= both <= min(ta, tb), "Frechet projection")
                frechet_checks += 1
            sets += 1
            nonzeros += len(atoms)
        require(handle.read() == b"", "extra four-sets")
    require(digest.hexdigest() == FOUR_SHA256, "four-stream hash")
    require(used_templates == set(templates), "unused compact template")
    require((sets, edge_checks, marginal_rows, footprint_rows, nonzeros, frechet_checks) ==
            (123410, 740460, 3949120, 74513, 1903846, 740460), "four-set coverage")
    return {
        "four_sets": sets,
        "physical_edge_marginals": edge_checks,
        "triangle_marginal_equalities": marginal_rows,
        "footprint_equalities": footprint_rows,
        "physical_nonzero_atoms": nonzeros,
        "frechet_checks": frechet_checks,
        "compact_templates_used": len(used_templates),
    }


def read_old_point(path):
    require(file_hash(path) == OLD_POINTS_SHA256, "old point hash")
    values = [None]
    header = "variable\tbaseline_rho=3/14\trepaired_rho=3/14\trepaired_rho=10/39\n"
    with path.open(encoding="ascii") as handle:
        require(next(handle, "") == header, "old point header")
        for index in range(1, 98759):
            fields = next(handle, "").split()
            require(len(fields) == 4 and fields[0] == str(index), "old point order")
            row = tuple(map(F, fields[2:]))
            require(all(0 <= x <= 1 for x in row), "old point box")
            values.append(row)
        require(handle.read() == "", "extra old coordinates")
    require(all(a == b for a, b in values[1:24246]), "old fixed triangle/wedge coordinates")
    return values


def old_triangle_atoms(triple, point, moments, edge, triangle_index, endpoint):
    a, b, c = triple
    A, B, C = (point[edge[pair]][endpoint] for pair in combinations(triple, 2))
    ma, mb, mc = moments[(b,c,a)], moments[(a,c,b)], moments[(a,b,c)]
    u, v, w = ma+A+B-1, mb+A+C-1, mc+B+C-1
    z = point[triangle_index[triple]][endpoint]
    atoms = (1-A-B-C+u+v+w-z, A-u-v+z, B-u-w+z, u-z,
             C-v-w+z, v-z, w-z, z)
    require(min(atoms) >= 0 and sum(atoms) == 1, "old triangle distribution")
    return atoms


def triple_event(atoms, triple, anchor, i, j):
    pairs = tuple(combinations(triple, 2))
    red = pairs.index(tuple(sorted((i, j))))
    blue = [pairs.index(tuple(sorted((anchor, h)))) for h in (i, j)]
    return sum(mass for mask, mass in enumerate(atoms)
               if mask >> red & 1 and all(not(mask >> bit & 1) for bit in blue))


def check_old_separator(point_path, moment_path, edge, q, triangle_index):
    old = read_old_point(point_path)
    moments = read_moments(moment_path, expected_hash=OLD_MOMENTS_SHA256)
    atoms = {}
    for endpoint in range(2):
        for triple in combinations(range(N), 3):
            atoms[endpoint, triple] = old_triangle_atoms(triple, old, moments, edge, triangle_index, endpoint)
    upper_violations = [0, 0]
    lower_violations = [0, 0]
    target_slacks = []
    target_upper = None
    for (a, b, i, j), index in q.items():
        triple_a = tuple(sorted((a, i, j)))
        triple_b = tuple(sorted((b, i, j)))
        for endpoint in range(2):
            ta = triple_event(atoms[endpoint, triple_a], triple_a, a, i, j)
            tb = triple_event(atoms[endpoint, triple_b], triple_b, b, i, j)
            xij = old[edge[i,j]][endpoint]
            lower, upper = max(F(0), ta+tb-xij), min(ta, tb)
            value = old[index][endpoint]
            lower_violations[endpoint] += value < lower
            upper_violations[endpoint] += value > upper
            if (a,b,i,j) == (2,30,15,16):
                target_upper = upper
                target_slacks.append(upper-value)
    require(upper_violations == [32437,32437], "old upper violation count")
    require(target_upper == F(6059,141960), "separator upper")
    require(target_slacks == [-F(493,141960), -F(137,10920)], "separator endpoint slacks")
    return {
        "old_upper_violations": upper_violations,
        "old_lower_violations": lower_violations,
        "separator_upper": str(target_upper),
        "separator_slacks": list(map(str, target_slacks)),
        "excluded_affine_interval": ["3/14", "10/39"],
    }


def self_tests():
    vertices = (2, 9, 16, 30)
    pairs = tuple(combinations(vertices, 2))
    checked = 0
    for mask in range(64):
        atoms = {mask: 1}
        for i, j in pairs:
            a, b = sorted(set(vertices)-{i,j})
            ta = one_anchor_event(atoms, pairs, a, i, j)
            tb = one_anchor_event(atoms, pairs, b, i, j)
            both = footprint(atoms, pairs, a, b, i, j)
            xij = (mask >> pairs.index((i,j))) & 1
            require(max(0,ta+tb-xij) <= both <= min(ta,tb), "Boolean Frechet test")
            checked += 1
        for order in permutations(vertices):
            moved = transport_atoms(atoms, order, vertices)
            red_edges = {
                frozenset((order[i], order[j]))
                for bit, (i, j) in enumerate(combinations(range(4), 2))
                if mask >> bit & 1
            }
            expected_mask = sum(
                1 << bit for bit, pair in enumerate(pairs)
                if frozenset(pair) in red_edges
            )
            require(moved == {expected_mask: 1}, "literal transport test")
            checked += 1
    require(checked == 1920, "self-test coverage")
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path, help="completed output directory from target reproduce.py")
    args = parser.parse_args()
    work = args.work.resolve()
    denominator, templates = read_certificate(TARGET_DIR / "certificate.json")
    require(file_hash(work / "moments.tsv") == MOMENTS_SHA256, "new moment file hash")
    point = read_point(work / "points.tsv", denominator)
    moments = read_moments(work / "moments.tsv", denominator)
    edge, roots, missed, q = physical_maps()
    opb_rows, opb_equalities = evaluate_base_opb(
        work / "prior/prior/prior/m214-3323.opb", point, denominator)
    triangle_index, triangle_atoms, global_stats = global_triangle_checks(
        point, moments, denominator, edge, missed)
    suffix_stats = check_predecessor_suffix(
        point, denominator, edge, roots, missed, q, triangle_index)
    four_stats = check_four_stream(
        work / "four-atoms.tsv", point, denominator, edge, q, triangle_atoms, templates)
    separator_stats = check_old_separator(
        work / "prior/points.tsv", work / "prior/moments.tsv", edge, q, triangle_index)
    prior_full_rows = (opb_rows + global_stats["triangle_atom_rows"] +
                       global_stats["global_star_equalities"] +
                       global_stats["red_codegree_rows"] +
                       global_stats["blue_codegree_rows"] +
                       suffix_stats["coupled_column_rows"] +
                       suffix_stats["reanchored_hull_rows"])
    prior_equalities = opb_equalities + global_stats["global_star_equalities"]
    four_nonnegative = 64 * four_stats["four_sets"]
    total_rows = (prior_full_rows + four_nonnegative + four_stats["four_sets"] +
                  four_stats["triangle_marginal_equalities"] +
                  four_stats["footprint_equalities"])
    total_equalities = (prior_equalities + four_stats["four_sets"] +
                        four_stats["triangle_marginal_equalities"] +
                        four_stats["footprint_equalities"])
    require((prior_full_rows, prior_equalities, total_rows, total_equalities) ==
            (3371665, 1893, 15416948, 4148936), "full formula counts")
    report = {
        "status": "INDEPENDENT_EXACT_M214_FOUR_SUPPORT_SURVIVOR",
        "base_opb_rows": opb_rows,
        "base_opb_equalities": opb_equalities,
        "common_denominator": str(denominator),
        "certificate_sha256": CERTIFICATE_SHA256,
        "four_nonnegative_rows": four_nonnegative,
        "normalization_equalities": four_stats["four_sets"],
        "prior_full_rows": prior_full_rows,
        "total_equalities": total_equalities,
        "total_rows": total_rows,
        "total_variables": 125169 + four_nonnegative,
        "self_test_instances": self_tests(),
        **global_stats,
        **suffix_stats,
        **four_stats,
        **separator_stats,
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
