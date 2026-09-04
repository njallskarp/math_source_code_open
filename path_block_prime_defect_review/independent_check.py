"""Independent exact audit of the unequal-width prime-defect pole theorem.

This checker does not import the target implementation.  Its finite-grid test
uses residue-wise polynomial tails, while its hard-case pole calculation uses
Berlekamp--Massey over the rational numbers.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from functools import cache
from itertools import product
from math import factorial, gcd, lcm

Partition = tuple[int, ...]
Polynomial = list[Fraction]

BASE_LEFT = (4, 4, 3, 3, 3, 3, 1)
BASE_RIGHT = (3, 3, 3, 3, 3, 2, 2, 2)
HARD_UNEQUAL_CASES = (
    (BASE_LEFT, (6, 3, 3, 3, 3, 2, 2, 2)),
    ((6, 4, 4, 3, 3, 3, 1), BASE_RIGHT),
    ((6, 4, 4, 3, 3, 3, 1), (9, 3, 3, 3, 3, 2, 2, 2)),
)


@cache
def partitions(total: int, maximum: int | None = None) -> tuple[Partition, ...]:
    """Integer partitions in nonincreasing order."""
    if total == 0:
        return ((),)
    if maximum is None or maximum > total:
        maximum = total
    result: list[Partition] = []
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, first):
            result.append((first, *tail))
    return tuple(result)


def accumulated_counts(partition: Partition, maximum: int) -> list[int]:
    """Coefficient prefix of 1/((1-t) product_a (1-t^a))."""
    exact = [0] * (maximum + 1)
    exact[0] = 1
    for weight in partition:
        for degree in range(weight, maximum + 1):
            exact[degree] += exact[degree - weight]
    running = 0
    for degree, value in enumerate(exact):
        running += value
        exact[degree] = running
    return exact


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return trim(answer)


def trim(poly: Polynomial) -> Polynomial:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def determinant(left: Partition, right: Partition) -> Polynomial:
    answer: Polynomial = [Fraction(1), Fraction(-1)]
    for weight in left + right:
        factor = [Fraction(0)] * (weight + 1)
        factor[0] = 1
        factor[weight] = -1
        answer = multiply(answer, factor)
    return answer


def convolve_prefix(sequence: list[int], poly: Polynomial) -> Polynomial:
    return [
        sum(
            (poly[j] * sequence[n - j] for j in range(min(n, len(poly) - 1) + 1)),
            Fraction(0),
        )
        for n in range(len(sequence))
    ]


def common_rectangular(left: Partition, right: Partition) -> bool:
    return len(set(left)) == 1 and len(set(right)) == 1 and left[0] == right[0]


def tail_polynomiality(left: Partition, right: Partition) -> bool:
    """Decide polynomiality from exact quasipolynomial tails.

    The coefficient product has period dividing L and degree at most r+s.
    After convolution by the determinant, each sufficiently late residue tail
    is therefore a polynomial of degree at most r+s.  Testing r+s+1 values in
    every residue is an exact identity test, not a numerical truncation.
    """
    period = lcm(*(left + right))
    degree_bound = len(left) + len(right)
    det = determinant(left, right)
    first_q = (len(det) + period - 1) // period + 1
    maximum = period * (first_q + degree_bound) + period - 1
    left_counts = accumulated_counts(left, maximum)
    right_counts = accumulated_counts(right, maximum)
    product_sequence = [a * b for a, b in zip(left_counts, right_counts, strict=True)]
    hstar = convolve_prefix(product_sequence, det)
    return all(
        hstar[residue + period * q] == 0
        for residue in range(period)
        for q in range(first_q, first_q + degree_bound + 1)
    )


def berlekamp_massey(sequence: list[int]) -> Polynomial:
    """Minimal recurrence connection polynomial over Q."""
    connection: Polynomial = [Fraction(1)]
    previous: Polynomial = [Fraction(1)]
    length = 0
    shift = 1
    previous_discrepancy = Fraction(1)
    values = [Fraction(value) for value in sequence]

    for n in range(len(values)):
        discrepancy = values[n]
        for i in range(1, length + 1):
            discrepancy += connection[i] * values[n - i]
        if discrepancy == 0:
            shift += 1
            continue

        old_connection = connection[:]
        scale = -discrepancy / previous_discrepancy
        required = len(previous) + shift
        if len(connection) < required:
            connection.extend([Fraction(0)] * (required - len(connection)))
        for i, coefficient in enumerate(previous):
            connection[i + shift] += scale * coefficient

        if 2 * length <= n:
            length = n + 1 - length
            previous = old_connection
            previous_discrepancy = discrepancy
            shift = 1
        else:
            shift += 1

    return trim(connection[: length + 1])


def divide_exact(dividend: Polynomial, divisor: Polynomial) -> Polynomial | None:
    work = trim(dividend[:])
    divisor = trim(divisor[:])
    if len(work) < len(divisor):
        return [Fraction(0)] if work == [0] else None
    quotient = [Fraction(0)] * (len(work) - len(divisor) + 1)
    for degree in range(len(work) - 1, len(divisor) - 2, -1):
        coefficient = work[degree] / divisor[-1]
        offset = degree - len(divisor) + 1
        quotient[offset] = coefficient
        for j, value in enumerate(divisor):
            work[offset + j] -= coefficient * value
    return trim(quotient) if all(value == 0 for value in work) else None


def valuation(poly: Polynomial, factor: Polynomial) -> int:
    order = 0
    work = poly[:]
    while True:
        quotient = divide_exact(work, factor)
        if quotient is None:
            return order
        order += 1
        work = quotient


def rational_hstar(left: Partition, right: Partition) -> tuple[Polynomial, Polynomial]:
    """Recover h-star as numerator/denominator by an exact recurrence."""
    period = lcm(*(left + right))
    recurrence_bound = period * (len(left) + len(right) + 1)
    training_length = 2 * recurrence_bound + 8
    validation_length = recurrence_bound + 8
    maximum = training_length + validation_length - 1
    left_counts = accumulated_counts(left, maximum)
    right_counts = accumulated_counts(right, maximum)
    sequence = [a * b for a, b in zip(left_counts, right_counts, strict=True)]
    denominator = berlekamp_massey(sequence[:training_length])
    if len(denominator) - 1 > recurrence_bound:
        raise AssertionError("recurrence exceeded the quasipolynomial bound")
    order = len(denominator) - 1
    for n in range(training_length, len(sequence)):
        if sum(
            denominator[i] * sequence[n - i] for i in range(order + 1)
        ) != 0:
            raise AssertionError("recovered recurrence failed held-out coefficients")
    raw_numerator = convolve_prefix(sequence, denominator)
    if any(raw_numerator[n] for n in range(order, len(raw_numerator))):
        raise AssertionError("recovered numerator did not terminate")
    numerator = trim(raw_numerator[: max(order, 1)])
    return multiply(numerator, determinant(left, right)), denominator


def phi3_pole_order(left: Partition, right: Partition) -> tuple[int, int]:
    numerator, denominator = rational_hstar(left, right)
    phi3 = [Fraction(1), Fraction(1), Fraction(1)]
    pole = valuation(denominator, phi3) - valuation(numerator, phi3)
    return len(denominator) - 1, max(pole, 0)


def prime_profile(partition: Partition) -> tuple[int, tuple[int, ...]]:
    primes: set[int] = set()
    for part in partition:
        value = part
        divisor = 2
        while divisor * divisor <= value:
            if value % divisor == 0:
                primes.add(divisor)
                while value % divisor == 0:
                    value //= divisor
            divisor += 1
        if value > 1:
            primes.add(value)
    if not primes:
        return len(partition), ()
    counts = {prime: sum(part % prime == 0 for part in partition) for prime in primes}
    maximum = max(counts.values())
    return len(partition) - maximum, tuple(sorted(p for p, count in counts.items() if count == maximum))


def cyclotomic_product(partition: Partition, prime: int) -> tuple[int, ...]:
    """Evaluate product(1-zeta^a) in the power basis of Q[zeta].

    The basis is 1,zeta,...,zeta^(p-2), with zeta^(p-1) replaced by
    -(1+...+zeta^(p-2)).  This quotient-ring representation is independent of
    polynomial divisibility in the target checker.
    """
    dimension = prime - 1
    value = [1] + [0] * (dimension - 1)

    def monomial(exponent: int) -> tuple[int, ...]:
        residue = exponent % prime
        if residue == dimension:
            return tuple(-1 for _ in range(dimension))
        return tuple(int(i == residue) for i in range(dimension))

    def ring_multiply(left: list[int], right: tuple[int, ...]) -> list[int]:
        answer = [0] * dimension
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                if a and b:
                    reduced = monomial(i + j)
                    for k, coefficient in enumerate(reduced):
                        answer[k] += a * b * coefficient
        return answer

    for part in partition:
        if part % prime:
            factor = tuple(a - b for a, b in zip(monomial(0), monomial(part), strict=True))
            value = ring_multiply(value, factor)
    return tuple(value)


def leading_cancellation(left: Partition, right: Partition, prime: int) -> bool:
    left_divisible = sum(part % prime == 0 for part in left)
    right_divisible = sum(part % prime == 0 for part in right)
    if len(left) - left_divisible != len(right) - right_divisible:
        return False
    left_product = 1
    right_product = 1
    for part in left:
        if part % prime:
            left_product *= part
    for part in right:
        if part % prime:
            right_product *= part
    left_scalar = factorial(len(left)) * factorial(right_divisible - 1) * left_product
    right_scalar = factorial(left_divisible - 1) * factorial(len(right)) * right_product
    d_left = cyclotomic_product(left, prime)
    d_right = cyclotomic_product(right, prime)
    return all(
        left_scalar * x + right_scalar * y == 0
        for x, y in zip(d_right, d_left, strict=True)
    )


def first_leading_cancellation(maximum_width: int = 21) -> dict[str, object]:
    checked = 0
    found_width = 0
    found: list[tuple[Partition, Partition, int]] = []
    for width in range(2, maximum_width + 1):
        groups: dict[tuple[int, tuple[int, ...]], list[Partition]] = {}
        for partition in partitions(width):
            if len(set(partition)) == 1:
                continue
            profile = prime_profile(partition)
            if profile[1]:
                groups.setdefault(profile, []).append(partition)
        current: list[tuple[Partition, Partition, int]] = []
        for (_, primes), group in groups.items():
            for prime in primes:
                if prime == 2:
                    continue
                for i, left in enumerate(group):
                    for right in group[i + 1 :]:
                        checked += 1
                        if leading_cancellation(left, right, prime):
                            current.append((left, right, prime))
        if current:
            found_width = width
            found = current
            break
    return {"checked": checked, "first_width": found_width, "found": found}


def audit(grid_width: int = 8) -> dict[str, object]:
    types = [partition for width in range(1, grid_width + 1) for partition in partitions(width)]
    unequal_pairs = 0
    predicted_polynomial = 0
    observed_polynomial = 0
    mismatches: list[tuple[Partition, Partition, bool, bool]] = []
    for left, right in product(types, repeat=2):
        if sum(left) == sum(right):
            continue
        unequal_pairs += 1
        predicted = common_rectangular(left, right)
        observed = tail_polynomiality(left, right)
        predicted_polynomial += int(predicted)
        observed_polynomial += int(observed)
        if predicted != observed:
            mismatches.append((left, right, predicted, observed))

    hard_cases: list[dict[str, object]] = []
    for left, right in HARD_UNEQUAL_CASES:
        left_profile = prime_profile(left)
        right_profile = prime_profile(right)
        if left_profile != (3, (3,)) or right_profile != (3, (3,)):
            raise AssertionError((left_profile, right_profile))
        recurrence_order, pole_order = phi3_pole_order(left, right)
        hard_cases.append(
            {
                "left": left,
                "right": right,
                "widths": (sum(left), sum(right)),
                "recurrence_order": recurrence_order,
                "phi3_pole_order": pole_order,
            }
        )

    cancellation_scan = first_leading_cancellation()

    result: dict[str, object] = {
        "grid_width": grid_width,
        "unequal_ordered_pairs": unequal_pairs,
        "predicted_polynomial": predicted_polynomial,
        "observed_polynomial": observed_polynomial,
        "mismatches": mismatches,
        "hard_cases": hard_cases,
        "cancellation_scan": cancellation_scan,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return result


def main() -> None:
    result = audit()
    print(
        "INDEPENDENT unequal-width grid; "
        f"max_width={result['grid_width']}; "
        f"ordered_pairs={result['unequal_ordered_pairs']}; "
        f"predicted_polynomial={result['predicted_polynomial']}; "
        f"observed_polynomial={result['observed_polynomial']}; "
        f"mismatches={len(result['mismatches'])}"
    )
    for item in result["hard_cases"]:
        print(
            "HARD leading-cancellation family; "
            f"widths={item['widths'][0]},{item['widths'][1]}; "
            f"recurrence_order={item['recurrence_order']}; "
            f"phi3_pole_order={item['phi3_pole_order']}"
        )
    scan = result["cancellation_scan"]
    print(
        "INDEPENDENT quotient-ring cancellation scan; "
        f"checked={scan['checked']}; first_width={scan['first_width']}; "
        f"found={len(scan['found'])}"
    )
    print(f"sha256={result['sha256']}")


if __name__ == "__main__":
    main()
