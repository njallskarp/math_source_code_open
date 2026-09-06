#!/usr/bin/env python3
"""Independent exact review of the M=216 intrinsic defect partition.

No researcher module or solver is imported.  Synthetic 43-vertex graphs test
only physical relabeling and are not Ramsey graphs or feasibility witnesses.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


N = 43
Z = frozenset((0, 1))
E = frozenset(range(2, 7))
C = frozenset(range(7, N))
PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
PAIRS43 = tuple(itertools.combinations(range(N), 2))
GROUP = tuple(z + e for z in itertools.permutations(range(2))
              for e in itertools.permutations(range(2, 7)))
CERTIFICATE_SHA = "6edd4bfa43dbd652acdbd2e83d6509d769a724459518bfe75a7a102c383aa94b"
LABELED_SHA = "c5f0657c29e84a085ccdfcfdfa5666054c1ed1ebd2048cc8bf259532f8671dc8"
SOURCE_HASHES = {
    "README.md": "faadd29d24e07f30954401ad89c31fe83bb172f7195f10e385dd3d0d85180b0d",
    "derive.py": "7f3b5b4a29ab670d6ef313953f95734dbcb6266efe2f5c4584128620af43263e",
    "check.py": "fa525367d021e71c9699913b0e384a48cbb46498f1c89434c3b4fdb95b15a12d",
    "census.cpp": "b24d59135843584d1fab79aedc5ae1412584a8deea7190958da23a76bd262b9c",
    "certificate.json": CERTIFICATE_SHA,
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def adjacency7(mask: int) -> tuple[int, ...]:
    rows = [0] * 7
    for bit, (u, v) in enumerate(PAIRS7):
        if mask >> bit & 1:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return tuple(rows)


def exceptional_deficits(mask: int) -> tuple[int, ...]:
    rows = adjacency7(mask)
    out = []
    for vertex in range(7):
        weighted = 2 * (rows[vertex] & 0b11).bit_count()
        weighted += (rows[vertex] & sum(1 << v for v in E)).bit_count()
        out.append(weighted - (5 if vertex in Z else 4))
    return tuple(out)


FIVE_MASKS7 = tuple(sum(1 << PAIR_INDEX7[pair]
                        for pair in itertools.combinations(vertices, 2))
                    for vertices in itertools.combinations(range(7), 5))


def admissible_core(mask: int) -> bool:
    deficits = exceptional_deficits(mask)
    if min(deficits) < 0 or sum(deficits) > 2:
        return False
    return all(mask & five_mask not in (0, five_mask) for five_mask in FIVE_MASKS7)


def transport7(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for bit, (u, v) in enumerate(PAIRS7):
        if mask >> bit & 1:
            pair = tuple(sorted((permutation[u], permutation[v])))
            result |= 1 << PAIR_INDEX7[pair]
    return result


def exhaustive_cores() -> tuple[list[int], list[dict[str, object]]]:
    labeled = [mask for mask in range(1 << 21) if admissible_core(mask)]
    need(len(labeled) == 1480, "complete 21-bit census")
    raw = "".join(f"{mask}\n" for mask in labeled).encode("ascii")
    need(sha256(raw) == LABELED_SHA, "labeled stream identity")

    classes = defaultdict(list)
    for mask in labeled:
        canonical = min(transport7(mask, permutation) for permutation in GROUP)
        classes[canonical].append(mask)
    need(len(classes) == 14, "core orbit count")
    records = []
    covered = set()
    for representative in sorted(classes):
        orbit = {transport7(representative, permutation) for permutation in GROUP}
        need(orbit == set(classes[representative]), "complete disjoint orbit")
        need(not covered & orbit, "orbit overlap")
        covered |= orbit
        deficits = exceptional_deficits(representative)
        records.append({
            "central_red_excess": 2 - sum(deficits),
            "closed_blue_degree19_pair": not bool(representative & 1),
            "exceptional_red_excess": list(deficits),
            "mask": representative,
            "orbit_size": len(orbit),
        })
    need(covered == set(labeled), "orbit coverage")
    need([(record["mask"], record["orbit_size"]) for record in records] == [
        (4094, 10), (40573, 60), (65209, 60), (111865, 30),
        (111989, 60), (113913, 60), (114037, 120), (128249, 120),
        (128373, 240), (380153, 120), (380277, 240), (451059, 120),
        (451061, 120), (451431, 120)], "canonical orbit census")
    blue = [record for record in records if record["closed_blue_degree19_pair"]]
    need(len(blue) == 1 and blue[0]["mask"] == 4094 and blue[0]["orbit_size"] == 10,
         "unique blue-pair core orbit")
    return labeled, records


def reconstructed_roots(records: list[dict[str, object]]) -> list[dict[str, object]]:
    roots = []
    for core in records:
        if core["closed_blue_degree19_pair"]:
            continue
        excess = core["central_red_excess"]
        if excess == 0:
            partitions = [[]]
        elif excess == 1:
            partitions = [[[7, 1]]]
        else:
            need(excess == 2, "central excess range")
            partitions = [[[7, 2]], [[7, 1], [8, 1]]]
        for partition in partitions:
            roots.append({"central_red_excess": partition,
                          "core_mask": core["mask"], "index": len(roots)})
    need(len(roots) == 15, "complete root count")
    need(Counter(sum(value for _, value in root["central_red_excess"])
                 for root in roots) == {0: 10, 1: 1, 2: 4}, "root excess census")
    return roots


def validate_document(document: dict[str, object], records: list[dict[str, object]],
                      roots: list[dict[str, object]]) -> None:
    need(document.get("format") == "r55-m216-intrinsic-partition-v1", "format")
    need(document.get("degree_profile") == [19, 19] + [20] * 5 + [21] * 36,
         "degree profile")
    need(document.get("labeled_necessary_cores") == 1480, "labeled core count")
    need(document.get("cores") == records, "all core certificate records")
    need(document.get("roots") == roots, "all root certificate records")


def certificate_check(directory: Path, records: list[dict[str, object]],
                      roots: list[dict[str, object]]) -> dict[str, object]:
    identities = {}
    for name, expected in SOURCE_HASHES.items():
        observed = sha256((directory / name).read_bytes())
        need(observed == expected, "pinned source identity: " + name)
        identities[name] = observed
    document = json.loads((directory / "certificate.json").read_text())
    validate_document(document, records, roots)
    return identities


def contains_mono_triangle(order: int, mask: int) -> bool:
    pairs = tuple(itertools.combinations(range(order), 2))
    index = {pair: i for i, pair in enumerate(pairs)}
    for triple in itertools.combinations(range(order), 3):
        values = {mask >> index[pair] & 1
                  for pair in itertools.combinations(triple, 2)}
        if len(values) == 1:
            return True
    return False


def small_lemma_checks() -> dict[str, object]:
    # This is the only finite premise used in the elementary proof of R(3,4)<=9.
    for mask in range(1 << 15):
        need(contains_mono_triangle(6, mask), "R(3,3)<=6")

    pairs5 = tuple(itertools.combinations(range(5), 2))
    equality = []
    for mask in range(1 << 10):
        red_tri = False
        for triple in itertools.combinations(range(5), 3):
            bits = [pairs5.index(pair) for pair in itertools.combinations(triple, 2)]
            if all(mask >> bit & 1 for bit in bits):
                red_tri = True
                break
        if red_tri:
            continue
        need(mask.bit_count() <= 6, "triangle-free five-vertex edge bound")
        if mask.bit_count() == 6:
            cuts = []
            for side in itertools.combinations(range(5), 2):
                side = set(side)
                cuts.append(sum(1 << bit for bit, (u, v) in enumerate(pairs5)
                                if (u in side) != (v in side)))
            need(mask in cuts, "six-edge equality is K2,3")
            equality.append(mask)
    need(len(equality) == 10, "labeled K2,3 equality count")

    impossible_labels = 0
    for labels in itertools.product((2, 3), repeat=3):
        if labels[0] != labels[1] and labels[1] != labels[2] and labels[2] != labels[0]:
            impossible_labels += 1
    need(impossible_labels == 0, "odd triangle two-label contradiction")
    return {"R33_colorings": 32768, "triangle_free_order5_colorings": 1024,
            "labeled_K23_equalities": len(equality),
            "triangle_codegree_labelings": 8}


def accounting_check() -> dict[str, object]:
    degrees = [19, 19] + [20] * 5 + [21] * 36
    red_caps = [85, 85] + [93] * 5 + [100] * 36
    blue_caps = [115, 115] + [107] * 5 + [100] * 36
    edges = sum(degrees) // 2
    mono_incidence = 3 * (math.comb(N, 3) -
                          sum(degree * (N - 1 - degree) for degree in degrees) // 2)
    need((edges, sum(red_caps), sum(blue_caps), mono_incidence) ==
         (447, 4235, 4365, 8598), "global defect accounting")
    total_defect = sum(red_caps) + sum(blue_caps) - mono_incidence
    red_defect_residue = sum(red_caps) % 3
    need((total_defect, red_defect_residue) == (2, 2), "two red deficit units")
    constants = {degree: math.comb(42 - degree, 2) - edges + 21 * degree
                 for degree in set(degrees)}
    need(constants == {19: 205, 20: 204, 21: 204}, "neighborhood identity constants")

    # Under a blue 01 edge the exact arithmetic forces the 14-vertex obstacle.
    e_internal_edges = 1
    central_neighbors_per_z = 19 - 5
    e_to_a = 2 * central_neighbors_per_z
    a_edges = 85 - e_internal_edges - e_to_a
    need((central_neighbors_per_z, e_to_a, a_edges) == (14, 28, 56),
         "blue-pair branch arithmetic")
    regular_local_sum = math.comb(5, 2) - 56 + 8 * 8
    need(regular_local_sum == 18 and 12 + 6 == regular_local_sum,
         "14-vertex regular neighborhood equality")

    buckets = []
    for eta in (0, 1):
        for cross in range(11):
            for internal in range(11):
                total = 4 * eta + 3 * cross + 2 * internal - 30
                if total < 0 or total > 2:
                    continue
                if cross < 10 - 4 * eta or cross + internal < 10:
                    continue
                buckets.append((eta, cross, internal))
    need(buckets == [(0, 10, 0), (0, 10, 1), (1, 6, 4), (1, 6, 5),
                     (1, 7, 3), (1, 8, 2)], "numerical bucket completeness")
    return {"red_edges": edges, "red_cap_sum": sum(red_caps),
            "blue_cap_sum": sum(blue_caps), "monochromatic_triangle_incidence": mono_incidence,
            "total_defect": total_defect, "red_defect": 2, "blue_defect": 0,
            "neighborhood_constants": constants, "blue_pair_forced_A_edges": a_edges,
            "regular_local_triangle_sum": regular_local_sum,
            "numerical_buckets": buckets}


def central_assignments(root: dict[str, object]):
    pattern = root["central_red_excess"]
    if not pattern:
        yield {}
    elif pattern == [[7, 1]]:
        for vertex in C:
            yield {vertex: 1}
    elif pattern == [[7, 2]]:
        for vertex in C:
            yield {vertex: 2}
    else:
        need(pattern == [[7, 1], [8, 1]], "central partition type")
        for u, v in itertools.combinations(C, 2):
            yield {u: 1, v: 1}


def canonicalize_support(assignment: dict[int, int], pattern: list[list[int]]):
    targets = [vertex for vertex, _ in pattern]
    sources = sorted(assignment)
    remaining_sources = [vertex for vertex in C if vertex not in assignment]
    remaining_targets = [vertex for vertex in C if vertex not in targets]
    permutation = list(range(N))
    for source, target in zip(sources + remaining_sources, targets + remaining_targets):
        permutation[source] = target
    need(sorted(permutation) == list(range(N)), "central support permutation")
    moved = {permutation[vertex]: value for vertex, value in assignment.items()}
    need(moved == dict(pattern), "canonical central deficit support")
    return permutation


def physical_transport_checks(roots: list[dict[str, object]]) -> dict[str, int]:
    placements = 0
    edge_checks = 0
    invariant_checks = 0
    for root in roots:
        graph = {(u, v): int(((u + 5) * (v + 11) + root["index"]) % 13 < 6)
                 for u, v in PAIRS43}
        for bit, pair in enumerate(PAIRS7):
            graph[pair] = root["core_mask"] >> bit & 1
        for assignment in central_assignments(root):
            permutation = canonicalize_support(assignment, root["central_red_excess"])
            moved = {tuple(sorted((permutation[u], permutation[v]))): value
                     for (u, v), value in graph.items()}
            need(len(moved) == 903, "all physical edges retained")
            for pair, value in graph.items():
                image = tuple(sorted((permutation[pair[0]], permutation[pair[1]])))
                need(moved[image] == value, "physical edge transport")
                edge_checks += 1
            placements += 1

        # One nontrivial exceptional-core transport per root also preserves
        # degrees and both literal local-triangle counts vertex by vertex.
        permutation7 = GROUP[(37 * root["index"] + 1) % len(GROUP)]
        permutation = list(permutation7) + list(range(7, N))
        moved = {tuple(sorted((permutation[u], permutation[v]))): value
                 for (u, v), value in graph.items()}
        for vertex in range(N):
            degree = sum(graph[tuple(sorted((vertex, other)))]
                         for other in range(N) if other != vertex)
            image_degree = sum(moved[tuple(sorted((permutation[vertex], permutation[other])))]
                               for other in range(N) if other != vertex)
            need(degree == image_degree, "degree transport")
            red_triangles = blue_triangles = 0
            moved_red = moved_blue = 0
            others = [other for other in range(N) if other != vertex]
            for a, b in itertools.combinations(others, 2):
                values = (graph[tuple(sorted((vertex, a)))],
                          graph[tuple(sorted((vertex, b)))], graph[tuple(sorted((a, b)))])
                red_triangles += all(values)
                blue_triangles += not any(values)
                images = (moved[tuple(sorted((permutation[vertex], permutation[a])))],
                          moved[tuple(sorted((permutation[vertex], permutation[b])))],
                          moved[tuple(sorted((permutation[a], permutation[b])))])
                moved_red += all(images)
                moved_blue += not any(images)
            need((red_triangles, blue_triangles) == (moved_red, moved_blue),
                 "literal triangle transport")
            invariant_checks += 1
    need((placements, edge_checks, invariant_checks) == (1378, 1_244_334, 645),
         "physical transport census")
    return {"central_defect_placements": placements, "physical_edge_checks": edge_checks,
            "degree_and_triangle_vertex_checks": invariant_checks}


def formula_semantics(records: list[dict[str, object]],
                      roots: list[dict[str, object]]) -> dict[str, int]:
    by_mask = {record["mask"]: record for record in records}
    red_caps = [85, 85] + [93] * 5 + [100] * 36
    blue_caps = [115, 115] + [107] * 5 + [100] * 36
    for root in roots:
        core = by_mask[root["core_mask"]]
        central = dict(root["central_red_excess"])
        deficits = core["exceptional_red_excess"] + [central.get(v, 0) for v in C]
        need(len(deficits) == N and min(deficits) >= 0 and sum(deficits) == 2,
             "complete root deficit vector")
        red_targets = [cap - deficit for cap, deficit in zip(red_caps, deficits)]
        need(min(red_targets) >= 0 and sum(red_targets) % 3 == 0,
             "red triangle targets")
        need(sum(blue_caps) % 3 == 0, "blue triangle targets")
    # For a Boolean ten-edge five-set sum, this is exactly the exclusion of
    # both monochromatic endpoint values, with no intermediate value removed.
    need([value for value in range(11) if 1 <= value <= 9] == list(range(1, 10)),
         "five-set double inequality")
    return {"Boolean_edge_variables": math.comb(N, 2),
            "fixed_exceptional_core_edges_per_root": math.comb(7, 2),
            "remaining_physical_edges_per_root": math.comb(N, 2) - math.comb(7, 2),
            "degree_equations_per_root": N,
            "red_triangle_equations_per_root": N,
            "blue_triangle_equations_per_root": N,
            "triangle_monomials_per_vertex_per_color": math.comb(42, 2),
            "five_set_double_inequalities_per_root": math.comb(N, 5)}


def parent_transport_check() -> tuple[int, list[int]]:
    candidates = [(transport7(901619, permutation), permutation) for permutation in GROUP]
    value, permutation = min(candidates)
    need(value == 380277, "h2731 parent core canonicalization")
    return value, list(permutation)


def mutation_controls(document: dict[str, object], records, roots) -> int:
    changes = []
    for name in ("drop_core", "orbit", "drop_root", "defect", "degree_profile", "mask"):
        altered = json.loads(json.dumps(document))
        if name == "drop_core":
            altered["cores"].pop()
        elif name == "orbit":
            altered["cores"][0]["orbit_size"] += 1
        elif name == "drop_root":
            altered["roots"].pop()
        elif name == "defect":
            altered["roots"][0]["central_red_excess"] = []
        elif name == "degree_profile":
            altered["degree_profile"][0] = 20
        else:
            altered["cores"][1]["mask"] += 1
        try:
            validate_document(altered, records, roots)
        except ValueError:
            changes.append(name)
        else:
            raise ValueError("mutation accepted")
    return len(changes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path,
                        help="ramsey_r55_m216_intrinsic_partition directory")
    args = parser.parse_args()
    labeled, records = exhaustive_cores()
    roots = reconstructed_roots(records)
    identities = certificate_check(args.source, records, roots)
    document = json.loads((args.source / "certificate.json").read_text())
    parent, parent_permutation = parent_transport_check()
    result = {
        "status": "INDEPENDENTLY_ACCEPTED_M216_INTRINSIC_PARTITION",
        "scope": "explicit cap profile partition; no root feasibility or M-slice exclusion",
        "accounting": accounting_check(),
        "small_lemmas": small_lemma_checks(),
        "core_census": {"labeled": len(labeled), "orbits": len(records),
                        "blue_pair_labeled": sum(not bool(mask & 1) for mask in labeled),
                        "remaining_orbits": 13, "labeled_sha256": LABELED_SHA},
        "root_partition": {"roots": len(roots),
                           "by_central_excess": dict(Counter(
                               sum(value for _, value in root["central_red_excess"])
                               for root in roots)),
                           **physical_transport_checks(roots)},
        "formula_semantics": formula_semantics(records, roots),
        "h2731_transport": {"canonical_core": parent,
                            "permutation": parent_permutation},
        "source_hashes": identities,
        "rejected_certificate_mutations": mutation_controls(document, records, roots),
        "trust_boundary": [
            "explicit local triangle caps (or imported h2099 extrema if read as hard deficiency)",
            "displayed hand reduction including the elementary R(3,4)<=9 argument",
            "CPython exact semantics, SHA-256, and ordinary hardware",
        ],
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
