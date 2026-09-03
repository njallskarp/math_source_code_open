# Formalization audit

## Exact interface

The project works over

```lean
{V : Type*} [Fintype V] [DecidableEq V]
(G : SimpleGraph V) [DecidableRel G.Adj]
```

and defines

```lean
farVertices G r = (insert r (G.neighborFinset r))ᶜ.
```

Thus `farVertices G r` is exactly the finite set of vertices unequal to `r`
and not adjacent to `r`.

Given the sole structural hypothesis

```lean
G.IsIndepSet (G.neighborSet r),
```

`graph_eq_star_sup_cross_sup_far` proves equality of `G` with the supremum of:

1. edges between `{r}` and `N_G(r)`;
2. edges between `N_G(r)` and `farVertices G r`; and
3. edges within `farVertices G r`.

The three pairwise-disjointness lemmas establish uniqueness of the edge
classes.  `card_edgeFinset_star` and `card_edgeFinset_cross` use
`SimpleGraph.isBipartiteWith_sum_degrees_eq_card_edges`.  For a neighbor `u`,
`neighborFinset_cross_eq_erase` proves that its cross-neighbors are exactly
`(G.neighborFinset u).erase r`, so its cut degree is `G.degree u - 1`.

Consequently:

```lean
#G.edgeFinset =
  G.degree r + (∑ u ∈ G.neighborFinset r, (G.degree u - 1)) +
    #((G.induce (↑(farVertices G r) : Set V)).edgeFinset)
```

and the reviewed subtraction form follows as

```lean
#((G.induce (↑(farVertices G r) : Set V)).edgeFinset) =
  #G.edgeFinset - G.degree r -
    ∑ u ∈ G.neighborFinset r, (G.degree u - 1).
```

`card_farVertices` independently proves

```text
|B| = |V| - (degree(r) + 1).
```

The headline specialization imports only these numerical hypotheses:

```text
|V|=17, |E(G)|=26, degree(r)=4,
degree(u)=3 for every u in N_G(r), and CliqueFree G 3.
```

Mathlib supplies `CliqueFree G 3 -> IsIndepSet G (neighborSet G r)`, after
which Lean derives `|B|=12` and `|E(G[B])|=14`.

## What is and is not formalized

Formalized:

- the vertex trichotomy `{r}`, `N_G(r)`, and `B`;
- equality of the three edge-class graphs;
- pairwise disjointness of their finite edge sets;
- star and neighborhood-to-far degree sums;
- both additive and subtraction forms of the generic identity;
- triangle-free neighborhoods being independent via an existing Mathlib
  theorem; and
- the exact 17-vertex `12/14` consequence.

Not formalized:

- derivation of the `3^16 4^1` complement profile from a negative
  Charney--Davis counterexample;
- simplicial complexes, generalized homology-sphere conditions, or gamma
  polynomials;
- the complement one-skeleton and flag-link identifications; or
- the published Gal, Labbé--Nevo, and Davis--Okun inputs.

This is therefore a formalization of the finite graph-incidence bridge, not an
end-to-end formalization of the 17-vertex Charney--Davis theorem.

## Verification record

With Lean 4.33.1 and Mathlib v4.33.1 pinned by `lean-toolchain`,
`lakefile.toml`, and `lake-manifest.json`:

```text
lake clean                         success
lake exe cache get                 8,690 artifacts available
lake build                         1,180 jobs completed successfully
lake env lean NeighborhoodEdgeDecomposition.lean
                                   success
```

All seven audited declarations report only:

```text
propext, Classical.choice, Quot.sound
```

The source scan found none of `sorry`, `admit`, a custom `axiom`, `unsafe`, or
`native_decide`.  There is no external executable or data boundary.

```text
444ab8d270ccd52c1d456df3a655ed17a5ee228bf3977b047b9e9e864be3e830
```

is the SHA-256 of `NeighborhoodEdgeDecomposition.lean`.
