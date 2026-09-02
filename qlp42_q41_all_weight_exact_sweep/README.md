# Exact all-weight closure of the QLP-42 `q=41` branch

## Theorem

In the established canonical coupled length-21 transform of the norm-32
QLP-42 shell, the complete `q=41` branch is empty.  More precisely, no lift
at any admissible binary Gaussian-axis weight

```text
wt(H_B axis) in {0,4,8,12,16,20}
```

satisfies the exact Gaussian sum and nonzero-shift autocorrelation equations
for both transformed components `H` and `S`.

The established third-order classification makes this list complete.  It
allows weights 4, 8, 12, and 16 in all six canonical global-sum cases,
weight 0 only in cases 2 and 5, and weight 20 only in cases 3 and 4.  The
all-weight computation leaves exact-`H` frontiers at weights 0, 4, 8, 12,
and 16 and eliminates weight 20 already modulo `(1+i)^7`.  Exact `S`
support intersection eliminates every remaining admissible axis/case pair.

This is a finite computer-assisted theorem inside the prior coupled QLP-42
reduction.  It closes the `q=41` branch, not the separate `q=1` branch, and
therefore does not by itself resolve QLP-42.  We write `pi=1+i`.

## Complete finite reduction

For even weight `w`, the equation `sum(H_B)=1` requires exactly `w/2`
negative imaginary entries and `(20-w)/2` negative real entries.  Therefore
each canonical axis orbit has

```text
C(w,w/2) C(21-w,(20-w)/2)
```

exact sign assignments.  Exhaustive rotation canonicalization gives:

| weight | labeled axes | rotation orbits | signs/orbit | evaluated assignments |
|---:|---:|---:|---:|---:|
| 0  | 1       | 1      | 352,716 | 352,716 |
| 4  | 5,985   | 285    | 145,860 | 41,570,100 |
| 8  | 203,490 | 9,690  | 120,120 | 1,163,962,800 |
| 12 | 293,930 | 14,000 | 116,424 | 1,629,936,000 |
| 16 | 20,349  | 969    | 128,700 | 124,710,300 |
| 20 | 21      | 1      | 184,756 | 184,756 |
| **total** | **524,776** | **24,946** | — | **2,960,716,672** |

Weight 12 is the only exceptional orbit manifest: five orbits have size 7
and 13,995 have size 21.  All other positive-weight orbits have size 21;
the weight-0 orbit has size 1.  The coordinator reconstructs these
multiplicities independently and rejects every missing, duplicate,
unexpected, or wrongly sized record.

The 24,946 canonical axes realize all 512 autocorrelation signatures.  The
sweep groups all six weights by signature, builds the family-`A` exact-sum
table once per signature, processes all associated family-`B` axes, and
then releases the table.  This shares 512 tables across weights without
holding them simultaneously.

For a Gaussian integer `z`, both implementations compute its canonical
`pi`-adic digits by repeatedly subtracting `(Re(z)+Im(z)) mod 2` and
dividing exactly by `pi`.  Concatenating all ten nonzero-shift PAF residues
gives a fingerprint in `(Z[i]/(pi^k))^10`.  Intersecting complete `H_B`
supports with the required `-2-PAF(H_A)` supports gives these surviving
family-`A`/family-`B` axis-orbit counts:

| weight | `pi^4` | `pi^5` | `pi^6` | `pi^7` | `pi^8` | `pi^9` through `pi^12` |
|---:|---:|---:|---:|---:|---:|---:|
| 0  | 8 | 8 | 8 | 6 | 6 | 4 |
| 4  | 129,384 | 113,476 | 3,192 | 54 | 54 | 42 |
| 8  | 4,440,762 | 4,243,802 | 93,178 | 546 | 330 | 198 |
| 12 | 6,426,598 | 6,173,100 | 136,390 | 792 | 396 | 252 |
| 16 | 438,432 | 412,518 | 10,176 | 36 | 36 | 24 |
| 20 | 512 | 418 | 4 | 0 | 0 | 0 |

At order 12 the surviving weights occupy respectively 1, 9, 81, 116, 12,
and 0 family-`B` orbits.  Order 12 is exact: a coordinate of the `H`
residual has real and imaginary magnitudes at most 43 and 41, so its modulus
is below 64.  A nonzero Gaussian integer divisible by `pi^12` has modulus at
least `|pi|^12=64`; hence a matching order-12 fingerprint is an equality,
not merely a congruence.

## Terminal exact-`S` obstruction

For every exact-`H` axis pair, the verifier imposes the complementary `S`
axes, the established third-order reflected-pair XORs, and the admissible
canonical exact-sum targets:

