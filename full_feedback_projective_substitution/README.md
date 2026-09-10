# Projective-plane substitutions still need at most two probes

Let \(G_i\) be incidence graphs of finite projective planes of orders
\(q_i\ge2\). For any finite Cartesian product
\(Q=G_1\square\cdots\square G_d\) and any nonempty finite internal
graphs \(H_v\),

\[
\zeta_d^*(Q[H_v])\le2.
\]

Two adjacent probes win within \(1+\sum_i q_i\) rounds. The internal
graphs can have arbitrary orders and edges and need not be connected.
This closes a natural amplification route using genuine two-probe
quotients. It does not settle the general question above two.

[THEOREM.md](THEOREM.md) gives the full proof. Its main step keeps the
posterior on one line, or among lines through one point, and shrinks
that set by at least one using an incident probe pair. Processing product
coordinates in successive phases preserves adjacency of the probes;
the module guard then transfers the strategy through substitution.

The known projective-plane parameter and unrestricted Cartesian-product
formula are credited to Jones and Kinnersley. The adjacent-probe
strategy and the resulting substitution bound are the proposed extension.
The round counts are upper bounds, not optimality claims.

## Reproduce

Use Python 3.12 or later with the standard library only. Tested with
CPython 3.12.12. From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
shasum -a 256 -c SHA256SUMS
```

The final output must be:

```text
result_sha256=9e562c470475e3bf070137e3f6500c80144a5213e6a68d7cf9c867a2b61f0af9
VERIFIED
```

`EXPECTED_OUTPUT.txt` records the complete deterministic output.
Normal and optimized-mode Python outputs agree. The verifier writes
no files and needs no packages, network, catalogue, solver, or data download.

## What the checks establish

- Classical planes over the fields of orders 2, 3, and 5 are generated
  explicitly and checked against the incidence axioms. Every edge is
  checked as an initial probe pair.
- All 3,876 nonsingleton subsets of line/point neighborhoods are audited,
  including all allowed choices of the two probes: 60,096 shrinking
  obligations and 295,404 unresolved response classes.
- The full policy on the 196-vertex product of two order-2 incidence
  graphs checks 229 states and 2,824 response branches, with worst
  duration four. Before that, 76,832 actual product response projections
  are checked against factor responses.
- Eight substitutions over the order-2 and order-3 planes cover empty,
  complete, path, and mixed singleton/nontrivial modules. Every policy
  response branch checks the module guard, quotient history, and final
  module resolution against distances in the expanded graph.

All response classes come from breadth-first graph distances and exact
sets. No incomplete search is used. The finite audits test the proposed
mechanism; the proof covers every finite projective plane, including
non-Desarguesian planes, every finite product, and all finite modules.

## Evidence and trust

Written combinatorial proof with exact finite audits. Remaining trust
is the mathematical proof, explicit finite generators, Python's integer
and set operations, and hardware. The proof is not formalized, and
independent peer review is pending. Novelty is relative to the graph and
primary sources searched on 2026-09-10; historical priority is not asserted.
