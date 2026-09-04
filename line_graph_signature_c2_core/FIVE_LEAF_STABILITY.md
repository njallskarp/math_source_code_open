# Five-leaf stability of extremal cyclomatic-two line-graph cores

## Theorem

Let `H` be a finite connected simple graph of minimum degree at least two,
with cyclomatic number `c(H)=2` and line-graph adjacency signature
`s(L(H))=1`. Choose vertices `x_1,...,x_5` of `H`, with repetitions allowed,
and adjoin one new leaf at each chosen vertex. If the resulting graph is `G`,
then

```text
s(L(G)) <= s(L(H))=1.                              (1)
```

Equality is possible. The result is subdivision-closed and is not a bounded
order census. It does not cover a leaf attached to a newly added vertex,
deeper pendant trees, or six simultaneous leaves.

The new ingredient is a response-specific five-dimensional inequality. The
height-1835 three-port theorem gives two exact finite alphabets for response
triangles. Every five-dimensional response whose ten principal triangles lie
in the appropriate alphabet has nonnegative signature. This finite matrix
lemma is checked exactly after a complete diagonal-switching reduction.

## 1. Five-port inertia identity

Put `M=Q(H)-2I`, let

```text
E=[e_(x_1),e_(x_2),e_(x_3),e_(x_4),e_(x_5)],
U=M+2EE^T.
```

Eliminating the five diagonal `-1` leaf pivots gives

```text
Q(G)-2I congruent to (-I_5) direct_sum U.           (2)
```

Since adjoining leaves preserves the cyclomatic number and
`s(L(J))=sig(Q(J)-2I)-c(J)+1`,

```text
s(L(G))-s(L(H))=sig(U)-sig(M)-5.                   (3)
```

If `M` is nonsingular, two Schur complements give

```text
s(L(G))-s(L(H))=-sig(S),
S=(1/2)I_5+E^T M^(-1)E.                            (4)
```

Every singular extremal core has `nullity(M)=1`. Let `G_0` be the inverse of
`M` on its range and let `b` be the kernel row of `E`. If `b=0`, (4) holds
with `G_0` in place of `M^(-1)`. If `b!=0`, eliminating the positive kernel
pivot gives

```text
s(L(G))-s(L(H))
 =-sig(S restricted to b^perp),
S=(1/2)I_5+E^T G_0 E.                              (5)
```

It remains to prove that every effective response form in (4) or (5) has
nonnegative signature.

## 2. The five-dimensional response-alphabet inequality

The height-1835 three-port classification gives the following exact local
data, including repeated supports.

For a nonsingular extremal core, `8S` has diagonal `7`, each off-diagonal
entry lies in

```text
{+/-1,+/-3,+/-5,+/-9},                             (6)
```

and each principal triangle has one of seven types. A triangle type is the
sorted triple of absolute off-diagonal entries together with their product
sign:

```text
(1,1,3)+, (1,1,5)-, (1,3,9)+, (3,3,3)+,
(3,3,5)-, (3,5,5)+, (3,9,9)+.                     (7)
```

For a singular core with `b=0`, `2S` has diagonal entries in `{2,4}`, every
off-diagonal entry lies in `{+/-1,+/-3}`, and each principal triangle is one
of the ten switching/permutation types listed in the three-leaf proof.

We need the following exact finite lemma.

**Response-alphabet lemma.**

1. Every symmetric `5 x 5` integer matrix with diagonal `7`, off-diagonal
   alphabet (6), and all principal triangles in (7) has nonnegative
   signature. Up to diagonal switching, exactly 1,678 such labeled matrices
   occur. Their inertias are

   ```text
   (3,0,2): 552; (4,0,1): 1,045; (5,0,0): 81.     (8)
   ```

2. Every symmetric `5 x 5` integer matrix with diagonal in `{2,4}`,
   off-diagonal alphabet `{+/-1,+/-3}`, and every principal triangle in the
   ten singular all-range types has nonnegative signature. Up to diagonal
   switching, exactly 2,160 occur, with inertias

   ```text
   (3,0,2): 612; (3,1,1): 140; (4,0,1): 1,301;
   (4,1,0): 15;  (5,0,0): 92.                     (9)
   ```

**Completeness of the finite lemma.** All off-diagonal entries in both
alphabets are nonzero. A unique diagonal sign switching, modulo the global
sign, therefore makes the four entries in the first row positive. There are
`4^4` possible first rows in (6). In the singular case there are `2^5`
diagonals and `2^4` positive first rows. Fill the six remaining upper entries
in lexicographic order from their complete signed alphabets, rejecting a
partial matrix exactly when a newly completed triangle is absent from the
appropriate list. Every switching class appears exactly once, and no class
outside the conditions is admitted. Exact rational congruence gives (8) and
(9). Thus the lemma is a finite proof of a matrix inequality, not a search
over graphs.

Every full response in (4), and every all-range response in (5), satisfies
the corresponding lemma hypothesis by height 1835. Equations (8)--(9)
therefore settle the nonsingular and `b=0` branches. In fact their response
signatures are strictly positive, so five leaves decrease the line-graph
signature in these branches.

## 3. Singular kernel compression

It remains that `b!=0`. A kernel vector `z` is supported on alternating odd
positions of the `0 mod 4` cycle, with values `+1,-1`. Let `u` be the number
of port coordinates on this support, counting repetitions.

