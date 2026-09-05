#!/usr/bin/env python3
"""Exact arithmetic audit for the 398-coclique deficit-two theorem."""


V = 3250
K = 57
S = 398
BASE = 8
OUTSIDE = V - S


def main() -> None:
    sum_a = K * S
    sum_a2 = S * (S + K - 1)
    sum_z = sum_a - BASE * OUTSIDE
    sum_z2 = sum_a2 - 2 * BASE * sum_a + BASE * BASE * OUTSIDE
    energy = sum_z2 + sum_z

    assert OUTSIDE == 2852
    assert (sum_a, sum_a2) == (22686, 180692)
    assert (sum_z, sum_z2, energy) == (-130, 244, 114)

    # In the nonpositive, nonextendible branch, weights 3,...,7 violate
    # degree <= weighted-neighbour-sum.
    forbidden_weights = tuple(
        w for w in range(3, 8) if 49 + w > 7 * w + 2
    )
    assert forbidden_weights == (3, 4, 5, 6, 7)

    # With only weights 1 and 2, the two moments solve uniquely.
    n2 = (244 - 130) // 2
    n1 = 130 - 2 * n2
    assert (n1, n2) == (16, 57)
    assert n1 + 2 * n2 == 130
    assert n1 + 4 * n2 == 244

    # For every possible e_11, the required two-W1 zero vertices exceed the
    # available nonadjacent W1 pairs by at least 244 (or have wrong parity).
    integral_gaps = []
    for e11 in range(0, n1 * (n1 - 1) // 2 + 1):
        twice_b = 728 - e11
        if twice_b % 2 == 0:
            b = twice_b // 2
            available = n1 * (n1 - 1) // 2 - e11
            integral_gaps.append(b - available)
            assert b > available
    assert min(integral_gaps) == 244

    positive_size_min = 27
    positive_size_max = energy // 2
    assert positive_size_max == 57

    # Energy lower bounds at a vertex with maximum positive defect M.
    lower_energy = {}
    for maximum in range(1, 11):
        if maximum <= 4:
            lower = (
                maximum * (maximum + 1)
                + (12 - 2 * maximum) * (7 * maximum - 2)
            )
        else:
            lower = maximum * maximum + 15 * maximum - 4
        lower_energy[maximum] = lower

    allowed_maxima = tuple(
        maximum for maximum, lower in lower_energy.items() if lower <= energy
    )
    assert allowed_maxima == (1, 2, 5)
    assert lower_energy == {
        1: 52, 2: 102, 3: 126, 4: 124, 5: 96,
        6: 122, 7: 150, 8: 180, 9: 212, 10: 246,
    }

    canonical_profile = {0: 2, 6: 1, 7: 112, 8: 2737}
    assert sum(canonical_profile.values()) == OUTSIDE
    assert sum(a * n for a, n in canonical_profile.items()) == sum_a
    assert sum(a * a * n for a, n in canonical_profile.items()) == sum_a2

    # The surviving positive-support barrier: weighted K_{1,33}.
    star_energy = 5 * 6 + 33 * 1 * 2
    assert star_energy == 96 < energy
    assert 33 == 7 * 5 - 2
    assert 5 == 7 * 1 - 2

    print("Moore(57,2) 398-coclique deficit-two audit")
    print(f"outside={OUTSIDE} sum_z={sum_z} sum_z2={sum_z2} energy={energy}")
    print(
        "nonpositive nonextension candidate: "
        f"w1={n1} w2={n2}; incidence minimum gap={min(integral_gaps)}"
    )
    print(
        "positive-support obstruction: "
        f"{positive_size_min}<=size<={positive_size_max}, rho>=5"
    )
    print(f"maximum positive defect allowed={allowed_maxima}")
    print("maximum-defect energy bounds=" + ",".join(
        f"{m}:{lower_energy[m]}" for m in sorted(lower_energy)
    ))
    print("canonical extension profile: 0^2 6^1 7^112 8^2737")
    print(
        "barrier: weighted K1,33 positive support consumes "
        f"{star_energy}/114 energy"
    )


if __name__ == "__main__":
    main()
