# Albertson r = 29: one-triple Kempe obstruction and freeze certificate

This directory is the second and final pass of the predeclared two-pass
`r=29` feasibility gate.  It proves a general structural lemma for the
order-`2k` connected-complement case, applies it to the three surviving
order-58 rows from the first pass, and records exactly why the current
inequalities do not close a row or compress the frontier to 30 profiles.

It does **not** prove Albertson's conjecture for `r=29`.  The conclusion of
this gate is to pause the direction pending a genuinely new structural input.

## The one-triple Kempe lemma

Let `G` be a `k`-vertex-critical graph on `2k` vertices, let
`H=bar(G)` be connected, and let `v` have degree `k-1` in `G`.  By Stehlik's
theorem, `G-v` has a `(k-1)`-colouring in which every colour class has at least
two vertices.  Necessarily there are `k-2` pairs and one triple.

Every colour occurs in `N_G(v)`, or the missing colour could be assigned to
`v`.  Since `|N_G(v)|=k-1`, each colour occurs there exactly once.  Write

```
B=N_G(v)={b_0,b_2,...,b_{k-1}},
A=N_H(v)={a_0,a_1,a_2,...,a_{k-1}},
C_0={b_0,a_0,a_1},       C_i={b_i,a_i}  (2 <= i <= k-1).
```

Each `C_i` is independent in `G`, hence a clique in `H`.

### Theorem

For every such colouring:

1. The vertices `{v} union B` are the branch vertices of a strong immersion
   of `K_k` in `G`.  Every branch path has length one or three.
2. If `q=e_H(A)` and `p=e_H(B)`, then

       q+p <= binom(k,2).

3. If `m=e(G)`, then

       p <= floor((m-(k-1)-binom(k-1,2))/2).

4. If `Delta(H[B]) <= 1`, the immersion paths can be chosen internally
   vertex-disjoint, so `G` contains a subdivision `TK_k`.  Consequently, if
   `G` contains no `TK_k`, then every degree-`k-1` vertex and every Stehlik
   colouring satisfy `Delta(H[N_G(v)]) >= 2`.

### Proof

Fix two colour classes `C_i,C_j`.  The representatives `b_i,b_j` lie in the
same component of the bichromatic graph `G[C_i union C_j]`: otherwise swap
the two colours in the component containing one representative and colour
`v` with the colour thereby removed from its neighbourhood.  A shortest
`b_i`--`b_j` path is odd.  The two classes contain at most five vertices, so
the path has length one or three.  Its internal vertices are not in `B`.

Choose one such shortest path for every unordered pair of colours.  Paths
for distinct colour pairs are edge-disjoint because every edge of `G-v`
belongs to a unique unordered pair of colour classes.  They also avoid all
other branch vertices.  Adding the direct edges `vb_i` proves the strong
immersion statement.

Put `A'={a_2,...,a_{k-1}}`.  If `b_i b_j` is an edge of `H` for distinct
`i,j >= 2`, its forced length-three path in `G` is

```
b_i - a_j - a_i - b_j,
```

so `a_i a_j` is not an edge of `H`.  Hence

```
e_H(A') + e_H(B-{b_0}) <= binom(k-2,2).
```

If `b_0 b_i` is an edge of `H`, a length-three path uses `a_i` and one of
`a_0,a_1`, so at least one of `a_i a_0,a_i a_1` is absent from `H`.  Therefore

```
e_H(A',{a_0,a_1}) + d_{H[B]}(b_0) <= 2(k-2).
```

Finally `a_0a_1` is an edge of `H`.  Adding the last two inequalities gives

```
q+p <= binom(k-2,2)+2(k-2)+1 = binom(k,2).
```

The edges of `G-v` partition by unordered colour pairs.  Every pair
contributes at least one edge; a pair whose representatives are adjacent in
`H[B]` contributes the three edges of its Kempe path.  Thus

```
m-(k-1) >= binom(k-1,2)+2p,
```

which proves the bound on `p`.

If `H[B]` is a matching, each colour class is incident with at most one
nontrivial branch path.  The length-three paths consequently use disjoint
internal vertices: a pair class has only its single `A`-representative, and
the triple class is incident with at most one such path.  The direct branch
paths have no internal vertices.  The strong immersion is therefore a
subdivision of `K_k`.  This proves the final assertion.

## Exact r = 29 consequences

