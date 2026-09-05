#!/usr/bin/env python3
"""Exact arithmetic audit for the sharp 398-coclique star saturation."""

from hashlib import sha256


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
    total_energy = sum_z2 + sum_z
    assert (OUTSIDE, sum_z, sum_z2, total_energy) == (2852, -130, 244, 114)

    center_weight = 5
    leaf_count = 33
    positive_sum = center_weight + leaf_count
    positive_square_sum = center_weight**2 + leaf_count
    positive_energy = center_weight * (center_weight + 1) + 2 * leaf_count
    assert (positive_sum, positive_square_sum, positive_energy) == (38, 58, 96)

    negative_sum = positive_sum - sum_z
    negative_square_sum = sum_z2 - positive_square_sum
    negative_energy = negative_square_sum - negative_sum
    assert (negative_sum, negative_square_sum, negative_energy) == (168, 186, 18)

    s_branches = center_weight + BASE
    zero_branches = (K - (center_weight + BASE)) - leaf_count
    weight_branches = s_branches + zero_branches
    assert (s_branches, zero_branches, weight_branches) == (13, 11, 24)
    assert weight_branches * 7 == negative_sum

    # For a W-vertex of weight r, A_W w=7r+2.  The two-walk inequality is
    #   7(7r+2)+2d <= r*d + (168-7-(7r+2)).
    # Record the least integral d it permits, and compare with 23 branches.
    degree_lower = {}
    for weight in (3, 4):
        neighbour_weight = 7 * weight + 2
        constant_left = 7 * neighbour_weight
        available = negative_sum - 7 - neighbour_weight
        # (weight-2)d >= constant_left-available.
        numerator = constant_left - available
        denominator = weight - 2
        lower = (numerator + denominator - 1) // denominator
        degree_lower[weight] = lower
    assert degree_lower == {3: 23, 4: 40}
    assert degree_lower[3] == weight_branches - 1
    assert degree_lower[4] > weight_branches - 1

    profiles = []
    for n3 in range(4):
        n2 = 9 - 3 * n3
        n1 = 150 + 3 * n3
        assert n1 + 2 * n2 + 3 * n3 == negative_sum
        assert n1 + 4 * n2 + 9 * n3 == negative_square_sum
        profiles.append((n1, n2, n3, n1 + n2 + n3))
    assert profiles == [
        (150, 9, 0, 159),
        (153, 6, 1, 160),
        (156, 3, 2, 161),
        (159, 0, 3, 162),
    ]

    payload = ";".join(
        f"{n1},{n2},{n3},{size}" for n1, n2, n3, size in profiles
    )
    digest = sha256(payload.encode("ascii")).hexdigest()

    print("Moore(57,2) sharp 398-coclique star saturation")
    print(
        f"outside={OUTSIDE} sum_z={sum_z} sum_z2={sum_z2} "
        f"total_energy={total_energy}"
    )
    print(
        f"positive: sum={positive_sum} square_sum={positive_square_sum} "
        f"energy={positive_energy} profile=5^1,1^{leaf_count}"
    )
    print(
        f"negative: sum={negative_sum} square_sum={negative_square_sum} "
        f"energy={negative_energy}"
    )
    print(
        f"Moore branches: S-rooted={s_branches} zero-rooted={zero_branches} "
        f"weight-bearing={weight_branches} weight_each=7"
    )
    print(
        "two-walk degree lower bounds: "
        f"w3={degree_lower[3]} (saturated), "
        f"w4={degree_lower[4]}>{weight_branches - 1} (excluded)"
    )
    for n1, n2, n3, size in profiles:
        print(f"profile: w1={n1} w2={n2} w3={n3} |W|={size}")
    print(f"profile_digest={digest}")


if __name__ == "__main__":
    main()
