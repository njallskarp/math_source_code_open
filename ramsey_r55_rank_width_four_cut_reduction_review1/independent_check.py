#!/usr/bin/env python3
"""Independent audit of the rank-width-four theorem and rank-four cut reduction.

No module from either reviewed source package is imported.  All arithmetic is
exact and all fixture graphs are decoded again from their physical edge words.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parity(value: int) -> int:
    return value.bit_count() & 1


def dot(x: int, y: int) -> int:
    return parity(x & y)


def gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for original in rows:
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return len(basis)


def pairs(n: int) -> list[tuple[int, int]]:
    return list(itertools.combinations(range(n), 2))


def decode_graph(n: int, text: str) -> tuple[int, list[list[int]]]:
    require(type(text) is str and set(text) <= set("0123456789abcdef"), "hex syntax")
    word = int(text, 16)
    require(word < (1 << (n * (n - 1) // 2)), "graph word overflow")
    graph = [[0] * n for _ in range(n)]
    for edge, (u, v) in enumerate(pairs(n)):
        graph[u][v] = graph[v][u] = (word >> edge) & 1
    return word, graph


def check_five(graph: list[list[int]], vertices: list[int], color: int) -> None:
    n = len(graph)
    require(type(vertices) is list and len(vertices) == 5, "five-set size")
    require(vertices == sorted(set(vertices)) and all(type(v) is int and 0 <= v < n for v in vertices), "five-set labels")
    require(type(color) is int and color in (0, 1), "five-set color")
    require(all(graph[u][v] == color for u, v in itertools.combinations(vertices, 2)), "false physical five-set")


def bounded_compositions(total: int, caps: tuple[int, ...]):
    values = [0] * len(caps)

    def visit(position: int, remaining: int):
        if position == len(caps):
            if remaining == 0:
                yield tuple(values)
            return
        tail_capacity = sum(caps[position + 1 :])
        low = max(0, remaining - tail_capacity)
        high = min(caps[position], remaining)
        for value in range(low, high + 1):
            values[position] = value
            yield from visit(position + 1, remaining - value)

    yield from visit(0, total)


def audit_rank_three_argument() -> dict:
    """Search every bounded abstract label profile left by the written lemmas."""
    ordered_triples = []
    triple_kinds = Counter()
    for p, q, r in itertools.permutations(range(1, 8), 3):
        cells = (
            frozenset(y for y in range(8) if dot(p, y) == 1 and dot(q, y) == 0),
            frozenset(y for y in range(8) if dot(q, y) == 1 and dot(r, y) == 0),
            frozenset(y for y in range(8) if dot(r, y) == 1 and dot(p, y) == 0),
        )
        require(all(len(cell) == 2 for cell in cells), "contact-cell label count")
        require(all(left.isdisjoint(right) for left, right in itertools.combinations(cells, 2)), "contact cells overlap")
        remainder = set(range(8)) - set().union(*cells)
        require(len(remainder) == 2 and 0 in remainder, "contact-cell remainder")
        rank = gf2_rank([p, q, r])
        require(rank in (2, 3) and (rank == 2) == (p ^ q ^ r == 0), "three-label rank classification")
        triple_kinds[f"rank_{rank}"] += 1
        ordered_triples.append((p, q, r, cells))
    require(triple_kinds == {"rank_2": 42, "rank_3": 168}, "ordered triple totals")

    for p, q in itertools.permutations(range(1, 8), 2):
        common = [y for y in range(8) if dot(p, y) == dot(q, y) == 1]
        require(len(common) == 2, "two-label red-contact intersection")
    require(all(sum(dot(x, y) == 0 for y in range(1, 8)) == 3 for x in range(1, 8)), "nonzero orthogonal labels")

    # Literal R(3,3) and the five-class distinguisher capacities.
    e6 = pairs(6)
    i6 = {edge: i for i, edge in enumerate(e6)}
    triangle_edges = [[i6[edge] for edge in itertools.combinations(q, 2)] for q in itertools.combinations(range(6), 3)]
    for word in range(1 << len(e6)):
        require(any(len({(word >> edge) & 1 for edge in triangle}) == 1 for triangle in triangle_edges), "R(3,3) counterexample")

    e5 = pairs(5)
    i5 = {edge: i for i, edge in enumerate(e5)}
    internal_maximum = 0
    for word in range(1 << len(e5)):
        count = 0
        for q in itertools.combinations(range(5), 3):
            for vertex in set(range(5)) - set(q):
                contacts = {(word >> i5[tuple(sorted((vertex, x)))]) & 1 for x in q}
                count += len(contacts) == 2
        internal_maximum = max(internal_maximum, count)
    outside_maximum = max(
        sum(len({(signature >> vertex) & 1 for vertex in q}) == 2 for q in itertools.combinations(range(5), 3))
        for signature in range(32)
    )
    require((internal_maximum, outside_maximum) == (20, 9), "five-class distinguisher capacities")

    # A-side populations: every population at least three is mixed, except
    # possibly one population-three blue clique in the 21+22 case.
    a_profiles = Counter()
    for a in (20, 21):
        for profile in bounded_compositions(a, (1,) + (4,) * 7):
            large = [label for label in range(1, 8) if profile[label] >= 3]
            require(len(large) >= 3, "fewer than three mixed classes without exception")
            a_profiles[f"a{a}_no_exception"] += 1
            if a == 21:
                for exceptional in [label for label in large if profile[label] == 3]:
                    require(len(set(large) - {exceptional}) >= 3, "fewer than three mixed classes with exception")
                    a_profiles["a21_one_exception"] += 1
    require(a_profiles == {"a20_no_exception": 5950, "a21_no_exception": 3935, "a21_one_exception": 7644}, "A-profile totals")

    # B-side populations: seek a counterexample to the three cell caps for
    # every possible ordered choice of the mixed labels.
    b_profiles_checked = 0
    for b, zero_cap in ((23, 2), (22, 1)):
        profiles = list(bounded_compositions(b, (zero_cap,) + (5,) * 7))
        for _, _, _, cells in ordered_triples:
            for profile in profiles:
                b_profiles_checked += 1
                cell_sizes = [sum(profile[label] for label in cell) for cell in cells]
                require(any(size > 5 for size in cell_sizes), "surviving balanced contact-cell profile")

    # Numerical boundary inequalities used to obtain those abstract caps.
    cases = []
    for a, b, b_zero_cap in ((20, 23, 2), (21, 22, 1)):
        require(10 * 17 > 20 + 9 * (a - 5), "five-class bound")
        require(a < 23, "zero pair on A")
        require(b < 25 and b_zero_cap == (2 if b == 23 else 1), "zero class on B")
        require(b - b_zero_cap - 3 * 5 == 6 > 4, "red triangle class exclusion")
        possible_t = [t for t in range(5) if 54 <= 2 * a + 4 + 2 * t]
        require(possible_t == ([] if a == 20 else [4]), "blue triangle boundary")
        if a == 21:
            require(2 * 18 - 22 == 14 > 2 * 5, "two exceptional labels")
        cases.append({"a": a, "b": b, "zero_cap_B": b_zero_cap, "possible_blue_contacts": possible_t})

    centroid_triples = 0
    for first in range(1, 22):
        for second in range(1, 22):
            third = 43 - first - second
            if 1 <= third <= 21:
                require(15 <= max(first, second, third) <= 21, "centroid cut range")
                centroid_triples += 1
    require(centroid_triples == 231, "centroid triple total")
    return {
        "ordered_label_triples": len(ordered_triples),
        "triple_kinds": dict(sorted(triple_kinds.items())),
        "a_profiles": dict(sorted(a_profiles.items())),
        "b_profile_triple_checks": b_profiles_checked,
        "six_vertex_graphs": 1 << len(e6),
        "five_class_graphs": 1 << len(e5),
        "five_class_capacities": [internal_maximum, outside_maximum],
        "balanced_cases": cases,
        "centroid_triples": centroid_triples,
    }


def spanning_dp(length: int, dimension: int, forbid_zero: bool) -> int:
    counts = [1] + [0] * dimension
    for _ in range(length):
        following = [0] * (dimension + 1)
        for rank, count in enumerate(counts):
            following[rank] += count * ((1 << rank) - int(forbid_zero))
            if rank < dimension:
                following[rank + 1] += count * ((1 << dimension) - (1 << rank))
        counts = following
    return counts[dimension]


def gaussian_binomial(dimension: int, rank: int) -> int:
    numerator = math.prod((1 << dimension) - (1 << i) for i in range(rank))
    denominator = math.prod((1 << rank) - (1 << i) for i in range(rank))
    return numerator // denominator


def nonzero_spanning_mobius(length: int, dimension: int) -> int:
    return sum(
        gaussian_binomial(dimension, rank)
        * (-1) ** (dimension - rank)
        * (1 << ((dimension - rank) * (dimension - rank - 1) // 2))
        * ((1 << rank) - 1) ** length
        for rank in range(dimension + 1)
    )


def onto_inclusion(length: int, alphabet: int) -> int:
    return sum((-1) ** missing * math.comb(alphabet, missing) * (alphabet - missing) ** length for missing in range(alphabet + 1))


def onto_recurrence(length: int, alphabet: int) -> int:
    counts = [1] + [0] * alphabet
    for _ in range(length):
        following = [0] * (alphabet + 1)
        for used, count in enumerate(counts):
            following[used] += used * count
            if used < alphabet:
                following[used + 1] += (alphabet - used) * count
        counts = following
    return counts[alphabet]


def audit_rank_four_counts() -> dict:
    for length in range(1, 24):
        for dimension in range(5):
            closed = math.prod((1 << length) - (1 << i) for i in range(dimension))
            require(spanning_dp(length, dimension, False) == closed, "full-rank tuple count")
            require(spanning_dp(length, dimension, True) == nonzero_spanning_mobius(length, dimension), "nonzero tuple count")

    small_matrices = zero_pair_matrices = 0
    for m in range(1, 5):
        for n in range(1, 5):
            by_rank = Counter()
            zero_by_rank = Counter()
            mask = (1 << n) - 1
            for word in range(1 << (m * n)):
                rows = [(word >> (n * row)) & mask for row in range(m)]
                rank = gf2_rank(rows)
                by_rank[rank] += 1
                column_zero = any(all(((row >> column) & 1) == 0 for row in rows) for column in range(n))
                if 0 in rows and column_zero:
                    zero_by_rank[rank] += 1
                    require(gf2_rank([row ^ mask for row in rows]) == rank + 1, "complement rank identity")
                    zero_pair_matrices += 1
                small_matrices += 1
            for rank in range(min(m, n) + 1):
                gl = spanning_dp(rank, rank, False)
                tm = spanning_dp(m, rank, False)
                tn = spanning_dp(n, rank, False)
                zm = tm - spanning_dp(m, rank, True)
                zn = tn - spanning_dp(n, rank, True)
                require(by_rank[rank] * gl == tm * tn, "rank-matrix factor count")
                require(zero_by_rank[rank] * gl == zm * zn, "zero-row/column factor count")

    fibers = Counter()
    for left in itertools.product(range(4), repeat=3):
        if gf2_rank(list(left)) != 2:
            continue
        for right in itertools.product(range(4), repeat=4):
            if gf2_rank(list(right)) != 2:
                continue
            matrix = tuple(sum(dot(x, y) << column for column, y in enumerate(right)) for x in left)
            fibers[matrix] += 1
    require(set(fibers.values()) == {6} and len(fibers) == 1470, "rank-two factor fibers")

    r = 4
    gl4 = spanning_dp(r, r, False)
    t20 = spanning_dp(20, r, False)
    t23 = spanning_dp(23, r, False)
    z20 = t20 - spanning_dp(20, r, True)
    z23 = t23 - spanning_dp(23, r, True)
    total = t20 * t23 // gl4
    removed = z20 * z23 // gl4
    remaining = total - removed
    onto20 = onto_inclusion(20, 16)
    onto23 = onto_inclusion(23, 16)
    require(onto20 == onto_recurrence(20, 16) and onto23 == onto_recurrence(23, 16), "surjection counts")
    full_support = onto20 * onto23 // gl4
    expected = {
        "gl4": 20160,
        "total": 296935236499420514245609548376980635622730104000,
        "removed": 166472869961950839672373904116655134899335779200,
        "remaining": 130462366537469674573235644260325500723394324800,
        "full_support": 370003189750044329182215197142967910400000,
        "fraction": "11082739332310042690903561559441706322/19768120928371528230187646401013892765",
    }
    observed = {
        "gl4": gl4,
        "total": total,
        "removed": removed,
        "remaining": remaining,
        "full_support": full_support,
        "fraction": str(Fraction(removed, total)),
    }
    require(observed == expected, "rank-four displayed counts")
    require(math.comb(20, 2) + math.comb(23, 2) == 443, "internal physical pairs")
    return {
        **observed,
        "small_matrices": small_matrices,
        "small_zero_pair_matrices": zero_pair_matrices,
        "rank2_factor_fibers": len(fibers),
        "internal_free_pairs": 443,
    }


def verify_manifest(directory: Path, expected_files: int, expected_bytes: int) -> dict:
    lines = (directory / "SHA256SUMS").read_text().splitlines()
    for line in lines:
        claimed, name = line.split("  ", 1)
        require(digest((directory / name).read_bytes()) == claimed, f"manifest mismatch: {name}")
    files = [entry for entry in directory.iterdir() if entry.is_file()]
    require(len(files) == expected_files, "published file count")
    total_bytes = sum(entry.stat().st_size for entry in files)
    require(total_bytes == expected_bytes, "published byte count")
    return {"files": len(files), "bytes": total_bytes, "manifest_entries": len(lines)}


def cut_rows(graph: list[list[int]], side: frozenset[int], color: int) -> list[int]:
    other = sorted(set(range(len(graph))) - side)
    return [sum((graph[u][v] == color) << column for column, v in enumerate(other)) for u in sorted(side)]


def smaller(side: set[int], n: int) -> frozenset[int]:
    return frozenset(side if len(side) <= n // 2 else set(range(n)) - side)


def tree_cuts(edges: list[list[int]]) -> list[frozenset[int]]:
    require(type(edges) is list and len(edges) == 83, "tree edge count")
    graph = [set() for _ in range(84)]
    for edge in edges:
        require(type(edge) is list and len(edge) == 2, "tree edge syntax")
        u, v = edge
        require(type(u) is int and type(v) is int and 0 <= u < v < 84, "tree labels")
        graph[u].add(v)
        graph[v].add(u)
    require([len(neighbors) for neighbors in graph] == [1] * 43 + [3] * 41, "tree degrees")
    cuts = []
    for u, v in [tuple(edge) for edge in edges]:
        seen = {u}
        queue = [u]
        for x in queue:
            for y in graph[x]:
                if {x, y} != {u, v} and y not in seen:
                    seen.add(y)
                    queue.append(y)
        require(v not in seen, "tree cycle")
        leaf_side = seen & set(range(43))
        require(leaf_side and len(leaf_side) < 43, "tree cut")
        cuts.append(smaller(leaf_side, 43))
    return cuts


def verify_rankwidth_fixture(directory: Path, stem: str) -> dict:
    obj = json.loads((directory / f"{stem}.json").read_text())
    cert = json.loads((directory / f"{stem}_certificate.json").read_text())
    require(obj.get("n") == 43 and obj.get("rank_color") in ("red", "blue"), "rank-width fixture header")
    _, graph = decode_graph(43, obj["red_hex"])
    color = int(obj["rank_color"] == "red")
    if obj["kind"] == "cut":
        cuts = [smaller(set(obj["cut"]), 43)]
    else:
        require(obj["kind"] == "decomposition", "fixture kind")
        cuts = tree_cuts(obj["tree_edges"])
    widths = [gf2_rank(cut_rows(graph, side, color)) for side in cuts]
    require(max(widths) == cert["measured_width"] <= 3, "fixture measured width")
    certificate_side = frozenset(cert["cut"])
    require(certificate_side in cuts, "fixture certificate cut")
    rows = cut_rows(graph, certificate_side, color)
    rank = gf2_rank(rows)
    require(rank == cert["cut_rank"], "fixture certificate rank")
    basis = cert["row_basis"]
    require(gf2_rank(basis) == rank, "fixture basis independence")
    span = {0}
    for vector in basis:
        span |= {member ^ vector for member in tuple(span)}
    require(all(row in span for row in rows), "fixture row-space coverage")
    canonical = (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()
    require(digest(canonical) == cert["input_sha256"], "fixture input binding")
    check_five(graph, cert["five"], int(cert["five_color"] == "red"))
    return {"kind": obj["kind"], "cuts": len(cuts), "width": max(widths), "physical_pairs": 10}


def independently_generate_rank4(parameters: dict) -> dict:
    left = parameters["left"]
    right = parameters["right"]
    require(len(left) == 20 and len(right) == 23 and gf2_rank(left) == gf2_rank(right) == 4, "rank-four parameters")
    internal = int(parameters["internal_hex"], 16)
    require(internal < (1 << 443), "internal word")
    red = 0
    inside_edge = 0
    for edge, (u, v) in enumerate(pairs(43)):
        if u < 20 <= v:
            bit = dot(left[u], right[v - 20])
        else:
            bit = (internal >> inside_edge) & 1
            inside_edge += 1
        red |= bit << edge
    require(inside_edge == 443, "internal edge consumption")
    return {"n": 43, "red_hex": format(red, "0226x"), "cut": list(range(20)), "color": 1}


def audit_physical_sources(rankwidth_dir: Path, rank4_dir: Path) -> dict:
    manifests = {
        "rankwidth": verify_manifest(rankwidth_dir, 15, 45933),
        "rank4cut": verify_manifest(rank4_dir, 15, 37532),
    }
    rankwidth_fixtures = [
        verify_rankwidth_fixture(rankwidth_dir, "fixture_cut"),
        verify_rankwidth_fixture(rankwidth_dir, "fixture_decomposition"),
    ]

    parameters = json.loads((rank4_dir / "fixture_parameters.json").read_text())
    graph_object = json.loads((rank4_dir / "fixture_graph.json").read_text())
    certificate = json.loads((rank4_dir / "fixture_certificate.json").read_text())
    require(independently_generate_rank4(parameters) == graph_object, "rank-four generator fixture")
    _, graph43 = decode_graph(43, graph_object["red_hex"])
    cut = set(graph_object["cut"])
    other = set(range(43)) - cut
    u, v = certificate["zero_pair"]
    color = graph_object["color"]
    require(u in cut and v in other, "zero pair sides")
    require(all(graph43[u][x] != color for x in other), "false zero row")
    require(all(graph43[v][x] != color for x in cut), "false zero column")
    canonical = json.dumps(graph_object, sort_keys=True, separators=(",", ":")).encode()
    require(digest(canonical) == certificate["input_sha256"], "rank-four certificate binding")
    check_five(graph43, certificate["five"], certificate["five_color"])

    core_raw = (rank4_dir / "core32.json").read_bytes()
    core = json.loads(core_raw)
    _, graph32 = decode_graph(32, core["red_hex"])
    literal_fives = 0
    for vertices in itertools.combinations(range(32), 5):
        require(len({graph32[x][y] for x, y in itertools.combinations(vertices, 2)}) == 2, "monochromatic core five")
        literal_fives += 1
    for x in range(16):
        for y in range(16):
            require(graph32[x][16 + y] == dot(x, y), "core dot-product table")
    red_rows = [sum(graph32[x][16 + y] << y for y in range(16)) for x in range(16)]
    blue_rows = [row ^ ((1 << 16) - 1) for row in red_rows]
    require((gf2_rank(red_rows), gf2_rank(blue_rows)) == (4, 5), "core cut ranks")
    require([sum(graph32[x]) for x in (0, 16)] == [14, 14], "core zero degrees")
    return {
        "manifests": manifests,
        "rankwidth_fixtures": rankwidth_fixtures,
        "rank4_fixture_pairs": 10,
        "core_literal_fives": literal_fives,
        "core_sha256": digest(core_raw),
    }


def main() -> None:
    require(len(sys.argv) == 3, "usage: independent_check.py RANKWIDTH_SOURCE RANK4CUT_SOURCE")
    rankwidth_dir = Path(sys.argv[1])
    rank4_dir = Path(sys.argv[2])
    evidence = {
        "rank_three": audit_rank_three_argument(),
        "rank_four_counts": audit_rank_four_counts(),
        "physical_sources": audit_physical_sources(rankwidth_dir, rank4_dir),
    }
    evidence_hash = digest(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode())
    print(json.dumps({"status": "INDEPENDENT_CLUSTER_ACCEPTED", "evidence_sha256": evidence_hash, **evidence}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
