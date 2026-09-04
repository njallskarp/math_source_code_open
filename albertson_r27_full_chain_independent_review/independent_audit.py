#!/usr/bin/env python3
"""Independent exact audit for the Albertson r=27 full chain.

This checker deliberately does not import the reviewed repository.  It
reconstructs the two recursive sampling tables using a gift-wrapping lower
hull (different from the supplied monotone-chain/PAVA and QuickHull code),
rechecks Sadhu's exact frontier cutoffs, ranges over the *actual* residual
crossing count in the local deletion profiles, and checks the finite
five-face shell.  The drawing-to-shell and sealed-disk implications remain
mathematical, not executable, interfaces; see REPORT.md.
"""

from __future__ import annotations

from bisect import bisect_right
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from json import dumps
from math import comb


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def z_value(r: int) -> int:
    return (r // 2) * ((r - 1) // 2) * ((r - 2) // 2) * ((r - 3) // 2) // 4


def sadhu_sample(n: int, m: int, k: int) -> Fraction:
    """Equation (1) of Sadhu arXiv:2609.01682v1."""
    return (
        5 * m * Fraction((n - 2) * (n - 3), (k - 2) * (k - 3))
        - Fraction(
            203 * n * (n - 1) * (n - 2) * (n - 3),
            9 * k * (k - 1) * (k - 3),
        )
    )


def critical_edge_floor(r: int, n: int) -> int:
    """Ceiling of the two applicable no-subdivision critical-edge bounds."""
    kostochka_yancey_twice = Fraction(
        (r + 1) * (r - 2) * n - r * (r - 3), r - 1
    )
    barat_toth_twice = Fraction((r - 1) * n + 2 * r - 6)
    twice_edges = max(kostochka_yancey_twice, barat_toth_twice)
    return ceil_fraction(twice_edges / 2)


def check_frontier() -> dict[str, object]:
    assert z_value(27) == 6084
    assert critical_edge_floor(27, 53) == 713
    assert critical_edge_floor(27, 54) == 726

    best_53_715 = max(sadhu_sample(53, 715, k) for k in range(4, 54))
    best_53_716 = max(sadhu_sample(53, 716, k) for k in range(4, 54))
    best_54_726 = max(sadhu_sample(54, 726, k) for k in range(4, 55))
    best_54_727 = max(sadhu_sample(54, 727, k) for k in range(4, 55))
    assert best_53_715 <= 6084 < best_53_716
    assert best_54_726 <= 6084 < best_54_727
    assert sadhu_sample(53, 716, 24) == best_53_716
    assert sadhu_sample(54, 727, 24) == best_54_727
    return {
        "rows": [(53, 713), (53, 714), (53, 715), (54, 726)],
        "first_excluded": {
            "53": str(best_53_716),
            "54": str(best_54_727),
        },
    }


LINEAR_BOUNDS = (
    (1, 3, 1),
    (7, 25, 3),
    (37, 155, 9),
    (45, 203, 9),
)


def universal_floor(n: int, m: int) -> int:
    s = n - 2
    return max(
        [0]
        + [ceil_fraction(Fraction(a * m - b * s, d)) for a, b, d in LINEAR_BOUNDS]
    )


Point = tuple[int, int]


def gift_wrap_lower_hull(values: list[int]) -> list[Point]:
    """Jarvis-style lower hull: repeatedly take the least outgoing slope."""
    last = len(values) - 1
    current = 0
    hull = [(0, values[0])]
    while current < last:
        best = current + 1
        for candidate in range(best + 1, last + 1):
            left = (values[candidate] - values[current]) * (best - current)
            right = (values[best] - values[current]) * (candidate - current)
            if left < right or (left == right and candidate > best):
                best = candidate
        hull.append((best, values[best]))
        current = best
    return hull


def hull_value(hull: list[Point], x: Fraction) -> Fraction:
    xs = [point[0] for point in hull]
    index = bisect_right(xs, x) - 1
    if x == hull[index][0] or index == len(hull) - 1:
        return Fraction(hull[index][1])
    x0, y0 = hull[index]
    x1, y1 = hull[index + 1]
    return y0 + (x - x0) * Fraction(y1 - y0, x1 - x0)


def audit_hull(values: list[int], hull: list[Point]) -> None:
    assert hull[0] == (0, values[0])
    assert hull[-1] == (len(values) - 1, values[-1])
    slopes = [
        Fraction(y1 - y0, x1 - x0)
        for (x0, y0), (x1, y1) in zip(hull, hull[1:])
    ]
    assert all(a < b for a, b in zip(slopes, slopes[1:]))
    for q, value in enumerate(values):
        assert hull_value(hull, Fraction(q)) <= value


def sampled_floor(n: int, m: int, sample: int, hull: list[Point]) -> int:
    mean = Fraction(m * sample * (sample - 1), n * (n - 1))
    incidence_ratio = Fraction(
        n * (n - 1) * (n - 2) * (n - 3),
        sample * (sample - 1) * (sample - 2) * (sample - 3),
    )
    return ceil_fraction(incidence_ratio * hull_value(hull, mean))


def build_tables(max_order: int, local24: bool) -> tuple[dict[int, list[int]], str]:
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[Point]] = {}
    digest = sha256()
    for n in range(4, max_order + 1):
        row: list[int] = []
        for m in range(comb(n, 2) + 1):
            candidates = [universal_floor(n, m)]
            if local24 and n == 24:
                candidates.append(max(0, 5 * m - 495))
            candidates.extend(
                sampled_floor(n, m, sample, hulls[sample])
                for sample in range(4, n)
            )
            value = max(candidates)
            row.append(value)
            digest.update(f"{n}:{m}:{value}\n".encode("ascii"))
        hull = gift_wrap_lower_hull(row)
        audit_hull(row, hull)
        tables[n] = row
        hulls[n] = hull
    return tables, digest.hexdigest()


