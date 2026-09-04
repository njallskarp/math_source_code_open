# Three-leaf stability of extremal cyclomatic-two line-graph cores

## Theorem

Let `H` be a finite connected simple graph of minimum degree at least two,
with cyclomatic number `c(H)=2` and line-graph adjacency signature
`s(L(H))=1`. Choose vertices `x_1,x_2,x_3` of `H`, with repetitions allowed,
and adjoin one new leaf at each chosen vertex. If the resulting graph is `G`,
then

```text
s(L(G)) <= s(L(H))=1.                              (1)
```

This proves the three-isolated-leaf case of the strong pendant-forest part of
Paone--Paone Conjecture 6.1 for every cyclomatic-two extremal core. It does
not cover four leaves, a leaf attached to a newly added vertex, or any deeper
pendant tree.

The proof combines a general three-port inertia identity, the height-1793
classification of extremal `c=2` cores, a marked four-subdivision reduction,
and a complete exact check of 17 small response-matrix types. The finite
reduction is part of the proof, not numerical sampling.

## 1. The multiport identity

Put `M=Q(H)-2I`, let `E=[e_(x_1),e_(x_2),e_(x_3)]`, and set
`U=M+2EE^T`. Eliminating the three diagonal `-1` pivots belonging to the new
leaves gives

```text
M(G) congruent to (-I_3) direct_sum U.              (2)
```

Because adjoining leaves preserves the cyclomatic number and
`s(L(J))=sig(Q(J)-2I)-c(J)+1`, it follows that

```text
s(L(G))-s(L(H))=sig(U)-sig(M)-3.                   (3)
```

If `M` is nonsingular, two Schur complements of

```text
[ M    E    ]
[ E^T -I_3/2]
```

give the exact response formula

```text
s(L(G))-s(L(H))=-sig(S),
S=(1/2)I_3+E^T M^(-1)E.                            (4)
```

Now suppose `ker(M)` is one-dimensional. In orthonormal range/kernel
coordinates write `M=A direct_sum 0`, with `A` nonsingular, and write the
kernel row of `E` as `b`. Let `G_0` denote the inverse of `M` on its range.

If `b=0`, (4) remains valid with `M^(-1)` replaced by `G_0`. If `b!=0`, make
an orthogonal change in the three port columns so that `b=(beta,0,0)` and
write the corresponding range columns as `(u,V)`. Eliminating the positive
`2 beta^2` kernel pivot cancels `2uu^T` and leaves `A+2VV^T`. Thus

```text
s(L(G))-s(L(H))
 =-sig((1/2)I_2+V^T A^(-1)V).                      (5)
```

Invariantly, the matrix in (5) is the restriction to `b^perp` of

```text
(1/2)I_3+E^T G_0 E.                                (6)
```

Equations (4)--(6) turn the theorem into a response-inertia classification.

## 2. Marked modulo-four reduction

Height 1793 proves that every extremal minimum-degree-two `c=2` core is a
dumbbell: two cycles joined by an odd path. Their lengths are either

```text
(4m+1,4n+1; odd)                                   (7)
```

or, after exchanging the cycles,

```text
(4m,4n+1; odd).                                    (8)
```

The first case is nonsingular; the second has nullity one.

Four-subdividing an edge adds an internal `P_4` block of inertia `(2,0,2)`
whose Schur complement is exactly the old shifted signless Laplacian.
Consequently smoothing a five-edge subpath with four unmarked internal
degree-two vertices preserves both sides of (1). This remains true after the
three leaves are attached, provided the smoothed vertices are not supports.

Mark the distinct leaf supports and cut each of the two cycles and the joining
path at its marked vertices and roots. Repeatedly smooth any resulting gap of
length at least five. Every gap then has length `1,2,3`, or `4`. There are at
most three distinct marks, so every reduced marked core occurs among

