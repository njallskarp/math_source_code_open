# Theorem alignment and kernel audit

## Formal statement and proof boundary

The 98-line source exports five proved declarations using native Mathlib
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
```

All five exported declarations report exactly:

```text
propext, Classical.choice, Quot.sound
```

The workspace build passes without warnings. The source uses ordinary
elaboration and the default heartbeat limit. Source scans find no proof
holes, custom axioms, native evaluation, unsafe declarations, diagnostic
traces or private paths. All dependency revisions are pinned in the
toolchain and manifest; see [README.md](README.md).

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

## Source integrity and omitted bridges

Principal source SHA-256:

```text
a4f4902e820dda6abc3cbf379c68451dc0addeb6f0b15c8e7a1d6659d7fd70ae
```

There is no external-data bridge inside the theorems. The remaining
surrounding claims are the local crossing estimates, restricted
monotonicity of the actual numerical recurrence, good-drawing and
crossing-survival interpretation, upstream enumeration, and any final
Albertson comparison. Neither the author program nor its independent
review is executed by this project. This is authoring, not independent
review of earlier artifacts signed by this contributor.
