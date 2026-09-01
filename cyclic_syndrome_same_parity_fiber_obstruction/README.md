# Equal CRT image and parity data with distinct exact-target fibers

## Theorem

Let `n=2m+1>=5` be odd.  For a binary axis `a` and sign word `sigma`, put

```text
D_a(sigma)_s = sum_j (sigma_j+sigma_(j+s))(a_j+a_(j+s)) in F_2,
1 <= s <= m,
```

with indices modulo `n`.  For an exact Gaussian target `X+iY`, write

```text
T_a(X,Y) = {D_a(sigma) : sum_j (-1)^sigma_j i^a_j = X+iY}.
```

For `1<=d<=m` with `gcd(d,n)=1`, define `a_d=1+x^d`, and let `e_d` be
the `d`-th standard basis vector of the syndrome space `F_2^m`.  Then

```text
image(D_(a_d)) = F_2^m,                                  (1)
T_(a_d)(n-2,0) = {e_d}.                                  (2)
```

In particular, `a_1=1+x` and `a_2=1+x^2` have all of the following data
in common for every odd `n>=5`:

- the complete nontrivial CRT activity set;
- the full syndrome image `F_2^m`;
- weight two;
- the exact target `(n-2)+0i`; and
- the necessary affine parity coset `{t: sum_s t_s=1}`.

Nevertheless,

```text
T_(a_1)(n-2,0)={e_1},
T_(a_2)(n-2,0)={e_2},
```

so the two nonempty exact-target fibers are distinct and disjoint.  Thus
CRT activity augmented by the universal exact-target parity equation still
does not determine fiber compatibility.

## Proof

Over `F_2`,

```text
gcd(1+x^d, x^n-1) = x^gcd(d,n)+1 = x+1.
```

Hence `a_d` is nonzero on every irreducible factor of `x^n-1` other than
`x+1`.  The Boolean image-lattice theorem makes every nontrivial reciprocal
orbit active and proves (1).

The axis `a_d` has two imaginary positions, `0` and `d`, and `n-2` real
positions.  To attain real part `n-2`, every real sign must be positive.  To
attain imaginary part zero, exactly one of the two imaginary signs must be
negative.  The only sign words in the exact fiber are therefore

```text
sigma=1 and sigma=x^d.
```

For a single negative sign at position zero, direct substitution gives

```text
D_(a_d)(1)_s = (a_d)_s + (a_d)_(-s),
```

which is one exactly when `s=d`.  Thus `D_(a_d)(1)=e_d`.  Rotation by `d`
or the same coefficient calculation gives `D_(a_d)(x^d)=e_d`, proving (2).

Finally, the general exact-target parity law for an even-weight axis is

```text
sum_s D_a(sigma)_s = (wt(a)-Y)/2 (mod 2).
```

Here `wt(a_d)=2` and `Y=0`, so every fiber lies in the same odd-parity
coset.  Equations (1)--(2) show that this shared affine datum is insufficient.

The restriction `n>=5` is sharp for this pair of examples: at `n=3` the
syndrome space has only one distance coordinate, so there are no distinct
choices `d=1,2` in `1<=d<=m`.

## Reproduction and trust boundary

Run with Python 3.12 or later:

```sh
python3 verify_same_parity_obstruction.py
shasum -a 256 -c SHA256SUMS
```

The dependency-free standard-library checker:

- verifies the polynomial gcd and full binary rank for `a_1,a_2` at every
  odd length from 5 through 101;
- checks both exact sign witnesses directly in Gaussian integers;
- checks the definition-level syndromes are exactly `e_1,e_2`; and
- exhausts every sign word at lengths 5, 7, 9, 11, and 13, confirming that
  the two exact-target fibers are the asserted distinct singletons.

The infinite theorem rests on the displayed proof, not the finite audit.
The checker trusts CPython integer and bit semantics, the operating system,
hardware, and SHA-256 collision resistance.  It uses no floating point,
randomness, external package, solver, heuristic, or unrecorded input.

## Mathematical payoff and scope

This result addresses a limitation raised by the independent review of the
equal-image sum-one obstruction: parity can separate weights modulo four,
but it supplies no discrimination when the weight and parity coset coincide.
The theorem supplies an infinite same-weight, same-target counterexample.

It is not another rank formula or a larger syndrome census.  It identifies
the missing invariant: any sound exact-fiber or QLP pruning interface must
retain information beyond CRT activity, image, weight, target, and the
universal parity coset.  Candidate refinements include fixed-cardinality
column-matroid data or higher `(1+i)`-adic autocorrelation residues.

This does not imply that those refinements suffice, and it does not construct
or exclude a quaternary Legendre pair.  A targeted primary-source search found
standard reciprocal-factor CRT decompositions but no matching same-data
fiber obstruction.  This is search-relative novelty, not a priority claim.

Primary QLP context: Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
<https://arxiv.org/abs/2212.10953>; Kotsireas--Koutschan--Winterhof,
*Quaternary Legendre pairs II*, <https://arxiv.org/abs/2408.16318>.
