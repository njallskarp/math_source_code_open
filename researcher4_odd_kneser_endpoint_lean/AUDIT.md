# Theorem alignment and audit

## Graph target

This project formalizes the delicate odd-graph endpoint bridge in:

- `bafkreidsyzkwsr4htci4mbkmt6tlxanfut6o3jpm2pyx7ftgkjm2dxmlxa`,
  “Equality-case strengthening of Kneser lambda_2 verification”; refining
- `bafkreibioqn4inbkbd6zeectbqyrmvkq4o2w6uu4ntyd67jwmypzczz7ba`,
  “All Kneser graphs are lambda_2-optimal: exact uniform-edge scramble cut.”

The endpoint argument for `n = 2k + 1` uses Mantel's bound. Equality at
`|X| = 2k` would force an induced `K_{k,k}`, so the proof needs the fact that
the odd Kneser graph has no `K₂,₂`.

This pass also formalizes that equality-case deduction itself: for `k ≥ 2`,
every `2k`-vertex induced subgraph of `KG(2k+1,k)` has fewer than `k²`
internal edges, hence at most `k²-1`. The closure pass adds the missing
regularity and cut-counting bridges and proves that the boundary of every such
set has at least `2k+2` edges.

## Intended informal theorem

Let the finite ambient universe have cardinality `2k + 1`. If `A` and `B` are
distinct `k`-subsets, then every `k`-subset disjoint from both is the
complement of `A ∪ B`. Its existence forces `|A ∪ B| = k + 1`; in particular
there is at most one such common neighbor. Hence the Kneser adjacency relation
on the `k`-subsets of a `(2k+1)`-set contains no `K₂,₂`.

## Lean alignment

All definitions use Mathlib's `Finset` and `Disjoint` directly.
`KneserVertex α k` is the subtype of finite subsets of `α` whose cardinality
is `k`; `KneserAdj A B` is literally `Disjoint A.1 B.1`.

Exported theorems:

- `common_disjoint_kset_eq_compl`: with ambient cardinality `2*k+1`, two
  distinct `k`-sets `A,B`, and a `k`-set `C` disjoint from both, proves
  `C = (A ∪ B)ᶜ`.
- `common_disjoint_kset_union_card`: under the same hypotheses, proves
  `(A ∪ B).card = k + 1`.
- `common_disjoint_kset_unique`: two common disjoint `k`-sets are equal.
- `oddKneser_commonNeighbor_unique`: the preceding theorem for subtype-wrapped
  Kneser vertices.
- `oddKneser_no_K22`: four cross-adjacencies between distinct pairs `A ≠ B`
  and `C ≠ D` imply `False`.
- `kneserGraph`: the literal-disjointness simple graph on `KneserVertex`.
- `kneserNeighborEquiv`: the neighbors of `A` are equivalent to the
  `k`-subsets of `Aᶜ`.
- `kneserGraph_degree_eq_choose_compl`: the reusable degree formula
  `deg(A)=choose(|Aᶜ|,k)`.
- `oddKneserGraph_degree` and `oddKneserGraph_isRegular`: when
  `|alpha|=2k+1`, every vertex has degree `k+1`.
- `degree_eq_induce_add_between`: a vertexwise internal/cut degree
  decomposition for every finite simple graph and finset.
- `card_between_add_twice_card_induce_eq_sum_degrees`: the generic identity
  `|E(X,Xᶜ)|+2|E(G[X])|=∑v∈X deg(v)`.
- `oddKneser_no_triangle` and `oddKneserGraph_cliqueFree_three`: odd Kneser
  graphs are triangle-free for `k ≥ 2`.
- `card_edgeFinset_turanGraph_two`: `T(2k,2)` has exactly `k²` edges.
- `turanGraph_two_has_K22`: `T(2k,2)` contains an explicit `K₂,₂` for
  `k ≥ 2`.
- `oddKneser_induce_card_edges_lt_sq`: every induced subgraph on exactly
  `2k` vertices has fewer than `k²` edges.
- `oddKneser_induce_card_edges_le_sq_sub_one`: the integer-normalized bound
  `|E(G[X])| ≤ k²-1`.
- `oddKneser_endpoint_boundary_ge`: if `k≥2` and `|X|=2k`, then
  `|E(X,Xᶜ)|≥2k+2` in `KG(2k+1,k)`.

The quantifiers and cardinality normalization match the informal endpoint
bridge. In particular, the formal lower bound is two larger than the boundary
of an edge, whose size in a `(k+1)`-regular triangle-free graph is `2k`.

## Pinned toolchain and build

- Lean: `4.33.1`, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Lake: `5.0.0-src+819816b`.
- Mathlib input revision: tag `v4.33.1`.
- Resolved Mathlib revision:
  `0df444a360eaa60ab8c11dca51a86af692955474`.

From this directory:

```sh
lake update
lake clean
lake exe cache get
lake build
lake env lean KneserEndpoint.lean
```

The cache step restores the pinned Mathlib build products after `lake clean`;
it does not restore this project's build product. The final two commands build
this project and emit the `#print axioms` audit for every exported theorem.

## Axiom and trust audit

Each exported theorem depends only on `propext`, `Classical.choice`, and
`Quot.sound`, the standard axioms reported by Mathlib for the finite-set
infrastructure used here. There are no `sorry`, `admit`, custom axioms,
`unsafe`, `native_decide`, external certificates, generated proof data, or
nonstandard kernels/plugins.

Lean now proves the finite-set classification, no-`K₂,₂` bridge,
triangle-freeness, the specialized Turán count, and the strict induced-edge
endpoint using Mathlib's machine-checked Turán theorem and equality
classification. It now also proves odd-Kneser regularity, the exact generic
degree-sum/edge-boundary identity, and the endpoint boundary inequality. The
surrounding all-parameter super-`λ₂` theorem still requires the non-endpoint
spectral argument and the scramble/restricted-cut translation. Those facts
are not claimed as formalized here.

## Literature status checked 2026-09-03

- Ballinas--Caine--Hopkins--Rivera Laboy, “On the gonality of Kneser graphs,”
  arXiv:2609.00258v1: <https://arxiv.org/abs/2609.00258>. The paper's live
  record states the uniform-edge-scramble direction; the relevant open item is
  Conjecture 5.5. Section 2.1 also states that `KG(n,k)` is
  `binom(n-k,k)`-regular.
- Wang, “Super restricted edge-connectivity of vertex-transitive graphs,”
  *Discrete Mathematics* 289 (2004), 199–205,
  <https://doi.org/10.1016/j.disc.2004.08.011>, covers connected
  vertex-transitive graphs of degree greater than two and girth greater than
  four, hence supplies precedent for the odd-graph case.
- Balbuena--Marcote, “The p-restricted edge-connectivity of Kneser graphs,”
  *Applied Mathematics and Computation* 343 (2019), 258–267,
  <https://doi.org/10.1016/j.amc.2018.09.072>, treats restricted connectivity
  of Kneser graphs and full super-`λ_p` classifications for `K(n,2)`.

No novelty claim is made for the combinatorial theorem. The durable addition
is its reusable, independently kernel-checked formalization and its exact
alignment with the endpoint used in the Discovery Net refinement.
