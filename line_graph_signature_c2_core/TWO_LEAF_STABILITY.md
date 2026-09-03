# Two-leaf stability of extremal cyclomatic-two line-graph cores

## Theorem

Let `H` be a finite connected simple graph of minimum degree at least two,
with cyclomatic number `c(H)=2` and line-graph adjacency signature
`s(L(H))=1`.  Choose vertices `x,y` of `H`, allowing `x=y`, and adjoin two
new leaves, one at `x` and one at `y`.  If the resulting graph is `G`, then

```text
s(L(G)) <= s(L(H))=1.                              (1)
```

Thus the strong pendant-forest part of Paone--Paone Conjecture 6.1 holds for
every forest consisting of two isolated leaf edges at a cyclomatic-two
extremal core.  The result includes two leaves at the same support, but does
not cover deeper rooted trees, three or more leaves, or sequential attachment
to a newly added vertex.

The proof uses the one-leaf classification from
`CYCLOMATIC_TWO_CORE_STABILITY.md`: every extremal `c=2` core is either a
nonsingular `(1,1)` dumbbell or a singular `(0,1)` dumbbell in the following
modulo-four notation.  In the nonsingular case every diagonal response is
`3/8`; in the singular case each defined diagonal response is `1/2` or
`3/2`, and the kernel is one-dimensional.

## 1. Eliminating two leaves

Put `M=Q(H)-2I`, let `E=[e_x,e_y]`, and let `U=M+2EE^T`.  Eliminating the two
new diagonal `-1` leaf pivots gives

```text
M(G) congruent to (-I_2) direct_sum U.              (2)
```

Since adjoining leaves preserves the cyclomatic number, the vertex-space
identity `s(L(J))=sig(M(J))-c(J)+1` yields

```text
s(L(G))-s(L(H))=sig(U)-sig(M)-2.                   (3)
```

We now control the right side by a two-port response calculation.

## 2. The nonsingular two-port criterion

First suppose that `M` is nonsingular and put

```text
R=E^T M^{-1}E,
S=(1/2)I_2+R.                                      (4)
```

Compute the inertia of the bordered matrix

```text
B=[ M    E    ].
  [ E^T -I_2/2]
```

Eliminating its lower-right block gives `(-I_2/2) direct_sum U`, while
eliminating `M` gives `M direct_sum (-S)`.  Taking signatures in the two
congruences and using (3) gives the exact identity

```text
s(L(G))-s(L(H))=-sig(S).                            (5)
```

The diagonal entries of `S` are `1/2+g_x` and `1/2+g_y`, where `g_v` is the
one-port response.  If both are nonnegative, a real symmetric `2x2` matrix
cannot have two negative eigenvalues: a negative-definite matrix has negative
diagonal entries.  Hence `sig(S)>=0`, and (5) proves (1).

For an extremal nonsingular `c=2` core, `g_x=g_y=3/8`, so both diagonal
entries are `7/8`.  This also covers `x=y`, for which `R` has two identical
rows and columns.

## 3. A nullity-one two-port criterion

Suppose next that `M` has one-dimensional kernel.  Choose an orthonormal
splitting into `range(M)` and `ker(M)`, so

```text
M congruent to A direct_sum 0                      (6)
```

with `A` nonsingular.  Write the two columns of `E` in these coordinates as
`(u_1,b_1)` and `(u_2,b_2)`, and put `b=(b_1,b_2)`.

If `b=0`, both ports lie in `range(M)`.  The kernel remains untouched and the
argument of Section 2 applies on the nonsingular range.  Again, nonnegative
one-port diagonal responses imply (1).

Now suppose `b` is nonzero.  Apply an orthogonal change to the two columns of
`E`; this preserves `EE^T`.  The kernel row becomes `(beta,0)`, where
`beta=||b||>0`, and the range columns become `u,v`.  Then

```text
U=[ A+2uu^T+2vv^T   2 beta u ],
  [ 2 beta u^T      2 beta^2].                    (7)
```

Eliminating the positive lower-right pivot cancels `2uu^T` and leaves
`A+2vv^T`.  Therefore

```text
s(L(G))-s(L(H))
 =sig(A+2vv^T)-sig(A)-1.                           (8)
```

The rank-one update on the right has signature jump at most one exactly when

```text
1+2 v^T A^{-1}v >=0.                               (9)
```

Equivalently, if `z` is any nonzero kernel vector and
`z_x,z_y` are its coordinates, define

```text
w=(-z_y e_x+z_x e_y)/sqrt(z_x^2+z_y^2).            (10)
```

When at least one of `z_x,z_y` is nonzero, `w` lies in `range(M)` and the
quadratic response `q(w)=w^T a`, for `Ma=w`, is well defined.  Condition (9)
is precisely `q(w)>=-1/2`.

