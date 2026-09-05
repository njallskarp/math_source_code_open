# Critical-vertex neighborhood obstruction

A standalone Lean formalization of the neighborhood-folding principle and its
complement non-domination consequence. This closes the **local non-domination
and clique-barrier bridge** used at Discovery Net height 2933; it does not
verify that artifact's order-58 enumeration or crossing-number conclusion.

## Exact theorem and removed dependencies

If `a ≠ w` and `N_G(a) ⊆ N_G(w)`, folding a onto w gives an actual graph
homomorphism from G to the induced graph G-a. Inclusion gives a homomorphism
back. Therefore

    χ(G-a) = χ(G).

The Lean theorem is `chromaticNumber_delete_eq_of_neighborSet_subset`.
It uses Mathlib's native `SimpleGraph`, `neighborSet`, `induce`, graph
homomorphisms, and extended-natural `chromaticNumber`. The graph may be
infinite; no palette cardinality or external colorability summary is used.

Consequently, if deleting a strictly lowers χ(G), and H = Gᶜ has the edge wa,
then some vertex u satisfies

    wu ∈ E(H), u ≠ a, au ∉ E(H).

This is `exists_compl_neighbor_not_adjacent`. Thus a cannot dominate all the
other H-neighbors of w. The theorem needs strict chromatic drop only at a.
It does **not** need order 2r, complement connectivity, a barrier, Stehlik's
deletion-cover theorem, large color classes, matching existence, or a special
triangle/edge partition. Those dependencies are unnecessary for this step.

The native-set consumer `not_isClique_of_neighborSet_subset` states: if every
vertex deletion strictly lowers χ(G), `N_H(w)` is nonempty, and
`N_H(w) ⊆ B`, then B is not an H-clique. This is the local contradiction used
when a clique barrier leaves a singleton component. The nonempty-neighborhood
premise is explicit; a universal vertex of G can be isolated in H, and that
case is not excluded by criticality alone.

## Proof architecture

`foldHom` fixes every vertex except a, which maps to w. Neighborhood inclusion
proves edge preservation. It also precludes an edge aw, without a separate
nonadjacency assumption. Chromatic-number monotonicity in both directions
gives equality. Strict chromatic drop contradicts the fold.

`neighborSet_subset_of_compl_domination` proves the exact complement
translation: the hypothesized local H-domination would give
`N_G(a) ⊆ N_G(w)`. Its contrapositive yields the explicit witness u. A clique
containing every H-neighbor of w would connect a to this u, a contradiction.

There are five exported theorems and one explicit homomorphism constructor.
No other campaign Lean project is imported.

## Literature and claim status

The no-comparable-neighborhood property of vertex-critical graphs is folklore,
explicitly recalled in Section 2, immediately before Lemma 2 of Cameron,
Goedgebeur, Huang and Shi, *k-Critical graphs in P5-free graphs*, Theoretical
Computer Science 864 (2021), 80–91,
[DOI 10.1016/j.tcs.2021.02.029](https://doi.org/10.1016/j.tcs.2021.02.029).
No new mathematical priority is claimed.

The specific campaign consumer is the non-domination proof and clique-barrier
corollary in the opening documentation of
[height 2933's order2r.py](https://github.com/abuzar08/discovery-net-notes/blob/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/order2r.py).
That argument splits the deleted color class into edge/triangle cases using
Stehlik. The folding proof covers both at once and removes the special
deletion-cover existence dependency from this local step. This is formalization
authoring, not an independent review of the complete height-2933 result.

## Reproduce

From this directory, with Elan installed:

    lake exe cache get
    lake build
    lake env lean Audit.lean

Lean `leanprover/lean4:v4.33.1`, release commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Lake `5.0.0-src+819816b`;
Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`.
The toolchain and transitive dependency manifest are pinned. Do not run
`lake update` for this version. Dependency caches are optional accelerators.

Expected: complete build succeeds (1004 jobs on the recorded runs); all six
audited declarations use only `propext`, `Classical.choice`, and `Quot.sound`.
No sorry, admit, custom axiom, native_decide, unsafe shortcut, generated input,
external solver, or data oracle is used. See [AUDIT.md](AUDIT.md).

## Explicit application boundary

Supplying the actual critical graph is external. The clique-barrier consumer
takes actual neighborhood containment and nonemptiness as hypotheses; it does
not construct a Tutte barrier or derive those facts from a singleton-component
encoding. All separator enumerations, the two-singleton disjoint-neighbor
argument, degree-excess bounds, Gallai spectra, crossing estimates, drawings,
and the alpha(G) >= 4 order-58 elimination remain outside this formalization.
No r=29 row or order family is claimed eliminated by this project.
