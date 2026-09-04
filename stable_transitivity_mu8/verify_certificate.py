#!/usr/bin/env python3
"""Definition-level exact verifier for the order-eight equal-margin certificate."""

from __future__ import annotations

import argparse
import itertools
import re
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

N = 8
PAIRS = tuple((i, j) for i in range(N) for j in range(i + 1, N))
TARGET = Fraction(13, 20)
HEADER = "CERTIFICATE stable_transitivity_mu8_v1 n=8 classes=96 target=13/20"
ROW = re.compile(
    r"CLASS (?P<index>\d+) tournament=(?P<tournament>\d+) "
    r"dual=(?P<dual>[\d,]+) primal=(?P<primal>.+)"
)


def read_obstructions(path: Path) -> list[tuple[int, int]]:
    records = []
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) != 2:
            raise ValueError("malformed obstruction record")
        records.append((int(fields[0]), int(fields[1])))
    if len(records) != 96 or len(set(records)) != 96:
        raise ValueError("expected 96 distinct obstruction records")
    return records


def order_vectors() -> tuple[tuple[int, ...], ...]:
    vectors = []
    for order in itertools.permutations(range(N)):
        position = [0] * N
        for rank, vertex in enumerate(order):
            position[vertex] = rank
        vectors.append(tuple(int(position[i] < position[j]) for i, j in PAIRS))
    if len(vectors) != 40_320 or len(set(vectors)) != 40_320:
        raise AssertionError("order enumeration is incomplete")
    return tuple(vectors)


def agrees(tournament: int, order: tuple[int, ...], edge: int) -> int:
    return int(order[edge] == ((tournament >> edge) & 1))


def parse_certificate(
    path: Path,
) -> list[tuple[int, int, tuple[int, ...], tuple[tuple[int, Fraction], ...]]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != HEADER:
        raise ValueError("wrong certificate header")
    records = []
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        match = ROW.fullmatch(line)
        if match is None:
            raise ValueError("malformed certificate row")
        dual = tuple(int(value) for value in match["dual"].split(","))
        primal = []
        for term in match["primal"].split(","):
            order_text, weight_text = term.split(":")
            primal.append((int(order_text), Fraction(weight_text)))
        records.append(
            (
                int(match["index"]),
                int(match["tournament"]),
                dual,
                tuple(primal),
            )
        )
    return records


def verify(certificate: Path, obstructions: Path) -> str:
    source = read_obstructions(obstructions)
    records = parse_certificate(certificate)
    if [(index, tournament) for index, tournament, _, _ in records] != source:
        raise ValueError("certificate records do not match the source obstruction list")
    orders = order_vectors()

    primal_terms = 0
    maximum_denominator = 0
    dual_order_checks = 0
    for index, tournament, dual, primal in records:
        if tournament < 0 or tournament >= 1 << len(PAIRS):
            raise ValueError(f"class {index}: tournament mask out of range")
        if len(dual) != 20 or len(set(dual)) != 20:
            raise ValueError(f"class {index}: dual must contain 20 distinct arcs")
        if any(edge < 0 or edge >= len(PAIRS) for edge in dual):
            raise ValueError(f"class {index}: dual arc out of range")
        dual_maximum = max(
            sum(agrees(tournament, order, edge) for edge in dual)
            for order in orders
        )
        dual_order_checks += len(orders)
        if dual_maximum != 13:
            raise ValueError(f"class {index}: dual maximum {dual_maximum} != 13")

        indices = [order for order, _ in primal]
        if len(indices) != len(set(indices)):
            raise ValueError(f"class {index}: repeated primal order")
        if any(order < 0 or order >= len(orders) for order in indices):
            raise ValueError(f"class {index}: primal order out of range")
        if any(weight <= 0 for _, weight in primal):
            raise ValueError(f"class {index}: primal weights must be positive")
        if sum(weight for _, weight in primal) != 1:
            raise ValueError(f"class {index}: primal weights do not sum to one")
        for edge in range(len(PAIRS)):
            coverage = sum(
                weight
                for order_index, weight in primal
                if agrees(tournament, orders[order_index], edge)
            )
            if coverage != TARGET:
                raise ValueError(
                    f"class {index}: edge {edge} coverage {coverage} != {TARGET}"
                )
        primal_terms += len(primal)
        maximum_denominator = max(
            maximum_denominator, *(weight.denominator for _, weight in primal)
        )

    canonical = "\n".join(
        [
            f"classes={len(records)}",
            f"orders={len(orders)}",
            f"dual_order_checks={dual_order_checks}",
            f"primal_terms={primal_terms}",
            f"maximum_denominator={maximum_denominator}",
            "equal_margin=13/20",
            "stable_rate=7/6",
        ]
    )
    digest = sha256(canonical.encode("ascii")).hexdigest()
    return canonical + f"\naudit_sha256={digest}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=Path("certificate.txt"))
    parser.add_argument("--obstructions", type=Path, default=Path("obstructions.txt"))
    args = parser.parse_args()
    print(verify(args.certificate, args.obstructions))


if __name__ == "__main__":
    main()
