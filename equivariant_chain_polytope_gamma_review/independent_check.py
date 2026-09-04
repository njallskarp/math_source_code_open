#!/usr/bin/env python3
"""Independent audit of equivariant chain-polytope transfer and target provenance.

The finite checks corroborate, but do not prove, the universal theorem.  The
universal proof uses Stanley's transfer theorem, the elementary equivariance
calculation, and D'Ali--Higashitani's Theorem 4.5.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


TARGET_COMMIT = "c28570c96f9aa413711d24ccf4bd53c15caa0e93"
TARGET_DIR = "equivariant_chain_polytope_gamma"
ACTUAL_TREE_HASHES = {
    "EXPECTED_OUTPUT.txt": "9a0b3851874316ff9f0edb60095dc5fff8e11826e7bea5930e17dff077673f49",
    "README.md": "e64346dea8d73ab476632d6dfa3e0032ba70ba339b37a4c2046aca153bcf1ff3",
    "SHA256SUMS": "8fa7d4d60712582ff6ea305849bd061b267055243faf2ca8fe4296cece099967",
    "test_verify.py": "a00cadbe6e5ae360d5ce7a16ba199d5c93355e205c2b5ed672c9a7ae57e3b26f",
    "verify.py": "2692a4ce2daf10638c98322ff6e6e322dc441dce4c72cfc000f558752afb0d0f",
}
TARGET_SUMMARY = (
    "VERIFIED equivariant transfer and gamma characters; structural_cases=132; "
    "graded_cases=44; nonuniform_graded_cases=24; named_cases=5; "
    "group_elements=13; transfer_checks=9176; "
    "sha256=ef1f4fd1fce50f6b028f53a6ab157bdcd6a30c0ce6cb8d60b7066ab9002cf53f"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def target_blob(repo: Path, name: str) -> bytes:
    return git(repo, "show", f"{TARGET_COMMIT}:{TARGET_DIR}/{name}")


def audit_target_provenance(repo: Path) -> dict[str, object]:
    git(repo, "cat-file", "-e", f"{TARGET_COMMIT}^{{commit}}")
    names = tuple(
        line.removeprefix(f"{TARGET_DIR}/")
        for line in git(
            repo,
            "ls-tree",
            "-r",
            "--name-only",
            TARGET_COMMIT,
            "--",
            TARGET_DIR,
        ).decode().splitlines()
    )
    if set(names) != set(ACTUAL_TREE_HASHES):
        raise AssertionError((names, tuple(ACTUAL_TREE_HASHES)))

    blobs = {name: target_blob(repo, name) for name in names}
    actual_hashes = {name: sha256(data) for name, data in blobs.items()}
    if actual_hashes != ACTUAL_TREE_HASHES:
        raise AssertionError(actual_hashes)
    manifest_entries = tuple(
        line for line in blobs["SHA256SUMS"].decode().splitlines() if line.strip()
    )
    test_tree = ast.parse(blobs["test_verify.py"])
    tests = tuple(
        node.name
        for node in ast.walk(test_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    )
    if len(manifest_entries) != 4 or len(tests) != 4:
        raise AssertionError((len(manifest_entries), len(tests)))

    with tempfile.TemporaryDirectory(prefix="equivariant-target-") as raw_tmp:
        tmp = Path(raw_tmp)
        for name, data in blobs.items():
            (tmp / name).write_bytes(data)
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        run = subprocess.run(
            [sys.executable, "verify.py"],
            cwd=tmp,
            env=env,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    lines = run.stdout.splitlines()
    if not lines or lines[0] != TARGET_SUMMARY:
        raise AssertionError(run.stdout)

    return {
        "target_commit": TARGET_COMMIT,
        "tree_files": len(names),
        "manifest_entries": len(manifest_entries),
        "test_methods": len(tests),
        "provenance_errors": 0,
        "tree_sha256": sha256(
            json.dumps(actual_hashes, sort_keys=True, separators=(",", ":")).encode()
        ),
        "target_stdout_sha256": sha256(run.stdout.encode()),
    }


Relation = frozenset[tuple[int, int]]
Permutation = tuple[int, ...]


def transitive(relation: Relation) -> bool:
    return all((i, k) in relation for i, j in relation for j2, k in relation if j == j2)


def natural_posets(n: int):
    pairs = tuple(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        relation = frozenset(pair for bit, pair in enumerate(pairs) if mask & (1 << bit))
        if transitive(relation):
            yield relation


def covers(relation: Relation) -> Relation:
    return frozenset(
        (i, j)
        for i, j in relation
        if not any((i, k) in relation and (k, j) in relation for k in range(j))
    )


def automorphisms(n: int, relation: Relation) -> tuple[Permutation, ...]:
    return tuple(
        p
        for p in itertools.permutations(range(n))
        if frozenset((p[i], p[j]) for i, j in relation) == relation
    )


def act(vector: tuple[int, ...], permutation: Permutation) -> tuple[int, ...]:
    image = [0] * len(vector)
    for old, new in enumerate(permutation):
        image[new] = vector[old]
    return tuple(image)


def is_chain(indices: tuple[int, ...], relation: Relation) -> bool:
    return all((i, j) in relation or (j, i) in relation for i, j in itertools.combinations(indices, 2))


def chain_subsets(n: int, relation: Relation) -> tuple[tuple[int, ...], ...]:
    return tuple(
        subset
        for size in range(1, n + 1)
        for subset in itertools.combinations(range(n), size)
        if is_chain(subset, relation)
    )


def transfer(point: tuple[int, ...], cover_relation: Relation) -> tuple[int, ...]:
    return tuple(
        point[i] - max((point[j] for j, k in cover_relation if k == i), default=0)
        for i in range(len(point))
    )


def inverse_transfer(point: tuple[int, ...], cover_relation: Relation) -> tuple[int, ...]:
    result: list[int] = []
    for i, value in enumerate(point):
        result.append(value + max((result[j] for j, k in cover_relation if k == i), default=0))
    return tuple(result)


def audit_transfer() -> dict[str, object]:
    rows: list[object] = []
    posets = actions = order_points = transfer_checks = complement_checks = 0
    for n in range(1, 5):
        for relation in natural_posets(n):
            posets += 1
            cover_relation = covers(relation)
            chains = chain_subsets(n, relation)
            group = automorphisms(n, relation)
            actions += len(group)
            for dilation in range(4):
                universe = tuple(itertools.product(range(dilation + 1), repeat=n))
                order = tuple(
                    z for z in universe if all(z[i] <= z[j] for i, j in relation)
                )
                chain = {
                    z for z in universe if all(sum(z[i] for i in c) <= dilation for c in chains)
                }
                image = {transfer(z, cover_relation) for z in order}
                if image != chain:
                    raise AssertionError((n, relation, dilation, image ^ chain))
                order_points += len(order)
                for z in order:
                    if inverse_transfer(transfer(z, cover_relation), cover_relation) != z:
                        raise AssertionError("inverse transfer failure")
                    opposite = tuple(dilation - value for value in z)
                    if not all(opposite[i] >= opposite[j] for i, j in relation):
                        raise AssertionError("opposite-convention complement failure")
                    for g in group:
                        if transfer(act(z, g), cover_relation) != act(transfer(z, cover_relation), g):
                            raise AssertionError("transfer equivariance failure")
                        if act(opposite, g) != tuple(dilation - value for value in act(z, g)):
                            raise AssertionError("complement equivariance failure")
                        transfer_checks += 1
                        complement_checks += 1
                rows.append((n, sorted(relation), dilation, len(order), len(group)))
    return {
        "natural_posets": posets,
        "automorphism_actions": actions,
        "order_points": order_points,
        "transfer_equivariance_checks": transfer_checks,
        "convention_complement_checks": complement_checks,
        "row_sha256": sha256(json.dumps(rows, separators=(",", ":")).encode()),
    }


def no_isolates(nx: int, ny: int, edges: Relation) -> bool:
    return {v for edge in edges for v in edge} == set(range(nx + ny))


def blowup_relation(nx: int, sizes: tuple[int, ...], edges: Relation):
    offsets = tuple(itertools.accumulate((0,) + sizes))
    elements = tuple((v, j) for v, size in enumerate(sizes) for j in range(size))
    relation = frozenset(
        (offsets[v] + i, offsets[w] + j)
        for v, i in elements
        for w, j in elements
        if (v == w and i < j) or (v < nx <= w and (v, w) in edges)
    )
    return elements, relation


def audit_blowups() -> dict[str, object]:
    rows: list[object] = []
    cases = graded = nonuniform_graded = subset_checks = 0
    for nx in (1, 2):
        for ny in (1, 2):
            possible = tuple((x, nx + y) for x in range(nx) for y in range(ny))
            for mask in range(1, 1 << len(possible)):
                edges = frozenset(e for bit, e in enumerate(possible) if mask & (1 << bit))
                if not no_isolates(nx, ny, edges):
                    continue
                for sizes in itertools.product((1, 2), repeat=nx + ny):
                    cases += 1
                    elements, relation = blowup_relation(nx, sizes, edges)
                    n = len(elements)
                    comparable = frozenset(
                        frozenset((i, j)) for i, j in relation
                    )
                    offsets = tuple(itertools.accumulate((0,) + sizes))
                    graph_edges = frozenset(
                        frozenset((i, j))
                        for i, j in itertools.combinations(range(n), 2)
                        if (
                            elements[i][0] == elements[j][0]
                            or (min(elements[i][0], elements[j][0]), max(elements[i][0], elements[j][0])) in edges
                        )
                    )
                    if comparable != graph_edges:
                        raise AssertionError("comparability graph mismatch")
                    maximal_expected = {
                        frozenset(range(offsets[x], offsets[x + 1]))
                        | frozenset(range(offsets[y], offsets[y + 1]))
                        for x, y in edges
                    }
                    all_chains = {
                        frozenset(c) for c in chain_subsets(n, relation)
                    }
                    maximal_actual = {
                        c for c in all_chains if not any(c < d for d in all_chains)
                    }
                    subset_checks += len(all_chains)
                    if maximal_actual != maximal_expected:
                        raise AssertionError("maximal-chain classification mismatch")
                    edge_sums = {sizes[x] + sizes[y] for x, y in edges}
                    is_graded = len({len(c) for c in maximal_actual}) == 1
                    if is_graded != (len(edge_sums) == 1):
                        raise AssertionError("constant-edge-sum criterion mismatch")
                    if is_graded:
                        graded += 1
                        nonuniform_graded += len(set(sizes)) > 1
                        c = next(iter(edge_sums))
                        if n - c < 0:
                            raise AssertionError("negative claimed h-star degree")
                    rows.append((nx, ny, sorted(edges), sizes, is_graded, sorted(map(len, maximal_actual))))
    return {
        "blowup_cases": cases,
        "graded_cases": graded,
        "nonuniform_graded_cases": nonuniform_graded,
        "chain_subset_checks": subset_checks,
        "row_sha256": sha256(json.dumps(rows, separators=(",", ":")).encode()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-repo", type=Path, required=True)
    args = parser.parse_args()
    provenance = audit_target_provenance(args.target_repo.resolve())
    transfer_report = audit_transfer()
    blowup_report = audit_blowups()
    report = {
        "provenance": provenance,
        "transfer": transfer_report,
        "blowups": blowup_report,
    }
    digest = sha256(json.dumps(report, sort_keys=True, separators=(",", ":")).encode())
    print(
        "INDEPENDENT AUDIT PASSED; "
        f"posets={transfer_report['natural_posets']}; "
        f"transfer_checks={transfer_report['transfer_equivariance_checks']}; "
        f"blowup_cases={blowup_report['blowup_cases']}; "
        f"provenance_errors={provenance['provenance_errors']}; sha256={digest}"
    )
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
