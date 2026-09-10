# Independent review: incomplete QLP(64) multiplier cover

**Verdict: major revision.** The full-family exclusion and its affine
corollary are unsupported and have been withdrawn. The supplied finite
queues have no witnesses, but the compression generator omits valid children.
See [REPORT.md](REPORT.md) for the complete assessment.

Independent direct enumeration gives **140** canonical compressed quadruples
at length 8. The historical generator retains **72** and omits **68**.
This package also independently exhausts both historical final queues using
all correlation lags. It does not claim a QLP(64) counterexample, a corrected
full-family search, or restoration of the withdrawn theorem.

## Reproduce the decisive coverage audit

Python 3.10+ standard library is sufficient. From the repository root:

```sh
python3 -B qlp64_fixed_multiplier_independent_review/coverage_check.py --check
```

Expected: `status: PASS`, `canonical: 140`, `retained_canonical: 72`,
`omitted_canonical: 68`, and `is_qlp_counterexample: false`.
The complete sorted canonical length-8 list, serialized as compact JSON plus
a newline, has SHA-256
`f842cbd61ebc90951c08c9b3a8b6e4d54fa3a62564f1f9b8748f9c834fd0fa12`.
The list itself is regenerated, not published.

To compare the entire retained set with the actual historical generator:

```sh
python3 -B qlp64_fixed_multiplier_independent_review/historical_source.py /tmp/qlp64-review/archived
python3 -B qlp64_fixed_multiplier_independent_review/coverage_check.py --check --historical-module /tmp/qlp64-review/archived/compress.py
```

The helper exports eight explicitly named, hash-verified historical files
from commit `005c8e773d178e0fb050261885ecfd445bfe8de3`. It does not alter the
current withdrawal notice or disabled runner. `source_hashes.json` pins all
eight historical files. The optional comparison imports the archived
generator **after** completing the independent direct-box enumeration.

## Reproduce the historical queues and independent final searches

These slower commands verify the finite queues only. They cannot repair
the coverage defect. A C++20 compiler is also needed:

```sh
python3 -B /tmp/qlp64-review/archived/run.py --workdir /tmp/qlp64-review
python3 -B /tmp/qlp64-review/archived/compress.py --audit-reduction
python3 -B qlp64_fixed_multiplier_independent_review/bridge_check.py
python3 -B qlp64_fixed_multiplier_independent_review/build.py /tmp/qlp64-review/full_lag_check
/tmp/qlp64-review/full_lag_check /tmp/qlp64-review/compressed.txt 31
/tmp/qlp64-review/full_lag_check /tmp/qlp64-review/compressed.txt 63
```

The old runner prints `verified: true`, 1,472 parents, and zero witnesses.
That output is historical and **does not verify the withdrawn theorem**.
Its regenerated parent input hash is
`26ed05773c9fc2d46bbabaac93ae61d8a17e14b718c2a21124b6305853d8957a`.

Each new final search must print `status: PASS`, 1,472 parents, 966 distinct
compressed rows, 343,104 full words, and zero witnesses. The pair counts
are 1,698,693,120 for multiplier 31 and 494,690,304 for multiplier 63.
Compact exact outputs are in `expected.json`; progress goes to stderr.

`full_lag_check.cpp` imports no reviewed code. It constructs rows by generic
negative-count equations on multiplier orbits, checks each word's compression
and invariance, and matches **unscaled** correlations at all 32 real and
31 skew lags using 16-bit entries and both skew orientations. It avoids the
author's seven/eight-lag reduction and sign-canonical key implementation.
The complete key is compared, so hash collisions cannot lose a match.
The three relevant Gray pairings are restored for multiplier 31. At 63,
every skew entry is explicitly computed and checked to be zero.

`bridge_check.py` compares pairing/sign restoration with the literal
Gaussian-integer definition on 20,752 labelled small-order quadruples,
including 256 positive QLP controls and 320 real-only false positives.
It also checks 4,160 half-period identities and all 2,048 affine permutations.
These checks remain valid but do not establish the missing compression cover.

Execution used CPython 3.12.12 and Apple clang 17.0.0
(`clang-1700.6.3.2`), C++20, `-O3 -Wall -Wextra -Wpedantic -Wshadow -Werror`.
All acceptance arithmetic is integral. There is no formal proof assistant,
solver, external queue input, or floating-point premise. Parent lists,
executables, and verbose output remain in temporary directories.
