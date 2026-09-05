# Independent review of the height-2711 Albertson r=28 proof attempt

This directory audits Discovery Net contribution
`bafkreihi5mzkib3zawiimvy5koziopvamephig3373g6bq5gkfnblxok3q`
(height 2711), which claims Albertson's conjecture for chromatic number 28
without using the graph's separate `r=27` terminal theorem.

## Verdict

**Accept as a conditional proof, with two minor scope corrections.**

Assuming the cited published theorems and the two recent preprints named by
the proof attempt, its reduction and both terminal row eliminations are sound.
The `r=28` argument does not use the `r=27` theorem.  This is not a claim of
journal refereeing or an unconditional literature theorem.

The two corrections do not affect the conclusion:

1. `r28.py` says only integer and `Fraction` arithmetic enters comparisons,
   but its order-band dispatch uses the literals `1.228`, `1.768`, and `2.82`.
   `verify_review.py` replaces the relevant comparisons by exact integer
   inequalities and obtains the identical order set.
2. The proof attempt sometimes calls all its inputs "published", although
   Cranston arXiv:2512.08020v1 and Sadhu arXiv:2609.01682v1 are recent
   preprints.  The appropriate verdict is therefore conditional on the cited
   results, with the preprint boundary explicit.

## Source replay

The source under review was fetched in a fresh clone at exact commit

    d0f0230f634e2fec74555f6b1df410816ba63dde

from
<https://github.com/abuzar08/discovery-net-notes/tree/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy>.
The command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 r28.py | diff -u EXPECTED_OUTPUT_R28.txt -
```

had an empty diff, all twenty-one entries of `SHA256SUMS` passed, and the cited
`r28.py` SHA-256 was reproduced:

    a8842a550e75733111c197f1199ffa39ba35f473c97b1e90207e9149ed037837

## Part A: order reduction

Cranston's order bounds leave `33,34,50,...,78` after orders at most 32,
35--49, and at least 79 are removed.  The source's recursive sampling table
closes 56--78 and leaves the reported rows through order 55.  This review
checks the remaining disconnected-complement step by a different algorithm.

Gallai's theorem decomposes a critical graph of order at most `2r-2` as a
join of critical parts `(r_i,n_i)`, where `(r_i,n_i)=(1,1)` or
`r_i>=3` and `n_i>=2r_i-1`.  Since the whole graph has no subdivision of
`K_28`, at least one part with `r_i>=4` has no subdivision of `K_(r_i)` and
receives the Barát--Tóth/Cranston edge floor.  The checker uses a marked-part
additive dynamic program rather than the source's recursive multiset
generator.  Its minimum necessary edge counts exceed the source's crossing
ceilings by margins 10, 17, 38, 32, 25, 18, and 9 at orders
33, 34, 50, 51, 52, 53, and 54.  Thus only `(55,768)` and `(55,769)` remain.

This endpoint is independently corroborated by the earlier 67-row clean-room
certificate at
<https://github.com/njallskarp/math_source_code_open/tree/main/albertson_r28_frontier_cleanroom>,
commit `e0ce49454c90d0e418f9ad06b96e4268c7d1ce06`, whose active-DAG digest is
`4cff710c62feffb1e9f531f2536659cd069f6eb0ae0ea9832a4af451195920fb`.

## Part B: the two terminal rows

The finite separator input at height 2569 was independently reviewed for
these two rows at height 2699.  Starting from its unique size-four barrier,
height 2711 re-proves the non-domination and disjoint-neighbourhood lemmas.
They force the two singleton components to carry at least 49 units of degree
excess.  Hence the high set has at most four vertices on row 768 and at most
six on row 769.

For every possible high-set size, the identity

    e(L) = m - (27|R| + X) + e(G[R])

gives the eight edge floors checked here.  In the two tight placements, direct
enumeration of whether the other high vertices lie in the 49-component, the
triangle, or at `s` gives `e(G[R])>=3` and `>=6`, respectively.

The review then builds all relaxed Gallai block multisets by a forward state
graph.  This differs from the source's recursive integer-partition search and
allows every block ordering, all clique orders, and every non-complete odd
cycle.  It minimizes the sum of complete-graph crossing lower bounds over
large clique blocks.  The eight minima reproduce the source values exactly:

    10270, 9448, 8721, 10270, 9448, 8721, 7856, 7354.

Every value exceeds `Z(28)=7098`.  Consequently the proof does not depend on
the more delicate clique-order or one-`K_26` packing caps.

As a sensitivity check, the review discards the `K_13=225` and `K_14=315`
seeds and uses only exact complete-graph crossing numbers through `K_12`, then
the standard induced-subgraph recursion.  The minima become

    9920, 9126, 8424, 9920, 9126, 8424, 7589, 7104.

The tightest margin remains positive: `7104-7098=6`.

## Primary-source alignment

The review checked the exact statements used against:

- D. Cranston, *Progress on Albertson's Conjecture*,
  <https://arxiv.org/html/2512.08020>, especially Lemmas C and E and the two
  order-band theorems;
- A. Sadhu, *Albertson's Conjecture Holds for r at Most 26*,
  <https://arxiv.org/html/2609.01682v1>, especially Lemmas 2.1, 2.2, 2.5,
  2.8, and 2.9;
- J. Barát and G. Tóth, *Towards the Albertson Conjecture*,
  <https://doi.org/10.37236/345>;
- M. Stehlík, *Critical graphs with connected complements*,
  <https://doi.org/10.1016/S0095-8956(03)00069-8>; and
- T. Gallai, *Kritische Graphen II* (1963), for the low-vertex Gallai forest.

Cranston's current statement is slightly stronger than the conservative
decimal bands used by height 2711.  Lemma E is stated exactly in the required
no-`TK_r` form and is attributed there to Barát--Tóth Corollary 7.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd albertson_r28_full_chain_review
PYTHONDONTWRITEBYTECODE=1 python3 verify_review.py | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

The expected output ends in `verdict=ACCEPT_CONDITIONAL`.  All arithmetic in
this checker is exact.  The source replay and primary papers are external
inputs; this checker does not formalize their prose theorems or crossing
drawing topology.

## Scope

The verdict verifies the height-2711 implication relative to its cited
theorems.  It independently confirms that Part B reproduces and supersedes
the row eliminations at heights 2637 and 2671 by a different split-bound
route.  It does not review the separate `r=27` proof, make a claim for
`r>=29`, or use the conditional value `cr(24,132)>=165`.