def check_sampling_tables() -> dict[str, object]:
    unconditional, unconditional_digest = build_tables(53, local24=False)
    assert unconditional_digest == (
        "55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43"
    )
    assert all(
        unconditional[50][q] >= 26 * q - 11706 for q in range(comb(50, 2) + 1)
    )
    assert [q for q in range(comb(50, 2) + 1) if unconditional[50][q] == 26 * q - 11706] == list(range(633, 640))

    row_714 = Fraction(
        26 * 714 * comb(51, 48) - 11706 * comb(53, 50), comb(49, 46)
    )
    row_715 = Fraction(
        26 * 715 * comb(51, 48) - 11706 * comb(53, 50), comb(49, 46)
    )
    assert row_714 == Fraction(14046318, 2303)
    assert row_715 == Fraction(56455997, 9212)
    assert ceil_fraction(row_714) == 6100
    assert ceil_fraction(row_715) == 6129

    conditional, conditional_digest = build_tables(53, local24=True)
    assert conditional_digest == (
        "79e615e691c84d697b2dbc3d6fded0d9657c37d3f91f4bebc1a61097fb39f7f6"
    )
    slacks = [
        5 * conditional[52][q] - (136 * q - 65166)
        for q in range(comb(52, 2) + 1)
    ]
    assert min(slacks) == 0
    assert [q for q, slack in enumerate(slacks) if slack == 0] == [686, 691]
    assert conditional[52][686] == 5626
    assert conditional[52][691] == 5762

    edge_sum = 51 * 713
    scaled_sum = Fraction(136 * edge_sum - 53 * 65166, 5)
    assert edge_sum == 36363
    assert scaled_sum == 298314
    assert scaled_sum == 49 * 6088 + 2
    assert ceil_fraction(scaled_sum / 49) == 6089
    assert conditional[53][713] == 6089
    return {
        "unconditional_digest": unconditional_digest,
        "row_bounds": {"53,714": 6100, "53,715": 6129},
        "conditional_digest": conditional_digest,
        "support_equality": [686, 691],
        "deletion_sum": int(scaled_sum),
        "row_53_713": 6089,
    }


def order54_sample_bound(sample: int, q: int) -> Fraction:
    rounded_constant = (203 * (sample - 2)) // 9
    return Fraction(
        5 * q * comb(30, sample - 2) - rounded_constant * comb(32, sample),
        comb(28, sample - 4),
    )


def check_order54() -> dict[str, object]:
    for q in range(comb(32, 2) + 1):
        sample = 25 if q <= 251 else 24
        assert ceil_fraction(order54_sample_bound(sample, q)) >= 9 * q - 1573
    assert order54_sample_bound(25, 251) - (9 * 251 - 1574) == Fraction(372, 1265)
    assert order54_sample_bound(24, 252) - (9 * 252 - 1574) == Fraction(998, 5313)
    bound = Fraction(
        9 * 726 * comb(52, 30) - 1573 * comb(54, 32), comb(50, 28)
    )
    assert bound == Fraction(218768121, 35960)
    assert ceil_fraction(bound) == 6084
    return {"bound": str(bound), "ceiling": 6084}


