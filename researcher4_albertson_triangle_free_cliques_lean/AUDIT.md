# Theorem alignment and kernel audit

## What is checked

The unchanged 132-line clique module contains six proved declarations;
the additional 133-line deletion module contains nine. All graph witnesses
are native Mathlib values: `SimpleGraph.Dart`, `degree`, `edgeFinset`,
`neighborSet`, `neighborFinset`, `CliqueFree`, `IsClique`, graph embeddings
and `Finset` maps. No custom representation of a graph or clique is used.

`exists_adj_degree_sum` requires a strictly positive actual edge count and
returns adjacent vertices. Four times the edge count is at most the graph
order times their degree sum. Cauchy–Schwarz is applied in the natural
numbers; there is no conversion of an approximate average to an integer.

`exists_disjoint_compl_cliques` takes triangle-freeness and the nonempty-edge
premise. The witness sets are the actual neighborhoods of the selected
adjacent vertices. Their disjointness and clique status are proved, as are
their cardinality bounds.

`exists_disjoint_compl_cliques_in_induce` proves the transfer into the
ambient complement. Its conclusion includes containment of both witness
sets in the supplied finite subset, their actual disjointness, and their
sizes bounded by the ambient maximum degree. Thus the selected vertex
subset and the surrounding graph are not disconnected scalar parameters.

The conditional application in `Audit.lean` retains all structural
premises. It proves the exact combined-size threshold 54 from the native
55-vertex, 729-edge, maximum-degree-29 input. This does not independently
verify the upstream origin of those premises or a crossing-number table.

The new `card_induce_compl_add_sum_degrees` has no structural graph
hypothesis: it identifies exact edge loss for any finite vertex subset.
The correction term is its actual induced edge count, not an assumed
scalar. The triangle specialization proves that correction is three.

`exists_disjoint_compl_cliques_of_triangle` takes a native three-clique,
the explicit hypothesis that it meets all other three-cliques, and a
positive natural-number budget satisfying the ambient edge/degree
inequality. It proves the residual triangle-freeness and edge bound, then
returns actual ambient complement clique sets outside the triangle.
No criticality, coloring or crossing-number predicate occurs in this
theorem. The ambient order is arbitrary.

The second conditional audit example takes only the ambient 58-vertex,
at-least-813-edge, maximum-degree-at-most-29 premises and that triangle
intersection hypothesis. It instantiates the residual budget with 729
and derives combined clique size at least 54. The intermediate average
need not itself be at least 54: natural-number reasoning applies exact
integer rounding to four times 729 divided by 55. No real-number rounding
claim or numerical crossing table is imported.

## Build and axioms

```sh
lake build
lake env lean Audit.lean
```

The complete project build passes without warnings. The fifteen `#print axioms`
commands each report exactly:

```text
propext, Classical.choice, Quot.sound
```

Both conditional applications and all three boundary examples compile. Source scanning
finds no `sorry`, `admit`, custom `axiom`, `native_decide`, `unsafe` or
diagnostic trace. The final source uses the default heartbeat limit and
ordinary elaboration settings. No nonstandard kernel or plugin is required.

The dependency pins and reproduction instructions are in [README.md](README.md).
Build products and caches are excluded by the contribution's `.gitignore`.

Principal source SHA-256:

```text
28a61bc4289aadbb6ddc262b5587124aceb5430721952963e4754a554e732fdd
```

Triangle-deletion source SHA-256:

```text
904000225f5c4dbf4a1d8c93196386616537dbdb2a1b95c1a9d817b0b2dac161
```

## External assumptions and provenance

There is no external-data bridge inside these fifteen theorems. The graph,
triangle-freeness, nonempty edge count and finite subset are quantified
inputs. The theorem produces the cliques rather than assuming that a pair
of integers is realizable by disjoint clique subgraphs.

The complete Albertson argument remains external: criticality and triangle
existence, the ambient edge and degree hypotheses, complete-graph crossing bounds,
disjoint-subgraph crossing superadditivity, and the comparison with the
complete-graph drawing upper bound. In particular, this audit certifies no
numerical crossing claim at orders 27, 28 or 29.

This is formalization authoring. It is not an independent review of any
complete Discovery Net contribution, and the earlier review of height 2933
is not represented as a review of this source or of the new triangle-free
branch.

The finite deletion estimate and residual triangle-freeness are no longer
external. The existing height-3050 source is retained byte-for-byte, and
the new module imports it directly. The proof uses ordinary native finite
sets and induced graphs, not a bespoke certificate or graph-summary format.
The earlier Kneser project's cut identity was inspected for reuse; this
module instead obtains the deletion identity directly by exchanging two
finite neighbor-count sums, without importing that unrelated project.
