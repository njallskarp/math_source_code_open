# Exact `H`/`S` closure of the QLP-42 `q=41`, weight-4 stratum

## Theorem

In the canonical coupled length-21 transform of the norm-32 QLP-42 shell,
assume the `q=41` branch and let `b` be the binary Gaussian-axis word of
`H_B`. There is no lift with `wt(b)=4` satisfying the exact Gaussian sum and
nonzero-shift autocorrelation equations for both transformed components `H`
and `S`.

The exact `H` equations alone leave 42 family-`A`/family-`B` axis-orbit pairs
on nine family-`B` rotation orbits. For each of the six canonical global-sum
cases, the exact `S` equations eliminate all 42. Since weight 4 is allowed in
every canonical case before this computation, the complete weight-4 stratum
is excluded.

This is a finite computer-assisted theorem inside the established coupled
QLP-42 reduction. It does not resolve QLP-42. We write `pi=1+i`.

## Complete finite reduction

A length-21 binary word of weight 4 cannot have a nontrivial cyclic
stabilizer: periods dividing 21 would force its weight to be divisible by 3
or 7. Consequently its `C(21,4)=5,985` labeled words form exactly 285 full
rotation orbits.

For one such `H_B` axis word there are four imaginary positions and 17 real
positions. The equation `sum(H_B)=1` requires two negative imaginary entries
and eight negative real entries, giving exactly

```text
C(4,2) C(17,8) = 145,860
```

sign assignments per orbit and 41,570,100 assignments over all 285 orbit
representatives.

The established `q=41` reflection theorem gives 1,024 half-axis words for
`H_A`. The third-order equations fix the ten sign XORs in the reflected
pairs. The verifier exhausts all 1,024 pair-sign masks and retains the exact
sum-zero assignments. It groups the resulting requirements by the 150
realized family-`B` autocorrelation signatures, without discarding any
assignment.

For a Gaussian integer `z`, both implementations compute its canonical
`pi`-adic digits by repeatedly subtracting `(Re(z)+Im(z)) mod 2` and dividing
exactly by `pi`. Concatenating the ten PAF residues gives a fingerprint in
`(Z[i]/(pi^k))^10`. Intersecting the `H_B` support with the required
`-2-PAF(H_A)` support gives:

| imposed `H` level | family-`B` orbits | axis orbits | labeled axis pairs | compatible `A` assignments |
|---:|---:|---:|---:|---:|
| modulo `pi^4` | 285 | 129,384 | 2,717,064 | 33,972,224 |
| modulo `pi^5` | 285 | 113,476 | 2,382,996 | 6,658,752 |
| modulo `pi^6` | 277 | 3,192 | 67,032 | 54,000 |
| modulo `pi^7` | 15 | 54 | 1,134 | 288 |
| modulo `pi^8` | 15 | 54 | 1,134 | 288 |
| modulo `pi^9` | 9 | 42 | 882 | 240 |
| modulo `pi^10` | 9 | 42 | 882 | 240 |
| modulo `pi^11` | 9 | 42 | 882 | 240 |
| modulo `pi^12` | 9 | 42 | 882 | 240 |

Order 12 is exact here. A residual coordinate of the `H` equation has real
and imaginary magnitudes bounded by 43 and 41, respectively, hence modulus
less than 64. A nonzero Gaussian integer divisible by `pi^12` has modulus at
least `|pi|^12=64`, so a matching order-12 fingerprint is an exact equality.

## Terminal exact-`S` obstruction

For every one of the 42 exact-`H` axis pairs, the verifier imposes the
complementary `S` axes, the established third-order reflected-pair XORs, and
each canonical exact-sum target:

| case | `sum(S_A)` | `sum(S_B)` | exact-`H` input axes | exact `H`+`S` survivors |
|---:|---:|---:|---:|---:|
| 0 | `(1,-1)` | `(4,-5)` | 42 | 0 |
| 1 | `(3,-3)` | `(4,-3)` | 42 | 0 |
| 2 | `(3,-3)` | `(0,-5)` | 42 | 0 |
| 3 | `(5,-1)` | `(4,-1)` | 42 | 0 |
| 4 | `(5,-1)` | `(4,1)`  | 42 | 0 |
| 5 | `(5,-3)` | `(0,-3)` | 42 | 0 |

The aggregate terminal scan evaluates 2,442,492 exact-sum `S_B` assignments
and 32,384 exact-sum `S_A` assignments. It intersects the exact target
fingerprints

