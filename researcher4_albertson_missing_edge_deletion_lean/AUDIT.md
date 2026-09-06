# Theorem alignment and kernel audit

## Formal statement and proof boundary

The original 98-line source exports five proved declarations using native Mathlib
`SimpleGraph`, `support`, `degree`, `edgeFinset`, `induce`, `Finset` and
`AntitoneOn` definitions. No custom graph or certificate representation
is introduced.

The main theorem quantifies over arbitrary finite missing-edge graphs,
an upper edge budget, an admissible support threshold, a local bound
function, local counts and an ambient count. It assumes restricted
monotonicity of the local bound, its validity for every actual residual
edge count, a crossing-survival-shaped sum inequality, and order greater
than four. These are premises, not claimed verified properties of a
particular numerical program or drawing.

Its native witness lemma treats exact and slack budgets separately.
Only the exact case derives a support lower bound. The slack case uses
all ambient vertices as available improved deletions. This closes the
upper-budget quantifier without claiming that an upper budget measures
the actual nonisolated support.

The general finite-set summation lemma has no graph hypothesis. The final
ceiling is Mathlib's natural ceiling division, with a strictly positive
denominator. There is no floating-point calculation or imported number.

## Build and axioms

```sh
lake build
lake env lean Audit.lean
lake env lean SharpnessAudit.lean
```

All five original and six sharpness declarations report exactly:

```text
propext, Classical.choice, Quot.sound
```

The workspace build passes without warnings. The source uses ordinary
elaboration and the default heartbeat limit. Source scans find no proof
holes, custom axioms, native evaluation, unsafe declarations, diagnostic
traces or private paths. All dependency revisions are pinned in the
toolchain and manifest; see [README.md](README.md).

The complete two-target build reports 1006 jobs. Builds use the pinned
dependency cache as acceleration, not a fresh source rebuild of all Mathlib.

## Eight checked examples

- An empty five-vertex graph with budget one has support size zero but
  still supplies two actual improved deletions.
- Two disjoint edges on four vertices leave exactly one edge after every
  vertex deletion. Thus no deletion is complete in the complementary
  graph; this tests the discarded stronger upstream argument.
- The same graph supplies three improved deletions for budget two.
- The complete graph on five vertices supplies all five deletions at
  its full edge budget ten.
- The zero budget cannot satisfy the strict threshold gap.
- One edge on three vertices refutes replacing the strict threshold gap
  by equality: the isolated vertex's deletion still leaves the edge.
- A six-vertex, two-edge graph with synthetic local counts instantiates
  the full recurrence and derives a bound of fourteen.
- The corresponding nonintegral quotient, twenty-seven divided by two,
  has ceiling fourteen, checked by kernel reduction.

The synthetic local counts are not represented as crossing counts of a
drawing. Finite fixtures use ordinary `decide`, not `native_decide`.
The strict-gap counterexample uses a cardinality-to-universe argument
and one finite residual-edge calculation rather than opaque enumeration.

## General sharpness alignment and ten new checks

The 131-line [AlbertsonDeletionSharpness.lean](AlbertsonDeletionSharpness.lean)
proves a uniform equivalence over arbitrary ambient order, feasible positive
budget, minimum support threshold and requested deletion count. An actual
native graph realizes the minimum number of improving deletions. The source
uses `Set.ncard` for edge and vertex sets, with explicit conversions to the
original `edgeFinset` interface. There is no arbitrary numerical graph summary.

The construction chooses a cardinality-constrained subset of a native complete
graph's edge finset, proves it contains no loops, forms `fromEdgeSet`, and maps
the graph through `Fin.castLEEmb`. Pair capacity forces exact support; native
edge-map and support-map identities preserve the counts. The reviewer-authored
exact-budget characterization at height 3150 is adapted as a set equality,
with attribution. The forward uniform implication uses the original selection
theorem; the converse uses the newly constructed extremal graph.

`SharpnessAudit.lean` checks:

- Edge selection at empty order and zero count.
- A symbolic ambient order with one edge and exactly two support vertices.
- Budget 16, minimum support seven, and five added isolated vertices; this
  exceeds the review's finite sharpness range, whose budgets stop at 15.
- The positive guarantee at a nontriangular budget and interior threshold.
- Failure of the next larger uniform guarantee at that same budget.
- Full ambient edge capacity, where every vertex is guaranteed.
- Failure if predecessor-capacity equality is treated as a strict gap.
- A requested deletion count larger than the ambient order.
- Failure of the support characterization at zero budget, because natural
  subtraction then allows every empty-graph deletion.
- Impossibility of realizing an edge count above pair capacity.

The symbolic and existence tests instantiate proved theorems, not an external
generator. The small capacity checks use ordinary kernel-reduced `decide`;
no exhaustive graph enumeration, solver or imported certificate is used.
The zero-budget condition is tested rather than hidden. The exact support
construction and uniform equivalence are not claims that a numerical crossing
recurrence is sharp or that its external premises hold.

## Source integrity and omitted bridges

Principal source SHA-256:

```text
a4f4902e820dda6abc3cbf379c68451dc0addeb6f0b15c8e7a1d6659d7fd70ae
```

Sharpness source SHA-256:

```text
96a6ddd74e144149fa9ba6785acbeaa47bc0bf98e8563ed66f7c31bd57db2074
```

There is no external-data bridge inside the theorems. The remaining
surrounding claims are the local crossing estimates, restricted
monotonicity of the actual numerical recurrence, good-drawing and
crossing-survival interpretation, upstream enumeration, and any final
Albertson comparison. Neither the author program nor its independent
review is executed by this project. This is authoring, not independent
review of earlier artifacts signed by this contributor.
