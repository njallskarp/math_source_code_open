#!/usr/bin/env python3
"""Formal KOH tail-alignment audit for the canonical (2,6)/(3,6) rays.

The checker works with affine indices in the parameter c.  It generates every
KOH summand from the partition formula, recursively expands only the one-row
tail of the width-two and width-three comparators, and compares the resulting
formal multisets with independently transcribed remainder formulas.  No value
of c is substituted into a Gaussian polynomial.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
import json
from math import comb
import sys


C_MIN = 16


@dataclass(frozen=True, order=True)
class Affine:
    slope: int
    constant: int = 0

    def __add__(self, other: "Affine | int") -> "Affine":
        if isinstance(other, int):
            return Affine(self.slope, self.constant + other)
        return Affine(self.slope + other.slope, self.constant + other.constant)

    def __sub__(self, other: "Affine | int") -> "Affine":
        if isinstance(other, int):
            return Affine(self.slope, self.constant - other)
        return Affine(self.slope - other.slope, self.constant - other.constant)

    def __mul__(self, scalar: int) -> "Affine":
        return Affine(self.slope * scalar, self.constant * scalar)

    __rmul__ = __mul__

    def value(self, c: int) -> int:
        return self.slope * c + self.constant

    def text(self) -> str:
        if self.slope == 0:
            return str(self.constant)
        head = "c" if self.slope == 1 else f"{self.slope}c"
        if self.constant > 0:
            return f"{head}+{self.constant}"
        if self.constant < 0:
            return f"{head}{self.constant}"
        return head


C = Affine(1, 0)


@dataclass(frozen=True, order=True)
class Atom:
    """The homogeneous Gaussian B(top,bottom)."""

    top: Affine
    bottom: int

    def record(self) -> list[object]:
        return [self.top.slope, self.top.constant, self.bottom]

    def text(self) -> str:
        return f"B({self.top.text()},{self.bottom})"


@dataclass(frozen=True, order=True)
class Monomial:
    e2_power: int
    factors: tuple[Atom, ...]

    def record(self) -> list[object]:
        return [self.e2_power, [factor.record() for factor in self.factors]]

    def text(self) -> str:
        product = "*".join(factor.text() for factor in self.factors) or "1"
        return f"e2^{self.e2_power}*{product}"


@dataclass(frozen=True)
class HRange:
    """A signed affine finite sum of e2^(u+shift) h_(degree(c,u))."""

    coefficient: int
    lower: Affine
    upper: Affine
    e2_shift: int
    degree_c_slope: int
    degree_u_slope: int
    degree_constant: int

    def record(self) -> dict[str, object]:
        return {
            "coefficient": self.coefficient,
            "lower": [self.lower.slope, self.lower.constant],
            "upper": [self.upper.slope, self.upper.constant],
            "e2_shift": self.e2_shift,
            "h_degree": [
                self.degree_c_slope,
                self.degree_u_slope,
                self.degree_constant,
            ],
        }


def atom(slope: int, constant: int, bottom: int) -> Atom:
    return Atom(Affine(slope, constant), bottom)


def h(slope: int, constant: int) -> Atom:
    """Return h_(slope*c+constant) as B(slope*c+constant+1,1)."""

    return atom(slope, constant + 1, 1)


def monomial(e2_power: int, *factors: Atom) -> Monomial:
    return Monomial(e2_power, tuple(sorted(factors)))


def assert_nonnegative_for_all(form: Affine, c_min: int = C_MIN) -> None:
    assert form.slope >= 0 and form.value(c_min) >= 0, form


def partitions(total: int, ceiling: int | None = None) -> list[tuple[int, ...]]:
    if total == 0:
        return [()]
    ceiling = total if ceiling is None else min(ceiling, total)
    result: list[tuple[int, ...]] = []
    for first in range(ceiling, 0, -1):
        for rest in partitions(total - first, first):
            result.append((first,) + rest)
    return result


def koh_summand(width: int, rectangle: Affine, partition: tuple[int, ...]) -> Monomial:
    """Generate F_lambda from Zeilberger's KOH partition formula."""

    assert sum(partition) == width
    padded = (0,) + partition + (0,)
    partial = [0]
    for part in partition:
        partial.append(partial[-1] + part)
    partial.append(width)

    factors: list[Atom] = []
    for j in range(1, len(partition) + 1):
        bottom = padded[j] - padded[j + 1]
        if bottom == 0:
            continue
        top = j * (rectangle + 2) - partial[j - 1] - partial[j + 1]
        assert_nonnegative_for_all(top - bottom)
        factors.append(Atom(top, bottom))
    exponent = 2 * sum(comb(part, 2) for part in partition)
    return monomial(exponent, *factors)


