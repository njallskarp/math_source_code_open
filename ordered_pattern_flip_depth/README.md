# Ordered pattern cliques: exactness through flip depth

This directory proves a uniform part of the Anastos--Jin--Kwan--Sudakov
ordered pattern-clique extremal conjecture.  If an `r`-partite pattern has `f`
sign changes in its normalized `AB/BA` block word, then for every `m>=2` and
`0<=s<=f`,

    ex_<(rm+s,P^(m)) = binom(rm+s,r)-binom(r+s,r).

Thus the first previously open boundary `n=rm+2` is exact for every pattern
with at least two flips.

The proof selects `binom(r+s,r)` canonical forbidden cliques and shows that
they are pairwise edge-disjoint.  Any collision would force the discrete
total variation of the difference of two `s`-element multiplicity vectors to
be `2|d|(f+1)`, although it is at most `2s`.  The source lower construction
deletes exactly the same number of edges.

## Reproduce

From this directory run:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_flip_depth.py
    diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_flip_depth.py)
    shasum -a 256 -c SHA256SUMS

The checker uses only Python's standard library and exact integer/tuple/set
operations.  It verifies the canonical embedding formula and edge-disjoint
packing for every normalized pattern in a documented parameter box, checks
the matching lower construction against all omitted-set copies in a smaller
box, and verifies the explicit collision showing that this packing mechanism
is sharp at depth `f+1`.  These finite checks corroborate but do not replace
the symbolic proof in `THEOREM.md`.

## Primary source and scope

Michael Anastos, Zhihan Jin, Matthew Kwan, and Benny Sudakov, *Extremal,
enumerative and probabilistic results on ordered hypergraph matchings*, Forum
of Mathematics, Sigma 13 (2025), e55:

https://doi.org/10.1017/fms.2024.144

Open manuscript: https://arxiv.org/abs/2308.12268

The paper states the all-pattern formula as Conjecture 1.20, supplies the
matching lower construction, and proves all `m=2` cases and all `n` for the
alternating pattern.  A reviewed Discovery Net theorem already proves every
pattern at `n=rm+1`.  No claim is made here for patterns with fewer than `s`
flips; the explicit collision at `s=f+1` is a limitation of this selected-copy
packing, not a counterexample to the conjecture.
