#!/usr/bin/env python3
"""Exact audit of the codegree-13 core transversal compression."""

from __future__ import annotations

import hashlib
import itertools
import json


N_CORE = 13
DIFFERENCES = frozenset((1, 5, 8, 12))
MULTIPLIERS = DIFFERENCES
FULL = (1 << N_CORE) - 1
SEEDS = (
    (5, frozenset((0, 1, 2, 5, 6))),
    (5, frozenset((0, 1, 2, 6, 9))),
    (6, frozenset((0, 1, 2, 3, 5, 8))),
)

# This is the 43-vertex height-2807 red graph, encoded compactly.  The decoded
# sorted edge-list stream is checked against the public certificate hash.
MODEL_GRAPH6 = (
    "jSyIic|JekmixW~?IxLkbGjwfp_NjVcJZXHaVKVuCmZCqztIR~MZQYARD[_nGeLBQ]"
    "[bNCUyb_E{Jj}sO@pyRIXtZFIldAXrHUFEd\\?}wXcTjSJTGycm]HtGqX{nV@grUwQ"
    "ThDZDVVGq\\IVUWpwcfdv_"
)
MODEL_EDGE_SHA256 = "bc92dd1f5f1f8827d35a58048ade97a102921f7cab193f6b30706cb5184eed99"
MODEL_CORE_LABELS = (1, 3, 5, 15, 16, 17, 18, 19, 20, 24, 25, 26, 28)
MODEL_TO_CYCLIC = {
    1: 0,
    25: 1,
    5: 2,
    15: 3,
    3: 4,
    19: 5,
    16: 6,
    18: 7,
    28: 8,
    26: 9,
    17: 10,
    24: 11,
    20: 12,
}


def core_edge(i: int, j: int) -> bool:
    return i != j and ((i - j) % N_CORE) in DIFFERENCES


def mask(vertices: set[int] | frozenset[int] | tuple[int, ...]) -> int:
    return sum(1 << vertex for vertex in vertices)


def vertices(bits: int) -> tuple[int, ...]:
    return tuple(i for i in range(N_CORE) if bits >> i & 1)


def independent_four_masks() -> tuple[int, ...]:
    result = []
    for subset in itertools.combinations(range(N_CORE), 4):
        if all(not core_edge(i, j) for i, j in itertools.combinations(subset, 2)):
            result.append(mask(subset))
    return tuple(result)


def is_transversal(bits: int, independent_fours: tuple[int, ...]) -> bool:
    return all(bits & four for four in independent_fours)


def affine_orbit(seed: frozenset[int]) -> frozenset[int]:
    return frozenset(
        mask(frozenset((multiplier * x + shift) % N_CORE for x in seed))
        for multiplier in MULTIPLIERS
        for shift in range(N_CORE)
    )


def canonical_stream(items: list[tuple[int, ...]] | tuple[tuple[int, ...], ...]) -> bytes:
    return (json.dumps(items, separators=(",", ":")) + "\n").encode("ascii")


def decode_graph6(record: str) -> tuple[int, frozenset[tuple[int, int]]]:
    raw = record.encode("ascii")
    if not raw or raw[0] < 63 or raw[0] > 125:
        raise ValueError("unsupported graph6 header")
    n = raw[0] - 63
    if n > 62:
        raise ValueError("only the one-byte graph6 order is supported")
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise ValueError("bad graph6 payload length or padding")
    edges: set[tuple[int, int]] = set()
    index = 0
    for j in range(1, n):
        for i in range(j):
            if bits[index]:
                edges.add((i, j))
            index += 1
    return n, frozenset(edges)


