# One-leaf stability of extremal cyclomatic-two line-graph cores

## Theorem

Let `H` be a finite connected simple graph of minimum degree at least two and
cyclomatic number

```text
c(H)=|E(H)|-|V(H)|+1=2.
```

Write `s(L(H))` for the adjacency signature of its line graph.  If
`s(L(H))=1`, then adjoining one new leaf at any vertex `x` of `H` does not
increase the line-graph signature.

More precisely, put `M(H)=Q(H)-2I`.  When `e_x` lies in the column space of
`M(H)`, define the response

```text
g_x=e_x^T y,  where M(H)y=e_x.
```

(This is independent of the solution.)  Every defined response of an
extremal cyclomatic-two core is one of

```text
3/8, 1/2, 3/2.                                  (1)
```

At the remaining vertices `e_x` is outside the column space.  Thus no
response is below the leaf-gain threshold `-1/2`.

This proves the one-leaf part of Conjecture 6.1 in Paone--Paone for
cyclomatic number two.  It does **not** address simultaneous or iterated
pendant-tree attachments.

## 1. Line signatures and the leaf threshold

For every connected graph `G` with at least one edge, the unsigned incidence
matrix identity gives

```text
s(L(G))=sig(M(G))-c(G)+1,                          (2)
```

where `sig` is positive inertia minus negative inertia.

Let `G` be obtained from `H` by adjoining a leaf at `x`.  Ordering the new
leaf last gives

```text
M(G) = [ M(H)+e_x e_x^T   e_x ] .
       [ e_x^T            -1  ]
```

Eliminating the `-1` pivot shows

```text
M(G) congruent to (-1) direct_sum (M(H)+2e_x e_x^T).       (3)
```

If `e_x` is outside `col(M(H))`, the positive rank-one update removes one
null direction and its signature jump is one.  Equation (3) then makes the
net signature change zero.  If `e_x` is in the column space, generalized
Schur complementation reduces the update to the scalar `1+2g_x`.  The update
has signature jump two exactly when `g_x<-1/2`, jump one at `g_x=-1/2`, and
jump zero when `g_x>-1/2`.  After the negative leaf pivot, adjoining a leaf
therefore raises `s(L(H))` exactly in the first case.  Values (1), as well as
an undefined response, cannot raise it.

## 2. Four-subdivision preserves inertia and vertex responses

Replace an edge `uv` of a graph by

```text
u--a--b--c--d--v,                                  (4)
```

so four internal vertices are inserted.  Let `K` be the new shifted
signless-Laplacian matrix.  With old vertices first,

```text
K=[ A_0  C ],
  [ C^T  P ],

P=[0 1 0 0; 1 0 1 0; 0 1 0 1; 0 0 1 0].          (5)
```

Here `A_0` is `M(H)` with its `uv` and `vu` entries removed, and `C` couples
`u` to `a` and `v` to `d`.  Direct calculation gives

```text
P^{-1}=[ 0  1  0 -1;
          1  0  0  0;
          0  0  0  1;
         -1  0  1  0],
In(P)=(2,0,2).                                      (6)
```

Consequently

```text
A_0-C P^{-1}C^T=M(H),
In(K)=In(M(H))+(2,0,2).                             (7)
```

Thus four-subdivision preserves `sig(M)`, the cyclomatic number, and the
line-graph signature.

The same elimination also works when `M(H)` is singular.  An old coordinate
right-hand side is solvable for `K` exactly when it is solvable for `M(H)`,
and its diagonal response is unchanged.  For the four new coordinates,

```text
C P^{-1}e_a=-e_v,   C P^{-1}e_b=e_u,
C P^{-1}e_c= e_v,   C P^{-1}e_d=-e_u.              (8)
```

Since every diagonal entry of `P^{-1}` is zero, solving the block equations
shows that the response status and value at `(a,b,c,d)` are respectively
copies of those at `(v,u,v,u)`.  In particular, four-subdivision introduces
no new response value and preserves undefined status in the same alternating
pattern.

## 3. Reduction of cyclomatic-two cores

A connected minimum-degree-two graph with cyclomatic number two has exactly
one of three topological forms after suppressing degree-two paths:

1. two cycles meeting in one vertex (a two-petal rose);
2. three internally disjoint paths with common endpoints (a theta graph);
3. two disjoint cycles joined by a path (a dumbbell).

Repeated inverse use of (4) reduces every path length modulo four.  For cycle
lengths use representatives

```text
residue:       0  1  2  3
length:        4  5  6  3,                         (9)
```