For coefficients supported on undefined ports and orthogonal to `b`, the
associated demand is supported on odd cycle positions and orthogonal to `z`.
The odd-even path-incidence image supplies a solution of `Ma=d` supported on
even positions. Hence its quadratic response is zero. By polarization the
`G_0` response vanishes on

```text
W={alpha: alpha is supported on undefined ports and b alpha=0}. (10)
```

Consequently `S restricted to W=(1/2)I`, a positive form of dimension
`u-1`.

The effective form in (5) has dimension four. If `u>=3`, it contains at
least two positive directions, so it has at most two negative directions and
nonnegative signature. If `u=1`, kernel orthogonality removes the single
undefined coordinate and leaves the four-port response on the defined
coordinates. The height-1853 four-leaf theorem applies.

Suppose `u=2`. Let the two undefined kernel values be
`epsilon_1,epsilon_2`, and use

```text
w=(epsilon_2,-epsilon_1,0,0,0)
```

together with the three defined coordinate vectors as a basis of `b^perp`.
The effective `4 x 4` matrix has positive first diagonal entry `1`. Its
principal submatrix on the three defined coordinates is one of the ten
height-1835 singular all-range triangles. Each principal submatrix on `w`
and two defined coordinates is precisely a two-undefined/two-defined
four-port response, one of the seven types in height 1853. Hence all four
principal `3 x 3` submatrices have nonnegative signature.

The four-dimensional local-to-global lemma from height 1853 says that a real
symmetric `4 x 4` matrix with a positive diagonal entry and safe principal
triangles has nonnegative signature. This proves the `u=2` case and completes
the proof of (1).

As a redundant exact audit, the production checker over-enumerates all
`4 x 4` matrices compatible with the three defined-port types and the seven
mixed types. Of 3,240 candidates, 344 survive all local constraints. Their
inertias are

```text
(3,0,1): 216; (3,1,0): 28; (4,0,0): 100.          (11)
```

## 4. Equality witness

The inequality is sharp. Start with a `C_4` and a `C_5` joined by one edge.
Label the `C_4` as `0-1-2-3-0`, label the `C_5` root `4`, and replace the
joining edge `0-4` by

```text
0-9-10-11-12-4.
```

Attach one leaf at each of vertices

```text
1, 9, 10, 11, 12.                                  (12)
```

The subdivided core has line-graph signature one, and the graph after the
five attachments also has signature one. The effective response form has
inertia `(2,0,2)`. Thus equality in (1) occurs even with five distinct leaf
supports.

## 5. Exact proof computation

Run

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_five_leaf.py
```

with CPython 3.11 or later. The standard-library checker uses only exact
`fractions.Fraction` arithmetic. It performs the complete switching-reduced
enumerations (8)--(9), the redundant 344-form audit (11), and 22,253 direct
full-matrix regressions on the four minimal cores, local port sets on every
one-edge four-subdivision, and the equality witness (12). It covers all seven
singular/nonsingular kernel branches and ends with

```text
result_sha256=b37bc71bff79ccf0c5d3a2bfd83d4ed162157aa24cbf1c2f3bf57036e08e176b
VERIFIED
```

An independent SymPy 1.14.0 audit reimplements both triangle predicates and
both switching-reduced searches, then obtains every response inertia from its
characteristic polynomial over `ZZ[x]`. It also constructs line graphs
directly for all 10,660 five-leaf placements on the four minimal cores and
for (12). Run

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_five_leaf_charpoly.py
```

It reproduces (8)--(9), finds minimal-core delta distribution

```text
-5: 5,616; -4: 2,195; -3: 2,501; -2: 329; -1: 19,
```

verifies the equality witness, and ends with

```text
result_sha256=f59cbfc4684bc947ab89d4ca4be85d165e832df14a6b11984bd6f4013873e8d1
VERIFIED
```

## Literature and trust boundary

Paone--Paone, *Line-Graph Signature Beyond the 2-Core* (version 1.3, 2026),
states extremal-core pendant-forest stability as open and reports 1,400
bounded two-leaf tests:
<https://doi.org/10.5281/zenodo.21706797>.

Paone--Paone, *Response Protection for Line-Graph Equality Families* (2026),
studies pair responses for adding missing edges at a different threshold. It
does not prove simultaneous-leaf stability:
<https://doi.org/10.5281/zenodo.21793638>.

Targeted primary-source and Discovery Net searches through indexed height
1866 on 2026-09-03 found no five-leaf theorem. This is search-relative
evidence, not a categorical priority claim.

The universal theorem depends on the height-1793 extremal-core
classification, height-1835 three-port response classification, height-1853
four-port theorem, the exact multiport identities, and the finite
response-alphabet lemma. CPython exact rational arithmetic is inside the
proof trust boundary. SymPy characteristic polynomials over `ZZ[x]` are an
independent computational audit, not a substitute for the mathematical
reduction. No floating point, randomness, solver, external dataset, omitted
certificate, raw dump, or large artifact establishes the theorem.

## Stopping point

The response-alphabet method can be posed at six ports, but the number of
locally admissible colored complete graphs grows with the port count. Another
arity extension is warranted only if it yields an explicit counterexample or
a finite-state or structural classification valid for unbounded port number.
A larger fixed-arity enumeration alone would be secondary optimization.
