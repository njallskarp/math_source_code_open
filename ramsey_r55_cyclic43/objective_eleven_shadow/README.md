# Objective-eleven boundary of the Cyclic(43) level-ten shadow

Let `P9` be the certified primary Cyclic(43) component induced by colorings
with at most nine monochromatic copies of `K5`. The preceding objective-ten
boundary audit identified exactly 65 objective-nine rotation orbits in `P9`
with no objective-ten neighbor. Every one has minimum external objective 11.
This directory classifies their complete one-flip objective-eleven
neighborhood.

## Exact result

Direct enumeration of all 903 reversals at the 65 shadow sources gives 528
quotient incidences with 427 distinct objective-eleven target orbits. Every
source--target orbit pair has multiplicity one, so the simple bipartite
quotient boundary also has 528 edges. All orbits are free, giving 18,361
labeled target colorings and 22,704 labeled directed incidences.

The source degrees have distribution

| degree | 6 | 7 | 8 | 9 | 14 | 15 |
|---:|---:|---:|---:|---:|---:|---:|
| source orbits | 6 | 20 | 16 | 20 | 1 | 2 |

The target degrees within the shadow incidence graph have distribution

| degree | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|
| target orbits | 336 | 83 | 6 | 2 |

Reverse scans against the complete primary objective-nine layer find 800
objective-nine incidences into these 427 targets. Exactly 196 targets also
touch a non-shadow primary objective-nine source; the other 231 meet the
primary objective-nine layer only through the shadow.

The 65-by-427 bipartite graph has eight connected components and cycle rank
44. Their `(source orbits, target orbits, edges)` profiles are

```text
(28,156,212), (18,108,136), (4,32,36), (4,32,36),
(4,28,32), (4,28,32), (2,29,30), (1,14,14).
```

Reflection fixes four components and exchanges the two equal-profile pairs.
It fixes 3 source rotation orbits and 7 target rotation orbits, so Burnside's
lemma gives 34 source and 217 target orbits under the full dihedral action.

This is the exact objective-eleven neighborhood of the 65 shadow sources, not
the complete objective-eleven frontier of the threshold-ten component. It
does not close the objective-eleven layer, classify disconnected low-objective
components, or determine `R(5,5)`.

## Reproduction

The checker independently reconstructs the Cyclic(43) seed, enumerates all
962,598 five-sets, verifies every source and target objective, canonicalizes
under all 43 rotations, and compares source- and target-side incidences.

```bash
g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  -Wall -Wextra -Wpedantic \
  verify_objective_eleven_shadow.cpp \
  -o verify_objective_eleven_shadow

OMP_NUM_THREADS=6 ./verify_objective_eleven_shadow \
  ../objective-nine-component-fast.json \
  ../objective-ten-frontier-independent.json \
  > objective-eleven-shadow.json

python3 -m unittest -v test_shadow_certificate.py
```

A fresh six-thread run with Homebrew GCC 16.2.0 took 2.47 seconds. The stored
target-list fingerprint is the deterministic FNV-1a value
`2774385fead7734e`; it is a regression fingerprint, not a cryptographic
commitment. A separate two-thread AddressSanitizer/UndefinedBehaviorSanitizer
build reproduced every mathematical field; only the recorded OpenMP thread
count differed.

SHA-256:

```text
06b9633c392b3b1fcfa43196cde2095144cf3095d264af8dfc88b324d441ff5d  verify_objective_eleven_shadow.cpp
86e1da636f1f266819be6eb9b5bc5552e94713c346e2fdd0ea29a3e100b867db  objective-eleven-shadow.json
06988814daa247540503bc2357065cd83fc873b1e1a2f26f9d33e415bf0b01bf  test_shadow_certificate.py
```
