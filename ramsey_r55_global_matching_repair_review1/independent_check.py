#!/usr/bin/env python3
"""Independent audit of the 21 global-matching exclusion certificates.

This checker deliberately imports no module from the reviewed contribution.  It
uses immutable graph words and matching states, verifies every proof-DAG edge,
rechecks the input graphs literally, and exercises the argument on all small
labelled graph families of orders three through five.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from itertools import combinations
from math import factorial
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def edge_data(n: int) -> tuple[list[tuple[int, int]], dict[tuple[int, int], int]]:
    pairs = list(combinations(range(n), 2))
    return pairs, {pair: i for i, pair in enumerate(pairs)}


def is_int(value: object) -> bool:
    return type(value) is int


def bad_set_count(n: int, word: int, k: int) -> list[int]:
    _, index = edge_data(n)
    counts = [0, 0]
    for vertices in combinations(range(n), k):
        colors = {(word >> index[pair]) & 1 for pair in combinations(vertices, 2)}
        if len(colors) == 1:
            counts[next(iter(colors))] += 1
    return counts


def has_bad_set(n: int, word: int, k: int) -> bool:
    _, index = edge_data(n)
    for vertices in combinations(range(n), k):
        bits = [(word >> index[pair]) & 1 for pair in combinations(vertices, 2)]
        if all(bit == bits[0] for bit in bits[1:]):
            return True
    return False


def canonical_edge_list(n: int, word: int) -> bytes:
    pairs, _ = edge_data(n)
    red = [pair for i, pair in enumerate(pairs) if (word >> i) & 1]
    text = f"{n} {len(red)}\n" + "".join(f"{u} {v}\n" for u, v in red)
    return text.encode()


def check_unsat_proof(n: int, parent_word: int, proof: object, k: int = 5) -> dict[str, int | str]:
    """Check a covering DAG using immutable graph words and edge-index states."""
    pairs, index = edge_data(n)
    limit = 1 << len(pairs)
    require(is_int(parent_word) and 0 <= parent_word < limit, "parent word range")
    require(type(proof) is dict, "proof object")
    require(proof.get("status") == "UNSAT", "certificate is not a completed exclusion")
    require(proof.get("n") == n and proof.get("k") == k, "certificate dimensions")
    require(proof.get("root") == 0, "root must be zero")
    nodes = proof.get("nodes")
    require(type(nodes) is list and nodes, "nonempty node array")

    bound_state: dict[int, tuple[int, ...]] = {}
    finished: set[int] = set()
    active: set[int] = set()
    stats = {
        "nodes": 0,
        "branches": 0,
        "leaves": 0,
        "max_depth": 0,
        "literal_pair_checks": 0,
        "shared_references": 0,
    }

    def visit(node_id: int, selected: tuple[int, ...]) -> None:
        require(is_int(node_id) and 0 <= node_id < len(nodes), "invalid node reference")
        if node_id in bound_state:
            require(bound_state[node_id] == selected, "shared node has a different matching state")
        else:
            bound_state[node_id] = selected
        if node_id in finished:
            stats["shared_references"] += 1
            return
        require(node_id not in active, "cycle in certificate")
        active.add(node_id)

        chosen_pairs = [pairs[e] for e in selected]
        endpoints = [v for pair in chosen_pairs for v in pair]
        require(len(endpoints) == len(set(endpoints)), "state is not a matching")
        used = set(endpoints)
        current_word = parent_word
        for edge in selected:
            current_word ^= 1 << edge

        node = nodes[node_id]
        require(type(node) is list and len(node) == 2, "node syntax")
        mask, children = node
        require(is_int(mask) and 0 < mask < (1 << n) and mask.bit_count() == k, "obstruction mask")
        require(type(children) is list and all(is_int(child) for child in children), "children syntax")
        vertices = [v for v in range(n) if (mask >> v) & 1]
        q_edges = list(combinations(vertices, 2))
        colors = [(current_word >> index[pair]) & 1 for pair in q_edges]
        require(colors and all(color == colors[0] for color in colors[1:]), "claimed obstruction is not monochromatic")
        available = [pair for pair in q_edges if pair[0] not in used and pair[1] not in used]
        require(len(children) == len(available), "incomplete covering branch list")

        stats["nodes"] += 1
        stats["branches"] += len(children)
        stats["literal_pair_checks"] += len(q_edges)
        stats["max_depth"] = max(stats["max_depth"], len(selected))
        if not children:
            stats["leaves"] += 1
        for pair, child in zip(available, children):
            edge = index[pair]
            require(edge not in selected, "repeated edge in state")
            visit(child, tuple(sorted(selected + (edge,))))

        active.remove(node_id)
        finished.add(node_id)

    visit(0, ())
    require(finished == set(range(len(nodes))), "unreachable certificate node")
    return {"status": "VERIFIED_COMPLETE_MATCHING_EXCLUSION", **stats}


def permute_word(n: int, word: int, permutation: list[int]) -> int:
    pairs, index = edge_data(n)
    require(sorted(permutation) == list(range(n)), "not a permutation")
    moved = 0
    for old_edge, (u, v) in enumerate(pairs):
        if (word >> old_edge) & 1:
            image = tuple(sorted((permutation[u], permutation[v])))
            moved |= 1 << index[image]
    return moved


def permute_proof(proof: dict, permutation: list[int]) -> dict:
    """Transport a certificate while independently reconstructing source states."""
    n = proof["n"]
    old_pairs, old_index = edge_data(n)
    new_nodes: list[object] = [None] * len(proof["nodes"])
    bound: dict[int, tuple[int, ...]] = {}

    def visit(node_id: int, selected: tuple[int, ...]) -> None:
        if node_id in bound:
            require(bound[node_id] == selected, "inconsistent source state during transport")
            return
        bound[node_id] = selected
        node = proof["nodes"][node_id]
        mask, children = node
        vertices = [v for v in range(n) if (mask >> v) & 1]
        used = {vertex for edge in selected for vertex in old_pairs[edge]}
        available = [pair for pair in combinations(vertices, 2) if pair[0] not in used and pair[1] not in used]
        require(len(available) == len(children), "source coverage during transport")
        mapped_children = []
        for pair, child in zip(available, children):
            edge = old_index[pair]
            visit(child, tuple(sorted(selected + (edge,))))
            image = tuple(sorted((permutation[pair[0]], permutation[pair[1]])))
            mapped_children.append((image, child))
        new_mask = sum(1 << permutation[v] for v in vertices)
        new_nodes[node_id] = [new_mask, [child for _, child in sorted(mapped_children)]]

    visit(0, ())
    require(all(node is not None for node in new_nodes), "unreachable source node during transport")
    return {"status": "UNSAT", "n": n, "k": proof["k"], "root": 0, "nodes": new_nodes}


def generate_matchings(vertices: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    if not vertices:
        return [()]
    first, rest = vertices[0], vertices[1:]
    result = generate_matchings(rest)
    for i, second in enumerate(rest):
        tail_vertices = rest[:i] + rest[i + 1 :]
        for tail in generate_matchings(tail_vertices):
            result.append(((first, second),) + tail)
    return result


def small_family_controls() -> dict[str, int]:
    """Compare literal enumeration with fresh obstruction recursion on all small graphs."""
    families = assignments = recursive_calls = 0
    for n in range(3, 6):
        pairs, index = edge_data(n)
        matchings = generate_matchings(tuple(range(n)))
        require(len(matchings) == {3: 4, 4: 10, 5: 26}[n], "small matching count")
        for k in ([3] if n < 5 else [3, 5]):
            q_sets = list(combinations(range(n), k))

            def good_by_branch(parent: int) -> bool:
                memo: dict[tuple[int, ...], bool] = {}

                def recurse(selected: tuple[int, ...]) -> bool:
                    nonlocal recursive_calls
                    recursive_calls += 1
                    if selected in memo:
                        return memo[selected]
                    current = parent
                    for edge in selected:
                        current ^= 1 << edge
                    obstruction = None
                    for q in q_sets:
                        colors = [(current >> index[pair]) & 1 for pair in combinations(q, 2)]
                        if colors and all(color == colors[0] for color in colors[1:]):
                            obstruction = q
                            break
                    if obstruction is None:
                        memo[selected] = True
                        return True
                    used = {v for edge in selected for v in pairs[edge]}
                    for pair in combinations(obstruction, 2):
                        if pair[0] not in used and pair[1] not in used:
                            edge = index[pair]
                            if recurse(tuple(sorted(selected + (edge,)))):
                                memo[selected] = True
                                return True
                    memo[selected] = False
                    return False

                return recurse(())

            for parent in range(1 << len(pairs)):
                literal = False
                for matching in matchings:
                    current = parent
                    for pair in matching:
                        current ^= 1 << index[pair]
                    literal |= not has_bad_set(n, current, k)
                    assignments += 1
                require(good_by_branch(parent) == literal, "small-family coverage mismatch")
                families += 1
    return {"small_families": families, "literal_matching_assignments": assignments, "recursive_calls": recursive_calls}


def mutation_controls(n: int, parent_word: int, proof: dict) -> int:
    """Require rejection of structurally and semantically corrupted proofs."""
    corruptions = []
    candidate = copy.deepcopy(proof)
    candidate["root"] = 1
    corruptions.append(candidate)
    candidate = copy.deepcopy(proof)
    candidate["n"] = n + 1
    corruptions.append(candidate)
    candidate = copy.deepcopy(proof)
    candidate["nodes"][0][0] = 1
    corruptions.append(candidate)
    candidate = copy.deepcopy(proof)
    candidate["nodes"][0][1].pop()
    corruptions.append(candidate)
    candidate = copy.deepcopy(proof)
    candidate["nodes"][0][1].append(0)
    corruptions.append(candidate)
    candidate = copy.deepcopy(proof)
    candidate["nodes"][0][1][0] = len(proof["nodes"])
    corruptions.append(candidate)
    candidate = copy.deepcopy(proof)
    candidate["nodes"].append(copy.deepcopy(candidate["nodes"][0]))
    corruptions.append(candidate)
    candidate = copy.deepcopy(proof)
    candidate["status"] = "UNKNOWN"
    corruptions.append(candidate)
    if len(proof["nodes"][0][1]) >= 2:
        candidate = copy.deepcopy(proof)
        candidate["nodes"][0][1][0], candidate["nodes"][0][1][1] = candidate["nodes"][0][1][1], candidate["nodes"][0][1][0]
        corruptions.append(candidate)
    for candidate in corruptions:
        try:
            check_unsat_proof(n, parent_word, candidate)
        except (ValueError, TypeError, IndexError, KeyError):
            pass
        else:
            raise RuntimeError("corrupted proof was accepted")

    root_mask = proof["nodes"][0][0]
    root_vertices = [v for v in range(n) if (root_mask >> v) & 1]
    _, index = edge_data(n)
    wrong_parent = parent_word ^ (1 << index[next(iter(combinations(root_vertices, 2)))])
    try:
        check_unsat_proof(n, wrong_parent, proof)
    except ValueError:
        pass
    else:
        raise RuntimeError("changed parent was accepted")
    return len(corruptions) + 1


def matching_counts(n: int) -> tuple[list[int], int]:
    closed = [factorial(n) // (factorial(n - 2 * k) * (1 << k) * factorial(k)) for k in range(n // 2 + 1)]
    recurrence = [1, 1]
    for size in range(2, n + 1):
        recurrence.append(recurrence[-1] + (size - 1) * recurrence[-2])
    require(sum(closed) == recurrence[n], "matching count formula/recurrence disagreement")
    return closed, recurrence[n]


def audit(source: Path) -> dict:
    parents_path = source / "parents.json"
    raw_parents = parents_path.read_bytes()
    parents = json.loads(raw_parents)
    require(parents.get("schema") == 1, "parent schema")
    require(parents.get("edge_order") == "combinations(range(43),2), bit k from least significant bit", "parent edge order")
    records = parents.get("records")
    require(type(records) is list and len(records) == 21, "expected 21 reference records")
    words = [int(record["red_edge_bits_hex"], 16) for record in records]
    require(len(set(words)) == 21, "physical parent words are not distinct")

    totals = {"nodes": 0, "branches": 0, "leaves": 0, "literal_pair_checks": 0, "shared_references": 0}
    max_depth = 0
    proof_bytes = 0
    proof_digests = []
    base_proofs = []
    reverse = list(reversed(range(43)))
    complement_mask = (1 << 903) - 1
    for i, (record, word) in enumerate(zip(records, words)):
        require(sha256(canonical_edge_list(43, word)) == record["canonical_edge_list_sha256"], f"canonical edge hash {i}")
        counts = bad_set_count(43, word, 5)
        require(counts == record["expected_blue_red_five_sets"], f"literal five-set counts {i}")
        proof_path = source / "proofs" / f"parent_{i:02}.json"
        payload = proof_path.read_bytes()
        proof = json.loads(payload)
        base_proofs.append(proof)
        facts = check_unsat_proof(43, word, proof)
        require(proof.get("discovery_nodes") == facts["nodes"], f"producer node count {i}")

        moved_word = permute_word(43, word, reverse)
        moved_proof = permute_proof(proof, reverse)
        variants = [
            (word ^ complement_mask, proof),
            (moved_word, moved_proof),
            (moved_word ^ complement_mask, moved_proof),
        ]
        for variant_word, variant_proof in variants:
            require(check_unsat_proof(43, variant_word, variant_proof) == facts, f"invariance check {i}")

        for field in totals:
            totals[field] += int(facts[field])
        max_depth = max(max_depth, int(facts["max_depth"]))
        proof_bytes += len(payload)
        proof_digests.append(sha256(payload))

    controls = small_family_controls()
    rejected_mutations = mutation_controls(43, words[0], base_proofs[0])
    by_size, per_parent = matching_counts(43)
    require(totals == {"nodes": 2155, "branches": 2138, "leaves": 934, "literal_pair_checks": 21550, "shared_references": 4}, "aggregate proof facts")
    require(max_depth == 13 and proof_bytes == 40749, "depth or certificate byte count")
    require(per_parent == 24484510749551977163109658624, "fixed-parent matching count")

    evidence = {
        "parents_sha256": sha256(raw_parents),
        "proof_set_sha256": sha256("\n".join(proof_digests).encode()),
        "references": len(records),
        "proof_checks": 4 * len(records),
        "proof_bytes": proof_bytes,
        "max_depth": max_depth,
        **totals,
        **controls,
        "rejected_mutations": rejected_mutations,
        "matchings_by_size": by_size,
        "matchings_per_fixed_parent": per_parent,
    }
    evidence_hash = sha256(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode())
    return {"status": "INDEPENDENT_CHECK_ACCEPTED", "evidence_sha256": evidence_hash, **evidence}


def main() -> None:
    require(len(sys.argv) == 2, "usage: independent_check.py SOURCE_DIRECTORY")
    result = audit(Path(sys.argv[1]))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
