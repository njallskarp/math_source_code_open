# Boundary eigenvalues and line-graph signature amplifiers

For a connected simple graph `G`, let `s(L(G))` denote the adjacency
signature of its line graph and let

```text
c(G) = |E(G)| - |V(G)| + 1.
```

The open sharp cyclomatic conjecture is

```text
2 s(L(G)) <= c(G) + 1.                                      (1)
```

This note gives an exact algebraic reduction for one natural counterexample
mechanism: zero-response rooted modules.

## Boundary-to-amplifier criterion

Let `J` be a connected simple graph such that:

1. `2` is a simple eigenvalue of its signless Laplacian `Q(J)`;
2. `2 s(L(J)) = c(J) + 1`.

Choose a `2`-eigenvector `y` of `Q(J)` and a vertex `v` with `y_v != 0`.
Form `M` by adjoining a new leaf `r` at `v`, and regard `r` as the root.
Write `rho = rv` for the root edge and `K = A(L(M))`. Then

```text
K is invertible,
(K inverse)_[rho,rho] = 0,
s(L(M)) = s(L(J)),
c(M) = c(J).
```

Starting from `C5` and attaching `k` disjoint copies of this rooted module
therefore gives connected simple graphs `G_k` satisfying

```text
c(G_k) = 1 + k c(J),
s(L(G_k)) = 1 + k (c(J)+1)/2,
2 s(L(G_k)) - (c(G_k)+1) = k.
```

Thus one boundary graph `J` with a simple signless-Laplacian eigenvalue `2`
would disprove (1) by an infinite family.

Conversely, every rooted-leaf graph `M` for which `A(L(M))` is invertible
and its inverse has zero diagonal at the root edge arises this way after
deleting the root leaf. The resulting graph `J` has a simple `2`-eigenvalue
of `Q(J)`, the corresponding eigenvector is nonzero at the attachment
vertex, and `s(L(J)) = s(L(M))`.

## Proof

Let `R` be the unsigned vertex-edge incidence matrix of `J` and put

```text
B = A(L(J)) = R^T R - 2 I.
```

The multiplicity of `2` in `Q(J) = R R^T` equals the nullity of `B`, since
the two Gram matrices have the same nonzero eigenvalues with multiplicity.
Hence `ker(B)` is one-dimensional. If `Q(J)y = 2y`, set

```text
x = (1/2) R^T y.
```

Then `Bx = 0` and `Rx = y`. Let `z = R^T e_v`, the indicator of the edges
of `J` incident with `v`. Therefore

```text
z^T x = e_v^T R x = y_v != 0.                              (2)
```

Ordering the root edge last gives the bordered matrix

```text
        [ B    z ]
K   =   [        ].                                         (3)
        [ z^T  0 ]
```

Use a congruence to split `B` into its nonsingular part and one zero
coordinate. Equation (2) says that the border couples nontrivially to that
zero coordinate. After eliminating the nonsingular part, the remaining
two-dimensional block has negative determinant and hence inertia `(1,0,1)`.
Thus

```text
In(B) = (p,1,n)  implies  In(K) = (p+1,0,n+1).              (4)
```

This proves invertibility and preservation of signature. The
`(rho,rho)` cofactor of `K` is `det(B)=0`, so Cramer's formula gives the
zero inverse diagonal. Adding a leaf preserves cyclomatic number.

For any host `H`, the adjacency matrix after identifying the root with a
vertex of `H` has off-diagonal coupling only through the root-edge
coordinate. Schur elimination of `K` changes the host block by the root
inverse diagonal times a rank-one matrix. That scalar is zero, so line-graph
inertia is additive. Repeated attachment to `C5` proves the formulas for
`G_k`.

For the converse, delete the root-edge row and column of `K`; the result is
`B = A(L(J))`. The zero inverse diagonal gives `det(B)=0`, while principal
interlacing with nonsingular `K` forces `nullity(B)=1`. If the border were
orthogonal to `ker(B)`, then `K` would remain singular, so the coupling is
nonzero. Reversing the incidence argument supplies the asserted simple
`2`-eigenvalue and nonzero eigenvector coordinate. The same hyperbolic-pair
argument proves signature preservation.

## Reproduction

The checker uses Python standard-library exact integer and rational
arithmetic. It verifies the incidence identities, exact inertias, singular
principal minor, and inverse-cofactor mechanism on Paone's rooted
`C4--C5` zero-response module.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
```

Expected final line:

```text
RESULT_SHA256=ff0955a9847d73d4bfce22f4bc14562379a96f4a0a7996399de72cca76e65997
```

The universal result is the proof above. The finite checker validates its
algebraic mechanism on a canonical module; it is not evidence for the
universal quantifiers. Exploratory numerical searches are excluded from the
claim.

## Literature boundary

The incidence identities and Schur complements are classical. Paone gives
the explicit `C4--C5` zero-response module and an unbounded-signature
family. Paone and Paone formulate (1), derive exact pendant-tree response
formulas, and leave (1) open. Francis and Uptain independently construct
unbounded line-graph signature. The contribution here is the exact
boundary-to-amplifier equivalence, not those ingredients or a proof of (1).

Primary sources checked:

- Andrea Paone, *Unbounded signature of line graphs: counterexamples and
  transfer mechanisms*, version 2, <https://doi.org/10.5281/zenodo.21534809>.
- Andrea Paone and Marco Paone, *Line-Graph Signature Beyond the 2-Core*,
  version 1.3, <https://aletheia-technologies.it/research/line-graph-signature-beyond-the-2-core/reader/>.
- Luke Francis and Trevor Uptain, *The signature of connected line graphs is
  unbounded*, <https://arxiv.org/abs/2607.22874>.
- Saieed Akbari et al., *A new conjecture on the inertia of graphs*,
  <https://arxiv.org/abs/2508.01163>.
