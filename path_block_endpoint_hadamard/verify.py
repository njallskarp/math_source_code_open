"""Exact checks for the endpoint-Hadamard formula on three path blocks."""

from __future__ import annotations

import hashlib
import itertools
import json
from functools import cache
from math import comb, gcd, lcm

Polynomial = list[int]  # constant coefficient first
Partition = tuple[int, ...]


def trim(poly: Polynomial) -> Polynomial:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    result[i + j] += a * b
    return trim(result)


def cycle_determinant(partition: Partition) -> Polynomial:
    result = [1]
    for length in partition:
        factor = [0] * (length + 1)
        factor[0] = 1
        factor[length] = -1
        result = poly_mul(result, factor)
    return result


@cache
def partitions(total: int, maximum: int | None = None) -> tuple[Partition, ...]:
    if total == 0:
        return ((),)
    if maximum is None or maximum > total:
        maximum = total
    result: list[Partition] = []
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, first):
            result.append((first, *tail))
    return tuple(result)


def exact_sum_counts(partition: Partition, maximum: int) -> list[int]:
    """Counts nonnegative cycle variables of exact weighted sum n."""
    result = [0] * (maximum + 1)
    result[0] = 1
    for weight in partition:
        for value in range(weight, maximum + 1):
            result[value] += result[value - weight]
    return result


def accumulated_counts(partition: Partition, maximum: int) -> list[int]:
    result = exact_sum_counts(partition, maximum)
    running = 0
    for index, value in enumerate(result):
        running += value
        result[index] = running
    return result


def fixed_ehrhart_counts(
    left: Partition,
    middle: Partition,
    right: Partition,
    maximum: int,
) -> list[int]:
    """Fixed counts for P_3^(a), summed over the exact middle-block sum."""
    left_acc = accumulated_counts(left, maximum)
    middle_exact = exact_sum_counts(middle, maximum)
    right_acc = accumulated_counts(right, maximum)
    return [
        sum(
            middle_exact[block_sum]
            * left_acc[dilation - block_sum]
            * right_acc[dilation - block_sum]
            for block_sum in range(dilation + 1)
        )
        for dilation in range(maximum + 1)
    ]


def direct_fixed_count(
    dilation: int,
    left: Partition,
    middle: Partition,
    right: Partition,
) -> int:
    """Definition-level enumeration in one variable per permutation cycle."""
    count = 0
    cycle_count = len(left) + len(middle) + len(right)
    for values in itertools.product(range(dilation + 1), repeat=cycle_count):
        first = len(left)
        second = first + len(middle)
        left_sum = sum(a * b for a, b in zip(left, values[:first], strict=True))
        middle_sum = sum(
            a * b for a, b in zip(middle, values[first:second], strict=True)
        )
        right_sum = sum(
            a * b for a, b in zip(right, values[second:], strict=True)
        )
        if left_sum + middle_sum <= dilation and middle_sum + right_sum <= dilation:
            count += 1
    return count


def series_times_polynomial(series: list[int], poly: Polynomial) -> list[int]:
    return [
        sum(poly[j] * series[index - j] for j in range(min(index, len(poly) - 1) + 1))
        for index in range(len(series))
    ]


def endpoint_hstar_prefix(
    left: Partition, right: Partition, maximum: int
) -> list[int]:
    left_acc = accumulated_counts(left, maximum)
    right_acc = accumulated_counts(right, maximum)
    hadamard = [a * b for a, b in zip(left_acc, right_acc, strict=True)]
    determinant = poly_mul([1, -1], cycle_determinant(left + right))
    return series_times_polynomial(hadamard, determinant)


def verify_middle_cancellation(maximum: int = 24) -> int:
    """Compare the full fixed-count definition with the endpoint formula."""
    checked = 0
    for width in (2, 3):
        types = partitions(width)
        for left in types:
            for middle in types:
                for right in types:
                    ehrhart = fixed_ehrhart_counts(left, middle, right, maximum)
                    full_det = poly_mul(
                        [1, -1], cycle_determinant(left + middle + right)
                    )
                    direct_hstar = series_times_polynomial(ehrhart, full_det)
                    endpoint_hstar = endpoint_hstar_prefix(left, right, maximum)
                    if direct_hstar != endpoint_hstar:
                        raise AssertionError((left, middle, right))
                    checked += 1
    return checked