def audit_core() -> dict[str, object]:
    edges = {
        (i, j)
        for i, j in itertools.combinations(range(N_CORE), 2)
        if core_edge(i, j)
    }
    degrees = tuple(sum(core_edge(i, j) for j in range(N_CORE)) for i in range(N_CORE))
    triangles = sum(
        all(core_edge(i, j) for i, j in itertools.combinations(subset, 2))
        for subset in itertools.combinations(range(N_CORE), 3)
    )
    independent_fives = sum(
        all(not core_edge(i, j) for i, j in itertools.combinations(subset, 2))
        for subset in itertools.combinations(range(N_CORE), 5)
    )
    fours = independent_four_masks()
    if len(edges) != 26 or degrees != (4,) * 13 or triangles or independent_fives:
        raise AssertionError("canonical core is not a (3,5;13) 4-regular graph")
    if len(fours) != 39:
        raise AssertionError(("independent fours", len(fours)))

    transversals = [bits for bits in range(1 << N_CORE) if is_transversal(bits, fours)]
    histogram = tuple(
        sum(bits.bit_count() == size for bits in transversals)
        for size in range(N_CORE + 1)
    )
    minimal = [
        bits
        for bits in transversals
        if all(not is_transversal(bits ^ (1 << x), fours) for x in vertices(bits))
    ]
    minimal_histogram = tuple(
        sum(bits.bit_count() == size for bits in minimal)
        for size in range(N_CORE + 1)
    )

    # The multipliers form the order-four subgroup {+/-1,+/-5}.  Check the
    # action directly rather than assuming that it preserves the core.
    for multiplier in MULTIPLIERS:
        for shift in range(N_CORE):
            for i, j in itertools.combinations(range(N_CORE), 2):
                if core_edge(i, j) != core_edge(
                    (multiplier * i + shift) % N_CORE,
                    (multiplier * j + shift) % N_CORE,
                ):
                    raise AssertionError("claimed affine map is not an automorphism")

    orbits = tuple(affine_orbit(seed) for _, seed in SEEDS)
    expected_sizes = (52, 13, 52)
    if tuple(map(len, orbits)) != expected_sizes:
        raise AssertionError(("orbit sizes", tuple(map(len, orbits))))
    if any(left & right for left, right in itertools.combinations(orbits, 2)):
        raise AssertionError("minimal-transversal orbits overlap")
    if frozenset().union(*orbits) != frozenset(minimal):
        raise AssertionError("three seed orbits do not exhaust the minimal transversals")
    if any(not is_transversal(seed_mask, fours) for orbit in orbits for seed_mask in orbit):
        raise AssertionError("orbit contains a nontransversal")
    if any(
        not any(seed_mask & bits == seed_mask for seed_mask in minimal)
        for bits in transversals
    ):
        raise AssertionError("a transversal contains no classified minimal member")

    four_stream = canonical_stream([vertices(bits) for bits in sorted(fours)])
    minimal_stream = canonical_stream([vertices(bits) for bits in sorted(minimal)])
    third_anchor_types = [
        (alpha, beta, 4, 8, alpha, beta, 7 - alpha, 7 - beta, 15 - alpha - beta, alpha + beta - 1)
        for alpha in range(8)
        for beta in range(8)
        if alpha + beta >= 1
    ]
    if len(third_anchor_types) != 63 or any(
        min(row[2:]) < 0 or sum(row[2:]) != 40 for row in third_anchor_types
    ):
        raise AssertionError("third-anchor cell census mismatch")
    return {
        "edges": len(edges),
        "independent_fours": len(fours),
        "transversals": len(transversals),
        "histogram": histogram,
        "minimal": len(minimal),
        "minimal_histogram": minimal_histogram,
        "orbit_sizes": expected_sizes,
        "four_sha256": hashlib.sha256(four_stream).hexdigest(),
        "minimal_sha256": hashlib.sha256(minimal_stream).hexdigest(),
        "third_anchor_types": len(third_anchor_types),
        "third_anchor_sha256": hashlib.sha256(canonical_stream(third_anchor_types)).hexdigest(),
        "fours": fours,
        "minimal_masks": tuple(minimal),
    }


