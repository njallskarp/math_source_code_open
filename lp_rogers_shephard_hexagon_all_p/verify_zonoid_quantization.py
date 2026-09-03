#!/usr/bin/env python3
"""Exact sanity checks for the slope-measure quantization shadow.

This checks two continuous uniform-measure examples with Fraction arithmetic:
the three-level branch without a horizontal atom and the two-level branch
with one.  It corroborates the construction in
ZONOID_QUANTIZATION_FULL_EQUALITY.md; it is not a proof of the general
measure theorem.

Tested with CPython 3.12.12.  No third-party package is required.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256


@dataclass(frozen=True)
class PiecewiseLinear:
    """Continuous piecewise-linear map on [0,1], given by exact knots."""

    knots: tuple[tuple[Fraction, Fraction], ...]

    def segments(self):
        for (x0, y0), (x1, y1) in zip(self.knots, self.knots[1:]):
            assert x0 < x1
            slope = (y1 - y0) / (x1 - x0)
            intercept = y0 - slope * x0
            yield x0, x1, slope, intercept

    def gini_area(self) -> Fraction:
        """Return integral_0^1 (2x-1)T(x) dx exactly."""

        total = Fraction(0)
        for x0, x1, slope, intercept in self.segments():
            total += Fraction(2, 3) * slope * (x1**3 - x0**3)
            total += Fraction(2 * intercept - slope, 2) * (x1**2 - x0**2)
            total -= intercept * (x1 - x0)
        return total

    def scaled(self, factor: Fraction) -> "PiecewiseLinear":
        return PiecewiseLinear(tuple((x, factor * y) for x, y in self.knots))

    def interpolate_identity(self, t: Fraction) -> "PiecewiseLinear":
        return PiecewiseLinear(
            tuple((x, (1 - t) * x + t * y) for x, y in self.knots)
        )

    def lipschitz_constant(self) -> Fraction:
        return max(abs(slope) for _, _, slope, _ in self.segments())

    def is_nondecreasing(self) -> bool:
        return all(slope >= 0 for _, _, slope, _ in self.segments())


def smooth_step(
    cuts: tuple[Fraction, ...], levels: tuple[Fraction, ...], eta: Fraction
) -> PiecewiseLinear:
    """Linearly smooth an ordered step map in eta-neighborhoods of cuts."""

    assert len(levels) == len(cuts) + 1
    assert all(a < b for a, b in zip(cuts, cuts[1:]))
    assert all(a < b for a, b in zip(levels, levels[1:]))
    knots: list[tuple[Fraction, Fraction]] = [(Fraction(0), levels[0])]
    for index, cut in enumerate(cuts):
        assert 0 < cut - eta < cut + eta < 1
        knots.append((cut - eta, levels[index]))
        knots.append((cut + eta, levels[index + 1]))
    knots.append((Fraction(1), levels[-1]))
    return PiecewiseLinear(tuple(knots))


def check_branch(
    name: str,
    cuts: tuple[Fraction, ...],
    levels: tuple[Fraction, ...],
    eta: Fraction,
    horizontal_length: Fraction,
) -> list[str]:
    identity_area = Fraction(1, 6)
    approximation = smooth_step(cuts, levels, eta)
    raw_area = approximation.gini_area()
    assert raw_area > 0
    scale = identity_area / raw_area
    quantization = approximation.scaled(scale)
    assert quantization.gini_area() == identity_area
    assert quantization.is_nondecreasing()

    lipschitz = quantization.lipschitz_constant()
    epsilon = Fraction(1, 2 * (1 + lipschitz))
    probes = (-epsilon, Fraction(0), Fraction(1, 3), Fraction(1))
    for t in probes:
        shadow_map = quantization.interpolate_identity(t)
        assert shadow_map.is_nondecreasing()
        assert shadow_map.gini_area() == identity_area

    total_area = identity_area + horizontal_length
    return [
        f"{name}_raw_area={raw_area}",
        f"{name}_scale={scale}",
        f"{name}_lipschitz={lipschitz}",
        f"{name}_epsilon={epsilon}",
        f"{name}_shadow_probes={','.join(str(t) for t in probes)}",
        f"{name}_constant_total_area={total_area}",
    ]


def main() -> None:
    lines = ["uniform_identity_gini_area=1/6"]
    lines.extend(
        check_branch(
            "three_level",
            (Fraction(1, 3), Fraction(2, 3)),
            (Fraction(0), Fraction(1), Fraction(2)),
            Fraction(1, 30),
            Fraction(0),
        )
    )
    lines.extend(
        check_branch(
            "two_level_horizontal",
            (Fraction(1, 2),),
            (Fraction(0), Fraction(1)),
            Fraction(1, 20),
            Fraction(2, 5),
        )
    )
    digest = sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    for line in lines:
        print(line)
    print(f"result_sha256={digest}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