and for a joining path use representatives `4,1,2,3`.  A theta reduction can
produce parallel terminal edges; this is harmless because (5)--(7) are
matrix congruences and the reduced matrix retains the correct edge
multiplicities.  In (10)--(13), “line signature” on such a reduced matrix
means the invariant `sig(M_reduced)-1`, which equals the line signature of
the original simple graph by (2) and (7); it is not an assertion about a
separately defined simple line graph of the reduced multigraph.

Exact rational congruence of the 16 reduced rose matrices gives line-signature
distribution

```text
signature       -2  -1   0
number            1   9   6.                       (10)
```

For the 64 ordered reduced theta triples the distribution is

```text
signature       -2  -1   0
number            6  26  32.                       (11)
```

In particular neither form is extremal at cyclomatic number two.

For a dumbbell, let the row and column be the residues modulo four of its two
cycle lengths.  When the joining-path length is even, the exact table is

```text
       0   1   2   3
0      0   0  -1  -1
1      0   0  -1   0
2     -1  -1  -1  -1
3     -1   0  -1  -2.                              (12)
```

When that length is odd, it is

```text
       0   1   2   3
0      0   1   0  -1
1      1   1   0  -1
2      0   0  -1  -2
3     -1  -1  -2  -2.                              (13)
```

These tables follow by applying the same `1x1` and zero-diagonal `2x2`
congruence pivots used in (6) to the 64 residual matrices.  They can also be
checked directly by the short exact script accompanying this note.

It follows that an extremal core is exactly a dumbbell whose joining path is
odd, whose cycle lengths both lie in residues `{0,1}`, and with at least one
cycle in residue `1`.

## 4. The four base response calculations

Up to exchanging the cycles and applying four-subdivision, every extremal
core reduces to one of

```text
(cycle lengths; joining length)
(4,5;1), (4,5;3), (5,5;1), (5,5;3).                (14)
```

Exact row reduction of `M(H)y=e_x` for every vertex gives

```text
base       defined diagonal responses   undefined vertices
(4,5;1)          {1/2,3/2}                       2
(4,5;3)          {1/2,3/2}                       2
(5,5;1)          {3/8}                           0
(5,5;3)          {3/8}                           0.          (15)
```

Section 2 propagates precisely these response values and statuses through
every sequence of four-subdivisions.  Equation (3) then proves the theorem.

## 5. Why extremality cannot be omitted

Take a 4-cycle and a 5-cycle joined by a path of length two.  Its line-graph
signature is zero.  At the internal joining-path vertex the response is

```text
g_x=-3/4.
```

Adding a leaf there raises the line-graph signature from zero to one.  Thus a
cyclomatic-two core can have a response below `-1/2`; the theorem isolates the
extremal subfamily rather than proving a false uniform response bound.

## Literature boundary

Paone--Paone, *Line-Graph Signature Beyond the 2-Core* (version 1.3,
2026), states the extremal-core leaf-stability conjecture, proves the exact
leaf threshold, and exhibits the nonextremal cyclomatic-two witness above:
<https://doi.org/10.5281/zenodo.21706797>.

Paone--Paone, *Line-graph inertia of roses and generalized theta graphs*
(2026), derives complete modulo-four inertia formulae for those two core
families but does not settle pendant-leaf stability:
<https://doi.org/10.5281/zenodo.21744051>.

Paone--Paone, *Response Protection for Line-Graph Equality Families* (2026),
proves stronger response inequalities for a generated nonsingular
odd-cyclomatic cactus family; it does not cover all extremal
cyclomatic-two cores, including the singular `(4,5;k)` bases:
<https://doi.org/10.5281/zenodo.21793638>.

Francis--Uptain, *The signature of connected line graphs is unbounded*
(2026), supplies the independent shifted-signless-Laplacian bridge mechanism
and unbounded examples, but not this fixed-cyclomatic leaf theorem:
<https://arxiv.org/abs/2607.22874>.

Targeted searches of these primary sources and their stated fixed-cyclomatic
open problems on 2026-09-03 found no prior proof of the theorem above.  This
is evidence of apparent novelty relative to the searched sources, not a
categorical priority claim.

## Reproduction and trust boundary

Run

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_c2_core.py
```

with CPython 3.11 or later.  It uses only `fractions.Fraction`, checks all
reduced matrices and all four base response systems, tests every one-edge
four-subdivision of every base, and verifies the sharpness witness.  It ends
with

```text
result_sha256=92b3ea8ffb472f39aaf452b83549404246772fe0b4cb67ea70979dffb35c70e8
VERIFIED
```

The theorem rests on the symbolic congruence proof, finite topological
classification, and displayed exact tables.  The checker corroborates the
finite rational arithmetic; it is not evidence for arbitrary pendant forests
or for the full cyclomatic conjecture.
