# Stable-transitivity growth and radial limits

This directory proves a structural theorem suite for the stable-transitivity
numbers introduced by Davis and Schroeder:

- stabilization is subadditive under tournament addition;
- `m(n,k+l)<=m(n,k)+m(n,l)` and `lim_k m(n,k)/k` exists;
- `m(n,k)=k` for every `k>=1` and `3<=n<=7`;
- `k<=m(8,k)<=2k`;
- `m(n,k)<=k floor((n-1)^2/4)`, improving the source's general bound; and
- the exact dilation rate of any fixed tournament is a radial Minkowski gauge
  in the linear-ordering polytope.

The exact values for ordinary tournaments through order seven and at order
eight are explicitly identified as prior, independently reviewed Discovery
Net dependencies.  The additive, all-`k`, general-bound, and radial-limit
arguments are new claims relative to the searched source and graph.

## Reproduce

From this directory run:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_growth.py
    diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_growth.py)
    shasum -a 256 -c SHA256SUMS

The checker uses only Python's standard library and exact integers, tuples,
and sets.  It exhausts the three-vertex TTD semigroup through degree 12,
checks all small three-vertex subadditivity instances, and compares permutation
enumeration with a separate subset dynamic program for every tournament
through order six.  The universal theorems are proved symbolically in
`THEOREM.md`; computation is corroborative.

## Primary source and scope

Matthew Davis and Michael W. Schroeder, *Relating tournaments and permutations
with xrays*, arXiv:2606.21532v1 (2026):

https://arxiv.org/abs/2606.21532v1

The paper introduces stable transitivity, proves finiteness, asks for the
growth of `m(n,k)`, and records the bound `k*binom(n,2)/2`.  Targeted searches
for the exact term "transitive tournament decomposition" found no other
primary source.  No novelty is claimed for Fekete's lemma, feedback-arc
orderings, rational linear programming, or Minkowski gauges in isolation.
