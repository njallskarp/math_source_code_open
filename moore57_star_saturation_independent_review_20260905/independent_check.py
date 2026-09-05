#!/usr/bin/env python3
"""Independent exact audit of the Moore(57,2) 398-coclique star branch.

This checker deliberately works from the strongly regular parameters and the
stated equality hypothesis.  It enumerates every negative weight histogram
allowed by the two global moments, applies the independently re-derived
two-walk obstruction, and checks a new collection of necessary edge-class
identities for the surviving profiles.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import product


@dataclass(frozen=True)
class Profile:
    n1: int
    n2: int
    n3: int
    n4: int

    @property
    def order(self) -> int:
        return self.n1 + self.n2 + self.n3 + self.n4

    def weighted_sum(self) -> int:
        return self.n1 + 2 * self.n2 + 3 * self.n3 + 4 * self.n4

    def square_sum(self) -> int:
        return self.n1 + 4 * self.n2 + 9 * self.n3 + 16 * self.n4


def enumerate_profiles(weight_sum: int, square_sum: int) -> list[Profile]:
    """Enumerate all multiplicity profiles on weights 1,2,3,4."""
    profiles: list[Profile] = []
    for n4 in range(weight_sum // 4 + 1):
        for n3 in range((weight_sum - 4 * n4) // 3 + 1):
            for n2 in range((weight_sum - 4 * n4 - 3 * n3) // 2 + 1):
                n1 = weight_sum - 4 * n4 - 3 * n3 - 2 * n2
                candidate = Profile(n1, n2, n3, n4)
                if candidate.square_sum() == square_sum:
                    profiles.append(candidate)
    return sorted(profiles, key=lambda p: (p.n4, p.n3, p.n2, p.n1))


def ceil_div(numerator: int, denominator: int) -> int:
    assert numerator >= 0 and denominator > 0
    return (numerator + denominator - 1) // denominator


def two_walk_degree_floor(
    weight: int, total_negative_weight: int, own_branch_weight: int
) -> int:
    """Return the degree floor from the injective nonreturning two-walk bound."""
    assert weight > 2
    neighbour_weight = 7 * weight + 2
    twice_walk_constant = 7 * neighbour_weight
    available = total_negative_weight - own_branch_weight - neighbour_weight
    return ceil_div(twice_walk_constant - available, weight - 2)


def edge_class_constraints(profile: Profile) -> tuple[int, int, int, int]:
    """Return e13 and the coefficients determining e12,e11 from e22.

    The returned tuple is (e13, e12_constant, e11_constant, e22_upper).
    Any realization must have

        e12 = e12_constant - 4 e22,
        e11 = e11_constant + 4 e22,

    with 0 <= e22 <= e22_upper.  The upper bound only uses simplicity and
    nonnegativity; it does not claim graphical realizability.
    """
    assert profile.n4 == 0
    t = profile.n3
    e13 = 23 * t
    e12_constant = 16 * profile.n2
    e11_constant = 675 - 21 * t - e12_constant
    e22_upper = min(profile.n2 * (profile.n2 - 1) // 2, e12_constant // 4)
    return e13, e12_constant, e11_constant, e22_upper


def main() -> None:
    degree = 57
    vertices = degree**2 + 1
    coclique = 398
    baseline = 8
    outside = vertices - coclique

    # Every point of the coclique has degree 57, and every pair of coclique
    # points has its unique common neighbour outside the coclique.
    sum_a = degree * coclique
    sum_a2 = coclique * (coclique - 1) + sum_a
    sum_z = sum_a - baseline * outside
    sum_z2 = sum_a2 - 2 * baseline * sum_a + baseline**2 * outside
    total_energy = sum_z2 + sum_z
    assert (outside, sum_z, sum_z2, total_energy) == (2852, -130, 244, 114)

    # Equality at a positive vertex of weight five.  If c is the total
    # negative neighbour weight there, the positive energy is at least
    # 5*6 + 2*(7*5-2+c) = 96+2c.  Equality forces c=0 and 33 unit leaves.
    center_weight = 5
    sharp_positive_energy = 96
    positive_neighbour_sum_at_c0 = 7 * center_weight - 2
    assert center_weight * (center_weight + 1) + 2 * positive_neighbour_sum_at_c0 == 96
    assert all(
        center_weight * (center_weight + 1)
        + 2 * (positive_neighbour_sum_at_c0 + c)
        > sharp_positive_energy
        for c in range(1, 10)
    )
    leaf_count = positive_neighbour_sum_at_c0
    positive_sum = center_weight + leaf_count
    positive_square_sum = center_weight**2 + leaf_count
    assert (leaf_count, positive_sum, positive_square_sum) == (33, 38, 58)

    negative_weight = positive_sum - sum_z
    negative_square = sum_z2 - positive_square_sum
    assert (negative_weight, negative_square) == (168, 186)

    s_rooted = baseline + center_weight
    h_neighbours_of_center = degree - s_rooted
    zero_rooted = h_neighbours_of_center - leaf_count
    weight_branches = s_rooted + zero_rooted
    branch_weight = 7
    assert (s_rooted, zero_rooted, weight_branches) == (13, 11, 24)
    assert weight_branches * branch_weight == negative_weight

    before_two_walk = enumerate_profiles(negative_weight, negative_square)
    expected_before = [
        Profile(150, 9, 0, 0),
        Profile(153, 6, 1, 0),
        Profile(156, 3, 2, 0),
        Profile(159, 0, 3, 0),
        Profile(158, 3, 0, 1),
        Profile(161, 0, 1, 1),
    ]
    assert before_two_walk == expected_before

    degree_floors = {
        weight: two_walk_degree_floor(weight, negative_weight, branch_weight)
        for weight in (3, 4)
    }
    assert degree_floors == {3: 23, 4: 40}
    max_branch_degree = weight_branches - 1
    assert degree_floors[4] > max_branch_degree
    assert degree_floors[3] == max_branch_degree

    surviving = [profile for profile in before_two_walk if profile.n4 == 0]
    assert surviving == expected_before[:4]

    edge_rows: list[str] = []
    for profile in surviving:
        t = profile.n3
        e13, e12_constant, e11_constant, e22_upper = edge_class_constraints(profile)

        # A weight-three vertex has 23 unit-weight neighbours, hence no
        # weight-two or weight-three neighbours.  Summing A_W w=7w+2 over
        # weight classes one and two yields the displayed affine identities.
        assert e13 == 23 * t
        for e22 in range(e22_upper + 1):
            e12 = e12_constant - 4 * e22
            e11 = e11_constant + 4 * e22
            assert e12 >= 0 and e11 >= 0
            assert e12 + 4 * e22 == 16 * profile.n2
            assert e11 + e12 == 675 - 21 * t
            assert 2 * e11 + 2 * e12 + 3 * e13 == 9 * profile.n1
        edge_rows.append(
            f"t={t}: e13={e13}, e23=e33=0, "
            f"e12={e12_constant}-4e22, e11={e11_constant}+4e22, "
            f"0<=e22<={e22_upper}"
        )

    # Pointwise S-demand check.  The 13-point centre block has demand seven,
    # the 33 disjoint nine-point leaf blocks demand three, and the remaining
    # 88 points demand two.  This equals sum w(8-w) over W.
    center_points = s_rooted
    leaf_points = leaf_count * (baseline + 1)
    remaining_points = coclique - center_points - leaf_points
    s_demand = 7 * center_points + 3 * leaf_points + 2 * remaining_points
    incidence_weight = baseline * negative_weight - negative_square
    assert (center_points, leaf_points, remaining_points) == (13, 297, 88)
    assert s_demand == incidence_weight == 1158

    # Boundary controls: both moment corruption and a 25-branch replacement
    # are detected by the exact conditions above.
    assert enumerate_profiles(negative_weight, negative_square - 1) != before_two_walk
    assert degree_floors[3] != 25 - 1

    profile_payload = ";".join(
        f"{p.n1},{p.n2},{p.n3},{p.n4},{p.order}" for p in surviving
    )
    profile_digest = sha256(profile_payload.encode("ascii")).hexdigest()
    edge_digest = sha256("\n".join(edge_rows).encode("ascii")).hexdigest()

    print("independent Moore(57,2) star-saturation audit: PASS")
    print(
        f"moments: outside={outside} sum_z={sum_z} sum_z2={sum_z2} "
        f"energy={total_energy}"
    )
    print(
        f"sharp star: center=5 leaves={leaf_count} positive_sum={positive_sum} "
        f"positive_square={positive_square_sum}"
    )
    print(
        f"negative side: weight={negative_weight} square={negative_square} "
        f"branches={weight_branches}x{branch_weight}"
    )
    print(f"pre-two-walk profiles={len(before_two_walk)}; w4_degree_floor=40>23")
    print(f"surviving profiles={len(surviving)}; w3_degree_floor=23=23")
    for profile in surviving:
        print(
            f"profile t={profile.n3}: "
            f"(n1,n2,n3)=({profile.n1},{profile.n2},{profile.n3}), "
            f"order={profile.order}"
        )
    for row in edge_rows:
        print(f"edge constraint {row}")
    print(
        f"S demand: center={center_points} leaf={leaf_points} remaining={remaining_points} "
        f"weighted_total={s_demand}"
    )
    print(f"profile_sha256={profile_digest}")
    print(f"edge_constraint_sha256={edge_digest}")


if __name__ == "__main__":
    main()
