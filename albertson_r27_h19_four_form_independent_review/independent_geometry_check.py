#!/usr/bin/env python3
"""Clean-room exact audit of the Albertson r=27, h=19 four-form reduction.

This checker deliberately does not import the target implementation.  Unlike
the two target scripts, it explicitly enumerates which labelled large blocks
meet directly and which components are joined by connector blocks.  It then
derives, rather than inserts, the four cases in which the unique largest
large block is isolated.
"""

from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations
import json
from math import comb


K = 27
N = 53
M = 713
HIGH = 19
LOW = N - HIGH
MIN_LARGE = K - HIGH
LOW_EDGE_FLOOR = 26 * LOW - M
PAIRS3 = ((0, 1), (0, 2), (1, 2))


def integer_partitions(total, length, lower, upper=26):
    """Nondecreasing bounded positive integer partitions."""
    if length == 0:
        if total == 0:
            yield ()
        return
    for first in range(lower, min(upper, total // length) + 1):
        for tail in integer_partitions(total - first, length - 1, first, upper):
            yield (first,) + tail


def colour_cap(edge_count):
    """Largest c not excluded by e >= binom(c,2)."""
    c = 1
    while comb(c + 1, 2) <= edge_count:
        c += 1
    assert comb(c, 2) <= edge_count < comb(c + 1, 2)
    return c


def components(edges):
    """Connected components of the graph on three labelled large blocks."""
    parent = list(range(3))

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = root(u), root(v)
        if ru != rv:
            parent[rv] = ru
    groups = {}
    for v in range(3):
        groups.setdefault(root(v), []).append(v)
    return tuple(sorted((tuple(group) for group in groups.values()), key=lambda x: x[0]))


def direct_forests(sizes, overlap):
    """All direct large-block intersection forests allowed by degree 26.

    Each direct edge denotes a shared cut vertex.  With two direct edges the
    two cut vertices are distinct; a common cut in all three blocks would
    have 33 low neighbours.
    """
    for edges in combinations(PAIRS3, overlap):
        if overlap == 2:
            # Any two edges of K3 form a path.  The common-cut alternative is
            # excluded separately by 34+2-3 = 33 > 26 low neighbours.
            assert len({x for edge in edges for x in edge}) == 3
        if all(sizes[u] + sizes[v] <= 28 for u, v in edges):
            yield tuple(edges)


def connector_schemes(component_count):
    """All connector-block hyperforests, represented on direct components.

    A two-component connector is a bridge K2.  With three components the
    possibilities are no connector, one bridge, two bridges forming a tree,
    or one K3 connector.  The final coordinate is the number of added edges.
    """
    yield ("none", (), 0)
    if component_count == 2:
        yield ("bridge", ((0, 1),), 1)
    elif component_count == 3:
        for edge in PAIRS3:
            yield ("bridge", (edge,), 1)
        for tree in combinations(PAIRS3, 2):
            yield ("two_bridges", tuple(tree), 2)
        yield ("triangle_connector", ((0, 1, 2),), 3)


def component_touched(component_index, connector_links):
    return any(component_index in link for link in connector_links)


def arithmetic_rows():
    """Reconstruct the 107 three-block budget rows and 14 exceptions."""
    connector_counts = {0: (0, 1, 2, 3), 1: (0, 1), 2: (0,)}
    rows = []
    for overlap in range(3):
        for sizes in integer_partitions(LOW + overlap, 3, MIN_LARGE):
            # It suffices that one labelled direct forest realizes the sizes.
            realizable = any(
                any(True for _ in direct_forests(labelled, overlap))
                for labelled in set(permutations(sizes))
            )
            if not realizable:
                continue
            for connector_edges in connector_counts[overlap]:
                low_edges = sum(comb(x, 2) for x in sizes) + connector_edges
                if low_edges < LOW_EDGE_FLOOR:
                    continue
                high_edges = low_edges - LOW_EDGE_FLOOR
                high_cap = colour_cap(high_edges)
                rows.append(
                    (sizes, overlap, connector_edges, low_edges, high_edges,
                     high_cap, max(sizes) + high_cap)
                )
    rows.sort()
    summary = tuple(
        (overlap,
         sum(row[1] == overlap for row in rows),
         max(row[-1] for row in rows if row[1] == overlap))
        for overlap in range(3)
    )
    exceptions = tuple(row for row in rows if row[-1] > 26)
    assert summary == ((0, 56, 27), (1, 32, 30), (2, 19, 32))
    assert len(rows) == 107
    assert len(exceptions) == 14
    return tuple(rows), summary, exceptions


def derive_residual_forms(exceptions):
    """Enumerate labelled geometries and derive isolated-largest cases."""
    exception_keys = {(row[0], row[1], row[2]) for row in exceptions}
    geometry_count = 0
    nonresidual_count = 0
    residual = set()
    strict_checks = set()

    for sizes_sorted, overlap, connector_edges in sorted(exception_keys):
        high_edges = sum(comb(x, 2) for x in sizes_sorted) + connector_edges - LOW_EDGE_FLOOR
        high_cap = colour_cap(high_edges)
        small = sizes_sorted[:2]
        assert sizes_sorted[1] < sizes_sorted[2]  # unique largest in every exception
        unused_colours = 26 - high_cap
        assert unused_colours > max(small) - 1
        strict_checks.add((sizes_sorted, overlap, connector_edges, high_cap, unused_colours))

        for sizes in sorted(set(permutations(sizes_sorted))):
            largest = sizes.index(max(sizes))
            for direct in direct_forests(sizes, overlap):
                comps = components(direct)
                block_component = next(i for i, comp in enumerate(comps) if largest in comp)
                for connector_kind, connector_links, added_edges in connector_schemes(len(comps)):
                    if added_edges != connector_edges:
                        continue
                    geometry_count += 1
                    largest_isolated = (
                        len(comps[block_component]) == 1
                        and not component_touched(block_component, connector_links)
                    )
                    if not largest_isolated:
                        # In the block-cut tree, a nontrivial component
                        # containing the unique largest block has another leaf;
                        # that leaf is a smaller large block and has strict list
                        # slack by the check above.
                        nonresidual_count += 1
                        continue

                    if overlap == 0 and added_edges == 0:
                        form = "three isolated cliques"
                    elif overlap == 0 and added_edges == 1:
                        # Isolation forces the single bridge to join the two
                        # smaller blocks.
                        form = "isolated largest; bridge between smaller cliques"
                    elif overlap == 1 and added_edges == 0:
                        # Isolation forces the direct cut to join the two
                        # smaller blocks.
                        form = "isolated largest; smaller cliques share one cut"
                    else:
                        raise AssertionError("unclassified isolated-largest geometry")
                    residual.add((sizes_sorted, overlap, added_edges, form))

    expected = {
        ((8, 8, 18), 0, 0, "three isolated cliques"),
        ((8, 8, 18), 0, 1, "isolated largest; bridge between smaller cliques"),
        ((8, 8, 19), 1, 0, "isolated largest; smaller cliques share one cut"),
        ((8, 9, 18), 1, 0, "isolated largest; smaller cliques share one cut"),
    }
    assert residual == expected
    return tuple(sorted(residual)), geometry_count, nonresidual_count, tuple(sorted(strict_checks))


def four_block_caps():
    caps = []
    for overlap in range(4):
        component_count = 4 - overlap
        maximum = max(
            sum(comb(x, 2) for x in sizes) + comb(component_count, 2)
            for sizes in integer_partitions(LOW + overlap, 4, MIN_LARGE)
        )
        caps.append(maximum)
    assert 5 * MIN_LARGE - 4 == 36 > LOW
    assert tuple(caps) == (135, 142, 151, 162)
    assert max(caps) < LOW_EDGE_FLOOR
    return tuple(caps)


def two_block_profiles():
    profiles = []
    for a in range(MIN_LARGE, LOW // 2 + 1):
        b = LOW - a
        if b >= K:
            continue
        p, q = a - MIN_LARGE, b - MIN_LARGE
        deficit = comb(HIGH, 2) - M + 26 * LOW - comb(a, 2) - comb(b, 2)
        if deficit < 0:
            continue
        assert p + q == 18
        assert a - (p + 1) == b - (q + 1) == 7
        assert a - p == b - q == 8
        assert b - (25 - (p + 1)) == 2
        assert b - (25 - (MIN_LARGE + p + 1)) == 10
        assert b - (25 - (MIN_LARGE + p + 2)) == 11
        profiles.append((a, b, p, q, deficit))
    assert tuple(row[-1] for row in profiles) == (6, 21, 34, 45, 54, 61, 66, 69, 70)
    return tuple(profiles)


def has_full_matching(rows):
    """Definition-level bipartite matching test for a small row family."""
    ordered = sorted(rows, key=len)

    def search(i, used):
        if i == len(ordered):
            return True
        return any(search(i + 1, used | {right}) for right in ordered[i] if right not in used)

    return search(0, set())


def uniform_row_small_cases():
    """Exhaustively falsify-test the uniform-row lemma for r <= 4."""
    results = []
    for r in range(1, 5):
        universe = range(r + 2)
        possible_rows = tuple(
            frozenset(row)
            for size in range(r, r + 3)
            for row in combinations(universe, size)
        )
        families = 0
        obstructions = 0
        for rows in combinations_with_replacement(possible_rows, r + 1):
            families += 1
            if not has_full_matching(rows):
                obstructions += 1
                assert len(set(rows)) == 1
                assert len(rows[0]) == r
        assert obstructions == comb(r + 2, r)
        results.append((r, families, obstructions))
    return tuple(results)


def main():
    assert LOW_EDGE_FLOOR == 171
    caps = four_block_caps()
    rows, summary, exceptions = arithmetic_rows()
    residual, geometries, nonresidual, strict = derive_residual_forms(exceptions)
    profiles = two_block_profiles()
    uniform_tests = uniform_row_small_cases()

    certificate = {
        "constants": [K, N, M, HIGH, LOW, MIN_LARGE, LOW_EDGE_FLOOR],
        "four_block_caps": caps,
        "three_block_summary": summary,
        "three_block_rows": rows,
        "exception_count": len(exceptions),
        "labelled_exception_geometries": geometries,
        "nonresidual_labelled_geometries": nonresidual,
        "strict_list_checks": strict,
        "derived_residual_forms": residual,
        "two_block_profiles": profiles,
        "uniform_row_small_cases": uniform_tests,
    }
    encoded = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()

    print("PASS clean-room Albertson h=19 geometry audit")
    print(f"four_block_caps={caps}")
    print(f"three_block_summary={summary}; exceptions={len(exceptions)}")
    print(f"labelled_exception_geometries={geometries}; nonresidual={nonresidual}")
    print(f"derived_residual_forms={residual}")
    print(f"two_block_profiles={profiles}")
    print(f"uniform_row_small_cases={uniform_tests}")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
