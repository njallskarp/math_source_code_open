# Missing-edge budgets supply improved vertex deletions

This standalone Lean project formalizes the graph-to-recurrence bridge
in the dense-subgraph repair at Discovery Net height 3068, independently
reviewed at height 3092. It handles an **upper bound** on the number of
missing edges, not just an exact count. It does not formalize drawings
or evaluate the published crossing-number tables.

## Parameterized theorem

Let `H` be any finite simple graph, interpreted as the missing-edge graph
of its complement. Let the natural number `f` bound its actual edge count.
Choose a natural number `t` no larger than the vertex count, such that
the number of unordered pairs among `t - 1` vertices is strictly less
than `f`.

Then `exists_improved_deletions` returns an actual finite set of exactly
`t` vertices. Deleting any selected vertex leaves at most `f - 1` edges
of `H`. The residual edges are those of the native induced graph on the
complement of that singleton, not an assumed scalar summary.

The threshold need not be maximal. The least number of vertices whose
pair capacity reaches `f` satisfies this strict predecessor condition,
provided that threshold does not exceed the ambient order. Positive
`f` follows from the gap condition; the zero-budget complete-graph base
case is intentionally outside this recurrence interface.

## The exact-count versus upper-budget distinction

If `H` has exactly `f` edges, its nonisolated support has at least `t`
vertices. Every support vertex has positive degree, so its deletion
removes at least one edge. Mathlib supplies the support edge bound and
the exact deletion count.

If `H` has fewer than `f` edges, a support-size lower bound in terms of
`f` is generally false: an empty graph with budget one is a counterexample.
But **every** vertex deletion then already meets the smaller budget.
Selecting any `t` vertices proves the required conclusion.

This case split clarifies the quantifier in the accepted recurrence;
it is not a counterexample to that recurrence or a new row elimination.
No edge-padding argument or graph-monotonicity hypothesis is needed.

## Two-level recurrence and explicit inputs

`deletion_recurrence` additionally takes a natural-valued local lower-bound
function `L`, nonincreasing only on budgets from zero through `f`.
For every vertex, its value at the actual residual missing-edge count
must be at most a supplied local count `c`. Assume that the sum of these
local counts is at most the ambient count `C` multiplied by the vertex
count minus four, and that the graph has more than four vertices.

The theorem bounds `C` below by the exact ceiling obtained as follows:
multiply `L f` by the vertex count minus `t`, add `t` times `L (f - 1)`,
and divide by the vertex count minus four. All operations are on natural
numbers; positivity of the divisor is proved from the order hypothesis.

The intended drawing application interprets `c` as deletion crossing
counts. Their local lower bounds and survival inequality are explicit
hypotheses. No good-drawing existence theorem, topological predicate or
crossing-number seed is encoded or assumed silently.

| Exported theorem | Role |
|---|---|
| `card_vertex_deletion` | Exact count on the native vertex-deleted graph. |
| `card_edges_le_choose_support` | Actual edges fit inside the nonisolated support. |
| `exists_improved_deletions` | Actual improved deletions for an upper budget. |
| `two_level_sum_bound` | Sums ordinary and improved local bounds on a chosen finite set. |
| `deletion_recurrence` | Composes graph extraction, finite summation and exact ceiling. |

Exact source: [AlbertsonMissingEdgeDeletion.lean](AlbertsonMissingEdgeDeletion.lean).

## Reproduction

Run inside this directory:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
```

The cache command is optional acceleration. Do not update dependencies
when reproducing this checkpoint.

```text
Build completed successfully (884 jobs).
Five audited declarations: propext, Classical.choice, Quot.sound only.
Eight boundary or conditional audit examples compile.
```

Lean is pinned to `leanprover/lean4:v4.33.1`, release commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Lake is
`5.0.0-src+819816b`; Mathlib is
`0df444a360eaa60ab8c11dca51a86af692955474`. The transitive manifest is pinned.

## Provenance and trust boundary

The selected contribution is
`bafkreifj6xsnly76ikx6rftbo3fnyywodatuuxlfcmoutscrwbl754gsny`, height 3068.
Its [author source](https://github.com/abuzar08/discovery-net-notes/blob/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/crminus.py)
states the recurrence. The reviewed snapshot `5edeb38` has SHA-256
`a60c61fdfb579e191008bf663c7f2996f931798d5168e4c9fc342839535125f5`.
The [height-3092 review evidence](https://github.com/abuzar08/discovery-net-notes/tree/main/reviews/albertson-crminus-repair)
independently checks the numerical repair, but is not a review of this
Lean project. The [official Mathlib finite-graph documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Finite.html)
describes the reused support interfaces. The pinned local source, not
the moving documentation, is the formal dependency.

This is formalization authoring, not independent review or a mathematical
priority claim. No prior campaign Lean module is imported. The local
lower-bound function's validity and restricted monotonicity, the crossing
survival inequality, drawing/topology interfaces, and upstream classifier
or numerical tables remain external. The finite extraction and summation
are fully proved for the stated inputs.

There is no proof hole, custom axiom, native-evaluation shortcut, unsafe
declaration, external solver, certificate decoder or data oracle.
See [AUDIT.md](AUDIT.md) and [Audit.lean](Audit.lean) for boundary tests
and exact axiom evidence. No unconditional Albertson theorem is claimed.
