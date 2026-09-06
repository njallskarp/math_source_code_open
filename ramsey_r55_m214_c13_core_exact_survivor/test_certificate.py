#!/usr/bin/env python3
"""Deterministic malformed-certificate controls for verify.py."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = json.loads((ROOT / "certificate.json").read_text(encoding="ascii"))


def rejected(name: str, transform) -> None:
    candidate = copy.deepcopy(BASE)
    transform(candidate)
    with tempfile.TemporaryDirectory(prefix="r55-c13-core-exact-") as temporary:
        path = Path(temporary) / "candidate.json"
        path.write_text(json.dumps(candidate), encoding="ascii")
        result = subprocess.run(
            [sys.executable, str(ROOT / "verify.py"), str(path)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    if result.returncode == 0:
        raise AssertionError(name)
    print(f"REJECTED {name}")


def main() -> None:
    rejected("footprint-bit", lambda data: data["footprints"].__setitem__(0, "1c49"))
    rejected(
        "outside-edge-bit",
        lambda data: data.__setitem__(
            "outside_red_bits", f"{int(data['outside_red_bits'], 16) ^ 1:095x}"
        ),
    )
    rejected(
        "mark-move",
        lambda data: (
            data.__setitem__("core_e", [0]),
            data["outside_e"].pop(),
        ),
    )
    rejected("pivot", lambda data: data.__setitem__("pivot", "D1"))
    rejected(
        "truncated-bits",
        lambda data: data.__setitem__("outside_red_bits", data["outside_red_bits"][1:]),
    )
    print("ALL 5 NEGATIVE CONTROLS REJECTED")


if __name__ == "__main__":
    main()
