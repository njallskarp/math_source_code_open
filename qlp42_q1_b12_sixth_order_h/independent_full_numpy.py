#!/usr/bin/env python3
"""Direct NumPy reproduction of the full b=12 case-0/case-2 H scan."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path

DIRECT_SHA256 = "baafcf32595790a4522818e1befb033017e4e0e0743f0124e9fa06df486a4688"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_direct(directory: Path):
    path = directory / "independent_numpy.py"
    assert digest(path) == DIRECT_SHA256
    spec = importlib.util.spec_from_file_location("b12_h_direct", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def theta_for_b(module, dependency, b_word: int) -> tuple[int, ...]:
    f_word = ((~b_word) & module.WORD_MASK) & ~1
    b_signature = dependency.autocorrelation_signature(b_word)
    f_signature = dependency.autocorrelation_signature(f_word)
    theta = []
    for shift in range(1, 11):
        bit = shift - 1
        tau = (dependency.TAU_SIGNATURE >> bit) & 1
        b_corr = (b_signature >> bit) & 1
        f_corr = (f_signature >> bit) & 1
        theta.append(1 ^ tau ^ b_corr ^ f_corr)
    return tuple(theta)


def read_frontier():
    header = sys.stdin.readline().rstrip("\n")
    assert header == "a_s_word\tb_s_word\tcases"
    rows = []
    for line in sys.stdin:
        a_word, b_word, cases = map(int, line.rstrip("\n").split("\t"))
        assert cases in (1, 4, 5)
        rows.append((a_word, b_word, cases))
    assert len(rows) == 375
    assert sum(cases.bit_count() for _, _, cases in rows) == 395
    assert len({a_word for a_word, _, _ in rows}) == 345
    assert len({b_word for _, b_word, _ in rows}) == 29
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit-supports", type=int)
    parser.add_argument("--quiet", action="store_true")
    arguments = parser.parse_args()
    directory = Path(__file__).resolve().parent
    module = load_direct(directory)
    dependency = module.load_dependency(directory)
    rows = read_frontier()
    by_support = defaultdict(list)
    for row in rows:
        by_support[row[0]].append(row)

    b_fingerprints = {}
    for b_word in {row[1] for row in rows}:
        theta = theta_for_b(module, dependency, b_word)
        exact, fingerprints = module.enumerate_h_b(b_word, theta, 1)
        assert 608 <= exact <= 676
        b_fingerprints[b_word] = fingerprints

    surviving_orbits = [0] * 6
    surviving_masks = [set() for _ in range(6)]
    surviving_rows = 0
    exact_assignments = 0
    direct_paf_evaluations = 0
    fingerprint_minimum = None
    fingerprint_maximum = 0
    supports_completed = 0
    for a_word, support_rows in sorted(by_support.items()):
        if (
            arguments.limit_supports is not None
            and supports_completed >= arguments.limit_supports
        ):
            break
        a_support = tuple(
            position for position in range(module.N) if (a_word >> position) & 1
        )
        exact, evaluations, needed = module.enumerate_h_a_needed(a_support)
        assert exact == 853_776
        exact_assignments += exact
        direct_paf_evaluations += evaluations
        fingerprint_minimum = (
            len(needed)
            if fingerprint_minimum is None
            else min(fingerprint_minimum, len(needed))
        )
        fingerprint_maximum = max(fingerprint_maximum, len(needed))
        for _, b_word, cases in support_rows:
            feasible = any(
                fingerprint in needed for fingerprint in b_fingerprints[b_word]
            )
            if not feasible:
                continue
            surviving_rows += 1
            for case_number in (0, 2):
                if (cases >> case_number) & 1:
                    surviving_orbits[case_number] += 1
                    surviving_masks[case_number].add(b_word)
        supports_completed += 1
        if not arguments.quiet:
            print(
                f"completed_a_support={supports_completed}/{len(by_support)};"
                f"surviving_rows={surviving_rows}",
                flush=True,
            )

    print("input_case02_orbit_incidences=395")
    print("input_case02_rows=375")
    print("input_unique_a_supports=345")
    print("input_unique_b_masks=29")
    print(f"supports_completed={supports_completed}")
    print(f"sixth_h_surviving_case0_orbits={surviving_orbits[0]}")
    print(f"sixth_h_surviving_case2_orbits={surviving_orbits[2]}")
    print(f"sixth_h_surviving_case0_masks={len(surviving_masks[0])}")
    print(f"sixth_h_surviving_case2_masks={len(surviving_masks[2])}")
    print(f"sixth_h_surviving_rows={surviving_rows}")
    print(f"h_a_fingerprint_range={fingerprint_minimum}-{fingerprint_maximum}")
    print(f"h_a_exact_assignments={exact_assignments}")
    print(f"h_a_direct_paf_evaluations={direct_paf_evaluations}")
    if arguments.limit_supports is None:
        assert supports_completed == 345
        assert exact_assignments == 345 * 853_776
        print("independent_full_numpy_certificate=verified")
    else:
        print("independent_partial_numpy_certificate=verified")


if __name__ == "__main__":
    main()
