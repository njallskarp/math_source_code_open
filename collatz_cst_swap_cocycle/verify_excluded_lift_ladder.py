"""Independent verifier for emitted excluded-lift ladder certificates.

The C++ frontier enumerator can be run with ``--emit-ladder``.  This verifier
does not import its parity-cylinder implementation: it rebuilds every stated
word, split barrier, candidate lift, and parity mismatch with Python integers.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Cylinder:
    length: int = 0
    odd_count: int = 0
    residue: int = 0
    endpoint: int = 0
    pow2: int = 1
    pow3: int = 1

    def extend(self, bit: int) -> "Cylinder":
        lift = self.endpoint & 1 if bit == 0 else (1 - self.endpoint) & 1
        intermediate = self.endpoint + self.pow3 * lift
        if (intermediate & 1) != bit:
            raise AssertionError("parity-cylinder extension failed")
        return Cylinder(
            length=self.length + 1,
            odd_count=self.odd_count + bit,
            residue=self.residue + self.pow2 * lift,
            endpoint=(
                intermediate // 2
                if bit == 0
                else (3 * intermediate + 1) // 2
            ),
            pow2=2 * self.pow2,
            pow3=self.pow3 if bit == 0 else 3 * self.pow3,
        )

    @property
    def numerator(self) -> int:
        return self.pow2 * self.endpoint - self.pow3 * self.residue


def cylinder(word: str) -> Cylinder:
    state = Cylinder()
    for character in word:
        if character not in "01":
            raise AssertionError("certificate word is not binary")
        state = state.extend(int(character))
    return state


def first_mismatch(prefix: Cylinder, candidate: int, suffix: str) -> int:
    numerator = 3 * prefix.pow3 * candidate + 3 * prefix.endpoint + 1
    value, remainder = divmod(numerator, 4)
    if remainder:
        raise AssertionError("candidate does not transport integrally")
    for index, expected_character in enumerate(suffix):
        observed = value & 1
        if observed != int(expected_character):
            return index + 1
        value = value // 2 if observed == 0 else (3 * value + 1) // 2
    return 0


def parse_record(line: str) -> dict[str, str]:
    if not line.startswith("ladder="):
        raise AssertionError("not a ladder record")
    fields: dict[str, str] = {}
    for item in line.removeprefix("ladder=").split(","):
        key, separator, value = item.partition(":")
        if not separator or key in fields:
            raise AssertionError("malformed or duplicate record field")
        fields[key] = value
    expected = {"K", "word", "j", "gap", "Q", "chi2", "steps", "mismatches"}
    if set(fields) != expected:
        raise AssertionError("record fields differ from the fixed schema")
    return fields


def verify_record(fields: dict[str, str]) -> tuple[int, int, int]:
    length = int(fields["K"])
    word = fields["word"]
    position = int(fields["j"])
    stated_gap = int(fields["gap"])
    stated_surplus = int(fields["Q"])
    stated_chi = int(fields["chi2"])
    stated_steps = int(fields["steps"])
    stated_mismatches = [int(value) for value in fields["mismatches"].split(";")]

    if len(word) != length or not (0 <= position + 2 <= length):
        raise AssertionError("invalid word length or split position")
    if word[position : position + 2] != "10":
        raise AssertionError("target split is not p10s")

    prefixes = [Cylinder()]
    for character in word:
        prefixes.append(prefixes[-1].extend(int(character)))
    target = prefixes[-1]
    if target.pow3 >= target.pow2:
        raise AssertionError("target is not coefficient-contracting")
    if any(state.pow3 < state.pow2 for state in prefixes[1:-1]):
        raise AssertionError("target is not coefficient-first-crossing")

    prefix = prefixes[position]
    if prefix.pow3 < 2 * prefix.pow2:
        raise AssertionError("reverse-swapped source is not first-crossing")
    suffix_word = word[position + 2 :]
    suffix = cylinder(suffix_word)
    local_modulus = 1 << (length - position)
    scale = 1 << position
    target_lift, remainder = divmod(target.residue - prefix.residue, scale)
    if remainder or target_lift < 0:
        raise AssertionError("target does not lift the split prefix")
    inverse = pow(3 * prefix.pow3, -1, local_modulus)
    if target_lift >= inverse:
        raise AssertionError("recorded edge is not wrapped")

    gap = target.pow2 - target.pow3
    surplus = (
        local_modulus * prefix.residue
        - suffix.pow3 * (3 * prefix.endpoint + 1)
        - 4 * suffix.numerator
    )
    if (gap, surplus) != (stated_gap, stated_surplus):
        raise AssertionError("stated gap or split surplus is incorrect")
    if gap * target_lift + surplus != local_modulus * (
        target.residue - target.endpoint
    ):
        raise AssertionError("split barrier identity failed")

    chi = target_lift & 3
    if chi != stated_chi or gap * chi + surplus > 0:
        raise AssertionError("invalid base two-bit obstruction")
    steps = (-(gap * chi + surplus)) // (4 * gap) + 1
    if steps != stated_steps or len(stated_mismatches) != steps:
        raise AssertionError("ladder length is not the least barrier-clearing rank")
    forced_lower_bound = chi + 4 * steps
    if forced_lower_bound > target_lift:
        raise AssertionError("ladder overshoots the true lift")
    if gap * forced_lower_bound + surplus <= 0:
        raise AssertionError("ladder does not clear the split barrier")

    for rank, stated_mismatch in enumerate(stated_mismatches):
        mismatch = first_mismatch(prefix, chi + 4 * rank, suffix_word)
        if mismatch == 0 or mismatch != stated_mismatch:
            raise AssertionError("candidate parity-mismatch certificate failed")
    return steps, sum(stated_mismatches), max(stated_mismatches)


def verify(path: Path) -> dict[str, int | str]:
    digest = hashlib.sha256()
    certificates = 0
    candidates = 0
    parity_bits = 0
    maximum_steps = 0
    maximum_mismatch = 0
    previous_record = ""
    with path.open("rt", encoding="ascii", newline="") as handle:
        for raw_line in handle:
            if not raw_line.startswith("ladder="):
                continue
            if not raw_line.endswith("\n"):
                raise AssertionError("unterminated certificate record")
            record = raw_line[:-1]
            if previous_record and record == previous_record:
                raise AssertionError("adjacent duplicate certificate record")
            previous_record = record
            steps, used_bits, mismatch = verify_record(parse_record(record))
            digest.update(raw_line.encode("ascii"))
            certificates += 1
            candidates += steps
            parity_bits += used_bits
            maximum_steps = max(maximum_steps, steps)
            maximum_mismatch = max(maximum_mismatch, mismatch)
    return {
        "certificates": certificates,
        "candidates": candidates,
        "parity_bits": parity_bits,
        "maximum_steps": maximum_steps,
        "maximum_mismatch": maximum_mismatch,
        "sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate_output", type=Path)
    args = parser.parse_args()
    report = verify(args.certificate_output)
    for key, value in report.items():
        print(f"{key}={value}")
    print("status=independent excluded-lift ladder verification passed")


if __name__ == "__main__":
    main()
