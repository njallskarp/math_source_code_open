#!/usr/bin/env python3
"""Decode a CaDiCaL SAT model for an exported QLP-42 pi^4 cell."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PI3_DIRECTORY = Path(__file__).resolve().parent.parent / "qlp42_q5_q37_pi3_witnesses"
sys.path.insert(0, str(PI3_DIRECTORY))

from solve_pi3_mq import state_index  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--solver-output", type=Path, required=True)
    args = parser.parse_args()
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    lines = args.solver_output.read_text(encoding="utf-8").splitlines()
    statuses = [line for line in lines if line.startswith("s ")]
    if statuses != ["s SATISFIABLE"]:
        raise RuntimeError(f"expected one SAT status, received {statuses}")
    literals = [
        int(token)
        for line in lines
        if line.startswith("v ")
        for token in line.split()[1:]
        if token != "0"
    ]
    values: dict[int, bool] = {}
    for literal in literals:
        variable = abs(literal)
        value = literal > 0
        if variable in values and values[variable] != value:
            raise RuntimeError(f"conflicting assignment for variable {variable}")
        values[variable] = value
    native_variables = int(metadata["native_variables"])
    missing = sorted(set(range(1, native_variables + 1)) - set(values))
    if missing:
        raise RuntimeError(f"model omits native variables: {missing[:10]}")

    support = tuple(int(word, 16) for word in metadata["support"])
    words = []
    for family, family_cells in enumerate(metadata["cell_variables"]):
        word = []
        for position, variables in enumerate(family_cells):
            bits = tuple(int(values[int(variable)]) for variable in variables)
            quarter = (support[family] >> position) & 1
            word.append(state_index(bits, quarter))
        words.append("".join(format(state, "x") for state in word))
    print(
        f"{metadata['q']}\t{metadata['orbit']}\t{metadata['case']}\t"
        f"{metadata['support'][0]}\t{metadata['support'][1]}\t"
        f"{words[0]}\t{words[1]}"
    )


if __name__ == "__main__":
    main()
