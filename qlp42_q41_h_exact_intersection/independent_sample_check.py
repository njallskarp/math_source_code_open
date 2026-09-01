#!/usr/bin/env python3
"""Independent direct audit of the new H-intersection criterion."""

from __future__ import annotations

from random import Random

Gaussian = tuple[int, int]
N = 21
FULL = (1 << N) - 1


def add(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] + y[0], x[1] + y[1]


def sub(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] - y[0], x[1] - y[1]


def mul(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def conj(x: Gaussian) -> Gaussian:
    return x[0], -x[1]


def neg(x: Gaussian) -> Gaussian:
    return -x[0], -x[1]


def div_pi(x: Gaussian) -> Gaussian:
    assert (x[0] + x[1]) % 2 == 0
    return (x[0] + x[1]) // 2, (x[1] - x[0]) // 2


def pi3_bit(x: Gaussian) -> int:
    for _ in range(3):
        x = div_pi(x)
    return (x[0] + x[1]) & 1


def unit(axis: int, sign: int) -> Gaussian:
    value = (1, 0) if axis == 0 else (0, 1)
    return neg(value) if sign else value


def paf(word: list[Gaussian], shift: int) -> Gaussian:
    total = (0, 0)
    for j, value in enumerate(word):
        total = add(total, mul(value, conj(word[(j + shift) % N])))
    return total


def rotate(mask: int, shift: int) -> int:
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def reflected_axes(a_half: int) -> int:
    result = 0
    for shift in range(1, 11):
        bit = (a_half >> (shift - 1)) & 1
        result |= bit << shift
        result |= bit << (N - shift)
    return result


def theta_h(a_half: int, signature: int) -> int:
    axes = reflected_axes(a_half)
    result = 0
    for shift in range(1, 11):
        axis = (a_half >> (shift - 1)) & 1
        correlation = (axes & rotate(axes, shift)).bit_count() & 1
        e_bit = (signature >> (shift - 1)) & 1
        result |= (1 ^ axis ^ correlation ^ e_bit) << (shift - 1)
    return result


def h_word(a_half: int, theta: int) -> list[Gaussian]:
    word = [(0, 0)] * N
    for shift in range(1, 11):
        axis = (a_half >> (shift - 1)) & 1
        word[shift] = unit(axis, 0)
        word[N - shift] = unit(axis, (theta >> (shift - 1)) & 1)
    return word


def criterion(a_half: int, theta: int) -> bool:
    active = [0, 0]
    for pair in range(10):
        if not ((theta >> pair) & 1):
            active[(a_half >> pair) & 1] += 1
    return active[0] % 2 == 0 and active[1] % 2 == 0


def direct_sum_zero_possible(base: list[Gaussian]) -> bool:
    pair_sums = [add(base[s], base[N - s]) for s in range(1, 11)]
    for flips in range(1 << 10):
        total = (0, 0)
        for pair, value in enumerate(pair_sums):
            total = add(total, neg(value) if ((flips >> pair) & 1) else value)
        if total == (0, 0):
            return True
    return False


def main() -> None:
    rng = Random(0x5141_4801)
    samples = {(0, 0), (0, 1023), (1023, 0), (1023, 1023)}
    while len(samples) < 512:
        samples.add((rng.randrange(1 << 10), rng.randrange(1 << 10)))

    direction_checks = 0
    for a_half, signature in sorted(samples):
        theta = theta_h(a_half, signature)
        base = h_word(a_half, theta)
        assert direct_sum_zero_possible(base) == criterion(a_half, theta)
        for pair in range(10):
            variant = base.copy()
            shift = pair + 1
            variant[shift] = neg(variant[shift])
            variant[N - shift] = neg(variant[N - shift])
            column = 0
            for autocorrelation_shift in range(1, 11):
                delta = sub(paf(variant, autocorrelation_shift), paf(base, autocorrelation_shift))
                column |= pi3_bit(delta) << (autocorrelation_shift - 1)
            assert column.bit_count() % 2 == 0
            direction_checks += 1

    print(f"direct_a_signature_samples={len(samples)}")
    print(f"direct_pair_direction_checks={direction_checks}")
    print("sum_zero_criterion=verified")
    print("even_direction_parity=verified")
    print("independent_sample_check=verified")


if __name__ == "__main__":
    main()
