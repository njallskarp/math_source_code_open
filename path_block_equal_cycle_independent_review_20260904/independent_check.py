"""Definition-level exact audit of the equal-cycle path-block theorem.

This file imports no target code.  For endpoint cycle types ``left`` and
``right`` it constructs

    (1-t) Q_left(t) Q_right(t) sum_n A_left(n) A_right(n) t^n,

where A_tau is computed by the elementary unbounded-coin recurrence.  A
common period L gives an a priori denominator
``(1-t**L)**(len(left)+len(right)+1)`` for the Hadamard series, so ordinary
integer polynomial division decides polynomiality without floating point.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from functools import cache
from itertools import combinations_with_replacement
from math import comb, factorial, gcd, lcm, prod

Partition = tuple[int, ...]
Polynomial = list[int]


def trim(poly: Polynomial) -> Polynomial:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def exact_division(numerator: Polynomial, denominator: Polynomial) -> Polynomial | None:
    numerator = trim(numerator[:])
    denominator = trim(denominator[:])
    if denominator == [0]:
        raise ZeroDivisionError
    if len(numerator) < len(denominator):
        return [0] if numerator == [0] else None
    quotient = [0] * (len(numerator) - len(denominator) + 1)
    lead = denominator[-1]
    for degree in range(len(numerator) - 1, len(denominator) - 2, -1):
        value = numerator[degree]
        if value % lead:
            return None
        coefficient = value // lead
        offset = degree - len(denominator) + 1
        quotient[offset] = coefficient
        for index, entry in enumerate(denominator):
            numerator[offset + index] -= coefficient * entry
    return trim(quotient) if not any(numerator) else None


@cache
def partitions(total: int, maximum: int | None = None) -> tuple[Partition, ...]:
    """All positive integer partitions, in decreasing lexicographic order."""
    if total == 0:
        return ((),)
    maximum = total if maximum is None else min(total, maximum)
    result: list[Partition] = []
    for first in range(maximum, 0, -1):
        result.extend((first, *tail) for tail in partitions(total - first, first))
    return tuple(result)


def series_coefficients(parts: Partition, limit: int) -> list[int]:
    """Coefficients of 1/((1-t) product_a (1-t^a)) through ``limit``."""
    coefficients = [1] + [0] * limit
    for weight in (1, *parts):
        for degree in range(weight, limit + 1):
            coefficients[degree] += coefficients[degree - weight]
    return coefficients


def cycle_determinant(parts: Partition) -> Polynomial:
    result = [1]
    for part in parts:
        factor = [0] * (part + 1)
        factor[0] = 1
        factor[part] = -1
        result = poly_mul(result, factor)
    return result


def period_denominator(period: int, exponent: int) -> Polynomial:
    result = [0] * (period * exponent + 1)
    for index in range(exponent + 1):
        result[index * period] = (-1) ** index * comb(exponent, index)
    return result


def hadamard_numerator(left: Partition, right: Partition) -> tuple[Polynomial, Polynomial]:
    """Return N,D with sum A_left(n)A_right(n)t^n = N/D exactly."""
    period = lcm(*left, *right)
    exponent = len(left) + len(right) + 1
    denominator = period_denominator(period, exponent)
    cutoff = period * exponent
    # One full period beyond the proper-numerator cutoff checks the recurrence.
    limit = cutoff + period - 1
    left_coefficients = series_coefficients(left, limit)
    right_coefficients = series_coefficients(right, limit)
    hadamard = [a * b for a, b in zip(left_coefficients, right_coefficients)]
    numerator_coefficients: list[int] = []
    for degree in range(limit + 1):
        value = 0
        for index in range(min(exponent, degree // period) + 1):
            value += (-1) ** index * comb(exponent, index) * hadamard[degree - index * period]
        numerator_coefficients.append(value)
    if any(numerator_coefficients[cutoff:]):
        raise AssertionError((left, right, "period recurrence failed"))
    return trim(numerator_coefficients[:cutoff]), denominator


def endpoint_numerator(left: Partition, right: Partition) -> Polynomial | None:
    """Return the polynomial h* evaluation, or None if it has a denominator."""
    numerator, denominator = hadamard_numerator(left, right)
    multiplier = poly_mul([1, -1], poly_mul(cycle_determinant(left), cycle_determinant(right)))
    return exact_division(poly_mul(multiplier, numerator), denominator)


def rectangular(parts: Partition) -> bool:
    return len(set(parts)) == 1


def prime_divisors(value: int) -> tuple[int, ...]:
    result: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            result.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        result.append(value)
    return tuple(result)


def prime_profile(parts: Partition) -> tuple[int, tuple[int, ...]]:
    primes = sorted({prime for part in parts for prime in prime_divisors(part)})
    if not primes:
        return len(parts), ()
    counts = {prime: sum(part % prime == 0 for part in parts) for prime in primes}
    maximum = max(counts.values())
    return len(parts) - maximum, tuple(prime for prime in primes if counts[prime] == maximum)


def p_valuation(value: int, prime: int) -> int:
    valuation = 0
    while value % prime == 0:
        value //= prime
        valuation += 1
    return valuation


def unit_residue(cycle_count: int, defect: int, prime: int) -> int:
    divisible_count = cycle_count - defect
    block = prod(range(divisible_count, cycle_count + 1))
    return (block // prime ** p_valuation(block, prime)) % prime


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return trim(result)


def poly_scale(poly: Polynomial, scalar: int) -> Polynomial:
    return trim([scalar * value for value in poly])


def leading_cross_numerator(left: Partition, right: Partition, prime: int) -> Polynomial:
    left_divisible = sum(part % prime == 0 for part in left)
    right_divisible = sum(part % prime == 0 for part in right)
    left_nondivisible = tuple(part for part in left if part % prime)
    right_nondivisible = tuple(part for part in right if part % prime)
    first_scalar = factorial(len(left)) * factorial(right_divisible - 1) * prod(left_nondivisible)
    second_scalar = factorial(left_divisible - 1) * factorial(len(right)) * prod(right_nondivisible)
    return poly_add(
        poly_scale(cycle_determinant(right_nondivisible), first_scalar),
        poly_scale(cycle_determinant(left_nondivisible), second_scalar),
    )


def cyclotomic_prime(prime: int) -> Polynomial:
    return [1] * prime


def leading_cross_cancels(left: Partition, right: Partition, prime: int) -> bool:
    return exact_division(leading_cross_numerator(left, right, prime), cyclotomic_prime(prime)) is not None


def normalized_pair(left: Partition, right: Partition) -> tuple[Partition, Partition]:
    common = 0
    for part in (*left, *right):
        common = gcd(common, part)
    return tuple(part // common for part in left), tuple(part // common for part in right)


def direct_grid(max_width: int) -> dict[str, int]:
    grouped: dict[int, list[Partition]] = defaultdict(list)
    for width in range(1, max_width + 1):
        for parts in partitions(width):
            grouped[len(parts)].append(parts)

    checked = polynomial = predicted = 0
    unequal_width = unequal_width_polynomial = 0
    equal_width_nonrectangular = equal_width_nonrectangular_polynomial = 0
    for group in grouped.values():
        for left, right in combinations_with_replacement(group, 2):
            checked += 1
            observed = endpoint_numerator(left, right) is not None
            expected = left == right and rectangular(left)
            polynomial += observed
            predicted += expected
            if sum(left) != sum(right):
                unequal_width += 1
                unequal_width_polynomial += observed
            elif not expected:
                equal_width_nonrectangular += 1
                equal_width_nonrectangular_polynomial += observed
            if observed != expected:
                raise AssertionError((left, right, observed, expected))
    return {
        "max_width": max_width,
        "partitions": sum(len(group) for group in grouped.values()),
        "unordered_equal_cycle_pairs": checked,
        "polynomial_pairs": polynomial,
        "predicted_rectangular_pairs": predicted,
        "unequal_width_pairs": unequal_width,
        "unequal_width_polynomial_pairs": unequal_width_polynomial,
        "equal_width_nonrectangular_pairs": equal_width_nonrectangular,
        "equal_width_nonrectangular_polynomial_pairs": equal_width_nonrectangular_polynomial,
    }


def local_unit_grid(max_width: int) -> dict[str, int]:
    checks = binary_checks = odd_checks = odd_cancellations = 0
    for width in range(2, max_width + 1):
        by_cycles: dict[int, list[Partition]] = defaultdict(list)
        for parts in partitions(width):
            by_cycles[len(parts)].append(parts)
        for group in by_cycles.values():
            for original_left, original_right in combinations_with_replacement(group, 2):
                left, right = normalized_pair(original_left, original_right)
                if rectangular(left) or rectangular(right):
                    continue
                left_profile = prime_profile(left)
                right_profile = prime_profile(right)
                if left_profile != right_profile or not left_profile[1]:
                    continue
                defect, primes = left_profile
                if defect <= 0:
                    raise AssertionError((left, right, left_profile))
                for prime in primes:
                    checks += 1
                    if prime == 2:
                        binary_checks += 1
                        # Every nondivisible part is odd, so both D(-1) products
                        # and both factorial/product scalars are positive.
                        numerator = leading_cross_numerator(left, right, prime)
                        value_at_minus_one = sum(
                            coefficient * (-1) ** degree
                            for degree, coefficient in enumerate(numerator)
                        )
                        if value_at_minus_one <= 0:
                            raise AssertionError((left, right, prime))
                    else:
                        odd_checks += 1
                        residue = 2 * unit_residue(len(left), defect, prime) % prime
                        if residue == 0:
                            raise AssertionError((left, right, prime, defect))
                        cancelled = leading_cross_cancels(left, right, prime)
                        odd_cancellations += cancelled
                        if cancelled:
                            raise AssertionError((left, right, prime, "unexpected cancellation"))
    return {
        "max_width": max_width,
        "common_profile_prime_checks": checks,
        "binary_phase_checks": binary_checks,
        "odd_unit_checks": odd_checks,
        "odd_leading_cancellations": odd_cancellations,
    }


HEIGHT_2095_LEFT: Partition = (
    9, 7, 6, 4, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1
)
HEIGHT_2095_RIGHT: Partition = (
    11, 7, 6, 4, 4, 4, 4, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1
)


def boundary_check() -> dict[str, int | bool]:
    left = HEIGHT_2095_LEFT
    right = HEIGHT_2095_RIGHT
    prime = 3
    defect = len(left) - sum(part % prime == 0 for part in left)
    left_block = prod(range(len(left) - defect, len(left) + 1))
    right_block = prod(range(len(right) - defect, len(right) + 1))
    left_v = p_valuation(left_block, prime)
    right_v = p_valuation(right_block, prime)
    residue = (left_block // prime**left_v + right_block // prime**right_v) % prime
    cancelled = leading_cross_cancels(left, right, prime)
    if (left_v, right_v, residue, cancelled) != (7, 7, 0, True):
        raise AssertionError((left_v, right_v, residue, cancelled))
    return {
        "prime": prime,
        "defect": defect,
        "left_valuation": left_v,
        "right_valuation": right_v,
        "normalized_sum_mod_p": residue,
        "leading_cancels": cancelled,
    }


def verify() -> dict[str, object]:
    report: dict[str, object] = {
        "claim": "same cycle count: polynomial iff identical rectangular endpoints",
        "direct_grid": direct_grid(12),
        "local_unit_grid": local_unit_grid(18),
        "height_2095_boundary": boundary_check(),
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    report = verify()
    direct = report["direct_grid"]
    local = report["local_unit_grid"]
    boundary = report["height_2095_boundary"]
    assert isinstance(direct, dict) and isinstance(local, dict) and isinstance(boundary, dict)
    print(
        "VERIFIED equal-cycle audit; "
        f"direct_pairs={direct['unordered_equal_cycle_pairs']}; "
        f"polynomial={direct['polynomial_pairs']}; "
        f"unequal_width_polynomial={direct['unequal_width_polynomial_pairs']}; "
        f"equal_width_nonrectangular_polynomial={direct['equal_width_nonrectangular_polynomial_pairs']}; "
        f"unit_checks={local['common_profile_prime_checks']}; "
        f"odd_cancellations={local['odd_leading_cancellations']}; "
        f"height2095_residue={boundary['normalized_sum_mod_p']}; "
        f"sha256={report['sha256']}"
    )


if __name__ == "__main__":
    main()
