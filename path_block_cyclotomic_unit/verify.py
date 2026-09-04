"""Exact checks for the cyclotomic-unit endpoint obstruction."""

from __future__ import annotations

import hashlib
import json
from functools import cache
from math import factorial, prod

Polynomial = list[int]
Partition = tuple[int, ...]


def trim(poly: Polynomial) -> Polynomial:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return trim(result)


def poly_scale(poly: Polynomial, scalar: int) -> Polynomial:
    return trim([scalar * value for value in poly])


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def exact_division(numerator: Polynomial, denominator: Polynomial) -> Polynomial | None:
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
            for index, entry in enumerate(denominator):
                numerator[offset + index] -= coefficient * entry
    return trim(quotient) if not any(numerator) else None


@cache
def cyclotomic_polynomial(order: int) -> tuple[int, ...]:
    result = [-1] + [0] * (order - 1) + [1]
    for divisor in range(1, order):
        if order % divisor == 0:
            quotient = exact_division(result, list(cyclotomic_polynomial(divisor)))
            if quotient is None:
                raise AssertionError((order, divisor))
            result = quotient
    return tuple(result)


@cache
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


def maximal_prime_profile(partition: Partition) -> tuple[int, tuple[int, ...]]:
    primes = sorted({prime for part in partition for prime in prime_divisors(part)})
    counts = {prime: sum(part % prime == 0 for part in partition) for prime in primes}
    maximum = max(counts.values())
    return len(partition) - maximum, tuple(prime for prime in primes if counts[prime] == maximum)


def p_valuation(value: int, prime: int) -> int:
    valuation = 0
    while value % prime == 0:
        value //= prime
        valuation += 1
    return valuation


def rising_block(start: int, defect: int) -> int:
    return prod(range(start, start + defect + 1))


def unit_obstruction(left: Partition, right: Partition, prime: int) -> dict[str, int | bool]:
    left_count = sum(part % prime == 0 for part in left)
    right_count = sum(part % prime == 0 for part in right)
    left_defect = len(left) - left_count
    right_defect = len(right) - right_count
    if not left_count or not right_count or left_defect != right_defect:
        raise ValueError("positive equal defects at the selected prime are required")
    defect = left_defect
    left_block = rising_block(left_count, defect)
    right_block = rising_block(right_count, defect)
    left_valuation = p_valuation(left_block, prime)
    right_valuation = p_valuation(right_block, prime)
    if left_valuation != right_valuation:
        obstructed = True
        normalized_sum = -1
    else:
        normalized_sum = (
            left_block // prime**left_valuation + right_block // prime**right_valuation
        ) % prime
        obstructed = normalized_sum != 0
    return {
        "prime": prime,
        "defect": defect,
        "left_divisible": left_count,
        "right_divisible": right_count,
        "left_block": left_block,
        "right_block": right_block,
        "left_valuation": left_valuation,
        "right_valuation": right_valuation,
        "normalized_sum_mod_p": normalized_sum,
        "obstructed": obstructed,
    }


def cycle_determinant(partition: Partition) -> Polynomial:
    result = [1]
    for length in partition:
        factor = [0] * (length + 1)
        factor[0] = 1
        factor[length] = -1
        result = poly_mul(result, factor)
    return result


def leading_cross_numerator(left: Partition, right: Partition, prime: int) -> Polynomial:
    left_count = sum(part % prime == 0 for part in left)
    right_count = sum(part % prime == 0 for part in right)
    defect = len(left) - left_count
    if defect != len(right) - right_count:
        raise ValueError("equal defects are required")
    left_nondivisible = tuple(part for part in left if part % prime)
    right_nondivisible = tuple(part for part in right if part % prime)
    left_product = prod(left_nondivisible)
    right_product = prod(right_nondivisible)
    first = factorial(len(left)) * factorial(right_count - 1) * left_product
    second = factorial(left_count - 1) * factorial(len(right)) * right_product
    return poly_add(
        poly_scale(cycle_determinant(right_nondivisible), first),
        poly_scale(cycle_determinant(left_nondivisible), second),
    )


def leading_cross_cancels(left: Partition, right: Partition, prime: int) -> bool:
    return (
        exact_division(
            leading_cross_numerator(left, right, prime),
            list(cyclotomic_polynomial(prime)),
        )
        is not None
    )


EQUAL_CYCLE_EXAMPLES: tuple[tuple[Partition, Partition, int], ...] = (
    ((9, 7, 6, 4, 3, 1), (12, 9, 4, 3, 1, 1), 3),
    ((25, 10, 7, 7, 5, 1, 1), (20, 15, 7, 7, 5, 1, 1), 5),
    ((28, 21, 7, 1, 1, 1, 1), (21, 14, 11, 7, 5, 1, 1), 7),
)

HEIGHT_2095_LEFT = (
    9,
    7,
    6,
    4,
    4,
    3,
    3,
    3,
    3,
    3,
    3,
    2,
    2,
    2,
    2,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
)
HEIGHT_2095_RIGHT = (
    11,
    7,
    6,
    4,
    4,
    4,
    4,
    3,
    3,
    3,
    3,
    3,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
)


def verify() -> dict[str, object]:
    examples: list[dict[str, object]] = []
    for left, right, prime in EQUAL_CYCLE_EXAMPLES:
        if sum(left) != sum(right) or len(left) != len(right):
            raise AssertionError((left, right))
        left_profile = maximal_prime_profile(left)
        right_profile = maximal_prime_profile(right)
        if left_profile != right_profile or left_profile[1] != (prime,):
            raise AssertionError((prime, left_profile, right_profile))
        obstruction = unit_obstruction(left, right, prime)
        if not obstruction["obstructed"]:
            raise AssertionError(obstruction)
        if leading_cross_cancels(left, right, prime):
            raise AssertionError((left, right, prime))
        examples.append(
            {
                "prime": prime,
                "width": sum(left),
                "cycles": len(left),
                "defect": left_profile[0],
                "normalized_sum_mod_p": obstruction["normalized_sum_mod_p"],
            }
        )

    hard_left_profile = maximal_prime_profile(HEIGHT_2095_LEFT)
    hard_right_profile = maximal_prime_profile(HEIGHT_2095_RIGHT)
    if hard_left_profile != (14, (3,)) or hard_right_profile != (14, (3,)):
        raise AssertionError((hard_left_profile, hard_right_profile))
    hard_obstruction = unit_obstruction(HEIGHT_2095_LEFT, HEIGHT_2095_RIGHT, 3)
    if hard_obstruction["obstructed"]:
        raise AssertionError(hard_obstruction)
    if not leading_cross_cancels(HEIGHT_2095_LEFT, HEIGHT_2095_RIGHT, 3):
        raise AssertionError("height-2095 leading cancellation was not recovered")

    report: dict[str, object] = {
        "theorem": "equal-width equal-cycle nonrectangular pairs are nonpolynomial",
        "equal_cycle_examples": examples,
        "height_2095_boundary": {
            "width": sum(HEIGHT_2095_LEFT),
            "left_cycles": len(HEIGHT_2095_LEFT),
            "right_cycles": len(HEIGHT_2095_RIGHT),
            "defect": hard_left_profile[0],
            "normalized_sum_mod_p": hard_obstruction["normalized_sum_mod_p"],
            "leading_cancels": True,
        },
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    report = verify()
    print(
        "VERIFIED cyclotomic-unit obstruction; "
        f"equal_cycle_primes=3,5,7; height_2095_boundary=passes; "
        f"sha256={report['sha256']}"
    )


if __name__ == "__main__":
    main()
