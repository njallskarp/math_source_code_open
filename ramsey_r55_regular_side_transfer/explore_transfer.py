#!/usr/bin/env python3
"""Discover exact cell-count witnesses avoiding every exceptional-root side of order 15/16.

SciPy is used only to discover integer witnesses.  The eventual certificate is
checked separately with standard-library exact arithmetic.
"""

from argparse import ArgumentParser
from collections import Counter
import csv
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_array, csr_array, vstack


B = {18: 220, 19: 221, 20: 220, 21: 220, 22: 221, 23: 223, 24: 223}
REMOVED = {"0,1,3,39,0,0,0", "0,2,3,38,0,0,0"}
SOURCE_PINS = {
    "ramsey_r55_exceptional_degree_sieve/PROFILES.tsv":
        "a8bd3a7def8d719947e74601f410255856a309e7f66af0ee16227370b9a4f3fa",
    "ramsey_r55_exceptional_signature_capacity/CENSUS.tsv":
        "08a4a09b677031faf9dc7c7dc403e8e06e3245e39d13ca260b251a5c34ed5363",
    "ramsey_r55_coupled_signature_counts/SUMMARY.tsv":
        "cce4476cf875ff5d086a2f4fe3a830ddd6ba74e119cb4f9e049f14bfd2f3c511",
    "ramsey_r55_signature_union_cuts/SUMMARY.tsv":
        "286258e842b2272da7787e74be41db6ac5f5b26921777202deff699a81143ffa",
}


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


@lru_cache(None)
def upper(a, b):
    if min(a, b) == 1:
        return 1
    p, q = upper(a - 1, b), upper(a, b - 1)
    return p + q - int(p % 2 == q % 2 == 0)


def read_rows(path):
    with path.open() as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def surviving_profiles(source):
    source = Path(source)
    for relative, digest in SOURCE_PINS.items():
        require(sha256((source / relative).read_bytes()).hexdigest() == digest,
                f"pinned campaign input {relative}")
    globals_ = read_rows(source / "ramsey_r55_exceptional_degree_sieve/PROFILES.tsv")
    marginal = read_rows(source / "ramsey_r55_exceptional_signature_capacity/CENSUS.tsv")
    coupled = read_rows(source / "ramsey_r55_coupled_signature_counts/SUMMARY.tsv")
    union = read_rows(source / "ramsey_r55_signature_union_cuts/SUMMARY.tsv")
    excluded = {row["counts_18_to_24"] for row in marginal if not int(row["pass"])}
    excluded |= {row["counts_18_to_24"] for row in coupled if not int(row["primal_cores"])}
    excluded |= {row["counts_18_to_24"] for row in union if not int(row["primal_cores"])}
    excluded |= REMOVED
    rows = [row for row in globals_ if row["status"] == "feasible" and row["counts_18_to_24"] not in excluded]
    require(len(rows) == 66 and sum(int(row["split_count"]) for row in rows) == 271,
            "authoritative 66/271 survivor list")
    return rows


def degree_list(row):
    counts = tuple(map(int, row["counts_18_to_24"].split(",")))
    return tuple(d for d, count in zip(range(18, 25), counts) if d != 21 for _ in range(count))


def core_constraints(ds, M, exclusions):
    k = len(ds)
    eps = tuple(d - 21 for d in ds)
    edges = tuple(combinations(range(k), 2))
    rows, lower, upper_bounds = [], [], []

    for vertex, degree in enumerate(ds):
        rows.append([eps[b] if a == vertex else eps[a] if b == vertex else 0 for a, b in edges])
        lower.append(-np.inf)
        upper_bounds.append(M - B[degree])

    central_constant = sum(e * d for e, d in zip(eps, ds))
    rows.append([eps[a] + eps[b] for a, b in edges])
    lower.append(central_constant - (43 - k) * (M - 220))
    upper_bounds.append(np.inf)

    for subset in combinations(range(k), 5):
        chosen = set(subset)
        row = [int(a in chosen and b in chosen) for a, b in edges]
        rows.append(row)
        lower.append(1)
        upper_bounds.append(9)

    for mask in exclusions:
        ones = mask.bit_count()
        rows.append([1 if mask >> index & 1 else -1 for index in range(len(edges))])
        lower.append(-np.inf)
        upper_bounds.append(ones - 1)

    matrix = np.array(rows, dtype=float) if rows else np.empty((0, len(edges)))
    return edges, LinearConstraint(matrix, np.array(lower), np.array(upper_bounds))


