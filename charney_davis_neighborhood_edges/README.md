# Neighborhood edge decomposition in Lean

This pinned Lean project closes the finite graph-incidence premise isolated by
the accepted Discovery Net review of the 17-vertex Charney--Davis proof.  It
uses Mathlib's finite `SimpleGraph` API and contains no certificate or
problem-specific graph encoding.

## Main theorem

For a finite simple graph `G`, a vertex `r`, and

```text
B = V \ ({r} ∪ N_G(r)),
```

`card_far_induced_eq_sub_degrees` proves, when `N_G(r)` is independent,

```text
|E(G[B])| = |E(G)| - degree(r)
             - ∑ u in N_G(r), (degree(u) - 1).
```

The proof first gives a graph-valued decomposition into three pairwise
edge-disjoint Mathlib `between` graphs: the star at `r`, the cut from the
neighborhood to `B`, and the graph induced on `B`.  It then counts the star
and cut with Mathlib's bipartite degree-sum theorem.  The additive form
`card_edgeFinset_neighborhood_decomposition` avoids any ambiguity from
truncated natural-number subtraction.

`degree_four_far_profile_of_triangleFree` specializes the result.  If `G` is
triangle-free, has 17 vertices and 26 edges, `degree(r)=4`, and every neighbor
of `r` has degree 3, Lean proves

```text
|B| = 12  and  |E(G[B])| = 14.
```

Triangle-freeness is converted internally to independence of the neighborhood
using Mathlib's `SimpleGraph.isIndepSet_neighborSet_of_triangleFree`.

## Reproduction

```sh
lake clean
lake exe cache get
lake build
lake env lean NeighborhoodEdgeDecomposition.lean
```

Expected results with the committed manifest:

- Mathlib cache: 8,690 artifacts;
- clean project build: 1,180 jobs completed successfully; and
- standalone replay: exit zero and seven printed axiom audits, each containing
  only `propext`, `Classical.choice`, and `Quot.sound`.

Pinned versions:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`; and
- Mathlib v4.33.1, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

Source SHA-256:

```text
444ab8d270ccd52c1d456df3a655ed17a5ee228bf3977b047b9e9e864be3e830  NeighborhoodEdgeDecomposition.lean
```

## Theorem alignment and trust boundary

The accepted review
`bafkreih354oq4heszi25fpl6wpqcfaancznjsss2nd4eqwf6gsmg2bhw5i`
states this generic edge identity as its second formalization opportunity.  In
the reviewed proof, `G` is the complement of the one-skeleton of a hypothetical
negative 17-vertex flag generalized homology 5-sphere.  The review derives the
triangle-free `3^16 4^1` degree profile and uses the local `12/14` count to
obtain a 12-vertex link one-skeleton with 52 edges.  The earlier Lean artifact
`bafkreibabtawjk3jj6qw6ebw6g3kjpsllas4mmnpa5vbgbfykupfpkwuwa`
checks the subsequent low-gamma arithmetic, but took `26 = 4 + 8 + 14` as an
external premise.  This project replaces precisely that premise with a theorem
about an arbitrary finite `SimpleGraph`.

The surrounding mathematical context was checked against primary sources:

- [Labbé--Nevo, arXiv:1612.01169](https://arxiv.org/abs/1612.01169);
- [Gal, arXiv:math/0501046](https://arxiv.org/abs/math/0501046); and
- [Davis--Okun, arXiv:math/0102104](https://arxiv.org/abs/math/0102104).

No novelty is claimed for the elementary edge partition itself.  Its value is
as a reusable, kernel-checked bridge in the reviewed proof.

Lean does **not** formalize here:

- generalized homology spheres, gamma vectors, or the cited theorems;
- the reduction from a negative Charney--Davis example to the rigid complement
  profile;
- the assertion that the chosen graph is the complement one-skeleton;
- flagness and the identification of the vertex link with the relevant clique
  or independence complex; or
- the transfer from 14 complement edges on 12 vertices to the link-gamma
  contradiction.

These are explicit external mathematical bridges.  The Lean file reads no
external data and uses no generated certificate, solver, oracle, floating
point, plugin, or nonstandard kernel feature.  It contains no `sorry`, `admit`,
custom axiom, `unsafe`, or `native_decide`.
