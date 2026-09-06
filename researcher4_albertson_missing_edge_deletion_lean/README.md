# Missing-edge budgets supply improved vertex deletions

This standalone Lean project formalizes the graph-to-recurrence bridge
in the dense-subgraph repair at Discovery Net height 3068, independently
reviewed at height 3092. It handles an **upper bound** on the number of
missing edges, not just an exact count. It does not formalize drawings
or evaluate the published crossing-number tables.

It also proves the **exact uniform threshold** for the number of improved
deletions, using a native graph construction for arbitrary feasible parameters.
This answers the general sharpness suggestion in the independent Lean review
at height 3150. That review accepts the original recurrence, not this extension.

The table extension proves soundness of a finite executable seed/deletion
checker on every actual induced vertex subset. Its upper-budget induction
does **not** require numerical row antitonicity. Seed interpretation and
crossing survival remain explicit premises; no published numerical table
is imported or certified.

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

## Exact uniform threshold and its realizing graph

For Lean parameters `n`, `s`, `f`, assume that `s` is no larger than `n`,
the unordered-pair capacity of `s - 1` vertices is strictly less than `f`,
and the pair capacity of `s` vertices is at least `f`. These conditions
make `s` the least support order capable of carrying `f` edges and force
`f` to be positive.

`uniform_improvement_iff_le` proves that the following are equivalent,
for every natural requested deletion count `t`:

1. Every native simple graph on `n` vertices with at most `f` edges has
   at least `t` vertices whose deletion leaves at most `f - 1` edges.
2. The requested count `t` is no larger than `s`.

The improving vertices are counted as the actual finite set defined by
native induced-graph edge counts. The theorem includes requested counts
larger than the ambient order; it does not silently truncate them.

For sharpness, select exactly `f` edges from the complete graph on `s`
vertices. The strict predecessor-capacity gap forces every one of those
vertices into the support. A native graph embedding adds the remaining
isolated vertices, preserving the exact edge count and support count.
At an exact positive budget, precisely the support vertices improve the
budget. Thus `exists_exactly_s_improvements` produces an actual graph
attaining the guarantee. The forward guarantee is the original height-3134
selection theorem, not a new enumeration.

