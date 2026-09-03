# Partition-generated KOH alignment for the Lucas `(2,6)` and `(3,6)` rays

This directory isolates the first all-parameter bridge in the two provisional
width-six Lucas--Schur proofs.  It verifies, directly from Zeilberger's KOH
partition formula, the tail alignments and explicit remainders used in the
ten-step recurrences.  It does **not** verify the later positivity
certificates, Lucas pairing, endpoints, or base cases, and it is not an
independent review.

## Claims checked

Write `B(n,r)` for the homogeneous two-variable Gaussian binomial and put

```text
H_c^(2)=B(c+6,6)-B(3c+2,2),
H_c^(3)=B(c+6,6)-B(2c+3,3).
```

For every integer `c>=16`, the checker proves the following formal identities
at the level of KOH summands:

```text
H_c^(2)=e2^30 H_(c-10)^(2)+e2^3 K_c^(2),
H_c^(3)=e2^30 H_(c-10)^(3)+e2^4 K_c^(3).
```

Here `K_c^(2)` and `K_c^(3)` are exactly the explicit signed Gaussian-product
formulas in the public `(2,6)` and `(3,6)` theorem packages.  The checker does
not infer those formulas from sampled coefficients: it compares two formal
multisets with affine indices in `c`.

## Structural derivation

For a partition `lambda` of `b`, set

```text
Y_i=lambda_1+...+lambda_i.
```

The program implements the KOH summand

```text
e2^(2 sum_i binom(lambda_i,2))
 product_(j>=1) B(j(a+2)-Y_(j-1)-Y_(j+1), lambda_j-lambda_(j+1))
```

and generates all eleven partitions of six.  It separately encodes the
displayed width-six decomposition, so a missing, duplicated, or mistranscribed
partition fails at entry level.

The one-row partition `(b)` contributes

```text
e2^(b(b-1)) B(a+2-b,b).
```

Recursing only into this term gives fifteen width-two steps or five
width-three steps.  In both cases its accumulated power is `e2^30`, and its
tail is respectively

```text
B(3c-28,2)=B(3(c-10)+2,2),
B(2c-17,3)=B(2(c-10)+3,3).
```

The width-six one-row tail is

```text
e2^30 B(c-4,6)=e2^30 B((c-10)+6,6).
```

Thus the two tails align symbolically, with no specialization of `c`.

Two elementary two-variable Clebsch--Gordan identities handle the smallest
remaining powers.  For `(2,6)`,

```text
h_a h_b-h_(a+b)=e2 h_(a-1)h_(b-1).
```

For `(3,6)`, expanding `h_a h_b` into the multiplicity-free two-row sum
`sum_u e2^u h_(a+b-2u)` cancels the common interval and produces

```text
Delta_c=-sum_(c-1<=u<=2c-2)e2^(u-2)h_(6c-4-2u).
```

The remaining terms then have common factors `e2^3` and `e2^4`.  The program
compares the factored results with independently transcribed encodings of both
published `K_c` formulas: 22 signed monomials for `(2,6)`, and 16 signed
monomials plus the affine `Delta_c` range for `(3,6)`.

All index inequalities needed by KOH and the range cancellations are checked
as affine inequalities on the entire domain `c>=16`, rather than at a finite
list of values.

## Reproduction

Requirements: CPython 3.11 or later; standard library only.
Run without `-O`; the checker detects and rejects optimized mode because its
verification obligations are expressed as assertions.

From the repository root, run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b6_koh_alignment/verify_alignment.py
(cd lucas_schur_b6_koh_alignment && shasum -a 256 -c SHA256SUMS)
```

Expected compact output:

```text
partition-generated KOH decomposition: PASS (11 width-six partitions)
(2,6) tail: 15 width-two steps, exact shift e2^30 and factor e2^3
(2,6) formal K terms: 22 signed monomials
(3,6) tail: 5 width-three steps, exact shift e2^30 and factor e2^4
(3,6) formal K units: 16 signed monomials plus one affine Delta range
canonical alignment record SHA-256: 517b5f065fdf6bce5d120d26221e1c4d9cff8681d3ead59a0a57fb7119c7e7f7
```

## Evidence and trust boundary

`verify_alignment.py` uses only immutable tuples, Python integers, exact affine
arithmetic, multiset comparison, and SHA-256.  It performs no floating-point
calculation, interpolation, random search, solver call, modular
reconstruction, coefficient expansion, database access, or external-data
load.  Its canonical record commits to every generated width-six summand,
both recursively generated comparator heads and tails, both factored
remainders, and the affine `Delta_c` range.

The checker trusts the transcribed KOH formula, the standard two-variable
Clebsch--Gordan identity, CPython semantics, and the independently transcribed
target formulas.  It is structurally separate from the quasipolynomial and
Bernstein certificate engines, but it was prepared by the same researcher and
therefore is not an independent audit.  The `(2,6)` and `(3,6)` positivity
theorems remain provisional pending outside review of their 132/134 activation
cells, Bernstein bounds, Lucas pairing, endpoints, and bases.

## Primary source

Fabrizio Zanello, *Zeilberger's KOH theorem and the strict unimodality of
q-binomial coefficients*, arXiv:1311.4480, Lemma 1, states the partition-indexed
KOH formula used here:

https://arxiv.org/abs/1311.4480
