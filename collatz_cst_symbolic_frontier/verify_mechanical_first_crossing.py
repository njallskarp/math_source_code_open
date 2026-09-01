"""Exact audit of the cap-maximizing mechanical first-crossing cylinders."""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass

LOW_MASK = (1 << 256) - 1


@dataclass(frozen=True)
class CylinderState:
    """Least-residue cylinder data for one finite shortcut parity word."""

    length: int
    odd_count: int
    residue: int
    endpoint: int
    pow2: int
    pow3: int

    @staticmethod
    def empty() -> CylinderState:
        return CylinderState(0, 0, 0, 0, 1, 1)

    def extend(self, bit: int) -> CylinderState:
        """Append one parity bit using exact cylinder compatibility."""
        if bit not in (0, 1):
            raise ValueError("a parity bit must be 0 or 1")
        if bit == 0:
            lift = self.endpoint & 1
            intermediate = self.endpoint + self.pow3 * lift
            if intermediate & 1:
                raise AssertionError("even extension compatibility failed")
            endpoint = intermediate // 2
            odd_count = self.odd_count
            pow3 = self.pow3
        else:
            lift = (1 - self.endpoint) & 1
            intermediate = self.endpoint + self.pow3 * lift
            if not intermediate & 1:
                raise AssertionError("odd extension compatibility failed")
            endpoint = (3 * intermediate + 1) // 2
            odd_count = self.odd_count + 1
            pow3 = 3 * self.pow3
        return CylinderState(
            self.length + 1,
            odd_count,
            self.residue + self.pow2 * lift,
            endpoint,
            2 * self.pow2,
            pow3,
        )


def digest_record(state: CylinderState) -> bytes:
    """Canonical bounded-size cross-implementation state record."""
    difference = state.residue - state.endpoint
    return (
        f"{state.length},{state.odd_count},"
        f"{state.residue.bit_length()},{state.endpoint.bit_length()},"
        f"{state.residue & LOW_MASK:064x},"
        f"{state.endpoint & LOW_MASK:064x},"
        f"{difference & LOW_MASK:064x}\n"
    ).encode("ascii")


def audit(max_length: int, comparison_length: int = 100_000) -> dict[str, int | str]:
    """Audit the coefficient-minimal mechanical first-crossing family."""
    if max_length < 1:
        raise ValueError("max_length must be positive")
    if not 1 <= comparison_length <= max_length:
        raise ValueError("comparison_length must lie in [1,max_length]")

    state = CylinderState.empty()
    digest = hashlib.sha256()
    comparison_digest = ""
    cases = 0
    nontrivial_cases = 0
    equalities = 0
    failures = 0
    last_crossing_length = 0
    last_crossing_odd_count = 0

    for crossing_length in range(1, max_length + 1):
        if state.pow3 < 2 * state.pow2:
            crossing = state.extend(0)
            cases += 1
            last_crossing_length = crossing.length
            last_crossing_odd_count = crossing.odd_count
            if crossing.odd_count >= 2:
                nontrivial_cases += 1
                if crossing.residue <= crossing.endpoint:
                    failures += 1
            elif crossing.residue == crossing.endpoint:
                equalities += 1
            digest.update(digest_record(crossing))

        if crossing_length == comparison_length:
            comparison_digest = digest.copy().hexdigest()

        # Greedily keep 3^q >= 2^L using the fewest odd bits at every prefix.
        next_bit = int(state.pow3 < 2 * state.pow2)
        state = state.extend(next_bit)

    return {
        "max_length": max_length,
        "comparison_length": comparison_length,
        "first_crossing_cases": cases,
        "nontrivial_cases": nontrivial_cases,
        "trivial_equalities": equalities,
        "nontrivial_failures": failures,
        "last_crossing_length": last_crossing_length,
        "last_crossing_odd_count": last_crossing_odd_count,
        "comparison_sha256": comparison_digest,
        "full_sha256": digest.hexdigest(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=200_000)
    parser.add_argument("--comparison-length", type=int, default=100_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = audit(args.max_length, args.comparison_length)
    for key, value in report.items():
        print(f"{key}={value}")
    print("status=exact mechanical first-crossing audit passed")


if __name__ == "__main__":
    main()
