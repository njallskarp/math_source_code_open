# Complete transition-closed repair of 22 BHR `{1,2,11}` cap orthants

## Result

For every row below, write `(A,B,C)` for the displayed cap.  Then for all
`p,q,r >= 0`, the multiset

\[
  \{1^{A+p},2^{B+2q},11^{C+11r}\}
\]

has a Hamiltonian-path realization in the cyclically labelled complete graph
on `A+B+C+p+2q+11r+1` vertices.

| residue | cap `(A,B,C)` | order |
|---|---:|---:|
| `(1,1,1)` | `(1,9,12)` | 23 |
| `(1,1,2)` | `(2,7,13)` | 23 |
| `(1,1,3)` | `(2,7,14)` | 24 |
| `(1,1,4)` | `(2,7,15)` | 25 |
| `(1,1,5)` | `(2,7,16)` | 26 |
| `(1,1,6)` | `(2,7,17)` | 27 |
| `(1,1,7)` | `(2,7,18)` | 28 |
| `(1,1,8)` | `(2,7,19)` | 29 |
| `(1,1,9)` | `(2,11,9)` | 23 |
| `(1,1,10)` | `(1,11,10)` | 23 |
| `(1,1,11)` | `(2,9,11)` | 23 |
| `(1,2,1)` | `(2,8,12)` | 23 |
| `(1,2,2)` | `(1,8,13)` | 23 |
| `(1,2,3)` | `(1,8,14)` | 24 |
| `(1,2,4)` | `(1,8,15)` | 25 |
| `(1,2,5)` | `(1,8,16)` | 26 |
| `(1,2,6)` | `(3,6,17)` | 27 |
| `(1,2,7)` | `(3,6,18)` | 28 |
| `(1,2,8)` | `(3,6,19)` | 29 |
| `(1,2,9)` | `(1,12,9)` | 23 |
| `(1,2,10)` | `(2,10,10)` | 23 |
| `(1,2,11)` | `(1,10,11)` | 23 |

This closes all seven nonempty boundary/interior strata above each of the 22
caps, as well as the cap itself.  It strictly strengthens the tri-modal-core
result in `TRIMODAL_SAFE_CORES.md`.  It is not a proof of the full BHR
conjecture for support `{1,2,11}`: finite-thickness regions below at least one
cap coordinate remain.

## The 66 pairwise face seeds

Each embedded cap path is simultaneously growable in modes `1`, `2`, and
`11`.  For each of the three unordered mode pairs, apply both modes once in
both possible orders, transporting every selected cut after each gap
insertion.  Direct definition-level checking proves, for every cap and pair,
that both operations are legal at every step and their two labelled endpoints
and transported cut triples agree exactly.  Hence there are 66 explicit face
seeds, all deterministically derived from the 22 embedded cap paths.

Every cap path has maximum edge length `D=11` and order at least 23.  The
derived face orders and two-mode safe-margin thresholds are:

| face modes | least face order | `2D+x+y` |
|---|---:|---:|
| `{1,2}` | 26 | 25 |
| `{1,11}` | 35 | 34 |
| `{2,11}` | 36 | 35 |

Thus the safe-margin gap-refinement lemma proved in
`DEAD_ORTHANT_REPAIR.md` applies to every face seed.  It preserves both modes
and makes their refinements commute indefinitely.

For example, starting from the `(1,9,12)` cap, growing once by `2` and `11`
in either order gives counts `(1,11,23)`, order 36, selected cuts `1` and `13`
for modes `2` and `11`, and the identical path

```text
(7,18,29,31,20,9,11,22,33,35,24,13,2,0,34,23,12,10,21,32,30,19,
 8,6,17,28,26,15,4,5,16,27,25,14,3,1).
```

Its maximum edge length is 11 and `2*11+2+11=35<36`, so it generates every
point `(1,11+2q,23+11r)` with `q,r >= 0`.

## Eight-stratum partition proof

