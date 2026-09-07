#!/usr/bin/env python3
"""Third-party exact audit of the 904-dimensional edge moment matrix.

This file deliberately imports no code from the reviewed package.  It expands
the certificate's cell-orbit tables, checks that every one- and two-edge
moment is independent of the padding used to reach four vertices, constructs
an explicit rational basis, and checks the resulting congruence blocks.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, combinations_with_replacement, permutations
import json
import math
from pathlib import Path


PAIR4 = tuple(combinations(range(4), 2))
EXPECTED_CERTIFICATE_SHA256 = (
    "92709ab05f92412d6088ecf357f6ea14690f53c40e87e312d7652dd1b927dbda"
)
EXPECTED_MATRIX_SHA256 = (
    "90ddeed70c602cba2f149c63d25475c3b173651a2eaea03a16ae7541aa294cc9"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def positive_rank(matrix):
    """Exact symmetric elimination, with simultaneous row/column pivoting."""
    a = [[Fraction(x) for x in row] for row in matrix]
    n = len(a)
    require(all(len(row) == n for row in a), "square block")
    require(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
            "symmetric block")
    rank = 0
    for k in range(n):
        positive = next((i for i in range(k, n) if a[i][i] > 0), None)
        if positive is None:
            require(all(a[i][i] == 0 for i in range(k, n)),
                    "negative diagonal in residual")
            require(all(a[i][j] == 0 for i in range(k, n) for j in range(k, n)),
                    "nonzero zero-diagonal residual")
            break
        if positive != k:
            a[k], a[positive] = a[positive], a[k]
            for row in a:
                row[k], row[positive] = row[positive], row[k]
        pivot = a[k][k]
        rank += 1
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return rank


def integer_kernel(rows):
    """Rational RREF nullspace, rescaled to primitive integer vectors."""
    a = [[Fraction(x) for x in row] for row in rows]
    nrows, ncols = len(a), len(a[0])
    pivots = []
    r = 0
    for col in range(ncols):
        found = next((i for i in range(r, nrows) if a[i][col]), None)
        if found is None:
            continue
        a[r], a[found] = a[found], a[r]
        pivot = a[r][col]
        a[r] = [x / pivot for x in a[r]]
        for i in range(nrows):
            if i == r or not a[i][col]:
                continue
            factor = a[i][col]
            a[i] = [x - factor * y for x, y in zip(a[i], a[r])]
        pivots.append(col)
        r += 1
        if r == nrows:
            break
    free = [j for j in range(ncols) if j not in pivots]
    basis = []
    for col in free:
        vector = {col: Fraction(1)}
        for i, pivot in enumerate(pivots):
            if a[i][col]:
                vector[pivot] = -a[i][col]
        scale = math.lcm(*(x.denominator for x in vector.values()))
        integer = {j: int(x * scale) for j, x in vector.items()}
        common = math.gcd(*map(abs, integer.values()))
        integer = {j: x // common for j, x in integer.items()}
        require(all(sum(row[j] * x for j, x in integer.items()) == 0
                    for row in rows), "kernel vector")
        basis.append(integer)
    return len(pivots), basis


def modular_rank(vectors, dimension, prime=1_000_003):
    """Prove full rational rank by one exact nonzero minor modulo a prime."""
    require(prime >= 2 and all(prime % divisor for divisor in range(2, math.isqrt(prime) + 1)),
            "rank modulus is not prime")
    pivots = {}
    for original in vectors:
        row = {j: x % prime for j, x in original.items() if x % prime}
        while row:
            col = min(row)
            if col not in pivots:
                inverse = pow(row[col], -1, prime)
                row = {j: (x * inverse) % prime for j, x in row.items()}
                pivots[col] = row
                break
            factor = row[col]
            pivot = pivots[col]
            for j, x in pivot.items():
                value = (row.get(j, 0) - factor * x) % prime
                if value:
                    row[j] = value
                else:
                    row.pop(j, None)
    require(len(pivots) == dimension, "basis is not full rank modulo prime")
    return len(pivots), prime


class Certificate:
    def __init__(self, path, expected_sha):
        raw_bytes = path.read_bytes()
        self.certificate_sha256 = hashlib.sha256(raw_bytes).hexdigest()
        if expected_sha:
            require(self.certificate_sha256 == expected_sha,
                    "unexpected certificate identity")
        raw = json.loads(raw_bytes)
        require(set(raw) == {"format", "denominator", "cells",
                             "active_selectors", "four_tables"},
                "certificate schema")
        require(raw["format"] == "class-state-orbits-v1", "certificate format")
        self.denominator = raw["denominator"]
        require(type(self.denominator) is int and self.denominator > 0,
                "positive integer denominator")
        self.cells = raw["cells"]
        require(all(type(cell) is list and cell for cell in self.cells),
                "nonempty cells")
        require(sorted(sum(self.cells, [])) == list(range(43)),
                "partition of the 43 physical vertices")
        self.cell_of = {v: i for i, cell in enumerate(self.cells) for v in cell}
        self.tables = {}
        for record in raw["four_tables"]:
            require(set(record) == {"types", "orbits"}, "table schema")
            types = tuple(record["types"])
            require(types == tuple(sorted(types)) and len(types) == 4,
                    "canonical four-type tuple")
            require(types not in self.tables, "duplicate four-type table")
            distribution = {}
            preserving = [p for p in permutations(range(4))
                          if all(types[p[i]] == types[i] for i in range(4))]
            for text, mass in record["orbits"].items():
                require(type(mass) is int and 0 < mass <= self.denominator,
                        "positive integer orbit mass")
                state = int(text)
                require(str(state) == text and 0 <= state < 64,
                        "canonical state encoding")
                edges = {PAIR4[j] for j in range(6) if state >> j & 1}
                orbit = set()
                for p in preserving:
                    image = {tuple(sorted((p[a], p[b]))) for a, b in edges}
                    orbit.add(sum(1 << PAIR4.index(edge) for edge in image))
                require(state == min(orbit), "noncanonical orbit representative")
                require(not (set(distribution) & orbit), "overlapping state orbits")
                distribution.update({image: mass for image in orbit})
            require(sum(distribution.values()) == self.denominator,
                    "four-table normalization")
            self.tables[types] = distribution
        expected = {
            types for types in combinations_with_replacement(range(len(self.cells)), 4)
            if all(types.count(i) <= len(self.cells[i]) for i in set(types))
        }
        require(set(self.tables) == expected, "complete feasible four-type support")
        self.event_cache = {}
        self.moment_cache = {}
        self.coordinates = [()] + list(combinations(range(43), 2))
        self.coordinate_index = {edge: i for i, edge in enumerate(self.coordinates)}

    def event_on_four(self, vertices, required_edges):
        require(len(vertices) == 4 and len(set(vertices)) == 4,
                "four distinct physical vertices")
        ordered = sorted(vertices, key=lambda v: (self.cell_of[v], v))
        types = tuple(self.cell_of[v] for v in ordered)
        positions = {v: i for i, v in enumerate(ordered)}
        required_mask = 0
        for edge in required_edges:
            pair = tuple(sorted((positions[edge[0]], positions[edge[1]])))
            required_mask |= 1 << PAIR4.index(pair)
        key = (types, required_mask)
        if key not in self.event_cache:
            self.event_cache[key] = sum(
                mass for state, mass in self.tables[types].items()
                if state & required_mask == required_mask
            )
        return self.event_cache[key]

    def event(self, required_edges, completion=None):
        required = tuple(sorted(set(required_edges)))
        vertices = set(sum(required, ()))
        if completion is None:
            completion = (v for v in range(43) if v not in vertices)
        for v in completion:
            if len(vertices) == 4:
                break
            require(v not in vertices, "completion repeats a vertex")
            vertices.add(v)
        require(len(vertices) == 4, "event completion")
        return self.event_on_four(tuple(vertices), required)

    def moment(self, i, j):
        if i > j:
            i, j = j, i
        key = (i, j)
        if key not in self.moment_cache:
            if i == 0 and j == 0:
                value = self.denominator
            else:
                required = [self.coordinates[k] for k in (i, j) if k]
                value = self.event(required)
            self.moment_cache[key] = value
        return self.moment_cache[key]

    def check_padding(self):
        checks = 0
        vertices = set(range(43))
        for edge in self.coordinates[1:]:
            expected = self.event([edge])
            outside = sorted(vertices - set(edge))
            for a, b in combinations(outside, 2):
                require(self.event_on_four(edge + (a, b), [edge]) == expected,
                        "one-edge marginal depends on padding")
                checks += 1
        for triple in combinations(range(43), 3):
            triangle_edges = list(combinations(triple, 2))
            for required in combinations(triangle_edges, 2):
                expected = self.event(required)
                for filler in sorted(vertices - set(triple)):
                    require(self.event_on_four(triple + (filler,), required) == expected,
                            "two-adjacent-edge marginal depends on padding")
                    checks += 1
        require(checks == 2_221_380, "padding-check census")
        return checks


def dot(left, right):
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(index, 0) for index, value in left.items())


def audit(certificate):
    coordinates = certificate.coordinates
    index = certificate.coordinate_index
    cell_of = certificate.cell_of

    def bilinear(left, right):
        return sum(a * b * certificate.moment(i, j)
                   for i, a in left.items() for j, b in right.items())

    groups = defaultdict(list)
    for i, edge in enumerate(coordinates):
        key = () if not edge else tuple(sorted(cell_of[v] for v in edge))
        groups[key].append(i)
    require(len(groups) == 43, "43 cell-pair coordinate orbits")

    families = []
    constant_vectors = [{i: 1 for i in group} for group in groups.values()]
    families.append(("constant", constant_vectors, None))

    for cell_index, cell in enumerate(certificate.cells):
        if len(cell) < 2:
            continue
        labels = [j for j in range(len(certificate.cells))
                  if j != cell_index or len(cell) >= 3]
        vectors = []
        base = cell[0]
        for other_vertex in cell[1:]:
            for label in labels:
                vector = Counter()
                for vertex, sign in ((base, 1), (other_vertex, -1)):
                    for w in certificate.cells[label]:
                        if w != vertex:
                            vector[index[tuple(sorted((vertex, w)))]] += sign
                vectors.append({i: x for i, x in vector.items() if x})
        families.append((f"standard-{cell_index}", vectors,
                         (len(cell) - 1, len(labels))))

    for cell_index, cell in enumerate(certificate.cells):
        if len(cell) < 4:
            continue
        edges = list(combinations(cell, 2))
        rows = [[int(vertex in edge) for edge in edges] for vertex in cell]
        incidence_rank, local = integer_kernel(rows)
        require(incidence_rank == len(cell), "signless incidence rank")
        require(len(local) == len(cell) * (len(cell) - 3) // 2,
                "internal residual dimension")
        vectors = [{index[edges[j]]: x for j, x in vector.items()}
                   for vector in local]
        families.append((f"internal-{cell_index}", vectors, None))

    for i, j in combinations(range(len(certificate.cells)), 2):
        if min(len(certificate.cells[i]), len(certificate.cells[j])) < 2:
            continue
        a, b = certificate.cells[i][0], certificate.cells[j][0]
        vectors = []
        for u in certificate.cells[i][1:]:
            for v in certificate.cells[j][1:]:
                vector = {
                    index[tuple(sorted((a, b)))]: 1,
                    index[tuple(sorted((a, v)))]: -1,
                    index[tuple(sorted((u, b)))]: -1,
                    index[tuple(sorted((u, v)))]: 1,
                }
                vectors.append(vector)
        families.append((f"tensor-{i}-{j}", vectors, None))

    all_vectors = [vector for _, vectors, _ in families for vector in vectors]
    require(len(all_vectors) == 904, "explicit basis cardinality")
    modular_dimension, prime = modular_rank(all_vectors, 904)

    rank = 0
    block_records = []
    for name, vectors, shape in families:
        if name == "constant":
            block = [[bilinear(v, w) for w in vectors] for v in vectors]
            block_rank = positive_rank(block)
            rank += block_rank
            block_records.append({"family": name, "dimension": len(vectors),
                                  "coefficient_rank": block_rank})
        elif name.startswith("standard-"):
            differences, labels = shape
            require(len(vectors) == differences * labels, "standard family shape")
            coefficient = []
            for j in range(labels):
                row = []
                for k in range(labels):
                    value = bilinear(vectors[j], vectors[k])
                    require(value % 2 == 0, "standard normalization parity")
                    row.append(value // 2)
                coefficient.append(row)
            block_rank = positive_rank(coefficient)
            for t in range(differences):
                for s in range(differences):
                    vertex_gram = 2 if t == s else 1
                    for j in range(labels):
                        for k in range(labels):
                            require(
                                bilinear(vectors[t * labels + j],
                                         vectors[s * labels + k])
                                == vertex_gram * coefficient[j][k],
                                "standard congruence block",
                            )
            rank += differences * block_rank
            block_records.append({"family": name, "dimension": len(vectors),
                                  "coefficient_rank": block_rank,
                                  "multiplicity": differences})
        else:
            norm = dot(vectors[0], vectors[0])
            eigenvalue = Fraction(bilinear(vectors[0], vectors[0]), norm)
            require(eigenvalue >= 0, "negative residual scalar")
            for v in vectors:
                for w in vectors:
                    require(bilinear(v, w) == eigenvalue * dot(v, w),
                            "residual scalar congruence")
            if eigenvalue > 0:
                rank += len(vectors)
            block_records.append({"family": name, "dimension": len(vectors),
                                  "positive": eigenvalue > 0})

    cross_checks = 0
    for a, (_, left, _) in enumerate(families):
        for _, right, _ in families[a + 1:]:
            for v in left:
                for w in right:
                    require(bilinear(v, w) == 0, "nonzero cross-family block")
                    cross_checks += 1
    require(cross_checks == 378_821, "cross-family census")
    require(rank == 740, "global matrix rank")

    digest = hashlib.sha256(f"904 {certificate.denominator}\n".encode())
    for i in range(904):
        row = " ".join(str(certificate.moment(i, j)) for j in range(904))
        digest.update((row + "\n").encode())
    matrix_sha256 = digest.hexdigest()
    require(matrix_sha256 == EXPECTED_MATRIX_SHA256, "complete matrix identity")

    return {
        "status": "INDEPENDENT_CONGRUENCE_PSD_PASS",
        "certificate_sha256": certificate.certificate_sha256,
        "matrix_sha256": matrix_sha256,
        "matrix_order": 904,
        "matrix_rank": rank,
        "basis_vectors": len(all_vectors),
        "basis_rank_mod_prime": modular_dimension,
        "basis_rank_prime": prime,
        "padding_independence_checks": certificate.check_padding(),
        "cross_family_zero_checks": cross_checks,
        "block_records": block_records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--expected-certificate-sha256",
                        default=EXPECTED_CERTIFICATE_SHA256)
    args = parser.parse_args()
    certificate = Certificate(args.certificate, args.expected_certificate_sha256)
    print(json.dumps(audit(certificate), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