def audit_previous_model(fours: tuple[int, ...]) -> dict[str, object]:
    n, red_edges = decode_graph6(MODEL_GRAPH6)
    if n != 43 or len(red_edges) != 445:
        raise AssertionError((n, len(red_edges)))
    edge_stream = "".join(f"{i} {j}\n" for i, j in sorted(red_edges)).encode("ascii")
    if hashlib.sha256(edge_stream).hexdigest() != MODEL_EDGE_SHA256:
        raise AssertionError("height-2807 model provenance mismatch")

    def red(i: int, j: int) -> bool:
        return tuple(sorted((i, j))) in red_edges

    u, v = 13, 14
    common = tuple(
        x for x in range(n) if x not in (u, v) and red(u, x) and red(v, x)
    )
    if common != MODEL_CORE_LABELS or set(MODEL_TO_CYCLIC) != set(common):
        raise AssertionError(("model core", common))
    for i, j in itertools.combinations(common, 2):
        if red(i, j) != core_edge(MODEL_TO_CYCLIC[i], MODEL_TO_CYCLIC[j]):
            raise AssertionError("stored core-to-cyclic isomorphism is invalid")

    failures: list[tuple[int, tuple[int, ...]]] = []
    passing_vertices = 0
    exterior = sorted(set(range(n)) - {u, v} - set(common))
    for z in exterior:
        footprint = mask(
            frozenset(MODEL_TO_CYCLIC[x] for x in common if red(z, x))
        )
        uncovered = [four for four in fours if not footprint & four]
        if uncovered:
            failures.extend((z, vertices(four)) for four in uncovered)
        else:
            passing_vertices += 1
    if len(exterior) != 28 or passing_vertices != 18 or len(failures) != 35:
        raise AssertionError((len(exterior), passing_vertices, len(failures)))

    first_z, first_cyclic = failures[0]
    inverse = {cyclic: model for model, cyclic in MODEL_TO_CYCLIC.items()}
    first_model_four = tuple(sorted(inverse[x] for x in first_cyclic))
    first_blue_five = tuple(sorted((first_z,) + first_model_four))
    if first_blue_five != (8, 15, 19, 20, 25):
        raise AssertionError(("first obstruction", first_blue_five))
    if any(red(i, j) for i, j in itertools.combinations(first_blue_five, 2)):
        raise AssertionError("reported obstruction is not a blue K5")

    failure_stream = canonical_stream(
        [(z,) + tuple(cyclic) for z, cyclic in failures]
    )
    return {
        "exterior": len(exterior),
        "passing_vertices": passing_vertices,
        "failing_vertices": len({z for z, _ in failures}),
        "uncovered_fours": len(failures),
        "first_blue_five": first_blue_five,
        "failure_sha256": hashlib.sha256(failure_stream).hexdigest(),
    }


def main() -> None:
    core = audit_core()
    model = audit_previous_model(core["fours"])  # type: ignore[arg-type]
    print(
        "PASS cyclic_core n=13 edges=26 degree=4^13 redK3=0 blueK5=0 "
        f"independent4={core['independent_fours']}"
    )
    print(
        "transversal_histogram="
        + ",".join(f"{size}:{count}" for size, count in enumerate(core["histogram"]) if count)  # type: ignore[union-attr]
    )
    print(
        "minimal_transversals=117 sizes=5:65,6:52 affine_orbits=5/52,5/13,6/52"
    )
    print(
        f"independent4_sha256={core['four_sha256']} "
        f"minimal_transversal_sha256={core['minimal_sha256']}"
    )
    print(
        f"third_anchor_types={core['third_anchor_types']} "
        f"third_anchor_sha256={core['third_anchor_sha256']}"
    )
    print(
        "height2807_interface="
        f"exterior:{model['exterior']},pass:{model['passing_vertices']},"
        f"fail:{model['failing_vertices']},uncovered4:{model['uncovered_fours']}"
    )
    print(
        "first_blueK5="
        + ",".join(map(str, model["first_blue_five"]))  # type: ignore[arg-type]
        + f" failure_sha256={model['failure_sha256']}"
    )


if __name__ == "__main__":
    main()
