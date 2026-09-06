# Triangle-free induced graphs force two disjoint complement cliques

This standalone Lean project formalizes the finite graph-to-clique chain in
the triangle-free branch of the Albertson argument at Discovery Net height
3014. It produces actual vertex sets and native clique proofs, not an
asserted pair of clique sizes. It does not formalize crossing numbers.

## Parameterized theorem

Let a finite simple graph have at least one edge and no triangle. Then its
complement contains two disjoint cliques whose combined size, multiplied by
the graph order, is at least four times the graph's edge count. Each clique
has size at most the maximum degree of the original triangle-free graph.

The stronger ambient version starts with any finite graph and a finite
subset of its vertices whose induced graph is triangle-free and has an
edge. It produces two disjoint cliques in the complement of the ambient
graph, both contained in that subset. The combined-size inequality uses
the subset's cardinality and the actual induced edge count. Both clique
sizes are bounded by the ambient graph's maximum degree.

The quantifiers range over arbitrary finite graphs and subsets. Neither
the graph order nor the chromatic parameter is fixed. The inequality is
written in natural numbers without division, so integer rounding is exact.

Exact source: [AlbertsonTriangleFreeCliques.lean](AlbertsonTriangleFreeCliques.lean).

## Triangle-deletion input interface

The additional module
[AlbertsonTriangleDeletion.lean](AlbertsonTriangleDeletion.lean) proves the
finite input bridge, not merely a restatement of the induced-graph premises.
Take any finite simple graph and a chosen triangle that meets every triangle
of that graph. Choose any positive natural-number residual edge budget.
Assume that budget plus three times the ambient maximum degree is at most
the ambient edge count plus three.

Then `exists_disjoint_compl_cliques_of_triangle` produces two disjoint
cliques in the ambient complement, outside the chosen triangle. Each has
size at most the ambient maximum degree. Multiplying their combined size
by the number of vertices outside the triangle gives at least four times
the residual budget.
The statement is parameterized by the graph and budget, not by 29 or 58.
Meeting the chosen triangle is sufficient; pairwise intersection of all
triangles is a stronger hypothesis that implies it.

The reusable `card_induce_compl_add_sum_degrees` proves the exact deletion
identity for **every** vertex subset: the remaining induced edge count
plus the sum of the deleted vertices' ambient degrees equals the ambient
edge count plus the deleted subset's induced edge count. There is no
truncated subtraction or missing correction for internal deleted edges.
For a triangle, its internal edge count is exactly three.

The proof partitions native neighbor finsets and swaps two finite sums to
equate the two orientations of the cut. Handshaking on the two induced
graphs and the ambient graph gives the identity. Native clique transfer
shows that a triangle remaining after deletion would contradict the
intersection hypothesis. The previous induced-to-ambient theorem then
supplies the actual clique witnesses.

| New declaration in `AlbertsonTriangleDeletion` | Role |
|---|---|
| `degree_induce_eq_card_inter` | Identifies an induced degree with the ambient neighbor intersection. |
| `sum_card_neighbor_inter` | Handshaking inside the actual induced graph. |
| `sum_card_neighbor_inter_comm` | Swaps the two orientations of a finite cut. |
| `card_induce_compl_add_sum_degrees` | Exact deletion identity for an arbitrary vertex subset. |
| `card_induce_triangle` | The induced triangle has exactly three edges. |
| `card_delete_triangle_add_sum_degrees` | Exact triangle-deletion identity. |
| `card_delete_triangle_bound` | Uniform edge-loss bound from the ambient maximum degree. |
| `cliqueFree_induce_compl` | A set meeting all triangles has triangle-free complement-induced graph. |
| `exists_disjoint_compl_cliques_of_triangle` | Composes the full finite input-to-clique bridge. |

## Obtaining the triangle from a deletion coloring