The pass-1 certificate leaves `(n,m)=(58,838),(58,839),(58,840)`.  Put
`x_u=d_G(u)-28`.  The total excesses are 52, 54, and 56, so the respective
numbers of degree-28 vertices are at least 6, 4, and 2.  The theorem applies
at each of these vertices.

For one fixed degree-28 vertex, let

```
q=e_H(A),   p=e_H(B),   c=e_H(A,B),   E=e(H).
```

Since `E=29+q+p+c`, the two-block inequality gives

```
m       E       q+p <= 406       c lower bound       p upper bound
838     815          406                380                216
839     814          406                379                216
840     813          406                378                217
```

If the candidate has no `TK_29`, then additionally
`Delta(H[B])>=2`, and in particular `p>=2`.

## Exact obstruction and gate decision

The verifier recomputes the convex deletion table through order 57 using
exact rational arithmetic.  For an order-58 row, deleting a vertex of excess
`x` leaves `(57,m-28-x)`.  Enumerating every connected-complement-compatible
excess histogram (`0<=x<=28`, 58 entries, fixed total excess) gives:

```
m       histograms       minimum deletion sum       minimizers
838       275826                443312                    27
839       376859                445104                   271
840       512081                446896                  1575
```

A counterexample drawing has at most 8280 crossings, so the sum over all
vertex deletions is at most `54*8280=447120`.  The exact extra deletion-sum
improvements needed for contradiction are therefore 3809, 2017, and 225.

The new scalar consequences alone still permit 10368, 10745, and 11122
formal five-tuples `(q,p,c,X_A,X_B)`, where

```
X_A=29*28-2q-c,      X_B=29*28-2p-c.
```

These are arithmetic profiles, not asserted realizable graphs.  Their role
is a sensitivity certificate: the one-triple identities, two-block bound,
Kempe edge penalty, and no-subdivision degree obstruction do not produce the
mandated compression to at most 30 canonical profiles.  Closing even the
tight row `(58,840)` requires either:

- a new overlap theorem coupling the `K3+27K2` factors for different deleted
  vertices;
- a theorem excluding the forced 2-star in every `H[N_G(v)]`; or
- a crossing inequality whose total one-deletion lift is at least 225 on
  every remaining degree profile.

None follows from the audited inputs.  Under the two-pass contract, this is
a precise missing-inequality certificate and the `r=29` lane is paused.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd albertson_r29_one_triple_kempe
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

The verifier recomputes the published affine lower envelope and convex
induced-subgraph recurrence through order 57; enumerates the exact excess
histograms; checks all displayed identities, bounds, profile counts, and
deletion deficits; and emits a compact digest.

## Trust and conditionality boundary

Unconditional within the stated hypotheses are the Kempe-chain proof, strong
immersion, two-block inequality, edge penalty, and matching-to-subdivision
criterion.  The Python output uses integers and `fractions.Fraction`; it is
an exact audit of arithmetic implications, not a proof of the graph lemma.

Application to a minimum `r=29` counterexample remains conditional on the
pass-1 frontier inputs, especially the order exclusions and critical-edge
bound stated in the recent Cranston preprint and the disconnected-complement
join estimate stated in the recent Sadhu preprint.  No `r=27` terminal
theorem, `r=28` case tree, crossing-table value such as
`cr(24,132)>=165`, floating-point computation, solver, or topology
classification is used.

## Literature and novelty audit

Primary sources checked on 2026-09-05:

- Matej Stehlik, [*Critical Graphs with Connected
  Complements*](https://doi.org/10.1016/S0095-8956(03)00069-8).
- Daniel W. Cranston, [*Progress on Albertson's
  Conjecture*](https://arxiv.org/abs/2512.08020v1).
- Jacob Fox, Janos Pach, and Andrew Suk, [*Immersions and Albertson's
  Conjecture*](https://arxiv.org/abs/2510.05893).
- Sylvia Vergara, [*Complete Graph Immersions in Dense
  Graphs*](https://arxiv.org/abs/1502.01786).

The Kempe connectivity step and complete-immersion viewpoint have broader
precedent; this directory does not claim priority for them in isolation.
The bounded literature and Discovery Net searches found no statement of the
specific order-`2k` one-triple inequalities or the matching-to-subdivision
criterion.  This is a reproducible scoped audit, not a claim of exhaustive
literature priority.
