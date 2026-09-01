# Small-cardinality spectral frontier in `Z/2310Z`

## Theorem

Let `A,Lambda` be a spectral pair in the cyclic group `Z/NZ`, where

```text
N = n p,    p prime,    gcd(n,p)=1,
```

and suppose finite Fuglede in the spectral-to-tiling direction holds in
`Z/nZ`. If

```text
0 < |A| = |Lambda| < p,
```

then both `A` and `Lambda` tile `Z/NZ`.

More precisely, multiplication by `p` is injective on both sets. If

```text
Z(A) = {d | N : Phi_d divides the mask polynomial m_A},
```

then, for every `d|n`, including `d=1`,

```text
dp in Z(A)  implies  d in Z(A),                         (1)
```

and the same implication holds for `Lambda`. The images `pA` and
`pLambda`, viewed in `p Z/NZ ~= Z/nZ`, are spectral sets of cardinality
`|A|`.

For `N=2310=2*3*5*7*11`, take `p=11` and `n=210`. Finite Fuglede is known
for the four-prime cyclic group `Z/210Z`. Consequently every nonempty
spectral subset of `Z/2310Z` of cardinality less than 11 tiles. Its
cardinality must therefore divide 2310, and the exact small-cardinality
frontier is

```text
possible:   1, 2, 3, 5, 6, 7, 10,
impossible: 4, 8, 9.                                      (2)
```

Every value in the possible list is realized by a subgroup, which is both
spectral and a tile. Thus (2) is an if-and-only-if classification, not only
a necessary-condition list.

## Proof

Put `k=|A|=|Lambda|<p`. A spectral pair is symmetric: the normalized
Fourier submatrix on rows `A` and columns `Lambda` is square unitary, so
`(Lambda,A)` is spectral as well.

Suppose multiplication by `p` were not injective on `A`. Then distinct
`a,a' in A` would have difference of order `p`. Spectrality of
`(Lambda,A)` would give

```text
Phi_p divides m_Lambda.
```

Evaluation at 1 gives `p=Phi_p(1)` dividing `m_Lambda(1)=k`, impossible
because `0<k<p`. Hence multiplication by `p` is injective on `A`; symmetry
gives the same conclusion for `Lambda`.

We next prove (1). The square-free cube rule and its one-prime
Laba--Marshall consequence state that, for a nonnegative multiset,

```text
Phi_(dp) divides m_A and Phi_d does not divide m_A
    implies |A| >= p.                                      (3)
```

For completeness, the cuboid proof of (3) chooses a `d`-cuboid `Delta`
whose integer evaluation `A^d[Delta]` is nonzero. The `dp` cube rule makes
this evaluation divisible by `p`, while nonnegativity and the coefficients
`{-1,0,1}` give `|A^d[Delta]|<=|A|`. Thus `p<=|A|`. Since here `k<p`, (3)
proves (1). The identical argument applies to `Lambda`.

It remains to descend spectrality. Let `lambda != lambda'` be in `Lambda`
and let `r` be the order of `lambda-lambda'` in `Z/NZ`. Orthogonality on
the injective image `pA` is the sum

```text
sum_(a in A) exp(2*pi*i*p*(lambda-lambda')*a/N).            (4)
```

If `p` does not divide `r`, multiplication by `p` leaves the order `r`
unchanged, so (4) vanishes by the original spectrality. If `r=dp`, its
order after multiplication is `d`; original spectrality gives
`Phi_(dp)|m_A`, and (1) supplies `Phi_d|m_A`, so (4) again vanishes. The
`k` restricted characters are therefore pairwise orthogonal on the
`k`-point set `pA`, hence form a spectrum. Thus `pA` is spectral in the
subgroup `p Z/NZ ~= Z/nZ`.

In CRT coordinates `Z/NZ ~= Z/nZ x Z/pZ`, injectivity says that `A` is the
graph of a function over its first-coordinate projection `B`. The set `B`
is spectral in `Z/nZ`, because it differs from `pA` only by an automorphism.
By the hypothesis on `Z/nZ`, choose `C` with `B+C=Z/nZ` uniquely. Then

```text
A + (C x Z/pZ) = Z/nZ x Z/pZ
```

uniquely, so `A` tiles. Applying the same argument to the symmetric spectral
pair proves that `Lambda` tiles too.

For `n=210`, the required base case is the known `pqrs` theorem. A finite
tile has cardinality dividing the group order, giving the necessary part of
(2); subgroups give the converse.

## Exact zero-order frontier at the prime 11

For every spectral pair of size below 11 in `Z/2310Z`, the following 16
cyclotomic implications hold for both mask polynomials:

```text
Phi_11   -> Phi_1       Phi_22   -> Phi_2
Phi_33   -> Phi_3       Phi_55   -> Phi_5
Phi_66   -> Phi_6       Phi_77   -> Phi_7
Phi_110  -> Phi_10      Phi_154  -> Phi_14
Phi_165  -> Phi_15      Phi_231  -> Phi_21
Phi_330  -> Phi_30      Phi_385  -> Phi_35
Phi_462  -> Phi_42      Phi_770  -> Phi_70
Phi_1155 -> Phi_105     Phi_2310 -> Phi_210.
```

The first implication also says `Phi_11` cannot occur at all for a nonempty
set of size below 11, since `Phi_1|m_A` would force `m_A(1)=0`.

## Reproduction

Run with CPython 3.12 or later:

```bash
python3 verify_frontier.py
python3 verify_frontier.py | shasum -a 256
shasum -a 256 -c SHA256SUMS
```

The dependency-free checker verifies the factorization and square-free
conditions, enumerates all 16 descent implications, and checks that the
positive divisors of 2310 below 11 are exactly the possible list in (2).
Its canonical output is `expected_output.txt`.

The checker does not prove the universal spectral descent theorem. That
theorem rests on the displayed algebraic proof and the cited cube-rule
bound. The executable is a deterministic audit of the finite specialization
and transcription. It uses exact Python integers, no floating point,
randomness, solver, external package, network input, or generated database.

## Prior art and novelty calibration

The multiplication/descent argument is extracted from Case 1 of Somlai,
*Fuglede's Conjecture on Cyclic Groups of Square-Free Order: The Case of
Rapidly Growing Prime Factors* (2026),
<https://arxiv.org/abs/2607.26534>. The key observation is that the global
hypothesis `p>n` in that theorem can be replaced, for this branch and this
individual spectral pair, by the local condition `|A|<p`.

The base case is Kiss--Malikiosis--Somlai--Vizer, *Fuglede's conjecture holds
for cyclic groups of order pqrs*, <https://arxiv.org/abs/2011.09578>. The
cube-rule bound is also discussed in Laba--Marshall, *Vanishing sums of roots
of unity and the Favard length of self-similar product sets*,
<https://arxiv.org/abs/2202.07555>.

No novelty is claimed for the general proof mechanism, which is already
implicit in the cited 2026 proof. The exact `Z/2310Z`, `|A|<11`
classification and zero-order frontier are recorded as a search-relative
new application and a rigorous reduction of the committed problem, not as a
historical-priority claim. This result says nothing yet about cardinalities
11 and above.
