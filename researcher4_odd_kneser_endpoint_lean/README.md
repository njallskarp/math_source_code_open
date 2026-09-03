# Odd Kneser endpoint formalization

This pinned Lean project formalizes the set-theoretic obstruction used in the
`n = 2k + 1` endpoint of the direct super-restricted-edge-connectivity proof
for Kneser graphs.

The intended informal endpoint theorem is:

> In an ambient set of cardinality `2k + 1`, if `A` and `B` are distinct
> `k`-subsets, then there is at most one `k`-subset disjoint from both.
> Consequently `KG(2k+1,k)` contains no `K₂,₂`.
> Moreover, if `k ≥ 2`, every induced subgraph on exactly `2k` vertices has
> strictly fewer than `k²` edges (equivalently, at most `k²-1`), and its
> edge boundary has at least `2k+2` edges.

The graph theorem combines the reusable finite-set obstruction with Mathlib's
finite Turán theorem and equality classification. Equality in the triangle-free
edge bound would identify the induced graph with the balanced two-part Turán
graph; an explicit `K₂,₂` in that graph pulls back to the forbidden
configuration. It also packages the neighborhood equivalence proving the
general degree formula `deg(A)=choose(|Aᶜ|,k)`, odd-Kneser `(k+1)`-regularity,
and the generic finite-graph cut identity
`|E(X,Xᶜ)|+2|E(G[X])|=∑v∈X deg(v)`. The project does not formalize the
non-endpoint spectral bound or the scramble/restricted-cut translation.

Build with:

```sh
lake clean
lake exe cache get
lake build
lake env lean KneserEndpoint.lean
```
