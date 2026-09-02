# Exact `H`/`S` closure of the QLP-42 `q=41`, weight-16 stratum

## Theorem

In the canonical coupled length-21 transform of the norm-32 QLP-42 shell,
assume the `q=41` branch and let `b` be the binary Gaussian-axis word of
`H_B`. There is no lift with `wt(b)=16` satisfying the exact Gaussian sum
and nonzero-shift autocorrelation equations for both transformed components
`H` and `S`.

The exact `H` equations alone leave 24 family-`A`/family-`B` axis-orbit
pairs on 12 family-`B` rotation orbits. For each of the six canonical global-
sum cases, the exact `S` equations eliminate all 24. Since weight 16 is
allowed in every canonical case before this computation, the complete
weight-16 stratum is excluded.

This is a finite computer-assisted theorem inside the established coupled
QLP-42 reduction. It does not resolve QLP-42. We write `pi=1+i`.

## Complete finite reduction

A length-21 binary word of weight 16 cannot have a nontrivial cyclic
stabilizer: periods dividing 21 would force its weight to be divisible by 3
or 7. Consequently its `C(21,16)=20,349` labeled words form exactly 969
full rotation orbits.

For one such `H_B` axis word, there are 16 imaginary positions and five real
positions. The equation `sum(H_B)=1` requires eight negative imaginary
entries and two negative real entries, giving exactly

```text
C(16,8) C(5,2) = 128,700
```

sign assignments per orbit and 124,710,300 assignments over all 969 orbit
representatives.

The established `q=41` reflection theorem gives 1,024 half-axis words for
`H_A`. The third-order equations fix the ten sign XORs in the reflected
pairs. The verifier exhausts all 1,024 pair-sign masks and retains the exact
sum-zero assignments. It groups the resulting requirements by the 322
realized family-`B` autocorrelation signatures, without discarding any
assignment.

For a Gaussian integer `z`, both implementations compute its canonical
`pi`-adic digits by repeatedly subtracting `(Re(z)+Im(z)) mod 2` and dividing
exactly by `pi`. Concatenating the ten PAF residues gives a fingerprint in
`(Z[i]/(pi^k))^10`. Intersecting the `H_B` support with the required
`-2-PAF(H_A)` support gives:

| imposed `H` level | family-`B` orbits | axis orbits | labeled axis pairs | compatible `A` assignments |
|---:|---:|---:|---:|---:|
| modulo `pi^4` | 969 | 438,432 | 9,207,072 | 119,566,496 |
| modulo `pi^5` | 969 | 412,518 | 8,662,878 | 26,086,080 |
| modulo `pi^6` | 957 | 10,176 | 213,696 | 95,376 |
| modulo `pi^7` | 18 | 36 | 756 | 288 |
| modulo `pi^8` | 18 | 36 | 756 | 288 |
| modulo `pi^9` | 12 | 24 | 504 | 192 |
| modulo `pi^10` | 12 | 24 | 504 | 192 |
| modulo `pi^11` | 12 | 24 | 504 | 192 |
| modulo `pi^12` | 12 | 24 | 504 | 192 |

Order 12 is exact here. A residual coordinate of the `H` equation has real
and imaginary magnitudes bounded by 43 and 41, respectively, hence modulus
less than 64. A nonzero Gaussian integer divisible by `pi^12` has modulus at
least `|pi|^12=64`, so a matching order-12 fingerprint is an exact equality.

## Terminal exact-`S` obstruction

For every one of the 24 exact-`H` axis pairs, the verifier imposes the
complementary `S` axes, the established third-order reflected-pair XORs, and
each canonical exact-sum target:

| case | `sum(S_A)` | `sum(S_B)` | exact-`H` input axes | exact `H`+`S` survivors |
|---:|---:|---:|---:|---:|
| 0 | `(1,-1)` | `(4,-5)` | 24 | 0 |
| 1 | `(3,-3)` | `(4,-3)` | 24 | 0 |
| 2 | `(3,-3)` | `(0,-5)` | 24 | 0 |
| 3 | `(5,-1)` | `(4,-1)` | 24 | 0 |
| 4 | `(5,-1)` | `(4,1)`  | 24 | 0 |
| 5 | `(5,-3)` | `(0,-3)` | 24 | 0 |

