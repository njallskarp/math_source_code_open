# Seventh-order `H` obstruction for QLP-42 `q=1`, `b=10`

## Exact computer-assisted theorem

In the canonical order-two-compression branch of the norm-32 quaternary
Legendre-pair problem at length 42 with `q=1` and `b=10`, no candidate lifts
through the seventh-order Gaussian `H` autocorrelation equations.

The certified exact-sum and sixth-order `H` predecessor contains 198 cyclic
`A`-rotation-orbit pairs on 192 distinct `A` supports and 64 reflected `B`
masks. The `H` equations are independent of the six exact-sum cases after the
forced orientation `H_B(0)=-1`, so these pairs represent 1,188 case
incidences. The complete seventh-order scan leaves

```text
seventh-order H orbit pairs       0
seventh-order H case incidences   0
supporting B masks                0
```

Therefore the full `q=1`, `b=10` shell is impossible. This does not exclude
the other unresolved norm-32 shells and does not resolve QLP-42.

## Seventh-order quotient

Every active non-quarter `H` cell is `(1+i)` times a Gaussian unit, while the
combined `H` autocorrelation target is `-2` at each nonzero shift. Since

```text
(1+i)^7 = 8-8i,
```

the seventh-order quotient of a Gaussian coordinate `r+si` is represented
exactly by

```text
(r mod 8, r+s mod 16).
```

The C++ implementation reconstructs the 198-pair predecessor from its full
third- and sixth-order definitions. For each of 192 supports, it enumerates
all 63,504 zero-sum ten-cell `H_A` phase words, totaling 12,192,768 exact
assignments. The seventh-order sign-change PAF is quadratic, so for every
fixed axis system the implementation derives its ten linear and 45 quadratic
coefficients from direct PAF evaluations, then checks one deterministic global
sign mask directly. This gives 5,505,024 direct coefficient evaluations and
98,304 global quadratic audits. Each of the 64 `B` masks has exactly 3,384
exact `H_B` assignments.

The resulting exact fingerprint ranges are

```text
H_A seventh-order fingerprints per support: 7,961--15,876
H_B seventh-order fingerprints per mask:     1,660--1,692
```

No required `H_A` fingerprint intersects its paired `H_B` complement set.

## Independent verification

`independent_numpy.py` consumes the exact 198-pair predecessor but does not
use quadratic interpolation. It constructs the 63,504 zero-sum phase words as
all independent choices of five positive real and five positive imaginary
coordinates, then directly evaluates all ten PAF coordinates. It agrees on
the exact assignment totals, both fingerprint ranges, and the empty frontier.
The inherited sixth-order frontier has SHA-256
`e73bdd9cf30807550ef62b04698823e5d9379de43a1cac14d73e74bb47732ea1`.

All arithmetic is integral and exhaustive. PAF coordinates are bounded well
inside signed 16-bit range in the NumPy route; the C++ route uses signed
integers for direct Gaussian coordinates and unsigned packed residue lanes.
No floating point, randomness, solver status, heuristic pruning, concurrency,
or time limit is used.

## Reproduction and resource cost

The recorded environment used Python 3.12.12, NumPy 2.2.2, and Homebrew GCC
16.2.0. Install the pinned Python dependency and run:

```bash
python3 -m pip install -r requirements.txt
python3 verify_b10_seventh_h.py
```

On an Apple-silicon macOS 26.2 host, the optimized proof scan took 8.16
seconds and about 20 MB peak resident memory. The direct NumPy replay,
including predecessor reconstruction, took 15.74 seconds and about 76 MB.
The complete driver took 27.90 seconds. A full GCC address- and
undefined-behavior-sanitized proof run also passed, taking 95.41 seconds.

The driver pins both implementations and every inherited source by SHA-256,
compiles C++20 with assertions and practical warnings enabled, verifies the
predecessor hash, and checks the two outputs field by field. The C++ and NumPy
routes share the transform and support conventions; their new seventh-order
enumeration is independent: quadratic interpolation plus a 5+5 exact join
versus direct vectorized evaluation of every exact phase word. This is an
exact finite computer-assisted theorem, not a formal proof-assistant theorem
or a historical-priority claim.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; Pender's 2026 thesis,
<https://theses.lib.sfu.ca/file/thesis/etd24298-thomasthomasscott-pender-pender-thesis-pdfa.pdf>;
and Djokovic--Kotsireas, *Compression of Periodic Complementary Sequences and
Applications*, <https://arxiv.org/abs/1302.0571>. A targeted primary-source
and committed-graph search found no matching `q=1`, `b=10` seventh-order
obstruction; apparent novelty is relative to those searches.

The strongest next step is to continue the largest unresolved `q=1` shell,
currently `b=8`, using the exact-sum and higher-order Gaussian engine.
