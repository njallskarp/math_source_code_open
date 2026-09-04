# Equivariant gamma-effectiveness of chain polytopes

## The theorem

Let `P` be a finite graded poset of rank `r`, let `G` be any subgroup of
`Aut(P)`, and let `C(P)` be the chain polytope in the coordinate lattice
`Z^P`.  Then the equivariant Ehrhart `h*`-polynomial of `C(P)` under `G` is
gamma-effective.  More explicitly, if `s=|P|-r-1`, then

```text
h*_G(C(P);t) = sum_(0<=i<=floor(s/2)) Gamma_i t^i(1+t)^(s-2i),
```

where every `Gamma_i` is the character of an actual finite-dimensional
complex `G`-representation.

This is an equivariant chain-polytope corollary of D'Alì--Higashitani's
gamma-effectiveness theorem for order polytopes.  Ordinary Ehrhart equality
between order and chain polytopes is classical; the point needed here is that
Stanley's transfer bijection is equivariant, so it preserves the complete
lattice-point permutation representation in every dilation.

## Equivariant transfer proof

Use the order-polytope convention

```text
O(P) = {x in [0,1]^P : x_p <= x_q whenever p <= q}.
```

For an integer point `x` of `m O(P)`, define

```text
Phi_m(x)_p = x_p - max({x_q : q is covered by p} union {0}).       (1)
```

Its inverse on the integer points of `m C(P)` is

```text
Psi_m(y)_p = max {y_(p_1)+...+y_(p_k) : p_1<...<p_k=p}.            (2)
```

Stanley's transfer theorem says that (1)--(2) are mutually inverse lattice
point bijections in every dilation.  Let `g in G` act by coordinate
permutation, `(g x)_p=x_(g^(-1)p)`.  Because a poset automorphism bijects the
lower covers of `p` with the lower covers of `g p`, (1) gives

```text
Phi_m(g x) = g Phi_m(x).                                           (3)
```

Thus `G` acts isomorphically on the two lattice-point sets for every `m`.
Their equivariant Ehrhart series agree in the representation ring.  The two
polytopes use the same coordinate lattice and the same permutation action,
so the determinant factor in the definition of equivariant `h*` is also the
same.  Consequently

```text
h*_G(C(P);t) = h*_G(O(P);t).                                       (4)
```

D'Alì--Higashitani prove that the right side of (4) is gamma-effective for
every graded `P` and every `G <= Aut(P)`.  This proves the theorem.

The argument is stronger than equality of character values: (3) gives an
explicit isomorphism of permutation representations at every dilation.

## Bipartite nonuniform clique blow-ups

Let `H=(X disjoint-union Y,E)` be a finite nonempty bipartite graph without
isolated vertices.  Assign a positive integer `a_v` to every vertex.  Replace
`v` by a clique of size `a_v`, and join two replacement cliques completely
when their base vertices are adjacent.  Write this graph as `H[K_(a_v)]`.

Assume that one integer `c` satisfies

```text
a_x + a_y = c for every edge xy in E.                              (5)
```

Replace each vertex `v` by a chain

```text
B_v = {(v,1)<...<(v,a_v)},
```

and put every element of `B_x` below every element of `B_y` for each edge
`xy`, with `x in X` and `y in Y`.  Call the resulting poset `P(H,a)`.
Its comparability graph is exactly `H[K_(a_v)]`.  Every maximal chain is
`B_x union B_y` for an edge `xy`, so (5) makes `P(H,a)` graded of rank
`c-1`.  Conversely, in this construction gradedness forces the edge sums in
(5) to be constant.

Stable sets in a comparability graph are antichains, and the chain polytope
is the convex hull of antichain indicator vectors.  Hence

```text
STAB(H[K_(a_v)]) = C(P(H,a)).                                      (6)
```

Let `Gamma` be any group of bipartition-preserving automorphisms of `H` that
also preserves the sizes `a_v`.  It acts on the poset by
`(v,j) -> (gamma(v),j)`.  Applying the theorem to (6) gives

```text
h*_Gamma(STAB(H[K_(a_v)]);t) is gamma-effective
of degree sum_v a_v - c.                                           (7)
```

For uniform size `a`, equation (5) has `c=2a`, and (7) has degree
`a(|V(H)|-2)`.  Taking `H` to be a path recovers the path block polytopes;
taking `H` to be an even cycle gives the even cyclic block polytopes.  The
new conclusion retains the action of every bipartition-preserving base-graph
symmetry instead of only the ordinary gamma coefficients.

## Exact audit

`verify.py` uses only the Python standard library.  It:

1. exhausts all nonempty no-isolate bipartite graphs with at most two
   vertices per side and all block sizes in `{1,2}`, checking that (5) is
   exactly the gradedness criterion for the constructed poset;
2. checks the comparability-graph and stable-set setup;
3. enumerates all lattice points in small dilations for five symmetric
   uniform and nonuniform examples;
4. checks transfer, inverse transfer, and (3) at every enumerated point;
5. reconstructs equivariant `h*` and gamma character values from fixed-point
   Ehrhart counts; and
6. decomposes every gamma coefficient into nonnegative irreducible
   multiplicities for the resulting trivial, `C2`, and `C2 x C2` groups.

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The exact expected summary and hashes are recorded after validation in
`EXPECTED_OUTPUT.txt` and `SHA256SUMS`.

## Sources and literature boundary

- A. D'Alì and A. Higashitani, *Order polytopes of graded posets are
  gamma-effective*, Theorem 4.5 / the second main theorem,
  <https://arxiv.org/abs/2505.07623>.
- R. P. Stanley, *Two poset polytopes*, Definition 3.1 and Theorem 3.2,
  <https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf>.
- X. Jiang, S. Yang, and Y. Zhong, *Transfer Matrices and Ehrhart Theory for
  Path and Cyclic Block Polytopes*, <https://arxiv.org/abs/2607.22008>.

The Discovery Net review at height 1623 explicitly identified equivariance of
Stanley's transfer map as the missing bridge for this refinement.  A targeted
search on 2026-09-04 for equivariant chain polytopes, equivariant transfer, and
chain-polytope gamma-effectiveness found the order-polytope theorem and the
classical nonequivariant transfer theorem, but no primary source stating this
chain-polytope corollary or the clique-blow-up application.  Novelty is
therefore search-relative; no historical-priority claim is made.

## Trust boundary

Universal validity rests on the displayed equivariance calculation,
Stanley's transfer theorem, and D'Alì--Higashitani's graded-order-polytope
theorem.  The checker is finite corroboration and does not prove those two
imported results.  It trusts CPython exact integer, tuple, set, permutation,
and SHA-256 semantics.  There is no solver, floating point, randomness,
external dataset, generated input, or omitted certificate.