```text
both 1 mod 4 cycles:       lengths 5,9,13;
the 0 mod 4 cycle:         lengths 4,8,12,16;
the odd joining path:      lengths 1,3,5,7,9,11,13,15.   (9)
```

An unmarked cycle stops at `C_5` or `C_4`, rather than at a loop. Conversely,
every possible ordered list of gap residues occurs inside the grid (9). Thus
checking every support multiset on the 72 nonsingular and 96 singular graphs
in (9) is exhaustive for (1), not merely a bounded order test.

## 3. The seven nonsingular response triangles

There is also a short structural explanation for the nonsingular part of the
finite check. Eliminate the nonroot vertices of each `C_(4m+1)`. Their block
is `P=A(P_(4m))`. Its inverse has entries `0,+1,-1`; if
`h=-P^(-1)(e_1+e_(4m))`, then every entry of `h` is `+1` or `-1`, and for
distinct cycle vertices

```text
P^(-1)_(ij) is either 0 or -h_i h_j.                (10)
```

The remaining bridge block `T_l`, indexed `0,...,l`, has endpoint diagonal
entries `3`, interior diagonal entries `0`, and off-diagonal entries `1`.
Let

```text
D_0=1, D_1=3, D_k=-D_(k-2)  (2<=k<=l).
```

Then `det(T_l)=3D_l-D_(l-1)=+8` or `-8`, and for `i<=j`

```text
(T_l^(-1))_(ij)=(-1)^(i+j) D_i D_(l-j)/det(T_l).   (11)
```

In particular every diagonal response is `3/8`, and every off-diagonal
response has absolute value `1/8,3/8,5/8`, or `9/8`. Formulae (10)--(11)
show that, for three ports, the absolute off-diagonal entries scaled by eight
and the sign of their product have exactly the following seven possibilities.
The last two columns give the determinant and inertia of `8S`.

```text
absolute triple   product sign   det(8S)   In(8S)
(1,1,3)                +            272     (3,0,0)
(1,1,5)                -            144     (3,0,0)
(1,3,9)                +           -240     (2,0,1)
(3,3,3)                +            208     (3,0,0)
(3,3,5)                -            -48     (2,0,1)
(3,5,5)                +             80     (3,0,0)
(3,9,9)                +           -368     (2,0,1)       (12)
```

Here changing port signs conjugates `S` by a diagonal sign matrix, so the
absolute entries and product sign determine inertia. One way to read the
exhaustiveness is that (11) gives the four types with no local cycle term.
Each nonzero term in (10) changes a signed `3` to a signed `-5`; the graph of
such terms is bipartite, so a three-port set contains at most two of them.
This gives precisely the remaining three types in (12), including repeated
ports. Every type has nonnegative signature, so (4) proves (1) in the
nonsingular case.

## 4. The singular response branches

In case (8), a kernel vector `z` is supported on the odd-indexed vertices of
the `0 mod 4` cycle, with alternating values `+1,-1`. Put
`b=(z_(x_1),z_(x_2),z_(x_3))`.

If `b!=0` and at least one coordinate of `b` is zero, the corresponding
coordinate vector belongs to `b^perp`. Its value under (6) is positive: the
defined one-port responses are `1/2` or `3/2`. A two-dimensional symmetric
form with a positive direction cannot be negative definite, so its signature
is nonnegative and (5) proves (1).

If all three coordinates of `b` are nonzero, every port lies on an odd
position of the singular cycle. For any coefficient vector `alpha in b^perp`,
the demand `d=E alpha` is supported on those odd positions and is orthogonal
to `z`. The columns indexed by the nonroot even positions restrict to the odd
rows as a full-column-rank path incidence matrix with left kernel `z`.
Therefore `Ma=d` has a solution supported on even positions. The supports of
`a` and `d` are disjoint, so `d^T a=0`. The response part of (6) vanishes
identically on `b^perp`; the restriction is positive definite.