def koh_decomposition(width: int, rectangle: Affine) -> dict[tuple[int, ...], Monomial]:
    return {
        partition: koh_summand(width, rectangle, partition)
        for partition in partitions(width)
    }


def signed_counter(values: list[tuple[int, Monomial]]) -> Counter[Monomial]:
    result: Counter[Monomial] = Counter()
    for coefficient, term in values:
        result[term] += coefficient
        if result[term] == 0:
            del result[term]
    return result


def add_counters(*values: Counter[Monomial]) -> Counter[Monomial]:
    result: Counter[Monomial] = Counter()
    for value in values:
        for term, coefficient in value.items():
            result[term] += coefficient
            if result[term] == 0:
                del result[term]
    return result


def scale_counter(value: Counter[Monomial], scalar: int) -> Counter[Monomial]:
    return Counter({term: scalar * coefficient for term, coefficient in value.items()})


def shift_counter(value: Counter[Monomial], amount: int) -> Counter[Monomial]:
    assert all(term.e2_power + amount >= 0 for term in value)
    return Counter(
        {
            Monomial(term.e2_power + amount, term.factors): coefficient
            for term, coefficient in value.items()
        }
    )


def recursive_one_row_tail(
    width: int, rectangle: Affine, steps: int
) -> tuple[Counter[Monomial], Monomial, list[Affine]]:
    """Expand all non-one-row KOH terms and recurse down the one-row tail."""

    cumulative = 0
    current = rectangle
    heads: Counter[Monomial] = Counter()
    parameters = [current]
    for _ in range(steps):
        decomposition = koh_decomposition(width, current)
        tail = decomposition[(width,)]
        expected_tail_exponent = width * (width - 1)
        assert tail.e2_power == expected_tail_exponent
        for partition, term in decomposition.items():
            if partition != (width,):
                shifted = Monomial(cumulative + term.e2_power, term.factors)
                heads[shifted] += 1
        cumulative += expected_tail_exponent
        current = current + 2 - 2 * width
        parameters.append(current)

    tail = monomial(cumulative, Atom(current + width, width))
    return heads, tail, parameters


def expected_width_six() -> Counter[Monomial]:
    return signed_counter(
        [
            (1, monomial(0, h(6, 0))),
            (1, monomial(2, h(1, -2), h(5, -2))),
            (1, monomial(4, h(2, -4), h(4, -4))),
            (1, monomial(6, atom(1, -2, 2), h(4, -4))),
            (1, monomial(6, atom(3, -4, 2))),
            (1, monomial(8, h(1, -4), h(2, -6), h(3, -6))),
            (1, monomial(12, atom(1, -3, 3), h(3, -6))),
            (1, monomial(12, atom(2, -5, 3))),
            (1, monomial(14, atom(1, -4, 2), atom(2, -6, 2))),
            (1, monomial(20, atom(1, -4, 4), h(2, -8))),
            (1, monomial(30, atom(1, -4, 6))),
        ]
    )


def expected_width_two_iteration() -> tuple[Counter[Monomial], Monomial]:
    heads = signed_counter(
        [(1, monomial(2 * j, h(6, -4 * j))) for j in range(15)]
    )
    return heads, monomial(30, atom(3, -28, 2))


def expected_width_three_iteration() -> tuple[Counter[Monomial], Monomial]:
    values: list[tuple[int, Monomial]] = []
    for j in range(5):
        values.extend(
            [
                (1, monomial(6 * j, h(6, -12 * j))),
                (
                    1,
                    monomial(
                        6 * j + 2,
                        h(2, -4 * j - 2),
                        h(4, -8 * j - 2),
                    ),
                ),
            ]
        )
    return signed_counter(values), monomial(30, atom(2, -17, 3))


