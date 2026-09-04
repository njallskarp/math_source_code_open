#!/usr/bin/env python3
"""Exact small-case audit for equivariant chain-polytope gamma-effectiveness.

The universal proof is deductive.  This standard-library program checks its
elementary bridges on small bipartite clique blow-ups: gradedness, the
comparability graph, Stanley transfer and inverse transfer, equivariance on
every lattice point, equality of fixed-point Ehrhart counts, and effectiveness
of the resulting gamma characters for elementary abelian 2-groups.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass

Element = tuple[int, int]
Edge = tuple[int, int]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class Case:
    name: str
    nx: int
    ny: int
    sizes: tuple[int, ...]
    edges: frozenset[Edge]

    @property
    def vertices(self) -> range:
        return range(self.nx + self.ny)


def edge_sums(case: Case) -> set[int]:
    return {case.sizes[x] + case.sizes[y] for x, y in case.edges}


def elements(case: Case) -> tuple[Element, ...]:
    return tuple((v, j) for v in case.vertices for j in range(case.sizes[v]))


def less(case: Case, p: Element, q: Element) -> bool:
    """Strict order in the two-level block poset."""
    v, i = p
    w, j = q
    if v == w:
        return i < j
    return v < case.nx <= w and (v, w) in case.edges


def covers(case: Case) -> tuple[tuple[Element, Element], ...]:
    result: list[tuple[Element, Element]] = []
    for v in case.vertices:
        for j in range(case.sizes[v] - 1):
            result.append(((v, j), (v, j + 1)))
    for x, y in sorted(case.edges):
        result.append(((x, case.sizes[x] - 1), (y, 0)))
    return tuple(result)


def maximal_chains(case: Case) -> tuple[tuple[Element, ...], ...]:
    return tuple(
        tuple((x, j) for j in range(case.sizes[x])) + tuple((y, j) for j in range(case.sizes[y]))
        for x, y in sorted(case.edges)
    )


def blowup_edges(case: Case) -> frozenset[frozenset[Element]]:
    elems = elements(case)
    return frozenset(
        frozenset((p, q))
        for p, q in itertools.combinations(elems, 2)
        if p[0] == q[0] or (min(p[0], q[0]), max(p[0], q[0])) in case.edges
    )


def comparability_edges(case: Case) -> frozenset[frozenset[Element]]:
    return frozenset(
        frozenset((p, q))
        for p, q in itertools.combinations(elements(case), 2)
        if less(case, p, q) or less(case, q, p)
    )


def automorphisms(case: Case) -> tuple[Permutation, ...]:
    """Bipartition- and block-size-preserving base automorphisms."""
    result: list[Permutation] = []
    for px in itertools.permutations(range(case.nx)):
        for py0 in itertools.permutations(range(case.ny)):
            py = tuple(case.nx + j for j in py0)
            g = tuple(px) + py
            if any(case.sizes[g[v]] != case.sizes[v] for v in case.vertices):
                continue
            image_edges = frozenset((g[x], g[y]) for x, y in case.edges)
            if image_edges == case.edges:
                result.append(g)
    return tuple(sorted(result))


def element_image(g: Permutation, p: Element) -> Element:
    return (g[p[0]], p[1])


def act_tuple(z: tuple[int, ...], g: Permutation, elems: tuple[Element, ...]) -> tuple[int, ...]:
    index = {p: i for i, p in enumerate(elems)}
    image = [0] * len(elems)
    for i, p in enumerate(elems):
        image[index[element_image(g, p)]] = z[i]
    return tuple(image)


def is_order_point(z: tuple[int, ...], cover_indices: tuple[tuple[int, int], ...]) -> bool:
    return all(z[i] <= z[j] for i, j in cover_indices)


def is_chain_point(
    z: tuple[int, ...], chain_indices: tuple[tuple[int, ...], ...], dilation: int
) -> bool:
    return all(sum(z[i] for i in chain) <= dilation for chain in chain_indices)


def transfer(z: tuple[int, ...], lower_covers: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(z[i] - max((z[j] for j in lower_covers[i]), default=0) for i in range(len(z)))


def inverse_transfer(
    y: tuple[int, ...], lower_covers: tuple[tuple[int, ...], ...]
) -> tuple[int, ...]:
    """Inverse transfer in a supplied topological element order."""
    z: list[int] = []
    for i in range(len(y)):
        if any(j >= i for j in lower_covers[i]):
            raise AssertionError("elements are not topologically ordered")
        z.append(y[i] + max((z[j] for j in lower_covers[i]), default=0))
    return tuple(z)


def poly_mul(a: list[int], b: list[int]) -> list[int]:
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def cycle_lengths(g: Permutation, case: Case) -> list[int]:
    elems = elements(case)
    index = {p: i for i, p in enumerate(elems)}
    perm = tuple(index[element_image(g, p)] for p in elems)
    seen: set[int] = set()
    lengths: list[int] = []
    for start in range(len(perm)):
        if start in seen:
            continue
        cur = start
        length = 0
        while cur not in seen:
            seen.add(cur)
            length += 1
            cur = perm[cur]
        lengths.append(length)
    return sorted(lengths)


def denominator(g: Permutation, case: Case) -> list[int]:
    """det(I-t*(coordinate permutation plus fixed height coordinate))."""
    result = [1, -1]
    for length in cycle_lengths(g, case):
        factor = [0] * (length + 1)
        factor[0] = 1
        factor[length] = -1
        result = poly_mul(result, factor)
    return result


def gamma_from_hstar(hstar: tuple[int, ...], degree: int) -> tuple[int, ...]:
    from math import comb

    gamma: list[int] = []
    for i in range(degree // 2 + 1):
        value = hstar[i]
        for j in range(i):
            value -= gamma[j] * comb(degree - 2 * j, i - j)
        gamma.append(value)
    reconstructed = [0] * (degree + 1)
    for j, value in enumerate(gamma):
        for k in range(degree - 2 * j + 1):
            reconstructed[j + k] += value * comb(degree - 2 * j, k)
    if tuple(reconstructed) != hstar:
        raise AssertionError((hstar, gamma, reconstructed))
    return tuple(gamma)


def compose(g: Permutation, h: Permutation) -> Permutation:
    return tuple(g[h[i]] for i in range(len(g)))


def sign_characters(group: tuple[Permutation, ...]) -> tuple[dict[Permutation, int], ...]:
    """All irreducible characters when the checked group is (C2)^r."""
    identity = tuple(range(len(group[0])))
    if any(compose(g, g) != identity for g in group):
        raise AssertionError("audit group is not elementary abelian")
    if any(compose(g, h) != compose(h, g) for g in group for h in group):
        raise AssertionError("audit group is not abelian")
    chars: list[dict[Permutation, int]] = []
    for values in itertools.product((-1, 1), repeat=len(group)):
        char = dict(zip(group, values, strict=True))
        if char[identity] != 1:
            continue
        if all(char[compose(g, h)] == char[g] * char[h] for g in group for h in group):
            chars.append(char)
    if len(chars) != len(group):
        raise AssertionError((len(chars), len(group)))
    return tuple(chars)


def verify_case(case: Case) -> dict[str, object]:
    sums = edge_sums(case)
    if len(sums) != 1:
        raise AssertionError("test case does not have constant edge sum")
    c = next(iter(sums))
    elems = elements(case)
    index = {p: i for i, p in enumerate(elems)}
    cover_pairs = covers(case)
    cover_indices = tuple((index[p], index[q]) for p, q in cover_pairs)
    lower = tuple(tuple(i for i, j in cover_indices if j == k) for k in range(len(elems)))
    chain_indices = tuple(tuple(index[p] for p in chain) for chain in maximal_chains(case))
    group = automorphisms(case)
    degree = len(elems) - c

    if comparability_edges(case) != blowup_edges(case):
        raise AssertionError("comparability graph is not the clique blow-up")
    if {len(chain) for chain in maximal_chains(case)} != {c}:
        raise AssertionError("poset is not graded with the claimed rank")
    for g in group:
        if any(
            less(case, p, q) != less(case, element_image(g, p), element_image(g, q))
            for p in elems
            for q in elems
        ):
            raise AssertionError("base automorphism does not act on the poset")

    fixed_counts: dict[Permutation, list[int]] = {g: [] for g in group}
    point_totals: list[int] = []
    transfer_checks = 0
    for dilation in range(degree + 2):
        universe = itertools.product(range(dilation + 1), repeat=len(elems))
        order = {z for z in universe if is_order_point(z, cover_indices)}
        chain = {
            z
            for z in itertools.product(range(dilation + 1), repeat=len(elems))
            if is_chain_point(z, chain_indices, dilation)
        }
        image = {transfer(z, lower) for z in order}
        if image != chain:
            raise AssertionError("transfer image differs from chain lattice points")
        if any(inverse_transfer(transfer(z, lower), lower) != z for z in order):
            raise AssertionError("inverse transfer failed")
        point_totals.append(len(order))
        for g in group:
            fixed_order = sum(act_tuple(z, g, elems) == z for z in order)
            fixed_chain = sum(act_tuple(z, g, elems) == z for z in chain)
            if fixed_order != fixed_chain:
                raise AssertionError("fixed-point Ehrhart counts differ")
            fixed_counts[g].append(fixed_order)
            for z in order:
                if transfer(act_tuple(z, g, elems), lower) != act_tuple(
                    transfer(z, lower), g, elems
                ):
                    raise AssertionError("transfer is not equivariant")
                transfer_checks += 1

    hstar: dict[Permutation, tuple[int, ...]] = {}
    gamma: dict[Permutation, tuple[int, ...]] = {}
    for g in group:
        den = denominator(g, case)
        counts = fixed_counts[g]
        coeffs = tuple(
            sum(den[j] * counts[k - j] for j in range(min(k, len(den) - 1) + 1))
            for k in range(degree + 1)
        )
        hstar[g] = coeffs
        gamma[g] = gamma_from_hstar(coeffs, degree)

    irreducibles = sign_characters(group)
    multiplicities: list[list[int]] = []
    for i in range(degree // 2 + 1):
        row: list[int] = []
        for char in irreducibles:
            numerator = sum(gamma[g][i] * char[g] for g in group)
            if numerator % len(group):
                raise AssertionError("nonintegral character multiplicity")
            multiplicity = numerator // len(group)
            if multiplicity < 0:
                raise AssertionError("gamma coefficient is not effective")
            row.append(multiplicity)
        multiplicities.append(sorted(row))

    ordered_group = sorted(group)
    return {
        "name": case.name,
        "dimension": len(elems),
        "rank": c - 1,
        "degree": degree,
        "group_order": len(group),
        "point_totals": point_totals,
        "hstar_values": [hstar[g] for g in ordered_group],
        "gamma_values": [gamma[g] for g in ordered_group],
        "gamma_irrep_multiplicities": multiplicities,
        "transfer_equivariance_checks": transfer_checks,
    }


def structural_scan() -> dict[str, int]:
    total = 0
    graded = 0
    nonuniform_graded = 0
    for nx in (1, 2):
        for ny in (1, 2):
            possible = tuple((x, nx + y) for x in range(nx) for y in range(ny))
            for mask in range(1, 1 << len(possible)):
                edges = frozenset(e for i, e in enumerate(possible) if mask & (1 << i))
                incident = {v for edge in edges for v in edge}
                if incident != set(range(nx + ny)):
                    continue
                for sizes in itertools.product((1, 2), repeat=nx + ny):
                    case = Case("scan", nx, ny, sizes, edges)
                    total += 1
                    chain_lengths = {len(chain) for chain in maximal_chains(case)}
                    constant = len(edge_sums(case)) == 1
                    if (len(chain_lengths) == 1) != constant:
                        raise AssertionError("edge-sum criterion disagrees with gradedness")
                    if constant:
                        graded += 1
                        if len(set(sizes)) > 1:
                            nonuniform_graded += 1
                        if comparability_edges(case) != blowup_edges(case):
                            raise AssertionError("scan comparability failure")
    return {
        "structural_cases": total,
        "graded_cases": graded,
        "nonuniform_graded_cases": nonuniform_graded,
    }


def named_cases() -> tuple[Case, ...]:
    return (
        Case(
            "path3_uniform_a2",
            2,
            1,
            (2, 2, 2),
            frozenset({(0, 2), (1, 2)}),
        ),
        Case(
            "path5_uniform_a1",
            3,
            2,
            (1, 1, 1, 1, 1),
            frozenset({(0, 3), (1, 3), (1, 4), (2, 4)}),
        ),
        Case(
            "cycle4_uniform_a1",
            2,
            2,
            (1, 1, 1, 1),
            frozenset({(0, 2), (0, 3), (1, 2), (1, 3)}),
        ),
        Case(
            "k22_nonuniform_1_2",
            2,
            2,
            (1, 1, 2, 2),
            frozenset({(0, 2), (0, 3), (1, 2), (1, 3)}),
        ),
        Case(
            "matching_nonuniform",
            2,
            2,
            (1, 2, 2, 1),
            frozenset({(0, 2), (1, 3)}),
        ),
    )


def main() -> None:
    report = {
        "structural_scan": structural_scan(),
        "cases": [verify_case(case) for case in named_cases()],
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    scan = report["structural_scan"]
    cases = report["cases"]
    print(
        "VERIFIED equivariant transfer and gamma characters; "
        f"structural_cases={scan['structural_cases']}; "
        f"graded_cases={scan['graded_cases']}; "
        f"nonuniform_graded_cases={scan['nonuniform_graded_cases']}; "
        f"named_cases={len(cases)}; "
        f"group_elements={sum(case['group_order'] for case in cases)}; "
        f"transfer_checks={sum(case['transfer_equivariance_checks'] for case in cases)}; "
        f"sha256={digest}"
    )
    for case in cases:
        print(
            f"{case['name']}: d={case['dimension']} rank={case['rank']} "
            f"degree={case['degree']} |G|={case['group_order']} "
            f"gamma_mult={case['gamma_irrep_multiplicities']}"
        )


if __name__ == "__main__":
    main()
