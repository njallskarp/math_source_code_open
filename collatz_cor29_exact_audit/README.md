# Exact prefix audit of Hercher's Corollary 29 search

This directory begins removing the largest remaining trust-boundary issue in
the published Collatz cycle-length bound: the official Corollary 29 C++ search
uses ordinary binary64 (`double`) arithmetic for quantities that decide whether
a residue branch has been proved.

`audit_prefix.py` mirrors the official residue-tree recurrence twice:

1. with the same binary64 formulas used in `collatz_cycle.cpp`; and
2. with exact integers and `fractions.Fraction` rational arithmetic.

It compares every pruning decision, every integer multiplier used to correct
the least starting value, and the condition that controls creation of the
second residue branch. (The corrected value itself commonly exceeds `2^53` and
is therefore not expected to be exactly representable as binary64.) Multiplier
differences are reported in both directions; a binary64 multiplier above the
exact ceiling is potentially nonconservative even when it does not change the
observed pruning decision on the audited prefix. The exact
state uses the identity that after `r` shortcut steps containing `o` odd steps,
the trajectory's leading factor is exactly `3^o/2^r`; no floating
approximation is required.

## Run

Tested with Python 3.12.12 and standard-library dependencies only.

```bash
python3 audit_prefix.py --depth 20 --c 1536
python3 -m unittest -v test_audit_prefix.py test_sharded_audit.py

g++-16 -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  -I/opt/homebrew/include \
  audit_prefix_fast.cpp -o audit_prefix_fast
python3 compare_implementations.py --binary ./audit_prefix_fast \
  --depth 12 --depth 16 --depth 20 --depth 25
./audit_prefix_fast --depth 45 --c 1536

./audit_prefix_fast --split-depth 25 \
  --frontier-out frontier-depth25.txt --c 1536
python3 run_sharded_audit.py \
  --binary ./audit_prefix_fast \
  --frontier frontier-depth25.txt \
  --depth 35 --shard-count 8 --jobs 8 \
  --results-directory shard-results-depth35 \
  --aggregate-out aggregate-depth35.txt
python3 verify_margin_witness.py \
  --aggregate aggregate-depth35.txt \
  --frontier frontier-depth25.txt \
  --binary ./audit_prefix_fast
```

The official computation used depth 300 and took weeks. This implementation is
still a **prefix auditor**, not a claimed reproduction of that full search. Its
purpose is to validate the exact recurrence, measure binary64 decision margins
on accessible prefixes, and provide a base for a checkpointed, parallel exact
depth-300 audit.

`audit_prefix_fast.cpp` removes normalized `Fraction` objects from the search's
hot path. If a state has `o` odd steps, it stores the running reciprocal sum as
an integer divided by `3^o`; a correction factor is stored as exponents in
`2^p/3^q`; and pruning is reduced to integer cross-products. The exact ceiling
correction uses

```text
ceil((S * min_factor_den - rest * min_factor_num)
     / (min_factor_num * 2^depth)).
```

The binary64 side retains the operation order and constants of the official
program. The comparison harness checks every reported field, including the
reduced exact minimum-margin fraction, against the slower Python reference.

The C++ measurements below used Homebrew GCC 16.2.0 and Boost 1.92.0 on arm64
macOS. The generated binary is intentionally not committed.

### Deterministic restartable decomposition

The compact checker can serialize every surviving state at a chosen split
depth. Format `collatz_cor29_frontier_v1` writes every exact integer in decimal
and every binary64 value by its 16 hexadecimal bits, so loading a frontier
recovers the exact machine state rather than a decimal approximation. The file
also records the complete audit counters and minimum margin through the split.

State indices are assigned by the deterministic depth-first traversal. For
`M` shards, shard `i` receives exactly the indices congruent to `i` modulo `M`.
These residue classes are disjoint and cover all serialized states. The Python
runner binds every shard result to the SHA-256 hashes of both the frontier and
compiled binary, writes results atomically, validates existing results before
reusing them, and checks that the selected-state counts sum to the full frontier
before aggregation. Additive counters are summed, the maximum multiplier error
is maximized, and exact rational margins are minimized.

A depth-16 frontier was serialized twice with identical SHA-256
`6ff2cb370ea46464804514d513b0dc97c6c70aeeb03ebe9a07a2bf5b20bd6e04`.
Partitioning its 1,492 states into four shards through depth 25 reproduced every
field of the monolithic depth-25 result. A second invocation reused all four
validated shard files and produced the same aggregate.

For a realistic checkpoint, the depth-25 frontier contains 108,417 states in
16,074,772 bytes and has SHA-256
`da01c7ecdef1538e77f583620df9ab29376b1b21340ab0c795933ebfe6264602`.
Eight independent modulo shards extended it through depth 35. Their exact
aggregate reproduced the earlier monolithic result: 40,609,380 generated
states, 7,966,661 exact prunes, 12,338,030 frontier states, zero decision or
branch disagreements, and the same minimum rational margin. This verifies the
decomposition on a nontrivial prefix; it does not yet constitute the remaining
depth-300 computation.

### Replayable minimum-margin witnesses

Frontier and aggregate format version 2 preserve a witness whenever the exact
audit finds a new smallest decision margin. A root witness records its complete
branch word. A sharded witness records the deterministic depth-25 frontier
index and its branch suffix, together with the depth, minimum-mean numerator
and denominator, residue representative, exact correction multiplier, and
corrected starting value. These fields directly recompute
`abs(A * local_mean - 1)` without floating-point arithmetic.

