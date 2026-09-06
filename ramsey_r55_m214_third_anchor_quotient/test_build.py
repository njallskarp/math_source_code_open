#!/usr/bin/env python3
"""Focused semantic and corruption controls for the third-anchor quotient."""

from __future__ import annotations

import itertools
import tempfile
from pathlib import Path

import build


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    controls = 0

    for left, right, selected in itertools.product(range(2), repeat=3):
        holds = left - right - selected >= -1
        require(holds == (not selected or left >= right), "ordering guard")
        controls += 1

    for common in range(9, 14):
        maximum_h = common - 1
        for selected in range(2):
            for red_h in range(maximum_h + 1):
                lower_holds = red_h - (common - 9) * selected >= 0
                upper_holds = -red_h - (common - 5) * selected >= -maximum_h
                require(lower_holds == (not selected or red_h >= common - 9), "H lower")
                require(upper_holds == (not selected or red_h <= 4), "H upper")
                controls += 2
            for side_total in range(20):
                upper_holds = -side_total - 7 * selected >= -19
                require(upper_holds == (not selected or side_total <= 12), "pair upper")
                controls += 1

    for key in build.ROOT_KEYS:
        root = build.root_layout(key)
        require(root["pool_size"] >= 2, "third-anchor pool")
        require(sum(len(bucket["vertices"]) for bucket in root["buckets"]) == 40,
                "residual partition")
        for bucket in root["buckets"]:
            bits = [int((vertex + root["third_anchor"]) % 3 == 0)
                    for vertex in bucket["vertices"]]
            sorted_bits = sorted(bits, reverse=True)
            require(sum(bits) == sum(sorted_bits), "bucket-count transport")
            require(all(left >= right for left, right in zip(sorted_bits, sorted_bits[1:])),
                    "bucket sorting")
        controls += 1

    certificate, summary = build.certificate()
    suffix_summary, suffix = build.suffix_summary()
    require(summary["roots"] == 389 and summary["pool_min"] == 2, "summary roots")
    require(summary["orbit_rows"] == 2_206_343, "summary orbits")
    require(summary["labeled_rows"] == 5_176_895_776_352, "summary labelings")
    require(summary["suffix_sha256"] == suffix_summary["suffix_sha256"], "suffix summary")
    require(certificate.endswith(b"\n") and suffix.endswith(b"\n"), "canonical newline")
    controls += 5

    with tempfile.TemporaryDirectory(prefix="r55-third-anchor-test-") as directory:
        bad_base = Path(directory) / "bad.opb"
        output = Path(directory) / "output.opb"
        bad_base.write_bytes(b"* damaged header\n")
        try:
            build.strengthen(bad_base, output, suffix)
        except ValueError:
            pass
        else:
            raise AssertionError("damaged base accepted")
        require(not output.exists() and not output.with_name("output.opb.partial").exists(),
                "partial cleanup")
        controls += 2

    print(f"PASS semantic_and_corruption_controls={controls}")
    print("PASS all_389_third_anchor_pools_and_bucket_sorts")
    print("PASS malformed_base_header_rejected")


if __name__ == "__main__":
    main()
