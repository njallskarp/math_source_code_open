# A symmetry-robust exact-fiber obstruction at length 9

## Theorem

Work over cyclic indices `Z/9Z`, with syndrome coordinates indexed by the
undirected distances `s=1,2,3,4`.  For a binary axis `a` and sign word
`sigma`, define

```text
D_a(sigma)_s = sum_j (sigma_j+sigma_(j+s))(a_j+a_(j+s)) in F_2.
```

For an exact Gaussian target `X+iY`, put

```text
T_a(X,Y) = {D_a(sigma) : sum_j (-1)^sigma_j i^a_j = X+iY}.
```

Let

```text
A = {0,1,2,3},              a_A = 1+x+x^2+x^3,
B = {0,1,3,6},              a_B = 1+x+x^3+x^6.
```

Then:

1. both syndrome maps have full image `F_2^4`, and both axes have the same
   complete nontrivial CRT activity set;
2. both axes have weight four, exact target `(X,Y)=(5,0)`, and the same
   even total-syndrome parity coset;
3. `A` and `B` are not equivalent under any affine multiplier/dihedral map
   `j -> uj+t`, where `u` is a unit modulo 9; and
4. even after every unit-induced permutation of syndrome coordinates, their
   exact-target fibers remain disjoint.

More precisely, identifying a syndrome with the set of its nonzero distance
coordinates,

```text
T_A(5,0) = { empty, {1,3} },
T_B(5,0) = { {1,2}, {1,4}, {2,4} }.
```

The six exact sign words have multiplicities `2,4` on the two syndromes for
`A`, and multiplicity `2` on each of the three syndromes for `B`.

## Proof

Over `F_2`, direct Euclidean division gives

```text
gcd(a_A, x^9+1) = x+1,
gcd(a_B, x^9+1) = x+1.
```

Indeed,

```text
x^9+1 = (x+1)(x^2+x+1)(x^6+x^3+1),
a_A    = (x+1)^3,
a_B    = (x+1)^3(x^3+x^2+1).
```

Thus both axes are active on every nontrivial factor of `x^9+1`.  The
Boolean image-lattice theorem gives full image.  This conclusion can also be
checked without that theorem: definition-level syndrome columns at positions
`0,1,4,5` for `A`, and `0,1,3,4` for `B`, form bases of `F_2^4`.

Because each axis has five real and four imaginary positions, the exact
target `5+0i` forces all real signs positive and exactly two imaginary signs
negative.  Therefore the exact fiber is the set of pairwise sums of the four
syndrome columns belonging to the support of the axis.  Direct substitution
gives

```text
A columns on A: {1,2,3}, {2}, {2}, {1,2,3};
B columns on B: {1}, {1,2,4}, {2}, {4}.
```

Taking all six pairwise symmetric differences yields the displayed fibers
and multiplicities.  The universal exact-target parity equation is

```text
sum_s D_a(sigma)_s = (wt(a)-Y)/2 = 2 = 0 (mod 2),
```

so the parity datum is identical.

It remains to remove the symmetry caveat.  Units modulo 9 preserve
`gcd(s,9)`.  Consequently the exceptional distance coordinate `3` is fixed,
while `{1,2,4}` is permuted.  Every unit image of `T_A(5,0)` is therefore
either the zero syndrome or a two-coordinate syndrome containing `3`.
Every unit image of `T_B(5,0)` is a two-element subset of `{1,2,4}` and never
contains `3`.  The two unit-orbit closures are disjoint.

Finally, an affine map preserves whether a pairwise difference is divisible
by 3.  The support `A` has exactly one unordered pair with difference
divisible by 3, namely `{0,3}`.  The support `B` has exactly three, namely
`{0,3}`, `{0,6}`, and `{3,6}`.  Hence no affine multiplier/dihedral map sends
`A` to `B`.

This proves a symmetry-robust version of the earlier fixed-coordinate fiber
obstruction: CRT activity, full image, weight, exact target, and universal
parity still do not determine compatibility, even after independent cyclic
affine canonicalization.

## Reproduction

Run with Python 3.12 or later:

```sh
python3 verify_symmetry_robust_obstruction.py
shasum -a 256 -c SHA256SUMS
```

The dependency-free checker independently evaluates the defining syndrome
sum for every one of the `2^9=512` sign words for each axis.  It verifies the
full 16-element images, exact Gaussian target, fiber multiplicities,
polynomial gcds, affine orbit separation, all unit-coordinate permutations,
and the hand proof's pair-divisibility invariant.

The theorem is proved by the displayed finite algebraic calculation.  The
checker is an exhaustive certificate and catches transcription or indexing
errors; it is not an inference from sampled data.  The software trust boundary
is CPython integer/bit semantics, the operating system and hardware, and
SHA-256 collision resistance.  There is no floating point, randomness,
external package, solver, heuristic pruning, concurrency, or external input.

## Scope and prior-art calibration

This is a structural counterexample to a proposed pruning interface, not a
construction or nonexistence proof for a quaternary Legendre pair.  It closes
the multiplier-equivalence caveat identified by the independent review of the
length-independent two-spike obstruction, but it does not show that a
particular stronger invariant is sufficient for QLP search.

The reciprocal-factor ingredients are standard; see Wu--Yue--Fan,
*Self-reciprocal and self-conjugate-reciprocal irreducible factors of
`x^n-lambda` and their applications*, <https://arxiv.org/abs/2001.04766>, and
Boripan--Jitman--Udomkavanich, *Self-Conjugate-Reciprocal Irreducible Monic
Factors of `x^n-1` over Finite Fields and Their Applications*,
<https://arxiv.org/abs/1804.06138>.  The QLP motivation and search context are
Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
<https://arxiv.org/abs/2212.10953>, and Kotsireas--Koutschan--Winterhof,
*Quaternary Legendre pairs II*, <https://arxiv.org/abs/2408.16318>.

A targeted primary-source search found no statement matching this exact
syndrome fiber obstruction or its symmetry-robust length-9 certificate.
Novelty is therefore search-relative only, not a priority claim.