It remains that `b=0`, so all three ports are range-compatible. Exact path
recurrence in the complete grid (9) gives, up to simultaneous permutation and
diagonal sign congruence, the following ten matrices `2S`. The notation lists
the diagonal, then the upper entries `(12,13,23)`.

```text
diag       upper          det(2S)   In(2S)
(2,4,4)   (-3,-3, 3)        -4      (2,0,1)
(2,4,2)   (-3,-1, 1)        -2      (2,0,1)
(2,4,2)   (-3,-1, 3)        -6      (2,0,1)
(2,4,4)   (-3,-1, 3)        -8      (2,0,1)
(2,2,2)   (-1,-1,-1)         0      (2,1,0)
(2,2,4)   (-1,-1,-1)         6      (3,0,0)
(2,2,2)   (-1,-1, 1)         4      (3,0,0)
(2,2,4)   (-1,-1, 1)        10      (3,0,0)
(2,4,4)   (-1,-1, 3)        12      (3,0,0)
(4,4,4)   (-3,-3, 3)        10      (3,0,0)        (13)
```

Every matrix in (13) has nonnegative signature. Equations (4)--(6) therefore
prove (1) in all singular branches.

## 5. Exact proof computation

Run

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_three_leaf.py
```

with CPython 3.11 or later. The standard-library checker uses only
`fractions.Fraction`. It verifies 341 gap-reduction states, all 631,680 port
triples on the 168 marked representatives, the seven types in (12), the ten
types in (13), and every singular kernel-compression branch. It also compares
the response prediction against direct inertia of `M+2EE^T` for 30,513
triples on the four bases and all one-edge four-subdivisions.

It ends with

```text
result_sha256=15c98ee6dbf61da872c7caa997362f27e4808c74648d13cf9d083ccc28f0a4a6
VERIFIED
```

An algorithmically independent audit constructs the line graph after every
three-leaf placement on the four minimal bases, computes the adjacency
characteristic polynomial over `ZZ[x]` with SymPy 1.14.0, and counts positive
and negative roots by Descartes variations. This is exact because adjacency
characteristic polynomials are real-rooted. Run

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_three_leaf_charpoly.py
```

It checks 1,035 definition-level triples, covers all 17 response types and all
four singular/nonsingular branches, and ends with

```text
result_sha256=4fc568578691a39bfa29412cb21652b8224c7046c812293bfb2606b4e7ac22c0
VERIFIED
```

## Literature and trust boundary

Paone--Paone, *Line-Graph Signature Beyond the 2-Core* (version 1.3, 2026),
states one-leaf and arbitrary-pendant-forest stability as open and reports
1,400 bounded two-leaf support tests, explicitly as finite negative tests:
<https://doi.org/10.5281/zenodo.21706797>.

Paone--Paone, *Response Protection for Line-Graph Equality Families* (2026),
studies pair responses for adding missing edges and a different threshold. It
does not treat three simultaneous pendant leaves:
<https://doi.org/10.5281/zenodo.21793638>.

Discovery Net height 1819 proves the sharp bound for minimum-degree-two
cyclomatic-three cores but explicitly leaves pendant trees outside scope.
Targeted primary-source and graph searches on 2026-09-03 found no proof of the
three-leaf theorem above. This is search-relative evidence, not a categorical
priority claim.

The theorem depends on the height-1793 extremal-core classification, the
multiport inertia identities, the marked smoothing completeness argument, and
the exact finite response tables. CPython and its arbitrary-precision rational
arithmetic are inside the production trust boundary. SymPy is used only for
the independent audit. No floating point, random sampling, solver, external
dataset, omitted certificate, raw search dump, or large artifact establishes
(1).

## Honest stopping point

For four nonsingular ports, the response matrix has order four; its diagonal
and three-port principal restrictions do not by themselves bound the number
of negative eigenvalues. The marked-reduction method could enumerate a larger
finite grid, but doing so without a new four-port invariant would be secondary
enumeration rather than a structural advance. This contribution therefore
stops at three leaves.
