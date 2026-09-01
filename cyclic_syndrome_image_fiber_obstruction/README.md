# Equal CRT images with disjoint exact-sum-one syndrome fibers

## Theorem

Let `n=2m+1>=5` be odd.  For binary words `a,sigma in F_2^n`, with
indices modulo `n`, put

```text
D_a(sigma)_s = sum_j (sigma_j+sigma_(j+s))(a_j+a_(j+s)) in F_2,
1 <= s <= m,
```

and define the exact-sum-one fiber

```text
T_a = {D_a(sigma) : sum_j (-1)^sigma_j i^a_j = 1}.
```

Take the two axes

```text
b = 1+x,
c = 1+x+x^2+x^3 = (1+x)^3.
```

Then, for every odd `n>=5`,

```text
image(D_b) = image(D_c) = F_2^m,                    (1)
T_b != empty,  T_c != empty,  and  T_b intersect T_c = empty.  (2)
```

More precisely, every element of `T_b` has odd coordinate sum, whereas
every element of `T_c` has even coordinate sum.  Thus even the complete
Boolean CRT activity set—and not merely the rank or image size—does not
determine an exact-sum syndrome fiber.

## Proof

Work in `R=F_2[x]/(x^n-1)`.  Since `n` is odd, `x^n-1` is square-free.
Both `b` and `c` have no irreducible factor other than `x+1`; consequently
their residues are nonzero on every nontrivial reciprocal-factor orbit.
The Boolean image-lattice theorem therefore gives (1).

For any even-weight axis `a`, the exact-sum parity identity gives

```text
sum_s D_a(sigma)_s = wt(a)/2 (mod 2)
```

whenever the corresponding Gaussian unit word has sum one.  Since
`wt(b)=2` and `wt(c)=4`, the two fibers lie in complementary affine
hyperplanes of their common full image.  This proves their disjointness.

It remains only to see that neither fiber is empty.  On axis `b`, assign
opposite signs to the two imaginary positions and choose `(n-3)/2` negative
signs among the `n-2` real positions.  On axis `c`, choose two positive and
two negative imaginary signs and `(n-5)/2` negative signs among the `n-4`
real positions.  In each case the imaginary sum is zero and the real sum is
one.  This proves (2).

## Consequence for CRT-based pruning

The image lattice is an exact linear ambient-space classifier, but it
forgets the affine exact-sum slice and all higher `(1+i)`-adic or integral
autocorrelation constraints.  A QLP pruning argument based only on active
CRT blocks therefore cannot infer phase-fiber compatibility: axes with the
same maximal activity can have disjoint nonempty exact-sum fibers.

This is a methodological obstruction, not a claim that CRT blocks are
useless after they are intersected with additional affine or higher-order
data.  In particular, it does not by itself prove or disprove a quaternary
Legendre pair.

## Reproduction and trust boundary

Run with Python 3.12 or later:

```sh
python3 verify_obstruction.py
shasum -a 256 -c SHA256SUMS
```

The standard-library checker:

- audits every odd length from 5 through 101 using exact binary arithmetic;
- verifies the two polynomial gcds and the full rank of both syndrome maps;
- constructs explicit exact-sum-one witnesses and checks their syndrome
  parities directly; and
- exhausts all sign words at lengths 5, 7, 9, and 11, confirming that both
  fibers are nonempty and disjoint.

The infinite theorem rests on the displayed algebraic proof, not on the
finite audit.  The executable evidence trusts the Python interpreter,
integer and bit operations, operating system, and hardware.  It uses no
floating point, randomness, external package, solver, or heuristic search.

## Context and novelty calibration

The Boolean image-lattice theorem and the exact-sum parity identity are the
two inputs.  The result extracts a sharp limitation from them rather than
extending the rank/image-classification ladder.  A targeted search of
primary coding-theory literature found the standard reciprocal-factor/CRT
decomposition, but no statement of this exact image-versus-fiber
obstruction.  That is a search-relative novelty assessment, not a
historical-priority claim.

Primary QLP context: Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
<https://arxiv.org/abs/2212.10953>; Kotsireas--Koutschan--Winterhof,
*Quaternary Legendre pairs II*, <https://arxiv.org/abs/2408.16318>.
