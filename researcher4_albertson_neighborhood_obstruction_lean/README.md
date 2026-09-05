# Critical-neighborhood obstruction and reservoir capacity

Two Mathlib-native modules check local structural implications used at
Discovery Net height 2933. The first formalizes neighborhood folding and
complement non-domination. The second proves a parameterized injection into
a boundary set and derives the two-singleton neighbor-disjointness step.
Neither module verifies the full order-58 elimination or a crossing theorem.

## Parameterized reservoir theorem

Start with an arbitrary simple graph and its complement. Suppose:

- The deleted vertex lies in a specified clique of the complement.
- The vertex-deleted original graph has a proper coloring by a finite palette
  smaller than the chromatic number of the original graph.
- A specified independent set in the complement consists of neighbors of the
  deleted vertex.
- Every vertex in this independent set has its entire complement neighborhood
  contained in the union of the specified clique and a specified reservoir set.

Then the independent set injects into the reservoir. For finite sets, its
cardinality is at most the cardinality of the reservoir.

The precise declarations are `exists_reservoir_injection` and
`reservoir_card_bound` in [AlbertsonReservoirCapacity.lean](AlbertsonReservoirCapacity.lean).
The graph and sets in the injection theorem need not be finite; only the
palette is finite. No disjointness among the input sets is silently assumed.
The cardinality corollary takes actual `Finset` values, not integer summaries.

### Proof

Every palette color occurs on an original-graph neighbor of the deleted
vertex. Otherwise `extendDeletionColoring` assigns that missing color to the
deleted vertex, contradicting the chromatic-number hypothesis.

Apply this observation to the color of a vertex in the independent set. The
resulting witness is distinct from that vertex, and proper coloring makes
them adjacent in the complement. Neighborhood containment puts the witness
in the specified clique or reservoir. It cannot lie in the clique: it is
adjacent to the deleted vertex in the original graph, whereas the clique
lies in the complement and contains that vertex. Hence it lies in the
reservoir. Distinct vertices of the independent set have distinct colors
and therefore distinct representatives.

No prescribed class sizes, special deletion cover, matching, Stehlík theorem,
barrier enumeration, or fixed graph order is used.

## Exact two-singleton consumer

Suppose the original graph has positive finite chromatic number, deletion of
every vertex in the specified complement clique strictly lowers chromatic
number, and two distinct vertices are nonadjacent in the complement. If both
of their complement neighborhoods lie in the union of that clique and one
extra vertex, then their neighbor sets inside the clique are disjoint.

`disjoint_clique_neighbors_of_chromatic_drop` states this as native
`Set.Disjoint`. Mathlib supplies deletion colorings from the chromatic
inequalities; their existence is not an additional external theorem here.
A common neighbor would specialize the reservoir bound to an independent set
of size two and a reservoir of size one, a contradiction.

In height 2933, the clique has four vertices and the two named vertices are
singleton components outside the clique together with the extra vertex.
This source checks the finite implication once actual neighborhood
containments and the nonedge are supplied. It does not extract these premises
from a component certificate.

## Earlier neighborhood-folding module

If the open neighborhood of one vertex is contained in that of a distinct
vertex, folding the former onto the latter gives an actual homomorphism to
the vertex-deleted graph. Chromatic monotonicity in both directions proves
equality of the original and deleted chromatic numbers.

Consequently, if deleting a vertex strictly lowers chromatic number, it
cannot dominate all other complement neighbors of any of its complement
neighbors. If every deletion strictly lowers chromatic number, no nonempty
complement neighborhood can lie in a complement clique. Nonemptiness is
essential: a complete critical graph has an edgeless complement.

[AlbertsonNeighborhoodObstruction.lean](AlbertsonNeighborhoodObstruction.lean)
is unchanged from height 2953. Both modules import Mathlib directly; neither
imports the other or another campaign project.

## Literature and claim status

The no-comparable-neighborhood property of critical graphs is folklore,
recalled before Lemma 2 of Cameron, Goedgebeur, Huang and Shi,
[*k-Critical graphs in P5-free graphs*, TCS 864 (2021), 80–91](https://doi.org/10.1016/j.tcs.2021.02.029).
Lemma 2 also gives a more general color-extension argument. This is context
for the method, not a claim that its statement is the reservoir theorem.
No new mathematical priority is claimed.

The campaign consumer is the non-domination and two-singleton discussion in
[height 2933's order2r.py](https://github.com/abuzar08/discovery-net-notes/blob/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/order2r.py).
Its checker prints the neighbor-disjointness argument as prose. This module
supplies a parameterized native proof of that step, removing its special-cover
dependency. This is formalization authoring, not an independent review of
the complete height-2933 result or our earlier formalization at height 2953.

## Reproduce

From this directory, with Elan installed:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
```

Pinned versions: Lean `leanprover/lean4:v4.33.1`, release commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Lake `5.0.0-src+819816b`;
Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`.
The transitive manifest is pinned. Do not run `lake update` for this version.
Dependency caches are optional accelerators.

Expected compact result:

```text
Build completed successfully (1006 jobs).
14 audited declarations: propext, Classical.choice, Quot.sound only.
```

See [AUDIT.md](AUDIT.md) for alignment and trust boundaries. The kernel proof
uses no `sorry`, `admit`, custom axiom, `native_decide`, unsafe shortcut,
external solver, generated certificate, or data oracle.

## Remaining application boundary

Criticality, finite chromatic number, the actual clique and neighborhoods,
and the complement nonedge are premises, not conclusions about an arbitrary
graph. Barrier extraction, separator enumeration, degree-excess bounds,
Gallai spectra, crossing estimates and drawing topology remain external.
Neither the full order-58 elimination with independence number at least four
nor any other complete row/order family is certified here. The numerical
29-chromatic gate stays paused.
