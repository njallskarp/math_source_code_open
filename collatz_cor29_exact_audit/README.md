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
python3 -m unittest -v test_audit_prefix.py
```

The official computation used depth 300 and took weeks. This implementation is
deliberately a **prefix auditor**, not a claimed reproduction of that full
search. Its purpose is to validate the exact recurrence, measure binary64
decision margins on accessible prefixes, and provide a base for an optimized
exact or interval-arithmetic implementation.

## Depth-25 result

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

## Primary source and trust boundary

- C. Hercher, official Corollary 29 program,
  <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/collatz_cycle.cpp>,
  retrieved 2026-08-31, SHA-256
  `aee76b12281e69f0ded6bc7e527f88c71453b10acbe5e1b19bca86fd69a2c372`.
- C. Hercher, “There are no Collatz m-Cycles with m <= 91,” *Journal of
  Integer Sequences* 26 (2023), Article 23.3.5,
  <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html>.

The exact mirror was independently transcribed from the published program, so
transcription and semantic-equivalence errors remain possible. Agreement with
binary64 on a finite prefix does not certify the unexamined depth-300 tree.
