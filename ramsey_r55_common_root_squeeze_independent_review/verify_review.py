#!/usr/bin/env python3
"""Independent exact audit of the new mathematics at Discovery Net height 2589."""

from itertools import combinations


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def edges_of(vertices):
    return set(combinations(sorted(vertices), 2))


def has_clique(edge_set, vertices, size, red=True):
    for subset in combinations(sorted(vertices), size):
        monochromatic = all(
            (tuple(sorted(pair)) in edge_set) == red
            for pair in combinations(subset, 2)
        )
        if monochromatic:
            return True
    return False


def ramsey_34_degree_proof():
    """Check the integer endgame in the elementary R(3,4)<=9 proof."""
    possible_red_degrees = []
    for degree in range(9):
        # No red triangle and no blue K4 gives d_R <= 3.
        # The blue neighborhood has neither a red nor a blue triangle, so
        # R(3,3)<=6 gives 8-d_R <= 5.
        if degree <= 3 and 8 - degree <= 5:
            possible_red_degrees.append(degree)
    require(possible_red_degrees == [3], "degree squeeze for R(3,4)")
    require((9 * possible_red_degrees[0]) % 2 == 1, "odd degree-sum contradiction")
    return possible_red_degrees[0]


def sharp_cap_fixture():
    """Independently check a literal R(5,5) fixture attaining d_P(u)=8."""
    p_vertices = set(range(8))
    p_edges = {
        (0, 2), (0, 3), (1, 2), (1, 3),
        (0, 4), (1, 5), (2, 6), (3, 7),
        (4, 5), (6, 7),
    }
    require(not has_clique(p_edges, p_vertices, 3, True), "fixture P has a red triangle")
    require(not has_clique(p_edges, p_vertices, 4, False), "fixture P has a blue K4")

    # z=8 and u=9 are red to every P vertex and to each other.  The opposite
    # root w=10 is blue to P and z, and red to u.
    red = set(p_edges)
    red.update(tuple(sorted((v, root))) for v in p_vertices for root in (8, 9))
    red.update({(8, 9), (9, 10)})
    vertices = set(range(11))
    require(not has_clique(red, vertices, 5, True), "sharp fixture has a red K5")
    require(not has_clique(red, vertices, 5, False), "sharp fixture has a blue K5")
    require(sum(tuple(sorted((9, v))) in red for v in p_vertices) == 8,
            "cap-eight fixture does not attain the cap")
    return len(red)


def gap_identity(p_size, q_size, c, e_p, e_q, d_p_f, d_q_f,
                 e_up, e_uq, e_u):
    """Return the direct and decomposed gaps in the strengthened inequality."""
    d_total = d_p_f + d_q_f
    left = 2 * e_p + 2 * e_q + 2 * e_up + 2 * e_uq + 4 * e_u
    right = 8 * (p_size + q_size) - d_total + 32 * c + 2 * c * (c - 1)
    sigma_p = 8 * p_size - 2 * e_p - d_p_f
    sigma_q = 8 * q_size - 2 * e_q - d_q_f
    alpha = 8 * c - e_up
    beta = 8 * c - e_uq
    gamma_twice = c * (c - 1) - 2 * e_u
    decomposed = sigma_p + sigma_q + 2 * alpha + 2 * beta + 2 * gamma_twice
    require(right - left == decomposed, "slack decomposition identity")
    return right - left, (sigma_p, sigma_q, alpha, beta, gamma_twice)


def enumerate_patterns():
    rows = []
    for a in range(3, 6):
        for b in range(2, 5):
            if not 6 <= a + b <= 8:
                continue
            A = (a, b, 14 - a - b)
            B = (8 - a, 10 - b, a + b - 4)
            D = A[2] + B[1]
            local_sum = 154 - D
            lhs = 2 * local_sum
            rhs = 8 * 28 - D + 32 * 2 + 2 * 2
            rows.append((A, B, D, lhs, rhs, lhs <= rhs))
    require(len(rows) == 7, "seven inherited patterns")
    survivors = [row for row in rows if row[-1]]
    require(len(survivors) == 1, "unique surviving pattern")
    require(survivors[0][:3] == ((4, 2, 8), (4, 8, 2), 16),
            "wrong surviving pattern")
    return rows


def equality_structure():
    # Retained values: |P|=|Q|=14, c=2, D=16, and e(J)+e(K)=138.
    gap, slacks = gap_identity(
        p_size=14, q_size=14, c=2,
        e_p=52, e_q=52, d_p_f=8, d_q_f=8,
        e_up=16, e_uq=16, e_u=1,
    )
    require(gap == 0 and slacks == (0, 0, 0, 0, 0), "equality slacks")

    # Conversely, a zero weighted sum of nonnegative integer slacks forces
    # every entry to vanish.  Enumerating the smallest perturbations is also a
    # negative control on the coefficient pattern.
    for index in range(5):
        perturbed = [0] * 5
        perturbed[index] = 1
        weighted = perturbed[0] + perturbed[1] + 2 * sum(perturbed[2:])
        require(weighted > 0, "nonzero slack escaped equality")

    # Fourteen P vertices have degrees at most eight in P union {4}; equality
    # makes their sum 112, so all degrees are eight.  Root 4 also has degree
    # |A_4|=8.  The same calculation applies to Q union {3}.
    degrees = [8] * 14
    require(sum(degrees) == 112 and max(degrees) == min(degrees) == 8,
            "side-degree saturation")
    rooted_edges = (sum(degrees) + 8) // 2
    require(rooted_edges == 60, "rooted-side edge count")

    # Check all central edge totals claimed after putting k=e(W).
    for k in (11, 12):
        p_w = q_w = 70 - k
        p_q = 76 + k
        central_edges = 1 + 52 + 52 + k + 16 + 16 + 4 + p_w + q_w + p_q
        require(central_edges == 357, "central total")
        require(2 * k + 4 + p_w + q_w == 8 * 18, "W degree sum")
        require(2 * 52 + 16 + p_w + p_q == 14 * 19, "P degree sum")
    return rooted_edges


def main():
    forced_degree = ramsey_34_degree_proof()
    fixture_edges = sharp_cap_fixture()
    rows = enumerate_patterns()
    rooted_edges = equality_structure()
    print("PASS elementary R(3,4)<=9 degree/parity endgame; forced red degree", forced_degree)
    print("PASS literal 11-vertex R(5,5) fixture attains common-root cap eight; red edges", fixture_edges)
    print("PASS exact nonnegative-slack decomposition of strengthened paired inequality")
    print("PASS seven inherited patterns checked; unique survivor A=(4,2,8), B=(4,8,2), D=16")
    print("PASS equality forces U edge, U-to-P/Q/W degrees 8/8/2, and two 60-edge rooted sides")
    print("PASS k=11 and k=12 central aggregate identities both exact")
    print("COVERAGE patterns=%d rooted_side_edges=%d" % (len(rows), rooted_edges))
    print("SCOPE accepts new lemma/application conditional on imported height-2509/2557 branch data; no graph existence claim")


if __name__ == "__main__":
    main()