[AlbertsonColoringClique.lean](AlbertsonColoringClique.lean) removes the
separately supplied triangle from the final endpoint. Its first theorem
is fully parameterized: if a properly colored finite graph has more
vertices than the number of available colors times a natural number,
its complement has an actual clique of size one greater than that natural
number. The coloring need not be optimal or use every available color.

The proof uses Mathlib's strong finite-fiber pigeonhole theorem, selects
a subset of the required size from one color class, and uses properness
to prove its clique status in the complement. The induced version maps
that actual vertex set into the ambient graph, retaining containment and
cardinality. It does not need the ambient vertex type to be finite.

At ambient order twice a positive parameter, one vertex deletion of the
complement colorable with one fewer color than that parameter supplies
a triangle avoiding the deleted vertex. This uses no special cover,
matching, connectivity, optimal coloring or Stehlík theorem.

The composed endpoint assumes that every two ambient triangles meet and
the same positive edge budget as above. It returns the extracted triangle
and two disjoint complement cliques outside it, with the previous bounds.
Only one specified deletion needs a coloring; there is no universal
deletion-colorability premise.

| Declaration in `AlbertsonColoringClique` | Role |
|---|---|
| `exists_compl_clique_of_coloring` | Parameterized finite-coloring pigeonhole witness. |
| `exists_clique_of_induced_compl_coloring` | Actual clique transferred into the ambient graph. |
| `exists_triangle_of_deletion_colorable` | Extracts a triangle avoiding one deleted vertex. |
| `exists_disjoint_compl_cliques_of_deletion_colorable` | Composes extraction, deletion accounting and the disjoint-clique bound. |

## Proof architecture

The edge-existence lemma does not require triangle-freeness. Summing the
degree of the first endpoint over native oriented edges counts each
vertex's degree as many times as that degree. Reversing oriented edges
gives the same degree-square sum at the second endpoints. Cauchy–Schwarz
and the handshaking lemma then force an edge with the required
endpoint-degree sum.

In a triangle-free graph each endpoint's neighborhood is independent,
and adjacent endpoints have disjoint neighborhoods. Taking those actual
neighborhoods gives the two complement cliques. For the induced version,
native graph embeddings and finite-set maps preserve their clique proofs,
disjointness and sizes. The embedding of each induced neighborhood into
the ambient neighborhood proves the maximum-degree bound.

| Declaration | Role |
|---|---|
| `sum_dart_fst_degree` | First-endpoint weighted count equals the degree-square sum. |
| `sum_dart_snd_degree` | The same identity at second endpoints by dart reversal. |
| `exists_adj_degree_sum` | An actual adjacent pair satisfies the integer degree-sum bound. |
| `disjoint_neighborSet_of_triangleFree` | Adjacent endpoints have disjoint actual neighborhoods. |
| `exists_disjoint_compl_cliques` | Two disjoint complement cliques with size and maximum-degree bounds. |
| `exists_disjoint_compl_cliques_in_induce` | The full induced-to-ambient graph interface. |

The neighborhood-disjointness lemma itself needs neither a finite vertex
type nor a decidable adjacency relation. Other declarations use native
Mathlib finiteness and decidability interfaces.

## Exact Albertson consumer

[Audit.lean](Audit.lean) type-checks the height-3014 input: a triangle-free
induced graph on 55 vertices with at least 729 edges, inside an ambient
graph of maximum degree at most 29. The conclusion is two disjoint actual
cliques in the ambient complement, both inside the selected vertices,
each of size at most 29 and with combined size at least 54.

This is a conditional theorem application. It does not construct such a
graph or prove that an Albertson counterexample supplies these premises.
The additional end-to-end application starts with an ambient graph on 58
vertices, at least 813 edges, maximum degree at most 29, and a chosen
triangle meeting every triangle. It derives the same combined-size
threshold 54; residual triangle-freeness and the 729-edge lower bound are
now proved, not assumed. This single monotone input covers ambient edge
counts 813, 814 and 815, conditionally on the stated structural premises.