def verify_direct_counts() -> int:
    checked = 0
    for left in partitions(2):
        for middle in partitions(2):
            for right in partitions(2):
                formula = fixed_ehrhart_counts(left, middle, right, 3)
                direct = [
                    direct_fixed_count(q, left, middle, right) for q in range(4)
                ]
                if formula != direct:
                    raise AssertionError((left, middle, right, formula, direct))
                checked += len(direct)
    return checked


def hadamard_numerator(
    left: Partition, right: Partition
) -> tuple[Polynomial, Polynomial]:
    """Return N,D with sum A_left(n)A_right(n)t^n=N/D.

    If L is the lcm of the cycle lengths and s is one plus the total number
    of cycles, the coefficient sequence is a quasipolynomial of degree s-1
    and period L.  Hence D=(1-t^L)^s is a valid exact denominator.
    """
    period = 1
    for length in left + right:
        period = lcm(period, length)
    exponent = len(left) + len(right) + 1
    cutoff = period * exponent
    left_acc = accumulated_counts(left, cutoff - 1)
    right_acc = accumulated_counts(right, cutoff - 1)
    sequence = [a * b for a, b in zip(left_acc, right_acc, strict=True)]
    numerator = [
        sum(
            (-1) ** j * comb(exponent, j) * sequence[index - j * period]
            for j in range(min(exponent, index // period) + 1)
        )
        for index in range(cutoff)
    ]
    denominator = [0] * (cutoff + 1)
    for j in range(exponent + 1):
        denominator[j * period] = (-1) ** j * comb(exponent, j)
    return trim(numerator), denominator


def exact_division(numerator: Polynomial, denominator: Polynomial) -> Polynomial | None:
    """Return the integral quotient, or None if divisibility fails."""
    numerator = trim(numerator[:])
    denominator = trim(denominator[:])
    if len(numerator) < len(denominator):
        return [0] if numerator == [0] else None
    quotient = [0] * (len(numerator) - len(denominator) + 1)
    leading = denominator[-1]
    for degree in range(len(numerator) - 1, len(denominator) - 2, -1):
        value = numerator[degree]
        if value:
            if value % leading:
                return None
            coefficient = value // leading
            offset = degree - len(denominator) + 1
            quotient[offset] = coefficient
            for j, entry in enumerate(denominator):
                if entry:
                    numerator[offset + j] -= coefficient * entry
    if any(numerator):
        return None
    return trim(quotient)


@cache
def cyclotomic_polynomial(order: int) -> tuple[int, ...]:
    """Return Phi_order in constant-coefficient-first form."""
    if order < 1:
        raise ValueError("cyclotomic order must be positive")
    result = [-1] + [0] * (order - 1) + [1]
    for divisor in range(1, order):
        if order % divisor == 0:
            quotient = exact_division(result, list(cyclotomic_polynomial(divisor)))
            if quotient is None:
                raise AssertionError((order, divisor))
            result = quotient
    return tuple(result)


def polynomial_valuation(poly: Polynomial, factor: Polynomial) -> int:
    """Return the exact multiplicity with which factor divides poly."""
    valuation = 0
    remainder = poly[:]
    while True:
        quotient = exact_division(remainder, factor)
        if quotient is None:
            return valuation
        remainder = quotient
        valuation += 1


def hstar_polynomial(left: Partition, right: Partition) -> Polynomial | None:
    numerator, denominator = hadamard_numerator(left, right)
    determinant = poly_mul([1, -1], cycle_determinant(left + right))
    return exact_division(poly_mul(numerator, determinant), denominator)


def rectangular_formula(width: int, cycle_length: int) -> Polynomial:
    cycles = width // cycle_length
    result = [0] * (width + 1)
    for j in range(cycles + 1):
        result[j * cycle_length] = comb(cycles, j) ** 2
    return trim(result)


def synchronized_pole_witness(
    partition: Partition,
) -> tuple[int, int, int, int] | None:
    """Return (common scale, root order, maximal pole count, residual order).

    A rectangular partition reduces to the identity and has no pole witness.
    Otherwise the selected primitive root has maximal nontrivial pole order.
    """
    common_scale = gcd(*partition)
    reduced = tuple(length // common_scale for length in partition)
    if all(length == 1 for length in reduced):
        return None
    cycle_count = len(reduced)
    divisible_counts = {
        order: sum(length % order == 0 for length in reduced)
        for order in range(2, max(reduced) + 1)
    }
    maximal_pole_count = max(divisible_counts.values())
    root_order = min(
        order
        for order, count in divisible_counts.items()
        if count == maximal_pole_count
    )

    numerator, _ = hadamard_numerator(reduced, reduced)
    determinant = poly_mul([1, -1], cycle_determinant(reduced + reduced))
    product = poly_mul(numerator, determinant)
    numerator_valuation = polynomial_valuation(
        product, list(cyclotomic_polynomial(root_order))
    )
    common_denominator_valuation = 2 * cycle_count + 1
    residual_order = common_denominator_valuation - numerator_valuation
    expected_order = cycle_count - maximal_pole_count
    if residual_order != expected_order:
        raise AssertionError(
            (
                partition,
                reduced,
                root_order,
                maximal_pole_count,
                residual_order,
                expected_order,
            )
        )
    return common_scale, root_order, maximal_pole_count, residual_order


def verify_synchronized_poles(
    maximum_width: int = 20,
) -> tuple[int, tuple[tuple[int, int], ...]]:
    checked = 0
    histogram: dict[int, int] = {}
    for width in range(1, maximum_width + 1):
        for partition in partitions(width):
            witness = synchronized_pole_witness(partition)
            if witness is None:
                if len(set(partition)) != 1:
                    raise AssertionError((width, partition))
                continue
            checked += 1
            residual_order = witness[-1]
            histogram[residual_order] = histogram.get(residual_order, 0) + 1
    return checked, tuple(sorted(histogram.items()))


def verify_classification_grid(maximum_width: int = 10) -> tuple[int, int, int, int]:
    endpoint_pairs = 0
    polynomial_pairs = 0
    rectangular_cases = 0
    one_sided_failures = 0
    for width in range(1, maximum_width + 1):
        identity = (1,) * width
        expected_rectangular = {
            ((length,) * (width // length), (length,) * (width // length))
            for length in range(1, width + 1)
            if width % length == 0
        }
        observed: set[tuple[Partition, Partition]] = set()
        for left in partitions(width):
            for right in partitions(width):
                endpoint_pairs += 1
                quotient = hstar_polynomial(left, right)
                if quotient is not None:
                    observed.add((left, right))
                    polynomial_pairs += 1
                    if left != right or len(set(left)) != 1:
                        raise AssertionError((width, left, right, quotient))
                    expected = rectangular_formula(width, left[0])
                    if quotient != expected:
                        raise AssertionError((width, left, quotient, expected))
                    rectangular_cases += 1
                if left != identity and right == identity:
                    if quotient is not None:
                        raise AssertionError((width, left, right, quotient))
                    one_sided_failures += 1
        if observed != expected_rectangular:
            raise AssertionError((width, observed, expected_rectangular))
    return endpoint_pairs, polynomial_pairs, rectangular_cases, one_sided_failures


def verify() -> dict[str, object]:
    direct_fixed_cases = verify_direct_counts()
    middle_formula_triples = verify_middle_cancellation()
    (
        endpoint_pairs,
        polynomial_pairs,
        rectangular_formula_cases,
        one_sided_failures,
    ) = verify_classification_grid()
    synchronized_nonrectangular, pole_order_histogram = verify_synchronized_poles()
    report: dict[str, object] = {
        "classification_width": 10,
        "direct_fixed_cases": direct_fixed_cases,
        "endpoint_pairs": endpoint_pairs,
        "middle_formula_triples": middle_formula_triples,
        "one_sided_failures": one_sided_failures,
        "polynomial_pairs": polynomial_pairs,
        "rectangular_formula_cases": rectangular_formula_cases,
        "synchronized_nonrectangular": synchronized_nonrectangular,
        "synchronized_width": 20,
        "pole_order_histogram": pole_order_histogram,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    report = verify()
    print(
        "VERIFIED endpoint-Hadamard theorem; "
        f"middle_formula_triples={report['middle_formula_triples']}; "
        f"direct_fixed_cases={report['direct_fixed_cases']}; "
        f"endpoint_pairs={report['endpoint_pairs']}; "
        f"polynomial_pairs={report['polynomial_pairs']}; "
        f"one_sided_failures={report['one_sided_failures']}; "
        f"sha256={report['sha256']}"
    )
    print(
        "classification_width=10; "
        f"rectangular_formula_cases={report['rectangular_formula_cases']}"
    )
    histogram = ",".join(
        f"{order}:{count}" for order, count in report["pole_order_histogram"]
    )
    print(
        f"synchronized_width={report['synchronized_width']}; "
        f"synchronized_nonrectangular={report['synchronized_nonrectangular']}; "
        f"pole_order_histogram={histogram}"
    )


if __name__ == "__main__":
    main()