| weight | admissible cases | exact-`H` axes per case | exact `S_B` assignments | surviving axis/case pairs |
|---:|:---|---:|---:|---:|
| 0  | 2,5 | 4 | 497,420 | 0 |
| 4  | 0–5 | 42 | 2,442,492 | 0 |
| 8  | 0–5 | 198 | 23,675,652 | 0 |
| 12 | 0–5 | 252 | 34,222,320 | 0 |
| 16 | 0–5 | 24 | 3,425,136 | 0 |
| 20 | 3,4 | 0 | 0 | 0 |

The combined terminal scan evaluates 64,263,020 exact-sum `S_B`
assignments.  Sharing the `S_A` support by signature, half-axis, and case
evaluates 231,400 exact-sum `S_A` assignments.  The independent verifier
checks all 3,104 admissible exact-`H` axis/case pairs and finds zero
survivors.  The `S` residual has component bounds 44 and 42 and likewise
has modulus below 64, so order 12 is exact for `S` as well.

The local-state theorem from the preceding reduction makes the `H` and `S`
sign variables independent after their complementary axes and required
pair XORs are fixed.  Exhausting the two exact supports is therefore
complete.

## Parallel certificate and independent replay

`verify_all_weights_exact_sweep.cpp` is the production scalar C++20
verifier.  It uses bit-popcount PAF evaluation and sorted exact residue
supports.  Stable hashes of the signature, axis, and sign identifiers select
369,577 assignments for comparison with a definition-level scalar PAF
implementation; audit selection is independent of worker scheduling.

Whole signature groups are assigned deterministically to isolated worker
processes.  Each process emits one record keyed by `(weight, canonical
axis)`.  The Python coordinator independently generates the full orbit
manifest, including the five short weight-12 orbits, reconstructs the
canonical stream in sorted order, and rejects incomplete or overlapping
shards.  Eight- and three-worker release sweeps produced identical summaries
and the same complete-stream SHA-256:

```text
294a1448ee1ca8b5051985a3771027d97432311215f7f13bd09c027fe3434c42
```

The eight-worker sweep took 220.550 seconds; the three-worker replay took
405.010 seconds on the recorded 10-core arm64 macOS host.  A complete
two-worker AddressSanitizer/UndefinedBehaviorSanitizer sweep took 1,807.276
seconds and produced the identical summary and stream digest with no
diagnostic.

`independent_numpy_frontier.py` is separately written.  It constructs fixed-
cardinality sign sets from Python's combination iterator, evaluates every
correlation directly in signed NumPy arrays, and implements explicit
Gaussian division.  It independently reconstructs all 24,946 orbits, fully
recomputes orders 4 through 12 for all 219 terminal family-`B` orbits and
nine deterministic empty controls, and checks all 3,104 terminal cases.  It
agrees exactly and finds zero survivors.  Its fixed-width arrays are safe:
all unit products are in `{-1,0,1}`, a length-21 PAF component is at most 21
in magnitude, and residue division is performed after conversion to signed
32-bit integers.

Run the complete release certificate and the full sanitizer sweep with:

```sh
python3 -m pip install -r requirements.txt
python3 verify_all_weights_exact_sweep.py --workers 8,3
python3 verify_all_weights_exact_sweep.py --workers 2 --sanitizers --skip-independent
shasum -a 256 -c SHA256SUMS
```

The driver honors `CXX`; otherwise it prefers `g++-16` and falls back to
`clang++`.  The recorded runs used GCC 16.2.0, Python 3.12.12, and NumPy
2.2.2.  C++ workers share no memory; Python threads only supervise isolated
subprocesses.  No randomness, heuristic cutoff, solver status, floating
point, or time limit enters the claim.

## Scope, provenance, and trust boundary

The proof trusts the established canonical coupled transform, the `q=41`
reflection and third-order axis/sign classification, the six canonical sum
cases, and local `H`/`S` sign independence; source inspection; C++ and NumPy
integer semantics; compiler/interpreter, operating system, and hardware.
It is not a proof-assistant formalization.

Primary context:

- Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
  <https://arxiv.org/abs/2212.10953>;
- Jedwab--Pender, *Two constructions of quaternary Legendre pairs of even
  length*, <https://arxiv.org/abs/2408.08472>;
- Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
  <https://arxiv.org/abs/2408.16318>.

The last source identifies length 42 as the smallest unresolved case.  A
fresh primary-source search and committed-graph query on 2026-09-02 found no
matching complete `q=41` obstruction.  Apparent novelty is relative to those
searches, not a historical-priority claim.

Public source directory:
<https://github.com/njallskarp/math_source_code_open/tree/main/qlp42_q41_all_weight_exact_sweep>.
The verified source commit is recorded separately in the Discovery Net
contribution and its post-commit graph receipt.

The strongest next step is to combine this complete branch obstruction with
the independent `q=1` branch results and determine the smallest remaining
exact frontier toward a full QLP-42 resolution.