Fix a cap `(A,B,C)` and nonnegative `(p,q,r)`.  Let `S` be the subset of
`{1,2,11}` whose corresponding parameter is positive.  The eight possible
subsets are disjoint and exhaustive.

- If `S` is empty, use the cap path itself.
- If `S` has one mode, repeatedly apply that same growth operation from the
  cap.  Same-mode growth preserves its selected cut by the one-gap
  subdivision argument.
- If `S` has two modes, apply each once to reach the exact face seed, then use
  its two-mode safe-margin family for the remaining nonnegative increments.
- If `S` has all three modes, apply each once to reach the safe seed from
  `TRIMODAL_SAFE_CORES.md`, then use its finite-mode safe-margin family for
  the remaining increments.

For an additional consistency check, each of the 66 face seeds reaches its
stored tri-modal safe seed after one application of the missing mode.  The
checker verifies all 66 links exactly.  The four cases above therefore prove
the claimed complete cap orthant, independently of how large the parameters
are.

## Exact reproduction

With CPython 3.12.12 and no third-party package, run:

```bash
cd bhr_1_2_11_transition_repair
python3 verify_cap_orthants.py trimodal_certificate.json --grid 3
python3 -m unittest -v test_cap_orthants.py
```

The reference run checks 66 face seeds, 264 ordered cap-to-face derivation
steps, 66 face-to-tri-modal links, 330 ray paths, 1,650 face-family paths,
2,112 coordinate transitions, and 1,056 commuting squares.  Its principal
hashes are:

```text
trimodal certificate SHA-256:
532470ffe31ff3e5acb4da51a78c15f172d2d00db6816dd43d5dc44a243bc059

transition record SHA-256:
76d79ab6bc3d0dc6237feaea50be1f1bc16093096dfbf8a1c8e6adffc6d76680
```

`expected_cap_orthants.txt` contains the complete reference output.  The
finite grid is a regression check of the structural proof, not the basis for
its unbounded quantifiers.  Two negative tests alter a cap cut and a cap path
and confirm rejection.

## Conservative source-coverage audit

Given the pinned external source certificate, reproduce the transition-aware
coverage count with:

```bash
python3 audit_repaired_coverage.py /path/to/pinned/certificate.json
```

The audit first validates the 628 source witnesses, all one-mode rays, the
eight earlier repaired orthants, and the cap-orthant inputs.  Of the source
certificate's 9,544 admissible clamped patterns, the cumulative counts are
3,273 after exact points and rays, 3,457 after the eight earlier orthants,
5,999 after the 22 tri-modal cores, and 8,052 after the complete cap orthants.
Exactly 1,492 symbolic boundary patterns remain.  Their canonical digest is
`29dc950cba5a9d65ca59bb860568321ef2580e1a825175e14fabd89f1e4a2f1f`.
This is a coverage audit of proved regions, not a nonexistence claim about the
residual patterns.

The first residual pattern is base `(1,1,1)`, clamped target `(2,21,1)`, with
only its length-2 coordinate at the high sentinel.  It supplies a concrete
next construction target rather than an undifferentiated search expansion.

## Trust and novelty boundaries

The theorem trusts the embedded explicit paths, exact Python-integer cyclic
length and growth checks, the written safe-margin and stratum-partition
arguments, and CPython.  It does not trust a solver, the source certificate's
coverage conclusion, a bounded grid as an induction proof, or the external
certificate for more than the optional coverage audit.  The external source
bytes are pinned by SHA-256
`e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c`.

The primary literature is Ollis, Pasotti, Pellegrini, and Schmitt,
*Growable Realizations: a Powerful Approach to the Buratti-Horak-Rosa
Conjecture* (<https://arxiv.org/abs/2105.00980>) and Chand and Ollis, *The
Buratti-Horak-Rosa Conjecture Holds for Some Underlying Sets of Size Three*
(<https://arxiv.org/abs/2202.07733>).  Live primary-source and exact-phrase
searches on 2026-09-03 found no prior transition-closed cap-orthant partition
for this support.  This is a search-relative novelty statement, not a priority
claim.