def solve_core(ds, M, exclusions, seed):
    edges, constraints = core_constraints(ds, M, exclusions)
    if not edges:
        return 0
    rng = np.random.default_rng(seed)
    objective = rng.integers(-1000, 1001, size=len(edges)).astype(float)
    result = milp(objective, integrality=np.ones(len(edges)), bounds=Bounds(0, 1),
                  constraints=constraints, options={"time_limit": 20})
    if not result.success:
        return None
    values = [round(value) for value in result.x]
    require(all(value in (0, 1) and abs(result.x[i] - value) < 1e-6 for i, value in enumerate(values)),
            "binary core solution")
    return sum(value << index for index, value in enumerate(values))


def adjacency(k, mask):
    adj = [0] * k
    for index, (a, b) in enumerate(combinations(range(k), 2)):
        if mask >> index & 1:
            adj[a] |= 1 << b
            adj[b] |= 1 << a
    return tuple(adj)


def subset_tables(adj):
    k = len(adj)
    full = (1 << k) - 1
    omega, alpha, red, blue = [0] * (1 << k), [0] * (1 << k), [False] * (1 << k), [False] * (1 << k)
    red[0] = blue[0] = True
    for mask in range(1, 1 << k):
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        rest = mask ^ bit
        omega[mask] = max(omega[rest], 1 + omega[rest & adj[vertex]])
        alpha[mask] = max(alpha[rest], 1 + alpha[rest & (full ^ adj[vertex] ^ (1 << vertex))])
        red[mask] = red[rest] and rest & ~adj[vertex] == 0
        blue[mask] = blue[rest] and rest & adj[vertex] == 0
    return omega, alpha, red, blue


def signature_data(adj, ds, M):
    k = len(ds)
    n = 43 - k
    full = (1 << k) - 1
    omega, alpha, red, blue = subset_tables(adj)
    require(omega[full] < 5 and alpha[full] < 5, "core Ramsey property")
    xs, caps = [], []
    for mask in range(1 << k):
        if sum(ds[i] - 21 for i in range(k) if mask >> i & 1) > M - 220:
            continue
        r, s = omega[mask], alpha[full ^ mask]
        if r >= 4 or s >= 4:
            continue
        xs.append(mask)
        caps.append(min(n, upper(5 - r, 5 - s) - 1))
    return tuple(xs), tuple(caps), red, blue


def exceptional_side_size(adj, values, xs, i, j):
    fixed = sum(h not in (i, j) and bool(adj[i] >> h & 1) and not bool(adj[j] >> h & 1)
                for h in range(len(adj)))
    central = sum(value for mask, value in zip(xs, values) if mask >> i & 1 and not (mask >> j & 1))
    return fixed + central


def union_rows(adj, xs, red, blue):
    k = len(adj)
    full = (1 << k) - 1
    index = {mask: column for column, mask in enumerate(xs)}
    row_indices, columns, data, rhs, roots = [], [], [], [], []
    row_number = 0
    red_roots = [mask for mask, valid in enumerate(red) if valid]
    blue_roots = [mask for mask, valid in enumerate(blue) if valid]
    for a in red_roots:
        for b in blue_roots:
            if a & b or not (a | b):
                continue
            outside = full ^ (a | b)
            common = sum(
                bool(adj[vertex] & a == a and not (adj[vertex] & b))
                for vertex in range(k)
                if outside >> vertex & 1
            )
            bound = upper(5 - a.bit_count(), 5 - b.bit_count()) - 1 - common
            require(bound >= 0, "exceptional common-neighborhood overflow")
            free = outside
            sub = free
            while True:
                mask = a | sub
                if mask in index:
                    row_indices.append(row_number)
                    columns.append(index[mask])
                    data.append(1)
                if sub == 0:
                    break
                sub = (sub - 1) & free
            rhs.append(bound)
            roots.append((a, b))
            row_number += 1
    matrix = coo_array((data, (row_indices, columns)), shape=(row_number, len(xs)), dtype=float).tocsr()
    return matrix, np.array(rhs, dtype=float), roots