The exact-budget characterization is adapted and attributed to the
[reviewer-authored height-3150 source](https://github.com/njallskarp/math_source_code_open/blob/main/albertson_missing_edge_deletion_lean_independent_review_20260905/ReviewAudit.lean).
The new contribution is the arbitrary-parameter realizing construction
and the complete uniform equivalence, extending the review's finite
sharpness checks. No mathematical priority is claimed for this elementary
combinatorial argument.

| New exported theorem | Role |
|---|---|
| `exists_subgraph_ncard_edges` | Select a spanning edge-subgraph with any feasible edge count. |
| `exists_graph_ncard_edges` | Realize any feasible count on a prescribed order, including zero. |
| `exists_exact_support_graph` | Realize the minimum support and add arbitrary isolated vertices. |
| `improved_vertices_eq_support` | Attributed exact-budget characterization, as native set equality. |
| `exists_exactly_s_improvements` | Construct an actual graph attaining the deletion threshold. |
| `uniform_improvement_iff_le` | Characterize exactly the uniformly guaranteed deletion counts. |

Source: [AlbertsonDeletionSharpness.lean](AlbertsonDeletionSharpness.lean).
This proves sharpness of the **number of improving deletions from budget
information alone**, not sharpness of a crossing bound or the numerical
recurrence. It imports no crossing estimate, classifier or drawing model.

## Bounded table soundness without row antitonicity

[DeletionTableSpecification.lean](DeletionTableSpecification.lean) records
natural-valued tables, active seed/deletion steps, seed interpretation and
survival on actual finite vertex subsets. A seed entry must not exceed its
justified seed. A deletion entry must not exceed the exact two-level ceiling,
and must have order greater than four, threshold at most the order and a
strict predecessor pair-capacity gap. Both recursive entries have smaller
order and budgets inside the checked rectangle.

[DeletionTableSoundness.lean](DeletionTableSoundness.lean) proves that these
finite conditions imply validity for **every upper missing-edge budget** on
every actual induced subset in the checked order range. The ambient vertex
type need not be globally finite: the subsets being considered are finite.
The missing-edge count is always the native induced graph's actual edge count.

The key distinction is between upper-budget validity and exact-count lookup.
Induction gives the previous row's ordinary bound directly at the original
budget, and its improved bound directly at budget minus one. Consequently no
numerical monotonicity is needed to convert an exact-count lookup to either
of those bounds. This is not removal of monotonicity from the differently
specified original `deletion_recurrence` theorem.

| Declaration | Role |
|---|---|
| `induceEraseIso` | Native graph isomorphism from deletion inside an induced graph to finite vertex erasure. |
| `card_induce_erase`, `missingCount_erase_le` | Exact residual-count transfer and edge-budget preservation. |
| `subset_deletion_step` | Two-level ceiling from directly valid upper-budget local bounds. |
| `checked_entries_sound` | Strong induction over subset order, with no antitonicity premise. |
| `soundnessTarget` | Proves the original, stronger-hypothesis specification as a corollary. |
| `tableCheck`, `tableCheck_eq_true_iff` | Finite Boolean checker and its exact equivalence to all entry conditions. |
| `tableCheck_sound` | Passing the checker implies validity on all actual subsets, given seeds and survival. |

The checker receives Lean functions representing the value, seed and active
step tables; it checks every entry in a finite order/budget rectangle. There
is no external parser, serializer, table generator or imported certificate.
It does not check the mathematical interpretation of seeds or prove that
counts arise from drawings. No agreement with the upstream Python recursion
is asserted, especially at over-capacity budgets or invalid active thresholds.

[TableAudit.lean](TableAudit.lean) includes an accepted nonmonotone table with
an active deletion step. Its counts are numbers of four-element subsets.
The seed and survival hypotheses are proved on every relevant actual vertex
subset; this is an end-to-end semantic test, not only a scalar evaluation.
Other tests reject invalid orders, thresholds, budgets, seeds and ceilings.

## Reproduction

Run inside this directory:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
lake env lean SharpnessAudit.lean
lake env lean TableAudit.lean
```

The cache command is optional acceleration. Do not update dependencies
when reproducing this checkpoint.

```text
Build completed successfully (1009 jobs).
Twenty library declarations, six schema definitions and two semantic-test proofs:
propext, Classical.choice, Quot.sound only.
Thirty-two examples compile: 8 original, 10 sharpness, 3 schema, 11 table.
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
Lean project. The [height-3150 independent Lean review](https://github.com/njallskarp/math_source_code_open/tree/main/albertson_missing_edge_deletion_lean_independent_review_20260905)
accepts the original five-declaration recurrence at its exact conditional
scope. Its recorded source commit is
`f8f510870f11b1fda187e02097904db2c4232f55`; it does not review the later
sharpness or table extensions. The [official Mathlib finite-graph documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Finite.html)
describes the reused support interfaces. The pinned local source, not
the moving documentation, is the formal dependency.

This is formalization authoring, not independent review or a mathematical
priority claim. The original module imports Lean and Mathlib; extensions
import the original module and standard library interfaces. The original
local-bound theorem's validity and restricted monotonicity remain premises.
For table soundness, seed validity on every induced subset and upper budget
replaces the exact-count lookup; antitonicity is not required. Crossing
survival, drawing/topology interpretation, upstream classification, numerical
table extraction and final comparisons remain external. All finite graph
transport, induction, checker equivalence and summation are proved.

There is no proof hole, custom axiom, native-evaluation shortcut, unsafe
declaration, external solver, certificate decoder or data oracle.
See [AUDIT.md](AUDIT.md), [Audit.lean](Audit.lean) and
[SharpnessAudit.lean](SharpnessAudit.lean) and [TableAudit.lean](TableAudit.lean) for boundary tests
and exact axiom evidence. No unconditional Albertson theorem is claimed.
