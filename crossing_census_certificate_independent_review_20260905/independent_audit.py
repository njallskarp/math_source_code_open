#!/usr/bin/env python3
"""Independent exact audit of the crossing-census certificate bundle.

This checker is intentionally not imported from the upstream project.  It
reconstructs planarizations, checks rotation systems through dart orbits, and
checks Kuratowski subdivisions by tracing every maximal branch-to-branch path.
It also audits the census/output linkage and isolates a definition mismatch in
the unrestricted-search output.

Usage:
    python3 independent_audit.py /path/to/crossing-number-two-subgraph
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path


EXPECTED_CENSUS_SHA256 = (
    "aef4486f0cb298201e6222405f96cfeeea28b031a7df54a36087ee103211ea66"
)
EXPECTED_C3_SHA256 = (
    "8f8ca3086722062e8e39a255846903c06c8fb1068ccb490c3bc17d647f44ee7f"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def edge(value) -> tuple[int, int]:
    require(len(value) == 2, f"not an edge: {value!r}")
    u, v = map(int, value)
    return (u, v) if u < v else (v, u)


def independent(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return len(set(a + b)) == 4


def validate_graph(n: int, edges) -> list[tuple[int, int]]:
    result = [edge(e) for e in edges]
    require(all(0 <= u < v < n for u, v in result), "bad vertex label or loop")
    require(len(result) == len(set(result)), "repeated edge")
    return result


def planarize(n: int, original_edges, configuration):
    """Use the certificate format's edge ordering, but rebuild every edge."""
    result = [edge(e) for e in original_edges]
    next_vertex = n
    for item in configuration:
        kind = item[0]
        if kind == "x":
            require(len(item) == 3, "bad one-crossing record")
            a, b = edge(item[1]), edge(item[2])
            require(a in result and b in result and a != b, "crossed edge absent")
            result.remove(a)
            result.remove(b)
            x = next_vertex
            result.extend(
                [edge((a[0], x)), edge((x, a[1])),
                 edge((b[0], x)), edge((x, b[1]))]
            )
            next_vertex += 1
        elif kind == "xx":
            require(len(item) == 4, "bad shared-edge crossing record")
            a, b, c = map(edge, item[1:])
            require(len({a, b, c}) == 3, "shared-edge record repeats an edge")
            require(all(e in result for e in (a, b, c)), "crossed edge absent")
            result.remove(a)
            result.remove(b)
            result.remove(c)
            x, y = next_vertex, next_vertex + 1
            result.extend(
                [edge((a[0], x)), edge((x, y)), edge((y, a[1])),
                 edge((b[0], x)), edge((x, b[1])),
                 edge((c[0], y)), edge((y, c[1]))]
            )
            next_vertex += 2
        else:
            raise AssertionError(f"unknown crossing kind: {kind!r}")
    validate_graph(next_vertex, result)
    return next_vertex, result