def rewrite_a2_leading(residual: Counter[Monomial]) -> Counter[Monomial]:
    """Use h_a h_b-h_(a+b)=e2 h_(a-1)h_(b-1) symbolically."""

    result = residual.copy()
    leading = [(term, coefficient) for term, coefficient in result.items() if term.e2_power == 2]
    assert len(leading) == 2 and sorted(coefficient for _, coefficient in leading) == [-1, 1]
    positive = next(term for term, coefficient in leading if coefficient == 1)
    negative = next(term for term, coefficient in leading if coefficient == -1)
    assert len(positive.factors) == 2 and all(atom_.bottom == 1 for atom_ in positive.factors)
    assert len(negative.factors) == 1 and negative.factors[0].bottom == 1

    h_degrees = [factor.top - 1 for factor in positive.factors]
    total = h_degrees[0] + h_degrees[1]
    assert negative.factors[0].top - 1 == total
    for degree in h_degrees:
        assert_nonnegative_for_all(degree - 1)

    del result[positive]
    del result[negative]
    replacement = monomial(
        3,
        Atom(positive.factors[0].top - 1, 1),
        Atom(positive.factors[1].top - 1, 1),
    )
    result[replacement] += 1
    return result


def rewrite_a3_leading(residual: Counter[Monomial]) -> tuple[Counter[Monomial], HRange]:
    """Cancel two Clebsch--Gordan ranges and return the exact Delta range."""

    result = residual.copy()
    leading = [(term, coefficient) for term, coefficient in result.items() if term.e2_power == 2]
    assert len(leading) == 2 and sorted(coefficient for _, coefficient in leading) == [-1, 1]
    positive = next(term for term, coefficient in leading if coefficient == 1)
    negative = next(term for term, coefficient in leading if coefficient == -1)
    assert all(len(term.factors) == 2 for term, _ in leading)
    assert all(factor.bottom == 1 for term, _ in leading for factor in term.factors)

    def product_data(term: Monomial) -> tuple[Affine, Affine]:
        degrees = sorted((factor.top - 1 for factor in term.factors), key=lambda x: x.value(C_MIN))
        assert_nonnegative_for_all(degrees[0])
        assert_nonnegative_for_all(degrees[1] - degrees[0])
        return degrees[0], degrees[0] + degrees[1]

    positive_upper, positive_total = product_data(positive)
    negative_upper, negative_total = product_data(negative)
    assert positive_total == negative_total
    assert_nonnegative_for_all(negative_upper - positive_upper - 1)

    # e2^2 times the product difference, followed by factoring e2^4,
    # leaves -sum_{u=positive_upper+1}^{negative_upper}
    # e2^(u-2) h_(positive_total-2u).
    delta = HRange(
        coefficient=-1,
        lower=positive_upper + 1,
        upper=negative_upper,
        e2_shift=-2,
        degree_c_slope=positive_total.slope,
        degree_u_slope=-2,
        degree_constant=positive_total.constant,
    )
    del result[positive]
    del result[negative]
    return result, delta


def expected_a2_k() -> Counter[Monomial]:
    values: list[tuple[int, Monomial]] = [
        (1, monomial(0, h(1, -3), h(5, -3))),
        (1, monomial(1, h(2, -4), h(4, -4))),
        (1, monomial(3, atom(1, -2, 2), h(4, -4))),
        (1, monomial(3, atom(3, -4, 2))),
        (1, monomial(5, h(1, -4), h(2, -6), h(3, -6))),
        (1, monomial(9, atom(1, -3, 3), h(3, -6))),
        (1, monomial(9, atom(2, -5, 3))),
        (1, monomial(11, atom(1, -4, 2), atom(2, -6, 2))),
        (1, monomial(17, atom(1, -4, 4), h(2, -8))),
    ]
    values.extend(
        (-1, monomial(2 * j - 3, h(6, -4 * j))) for j in range(2, 15)
    )
    return signed_counter(values)


def expected_a3_k() -> tuple[Counter[Monomial], HRange]:
    values = [
        (1, monomial(0, h(2, -4), h(4, -4))),
        (1, monomial(2, atom(1, -2, 2), h(4, -4))),
        (1, monomial(2, atom(3, -4, 2))),
        (-1, monomial(2, h(6, -12))),
        (1, monomial(4, h(1, -4), h(2, -6), h(3, -6))),
        (-1, monomial(4, h(2, -6), h(4, -10))),
        (1, monomial(8, atom(1, -3, 3), h(3, -6))),
        (1, monomial(8, atom(2, -5, 3))),
        (-1, monomial(8, h(6, -24))),
        (1, monomial(10, atom(1, -4, 2), atom(2, -6, 2))),
        (-1, monomial(10, h(2, -10), h(4, -18))),
        (-1, monomial(14, h(6, -36))),
        (1, monomial(16, atom(1, -4, 4), h(2, -8))),
        (-1, monomial(16, h(2, -14), h(4, -26))),
        (-1, monomial(20, h(6, -48))),
        (-1, monomial(22, h(2, -18), h(4, -34))),
    ]
    delta = HRange(-1, C - 1, 2 * C - 2, -2, 6, -2, -4)
    return signed_counter(values), delta


