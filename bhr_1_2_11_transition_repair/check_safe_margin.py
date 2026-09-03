#!/usr/bin/env python3
"""Exhaustive small-order regression check for the safe-margin lemma."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json

from audit_source_certificate import transported_cut
from verify import cyclic_length, grow_once, growth_cuts, verify_growth


def check(max_order: int) -> dict[str, object]:
    if not 4 <= max_order <= 10:
        raise ValueError("max-order must lie between 4 and 10")
    path_counts: dict[int, int] = {}
    obligation_counts: dict[int, int] = {}
    record_hash = hashlib.sha256()
    for order in range(4, max_order + 1):
        paths = obligations = 0
        for tail in itertools.permutations(range(1, order)):
            path = (0,) + tail
            paths += 1
            maximum = max(
                cyclic_length(u, v, order) for u, v in zip(path, path[1:])
            )
            cuts = {
                mode: growth_cuts(path, mode)
                for mode in range(1, order // 2 + 1)
            }
            for inserted_mode, tested_mode in itertools.permutations(cuts, 2):
                if 2 * maximum + inserted_mode + tested_mode > order:
                    continue
                for inserted_cut in cuts[inserted_mode]:
                    for tested_cut in cuts[tested_mode]:
                        obligations += 1
                        first = grow_once(path, inserted_mode, inserted_cut)
                        transported_tested = transported_cut(
                            tested_cut, inserted_cut, inserted_mode
                        )
                        verify_growth(first, tested_mode, transported_tested)

                        second = grow_once(path, tested_mode, tested_cut)
                        transported_inserted = transported_cut(
                            inserted_cut, tested_cut, tested_mode
                        )
                        verify_growth(second, inserted_mode, transported_inserted)
                        final_a = grow_once(first, tested_mode, transported_tested)
                        final_b = grow_once(second, inserted_mode, transported_inserted)
                        if final_a != final_b:
                            raise ValueError(
                                ("noncommuting", path, inserted_mode, tested_mode)
                            )
                        record = [
                            order,
                            path,
                            maximum,
                            inserted_mode,
                            inserted_cut,
                            tested_mode,
                            tested_cut,
                            final_a,
                        ]
                        record_hash.update(
                            json.dumps(record, separators=(",", ":")).encode()
                        )
                        record_hash.update(b"\n")
        path_counts[order] = paths
        obligation_counts[order] = obligations
    return {
        "max_order": max_order,
        "paths_by_order": path_counts,
        "obligations_by_order": obligation_counts,
        "total_paths": sum(path_counts.values()),
        "total_obligations": sum(obligation_counts.values()),
        "record_sha256": record_hash.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=8)
    args = parser.parse_args()
    for key, value in check(args.max_order).items():
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
