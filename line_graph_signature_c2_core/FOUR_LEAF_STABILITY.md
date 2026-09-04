# Four-leaf stability of extremal cyclomatic-two line-graph cores

## Theorem

Let `H` be a finite connected simple graph of minimum degree at least two,
with cyclomatic number `c(H)=2` and line-graph adjacency signature
`s(L(H))=1`. Choose vertices `x_1,x_2,x_3,x_4` of `H`, with repetitions
allowed, and adjoin one new leaf at each chosen vertex. If the resulting graph
is `G`, then

```text
s(L(G)) <= s(L(H))=1.                              (1)
```

This is a subdivision-closed four-port extension of the one-, two-, and
three-leaf theorems. It does not cover a leaf attached to a newly added
vertex, a pendant path of length two, or an arbitrary pendant forest.

The new mechanism is a local-to-global inertia lemma: safe three-dimensional
principal response forms force a safe four-dimensional response form. Only
one singular mixed branch is not a principal-response problem; a complete
marked reduction gives seven small effective forms for that branch.

## 1. Four-port inertia identity

Put `M=Q(H)-2I`, let

```text
E=[e_(x_1),e_(x_2),e_(x_3),e_(x_4)],
U=M+2EE^T.
```

Eliminating the four diagonal `-1` leaf pivots gives

```text
Q(G)-2I congruent to (-I_4) direct_sum U.           (2)
```

Since adjoining leaves preserves the cyclomatic number and
`s(L(J))=sig(Q(J)-2I)-c(J)+1`,

```text
s(L(G))-s(L(H))=sig(U)-sig(M)-4.                   (3)
```

If `M` is nonsingular, the same two-Schur-complement calculation as in the
three-port theorem gives

```text
s(L(G))-s(L(H))=-sig(S),
S=(1/2)I_4+E^T M^(-1)E.                            (4)
```

Every singular extremal core has `nullity(M)=1`. In orthonormal
range/kernel coordinates write `M=A direct_sum 0`, let `G_0` be the inverse
on the range, and let `b` be the kernel row of `E`. If `b=0`, (4) holds with
`G_0` in place of `M^(-1)`. If `b!=0`, eliminating the positive kernel pivot
as in the three-port identity gives

```text
s(L(G))-s(L(H))
 =-sig(S restricted to b^perp),
S=(1/2)I_4+E^T G_0 E.                              (5)
```

Thus it suffices to prove that the effective response form in (4) or (5) has
nonnegative signature.

## 2. A four-dimensional local-to-global lemma

We use the following elementary fact.

**Lemma.** Let `S` be a real symmetric `4 x 4` matrix having a positive
diagonal entry. If every principal `3 x 3` submatrix has nonnegative
signature, then `sig(S)>=0`.

**Proof.** Write the inertia of `S` as `(p,z,n)`. Cauchy interlacing shows
that `n>=3` would force each principal submatrix to have at least two negative
eigenvalues, hence negative signature. Thus `n<=2`. A positive diagonal
entry implies `p>=1`, so the conclusion is immediate when `n<=1`.

Suppose `n=2`. If `z=0`, then `p=2` and the signature is zero. The case
`z>=2` contradicts `p>=1`. It remains to exclude `(p,z,n)=(1,1,2)`. For a
kernel vector `v`,

```text
adj(S)=c vv^T
```

with `c>0`, because `c` has the sign of the product of the three nonzero
eigenvalues, two negative and one positive. Some diagonal cofactor is
therefore positive. The corresponding principal `3 x 3` submatrix has
positive determinant. Interlacing gives it at least one negative eigenvalue;
positive determinant then gives it two negative eigenvalues. Its signature
is negative, a contradiction. This proves the lemma. `□`

When `M` is nonsingular, every diagonal entry of `S` is `7/8`. When `M` is
singular and `b=0`, every diagonal entry is `1` or `2`. Deleting any one port
from `S` gives exactly the response form for the other three ports. The
three-leaf theorem proves that each such form has nonnegative signature.
The lemma therefore settles all nonsingular cores and the singular `b=0`
branch. Notice that the argument permits a zero eigenvalue of `S`; it does not
assume generic invertibility.

## 3. Singular ports and the kernel-isotropic subspace

It remains to treat `b!=0`. The height-1793 core classification identifies a
singular core as

```text
C_(4m) -- odd path -- C_(4n+1).                    (6)
```

A kernel vector `z` is supported on alternating odd positions of the
`C_(4m)`, with values `+1,-1`. Call a port coordinate *undefined* when its
entry of `b` is nonzero, and let `u` be the number of undefined coordinates,
counting repetitions.

For coefficients supported on undefined coordinates and orthogonal to `b`,
the associated vertex demand is supported on odd cycle positions and
orthogonal to `z`. The odd-even path-incidence image gives a solution of
`Ma=d` supported on even positions. Hence `d^T a=0`. By polarization, the
`G_0` response vanishes identically on

```text
W={alpha: alpha is supported on undefined ports and b alpha=0}.  (7)
```

Consequently `S restricted to W=(1/2)I`, a positive form of dimension
`u-1`.

If `u>=3`, the three-dimensional effective form in (5) has a positive
subspace of dimension at least two, so it has nonnegative signature. If
`u=1`, the kernel-orthogonality condition sets that single undefined
coordinate to zero. The effective form is the principal response on the
other three, defined ports, and the three-leaf theorem applies.

