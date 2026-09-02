# QLP-42 fourth Gaussian-layer witnesses

This directory gives exact, independently checkable witnesses showing that at
least 67 of the 216 exact-sum cells on the surviving QLP-42 `q=5/q=37`
frontier pass the fourth Gaussian residue layer.  There are 38 certified
`q=5` cells and 29 certified `q=37` cells.

Let `pi = 1+i`.  For each component `s,h` and each shift `1,...,10`, the
required residual is a Gaussian integer.  Since `pi^4=-4`, the fourth-layer
condition is exactly that both integer coordinates of every residual are zero
modulo 4.  Every one of the 18 `q=5` support orbits has at least one certified
surviving case, so this layer has zero support-orbit pruning power on that
branch.  Thirteen of the 18 `q=37` support orbits are certified.  This is a
lower-bound result, not a complete fourth-layer census: the other 149 cells are
unknown, and no fourth-layer exclusion is claimed.

The initial bounded sweep found four cells.  Its historical certificate is
preserved as `first_sweep_witnesses.tsv`, and its committed graph receipt is
`graph_receipt.json`.

A second deterministic pass seeded every unresolved cell with its original
third-layer word and, when available, every fourth-layer witness on the same
support orbit.  It completed all 212 unresolved keys with 56 local attempts per
key at free-cell counts `2,4,6,8,10,12,14` and found no additional witness.
This records the exhaustion of that bounded local-deformation strategy only;
it is not evidence that the unresolved cells are unsatisfiable.

An unrestricted pure-CNF sweep then processed the other 211 cells with a
60-second CaDiCaL time slice per cell.  It found 62 additional SAT witnesses,
149 cells timed out, and no cell returned UNSAT.  The deterministic exporter
generated 211 distinct CNF hashes while streaming temporary instances, so disk
use stayed bounded.  `unrestricted_sweep_summary.json` records exact dimensions,
versions, hashes, coverage, and resource limits.

## Files

- `pi4_witnesses.tsv` is the current 67-row certificate.
- `first_sweep_witnesses.tsv` preserves the original four-row certificate.
- `unrestricted_initial_witnesses.tsv` preserves the five-row starting point
  needed to reproduce the 211-cell unrestricted partition.
- `verify_pi4_witnesses.py` is a dependency-free definition-level verifier.
- `verify_pi4_witnesses.cpp` is a separately written exact verifier.
- `solve_pi4_mq.py` is the sparse XOR/CNF encoding.
- `export_pi4_cnf.py` deterministically expands one cell to pure DIMACS CNF,
  and `decode_pi4_cadical.py` converts a SAT model back to a state-word row.
- `sweep_pi4_cnf.py` streams independent CNF jobs with resumable witness and
  evidence checkpoints.
- `test_pi4_encoding.py` checks all 2,048 local product-coordinate truth-table
  cases and eight fixed-word end-to-end encoding/direct-arithmetic equivalences.
- `sweep_pi4_hints.py` partitions all 216 keys deterministically, uses atomic
  checkpoint replacement, rejects duplicate keys, and asserts exact scheduled
  coverage at completion.
- `first_sweep_summary.json` records the bounded search schedule, dependency
  hashes, and the necessary trust-boundary warning.
- `second_sweep_summary.json` records the complete support-orbit-seeded pass
  and its zero-new-witness outcome.
- `unrestricted_sweep_summary.json` records the 211-cell CNF pass and exact
  67-row coverage statistics.
- `verify.sh` reruns the Python exact verifier plus optimized and sanitized C++
  checks.  Run `test_pi4_encoding.py` inside the pinned environment to repeat
  the SAT-encoding regression.

## Reproduce the certificate checks

From the repository root:

```bash
python3 qlp42_q5_q37_pi4_census/verify_pi4_witnesses.py \
  qlp42_q5_q37_pi4_census/pi4_witnesses.tsv
bash qlp42_q5_q37_pi4_census/verify.sh
```

The sparse encoding and sweep use the pinned Python packages in
`requirements.txt`.  A complete first bounded sweep was run as follows on a
10-core host (nine worker processes were used):

```bash
python qlp42_q5_q37_pi4_census/sweep_pi4_hints.py \
  --input qlp42_q5_q37_pi3_witnesses/full_witnesses.tsv \
  --output pi4_witnesses.tsv --workers 9 --time-limit 1 --trials 4 \
  --free-cells 4 --free-cells 8 --free-cells 12 --free-cells 16 \
  --free-cells 20 --free-cells 24 --free-cells 30 \
  --free-cells 36 --free-cells 42 --batch 0
```

The unrestricted pass used CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`:

```bash
python qlp42_q5_q37_pi4_census/sweep_pi4_cnf.py \
  --input qlp42_q5_q37_pi4_census/unrestricted_initial_witnesses.tsv \
  --output pi4_witnesses.tsv \
  --evidence-output unrestricted_evidence.json \
  --cadical /absolute/path/to/cadical --workers 8 --time-limit 60
```

## Correctness and trust boundary

The mathematical certificate is only the state words and the exact verifier.
SAT models are decoded and then recomputed from definitions.  Parallel workers
do not share mutable solver state, output rows are keyed and sorted, writes use
`fsync` plus atomic replacement, and the final key-set assertion prevents a
hole in the 216-cell schedule.

PyCryptoSAT, CaDiCaL, and process scheduling are outside the theorem trust base
for the 67 positive results.  A timeout or a locally unsatisfiable neighborhood
does **not** prove cell unsatisfiability.  No fourth-layer exclusion is claimed;
such a claim would require an unrestricted exact encoding and an independently
checked proof trace.

## Literature context

The length-42 quaternary Legendre-pair case is identified as the smallest open
case in Kotsireas--Koutschan--Winterhof,
[Quaternary Legendre pairs II](https://arxiv.org/abs/2408.16318).  Definitions
and the decompression setting originate in Kotsireas--Winterhof,
[Quaternary Legendre Pairs](https://arxiv.org/abs/2212.10953); the general
construction landscape is complemented by Jedwab--Pender,
[Two constructions of quaternary Legendre pairs of even length](https://arxiv.org/abs/2408.08472).

The immediate dependency is the adjacent complete third-layer certificate,
published at immutable source commit
[`9c528277ccf06d4bc88d2c092c899140a6f2475f`](https://github.com/njallskarp/math_source_code_open/tree/9c528277ccf06d4bc88d2c092c899140a6f2475f/qlp42_q5_q37_pi3_witnesses).
