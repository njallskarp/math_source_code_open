#!/usr/bin/env python3
"""Independent exact check of Discovery Net artifact bafkreieymqno...ywbm.

The implementation uses the quotient ring Q[T]/(Phi_42), polynomial
extended Euclid for division, and a DSATUR-style exhaustive enumeration.
It does not import the reviewed source or read its generated graph.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import reduce as fold
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
import sys
import time


PHI = (1, 1, 0, -1, -1, 0, 1, 0, -1, -1, 0, 1, 1)
DEGREE = 12
ZERO = (Fraction(0),) * DEGREE
ONE = (Fraction(1),) + ZERO[1:]
EXPECTED_ROWS_SHA256 = "f90259563b3c96a57a07618318c18b4e410e49bf2b3613045cf82a296091e592"


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def trim(p: list[Fraction]) -> list[Fraction]:
    while p and p[-1] == 0:
        p.pop()
    return p


def poly_add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += value
    return trim(out)


def poly_sub(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    return poly_add(a, [-value for value in b])


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    if not a or not b:
        return []
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def poly_divmod(a: list[Fraction], b: list[Fraction]) -> tuple[list[Fraction], list[Fraction]]:
    require(bool(b), "polynomial division by zero")
    remainder = a[:]
    quotient = [Fraction(0)] * max(1, len(a) - len(b) + 1)
    while remainder and len(remainder) >= len(b):
        shift = len(remainder) - len(b)
        coeff = remainder[-1] / b[-1]
        quotient[shift] += coeff
        for i, value in enumerate(b):
            remainder[i + shift] -= coeff * value
        trim(remainder)
    return trim(quotient), remainder


def poly_inverse_mod(a: list[Fraction], modulus: list[Fraction]) -> list[Fraction]:
    """Return a^(-1) modulo modulus by polynomial extended Euclid."""
    old_r, r = modulus[:], trim(a[:])
    old_s, s = [], [Fraction(1)]
    while r:
        quotient, remainder = poly_divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, poly_sub(old_s, poly_mul(quotient, s))
    require(len(old_r) == 1 and old_r[0] != 0, "noninvertible field element")
    return [value / old_r[0] for value in old_s]


def reduce_poly(values) -> tuple[Fraction, ...]:
    out = [Fraction(value) for value in values]
    out += [Fraction(0)] * max(0, DEGREE - len(out))
    for j in range(len(out) - 1, DEGREE - 1, -1):
        lead = out[j]
        if lead:
            for k in range(DEGREE):
                out[j - DEGREE + k] -= lead * PHI[k]
    return tuple(out[:DEGREE])


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(a, value):
    return tuple(value * x for x in a)


def mul(a, b):
    return reduce_poly(poly_mul(list(a), list(b)))


T = reduce_poly((0, 1))


def power(base, exponent: int):
    require(exponent >= 0, "negative exponent passed to power")
    result = ONE
    factor = base
    while exponent:
        if exponent & 1:
            result = mul(result, factor)
        factor = mul(factor, factor)
        exponent >>= 1
    return result


T_POWERS = tuple(power(T, k) for k in range(42))


def t_power(exponent: int):
    return T_POWERS[exponent % 42]


def inverse(a):
    require(a != ZERO, "zero has no inverse")
    candidate = reduce_poly(poly_inverse_mod(list(a), list(map(Fraction, PHI))))
    require(mul(a, candidate) == ONE, "extended-Euclid inverse failed")
    return candidate


def conjugate(a):
    result = ZERO
    for exponent, coefficient in enumerate(a):
        result = add(result, scale(t_power(-exponent), coefficient))
    return result


def norm(a):
    return mul(a, conjugate(a))


def host_coordinates():
    p = inverse(sub(t_power(24), t_power(-24)))
    q = neg(mul(t_power(-7), inverse(sub(t_power(6), t_power(-6)))))
    r = neg(mul(t_power(7), inverse(sub(t_power(12), t_power(-12)))))
    return [mul(base, t_power(6 * j)) for base in (p, q, r) for j in range(7)]


def integerize(points):
    denominator = 1
    for point in points:
        for value in point:
            denominator = denominator * value.denominator // gcd(denominator, value.denominator)
    integer_points = [tuple(int(value * denominator) for value in point) for point in points]
    return integer_points, denominator


def pair_inventory(points, denominator):
    edges = []
    distance3 = []
    sqrt3 = []
    sqrt7 = []
    targets = {
        denominator * denominator: edges,
        9 * denominator * denominator: distance3,
        3 * denominator * denominator: sqrt3,
        7 * denominator * denominator: sqrt7,
    }
    for i, j in combinations(range(len(points)), 2):
        squared = norm(sub(points[i], points[j]))
        for target, output in targets.items():
            if squared == scale(ONE, target):
                output.append((i, j))
                break
    return edges, distance3, sqrt3, sqrt7


def enumerate_potentials(constraints):
    pair_constraints = [row for row in constraints if len(row) == 2]
    adjacency = [set() for _ in range(21)]
    incident = [[] for _ in range(21)]
    for row in constraints:
        for vertex in row:
            incident[vertex].append(row)
    for a, b in pair_constraints:
        adjacency[a].add(b)
        adjacency[b].add(a)

    colours = [-1] * 21
    colours[0], colours[7], colours[14] = 0, 1, 2
    solutions = []
    nodes = 0

    def allowed(vertex):
        domain = {0, 1, 2, 3}
        domain -= {colours[other] for other in adjacency[vertex] if colours[other] >= 0}
        for row in incident[vertex]:
            other_values = [colours[other] for other in row if other != vertex]
            if all(value >= 0 for value in other_values):
                forbidden = 0
                for value in other_values:
                    forbidden ^= value
                domain.discard(forbidden)
        return sorted(domain)

    def recurse():
        nonlocal nodes
        nodes += 1
        uncoloured = [vertex for vertex, colour in enumerate(colours) if colour < 0]
        if not uncoloured:
            require(
                all(fold(int.__xor__, (colours[v] for v in row), 0) for row in constraints),
                "invalid enumerated leaf",
            )
            solutions.append(tuple(colours))
            return

        # DSATUR on the two-variable constraint graph; total constraint incidence
        # and the label provide deterministic tie-breaks.
        vertex = max(
            uncoloured,
            key=lambda v: (
                len({colours[u] for u in adjacency[v] if colours[u] >= 0}),
                len(adjacency[v]),
                len(incident[v]),
                -v,
            ),
        )
        for colour in allowed(vertex):
            colours[vertex] = colour
            recurse()
        colours[vertex] = -1

    recurse()
    return sorted(solutions), nodes


def normalized_rotation(row, shift):
    shifted = [row[7 * (i // 7) + (i + shift) % 7] for i in range(21)]
    anchors = [shifted[i] for i in (0, 7, 14)]
    require(len(set(anchors)) == 3, "rotation destroyed anchor triangle")
    rename = {value: index for index, value in enumerate(anchors)}
    rename[next(iter({0, 1, 2, 3} - set(anchors)))] = 3
    return tuple(rename[value] for value in shifted)


def main():
    started = time.perf_counter()
    require(power(T, 42) == ONE, "T is not a 42nd root")
    for proper_divisor in (1, 2, 3, 6, 7, 14, 21):
        require(power(T, proper_divisor) != ONE, "T is not primitive")
    require(inverse(add(ONE, T)) == inverse(add(T, ONE)), "inverse is nondeterministic")

    rational_host = host_coordinates()
    host, denominator = integerize(rational_host)
    require(denominator == 7, "unexpected coordinate denominator")
    require(len(host) == len(set(host)) == 21, "host does not have 21 distinct points")
    host_edges, _, _, _ = pair_inventory(host, denominator)
    require(len(host_edges) == 42, "host does not have 42 unit edges")

    directed_units = {
        sub(host[i], host[j]) for i, j in host_edges
    } | {
        sub(host[j], host[i]) for i, j in host_edges
    }
    require(len(directed_units) == 84, "unit directions are not distinct")

    points = sorted({sub(a, b) for a in host for b in host})
    require(len(points) == 421, "difference set does not have 421 points")
    point_index = {point: index for index, point in enumerate(points)}
    origin = point_index[tuple(0 for _ in range(DEGREE))]
    representations = {origin: frozenset()}
    for a, b in combinations(range(21), 2):
        for point in (sub(host[a], host[b]), sub(host[b], host[a])):
            index = point_index[point]
            require(index not in representations, "nonzero difference is not uniquely represented")
            representations[index] = frozenset((a, b))
    require(len(representations) == 421, "representation map is incomplete")

    edges, distance3, sqrt3, sqrt7 = pair_inventory(points, denominator)
    require(len(edges) == 1848, "wrong difference-graph edge count")
    require(not distance3, "unexpected distance-3 pair")
    require(len(sqrt3) == 126, "wrong sqrt(3)-pair count")
    require(not sqrt7, "unexpected sqrt(7)-pair")
    degrees = Counter()
    for a, b in edges:
        degrees[a] += 1
        degrees[b] += 1
    degree_histogram = dict(sorted(Counter(degrees.values()).items()))
    require(degree_histogram == {7: 42, 8: 168, 9: 126, 10: 84, 84: 1}, "wrong degree histogram")

    constraints = sorted(
        {
            tuple(sorted(representations[a] ^ representations[b]))
            for a, b in edges
        }
    )
    require(Counter(map(len, constraints)) == {2: 42, 4: 42}, "wrong XOR support profile")
    require(
        {row for row in constraints if len(row) == 2} == {tuple(edge) for edge in host_edges},
        "two-variable supports are not exactly the host edges",
    )
    require({(0, 7), (0, 14), (7, 14)} <= set(constraints), "normalizing triangle is absent")

    rows, search_nodes = enumerate_potentials(constraints)
    require(len(rows) == 42, "wrong number of normalized potentials")
    rows_bytes = (json.dumps(rows, separators=(",", ":")) + "\n").encode()
    rows_hash = sha256(rows_bytes).hexdigest()
    require(rows_hash == EXPECTED_ROWS_SHA256, "rows differ from the published certificate")

    checked_edges = 0
    checked_sqrt3 = 0
    for row in rows:
        colours = []
        for index in range(421):
            colour = 0
            for potential in representations[index]:
                colour ^= row[potential]
            colours.append(colour)
        require(all(colours[a] != colours[b] for a, b in edges), "improper lifted colouring")
        require(all(colours[a] != colours[b] for a, b in sqrt3), "monochromatic sqrt(3) pair")
        checked_edges += len(edges)
        checked_sqrt3 += len(sqrt3)

    # Exact preservation test for all 84 declared rotation/reflection candidates.
    point_set = set(points)
    preserving_rotations = []
    preserving_reflections = []
    for k in range(42):
        rotated = {mul(t_power(k), point) for point in points}
        if rotated == point_set:
            preserving_rotations.append(k)
        reflected = {mul(t_power(k), conjugate(point)) for point in points}
        if reflected == point_set:
            preserving_reflections.append(k)
    require(preserving_rotations == list(range(0, 42, 3)), "wrong preserving rotations")
    require(not preserving_reflections, "unexpected preserving reflection")

    rotation_permutations = []
    for k in preserving_rotations:
        rotation_permutations.append([point_index[mul(t_power(k), point)] for point in points])
    remaining_pairs = set(sqrt3)
    sqrt3_orbits = []
    while remaining_pairs:
        a, b = min(remaining_pairs)
        orbit = {
            tuple(sorted((permutation[a], permutation[b])))
            for permutation in rotation_permutations
        }
        require(orbit <= remaining_pairs, "sqrt(3) orbit left the pair set")
        remaining_pairs -= orbit
        sqrt3_orbits.append(orbit)
    require(sorted(map(len, sqrt3_orbits)) == [14] * 9, "wrong sqrt(3)-pair orbit profile")

    remaining_rows = set(rows)
    potential_orbits = []
    while remaining_rows:
        seed = min(remaining_rows)
        orbit = {normalized_rotation(seed, shift) for shift in range(7)}
        require(orbit <= remaining_rows, "potential orbit left the solution set")
        remaining_rows -= orbit
        potential_orbits.append(orbit)
    require(sorted(map(len, potential_orbits)) == [7] * 6, "wrong potential orbit profile")

    # The reviewed source left its first ordinary sqrt(3)-pair query unresolved.
    # Search the complete potential list for a one-vertex recolouring witness.
    target_pair = (0, 332)
    require(target_pair in set(sqrt3), "the stated terminal pair is not at distance sqrt(3)")
    neighbours = sorted(
        b if a == target_pair[1] else a
        for a, b in edges
        if target_pair[1] in (a, b)
    )
    recolouring_certificate = None
    for row_index, row in enumerate(rows):
        colours = []
        for index in range(421):
            colour = 0
            for potential in representations[index]:
                colour ^= row[potential]
            colours.append(colour)
        replacement = colours[target_pair[0]]
        if replacement == colours[target_pair[1]]:
            continue
        if replacement in {colours[v] for v in neighbours}:
            continue
        recoloured = colours.copy()
        old_colour = recoloured[target_pair[1]]
        recoloured[target_pair[1]] = replacement
        require(all(recoloured[a] != recoloured[b] for a, b in edges), "bad recolouring witness")
        require(recoloured[target_pair[0]] == recoloured[target_pair[1]], "terminals did not coalesce")
        recolouring_certificate = {
            "sorted_potential_row_index": row_index,
            "potential_row": list(row),
            "modified_vertex": target_pair[1],
            "old_colour": old_colour,
            "new_colour": replacement,
            "neighbours": neighbours,
            "neighbour_colours": [colours[v] for v in neighbours],
            "ordinary_colouring": recoloured,
        }
        break
    require(recolouring_certificate is not None, "no one-vertex terminal witness found")
    recoloured = recolouring_certificate.pop("ordinary_colouring")
    monochromatic_sqrt3 = [pair for pair in sqrt3 if recoloured[pair[0]] == recoloured[pair[1]]]
    require(monochromatic_sqrt3 == [target_pair], "unexpected monochromatic sqrt(3) profile")
    antipodes = [point_index[neg(point)] for point in points]
    require(
        any(recoloured[v] != recoloured[antipodes[v]] for v in range(421)),
        "recoloured witness unexpectedly remained antipodally symmetric",
    )
    target_orbit = next(orbit for orbit in sqrt3_orbits if target_pair in orbit)
    require(len(target_orbit) == 14, "canonical terminal orbit is not full")
    bad_control = recoloured.copy()
    bad_control[target_pair[1]] = recoloured[neighbours[0]]
    require(
        any(bad_control[a] == bad_control[b] for a, b in edges),
        "deliberately bad recolouring was not rejected",
    )
    recoloured_bytes = (json.dumps(recoloured, separators=(",", ":")) + "\n").encode()

    edge_bytes = (json.dumps(edges, separators=(",", ":")) + "\n").encode()
    result = {
        "status": "INDEPENDENT EXACT CHECK PASSED",
        "target": "bafkreieymqno3tggkhnxvrwoprgctvvi4mtk3yjvfs7vt6ykfwyje4ywbm",
        "field_model": "Q[T]/(Phi_42), polynomial extended Euclid",
        "coordinate_denominator": denominator,
        "host_vertices": len(host),
        "host_unit_edges": len(host_edges),
        "directed_unit_differences": len(directed_units),
        "difference_vertices": len(points),
        "difference_unit_edges": len(edges),
        "degree_histogram": {str(k): v for k, v in degree_histogram.items()},
        "distance_3_pairs": len(distance3),
        "sqrt_7_pairs": len(sqrt7),
        "sqrt_3_pairs": len(sqrt3),
        "sqrt_3_orbit_sizes": sorted(map(len, sqrt3_orbits)),
        "constraints_by_size": {str(k): v for k, v in sorted(Counter(map(len, constraints)).items())},
        "normalized_potentials": len(rows),
        "potential_orbit_sizes": sorted(map(len, potential_orbits)),
        "dsatur_search_nodes": search_nodes,
        "lifted_unit_edges_checked": checked_edges,
        "lifted_sqrt_3_pairs_checked": checked_sqrt3,
        "preserving_rotation_exponents": preserving_rotations,
        "preserving_reflection_exponents": preserving_reflections,
        "ordinary_recolouring_certificate": {
            **recolouring_certificate,
            "terminal_pair": list(target_pair),
            "terminal_squared_distance": 3,
            "monochromatic_sqrt_3_pairs": 1,
            "rotationally_equivalent_terminal_pairs": len(target_orbit),
            "antipodally_symmetric": False,
            "colouring_sha256": sha256(recoloured_bytes).hexdigest(),
        },
        "sorted_edge_list_sha256": sha256(edge_bytes).hexdigest(),
        "sorted_potential_rows_sha256": rows_hash,
        "python": sys.version.split()[0],
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except CheckFailure as error:
        raise SystemExit(f"CHECK FAILED: {error}") from error
