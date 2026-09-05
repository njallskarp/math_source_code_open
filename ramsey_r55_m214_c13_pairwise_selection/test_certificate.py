#!/usr/bin/env python3
"""Deterministic rejection tests for the pairwise-selection checker."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = json.loads((ROOT / "certificate.json").read_text())


def rejected(name: str, transform) -> None:
    candidate = copy.deepcopy(BASE)
    transform(candidate)
    with tempfile.TemporaryDirectory(prefix="r55-pairwise-selection-") as temporary:
        path = Path(temporary) / "bad.json"
        path.write_text(json.dumps(candidate))
        result = subprocess.run(
            [sys.executable, str(ROOT / "check_certificate.py"), str(path)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    if result.returncode == 0:
        raise AssertionError(name)
    print(f"REJECTED {name}")


def main() -> None:
    rejected("nontransversal", lambda data: data["footprints"].__setitem__(0, "0000"))
    rejected("wrong-column", lambda data: data["footprints"].__setitem__(0, "1127"))
    rejected("wrong-mark", lambda data: data["outside_e"].__setitem__(0, 6))
    rejected("edge-capacity", lambda data: data.__setitem__("m_o", 4))
    rejected("wrong-pivot", lambda data: data.__setitem__("pivot", "C0"))
    print("ALL 5 NEGATIVE CONTROLS REJECTED")


if __name__ == "__main__":
    main()
