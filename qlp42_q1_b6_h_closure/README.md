# Seventh-order `H` obstruction for QLP-42 `q=1`, `b=6`

## Exact computer-assisted theorem

In the canonical order-two-compression branch of the norm-32 quaternary
Legendre-pair problem at length 42 with `q=1` and `b=6`, no candidate lifts
through the seventh-order Gaussian `H` autocorrelation equations. Hence the
complete `q=1`, `b=6` shell is impossible.

This closes one shell of QLP-42. It does not resolve the full length-42
existence problem; within the complete third-order `q=1` classification only
the `b=4` shell remains open.

## Finite reduction

The pinned complete third-order type equations reconstruct exactly

```text
reflected B masks                    50
labeled type pairs                3,402
A-rotation-orbit pairs              162
distinct A supports                 134
```

Here the opposite-cell support of `A` has weight 15, so its active `H_A`
support has six cells. Its exact zero-sum phase words number

```text
C(6,3)^2 = 400
```

per support. The active noncentral `H_B` support consists of seven reflected
pairs. Exact pair-sum convolution forces `H_B(0)=-1`: `H_B(0)=+1` has no
exact-sum lifts, while every one of the 50 masks has exactly 164,728 negative-
center assignments. Thus the proof evaluates 8,236,400 exact `H_B` assignments
and 53,600 exact `H_A` assignments.

For a Gaussian PAF coordinate `r+si`, the sixth-order quotient records
`(r mod 8,s mod 8)`. Since `(1+i)^7=8-8i`, the seventh-order quotient records
`(r mod 8,r+s mod 16)`. Exhaustive matching gives

```text
sixth-order H orbit pairs       4
seventh-order H orbit pairs     0
```

The four canonical sixth-order pairs `(A support, B mask)` are

```text
196091  1441818
229117  1441818
751471   273672
777147   273672
```

Their tab-separated canonical stream has SHA-256

```text
7b8a809ac94ef89ad16171dbd3b5f96098f5977e704a09fbc5ac5a9cf9830f77
```

The exact fingerprint ranges are

```text
H_A sixth order per support:    46--100
H_A seventh order per support:  55--100
H_B sixth order per mask:   76,092--82,364
H_B seventh order per mask: 81,915--82,364
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

`independent_scalar.cpp` independently enumerates the six-cell `H_A` words as
all `4^6` root words and filters their exact sum. For `H_B`, it derives the
quadratic sign-change PAF from direct evaluations for each axis system and
uses a deterministic 7+7 exact-sum join. It performs 774,400 direct coefficient
evaluations and 102,400 global quadratic audits before matching the quotient
fingerprints. This route agrees on all theorem-level counts, fingerprint
ranges, the exact four-row sixth-order frontier, and the empty seventh-order
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
python3 verify_b6_seventh_h.py
```

The driver pins both implementations and the two inherited source files by
SHA-256, compiles C++20 with assertions and practical warnings, runs both
routes, compares their theorem-level fields, and verifies the canonical
frontier hash. The recorded scalar run took about 10 seconds and the direct
NumPy run about 138 seconds. Observed maximum resident memory was below 500 MB
for each route. A full GCC address- and undefined-behavior-sanitized scalar run
also passed in about 30 seconds, with approximately 762 MB maximum resident
memory.

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
`q=1`, `b=6` seventh-order obstruction. Apparent novelty is relative to those
searches. The strongest next step is the sole remaining third-order `q=1`
shell, `b=4`, whose small 20-orbit frontier should permit a complete exact
`H`/`S` analysis.
