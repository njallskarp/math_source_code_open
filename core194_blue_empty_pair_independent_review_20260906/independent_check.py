#!/usr/bin/env python3
"""Clean-room exact check of the Core194 blue-empty-pair lemma.

The checker deliberately does not import the target's Python modules.  It
decodes the four-triangle core directly from the published 18-bit orbit word,
enumerates all relevant five-sets, validates the two edge-list boundary
fixtures, and checks the fixed-edge clause translation by a complete truth
table.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import shutil
from pathlib import Path
from typing import Iterable


CORE_WORD = "100110110110110100"
TRIANGLES = tuple(tuple(range(3 * i, 3 * i + 3)) for i in range(4))
U, V, F = 12, 13, 14


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def edge(a: int, b: int) -> tuple[int, int]:
    require(a != b, "loops are not edges")
    return (a, b) if a < b else (b, a)


def core_red_edges(word: str = CORE_WORD) -> set[tuple[int, int]]:
    """Decode the four C3-orbit triangles without target code."""
    require(len(word) == 18 and set(word) <= {"0", "1"}, "bad core word")
    red: set[tuple[int, int]] = set()
    for triangle in TRIANGLES:
        red.update(itertools.combinations(triangle, 2))
    for block, (left, right) in enumerate(itertools.combinations(range(4), 2)):
        for residue_left in range(3):
            for residue_right in range(3):
                offset = (residue_right - residue_left) % 3
                if word[3 * block + offset] == "1":
                    red.add(edge(3 * left + residue_left, 3 * right + residue_right))
    return red


def monochromatic_fives(
    order: int, red: set[tuple[int, int]]
) -> dict[str, list[tuple[int, ...]]]:
    answer: dict[str, list[tuple[int, ...]]] = {"red": [], "blue": []}
    for vertices in itertools.combinations(range(order), 5):
        colors = {edge(a, b) in red for a, b in itertools.combinations(vertices, 2)}
        if colors == {True}:
            answer["red"].append(vertices)
        elif colors == {False}:
            answer["blue"].append(vertices)
    return answer


def is_monochromatic(
    vertices: Iterable[int], color: str, red: set[tuple[int, int]]
) -> bool:
    want_red = color == "red"
    return all(
        (edge(a, b) in red) == want_red
        for a, b in itertools.combinations(vertices, 2)
    )


def signature_graph(mask: int) -> set[tuple[int, int]]:
    require(0 <= mask < 16, "signature mask outside 0,...,15")
    red = core_red_edges()
    for triangle_index, triangle in enumerate(TRIANGLES):
        if mask & (1 << triangle_index):
            red.update(edge(x, F) for x in triangle)
    # Every unlisted edge incident with U,V,F is blue.  In particular U,V
    # are empty, UV is blue, and F is a common blue neighbor of U,V.
    return red


def canonical_json_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def core_structure() -> dict[str, object]:
    red = core_red_edges()
    require(len(red) == 42, "Core194 should have 42 red edges")
    require(not any(monochromatic_fives(12, red).values()), "core has a monochromatic K5")

    rotation = {3 * i + r: 3 * i + (r + 1) % 3 for i in range(4) for r in range(3)}
    require(
        all(((a, b) in red) == (edge(rotation[a], rotation[b]) in red) for a, b in itertools.combinations(range(12), 2)),
        "core is not invariant under the stated order-three action",
    )

    blue_cross_counts: list[int] = []
    for left, right in itertools.combinations(range(4), 2):
        cross = [edge(a, b) for a in TRIANGLES[left] for b in TRIANGLES[right]]
        count = sum(e not in red for e in cross)
        require(count > 0, "a pair of red triangles has no blue cross-edge")
        blue_cross_counts.append(count)

    complementary_k4s: dict[str, list[list[int]]] = {}
    for omitted in range(4):
        allowed = [v for i, triangle in enumerate(TRIANGLES) if i != omitted for v in triangle]
        witnesses = [
            list(q)
            for q in itertools.combinations(allowed, 4)
            if all(edge(a, b) in red for a, b in itertools.combinations(q, 2))
        ]
        require(witnesses, f"no complementary red K4 when triangle {omitted} is omitted")
        complementary_k4s[str(omitted)] = witnesses

    return {
        "red_edges": len(red),
        "blue_cross_edges_by_triangle_pair": blue_cross_counts,
        "complementary_red_k4_counts": {
            omitted: len(witnesses) for omitted, witnesses in complementary_k4s.items()
        },
        "lexicographically_first_complementary_red_k4": {
            omitted: witnesses[0] for omitted, witnesses in complementary_k4s.items()
        },
        "order_three_invariant": True,
    }


def signature_obstructions(certificate_path: Path) -> dict[str, object]:
    all_obstructions: list[dict[str, object]] = []
    expected_color: dict[int, str] = {}
    for mask in range(16):
        red = signature_graph(mask)
        cliques = monochromatic_fives(15, red)
        color = "red" if mask.bit_count() >= 3 else "blue"
        require(cliques[color], f"signature {mask} lacks its structural obstruction")
        expected_color[mask] = color
        all_obstructions.append(
            {
                "mask": mask,
                "red": [list(q) for q in cliques["red"]],
                "blue": [list(q) for q in cliques["blue"]],
            }
        )

    certificate = json.loads(certificate_path.read_text())
    require(certificate["bits"] == CORE_WORD, "certificate uses another core")
    require(certificate["empty_pair"] == [U, V], "certificate uses another pair")
    require(certificate["third_fixed"] == F, "certificate uses another third vertex")
    rows = certificate["forbidden_common_blue_signatures"]
    require([row["mask"] for row in rows] == list(range(16)), "certificate does not cover all signatures")
    for row in rows:
        mask = row["mask"]
        require(row["color"] == expected_color[mask], "wrong certificate obstruction color")
        vertices = row["vertices"]
        require(len(vertices) == len(set(vertices)) == 5, "certificate witness is not a five-set")
        require(
            is_monochromatic(vertices, row["color"], signature_graph(mask)),
            f"certificate witness for mask {mask} is not monochromatic",
        )

    return {
        "signature_masks_checked": 16,
        "blue_signature_cases": sum(color == "blue" for color in expected_color.values()),
        "red_signature_cases": sum(color == "red" for color in expected_color.values()),
        "submitted_witness_pairs_checked": 16 * 10,
        "complete_obstruction_list_sha256": canonical_json_hash(all_obstructions),
    }


def read_edge_list(path: Path) -> tuple[int, set[tuple[int, int]]]:
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    require(lines, f"empty edge list: {path}")
    order = int(lines[0])
    red: set[tuple[int, int]] = set()
    for line in lines[1:]:
        a, b = map(int, line.split())
        require(0 <= a < b < order, f"bad edge in {path}: {line}")
        require((a, b) not in red, f"duplicate edge in {path}: {line}")
        red.add((a, b))
    return order, red


def fixture_check(path: Path, expected_order: int, pair_red: bool) -> dict[str, object]:
    order, red = read_edge_list(path)
    require(order == expected_order, "fixture order mismatch")
    require({e for e in red if e[1] < 12} == core_red_edges(), "fixture core mismatch")
    require(
        all(edge(core, fixed) not in red for core in range(12) for fixed in range(12, order)),
        "fixture has a nonempty fixed signature",
    )
    require(((U, V) in red) == pair_red, "fixture pair has the wrong color")
    cliques = monochromatic_fives(order, red)
    require(not cliques["red"] and not cliques["blue"], "fixture has a monochromatic K5")
    common = [x for x in range(14, order) if edge(U, x) not in red and edge(V, x) not in red]
    expected_common = [] if order == 14 else [14]
    require(common == expected_common, "fixture common-neighbor count mismatch")

    rotation = {3 * i + r: 3 * i + (r + 1) % 3 for i in range(4) for r in range(3)}
    rotation.update({x: x for x in range(12, order)})
    require(
        all(((a, b) in red) == (edge(rotation[a], rotation[b]) in red) for a, b in itertools.combinations(range(order), 2)),
        "fixture violates the order-three action",
    )
    return {
        "vertices": order,
        "red_edges": len(red),
        "five_sets_checked": sum(1 for _ in itertools.combinations(range(order), 5)),
        "pair_red": pair_red,
        "common_blue_fixed_neighbors": common,
        "order_three_invariant": True,
    }


def clause_bridge() -> dict[str, object]:
    fixed_pairs = list(itertools.combinations(range(33, 43), 2))
    variable = {pair: 166 + index for index, pair in enumerate(fixed_pairs)}
    require(variable[(33, 34)] == 166, "first empty-pair variable is not 166")
    mapped = [
        {
            "fixed_vertex": f,
            "clause": [variable[(33, f)], variable[(34, f)]],
        }
        for f in range(35, 43)
    ]
    require(
        [entry["clause"] for entry in mapped]
        == [[167 + i, 175 + i] for i in range(8)],
        "fixed-pair variable map does not match the claimed bridge",
    )

    blue_count = red_count = union_count = overlap_count = 0
    for pair_red, contacts in itertools.product((False, True), itertools.product((False, True), repeat=16)):
        blue_child = (not pair_red) and all(contacts[2 * i] or contacts[2 * i + 1] for i in range(8))
        red_child = pair_red
        semantic_guard = pair_red or all(contacts[2 * i] or contacts[2 * i + 1] for i in range(8))
        require((blue_child or red_child) == semantic_guard, "split does not cover the intended guard")
        blue_count += int(blue_child)
        red_count += int(red_child)
        union_count += int(blue_child or red_child)
        overlap_count += int(blue_child and red_child)

    require((blue_count, red_count, union_count, overlap_count) == (6561, 65536, 72097, 0), "truth-table count mismatch")
    return {
        "first_empty_pair": [33, 34],
        "pair_variable": 166,
        "blue_branch_binary_clauses": mapped,
        "assignments_checked": 131072,
        "accepted_blue_branch": blue_count,
        "accepted_red_branch": red_count,
        "accepted_union": union_count,
        "branch_overlap": overlap_count,
    }


def full_formula_check(base: Path, blue: Path, red: Path) -> dict[str, object]:
    expected = {
        "base": (base, 24_968_424, "214cbdad727ec3f48e97e62246134b341719277981119bd6b89baa5475b2dbb4"),
        "blue": (blue, 24_968_511, "21b9a5e9d4b4ddb9e91388abf6bc45d87488f356adbcbc70fb60d752ad5f13e1"),
        "red": (red, 24_968_430, "941df55fb7a26c64b1e72dfdff819d3cad15409a5eb83521a57ac2e353562224"),
    }


    identities: dict[str, object] = {}
    for name, (path, expected_bytes, expected_hash) in expected.items():
        require(path.is_file(), f"missing {name} CNF")
        require(path.stat().st_size == expected_bytes, f"{name} CNF byte count mismatch")
        actual_hash = sha256(path)
        require(actual_hash == expected_hash, f"{name} CNF hash mismatch")
        identities[name] = {"bytes": expected_bytes, "sha256": actual_hash}

    with base.open("rb") as stream:
        require(stream.readline() == b"p cnf 34320 617936\n", "base header mismatch")
        base_body = stream.read()
    tails = {
        "blue": b"-166 0\n" + b"".join(f"{167 + i} {175 + i} 0\n".encode() for i in range(8)),
        "red": b"166 0\n",
    }
    for name, path, clauses in (("blue", blue, 617_945), ("red", red, 617_937)):
        with path.open("rb") as stream:
            require(stream.readline() == f"p cnf 34320 {clauses}\n".encode(), f"{name} header mismatch")
            body = stream.read()
        require(body == base_body + tails[name], f"{name} child is not exact base plus intended tail")

    base_lines = set(base_body.splitlines())
    inherited = {
        f"166 {211 + i} {222 + i} 0".encode()
        for i in range(4, 11)
    }
    require(inherited <= base_lines, "one or more inherited blue-moving-triangle clauses is absent")
    return {
        "identities": identities,
        "base_preserved_exactly": True,
        "blue_tail_clauses": 9,
        "red_tail_clauses": 1,
        "inherited_blue_moving_triangle_clauses_found": 7,
    }


def build_children_from_base(base: Path, output_dir: Path) -> tuple[Path, Path]:
    require(base.is_file(), "cannot build children without the rebuilt base")
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {"blue": output_dir / "blue.cnf", "red": output_dir / "red.cnf"}
    tails = {
        "blue": [(-166,), *[(167 + i, 175 + i) for i in range(8)]],
        "red": [(166,)],
    }
    for name, output in outputs.items():
        with base.open("rb") as source, output.open("wb") as destination:
            require(source.readline() == b"p cnf 34320 617936\n", "base header mismatch")
            destination.write(f"p cnf 34320 {617_936 + len(tails[name])}\n".encode())
            shutil.copyfileobj(source, destination)
            for clause in tails[name]:
                destination.write((" ".join(map(str, clause)) + " 0\n").encode())
    return outputs["blue"], outputs["red"]


def corruption_controls(certificate_path: Path, fixture_path: Path) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    rejected: list[str] = []

    def expect_rejection(name: str, function) -> None:  # type: ignore[no-untyped-def]
        try:
            function()
        except (AssertionError, KeyError, ValueError):
            rejected.append(name)
        else:
            raise AssertionError(f"malformed input accepted: {name}")

    missing = json.loads(json.dumps(certificate))
    missing["forbidden_common_blue_signatures"].pop()
    temp_missing = certificate_path.parent / ".review-control-missing.json"
    temp_missing.write_text(json.dumps(missing))
    try:
        expect_rejection("missing_signature", lambda: signature_obstructions(temp_missing))
    finally:
        temp_missing.unlink()

    wrong = json.loads(json.dumps(certificate))
    wrong["forbidden_common_blue_signatures"][0]["vertices"] = [0, 1, 2, 12, 13]
    temp_wrong = certificate_path.parent / ".review-control-wrong.json"
    temp_wrong.write_text(json.dumps(wrong))
    try:
        expect_rejection("wrong_witness", lambda: signature_obstructions(temp_wrong))
    finally:
        temp_wrong.unlink()

    order, red = read_edge_list(fixture_path)
    expect_rejection(
        "wrong_pair_color",
        lambda: require(((U, V) in red) is True, "control pair is blue"),
    )
    expect_rejection(
        "bad_fixture_order",
        lambda: require(order == 15, "control order differs"),
    )
    require(len(rejected) == 4, "not all controls rejected")
    return {"rejected": rejected}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--author-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--rebuilt-base", type=Path)
    parser.add_argument("--rebuilt-blue", type=Path)
    parser.add_argument("--rebuilt-red", type=Path)
    parser.add_argument("--build-children-dir", type=Path)
    args = parser.parse_args()
    source = args.author_dir
    certificate = source / "certificate.json"
    blue_fixture = source / "blue_pair14.edges"
    red_fixture = source / "red_pair15.edges"
    for path in (certificate, blue_fixture, red_fixture):
        require(path.is_file(), f"missing target evidence: {path}")

    report = {
        "target": {
            "artifact_ref": "bafkreiazogh6ocmkqa6v2uk25mqefnbo7mmd2472jyekl4hzbmgzhpgpnq",
            "source_commit": "74654f8988817a389becc1a25c0a382b1ab7e855",
            "input_sha256": {
                "certificate.json": sha256(certificate),
                "blue_pair14.edges": sha256(blue_fixture),
                "red_pair15.edges": sha256(red_fixture),
            },
        },
        "runtime": {
            "implementation": platform.python_implementation(),
            "python": platform.python_version(),
            "dependencies": "Python standard library only",
        },
        "core": core_structure(),
        "signatures": signature_obstructions(certificate),
        "fixtures": {
            "blue_pair14": fixture_check(blue_fixture, 14, False),
            "red_pair15": fixture_check(red_fixture, 15, True),
        },
        "clause_bridge": clause_bridge(),
        "controls": corruption_controls(certificate, blue_fixture),
        "proved_general_criterion": (
            "For disjoint red triangles C_0,...,C_{m-1}, an empty blue pair has no "
            "common uniform fixed blue neighbor whenever every pair of triangles has a "
            "blue cross-edge and the union of every m-1 triangles contains a red K4."
        ),
        "trust_boundary": (
            "Exact CPython integer, set, combination, JSON, and SHA-256 semantics; faithful "
            "decoding of the published orbit-word convention and edge-list files. The omitted "
            "24.9 MB inherited CNF and the two UNKNOWN solver traces are not checked."
        ),
    }
    if args.build_children_dir is not None:
        require(args.rebuilt_base is not None, "--build-children-dir requires --rebuilt-base")
        require(args.rebuilt_blue is None and args.rebuilt_red is None, "do not mix built and supplied children")
        args.rebuilt_blue, args.rebuilt_red = build_children_from_base(args.rebuilt_base, args.build_children_dir)
    rebuilt = (args.rebuilt_base, args.rebuilt_blue, args.rebuilt_red)
    require(all(path is not None for path in rebuilt) or all(path is None for path in rebuilt), "supply either all three rebuilt CNFs or none")
    if all(path is not None for path in rebuilt):
        report["full_formula_reproduction"] = full_formula_check(
            args.rebuilt_base, args.rebuilt_blue, args.rebuilt_red  # type: ignore[arg-type]
        )
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS: local theorem, 16 signatures, fixtures, and clause bridge")
    print(f"RESULT_SHA256={sha256(args.report)}")


if __name__ == "__main__":
    main()
