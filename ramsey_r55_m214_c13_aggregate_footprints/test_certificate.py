#!/usr/bin/env python3
"""Positive and deterministic negative controls for check_certificate.py."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_certificate.py"
CERTIFICATE = HERE / "certificate.json"


def run(data: dict[str, object]) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix="r55-c13-aggregate-test-") as temporary:
        path = Path(temporary) / "certificate.json"
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="ascii")
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(CHECKER), str(path)],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )


def main() -> None:
    original = json.loads(CERTIFICATE.read_text(encoding="ascii"))
    positive = run(original)
    if positive.returncode != 0 or "VERIFIED AGGREGATE COUNTEREXAMPLE" not in positive.stdout:
        raise AssertionError((positive.returncode, positive.stdout, positive.stderr))

    mutations = []
    bad_mask = copy.deepcopy(original)
    bad_mask["rows"][0]["mask"] = "0000"
    mutations.append(("nontransversal", bad_mask))

    bad_count = copy.deepcopy(original)
    bad_count["rows"][0]["count"] = 2
    mutations.append(("row_count", bad_count))

    bad_edge = copy.deepcopy(original)
    bad_edge["edge_counts"]["m_A"] = 15
    mutations.append(("anchor_equation", bad_edge))

    bad_mark = copy.deepcopy(original)
    bad_mark["core_e"] = [0]
    bad_mark["k"] = 1
    mutations.append(("mark_columns", bad_mark))

    bad_pivot = copy.deepcopy(original)
    bad_pivot["outside_pivot"] = False
    mutations.append(("pivot", bad_pivot))

    for name, mutation in mutations:
        result = run(mutation)
        if result.returncode == 0:
            raise AssertionError((name, result.stdout))

    print("PASS positive=1 rejected_mutations=5")


if __name__ == "__main__":
    main()