```text
PAF(S_A,s) + PAF(S_B,s) = -2  at s=4,
                           2  at s=10,
                           0  otherwise.
```

Again order 12 is exact: an `S` residual has component bounds 44 and 42 and
therefore modulus below 64. The local-state theorem makes the `H` and `S`
sign choices independent once their complementary axes and required pair
XORs are fixed, so exhausting the two exact supports is complete.

## Fail-closed parallel certificate

`verify_weight4_exact_closure.cpp` is the aggregate scalar C++20 verifier.
It uses bit-popcount PAF evaluation and sorted exact residue supports. It
also compares 7,546 assignments, selected solely from stable signature,
orbit, axis, and sign identifiers, against a definition-level scalar PAF
implementation. The selection is independent of worker scheduling.

The Python driver first performs the complete serial run. It then assigns
whole autocorrelation-signature groups deterministically to isolated worker
processes. Every worker builds each assigned `A` table once and emits one
record per canonical `B` orbit. The coordinator independently enumerates all
5,985 weight-4 words, proves that they form 285 disjoint size-21 orbits, and
rejects missing, duplicate, unexpected, failed, or unfinished shard output.
It sorts by canonical orbit ID and compares every merged record and aggregate
counter with the serial run.

Two-, three-, and eight-worker runs agree entry-for-entry with the serial
run. On the recorded 10-core host their orbit phases took 17.1, 12.2, and
6.6 seconds, versus 32.5 seconds serial. Thus the measured eight-worker
speedup is about 4.9 times; no larger speedup is claimed. The canonical
285-record stream SHA-256 is

```text
d500ed89afbb5bf98c66afd93236b0f508dc447081835d3c16f461e5ddf79924
```

`independent_numpy_frontier.py` is separately written. It constructs fixed-
cardinality sign sets from Python's combination iterator, evaluates every
correlation directly in signed NumPy arrays, and performs explicit Gaussian
division. It verifies the orbit manifest, fully recomputes orders 4 through
12 for all nine terminal family-`B` orbits and eight deterministic empty
controls, then independently checks all `42*6=252` terminal exact-`S` cases.
It finds zero survivors.

Run the complete certificate and a sanitizer build with:

```sh
python3 -m pip install -r requirements.txt
python3 verify_weight4_exact_closure.py
python3 verify_weight4_exact_closure.py --sanitizers
shasum -a 256 -c SHA256SUMS
```

The driver honors `CXX`; otherwise it prefers `g++-16` when installed and
falls back to `clang++`. The recorded run used GCC 16.1.0, Python 3.12.12,
and NumPy 2.2.2 on arm64 macOS. AddressSanitizer and
UndefinedBehaviorSanitizer pass in serial and two-process modes. The C++
workers do not share memory, so the parallel proof kernel has no C++ data
race surface; Python threads only supervise independent subprocesses.

## Scope, provenance, and trust boundary

The proof trusts the previously established `q=41` coupled transform,
reflection theorem, third-order pair-XOR equations, canonical sum cases, and
the local-state independence of `H` and `S`; source inspection; C++ and
NumPy signed-integer semantics; the compiler/interpreter, Python subprocess
supervision, operating system, and hardware. All mathematical arithmetic is
integral. There is no floating point, randomness, solver status, heuristic
cutoff, concurrency-dependent audit selection, or time limit. This is not a
proof-assistant formalization.

Primary context:

- Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
  <https://arxiv.org/abs/2212.10953>;
- Jedwab--Pender, *Two constructions of quaternary Legendre pairs of even
  length*, <https://arxiv.org/abs/2408.08472>;
- Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
  <https://arxiv.org/abs/2408.16318>.

The last source identifies length 42 as the smallest unresolved case. A
fresh search as of 2026-09-01 found no later primary source resolving
length 42 and no matching exact weight-4 `H`/`S` obstruction. Apparent
novelty is relative to those primary-source and committed-graph searches,
not a historical-priority claim.

Public source directory:
<https://github.com/njallskarp/math_source_code_open/tree/main/qlp42_q41_weight4_exact_closure>.
The verified source commit is recorded separately in the Discovery Net
contribution and its post-commit graph receipt.

The strongest next step is weight 8. It has a much larger orbit space, so the
validated deterministic sharding and signature-table reuse introduced here
should materially affect feasibility.
