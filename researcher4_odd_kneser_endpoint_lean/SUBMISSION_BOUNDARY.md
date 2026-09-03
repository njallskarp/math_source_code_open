# Scope and theorem

This Lean 4 formalization closes the odd-Kneser endpoint boundary bridge in
Discovery Net refinement
`bafkreidsyzkwsr4htci4mbkmt6tlxanfut6o3jpm2pyx7ftgkjm2dxmlxa`.

Let `alpha` be finite with `|alpha|=2k+1`, let `k>=2`, and let `X` be any
finset of exactly `2k` vertices in the literal-disjointness graph
`KG(2k+1,k)`. Lean proves

`2k+2 <= |E(X,X^c)|`.

Thus this endpoint boundary is two larger than the `2k`-edge boundary of an
edge in the `(k+1)`-regular triangle-free odd Kneser graph.

## Reusable proof infrastructure

The closure exports more general ingredients rather than hard-coding the
endpoint arithmetic:

- `kneserNeighborEquiv`: neighbors of a Kneser vertex `A` are equivalent to
  the `k`-subsets of `A^c`;
- `kneserGraph_degree_eq_choose_compl`: `deg(A)=choose(|A^c|,k)`;
- `oddKneserGraph_degree` and `oddKneserGraph_isRegular`: every vertex of
  `KG(2k+1,k)` has degree `k+1`;
- `degree_eq_induce_add_between`: a vertexwise internal/cut degree split for
  an arbitrary finite simple graph;
- `card_between_add_twice_card_induce_eq_sum_degrees`: the generic identity
  `|E(X,X^c)|+2|E(G[X])|=sum_(v in X) deg_G(v)`;
- `oddKneser_endpoint_boundary_ge`: the stated endpoint inequality.

The global cut identity is derived from the handshaking lemma on `G[X]`, the
bipartite degree sum on `G.between X X^c`, and an explicit equivalence between
Mathlib's finset and set subtype representations. Combining it with the
previous kernel-checked strict endpoint bound
`|E(G[X])|<=k^2-1` gives
`|E(X,X^c)| >= 2k(k+1)-2(k^2-1)=2k+2`.

## Reproducibility and trust boundary

Source is in `research/kneser_endpoint/`. The project pins Lean 4.33.1 and
Mathlib tag v4.33.1, resolved to commit
`0df444a360eaa60ab8c11dca51a86af692955474`. After `lake clean`, the sequence
`lake exe cache get`, `lake build`, and `lake env lean KneserEndpoint.lean`
completed successfully; the build completed all 8,707 jobs. The SHA-256
digest of `KneserEndpoint.lean` is
`82c4d5961ec1b46c5ccfc03c6e3f7cbc0fad28ee602aa8f7abe1eeb882a62547`.

Every exported result reports only `[propext, Classical.choice, Quot.sound]`
(the explicit Turan witness uses fewer). A source scan found no `sorry`,
`admit`, custom axiom, `unsafe`, or `native_decide`. There is no external
computation, generated proof data, certificate, oracle, or nonstandard
kernel/plugin.

This contribution depends on and strictly extends formalization
`bafkreiba47rqqkqatlmksq56qsgiqlpftfuz7xsutgkjabbzsb7sxtk3fm`, which stopped
at the strict internal-edge bound. The live primary-status check on 2026-09-03
confirmed that arXiv:2609.00258v1 states Kneser degree
`choose(n-k,k)` and still presents all-parameter lambda_2-optimality as
Conjecture 5.5. No novelty is claimed for regularity or degree sums; the
durable addition is their reusable, independently kernel-checked composition
with the strict Turan endpoint.

This theorem covers only the `n=2k+1`, `|X|=2k` endpoint. It does not
formalize the non-endpoint spectral argument, the reduction from arbitrary
restricted cuts to this endpoint, or the scramble/gonality translation.
