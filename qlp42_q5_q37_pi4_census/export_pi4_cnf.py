#!/usr/bin/env python3
"""Export one exact QLP-42 pi^4 cell as deterministic pure DIMACS CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent
PI3_DIRECTORY = DIRECTORY.parent / "qlp42_q5_q37_pi3_witnesses"
sys.path[:0] = [str(DIRECTORY), str(PI3_DIRECTORY)]

import solve_pi3_mq  # noqa: E402
import solve_pi4_mq  # noqa: E402
from export_pi3_cnf import (  # noqa: E402
    Recorder,
    check_xor_gate,
    expand_xors,
    write_dimacs,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("q", type=int, choices=(5, 37))
    parser.add_argument("orbit", type=int, choices=range(18))
    parser.add_argument("case", type=int, choices=range(6))
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    check_xor_gate()

    recorder = Recorder()
    original_solver = solve_pi3_mq.Solver
    solve_pi3_mq.Solver = lambda threads=1: recorder  # type: ignore[assignment]
    try:
        encoding, cells, support = solve_pi4_mq.encode_problem(
            args.q, args.orbit, args.case
        )
    finally:
        solve_pi3_mq.Solver = original_solver
    assert encoding.solver is recorder
    variables, clauses = expand_xors(
        encoding.variables, recorder.clauses, recorder.xors
    )
    cnf_sha256 = write_dimacs(args.cnf, variables, clauses)
    metadata = {
        "q": args.q,
        "orbit": args.orbit,
        "case": args.case,
        "support": [f"{support[0]:06x}", f"{support[1]:06x}"],
        "cell_variables": cells,
        "native_variables": encoding.variables,
        "native_clauses": len(recorder.clauses),
        "native_xors": len(recorder.xors),
        "cnf_variables": variables,
        "cnf_clauses": len(clauses),
        "cnf_sha256": cnf_sha256,
        "generator_sha256": sha256(Path(__file__)),
        "pi4_encoder_sha256": sha256(DIRECTORY / "solve_pi4_mq.py"),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"q={args.q};orbit={args.orbit};case={args.case};"
        f"native_variables={encoding.variables};"
        f"native_clauses={len(recorder.clauses)};"
        f"native_xors={len(recorder.xors)};"
        f"cnf_variables={variables};cnf_clauses={len(clauses)};"
        f"cnf_sha256={cnf_sha256}"
    )


if __name__ == "__main__":
    main()
