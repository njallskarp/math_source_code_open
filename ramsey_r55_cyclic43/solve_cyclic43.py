#!/usr/bin/env python3
"""Exact MaxSAT study of red-to-blue perturbations of Exoo's Cyclic(43).

Variables represent initially red edges.  A true variable means that the edge is
changed to blue.  Every possible monochromatic state contributes one unit-weight
soft clause which is violated exactly when that state occurs after the changes.
Therefore the optimum MaxSAT cost is the exact number of monochromatic K5s.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import sys
from pathlib import Path


ORDER = 43
RED_LENGTHS = frozenset({1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21})


def cyclic_distance(a: int, b: int) -> int:
    delta = (a - b) % ORDER
    return min(delta, ORDER - delta)


def edge(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def red_edge_variables() -> tuple[dict[tuple[int, int], int], list[tuple[int, int]]]:
    edges = [
        (a, b)
        for a in range(ORDER)
        for b in range(a + 1, ORDER)
        if cyclic_distance(a, b) in RED_LENGTHS
    ]
    return {e: i + 1 for i, e in enumerate(edges)}, edges


def five_set_red_variables(
    vertices: tuple[int, ...], variables: dict[tuple[int, int], int]
) -> tuple[int, ...]:
    return tuple(
        variables[edge(a, b)]
        for a, b in itertools.combinations(vertices, 2)
        if edge(a, b) in variables
    )


def build_wcnf():
    try:
        from pysat.formula import WCNF
    except ImportError as exc:  # pragma: no cover - dependency diagnostic
        raise SystemExit(
            "python-sat is required; run with `uv run --with python-sat ...`"
        ) from exc

    variables, red_edges = red_edge_variables()
    formula = WCNF()
    red_cliques = 0
    five_sets = 0

    for vertices in itertools.combinations(range(ORDER), 5):
        five_sets += 1
        red_vars = five_set_red_variables(vertices, variables)
        if len(red_vars) == 10:
            # Unsatisfied exactly when the original red K5 remains all red.
            formula.append(list(red_vars), weight=1)
            red_cliques += 1
        if len(red_vars) == 0:
            raise AssertionError(f"Cyclic(43) unexpectedly has a blue K5: {vertices}")
        # Unsatisfied exactly when every initially red edge has been flipped,
        # making all ten edges of this 5-set blue.  This is also needed for an
        # initially red K5 because all ten of its edges could be flipped.
        formula.append([-var for var in red_vars], weight=1)

    assert len(red_edges) == 473
    assert five_sets == 962_598
    assert red_cliques == 43
    assert len(formula.soft) == five_sets + red_cliques
    return formula, variables, red_edges


def verify_flips(flips: set[tuple[int, int]]) -> dict[str, object]:
    variables, _ = red_edge_variables()
    invalid = sorted(flips - set(variables))
    if invalid:
        raise ValueError(f"only initially red edges may be flipped: {invalid}")

    red_k5: list[tuple[int, ...]] = []
    blue_k5: list[tuple[int, ...]] = []
    for vertices in itertools.combinations(range(ORDER), 5):
        colors = []
        for a, b in itertools.combinations(vertices, 2):
            e = edge(a, b)
            initially_red = e in variables
            colors.append(initially_red and e not in flips)
        if all(colors):
            red_k5.append(vertices)
        elif not any(colors):
            blue_k5.append(vertices)

    return {
        "flip_count": len(flips),
        "red_k5_count": len(red_k5),
        "blue_k5_count": len(blue_k5),
        "monochromatic_k5_count": len(red_k5) + len(blue_k5),
        "red_k5": red_k5,
        "blue_k5": blue_k5,
    }


def solve(algorithm: str, solver: str, adapt: bool) -> dict[str, object]:
    try:
        import pysat
        from pysat.examples.rc2 import RC2
    except ImportError as exc:  # pragma: no cover - dependency diagnostic
        raise SystemExit(
            "python-sat is required; run with `uv run --with python-sat ...`"
        ) from exc

    formula, _, red_edges = build_wcnf()
    if algorithm == "rc2":
        with RC2(
            formula, solver=solver, adapt=adapt, exhaust=True, incr=False
        ) as optimizer:
            model = optimizer.compute()
            optimum = optimizer.cost
        algorithm_name = "RC2"
    else:
        from pysat.examples.fm import FM

        with FM(formula, solver=solver, verbose=0) as optimizer:
            success = optimizer.compute()
            if not success:
                raise AssertionError("Fu-Malik optimizer unexpectedly failed")
            model = optimizer.model
            optimum = optimizer.cost
        algorithm_name = "Fu-Malik WMSU1"
    if model is None:
        raise AssertionError("weighted formula unexpectedly has no model")

    positive = {literal for literal in model if literal > 0}
    flips = {red_edges[var - 1] for var in positive if var <= len(red_edges)}
    verification = verify_flips(flips)
    if verification["monochromatic_k5_count"] != optimum:
        raise AssertionError((optimum, verification))

    return {
        "problem": "Cyclic(43) red-to-blue perturbation minimum",
        "order": ORDER,
        "red_lengths": sorted(RED_LENGTHS),
        "algorithm": algorithm_name,
        "solver": f"PySAT backend {solver}",
        "adapt": adapt if algorithm == "rc2" else None,
        "python_sat_version": getattr(pysat, "__version__", "unknown"),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "optimum": optimum,
        "flipped_edges": sorted(flips),
        "verification": verification,
    }


def load_certificate(path: Path) -> set[tuple[int, int]]:
    payload = json.loads(path.read_text())
    return {tuple(item) for item in payload["flipped_edges"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", type=Path, metavar="CERTIFICATE_JSON")
    parser.add_argument("--output", type=Path, default=Path("certificate.json"))
    parser.add_argument("--algorithm", choices=("rc2", "fm"), default="rc2")
    parser.add_argument("--solver", default="g4", help="PySAT solver backend")
    parser.add_argument("--no-adapt", action="store_true")
    args = parser.parse_args()

    if args.verify:
        result = verify_flips(load_certificate(args.verify))
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    result = solve(args.algorithm, args.solver, not args.no_adapt)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.write_text(serialized)
    digest = hashlib.sha256(serialized.encode()).hexdigest()
    print(serialized, end="")
    print(f"certificate_sha256={digest}", file=sys.stderr)


if __name__ == "__main__":
    main()
