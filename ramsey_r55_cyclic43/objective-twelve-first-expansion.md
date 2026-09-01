# Exact first one-flip expansion of the complete Cyclic(43) objective-twelve frontier

## Setting

Let (M(x)) be the number of monochromatic copies of (K_5) in the
red-blue coloring of (K_{43}) encoded by a perturbation state (x), and
quotient states by the cyclic action (C_{43}).  Let (P_{11}) be the
certified primary component induced by (M\leq 11), and let

\[
F_{12}=\{[y]:M(y)=12,\ d_H(x,y)=1\text{ for some }x\in P_{11}\}
\]

be its complete objective-twelve boundary.  The preceding certificate gives

\[
|F_{12}|=1{,}041{,}887
\]

free rotation orbits.  Define the genuinely new part of its first sublevel-12
expansion by

\[
A_{12}^{(1)}=\{[z]:M(z)\leq12,\ d_H(y,z)=1\text{ for some }[y]\in F_{12}\}
\setminus(P_{11}\cup F_{12}).
\]

## Exact computational lemma

An exhaustive scan of all

\[
1{,}041{,}887\cdot903=940{,}823{,}961
\]

quotient-source edge flips proves

\[
\boxed{|A_{12}^{(1)}|=229}.
\]

Every new orbit is free and has objective exactly twelve.  In particular,

\[
A_{12}^{(1)}\cap\{[z]:M(z)\leq11\}=\varnothing.
\]

The 229 targets represent 9,847 labeled colorings.  Exactly 1,307 quotient
incidences join (F_{12}) to the new shell, with no parallel excess: the
number of distinct source-target pairs is also 1,307.  Only 1,196 frontier
orbits touch the shell.  Their numbers of distinct new targets have histogram

\[
\begin{array}{c|rrrrr}
d&0&1&2&3&4\\\hline
\#\text{ sources}&1{,}040{,}691&1{,}095&93&6&2.
\end{array}
\]

The target degrees are supported on (1,\dots,11), with exact histogram

\[
(23,3,22,38,25,24,30,26,11,23,4).
\]

The same scan independently recovers 4,656,506 reverse incidences from
(F_{12}) to (P_{11}) and finds 3,318,138 directed incidences internal to
(F_{12}), giving 1,659,069 quotient edges in the frontier layer.

## Independent verification

The optimized enumerator assigns contiguous source blocks to ten OpenMP
workers.  Each worker maintains exact single-edge monochromatic-(K_5) deltas,
canonicalizes every accepted neighbor under all 43 rotations, and aggregates
source-local multiplicities before a deterministic merge.

A separate verifier reconstructs each coloring and directly enumerates all
(\binom{43}{5}=962{,}598) five-sets at every source, for

\[
1{,}002{,}918{,}342{,}426
\]

five-set evaluations.  It independently rebuilt all 903 deltas and reproduced
all 229 representatives exactly.  It also agreed on every objective
histogram, every source and target degree histogram, all three incidence
totals, and the empty lower-objective set.  It reported zero omitted targets,
zero unexpected targets, zero objective mismatches, and zero canonicality or
orbit errors.

## Reproduction and hashes

Immutable source, full compact representative arrays, direct output, and tests:

<https://github.com/njallskarp/math_source_code_open/commit/36115a3fad927845b31f5ba23df093e4d172e7e8>

```bash
g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  scan_objective_twelve_first_expansion.cpp \
  -o /tmp/scan_objective_twelve_first_expansion

g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  verify_objective_twelve_first_expansion.cpp \
  -o /tmp/verify_objective_twelve_first_expansion

python3 -m unittest test_objective_twelve_component.py
```

```text
903d11599d0327dfa4e9a7994c76ffee387310f8ed23edc23ca1588b4d3c283e  scan_objective_twelve_first_expansion.cpp
95e489bde2bc8557737fe5bcf82fd5e533c3403ad48c5f3f4004a51d7cf33439  verify_objective_twelve_first_expansion.cpp
5b44b4a670e991dfd30c4c19c1f532702a50c42b8bc8bc26e77f7ebae00cca53  objective-twelve-first-expansion-fast.json
65ba9656a2c6ea1bfd8a189ffb14abd239d95524fe27507ac4421f35fcc7657d  objective-twelve-first-expansion-direct.json
653d1068c456d228c12d640a50eca409fceaf570dbb6040b66bebef296b2615c  temporary complete F12 representative input
```

The run used Homebrew GCC 16.2.0, Python 3.12.12, and ten OpenMP threads.

## Literature and novelty assessment

The search was contextualized by Ge et al.'s study of Exoo's low-
monochromatic-(K_5) Cyclic(43) construction
(<https://arxiv.org/abs/2212.12630>), Angeltveit and McKay's current
(R(5,5)\leq46) computation (<https://arxiv.org/abs/2409.15709>), and
McKay's Ramsey graph data
(<https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>).  No matching
classification of this first perturbation expansion was found in those
primary sources or in the committed Discovery Net graph before this run.
The result is apparently new relative to the searched sources; no universal
priority claim is made.

## Scope and trust boundary

This is a complete first expansion of the certified (F_{12}), not yet the
closure theorem by itself.  It concerns the primary Cyclic(43) perturbation
component only; it neither classifies disconnected low-objective components
nor changes the global numerical bounds on (R(5,5)).  The two enumerators
use different objective-update methods but share C++, the seed convention,
some cyclic canonicalization logic, and the persisted lower certificates.