def solve_cells(adj, ds, M, seed, side_limit=14):
    k, n = len(ds), 43 - len(ds)
    xs, caps, red, blue = signature_data(adj, ds, M)
    target = [n] + [degree - adj[i].bit_count() for i, degree in enumerate(ds)]
    eq_rows = [[1] * len(xs)] + [[int(mask >> i & 1) for mask in xs] for i in range(k)]
    equality = csr_array(np.array(eq_rows, dtype=float))

    union_matrix, union_rhs, roots = union_rows(adj, xs, red, blue)
    side_rows, side_rhs, pairs = [], [], []
    for i in range(k):
        for j in range(k):
            if i == j:
                continue
            fixed = sum(h not in (i, j) and bool(adj[i] >> h & 1) and not bool(adj[j] >> h & 1)
                        for h in range(k))
            if side_limit is not None:
                side_rows.append([int(mask >> i & 1 and not (mask >> j & 1)) for mask in xs])
                side_rhs.append(side_limit - fixed)
            pairs.append((i, j))
    side_matrix = csr_array(np.array(side_rows, dtype=float)) if side_rows else csr_array((0, len(xs)))
    matrix = vstack((equality, union_matrix, side_matrix), format="csr")
    lower = np.concatenate((np.array(target, dtype=float), np.full(len(union_rhs) + len(side_rhs), -np.inf)))
    upper_bounds = np.concatenate((np.array(target, dtype=float), union_rhs, np.array(side_rhs, dtype=float)))
    rng = np.random.default_rng(seed)
    objective = rng.integers(-1000, 1001, size=len(xs)).astype(float)
    result = milp(objective, integrality=np.ones(len(xs)), bounds=Bounds(0, np.array(caps, dtype=float)),
                  constraints=LinearConstraint(matrix, lower, upper_bounds), options={"time_limit": 30})
    if not result.success:
        return None
    values = [round(value) for value in result.x]
    require(all(0 <= value <= cap and abs(result.x[i] - value) < 1e-6
                for i, (value, cap) in enumerate(zip(values, caps))), "integral cell solution")
    require(list(equality @ np.array(values)) == target, "cell margins")
    require(all(left <= right for left, right in zip(union_matrix @ np.array(values), union_rhs)), "union cuts")
    side_sizes = [exceptional_side_size(adj, values, xs, i, j) for i, j in pairs]
    if side_limit is not None:
        require(all(size <= side_limit for size in side_sizes), "regular-side nonactivation")
    return {
        "cells": [[mask, value] for mask, value in zip(xs, values) if value],
        "eligible_signatures": len(xs),
        "union_cuts": len(roots),
        "maximum_exceptional_root_side": max(side_sizes, default=0),
        "side_size_histogram": dict(sorted(Counter(side_sizes).items())),
    }


def solve_profile(row, index, attempts):
    ds = degree_list(row)
    M = int(row["M"])
    excluded = []
    for attempt in range(attempts):
        seed = 1000003 * (index + 1) + 7919 * attempt
        core = solve_core(ds, M, excluded, seed)
        if core is None:
            break
        adj = adjacency(len(ds), core)
        witness = solve_cells(adj, ds, M, seed + 1)
        if witness is not None:
            return {
                "counts_18_to_24": row["counts_18_to_24"],
                "M": M,
                "split_count": int(row["split_count"]),
                "exceptional_degrees": list(ds),
                "core_mask": core,
                **witness,
            }
        excluded.append(core)
    return None


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="pinned math-results checkout")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--attempts", type=int, default=20)
    parser.add_argument("--only", help="exact counts_18_to_24 row")
    parser.add_argument("--two-degree19", action="store_true",
                        help="select the five remaining profiles with exactly two degree-19 vertices")
    args = parser.parse_args()

    profiles = surviving_profiles(args.source)
    if args.only:
        profiles = [row for row in profiles if row["counts_18_to_24"] == args.only]
        require(len(profiles) == 1, "selected profile")
    if args.two_degree19:
        profiles = [row for row in profiles if row["counts_18_to_24"].split(",")[1] == "2"]
        require(len(profiles) == 5, "five-row double-degree-19 family")
    records = []
    for index, row in enumerate(profiles):
        record = solve_profile(row, index, args.attempts)
        if record is None:
            print(f"FAIL {row['counts_18_to_24']} M={row['M']}", flush=True)
            continue
        records.append(record)
        print(f"PASS {record['counts_18_to_24']} M={record['M']} k={len(record['exceptional_degrees'])} "
              f"side_max={record['maximum_exceptional_root_side']} union={record['union_cuts']}", flush=True)
    document = {
        "format": "r55-exceptional-root-regular-side-transfer-v1",
        "profiles_requested": len(profiles),
        "profiles_with_witness": len(records),
        "scope": "integer core/signature/union relaxation with every exceptional-root one-way side at most fourteen",
        "records": records,
    }
    if args.output:
        args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    require(len(records) == len(profiles), "not every requested profile has a witness")


if __name__ == "__main__":
    main()