Boundary tests cover an empty graph's absence of an edge witness, deletion
of the entire three-vertex complete graph, and the empty deletion set.
The entire-triangle case has zero residual edges, so it does not meet the
positive residual-budget hypothesis.

The newest end-to-end example replaces the chosen triangle with one
28-colorable vertex deletion of the ambient complement, keeping the
58-vertex, at-least-813-edge, degree-at-most-29 and triangle-intersection
premises. It returns an actual triangle and the two cliques of combined
size at least 54. No triangle existence theorem is assumed.

Two concrete coloring tests check the strict threshold. The canonical
two-coloring of the complete bipartite graph with parts of size three
produces a complement triangle. With parts of size two instead, there
are exactly twice as many vertices as colors, but the complement is
triangle-free: equality cannot replace strict pigeonhole excess.
All eight examples are kernel-checked.

## Reproduction

Run inside this directory:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
```

The cache command is optional acceleration. The project pins its toolchain
and Mathlib revision; `lake-manifest.json` pins transitive dependencies.
Do not update dependencies to reproduce this checkpoint.

Expected result:

```text
Build completed successfully (1285 jobs).
Nineteen audited declarations: propext, Classical.choice, Quot.sound only.
Three conditional applications and five concrete or boundary tests compile.
```

Lean is `leanprover/lean4:v4.33.1`, release commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Lake is
`5.0.0-src+819816b`; Mathlib is
`0df444a360eaa60ab8c11dca51a86af692955474`.

## Status, literature and trust boundary

The selected graph contribution is
`bafkreiafu3krb262eyahjjcr7ctiei5vqluq2wqri5vqxrcb26hjfgfpe4`,
height 3014, whose [author source](https://github.com/abuzar08/discovery-net-notes/blob/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/order2r.py)
contains the triangle-free branch. This project formalizes its finite
triangle-deletion-to-clique chain, not the crossing-number conclusion.
The independent height-3064 review accepts the triangle branch while
correcting the crossing constant obtained from its stated seeding.
That numerical discrepancy does not enter this project, which assumes
no crossing-number constant. The review is not a review of these Lean
modules. Its [public evidence directory](https://github.com/abuzar08/discovery-net-notes/tree/main/reviews/albertson-order-58-branch)
records the separate checks. The later review was read from committed
RPC transactions because the prescribed local graph index remained at
height 3052; all 23 committed transactions after that height through
3098 were inspected for current scope and overlap.

The degree-square argument is classical. Christoph Spiegel's
[2024 formal treatment of the related Mantel proof](https://thebook.zib.de/graph%20theory/2024/10/15/mantel-cauchy-schwarz.html)
was consulted for literature and library context. The present source uses
native dart fibers and reversal and exports the existential clique witness;
it makes no new mathematical priority or first-formalization claim.

The coloring argument is the classical independence-number pigeonhole
bound. The [Mathlib pigeonhole documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/Pigeonhole.html)
describes the reused finite-fiber theorem. The implementation uses the
project's pinned Mathlib revision; the moving documentation page is
context, not a formal dependency.

Trust consists of the ordinary Lean kernel, the three axioms reported above,
the pinned Mathlib source and the toolchain. No proof hole, custom axiom,
native-evaluation shortcut, unsafe declaration, external solver, numerical
table, generated graph, certificate decoder or data oracle is used.

Unformalized surrounding inputs are critical-graph reductions supplying
the deletion coloring, the triangle-intersection branch assumption,
the ambient degree and edge premises,
crossing-number lower bounds for complete graphs, and the drawing argument
that disjoint clique subgraphs give an additive lower bound. No
unconditional Albertson theorem or new complete row elimination is claimed.
Given the explicit deletion-coloring input, triangle existence, residual
triangle-freeness and deletion edge accounting are now all formalized.
See [AUDIT.md](AUDIT.md) for the precise evidence boundary.
