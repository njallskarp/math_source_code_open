# Exact `H`/`S` closure of QLP-42 `q=1`, `b=8`

## Exact computer-assisted theorem

In the canonical order-two-compression branch of the norm-32 quaternary
Legendre-pair problem at length 42 with `q=1` and `b=8`, no candidate lifts
through the full Gaussian autocorrelation equations. Hence the complete
`q=1`, `b=8` shell is impossible.

This closes one shell of QLP-42. It does not resolve the full length-42
existence problem; the remaining `q=1` shells are `b=4` and `b=6`.

## Finite reduction

The inherited complete third-order type equations give exactly

```text
reflected B masks                         98
labeled type pairs                    49,350
A-rotation-orbit pairs per sum case    2,350
distinct A supports                    1,867
```

There are six canonical exact Gaussian-sum cases. Exact `H_B` sums force the
exceptional orientation `H_B(0)=+1`: depending on the reflected mask it has
27,072 or 28,496 assignments, while `H_B(0)=-1` has none. Every `H_A`
support has exactly

```text
C(8,4)^2 = 4,900
```

zero-sum phase words. Exhaustive `H` autocorrelation matching then gives

```text
sixth-order H orbit pairs      739  (685 A supports, 54 B masks)
seventh-order H orbit pairs     54  ( 54 A supports, 14 B masks)
full-integer H orbit pairs      40  ( 40 A supports, 11 B masks)
```

The canonical full-integer frontier SHA-256 is

```text
0e3fa74a39e7a5ff91ef3d56a33a5f1a62a9528839f6facfdd47e2b789418cfd
```

For a Gaussian PAF coordinate `r+si`, the sixth-order quotient records
`(r mod 8,s mod 8)`, while the seventh-order quotient records
`(r mod 8,r+s mod 16)` because `(1+i)^7=8-8i`. The final `H` pass compares
all twenty signed integer coordinates, so the 40-pair frontier is not merely
a residue frontier.

## Decisive exact `S` obstruction

The forced positive `H` center pairs with `S_B(0)=-i` in cases 0, 2, and 3,
and with `S_B(0)=+i` in cases 1, 4, and 5. Direct enumeration gives respectively

```text
exact S_B assignments by case: 96, 96, 248, 248, 248, 248.
```

The four distinct 13-cell `S_A` sum targets contain

```text
target  1-i:  C(13,7) C(13,6) = 2,944,656 phase words
target  3-3i: C(13,8) C(13,5) = 1,656,369 phase words
target  5-i:  C(13,9) C(13,6) = 1,226,940 phase words
target  5-3i: C(13,9) C(13,5) =   920,205 phase words.
```

Across the 40 exact-`H` pairs, the proof checks 269,926,800 distinct phase
words (385,259,160 case incidences). No exact `S_A` autocorrelation vector is
the required complement of an exact `S_B` vector. Thus no one of the six sum
cases survives.

## Two verification routes

`independent_numpy.py` reconstructs all 98 masks, all 49,350 labeled type
pairs, and all 2,350 rotation-orbit pairs directly from the pinned
third-order definitions. It evaluates every relevant `H` and `S`
autocorrelation coordinate with signed integer NumPy arrays. For the large
final `S` scan it first applies a fixed linear map from the twenty exact
coordinates to `uint64` modulo `2^64`. Equality of exact vectors necessarily
implies equality of these linear images. Any hash match is replayed against
the complete signed vectors; the recorded run had zero hash collisions and
zero exact matches.

`independent_scalar.cpp` independently checks the decisive exact-`S`
obstruction from the canonical 40-pair frontier. It expands the same linear
image as a quadratic form in the independent real and imaginary sign masks,
uses a 6+7 meet-in-the-middle evaluation, and directly audits the formula on
160 phase words. It checks all 269,926,800 phase words and finds zero linear
image matches. Since equality of exact PAF vectors would force equality of
their linear images, this zero is itself a complete exclusion certificate;
hash injectivity is not assumed.

All mathematical arithmetic is exact. There is no floating point,
randomness, solver status, heuristic pruning, concurrency, or time limit.
The two routes share the transform conventions and the published predecessor
definitions, but use direct vectorized PAF evaluation versus a scalar
quadratic decomposition for the decisive scan.

## Reproduction

The recorded environment used Python 3.12.12, NumPy 2.2.2, Homebrew GCC
16.2.0, and macOS 26.2 on Apple silicon. Run:

```bash
python3 -m pip install -r requirements.txt
python3 verify_b8_exact_closure.py
```

The combined pinned driver compiles C++20 with assertions and practical
warnings, verifies all source and predecessor SHA-256 values, checks the
canonical 40-pair stream, runs both implementations, and compares their
theorem-level fields. In the combined recorded run the scalar C++ route took
11.52 seconds and the definition-level NumPy route 384.77 seconds (a separate
unloaded NumPy run took 228.75 seconds). Peak resident memory was about 9 MB
and 271 MB respectively. A full GCC address- and undefined-behavior-sanitized
scalar run passed in 46.88 seconds at about 12 MB peak resident memory.

## Scope and sources

This is an exact finite computer-assisted theorem, not a proof-assistant
formalization or a historical-priority claim. The remaining trust boundary
is the stated mathematical reduction, source inspection, the Python/NumPy
and C++ toolchains, and the pinned predecessor files. The compact publication
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
`q=1`, `b=8` exact closure. Apparent novelty is relative to those searches.
The strongest next step is the larger of the two remaining `q=1` shells,
`b=6`, using the same staged exact-sum and Gaussian autocorrelation engine.
