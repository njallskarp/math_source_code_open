#!/usr/bin/env python3
"""Exact, solver-free verifier for the exceptional-ray residue profiles."""

from __future__ import annotations

import argparse
import collections
import itertools
import re
from hashlib import sha256
from pathlib import Path

from verify_certificate import parse_certificate

PAIRS = tuple((left, right) for left in range(8) for right in range(left + 1, 8))

HEADER = "CERTIFICATE stable_transitivity_residue_profiles_v1 n=8"
ROW = re.compile(
    r"CLASS (?P<index>\d+) tournament=(?P<tournament>\d+) "
    r"dilation=(?P<dilation>\d+) stabilizer=(?P<stabilizer>\d+) "
    r"deficit=(?P<deficit>\d+) candidates=(?P<candidates>\d+) "
    r"profile=(?P<profile>.+)"
)
EXPECTED_LAYERS = {0: 832, 1: 4192, 2: 9344, 3: 11584, 4: 9344, 5: 4192, 6: 832}
EXPECTED_CANDIDATES = {2: 35296, 3: 25952, 4: 14368, 5: 5024}


def order_masks_definition() -> tuple[int, ...]:
    """Enumerate order masks directly, independently of the generator helper."""
    masks = []
    for order in itertools.permutations(range(8)):
        position = [0] * 8
        for rank, vertex in enumerate(order):
            position[vertex] = rank
        masks.append(
            sum(
                int(position[left] < position[right]) << edge
                for edge, (left, right) in enumerate(PAIRS)
            )
        )
    if len(masks) != 40320 or len(set(masks)) != 40320:
        raise AssertionError("direct order enumeration is incomplete")
    return tuple(masks)


def agrees_definition(tournament: int, order_mask: int, edge: int) -> int:
    return int(((tournament ^ order_mask) >> edge) & 1 == 0)


def read_profiles(
    path: Path,
) -> list[tuple[int, int, int, int, int, int, tuple[tuple[int, int], ...]]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != HEADER:
        raise ValueError("wrong residue-profile header")
    records = []
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        match = ROW.fullmatch(line)
        if match is None:
            raise ValueError("malformed residue-profile row")
        profile = []
        for term in match["profile"].split(","):
            order, multiplicity = term.split(":")
            profile.append((int(order), int(multiplicity)))
        records.append(
            (
                int(match["index"]),
                int(match["tournament"]),
                int(match["dilation"]),
                int(match["stabilizer"]),
                int(match["deficit"]),
                int(match["candidates"]),
                tuple(profile),
            )
        )
    return records


def verify(radial_certificate: Path, profiles_path: Path) -> str:
    radial = parse_certificate(radial_certificate)
    source = {index: (tournament, dual) for index, tournament, dual, _ in radial}
    if len(source) != 96:
        raise ValueError("expected 96 radial source classes")
    profiles = read_profiles(profiles_path)
    expected_keys = [
        (index, dilation)
        for index, _, _, _ in radial
        for dilation in range(2, 6)
    ]
    if [(index, dilation) for index, _, dilation, *rest in profiles] != expected_keys:
        raise ValueError("residue-profile coverage or canonical order is wrong")

    orders = order_masks_definition()
    dual_deficits: dict[int, tuple[int, ...]] = {}
    for index, (tournament, dual) in source.items():
        deficits = tuple(
            13 - sum(agrees_definition(tournament, order, edge) for edge in dual)
            for order in orders
        )
        if min(deficits) != 0 or max(deficits) != 6:
            raise ValueError(f"class {index}: wrong dual order range")
        if collections.Counter(deficits) != EXPECTED_LAYERS:
            raise ValueError(f"class {index}: wrong G8 defect distribution")
        dual_deficits[index] = deficits

    arc_checks = 0
    profile_orders = 0
    squarefree_profiles = 0
    for (
        index,
        tournament,
        dilation,
        stabilizer,
        declared_deficit,
        candidate_count,
        profile,
    ) in profiles:
        source_tournament, dual = source[index]
        if tournament != source_tournament:
            raise ValueError(f"class {index}, d={dilation}: tournament mismatch")
        if stabilizer != dilation + 1:
            raise ValueError(f"class {index}, d={dilation}: wrong stabilizer")
        if declared_deficit != 6 - dilation:
            raise ValueError(f"class {index}, d={dilation}: wrong declared deficit")
        actual_candidates = sum(
            deficit <= declared_deficit for deficit in dual_deficits[index]
        )
        if candidate_count != actual_candidates or candidate_count != EXPECTED_CANDIDATES[dilation]:
            raise ValueError(f"class {index}, d={dilation}: wrong candidate count")

        indices = [order for order, _ in profile]
        if len(indices) != len(set(indices)):
            raise ValueError(f"class {index}, d={dilation}: repeated order index")
        if any(order < 0 or order >= len(orders) for order in indices):
            raise ValueError(f"class {index}, d={dilation}: order index out of range")
        if any(multiplicity != 1 for _, multiplicity in profile):
            raise ValueError(f"class {index}, d={dilation}: profile is not square-free")
        profile_size = 3 * dilation + 2
        if len(profile) != profile_size:
            raise ValueError(f"class {index}, d={dilation}: wrong profile size")
        margin = 2 * dilation + 1
        for edge in range(28):
            count = sum(
                agrees_definition(tournament, orders[order], edge)
                for order in indices
            )
            if count != margin:
                raise ValueError(
                    f"class {index}, d={dilation}: edge {edge} count {count} != {margin}"
                )
            arc_checks += 1
        actual_deficit = sum(dual_deficits[index][order] for order in indices)
        if actual_deficit != declared_deficit:
            raise ValueError(f"class {index}, d={dilation}: wrong total G8 deficit")
        profile_orders += len(profile)
        squarefree_profiles += 1

    rows = [
        "classes=96",
        "residues=2,3,4,5",
        f"profiles={len(profiles)} profile_orders={profile_orders} squarefree_profiles={squarefree_profiles}",
        f"arc_count_checks={arc_checks}",
        "g8_defect_layers=0:832,1:4192,2:9344,3:11584,4:9344,5:4192,6:832",
        "candidate_counts=d2:35296,d3:25952,d4:14368,d5:5024",
        "residue_values=m(dT)=d+1_for_d=2,3,4,5",
        "exact_rays=m(kT)=ceil(7k/6)_using_d1_and_d6_dependencies",
    ]
    canonical = "\n".join(rows)
    return canonical + "\naudit_sha256=" + sha256(canonical.encode("ascii")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radial-certificate", type=Path, default=Path("certificate.txt"))
    parser.add_argument("--profiles", type=Path, default=Path("residue_profiles.txt"))
    args = parser.parse_args()
    print(verify(args.radial_certificate, args.profiles))


if __name__ == "__main__":
    main()