def enumerate_actual_profiles() -> list[tuple[int, ...]]:
    """Range over actual x2 >= the PRTT floor, not just the floor itself."""
    rows: list[tuple[int, ...]] = []
    s = 22
    for a in range(23):
        for b in range(23 - a):
            c = 22 - a - b
            for d in range(5 * s - 2 * c + 1):
                e2 = 5 * s - 2 * c - d
                removed = 5 * a + 4 * b + 9 * c + 3 * d
                for empty in range(2 * s + 1):
                    x2_floor = max(
                        0, ceil_fraction(Fraction(7 * e2 - 25 * s + 2 * empty, 3))
                    )
                    for x2 in range(x2_floor, 164 - removed + 1):
                        total = removed + x2
                        for missing in range(d + 1):
                            for pentagons in range((2 * s - 4 * c) // 3 + 1):
                                for hexagons in range((2 * s - 4 * c - 3 * pentagons) // 4 + 1):
                                    outside = 2 * s - 4 * c - 3 * pentagons - 4 * hexagons
                                    if 3 * (pentagons + hexagons) < 2 * s - 4 * c - 3 * d + 3 * missing:
                                        continue
                                    if b > c + hexagons + 4 * missing + 2 * outside:
                                        continue
                                    rows.append((a, b, c, d, empty, missing, pentagons, hexagons, outside, e2, x2, total))
    return rows


def check_profiles() -> dict[str, object]:
    rows = enumerate_actual_profiles()
    expected = [
        (0, 20, 2, 3, 0, 0, 9, 0, 9, 103, 57, 164),
        (0, 22, 0, 4, 0, 0, 11, 0, 11, 106, 64, 164),
    ]
    assert rows == expected
    components = []
    for row in rows:
        e2, x2, full = row[9], row[10], row[6]
        c5, remainder = divmod(2 * e2 - 8 * 22, 3)
        assert remainder == 0
        k2 = x2 - 5 * c5
        free = e2 - 5 * c5 - 2 * k2
        terminal_e = e2 - 2 * c5
        terminal_x = x2 - 4 * c5
        assert c5 == full + 1
        assert terminal_x - terminal_e + 3 * 22 == 0
        planar_v = 24 + terminal_x
        planar_e = terminal_e + 2 * terminal_x
        assert planar_e == 3 * planar_v - 6
        components.append((c5, k2, free, terminal_e, terminal_x))
    assert components == [(10, 7, 39, 83, 17), (12, 4, 38, 82, 16)]
    return {"rows": rows, "components": components}


def undirected(left: str, right: str) -> frozenset[str]:
    assert left != right
    return frozenset((left, right))


def face_edges(face: tuple[str, str, str]) -> list[frozenset[str]]:
    return [undirected(face[i], face[(i + 1) % 3]) for i in range(3)]


def check_five_face_shell() -> dict[str, object]:
    faces = [
        ("u", "z", "w"),
        ("w", "z", "x"),
        ("z", "t", "x"),
        ("t", "r", "x"),
        ("r", "w", "x"),
    ]
    counts = Counter(edge for face in faces for edge in face_edges(face))
    boundary = {edge for edge, count in counts.items() if count == 1}
    expected_boundary = {
        undirected("u", "z"), undirected("z", "t"), undirected("t", "r"),
        undirected("r", "w"), undirected("w", "u"),
    }
    assert boundary == expected_boundary
    assert 6 - len(counts) + len(faces) == 1

    links: dict[str, list[frozenset[str]]] = defaultdict(list)
    for a, b, c in faces:
        links[a].append(undirected(b, c))
        links[b].append(undirected(a, c))
        links[c].append(undirected(a, b))
    for vertex, edges in links.items():
        degrees = Counter(endpoint for edge in edges for endpoint in edge)
        if vertex == "x":
            assert set(degrees.values()) == {2}
        else:
            assert set(degrees.values()) <= {1, 2}
            assert sum(value == 1 for value in degrees.values()) == 2

    crossed = {
        undirected("z", "w"), undirected("u", "r"), undirected("u", "t"),
        undirected("z", "r"), undirected("w", "t"),
    }
    complete = {undirected(a, b) for a, b in combinations(("u", "z", "t", "r", "w"), 2)}
    assert crossed.isdisjoint(boundary)
    assert crossed | boundary == complete
    return {
        "faces": faces,
        "boundary": ["u", "z", "t", "r", "w", "u"],
        "euler_characteristic": 1,
    }


def main() -> None:
    certificate = {
        "frontier": check_frontier(),
        "order54": check_order54(),
        "sampling": check_sampling_tables(),
        "profiles": check_profiles(),
        "five_face_shell": check_five_face_shell(),
        "Z27": z_value(27),
    }
    digest = sha256(dumps(certificate, sort_keys=True).encode("ascii")).hexdigest()
    print("PASS independent Albertson r=27 full-chain arithmetic audit")
    print(f"frontier_rows={certificate['frontier']['rows']}")
    print(f"order54={certificate['order54']}")
    print(f"sampling={certificate['sampling']}")
    print(f"profiles={certificate['profiles']['components']}")
    print("five_face_boundary=u-z-t-r-w-u; chi=1")
    print(f"Z(27)={certificate['Z27']}")
    print(f"review_certificate_sha256={digest}")


if __name__ == "__main__":
    main()
