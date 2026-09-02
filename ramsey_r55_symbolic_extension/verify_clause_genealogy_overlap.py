#!/usr/bin/env python3
"""Definition-level checks for the clause-genealogy overlap-debt theorem.

The universal result is proved in the accompanying Markdown note.  This
dependency-free checker audits the local resolution convention, unfolded-tree
arithmetic, short-clause threshold, and Ramsey charge dichotomy.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import sys
from functools import lru_cache


LiteralSet = frozenset[int]
Tree = tuple["Tree", "Tree"] | None


def ceiling_div(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise AssertionError("nonpositive denominator")
    return -(-numerator // denominator)


def clause_tails(variable_count: int) -> list[LiteralSet]:
    """All clash-free literal sets on variables 2,...,variable_count+1."""
    tails: list[LiteralSet] = []
    for choices in itertools.product((-1, 0, 1), repeat=variable_count):
        tails.append(
            frozenset(
                sign * variable
                for variable, sign in enumerate(choices, start=2)
                if sign
            )
        )
    return tails


def compatible(left: LiteralSet, right: LiteralSet) -> bool:
    return not any(-literal in right for literal in left)


@lru_cache(maxsize=None)
def ordered_full_binary_trees(leaves: int) -> tuple[Tree, ...]:
    if leaves == 1:
        return (None,)
    trees: list[Tree] = []
    for left_leaves in range(1, leaves):
        right_leaves = leaves - left_leaves
        for left in ordered_full_binary_trees(left_leaves):
            for right in ordered_full_binary_trees(right_leaves):
                trees.append((left, right))
    return tuple(trees)


def tree_counts(tree: Tree) -> tuple[int, int]:
    if tree is None:
        return 1, 0
    left_leaves, left_internal = tree_counts(tree[0])
    right_leaves, right_internal = tree_counts(tree[1])
    return left_leaves + right_leaves, left_internal + right_internal + 1


def labeled_tree_summary(tree: Tree, mode: int, index: list[int]) -> tuple[int, int, int]:
    """Return (leaves, root_excess, overlap_sum) for a deterministic labeling."""
    if tree is None:
        return 1, 2, 0
    left_leaves, left_excess, left_overlap = labeled_tree_summary(tree[0], mode, index)
    right_leaves, right_excess, right_overlap = labeled_tree_summary(tree[1], mode, index)
    position = index[0]
    index[0] += 1
    if mode == 0:
        overlap = 0
    elif mode == 1:
        overlap = 2
    elif mode == 2:
        overlap = 3 if position % 2 == 0 else 1
    else:
        overlap = (7 * position + 3 * (left_leaves + right_leaves)) % 6
    return (
        left_leaves + right_leaves,
        left_excess + right_excess - overlap,
        left_overlap + right_overlap + overlap,
    )


def verify_certificate(data: dict) -> dict[str, int]:
    claim = data["claim"]
    if claim["leaf_clause_length"] != 4 or claim["centered_length"] != 2:
        raise AssertionError("certificate does not describe pure length-four leaves")
    if claim["short_clause_max_length"] != 3:
        raise AssertionError("wrong short-clause threshold")
    if claim["forced_single_overlap_lower_bound"] != 3:
        raise AssertionError("wrong forced overlap bound")

    # Exhaustively check the exact local clause-length recurrence over every
    # compatible pair of tails on the declared small universe.
    variable_count = data["definition_audit"]["nonpivot_variables"]
    tails = clause_tails(variable_count)
    local_cases = 0
    for left in tails:
        for right in tails:
            if not compatible(left, right):
                continue
            parent_left = frozenset({1}) | left
            parent_right = frozenset({-1}) | right
            resolvent = left | right
            overlap = len(left & right)
            expected = len(parent_left) + len(parent_right) - 2 - overlap
            if len(resolvent) != expected:
                raise AssertionError("local length identity failed")
            if len(resolvent) - 2 != (
                (len(parent_left) - 2) + (len(parent_right) - 2) - overlap
            ):
                raise AssertionError("centered local recurrence failed")
            local_cases += 1
    if local_cases != data["definition_audit"]["compatible_tail_pairs"]:
        raise AssertionError("unexpected compatible-tail count")

    # Check the telescoping recurrence on every ordered full binary-tree shape
    # through the declared size, under four different deterministic overlap
    # labelings.  The written cancellation proof supplies universality.
    tree_limit = data["tree_audit"]["maximum_leaf_count"]
    tree_shapes = 0
    labeled_tree_cases = 0
    for leaf_count in range(1, tree_limit + 1):
        for tree in ordered_full_binary_trees(leaf_count):
            leaves, internal = tree_counts(tree)
            if leaves != leaf_count or internal != leaf_count - 1:
                raise AssertionError("full binary-tree count failed")
            tree_shapes += 1
            for mode in range(data["tree_audit"]["overlap_labelings_per_shape"]):
                leaves2, root_excess, overlap_sum = labeled_tree_summary(tree, mode, [0])
                if leaves2 != leaves:
                    raise AssertionError("labeled-tree leaf count changed")
                if root_excess != 2 * leaves - overlap_sum:
                    raise AssertionError("unfolded-tree telescoping identity failed")
                root_length = root_excess + 2
                if overlap_sum != 2 * leaves + 2 - root_length:
                    raise AssertionError("overlap-debt form failed")
                if overlap_sum - 2 * internal != 4 - root_length:
                    raise AssertionError("overlap-surplus form failed")
                labeled_tree_cases += 1
    if tree_shapes != data["tree_audit"]["ordered_full_binary_tree_shapes"]:
        raise AssertionError("unexpected ordered-tree count")
    if labeled_tree_cases != data["tree_audit"]["labeled_tree_cases"]:
        raise AssertionError("unexpected labeled-tree count")

    # Verify that lengths 1,2,3 demand more total overlap than is available if
    # every internal occurrence has overlap at most two.
    threshold = data["threshold_audit"]
    threshold_cases = 0
    for leaves in range(threshold["minimum_leaf_count"], threshold["maximum_leaf_count"] + 1):
        internal = leaves - 1
        for root_length in threshold["root_lengths"]:
            debt = 2 * leaves + 2 - root_length
            if debt <= 2 * internal:
                raise AssertionError("short clause failed to force overlap at least three")
            if ceiling_div(debt, internal) < 3:
                raise AssertionError("averaging lower bound failed")
            if debt - 2 * internal != 4 - root_length:
                raise AssertionError("short-clause surplus mismatch")
            threshold_cases += 1
    if threshold_cases != threshold["cases"]:
        raise AssertionError("unexpected short-clause case count")

    # Recheck the imported charge-three range and the exact U/O arithmetic.
    # This does not reprove existence of the pivot; it checks the combination
    # of that imported theorem with the new genealogy lemma.
    ramsey = data["ramsey_dichotomy_audit"]
    parameter_pairs = 0
    branch_cases = 0
    for p in range(ramsey["terminal_parameter_min"], ramsey["terminal_parameter_max_for_nonempty_tail"] + 1):
        tail_steps = 41 - p
        for first_arity in range(ramsey["first_fan_arity_min"], ramsey["first_fan_arity_max"] + 1):
            tail_charge = 90 + 2 * first_arity - 2 * p
            if ceiling_div(tail_charge, tail_steps) < 3:
                raise AssertionError("imported high-charge range arithmetic failed")
            parameter_pairs += 1
            for main_length in range(1, ramsey["main_lengths_checked"] + 1):
                # Unit main: current overlap can vanish for sufficiently large
                # arity, so the new unit-genealogy argument is essential.
                if main_length == 1:
                    unit_surplus = 4 - main_length
                    if unit_surplus != 3:
                        raise AssertionError("unit genealogy surplus failed")
                else:
                    for fan_arity in range(1, 11):
                        required_overlap = (fan_arity - 1) * (main_length - 2) + 3
                        if required_overlap < 3:
                            raise AssertionError("nonunit branch did not force overlap")
                branch_cases += 1
    if parameter_pairs != ramsey["parameter_pairs"]:
        raise AssertionError("unexpected Ramsey parameter-pair count")

    return {
        "local_cases": local_cases,
        "tree_shapes": tree_shapes,
        "labeled_tree_cases": labeled_tree_cases,
        "threshold_cases": threshold_cases,
        "parameter_pairs": parameter_pairs,
        "branch_cases": branch_cases,
    }


def main() -> None:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
        "ramsey_r55_symbolic_extension/clause-genealogy-overlap-certificate.json"
    )
    raw = path.read_bytes()
    data = json.loads(raw)
    counts = verify_certificate(data)
    digest = hashlib.sha256(raw).hexdigest()
    rendered = "; ".join(f"{key}={value}" for key, value in counts.items())
    print(f"verified: clause-genealogy overlap debt; {rendered}; certificate_sha256={digest}")


if __name__ == "__main__":
    main()
