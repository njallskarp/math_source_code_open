#!/usr/bin/env python3
"""Independent exact arithmetic and coverage audit. Imports no target code.

Inputs: the two public rational certificates, case manifests, and optionally
fresh replay directories. See README.md for the mathematical trust boundary.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def check(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def types_and_edges():
    sizes = (17, 24, 13)
    ts = sorted((d, (a, b, d-a-b))
                for d in (6, 7, 8) for a in range(d+1)
                for b in range(d-a+1)
                if 6*a+7*b+8*(d-a-b) <= 53
                and all(x <= sizes[j]-(d == j+6)
                        for j, x in enumerate((a, b, d-a-b))))
    es = [(i, j) for i in range(len(ts)) for j in range(i, len(ts))
          if ts[i][1][ts[j][0]-6] > 0 and ts[j][1][ts[i][0]-6] > 0]
    check((len(ts), len(es)) == (72, 1638), "type/edge domain")
    return ts, es


def certificate(source, upper):
    """Rebuild each matrix COLUMN from the mathematical counting equations."""
    ts, es = types_and_edges()
    sizes = (17, 24, 13)
    pairs = list(combinations(range(3), 2))
    name = "forest_degree2_certificate.json" if upper else "forest_lower_certificate.json"
    data = json.loads((source/name).read_text())
    denominator = data["denominator"]
    check(type(denominator) is int and denominator > 0, "denominator")
    multipliers = []
    for field, nrows in (("equality_multipliers", 222),
                         ("inequality_multipliers", 224 if upper else 222)):
        values = [0]*nrows
        seen = set()
        for i, numerator in data[field]:
            check(type(i) is int and 0 <= i < nrows and i not in seen, "row index")
            check(type(numerator) is int, "integer numerator")
            if field.startswith("inequality"):
                check(numerator <= 0, "wrong inequality sign")
            seen.add(i)
            values[i] = numerator
        multipliers.append(values)
    e, u = multipliers
    # Only the first three equalities and first six inequalities have
    # nonzero right-hand sides, apart from the optional -m<=-5, m<=6.
    bound_numerator = sum(e[j]*sizes[j] for j in range(3))
    bound_numerator += sum(u[j]*sizes[j]*(sizes[j]-1) for j in range(3))
    bound_numerator += sum(u[3+r]*sizes[a]*sizes[b]
                           for r, (a, b) in enumerate(pairs))
    if upper:
        bound_numerator += -5*u[222]+6*u[223]
    errors = []
    for i, (d, ns) in enumerate(ts):
        value = Q(e[d-6])
        for r, (a, b) in enumerate(pairs):
            value += e[3+r]*((d == a+6)*ns[b]-(d == b+6)*ns[a])
        for a in range(3):
            value += u[a]*(ns[a]*(ns[a]-1)+(d == a+6)*ns[a])
            value -= e[6+3*i+a]*ns[a]
            value += u[6+3*i+a]*(ns[a]-sizes[a]-(d-1)*(d == a+6))
        for r, (a, b) in enumerate(pairs):
            value += u[3+r]*(ns[a]*ns[b]+(d == a+6)*ns[b])
        m = Q(ns[2], 2) if d == 8 else Q(0)
        if upper:
            value += (u[223]-u[222])*m
        objective = -m-int(d == 8 and ns[2] == 2) if upper else m
        allowed = d != 8 or ns[1]+2*ns[2] == 5
        errors.append(value/denominator-objective if allowed else Q(0))
    for i, j in es:
        value = e[6+3*i+ts[j][0]-6]
        value += sum(u[6+3*i+a]*ts[j][1][a] for a in range(3))
        if i != j:
            value += e[6+3*j+ts[i][0]-6]
            value += sum(u[6+3*j+a]*ts[i][1][a] for a in range(3))
        errors.append(Q(value, denominator))
    error = max([Q(0)]+errors)
    bound = Q(bound_numerator, denominator)
    corrected = bound-428*error
    check(str(bound) == data["uncorrected_bound"], "uncorrected bound")
    check(str(error) == data["max_coefficient_error"], "coefficient excess")
    check(str(corrected) == data["corrected_bound"], "corrected bound")
    check(corrected > (-9 if upper else 4), "integer threshold")
    # Independent, slightly sharper error payment from the separate budgets.
    grouped = bound-54*max([Q(0)]+errors[:72])-374*max([Q(0)]+errors[72:])
    check(grouped >= corrected, "grouped payment")
    return {"objective": "-(m+k)" if upper else "m", "bound": str(bound),
            "delta": str(error), "corrected": str(corrected),
            "separate_budget_bound": str(grouped)}


def high_histograms(d, n, total, budget):
    """Enumerate nondecreasing lists of c-values, not the author's deficit split."""
    answer = set()
    costs = [(c-3)*(c-4)//2 if d == 6 else (c-1)*(c-2)//2
             for c in range(d+1)]

    def visit(first, remaining, moment, cost, counts):
        if not remaining:
            if moment == 0:
                answer.add((cost, tuple(counts)))
            return
        if moment < first*remaining or moment > d*remaining:
            return
        if cost+remaining*min(costs[first:]) > budget:
            return
        for c in range(first, min(d, moment//remaining)+1):
            new_cost = cost+costs[c]
            if new_cost <= budget:
                counts[c] += 1
                visit(c, remaining-1, moment-c, new_cost, counts)
                counts[c] -= 1
    visit(0, n, total, 0, [0]*(d+1))
    return answer


def forest_cover(source):
    # Enumerate all integer partitions of 13 vertices, allowing cycles as
    # components initially; short cycles are excluded by girth.
    def partitions(n, least=1):
        if n == 0:
            yield ()
        for a in range(least, n+1):
            for tail in partitions(n-a, a):
                yield (a,)+tail
    paths = set()
    cyclic_survivors = 0
    for sizes in partitions(13):
        cycle_eligible = [i for i, a in enumerate(sizes) if a >= 5]
        for mask in range(1 << len(cycle_eligible)):
            cycles = {i for j, i in enumerate(cycle_eligible) if mask >> j & 1}
            m = sum(a if i in cycles else a-1 for i, a in enumerate(sizes))
            k = sum(a if i in cycles else max(0, a-2) for i, a in enumerate(sizes))
            if 5 <= m <= 6 and m+k <= 8:
                if cycles:
                    cyclic_survivors += 1
                else:
                    paths.add(tuple(sorted((a for a in sizes if a > 1), reverse=True)))
    named = {"5_0": (2,)*5, "5_1": (3,2,2,2), "5_2a": (4,2,2),
             "5_2b": (3,3,2), "5_3a": (5,2), "5_3b": (4,3),
             "6_0": (2,)*6, "6_1": (3,2,2,2,2),
             "6_2a": (4,2,2,2), "6_2b": (3,3,2,2)}
    check(cyclic_survivors == 0 and paths == set(named.values()), "forest domain")
    counts = {}
    histograms = {}
    for lengths in sorted(paths):
        m, k = sum(a-1 for a in lengths), sum(a-2 for a in lengths)
        if (m, k) in histograms:
            continue
        D = 22-3*m-k
        a = high_histograms(6, 17, 39+2*m, D)
        b = high_histograms(7, 24, 65-4*m, D)
        rows = sorted((x,y) for q,x in a for r,y in b if q+r == D)
        histograms[m,k] = rows
        counts[f"{m},{k}"] = len(rows)
    excluded = {"5_3a", "5_3b", "6_2a"}
    manifest = json.loads((source/"forest_expected.json").read_text())
    check(set(manifest["excluded_forests"]) == excluded, "excluded names")
    expected_cases = {f"{name}_{i}" for name in excluded
                      for i in range(len(histograms[sum(a-1 for a in named[name]),
                                                   sum(a-2 for a in named[name])]))}
    check({c["case"] for c in manifest["cases"]} == expected_cases
          and len(manifest["cases"]) == 22, "complete case manifest")
    total = sum(len(histograms[sum(a-1 for a in L),sum(a-2 for a in L)])
                for L in named.values())
    check(total == 173, "profile total")
    record = {f"{m},{k}": rows for (m,k), rows in sorted(histograms.items())}
    return {"forests": 10, "cyclic_survivors": 0, "profiles": counts,
            "total_forest_profiles": total, "excluded_cases": 22,
            "remaining_cases": total-22, "remaining_forests": sorted(set(named)-excluded),
            "sorted_histograms_sha256": sha256(json.dumps(record, sort_keys=True,
                separators=(",", ":")).encode()).hexdigest()}


def replay_check(source, work, family):
    """Validate fresh receipts AND actual formulas, traces and checker logs."""
    filename = "forest_expected.json" if family == "forest" else "seven_edge_expected.json"
    manifest = json.loads((source/filename).read_text())["cases"]
    actual = json.loads((work/"validation.json").read_text())
    records = {r["case"]: r for r in actual["cases"]}
    n = 22 if family == "forest" else 50
    check(len(records) == len(actual["cases"]) == len(manifest) == n, "replay size")
    check(actual["verified_unsat"] == n, "replay coverage")
    proof_matches = 0
    rows = []
    for expected in manifest:
        name = expected["case"]
        row = records[name]
        check(row["status"] == "UNSAT" and row["checker_status"] == "VERIFIED", "status")
        formula_hash = digest(work/(name+".cnf"))
        proof_hash = digest(work/(name+".drup"))
        check(formula_hash == expected["cnf_sha256"] == row["cnf_sha256"], "CNF hash")
        check(proof_hash == row["proof_sha256"], "proof receipt")
        check("s VERIFIED" in (work/(name+"_check.txt")).read_text(), "checker log")
        proof_matches += proof_hash == expected["drup_sha256"]
        check(row["variables"] == expected["variables"]
              and row["clauses"] == expected["clauses"], "formula sizes")
        rows.append([name, formula_hash, proof_hash])
    return {"verified_cases": n, "matching_CNF_hashes": n,
            "matching_historical_proof_hashes": proof_matches,
            "case_hashes_sha256": sha256(json.dumps(sorted(rows),
                separators=(",", ":")).encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--forest-replay", type=Path)
    parser.add_argument("--seven-replay", type=Path)
    args = parser.parse_args()
    manifest = Path(__file__).with_name("TARGET_SHA256SUMS")
    for line in manifest.read_text().splitlines():
        expected, name = line.split("  ", 1)
        check(digest(args.source/name) == expected, "target source changed: "+name)
    result = {"certificates": [certificate(args.source, False), certificate(args.source, True)],
              "coverage": forest_cover(args.source)}
    for family, work in (("forest", args.forest_replay), ("seven_edge", args.seven_replay)):
        if work:
            result[family+"_replay"] = replay_check(args.source, work, family)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
