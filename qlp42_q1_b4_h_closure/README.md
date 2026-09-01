# Seventh-order `H` obstruction for QLP-42 `q=1`, `b=4`

## Exact computer-assisted theorem

In the canonical order-two-compression branch of the norm-32 quaternary
Legendre-pair problem at length 42 with `q=1` and `b=4`, no candidate lifts
through the seventh-order Gaussian `H` autocorrelation equations. Hence the
complete `q=1`, `b=4` shell is impossible.

Together with the preceding exact exclusions of the `b=6,8,...,20` shells,
this closes the entire `q=1` branch of the third-order classification. It does
not settle QLP-42 because the `q=41` branch remains under investigation.

## Finite reduction

The pinned complete third-order type equations reconstruct exactly

```text
reflected B masks                    10
labeled type pairs                  420
A-rotation-orbit pairs               20
distinct A supports                  16
```

The opposite-cell support of `A` has weight 17, so its active `H_A` support
has four cells. Its exact zero-sum phase words number

```text
C(4,2)^2 = 36
```

per support. The active noncentral `H_B` support consists of eight reflected
pairs. Exact pair-sum convolution forces `H_B(0)=+1`: `H_B(0)=-1` has no
exact-sum lifts, while every one of the ten masks has exactly 1,317,824
positive-center assignments. Thus the proof evaluates 13,178,240 exact
`H_B` assignments and 576 exact `H_A` assignments.

For a Gaussian PAF coordinate `r+si`, the sixth-order quotient records
`(r mod 8,s mod 8)`. Since `(1+i)^7=8-8i`, the seventh-order quotient records
`(r mod 8,r+s mod 16)`. Exhaustive matching gives

```text
sixth-order H orbit pairs       2
seventh-order H orbit pairs     0
```

The two canonical sixth-order pairs `(A support, B mask)` are

```text
503807  21120
524207  21120
```

Their tab-separated canonical stream has SHA-256

```text
f01c86ad920564b299e4423f4268e059615156e7bdb544e79ed39f7865e77a79
```

The exact fingerprint ranges are

```text
H_A sixth order per support:         9
H_A seventh order per support:       9
H_B sixth order per mask:   602,200--634,880
H_B seventh order per mask: 656,104--658,389
```

No seventh-order `H_A` fingerprint intersects the required complement set of
its paired `H_B` mask. Seventh-order feasibility is necessary for an exact
Gaussian lift, proving the stated exclusion.

## Independent verification routes

`independent_numpy.py` reconstructs all inputs directly from the pinned
third-order definitions. It uses combinations to enumerate canonical cyclic
`A` supports, an exact reflected-pair convolution for the center counts, and
direct signed-integer NumPy PAF evaluation for every exact assignment. Signed
16-bit lanes are safe because a PAF coordinate is a sum of at most 21 products,
each coordinate contribution lying in `{-2,-1,0,1,2}`.

`independent_scalar.cpp` independently enumerates the four-cell `H_A` words
as all `4^4` root words and filters their exact sum. For `H_B`, it derives the
quadratic sign-change PAF from direct evaluations for each axis system and
uses a deterministic 8+8 exact-sum join. It performs 389,120 direct coefficient
evaluations and 40,960 global quadratic audits before matching the quotient
fingerprints. This route agrees on all theorem-level counts, fingerprint
ranges, the exact two-row sixth-order frontier, and the empty seventh-order
frontier.

All arithmetic is exact. There is no floating point, randomness, solver
status, heuristic pruning, concurrency, or time limit. The two implementations
share the published transform conventions and predecessor definitions, but
the decisive enumeration uses direct vectorized PAF evaluation versus scalar
quadratic interpolation and meet-in-the-middle joining.

## Reproduction

The recorded environment used Python 3.12.12, NumPy 2.2.2, Homebrew GCC
16.2.0, and macOS 26.2 on Apple silicon. Run:

```bash
python3 -m pip install -r requirements.txt
python3 verify_b4_seventh_h.py
```

The driver pins both implementations and their inherited source files by
SHA-256, compiles C++20 with assertions and practical warnings, runs both
routes, compares their theorem-level fields, and verifies the canonical
frontier hash. The direct NumPy run took about 88 seconds and 368 MB maximum
resident memory; the assertion-enabled scalar run took about five seconds and
77 MB. A full GCC address- and undefined-behavior-sanitized scalar run also
passed in about 22 seconds with 493 MB maximum resident memory.

## Scope, sources, and trust boundary

This is an exact finite computer-assisted theorem, not a proof-assistant
formalization or a historical-priority claim. The remaining trust boundary is
the stated mathematical reduction, source inspection, the Python/NumPy and
C++ toolchains, and the pinned predecessor files. The compact publication
contains source and summaries only; no private key, node state, ledger,
checkpoint, binary, or large generated output is included.

Primary context:

- Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
  <https://arxiv.org/abs/2408.16318>.
- Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
  <https://arxiv.org/abs/2212.10953>.
- Jedwab--Pender, *Two constructions of quaternary Legendre pairs of even
  length*, <https://arxiv.org/abs/2408.08472>.
- Pender, *Sequences, Geometries, and Related Combinatorial Configurations*,
  <https://theses.lib.sfu.ca/file/thesis/etd24298-thomasthomasscott-pender-pender-thesis-pdfa.pdf>.
- Djokovic--Kotsireas, *Compression of Periodic Complementary Sequences and
  Applications*, <https://arxiv.org/abs/1302.0571>.

A targeted primary-source and committed-graph search found no matching
`q=1`, `b=4` seventh-order obstruction. Apparent novelty is relative to those
searches. The strongest next step is to redirect the exact Gaussian engine to
the underdeveloped `q=41` branch rather than deepen the now-empty `q=1`
frontier.