`verify_margin_witness.py` checks the frontier and binary SHA-256 bindings,
independently rebuilds the selected frontier state's exact integers and
rationals from the root using the slower Python representation, replays the
suffix, and checks every exact witness field. The independently computed
binary64 mean can differ from the serialized optimized-C++ value by one ULP
because the two representations do not use identical floating-point operation
sequences. The replay claim is therefore deliberately restricted to exact
reachability and exact decision arithmetic; the serialized C++ bits remain the
binding for the paired binary64 audit. Global minimality of a witness still
depends on the exhaustive, hash-bound shard aggregate rather than on the local
replay alone.

## Audited results

### Independent depth-25 frontier check

For `c = 1536`, the exact auditor exhausts the full residue prefix through
depth 25:

```text
generated=354394
pruned_exact=68781
frontier=108417
decision_disagreements=0
corrected_multiplier_disagreements=34684
float_multiplier_below_exact=9116
float_multiplier_above_exact=25568
maximum_multiplier_error=10923
second_branch_disagreements=0
minimum_scaled_margin=
  11796408962455432207351/8460546455991037544567792649
```

Here the scaled margin is `abs(A * local_mean - 1)`; its minimum is about
`1.39428e-6`. Thus no binary64 pruning decision differs from exact arithmetic
on this prefix, but the smallest observed decision margin is already small.
Moreover, binary64 selects a different ceiling multiplier in 34,684 states,
including 25,568 potentially nonconservative upward differences. Those
differences did not flip a prefix decision, but they show why a full exact or
directed-rounding audit is warranted rather than assuming numerical safety.

As an independent implementation check, the unmodified official C++ source was
compiled with GCC 14.4.0 in the `gcc:14` container image (image digest
`sha256:88134abee5c979390be4fedf9af2635e324004f0f3c1266a8c924c7a08e69500`).
Before entering its depth-300 continuation it printed the same depth-25
frontier count, `108417`. The full run was intentionally stopped; no conclusion
about the remaining tree is claimed.

### Exact extension through depth 30

The paired exact/binary64 audit was extended five levels beyond the official
parallelization frontier:

```text
depth=30
generated=3790686
pruned_exact=734461
frontier=1160883
decision_disagreements=0
corrected_multiplier_disagreements=39878
float_multiplier_below_exact=10026
float_multiplier_above_exact=29852
maximum_multiplier_error=10923
second_branch_disagreements=0
minimum_scaled_margin=
  2989566120402674981159/2058234223534933879597325018841
```

The final margin is about `1.45249e-9`. No unsafe pruning is observed among
3,790,686 generated states, although the continued upward multiplier drift
still prevents extrapolation to the 270 unexamined levels. The depth-30 run is
an exact verified computation of this implementation; unlike the depth-25
frontier count, it was not separately reproduced with the official C++ binary.

### Compact-invariant extension through depth 45

The optimized implementation exactly matched the Python reference at depths
12, 16, 20, 25, and 32. At depth 32 it reduced elapsed time on this machine from
337.68 seconds to 5.27 seconds while reproducing all output fields. Depth 41
was run both monolithically and as eight hash-bound shards; every field matched.
Depths 42 through 45 were then completed with the same decomposition. The
depth-45 run used the replayable version-2 certificate:

```text
frontier_sha256=75bd7a0c0e18263935910646c097c3fecb008c4ede6d3005ecec9749d8c32198
binary_sha256=40765190d1e7ab7bd18b84c70741381398b632c91df88b21b33d27097f18cb40
shard_count=8
selected_states=108417
```

```text
generated=4677343410
pruned_exact=936919394
frontier=1401752312
decision_disagreements=0
corrected_multiplier_disagreements=42521
float_multiplier_below_exact=10436
float_multiplier_above_exact=32085
maximum_multiplier_error=10923
second_branch_disagreements=0
minimum_scaled_margin=
  575662982657459068858763/221051743115939704517342540931141237
minimum_margin_origin=29559
minimum_margin_depth=43
minimum_margin_path=010100000110000010
minimum_margin_mean_num=202335691639831
minimum_margin_mean_den=213516729579636
minimum_margin_rest_start=2250912350777
minimum_margin_exact_multiplier=470795402
minimum_margin_corrected_start=4141160152670722638393
```

The minimum scaled margin is approximately `2.60420e-12`; it first appears by
depth 43 and remains the minimum at depth 45. The Python replay checker rebuilt
frontier state 29,559 from the root, reproduced its exact rational state,
replayed the 18-bit suffix, and independently recovered every exact witness
field and the reduced margin. This is an exact verified computation of the
compact-invariant implementation, cross-checked against the independent Python
representation on smaller complete prefixes and against the monolithic
execution at depth 41. It does not certify depths 46 through 300.

## Primary source and trust boundary

- C. Hercher, official Corollary 29 program,
  <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/collatz_cycle.cpp>,
  retrieved 2026-08-31, SHA-256
  `aee76b12281e69f0ded6bc7e527f88c71453b10acbe5e1b19bca86fd69a2c372`.
- C. Hercher, “There are no Collatz m-Cycles with m <= 91,” *Journal of
  Integer Sequences* 26 (2023), Article 23.3.5,
  <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html>.

The exact mirror was independently transcribed from the published program, so
transcription and semantic-equivalence errors remain possible. The two local
implementations share that transcription and therefore are not fully
independent. Agreement with binary64 on a finite prefix does not certify the
unexamined depth-300 tree. The deterministic frontier, parallel subtree,
restartable checkpoint, and exact aggregate layers are now implemented and
tested, but a complete audit still requires executing depths 46 through 300 and
independently checking the semantic transcription from the official program.
