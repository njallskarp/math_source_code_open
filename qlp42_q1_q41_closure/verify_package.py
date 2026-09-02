#!/usr/bin/env python3
"""Check immutable source pins and theorem-level partition arithmetic."""

from __future__ import annotations

import json
from math import comb
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> None:
    data = json.loads((HERE / "SOURCE_PINS.json").read_text())
    assert data["schema"] == "qlp42-q1-q41-closure-source-pins-v1"

    seen_ids: set[str] = set()
    for pin in data["proof_sources"]:
        assert pin["id"] not in seen_ids
        seen_ids.add(pin["id"])
        assert len(pin["commit"]) == 40
        assert len(pin["tree"]) == 40
        git("cat-file", "-e", f'{pin["commit"]}^{{commit}}')
        actual_tree = git("rev-parse", f'{pin["commit"]}:{pin["path"]}')
        assert actual_tree == pin["tree"], (pin["id"], actual_tree, pin["tree"])
        ref = pin.get("graph_artifact_ref")
        if ref is not None:
            assert ref.startswith("bafkrei") and len(ref) == 59, (pin["id"], ref)

    partitions = data["partitions"]
    assert partitions["q1_b_values"] == list(range(4, 21, 2))
    assert sum(partitions["q1_b_mask_counts"]) == 480
    assert partitions["q41_weights"] == [0, 4, 8, 12, 16, 20]
    assert partitions["q41_labeled_words"] == [comb(21, w) for w in partitions["q41_weights"]]
    assert sum(partitions["q41_labeled_words"]) == partitions["q41_correct_labeled_word_total"] == 523_776
    assert partitions["q41_legacy_mistyped_labeled_word_total"] == 524_776
    assert sum(partitions["q41_rotation_orbits"]) == 24_946
    assert sum(partitions["q41_exact_hb_assignments"]) == 2_960_716_672
    assert 5 * 7 + 13_995 * 21 == comb(21, 12) == 293_930

    pi4 = data["positive_only_pi4_context"]
    assert pi4["witnesses"] == pi4["q5_witnesses"] + pi4["q37_witnesses"] == 67
    assert pi4["negative_certificates"] == 0
    git("cat-file", "-e", f'{pi4["source_commit"]}^{{commit}}')

    print(f"source_pins_verified={len(seen_ids)}")
    print("q1_partition_verified=9_rows_480_masks")
    print("q41_partition_verified=6_weights_523776_words_24946_orbits")
    print("weight12_short_orbits_verified=5x7_plus_13995x21")
    print("pi4_scope_verified=67_positive_0_negative")
    print("package_consistency=verified")


if __name__ == "__main__":
    main()