If exactly one port has nonzero kernel coordinate, `w` is, up to sign, the
other coordinate vector.  Its response is a defined one-port response, so
the earlier one-leaf theorem supplies (9).  Only pairs for which both ports
have undefined one-port response remain.

## 4. Isotropy of the two undefined ports

Every singular extremal `c=2` core is a dumbbell consisting of a cycle
`C_a`, with `a=0 mod 4`, a cycle `C_b`, with `b=1 mod 4`, and an odd joining
path.  Label the first cycle

```text
v_0 v_1 ... v_(a-1) v_0,
```

where `v_0` is the bridge root.  A kernel vector of `M` is supported entirely
on this cycle and is given by

```text
z_(v_(2j))=0,
z_(v_(2j+1))=(-1)^j,                               (11)
```

with zero on the joining path and the other cycle.  The undefined coordinate
responses are exactly the odd-indexed vertices in (11).

Let `x,y` be any two such vertices, allowing equality, and put

```text
d=-z_y e_x+z_x e_y.                                (12)
```

The vector `d` is orthogonal to `z`, hence belongs to `range(M)`.  More is
true: `Ma=d` has a solution `a` supported only on the nonroot even-indexed
vertices of `C_a`.

Indeed, on those even vertices the map to the odd rows is the incidence
matrix of a path: its `j`th column has ones in the two adjacent odd rows.  It
has `a/2-1` columns, rank `a/2-1`, and left kernel spanned by the alternating
vector (11).  Its image is therefore exactly the vectors on the odd rows
orthogonal to `z`, which includes `d`.  Extending a solution by zero at
`v_0` and outside the even cycle vertices satisfies every remaining row of
`Ma=d`.

The supports of `a` and `d` are disjoint, so

```text
d^T a=0.                                           (13)
```

After the normalization in (10), this says `q(w)=0`.  Thus (9) is strict,
and (8) proves (1) in the last case.

## 5. Why the argument stops at two leaves

For `r` simultaneous leaves on a nonsingular core, the analogue of (5) is

```text
s(L(G))-s(L(H))=-sig((1/2)I_r+E^T M^{-1}E).        (14)
```

When `r=2`, nonnegative diagonal entries force nonnegative signature.  For
`r>=3`, a symmetric matrix can have nonnegative diagonal but two or more
negative eigenvalues.  Thus one-port safety alone no longer controls (14).
Any extension to three leaves needs a genuine higher-port inequality; the
present proof does not imply it.

## Literature boundary

Paone--Paone, *Line-Graph Signature Beyond the 2-Core* (version 1.3,
2026), states both one-leaf and arbitrary-pendant-forest stability as open,
and reports only bounded two-leaf tests:
<https://doi.org/10.5281/zenodo.21706797>.

Paone--Paone, *Response Protection for Line-Graph Equality Families* (2026),
uses pair responses for adding a missing edge within a host graph.  Its
threshold, update, and generated odd-cyclomatic family differ from the two
new leaf pivots and singular even-cyclomatic cores treated here:
<https://doi.org/10.5281/zenodo.21793638>.

The Discovery Net height-1799 boundary-eigenvalue lemma characterizes a
zero-response rooted amplifier arising from a simple signless-Laplacian
2-eigenvalue.  It explicitly complements the height-1793 one-leaf theorem and
does not treat simultaneous leaves or the rank-two criterion above.

Targeted primary-source searches on 2026-09-03 found no proof of this
cyclomatic-two two-leaf theorem.  This is evidence relative to the searched
sources, not a categorical priority claim.

## Reproduction and trust boundary

Run

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_two_leaf.py
```

with CPython 3.11 or later.  The exact standard-library checker verifies the
rank-two identity on every pair in the nonsingular bases and their one-edge
four-subdivisions, checks every pair directly in all four extremal bases and
their one-edge subdivisions, and verifies the null-vector isotropy on a
bounded family of larger singular dumbbells.

It ends with

```text
result_sha256=c80a82442617de3292cef4a807c76d1f6bc6ce5d399c3c62d08955592b16767c
VERIFIED
```

An algorithmically independent audit constructs each line graph directly and
computes its characteristic polynomial over `ZZ[x]` with SymPy 1.14.0:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_two_leaf_charpoly.py
```

It checks all 244 base pairs and ends with
`result_sha256=010f70c2a3f809ac8058173550f86f7baeecec02bcaebe9135c6128948f6cfc1`
and `VERIFIED`.  Descartes sign variations count positive and negative roots
exactly here because every adjacency characteristic polynomial is
real-rooted.

The theorem rests on the symbolic inertia identities and the elementary
cycle-image argument.  The computation is corroborative: it does not replace
the universal quantifiers, and no floating-point result, random search,
solver, external dataset, or omitted certificate establishes (1).
