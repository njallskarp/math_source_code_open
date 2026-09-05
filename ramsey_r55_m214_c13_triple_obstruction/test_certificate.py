#!/usr/bin/env python3
"""Deterministic rejection controls for the triple-obstruction verifier."""

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
    with tempfile.TemporaryDirectory(prefix="r55-c13-triple-") as temporary:
        path = Path(temporary) / "bad.json"
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
    rejected("missing-common-bit", lambda data: data["footprints"].__setitem__(1, "062c"))
    rejected(
        "nonindependent-witness",
        lambda data: data["pair_blue_witnesses"][0].__setitem__(
            "independent_core_triple", [0, 1, 4]
        ),
    )
    rejected(
        "witness-meets-union",
        lambda data: data["pair_blue_witnesses"][1].__setitem__(
            "independent_core_triple", [0, 4, 10]
        ),
    )
    rejected("nonedge-common-pair", lambda data: data.__setitem__("common_red_core_edge", [10, 12]))
    rejected(
        "duplicate-outside-pair",
        lambda data: data["pair_blue_witnesses"][2].__setitem__("outside_pair", [0, 10]),
    )
    rejected("wrong-source-hash", lambda data: data.__setitem__("source_certificate_sha256", "0" * 64))
    print("ALL 6 NEGATIVE CONTROLS REJECTED")


if __name__ == "__main__":
    main()