def counter_record(value: Counter[Monomial]) -> list[list[object]]:
    return [
        [coefficient, term.record()]
        for term, coefficient in sorted(value.items())
    ]


def main() -> None:
    if sys.flags.optimize:
        raise RuntimeError("run without -O: exact verification requires assertions")

    width_six_labeled = koh_decomposition(6, C)
    width_six = Counter(width_six_labeled.values())
    assert len(width_six_labeled) == 11
    assert width_six == expected_width_six()

    tail6 = width_six_labeled[(6,)]
    previous_width_six = monomial(30, Atom((C - 10) + 6, 6))
    assert tail6 == previous_width_six
    width_six_head = add_counters(width_six, scale_counter(Counter({tail6: 1}), -1))

    a2_heads, a2_tail, a2_parameters = recursive_one_row_tail(2, 3 * C, 15)
    expected_a2_heads, expected_a2_tail = expected_width_two_iteration()
    assert a2_heads == expected_a2_heads and a2_tail == expected_a2_tail
    assert a2_tail == monomial(30, Atom(3 * (C - 10) + 2, 2))
    for parameter in a2_parameters:
        assert_nonnegative_for_all(parameter - 2)

    a3_heads, a3_tail, a3_parameters = recursive_one_row_tail(3, 2 * C, 5)
    expected_a3_heads, expected_a3_tail = expected_width_three_iteration()
    assert a3_heads == expected_a3_heads and a3_tail == expected_a3_tail
    assert a3_tail == monomial(30, Atom(2 * (C - 10) + 3, 3))
    for parameter in a3_parameters:
        assert_nonnegative_for_all(parameter - 3)

    a2_residual = add_counters(width_six_head, scale_counter(a2_heads, -1))
    a2_rewritten = rewrite_a2_leading(a2_residual)
    a2_k = shift_counter(a2_rewritten, -3)
    assert a2_k == expected_a2_k()
    assert sum(abs(value) for value in a2_k.values()) == 22

    a3_residual = add_counters(width_six_head, scale_counter(a3_heads, -1))
    a3_rewritten, derived_delta = rewrite_a3_leading(a3_residual)
    a3_k = shift_counter(a3_rewritten, -4)
    expected_a3_terms, expected_delta = expected_a3_k()
    assert a3_k == expected_a3_terms and derived_delta == expected_delta
    assert sum(abs(value) for value in a3_k.values()) == 16

    record = {
        "schema": "lucas-b6-koh-alignment-v1",
        "parameter_domain": "c>=16",
        "koh_formula": {
            "width_six_partitions": len(width_six_labeled),
            "width_six_summands": [
                [list(partition), term.record()]
                for partition, term in sorted(width_six_labeled.items(), reverse=True)
            ],
        },
        "a2": {
            "comparator_width": 2,
            "tail_steps": 15,
            "head_terms": sum(abs(x) for x in a2_heads.values()),
            "tail": a2_tail.record(),
            "factored_remainder_power": 3,
            "remainder_terms": counter_record(a2_k),
        },
        "a3": {
            "comparator_width": 3,
            "tail_steps": 5,
            "head_terms": sum(abs(x) for x in a3_heads.values()),
            "tail": a3_tail.record(),
            "factored_remainder_power": 4,
            "delta": derived_delta.record(),
            "remainder_terms": counter_record(a3_k),
        },
    }
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()

    print("partition-generated KOH decomposition: PASS (11 width-six partitions)")
    print("(2,6) tail: 15 width-two steps, exact shift e2^30 and factor e2^3")
    print("(2,6) formal K terms: 22 signed monomials")
    print("(3,6) tail: 5 width-three steps, exact shift e2^30 and factor e2^4")
    print("(3,6) formal K units: 16 signed monomials plus one affine Delta range")
    print(f"canonical alignment record SHA-256: {digest}")


if __name__ == "__main__":
    main()
