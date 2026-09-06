#!/usr/bin/env python3
"""Definition-level check of the corrected four-dimensional link factor.

The explicit flag sphere is C5 * C5 * S0. Its clique complex is enumerated
on 12 labeled vertices; face counts, h/gamma coefficients, and link kappas
are computed exactly. The join-of-spheres topology is a human premise.
No third-party package is required. Tested with CPython 3.12.12.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import comb


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def component(vertex):
    return 0 if vertex < 5 else 1 if vertex < 10 else 2


def adjacent(a, b):
    if a == b:
        return False
    if component(a) != component(b):
        return True
    if component(a) == 2:
        return False
    return (a - b) % 5 in (1, 4)


def face_counts(faces):
    counts = [0] * (max(f.bit_count() for f in faces) + 1)
    for face in faces:
        counts[face.bit_count()] += 1
    return counts


def h_coefficients(counts):
    d = len(counts) - 1
    return [
        sum(counts[i] * (-1) ** (j - i) * comb(d - i, j - i)
            for i in range(j + 1))
        for j in range(d + 1)
    ]


def gamma_coefficients(h):
    d = len(h) - 1
    remainder = h.copy()
    gamma = []
    for i in range(d // 2 + 1):
        coefficient = remainder[i]
        gamma.append(coefficient)
        for j in range(d - 2 * i + 1):
            remainder[i + j] -= coefficient * comb(d - 2 * i, j)
    require(not any(remainder), "h-polynomial has no claimed gamma expansion")
    return gamma


def kappa(counts):
    return sum((Fraction(-1, 2) ** i) * count
               for i, count in enumerate(counts))


def main():
    faces = {
        mask for mask in range(1 << 12)
        if all(adjacent(a, b) for a, b in combinations(
            [v for v in range(12) if mask & (1 << v)], 2))
    }
    counts = face_counts(faces)
    require(counts == [1, 12, 55, 120, 125, 50], "unexpected join face counts")
    require(len(faces) == 363, "unexpected number of faces")
    h = h_coefficients(counts)
    gamma = gamma_coefficients(h)
    require(h == [1, 7, 17, 17, 7, 1], "incorrect h-vector")
    require(gamma == [1, 2, 1], "incorrect gamma-vector")

    link_h_sum = [0] * 5
    link_kappas = []
    for v in range(12):
        bit = 1 << v
        link = {face for face in faces if not (face & bit) and (face | bit) in faces}
        link_counts = face_counts(link)
        require(len(link_counts) == 5, "vertex link has incorrect dimension")
        link_h = h_coefficients(link_counts)
        link_gamma = gamma_coefficients(link_h)
        link_kappa = kappa(link_counts)
        require(link_gamma[2] == 16 * link_kappa, "3-sphere normalization fails")
        link_kappas.append(link_kappa)
        link_h_sum = [a + b for a, b in zip(link_h_sum, link_h)]

    # Coefficients of 5 h(t) + (1-t) h'(t), including its vanishing top term.
    rhs = [5 * h[j] - j * h[j] + ((j + 1) * h[j + 1] if j < 5 else 0)
           for j in range(6)]
    require(link_h_sum + [0] == rhs, "full face-link polynomial identity fails")
    require(link_kappas == [Fraction(0)] * 10 + [Fraction(1, 16)] * 2,
            "unexpected link kappa distribution")
    total = sum(link_kappas)
    corrected = 8 * total
    recorded = Fraction(1, 8) * total
    require(gamma[2] == corrected, "corrected factor does not reproduce gamma_2")
    require(gamma[2] != recorded, "example fails to refute reciprocal factor")

    lines = [
        "sphere=C5*C5*S0",
        "vertices=12",
        "faces_including_empty=363",
        "f_by_cardinality=" + ",".join(map(str, counts)),
        "h=" + ",".join(map(str, h)),
        "gamma=" + ",".join(map(str, gamma)),
        "link_kappa_sum=" + str(total),
        "correct_factor_8_rhs=" + str(corrected),
        "recorded_factor_1_over_8_rhs=" + str(recorded),
        "face_link_polynomial_identity=VERIFIED",
    ]
    for line in lines:
        print(line)
    print("result_sha256=" + sha256(("\n".join(lines) + "\n").encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