def rotation_is_spherical(n: int, edges, rotation) -> bool:
    """Check a rotation system by a permutation of directed edge-darts."""
    edges = validate_graph(n, edges)
    adjacency = {v: set() for v in range(n)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    require(set(rotation) == {str(v) for v in range(n)}, "wrong rotation keys")
    cyclic = {}
    for v in range(n):
        row = list(rotation[str(v)])
        require(len(row) == len(set(row)), f"duplicate rotation neighbor at {v}")
        require(set(row) == adjacency[v], f"wrong rotation neighbors at {v}")
        cyclic[v] = row

    component = {}
    for root in range(n):
        if root in component:
            continue
        component[root] = root
        todo = [root]
        while todo:
            u = todo.pop()
            for v in adjacency[u]:
                if v not in component:
                    component[v] = root
                    todo.append(v)

    successor = {}
    for u, v in itertools.chain(edges, ((v, u) for u, v in edges)):
        row = cyclic[v]
        successor[(u, v)] = (v, row[(row.index(u) + 1) % len(row)])
    require(set(successor.values()) == set(successor), "dart map is not a permutation")

    unseen = set(successor)
    faces = collections.Counter()
    while unseen:
        start = min(unseen)
        dart = start
        orbit = set()
        while dart not in orbit:
            require(dart in unseen, "face orbit merged into an earlier orbit")
            orbit.add(dart)
            unseen.remove(dart)
            dart = successor[dart]
        require(dart == start, "face orbit did not close at its start")
        faces[component[start[0]]] += 1

    vertices = collections.Counter(component.values())
    edge_counts = collections.Counter(component[u] for u, _ in edges)
    for root, vertex_count in vertices.items():
        if edge_counts[root] == 0:
            continue
        require(
            vertex_count - edge_counts[root] + faces[root] == 2,
            f"non-spherical rotation on component rooted at {root}",
        )
    return True


def kuratowski_type(n: int, edges, mask) -> str:
    """Recognize an exact K5/K3,3 subdivision, consuming every witness edge."""
    edges = validate_graph(n, edges)
    require(type(mask) is int and 0 <= mask < (1 << len(edges)), "bad witness mask")
    witness = [e for index, e in enumerate(edges) if mask & (1 << index)]
    require(witness, "empty witness")

    adjacency = collections.defaultdict(set)
    for u, v in witness:
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(all(len(row) >= 2 for row in adjacency.values()), "witness has a leaf")
    branches = sorted(v for v, row in adjacency.items() if len(row) != 2)
    require(branches, "witness has no branch vertices")

    consumed = set()
    contracted = collections.Counter()
    for start in branches:
        for neighbor in sorted(adjacency[start]):
            first_edge = edge((start, neighbor))
            if first_edge in consumed:
                continue
            previous, current = start, neighbor
            path_edges = [first_edge]
            while current not in branches:
                choices = adjacency[current] - {previous}
                require(len(choices) == 1, "non-path internal witness vertex")
                following = next(iter(choices))
                path_edges.append(edge((current, following)))
                previous, current = current, following
                require(len(path_edges) <= len(witness), "cycle in branch path")
            require(current != start, "loop after suppression")
            require(not consumed.intersection(path_edges), "witness paths overlap")
            consumed.update(path_edges)
            contracted[edge((start, current))] += 1
    require(consumed == set(witness), "witness has an unconsumed component")
    require(all(count == 1 for count in contracted.values()), "parallel core edge")

    core = set(contracted)
    degree = collections.Counter(v for e in core for v in e)
    if len(degree) == 5 and len(core) == 10 and set(degree.values()) == {4}:
        return "K5"
    if len(degree) == 6 and len(core) == 9 and set(degree.values()) == {3}:
        color = {}
        core_adjacency = collections.defaultdict(set)
        for u, v in core:
            core_adjacency[u].add(v)
            core_adjacency[v].add(u)
        for seed in sorted(degree):
            if seed in color:
                continue
            color[seed] = 0
            todo = [seed]
            while todo:
                u = todo.pop()
                for v in core_adjacency[u]:
                    if v not in color:
                        color[v] = 1 - color[u]
                        todo.append(v)
                    require(color[v] != color[u], "non-bipartite cubic core")
        require(collections.Counter(color.values()) == {0: 3, 1: 3}, "not K3,3")
        return "K3,3"
    raise AssertionError("witness core is neither K5 nor K3,3")


def good_two_crossing_configuration(edges, raw):
    configuration = [tuple([item[0], *map(edge, item[1:])]) for item in raw]
    if len(configuration) == 2 and all(item[0] == "x" for item in configuration):
        crossed = [e for item in configuration for e in item[1:]]
        require(len(set(crossed)) == 4, "two-crossing configuration repeats an edge")
        require(all(e in edges for e in crossed), "crossed edge not in graph")
        require(all(independent(item[1], item[2]) for item in configuration),
                "adjacent edges declared crossing")
    elif len(configuration) == 1 and configuration[0][0] == "xx":
        _, common, first, second = configuration[0]
        require(len({common, first, second}) == 3, "shared configuration repeats edge")
        require(all(e in edges for e in (common, first, second)), "crossed edge absent")
        require(independent(common, first) and independent(common, second),
                "adjacent edges declared crossing")
    else:
        raise AssertionError("not a complete two-crossing configuration")
    return configuration


def one_crossing_pairs(edges):
    return [(a, b) for a, b in itertools.combinations(edges, 2) if independent(a, b)]


def two_crossing_configurations(edges):
    pairs = one_crossing_pairs(edges)
    for first, second in itertools.combinations(pairs, 2):
        if len(set(first + second)) == 4:
            yield [("x", first[0], first[1]), ("x", second[0], second[1])]
    for common in edges:
        others = [e for e in edges if e != common and independent(common, e)]
        for first, second in itertools.permutations(others, 2):
            yield [("xx", common, first, second)]


def parse_rows(path: Path):
    rows = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        fields = line.split()
        require(len(fields) == 4, f"malformed {path.name}:{line_number}")
        tag, n_text, m_text, encoded = fields
        require(tag in {"CRIT2", "CRIT_GE3"}, "unknown census tag")
        n, m = int(n_text), int(m_text)
        edges = validate_graph(n, [part.split("-") for part in encoded.rstrip(",").split(",")])
        require(len(edges) == m, "declared edge count mismatch")
        rows.append((tag, n, edges))
    return rows


def c3_box_c3_edges():
    result = set()
    for i in range(3):
        for j in range(3):
            u = 3 * i + j
            result.add(edge((u, 3 * ((i + 1) % 3) + j)))
            result.add(edge((u, 3 * i + (j + 1) % 3)))
    return sorted(result)


def isomorphic_small_graph(left, right, n: int) -> bool:
    left_set, right_set = set(left), set(right)
    if sorted(collections.Counter(v for e in left_set for v in e).values()) != sorted(
        collections.Counter(v for e in right_set for v in e).values()
    ):
        return False
    for permutation in itertools.permutations(range(n)):
        if {edge((permutation[u], permutation[v])) for u, v in left_set} == right_set:
            return True
    return False


def audit_census(source: Path):
    certificate_path = source / "census_certificate.json"
    require(sha256(certificate_path) == EXPECTED_CENSUS_SHA256, "census hash mismatch")
    certificate = json.loads(certificate_path.read_text())
    members = certificate["members"]
    require(len(members) == 63, "wrong certified member count")

    member_keys = set()
    kuratowski_count = 0
    rotation_count = 0
    order_counts = collections.Counter()
    for index, record in enumerate(members):
        n = int(record["n"])
        edges = sorted(validate_graph(n, record["edges"]))
        degrees = collections.Counter(v for e in edges for v in e)
        require(set(degrees) == set(range(n)) and min(degrees.values()) >= 3,
                f"member {index} violates minimum degree")
        key = (n, tuple(edges))
        require(key not in member_keys, f"duplicate member {index}")
        member_keys.add(key)
        order_counts[n] += 1

        kuratowski_type(n, edges, record["nonplanar"])
        kuratowski_count += 1
        pairs = one_crossing_pairs(edges)
        require(len(pairs) == len(record["one_crossing"]), "one-crossing list mismatch")
        for pair, mask in zip(pairs, record["one_crossing"]):
            nn, planarized = planarize(n, edges, [("x", pair[0], pair[1])])
            kuratowski_type(nn, planarized, mask)
            kuratowski_count += 1

        configuration = good_two_crossing_configuration(edges, record["cr_le_2"]["config"])
        nn, planarized = planarize(n, edges, configuration)
        require(rotation_is_spherical(nn, planarized, record["cr_le_2"]["rotation"]),
                "bad two-crossing rotation")
        rotation_count += 1

        deletions = record["delete"]
        require(len(deletions) == len(edges), "wrong deletion-witness count")
        covered = set()
        for deletion in deletions:
            removed = edge(deletion["e"])
            require(removed in edges and removed not in covered, "bad/duplicate deletion")
            covered.add(removed)
            remainder = [e for e in edges if e != removed]
            if deletion["crossing"] is None:
                nn, planarized = n, remainder
            else:
                a, b = map(edge, deletion["crossing"])
                require(a in remainder and b in remainder and independent(a, b),
                        "bad deletion crossing")
                nn, planarized = planarize(n, remainder, [("x", a, b)])
            require(rotation_is_spherical(nn, planarized, deletion["rotation"]),
                    "bad deletion rotation")
            rotation_count += 1
        require(covered == set(edges), "incomplete deletion coverage")

    restricted_rows = []
    for n in range(6, 11):
        restricted_rows.extend(parse_rows(source / f"n{n}.txt"))
    crit2_keys = {(n, tuple(sorted(edges))) for tag, n, edges in restricted_rows if tag == "CRIT2"}
    require(member_keys == crit2_keys, "certificate set differs from CRIT2 output set")
    exceptional = [(n, edges) for tag, n, edges in restricted_rows if tag == "CRIT_GE3"]
    require(len(exceptional) == 1 and exceptional[0][0] == 9, "wrong exceptional row count")
    require(isomorphic_small_graph(exceptional[0][1], c3_box_c3_edges(), 9),
            "exceptional row is not C3 box C3")
    require(kuratowski_count == 5563, "unexpected census Kuratowski count")
    require(rotation_count == 1123, "unexpected census rotation count")
    return {
        "certified_members": len(members),
        "members_by_order": dict(sorted(order_counts.items())),
        "kuratowski_subdivisions": kuratowski_count,
        "rotation_systems": rotation_count,
        "restricted_rows": len(restricted_rows),
        "unique_cr_ge_3_row_is_c3_box_c3": True,
    }


def audit_c3(source: Path):
    certificate_path = source / "certificate.json"
    require(sha256(certificate_path) == EXPECTED_C3_SHA256, "C3 certificate hash mismatch")
    certificate = json.loads(certificate_path.read_text())
    n = int(certificate["graph"]["n"])
    edges = sorted(validate_graph(n, certificate["graph"]["edges"]))
    require(n == 9 and edges == c3_box_c3_edges(), "certificate graph is not C3 box C3")

    kuratowski_type(n, edges, certificate["G_nonplanar"])
    kuratowski_count = 1
    pairs = one_crossing_pairs(edges)
    require(len(pairs) == len(certificate["one_crossing_witnesses"]),
            "C3 one-crossing list mismatch")
    for pair, mask in zip(pairs, certificate["one_crossing_witnesses"]):
        nn, planarized = planarize(n, edges, [("x", pair[0], pair[1])])
        kuratowski_type(nn, planarized, mask)
        kuratowski_count += 1

    configurations = list(two_crossing_configurations(edges))
    require(len(configurations) == certificate["two_crossing_configs"] == 5841,
            "C3 two-crossing configuration mismatch")
    require(len(configurations) == len(certificate["kuratowski_witnesses"]),
            "C3 two-crossing witness mismatch")
    for configuration, mask in zip(configurations, certificate["kuratowski_witnesses"]):
        nn, planarized = planarize(n, edges, configuration)
        kuratowski_type(nn, planarized, mask)
        kuratowski_count += 1

    upper = certificate["cr_le_3"]
    require(len(upper["crossings"]) == 3, "upper witness is not a 3-crossing witness")
    upper_configuration = [("x", edge(a), edge(b)) for a, b in upper["crossings"]]
    crossed = [e for item in upper_configuration for e in item[1:]]
    require(len(set(crossed)) == 6 and all(e in edges for e in crossed),
            "upper witness repeats or invents an edge")
    require(all(independent(item[1], item[2]) for item in upper_configuration),
            "upper witness crosses adjacent edges")
    nn, planarized = planarize(n, edges, upper_configuration)
    require(rotation_is_spherical(nn, planarized, upper["rotation"]),
            "bad C3 upper rotation")

    deletion_rows = certificate["cr_G_minus_e_le_1"]
    require(len(deletion_rows) == len(edges), "wrong C3 deletion count")
    covered = set()
    for row in deletion_rows:
        removed = edge(row["deleted"])
        require(removed in edges and removed not in covered, "bad C3 deletion")
        covered.add(removed)
        remainder = [e for e in edges if e != removed]
        if row["crossing"] is None:
            nn, planarized = n, remainder
        else:
            a, b = map(edge, row["crossing"])
            require(a in remainder and b in remainder and independent(a, b),
                    "bad C3 deletion crossing")
            nn, planarized = planarize(n, remainder, [("x", a, b)])
        require(rotation_is_spherical(nn, planarized, row["rotation"]),
                "bad C3 deletion rotation")
    require(covered == set(edges), "incomplete C3 deletion coverage")
    require(kuratowski_count == 5941, "unexpected C3 Kuratowski count")
    return {
        "graph": "C3 box C3",
        "one_crossing_configurations": len(pairs),
        "two_crossing_configurations": len(configurations),
        "kuratowski_subdivisions": kuratowski_count,
        "three_crossing_rotation_systems": 1,
        "edge_deletion_rotation_systems": len(deletion_rows),
    }


def audit_unrestricted_outputs(source: Path):
    by_order = {}
    total = isolated = cr_ge_3 = 0
    for n in range(6, 10):
        rows = parse_rows(source / "unrestricted" / f"u{n}.txt")
        isolated_here = 0
        for tag, declared_n, edges in rows:
            require(declared_n == n, "unrestricted file/order mismatch")
            degree = collections.Counter(v for e in edges for v in e)
            has_isolate = len(degree) < n
            isolated_here += int(has_isolate)
            isolated += int(has_isolate)
            cr_ge_3 += int(tag == "CRIT_GE3")
        total += len(rows)
        by_order[n] = {"edge_deletion_survivors": len(rows), "with_isolate": isolated_here}
    require((total, isolated, cr_ge_3) == (311, 51, 1), "unexpected unrestricted counts")
    return {
        "by_order": by_order,
        "edge_deletion_survivors": total,
        "not_standard_critical_due_to_isolates": isolated,
        "standard_critical_candidates": total - isolated,
        "cr_ge_3_rows": cr_ge_3,
    }


def mutation_smoke(source: Path) -> None:
    certificate = json.loads((source / "certificate.json").read_text())
    edges = c3_box_c3_edges()
    try:
        kuratowski_type(9, edges, 1 << len(edges))
    except AssertionError:
        pass
    else:
        raise AssertionError("out-of-range Kuratowski mutation was accepted")

    upper = certificate["cr_le_3"]
    configuration = [("x", edge(a), edge(b)) for a, b in upper["crossings"]]
    nn, planarized = planarize(9, edges, configuration)
    mutated = {key: list(value) for key, value in upper["rotation"].items()}
    victim = next(key for key, value in mutated.items() if value)
    mutated[victim] = mutated[victim][1:]
    try:
        rotation_is_spherical(nn, planarized, mutated)
    except AssertionError:
        return
    raise AssertionError("truncated rotation mutation was accepted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    require(source.is_dir(), "source directory does not exist")

    summary = {
        "c3_certificate": audit_c3(source),
        "census_certificate": audit_census(source),
        "certificate_sha256": EXPECTED_C3_SHA256,
        "census_certificate_sha256": EXPECTED_CENSUS_SHA256,
        "unrestricted_output_scope": audit_unrestricted_outputs(source),
    }
    mutation_smoke(source)
    summary["mutation_smoke"] = "rejected out-of-range mask and truncated rotation"
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
