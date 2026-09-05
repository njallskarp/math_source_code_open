#!/usr/bin/env python3
"""Search an exact M=216 aggregate witness avoiding the height-2715 signature cut."""

from argparse import ArgumentParser
from itertools import combinations, permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
import aggregate_search as base
import search_pointwise_lift as pointwise


TEMPLATE_EDGES = {
    (0, 1), (0, 2), (0, 3), (0, 6), (1, 4), (1, 5), (1, 6),
    (2, 3), (2, 4), (2, 5), (3, 6), (4, 5),
}
TEMPLATE_THRESHOLDS = {49: 1, 50: 2, 60: 1, 73: 2, 116: 2, 120: 3}


def core_edges(mask):
    return {
        pair for index, pair in enumerate(combinations(range(7), 2)) if mask >> index & 1
    }


def transform_mask(mask, permutation):
    return sum(1 << permutation[vertex] for vertex in range(7) if mask >> vertex & 1)


def template_embeddings(mask):
    target = core_edges(mask)
    answer = []
    for permutation in permutations(range(7)):
        image = {tuple(sorted((permutation[left], permutation[right]))) for left, right in TEMPLATE_EDGES}
        if image == target:
            answer.append(permutation)
    return tuple(answer)


def passes_signature_cut(mask, cells):
    values = dict(cells)
    embeddings = template_embeddings(mask)
    violations = []
    for permutation in embeddings:
        if all(values.get(transform_mask(signature, permutation), 0) >= threshold
               for signature, threshold in TEMPLATE_THRESHOLDS.items()):
            violations.append(permutation)
    return not violations, embeddings, tuple(violations)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--core-attempts", type=int, default=100)
    parser.add_argument("--cell-attempts", type=int, default=100)
    parser.add_argument("--edge-time-limit", type=float, default=10)
    parser.add_argument("--pointwise-time-limit", type=float, default=10)
    args = parser.parse_args()
    excluded = []
    seen = set()
    cell_trials = edge_trials = 0
    for core_attempt in range(args.core_attempts):
        seed = 17000023 + base.M * 100003 + core_attempt * 7919
        core = base.solve_core(excluded, seed)
        if core is None:
            break
        excluded.append(core)
        adjacency = base.adjacency(core)
        for cell_attempt in range(args.cell_attempts):
            candidate = base.solve_cells(adjacency, seed + 104729 * (cell_attempt + 1))
            if candidate is None:
                break
            key = tuple(tuple(pair) for pair in candidate["cells"])
            if (core, key) in seen:
                continue
            seen.add((core, key))
            cell_trials += 1
            passes, embeddings, violations = passes_signature_cut(core, candidate["cells"])
            if not passes:
                print(
                    f"cell={cell_trials} core={core} embeddings={len(embeddings)} "
                    f"template_violations={len(violations)}",
                    flush=True,
                )
                continue
            record = {
                "counts_18_to_24": "0,2,5,36,0,0,0",
                "M": base.M,
                "split_count": 3,
                "exceptional_degrees": list(base.DEGREES),
                "core_mask": core,
                **candidate,
            }
            edge_trials += 1
            lifted = base.lift(record, args.edge_time_limit)
            print(
                f"cell={cell_trials} edge={edge_trials} core={core} "
                f"embeddings={len(embeddings)} side={candidate['maximum_exceptional_root_side']} "
                f"lifted={lifted is not None}",
                flush=True,
            )
            if lifted is None:
                continue
            pairs, values, row_count = lifted
            output = {
                "format": "r55-m216-height2715-cut-survivor-v1",
                "record": record,
                "aggregate_edges": [
                    [left, right, value]
                    for (left, right), value in zip(pairs, values) if value
                ],
                "edge_variables": len(pairs),
                "generated_two_sided_rows": row_count,
                "template_embeddings": [list(permutation) for permutation in embeddings],
                "template_violations": 0,
                "cell_trials": cell_trials,
                "edge_trials": edge_trials,
            }
            pointwise_result = pointwise.solve(output, args.pointwise_time_limit)
            print(f"pointwise={pointwise_result is not None}", flush=True)
            if pointwise_result is None:
                continue
            labels, central_pairs, central_values, pointwise_rows, lifted_counts = pointwise_result
            output.update({
                "format": "r55-m216-height2715-cut-pointwise-survivor-v1",
                "central_labels": labels,
                "central_red_edges": [
                    [left, right] for (left, right), value in zip(central_pairs, central_values) if value
                ],
                "binary_variables": len(central_pairs),
                "pointwise_rows": pointwise_rows,
                "pointwise_lifted_counts": lifted_counts,
            })
            args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
            print(f"FOUND core={core} after {cell_trials} cell and {edge_trials} edge trials")
            return
    raise SystemExit(
        f"NO SURVIVOR after {cell_trials} cell and {edge_trials} edge trials over {len(excluded)} cores"
    )


if __name__ == "__main__":
    main()
