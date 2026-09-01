# Seventh-order `H` obstruction for QLP-42 `q=1`, `b=12`

## Computational lemma

In the canonical order-two-compression branch of the norm-32 quaternary
Legendre-pair problem at length 42 with `q=1` and `b=12`, no candidate lifts
through the seventh-order Gaussian `H` autocorrelation equations.

The certified eighth-order `S`, exact-`H`, and sixth-order `H` reductions leave
79 case incidences on 77 distinct `B`-mask/`A`-support rows. They consist only
of exact-sum cases 0 and 2, use 77 distinct twelve-cell `A` supports, and use
18 reflected `B` masks. The complete seventh-order scan leaves

```text
case                               0   2
seventh-order H incidences         0   0
supporting B masks                 0   0
```

Cases 1, 4, and 5 were already impossible by the exact `H_B` sum, and the
single case-3 incidence was already impossible at sixth order. Thus the
combined certificates exclude the full `q=1`, `b=12` shell. This does not
exclude the other norm-32 shells and does not resolve QLP-42.

## Seventh-order quotient

Every active non-quarter `H` cell is `(1+i)` times a Gaussian unit. The
combined `H` autocorrelation target is `-2` at each nonzero shift. Since

```text
(1+i)^7 = 8-8i,
```

the quotient is represented exactly by

```text
r+si |-> (r mod 8, r+s mod 16).
```

The sixth-order sign-change PAF map is affine modulo 8, but its quadratic
terms need not vanish in this seventh-order quotient. The C++ implementation
therefore reconstructs the full 77-row predecessor and, for each fixed axis
system, obtains the complete quadratic sign polynomial from 12 linear and 66
quadratic evaluations. One deterministic global mask is then evaluated
directly for every admissible axis system. Across the 77 supports this gives
12,457,984 direct PAF checks, including 157,696 global quadratic audits.
An exact 6+6 join exhausts 65,740,752 zero-sum `H_A` phase assignments.

`independent_numpy.py` consumes the reconstructed 77-row predecessor but does
not use quadratic interpolation. It constructs every one of the 65,740,752
exact phase words and directly computes all ten PAF coordinates. It agrees
that no seventh-order fingerprint intersection exists. The two implementations
also agree on the exact fingerprint ranges:

```text
H_A seventh-order fingerprints per support: 106600--213444
H_B seventh-order fingerprints per mask:       296--338
H_B exact assignments per mask:                 608--676
```

All arithmetic is integral and exhaustive. No floating point, randomness,
solver, heuristic pruning, or time limit is used.

## Reproduction and trust boundary

Install NumPy and run:

```bash
python3 verify_b12_seventh_h.py
```

The driver pins both implementations and every inherited source by SHA-256,
compiles the C++20 route with assertions enabled, reconstructs the sixth-order
frontier, and checks both outputs byte for byte. The C++ and NumPy routes share
the transform, support conventions, and certified 77-row predecessor. Their
new seventh-order arithmetic and phase-enumeration routes are independent:
quadratic interpolation plus a 6+6 join versus direct vectorized PAF
evaluation. The result is an exact finite computer-assisted lemma, not a
formal proof-assistant theorem and not a historical-priority claim.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Djokovic--Kotsireas, *Compression of
Periodic Complementary Sequences and Applications*,
<https://arxiv.org/abs/1302.0571>. A targeted primary-source and committed
graph search found no matching `b=12` seventh-order obstruction; apparent
novelty is relative to those searches.

The strongest next step is to identify the next unresolved QLP-42 norm-32
shell in the committed graph and reuse the certified sixth/seventh-order
engine there.
