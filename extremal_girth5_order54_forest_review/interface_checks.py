#!/usr/bin/env python3
"""Adversarial checks of the reviewed encoding's mathematical interfaces.

This file deliberately imports the target's profile generator and comparator
for differential testing. audit.py does not import any target implementation.
"""
import argparse
from itertools import combinations, product
import json
from pathlib import Path
import sys

from audit import check, high_histograms


def profiles_check(author_profiles):
    totals = {}
    for m in (5, 6):
        for k in range(9-m):
            budget = 22-3*m-k
            left = high_histograms(6, 17, 39+2*m, budget)
            right = high_histograms(7, 24, 65-4*m, budget)
            independent = {(x,y) for a,x in left for b,y in right if a+b == budget}
            generated = [(tuple(x),tuple(y)) for x,y in author_profiles(m,k)]
            check(len(generated) == len(set(generated)), "duplicate author profile")
            check(set(generated) == independent, "profile mismatch")
            totals[f"{m},{k}"] = len(generated)
    return totals


def primitive_checks(lex_chain):
    from pysat.card import CardEnc, EncType
    from pysat.formula import CNF, IDPool
    from pysat.solvers import Solver
    weights = (-1,0,1,2,3,4,5,6)
    literals = [(-i if w < 0 else i) for i,w in enumerate(weights,1)
                for _ in range(abs(w))]
    offset = -sum(w for w in weights if w < 0)
    cardinality_checks = 0
    for target in range(-2, 23):
        bound = target+offset
        if bound < 0 or bound > len(literals):
            clauses = [[]]
        else:
            clauses = CardEnc.equals(literals, bound=bound, top_id=8,
                                     encoding=EncType.seqcounter).clauses
        with Solver(name="g4", bootstrap_with=clauses) as solver:
            for bits in product((0,1), repeat=8):
                result = solver.solve(assumptions=[i if b else -i
                                      for i,b in enumerate(bits,1)])
                check(result == (sum(w*b for w,b in zip(weights,bits)) == target),
                      "signed repeated-literal cardinality mismatch")
                cardinality_checks += 1
    lex_checks = 0
    # Independent rows, identical rows, reversal, repeated coordinates,
    # shared middle entries, and reversed complete blocks.
    cases = [([1,2,3,4],[5,6,7,8]), ([1,2,3,4],[1,2,3,4]),
             ([1,2,3,4],[4,3,2,1]), ([1,2,1,3],[2,1,2,3]),
             ([1,2,3],[3,2,1]), ([1,2,3,4,5,6],[2,1,4,3,6,5])]
    for left,right in cases:
        n = max(left+right)
        pool = IDPool(start_from=n+1)
        cnf = CNF()
        lex_chain(cnf, pool, [left,right])
        with Solver(name="g4", bootstrap_with=cnf) as solver:
            for bits in product((0,1), repeat=n):
                valid = tuple(bits[i-1] for i in left) <= tuple(bits[i-1] for i in right)
                result = solver.solve(assumptions=[i if b else -i
                                      for i,b in enumerate(bits,1)])
                check(result == valid, "shared-input comparator mismatch")
                lex_checks += 1
    return {"signed_cardinality_assignments": cardinality_checks,
            "lex_assignments": lex_checks}


def small_graphs():
    """Check generalized partition equations on ALL labeled graphs of order <=6.

    For every girth>=5 graph, enumerate every subset of its sinks as T.
    This checks equations independently of degree 6/7/8 assumptions.
    """
    graphs = valid = subsets = vertex_equations = 0
    for n in range(7):
        pairs = list(combinations(range(n),2))
        for mask in range(1 << len(pairs)):
            graphs += 1
            adj = [set() for _ in range(n)]
            for i,(u,v) in enumerate(pairs):
                if mask >> i & 1:
                    adj[u].add(v)
                    adj[v].add(u)
            if any(len(adj[u]&adj[v]) > 1 or (v in adj[u] and adj[u]&adj[v])
                   for u,v in pairs):
                continue
            valid += 1
            sinks = [v for v in range(n)
                     if len({v}|adj[v]|set().union(*(adj[u] for u in adj[v]))) == n]
            for bits in range(1 << len(sinks)):
                T = {v for i,v in enumerate(sinks) if bits >> i & 1}
                low = set(range(n))-T
                c = [len(adj[v]&T) for v in range(n)]
                subsets += 1
                for v in range(n):
                    lhs = sum(c[u]-1 for u in adj[v]&low)
                    if v in T:
                        rhs = len(T)-1-sum(c[t] for t in adj[v]&T)
                    else:
                        lhs += sum(c[t] for t in adj[v]&T)
                        rhs = len(T)-len(adj[v])
                        pieces = [adj[u]&T for u in adj[v]&low]
                        occupied = (adj[v]&T)|set().union(*(adj[t]&T for t in adj[v]&T))
                        check(sum(map(len,pieces)) == len(set().union(*pieces)), "partition overlap")
                        check(set().union(*pieces) == T-occupied, "partition coverage")
                    check(lhs == rhs, "individual high-neighbor equation")
                    vertex_equations += 1
    return {"labeled_graphs": graphs, "girth_at_least_five_graphs": valid,
            "sink_subsets": subsets, "vertex_equations": vertex_equations}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(args.source.resolve()))
    from forest_profiles import profiles
    from seven_edge_sat import lex_chain
    result = {"author_profiles_equal_independent": profiles_check(profiles),
              "encoding_primitives": primitive_checks(lex_chain),
              "partition_equations": small_graphs()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
