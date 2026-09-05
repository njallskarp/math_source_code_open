#!/usr/bin/env python3
"""Exact arithmetic audit for the 399-coclique extension theorem."""

from fractions import Fraction


V = 3250
K = 57
S = 399
BASE = 8
OUTSIDE = V - S


def count_profiles() -> list[tuple[int, ...]]:
    """Enumerate counts of positive w-values after the spectral m>=58 step.

    A profile (n_1,...,n_8) has sum j*n_j=65, sum j^2*n_j=121,
    and total support at least 58.  Values above 8 are impossible already
    from sum w(w-1)=56.
    """

    answers: list[tuple[int, ...]] = []

    def visit(j: int, remaining_sum: int, remaining_sq: int,
              support: int, counts: list[int]) -> None:
        if j == 9:
            if remaining_sum == 0 and remaining_sq == 0 and support >= 58:
                answers.append(tuple(counts))
            return
        max_count = min(remaining_sum // j, remaining_sq // (j * j))
        for count in range(max_count + 1):
            visit(
                j + 1,
                remaining_sum - j * count,
                remaining_sq - j * j * count,
                support + count,
                counts + [count],
            )

    visit(1, 65, 121, 0, [])
    return answers


def main() -> None:
    sum_a = K * S
    sum_a2 = S * (S + K - 1)
    sum_z = sum_a - BASE * OUTSIDE
    sum_z2 = sum_a2 - 2 * BASE * sum_a + BASE * BASE * OUTSIDE
    energy = sum_z2 + sum_z

    assert OUTSIDE == 2851
    assert (sum_a, sum_a2) == (22743, 181545)
    assert (sum_z, sum_z2, energy) == (-65, 121, 56)

    positive_support_max = energy // 2
    positive_rho_lower = 6
    positive_order_required = positive_rho_lower**2 + 1
    assert positive_support_max == 28
    assert positive_order_required == 37
    assert positive_order_required > positive_support_max

    negative_rho_lower = Fraction(912, 121)
    square_surplus = 912**2 - 56 * 121**2
    assert square_surplus == 11848
    assert negative_rho_lower**2 > 56
    negative_support_min = 58

    profiles = count_profiles()
    assert profiles == [(57, 0, 0, 0, 0, 0, 0, 1)]

    n_w = profiles[0]
    degree_profile = {
        BASE - w: n_w[w - 1]
        for w in range(1, 9)
        if n_w[w - 1]
    }
    degree_profile[BASE] = OUTSIDE - sum(n_w)
    assert degree_profile == {0: 1, 7: 57, 8: 2793}
    assert sum(degree_profile.values()) == OUTSIDE
    assert sum(a * n for a, n in degree_profile.items()) == sum_a
    assert sum(a * a * n for a, n in degree_profile.items()) == sum_a2

    print("Moore(57,2) 399-coclique exact audit")
    print(f"outside={OUTSIDE} sum_a={sum_a} sum_a2={sum_a2}")
    print(f"sum_z={sum_z} sum_z2={sum_z2} defect_energy={energy}")
    print(
        "positive-support contradiction: "
        f"size<={positive_support_max}, spectral size>={positive_order_required}"
    )
    print(
        "negative-support threshold: "
        f"rho>={negative_rho_lower}, square_surplus={square_surplus}, "
        f"size>={negative_support_min}"
    )
    print(f"admissible exact profiles after threshold={len(profiles)}")
    print("neighbor-count profile: 0^1 7^57 8^2793")
    print("conclusion: every 399-coclique has a unique 400-coclique extension")


if __name__ == "__main__":
    main()
