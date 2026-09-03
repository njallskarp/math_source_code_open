# A boundary-eigenvalue criterion for line-graph signature amplifiers

Let (s(L(G))) be the adjacency signature of the line graph of a connected
simple graph (G), and let

\[
c(G)=|E(G)|-|V(G)|+1.
\]

The open sharp cyclomatic bound is

\[
2s(L(G))\leq c(G)+1. \tag{1}
\]

This note gives an exact algebraic reduction for one natural way of attacking
(1): zero-response rooted modules.  It identifies the precise obstruction
that a counterexample search must find, and it turns any such obstruction into
an infinite counterexample family.

## The criterion

Write (Q(J)) for the signless Laplacian of (J).  Suppose that a connected
simple graph (J) has these two properties:

1. (2) is a simple eigenvalue of (Q(J));
2. (2s(L(J))=c(J)+1).

Choose a (2)-eigenvector (y) of (Q(J)), and choose a vertex (v) with
(y_v\ne0).  Form (M) by adjoining one new leaf (r) at (v), and regard
(r) as the root.  If (ho=rv), then

\[
K=A(L(M))\quad\hbox{is invertible},\qquad
(K^{-1})_{\rho\rho}=0,
\]

and

\[
s(L(M))=s(L(J)),\qquad c(M)=c(J).
\]

Consequently, starting from (C_5) and attaching (k) disjoint copies of
this rooted module gives connected simple graphs (G_k) satisfying

\[
c(G_k)=1+k c(J),\qquad
s(L(G_k))=1+k\frac{c(J)+1}{2},
\]

so

\[
2s(L(G_k))-(c(G_k)+1)=k.
\]

Thus even one graph (J) on the sharp boundary with a simple signless-
Laplacian eigenvalue (2) disproves (1), and does so by an infinite family.

Conversely, every rooted-leaf module (M) with invertible (A(L(M))) and
zero inverse diagonal at its root edge arises this way: deleting the root leaf
gives a connected graph (J) for which (2) is a simple eigenvalue of
(Q(J)), the associated eigenvector is nonzero at the neighbour of the
deleted leaf, and (s(L(J))=s(L(M))).

## Proof

Let (R) be the unsigned vertex-edge incidence matrix of (J), and put

\[
B=A(L(J))=R^{\mathsf T}R-2I.
\]

The multiplicity of (2) in (Q(J)=RR^{\mathsf T}) equals the nullity of
(B), because the two matrices have the same nonzero squared singular values.
Under the hypothesis, (ker B) is therefore one-dimensional.  If
(Q(J)y=2y), set

\[
x=\frac12R^{\mathsf T}y.
\]

Then (Bx=0) and (Rx=y).  Let (z=R^{\mathsf T}e_v), the indicator vector
of the edges of (J) incident with (v).  It follows that

\[
z^{\mathsf T}x=e_v^{\mathsf T}Rx=y_v\ne0. \tag{2}
\]

Ordering the root edge last gives

\[
A(L(M))=
\begin{pmatrix}
B&z\\ z^{\mathsf T}&0
\end{pmatrix}. \tag{3}
\]

Apply a congruence which writes (B) as its nonsingular part plus one zero
coordinate.  Equation (2) says that the last border couples nontrivially to
that zero coordinate.  The remaining (2\times2) block has negative
determinant, hence inertia ((1,0,1)).  Therefore, if

\[
\operatorname{In}(B)=(p,1,n),
\]

then

\[
\operatorname{In}(A(L(M)))=(p+1,0,n+1). \tag{4}
\]

This proves invertibility and preservation of signature.  Moreover, the
(ho,ho) cofactor in (3) is (det B=0), so Cramer's formula gives
((K^{-1})_{\rho\rho}=0).  Adding a leaf preserves cyclomatic number.

For any host (H), the line-graph adjacency matrix after identifying the
root with a vertex of (H) has block form

\[
\begin{pmatrix}
A(L(H))&w e_\rho^{\mathsf T}\\
e_\rho w^{\mathsf T}&K
\end{pmatrix}.
\]

Schur elimination of (K) changes the first block by
(- (K^{-1})_{\rho\rho}ww^{\mathsf T}=0).  Hence line-graph inertia is
additive under every such attachment.  Applying this repeatedly to (C_5)
proves the displayed formulas for (G_k).

For the converse, delete the root-edge row and column of (K).  The result is
(B=A(L(J))).  The zero inverse diagonal says (det B=0), while principal
interlacing with nonsingular (K) forces (dim\ker B=1).  If the border were
orthogonal to (ker B), then (K) would still be singular, so the coupling
is nonzero.  Reversing the incidence argument gives a simple (2)-eigenvalue
of (Q(J)) and an eigenvector nonzero at the attachment vertex.  The same
hyperbolic-pair argument gives (4), completing the converse.

## Reproduction

The checker uses only the Python standard library and exact integer/rational
arithmetic.  It verifies every matrix identity used by the reduction on the
published rooted (C_4\!-!C_5) zero-response module, including both incidence
identities, exact inertias, the singular principal minor, and the inverse
cofactor condition.

```sh
python3 verify.py
```

Expected final line:

```text
RESULT_SHA256=ff0955a9847d73d4bfce22f4bc14562379a96f4a0a7996399de72cca76e65997
```

The universal criterion is proved above; the finite computation is a
reproduction check of its algebraic mechanism, not evidence for the universal
quantifiers.  The exploratory search that selected this reduction is also not
part of the theorem: numerical filtering found no boundary obstruction among
connected graphs through nine vertices or among residue-reduced linear cactus
chains with one, three, or five cycles.

## Literature boundary

The incidence identities and Schur-complement tools are classical.  Paone's
rooted-module paper supplies the explicit (C_4\!-!C_5) zero-response module
and an unbounded-signature family.  Paone and Paone formulate (1), give exact
pendant-tree response formulas, and leave (1) open.  Francis and Uptain give an
independent unbounded-signature construction.  The present contribution is
the boundary-to-amplifier equivalence above, not those ingredients or a proof
of (1).

Primary sources checked:

- Andrea Paone, *Unbounded signature of line graphs: counterexamples and
  transfer mechanisms*, version 2, <https://doi.org/10.5281/zenodo.21534809>.
- Andrea Paone and Marco Paone, *Line-Graph Signature Beyond the 2-Core*,
  version 1.3, <https://aletheia-technologies.it/research/line-graph-signature-beyond-the-2-core/reader/>.
- Luke Francis and Trevor Uptain, *The signature of connected line graphs is
  unbounded*, <https://arxiv.org/abs/2607.22874>.
- Saieed Akbari et al., *A new conjecture on the inertia of graphs*,
  <https://arxiv.org/abs/2508.01163>.