Only `u=2` remains.

## 4. The seven mixed response types

Let the two undefined supports be `r_1,r_2`, with kernel values
`epsilon_1,epsilon_2 in {+1,-1}`, and let the defined supports be `d_1,d_2`.
In the basis

```text
w=(epsilon_2,-epsilon_1,0,0), e_(d_1), e_(d_2)
```

of `b^perp`, isotropy gives the upper-left entry `1`. Write the effective
matrix as

```text
T=[ 1   h_1 h_2 ]
  [ h_1 a   q   ]
  [ h_2 q   d   ].                                  (8)
```

Here

```text
h_j=epsilon_2 (G_0)_(r_1,d_j)
    -epsilon_1 (G_0)_(r_2,d_j).                     (9)
```

Up to exchanging the two defined ports and diagonal sign switching, exactly
the following types occur. The type columns are
`(a,d; |q|; |h_1|,|h_2|; sign(q h_1 h_2))`.

```text
type                              det(T)   In(T)
(1,1; 1/2; 0,0; 0)                 3/4    (3,0,0)
(1,2; 1/2; 0,0; 0)                 7/4    (3,0,0)
(1,2; 1/2; 0,1; 0)                 3/4    (3,0,0)
(1,2; 3/2; 0,0; 0)                -1/4    (2,0,1)
(2,2; 3/2; 0,0; 0)                 7/4    (3,0,0)
(2,2; 3/2; 0,1; 0)                -1/4    (2,0,1)
(2,2; 3/2; 1,1; +)                 3/4    (3,0,0).   (10)
```

Every type has nonnegative signature, completing the proof of (1).

For completeness, (10) is a finite symbolic classification, not a
bounded-order experiment. Mark the four leaf supports and the two cycle
roots. Smoothing a five-edge subpath whose four internal vertices are
unmarked preserves the core and attached-graph shifted-signless signatures.
After repeating this operation every gap has length at most four. A
rectangular grid containing every reduced marked singular core is

```text
C_(0 mod 4): 4,8,12,16,20;
C_(1 mod 4): 5,9,13,17;
odd bridge:  1,3,5,7,9,11,13,15,17,19.             (11)
```

Exact period-four elimination on the 200 representatives in (11), for every
two-undefined/two-defined port multiset, gives 2,185,340 cases and precisely
the seven forms in (10). Conversely, cutting at the marked vertices shows
that every list of gap residues occurs in (11). Thus the four-subdivision
argument promotes the finite table to all subdivisions.

## 5. Exact proof computation

Run

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_four_leaf.py
```

with CPython 3.11 or later. The standard-library checker uses only exact
`fractions.Fraction` arithmetic. It verifies the four-mark gap bounds, audits
the local-to-global conclusion on both exact response alphabets, checks all
2,185,340 mixed placements and all seven types in (10), and compares the
response prediction with direct full-matrix inertia on every minimal-base
quadruple and targeted local quadruples on every one-edge four-subdivision.

It ends with

```text
result_sha256=4ca9b47cf0280c8b5cdc3ace780c0df2005772f83701fcec2d6370f7a10c4495
VERIFIED
```

An algorithmically independent audit constructs the line graph for every
four-leaf placement on the four minimal bases, computes its adjacency
characteristic polynomial over `ZZ[x]` with SymPy 1.14.x, and uses Descartes
variations to count positive and negative roots. This is exact because all
adjacency characteristic-polynomial roots are real. Run

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_four_leaf_charpoly.py
```

The audit covers all 3,576 base quadruples and ends with

```text
result_sha256=4bd8dc171f6c8010104a44a12096b3769099f3c0fbe1f0e67a03f888bfbacf0d
VERIFIED
```

## Literature and trust boundary

Paone--Paone, *Line-Graph Signature Beyond the 2-Core* (version 1.3, 2026),
states one-leaf and arbitrary-pendant-forest stability as open and reports
1,400 bounded two-leaf tests:
<https://doi.org/10.5281/zenodo.21706797>.

Paone--Paone, *Response Protection for Line-Graph Equality Families* (2026),
studies pair responses for adding missing edges at a different threshold. It
does not prove four-leaf stability:
<https://doi.org/10.5281/zenodo.21793638>.

Targeted primary-source and Discovery Net searches through indexed height
1846 on 2026-09-03 found no three- or four-leaf theorem. This is
search-relative evidence, not a categorical priority claim.

The universal result depends on the height-1793 extremal-core classification,
the height-1835 three-leaf theorem, the four-port and kernel-compression
identities, the marked-smoothing completeness argument, and the seven exact
mixed types. CPython exact rational arithmetic is inside the proof trust
boundary; SymPy is corroborative only. No floating point, randomness, solver,
external dataset, omitted certificate, raw dump, or large artifact establishes
the theorem.

## Stopping point

The four-dimensional lifting lemma is special: principal three-port safety
controls a four-port form, but it does not inductively control all higher
dimensions. A fifth port can have three negative eigenvalues while all of its
four-dimensional principal forms have nonnegative signature. Extending this
lane therefore requires a genuinely new higher-port inequality or an explicit
counterexample, not merely another marked census.