The aggregate terminal scan evaluates 3,425,136 exact-sum `S_B` assignments
and 7,520 exact-sum `S_A` assignments. It intersects the exact target
fingerprints

```text
PAF(S_A,s) + PAF(S_B,s) = -2  at s=4,
                           2  at s=10,
                           0  otherwise.
```

Again order 12 is exact: an `S` residual has component bounds 44 and 42 and
therefore modulus below 64. The local-state theorem makes the `H` and `S`
sign choices independent once their complementary axes and the required
pair XORs are fixed, so exhausting the two exact supports is complete.

## Independent implementations and certificate

`verify_weight16_exact_closure.cpp` is the aggregate C++20 verifier. It uses
bit-popcount PAF evaluation, sorted exact residue supports, and no
probabilistic filter. It also compares 8,192 deterministically selected PAFs
against a scalar definition-level evaluator. With `--stream` it emits all
969 canonical orbit records and every order-4-through-order-12 survivor
mask. The canonical stream SHA-256 is

```text
e46bcdc794b24be06743b4ecdca8a1d9feb5e501fd8e78981ad71165b2ef307b
```

`independent_numpy_frontier.py` is separately written. It constructs fixed-
cardinality sign sets from Python's combination iterator, evaluates every
correlation directly in signed NumPy arrays, and uses explicit Gaussian
division for residues. It verifies that the 969 stream orbits partition all
20,349 labeled axes, fully recomputes orders 4 through 12 for all 12 terminal
family-`B` orbits and eight deterministic empty controls, then independently
checks all `24*6=144` terminal exact-`S` cases. It finds zero survivors.

Run the dual certificate and a sanitizer build with:

```sh
python3 -m pip install -r requirements.txt
python3 verify_weight16_exact_closure.py
python3 verify_weight16_exact_closure.py --sanitizers
shasum -a 256 -c SHA256SUMS
```

The driver honors `CXX`; otherwise it prefers `g++-16` when installed and
falls back to `clang++`. The recorded normal run used GCC 16.1.0, Python
3.12.12, and NumPy 2.2.2 on arm64 macOS. It takes about two minutes and stays
below 0.6 GB on the recorded machine. AddressSanitizer and
UndefinedBehaviorSanitizer are run separately.

## Scope, provenance, and trust boundary

The proof trusts the previously established `q=41` coupled transform,
reflection theorem, third-order pair-XOR equations, canonical sum cases, and
the local-state independence of `H` and `S`; source inspection; C++ and
NumPy signed-integer semantics; the compiler/interpreter, operating system,
and hardware. All mathematical arithmetic is integral. There is no floating
point, randomness, solver status, heuristic cutoff, concurrency, or time
limit. This is not a proof-assistant formalization.

Primary context:

- Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
  <https://arxiv.org/abs/2212.10953>;
- Jedwab--Pender, *Two constructions of quaternary Legendre pairs of even
  length*, <https://arxiv.org/abs/2408.08472>;
- Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
  <https://arxiv.org/abs/2408.16318>.

The last source identifies length 42 as the smallest unresolved case. A
targeted search of these primary sources and the committed Discovery Net
graph found no matching exact weight-16 `H`/`S` obstruction. Apparent novelty
is relative to those searches, not a historical-priority claim.

Public source directory:
<https://github.com/njallskarp/math_source_code_open/tree/main/qlp42_q41_weight16_exact_closure>.
The verified immutable source commit is recorded in the Discovery Net
contribution and its post-commit graph receipt.

The strongest next step is the weight-4 stratum, where the same quotient
ladder should be substantially cheaper; weights 8 and 12 will likely require
the grouped or meet-in-the-middle refinements developed here.
