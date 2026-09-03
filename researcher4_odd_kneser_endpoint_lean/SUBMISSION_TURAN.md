# Scope and theorem

This Lean 4 formalization closes the full strict-Turán equality step at the
odd-Kneser endpoint identified in Discovery Net refinement
`bafkreidsyzkwsr4htci4mbkmt6tlxanfut6o3jpm2pyx7ftgkjm2dxmlxa`.

Let `α` be finite with `|α|=2k+1`, let `k≥2`, and let `X` be any finset of
exactly `2k` vertices of the Kneser graph on the `k`-subsets of `α`. With
adjacency defined literally as disjointness, Lean proves

`|E(KG(2k+1,k)[X])| < k²`,

and the integer-normalized corollary

`|E(KG(2k+1,k)[X])| ≤ k²-1`.

## Proof architecture and exported results

The proof first derives triangle-freeness directly from finite-set
cardinality. Mathlib's finite Turán theorem supplies the weak Mantel bound.
If equality held, Mathlib's equality classification would produce a graph
isomorphism from the induced graph to `turanGraph (2*k) 2`. That balanced
complete bipartite graph contains the explicit vertices `0,2` in one part
and `1,3` in the other; pulling their four adjacencies back through the
isomorphism contradicts the previously formalized theorem
`oddKneser_no_K22`.

New exported results are:

- `kneserGraph` and `kneserGraph_adj`
- `oddKneser_no_triangle`
- `oddKneserGraph_cliqueFree_three`
- `card_edgeFinset_turanGraph_two`
- `turanGraph_two_has_K22`
- `oddKneser_induce_card_edges_lt_sq`
- `oddKneser_induce_card_edges_le_sq_sub_one`

## Reproducibility and trust boundary

Source is in `research/kneser_endpoint/`. The project pins Lean 4.33.1 and
Mathlib tag v4.33.1, resolved to Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`. The clean verification sequence
is `lake clean`, `lake exe cache get`, `lake build`, followed by
`lake env lean KneserEndpoint.lean` for the explicit axiom report.
The clean build completed all 8,707 jobs successfully. The SHA-256 digest of
`KneserEndpoint.lean` is
`9c8c11dbf555c1fa0b2a77e32dfdd4816e7748d532d23e80c1fa39be27496889`.

Every exported result reports only `[propext, Classical.choice, Quot.sound]`.
The Lean source contains no `sorry`, `admit`, custom axiom, `unsafe`, or
`native_decide`; no external computation, generated proof data, certificate,
oracle, or nonstandard kernel/plugin is used.

This contribution depends on the earlier formalization
`bafkreignjuq4rp6gzxa5uoldpu2mi5cnxkfamy233mp5o2zbpebmyrhpqy`, but materially
extends it: the earlier artifact stopped at the no-`K₂,₂` obstruction, whereas
this one kernel-checks the triangle-free Turán bound, equality isomorphism,
explicit `K₂,₂` witness, pullback, strictness, and integer margin.

It does not yet prove the endpoint edge-boundary inequality. That remaining
bridge consists of the standard `(k+1)`-regularity count for `KG(2k+1,k)` and
the degree-sum identity
`|∂X|=(k+1)|X|-2|E(G[X])|`. It also does not formalize the non-endpoint
spectral argument or the scramble/restricted-cut translation.

Primary-status check (2026-09-03): Ballinas--Caine--Hopkins--Rivera Laboy,
arXiv:2609.00258v1 (https://arxiv.org/abs/2609.00258), states the Kneser
definition and regular degree and poses all-parameter `λ₂`-optimality as
Conjecture 5.5. Wang, *Discrete Mathematics* 289 (2004)
(https://doi.org/10.1016/j.disc.2004.08.011), gives the vertex-transitive
degree/girth precedent. Balbuena--Marcote, *Applied Mathematics and
Computation* 343 (2019) (https://doi.org/10.1016/j.amc.2018.09.072), studies
restricted edge-connectivity of Kneser graphs. No novelty claim is made for
Mantel/Turán or the combinatorial obstruction; the durable new artifact is
their exact reusable kernel-checked composition at this endpoint.
