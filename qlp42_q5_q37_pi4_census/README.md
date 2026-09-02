# QLP-42 fourth Gaussian-layer witnesses

This directory gives exact, independently checkable witnesses showing that at
least four of the 216 exact-sum cells on the surviving QLP-42 `q=5/q=37`
frontier pass the fourth Gaussian residue layer.

Let `pi = 1+i`.  For each component `s,h` and each shift `1,...,10`, the
required residual is a Gaussian integer.  Since `pi^4=-4`, the fourth-layer
condition is exactly that both integer coordinates of every residual are zero
modulo 4.  The four certified cells are

| q | support orbit | exact-sum case |
|---:|---:|---:|
| 5 | 0 | 1 |
| 5 | 3 | 1 |
| 5 | 10 | 0 |
| 37 | 4 | 4 |

Thus neither binary frontier branch is eliminated at this layer.  This is a
lower-bound result, not a complete fourth-layer census: the bounded first sweep
visited all 216 cells exactly once but did not prove anything about the other
212 cells.

## Files

- `pi4_witnesses.tsv` is the four-row certificate.
- `verify_pi4_witnesses.py` is a dependency-free definition-level verifier.
- `verify_pi4_witnesses.cpp` is a separately written exact verifier.
- `solve_pi4_mq.py` is the sparse XOR/CNF encoding.
- `test_pi4_encoding.py` checks all 2,048 local product-coordinate truth-table
  cases and eight fixed-word end-to-end encoding/direct-arithmetic equivalences.
- `sweep_pi4_hints.py` partitions all 216 keys deterministically, uses atomic
  checkpoint replacement, rejects duplicate keys, and asserts exact scheduled
  coverage at completion.
- `first_sweep_summary.json` records the bounded search schedule, dependency
  hashes, and the necessary trust-boundary warning.
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

## Correctness and trust boundary

The mathematical certificate is only the state words and the exact verifier.
SAT models are decoded and then recomputed from definitions.  Parallel workers
do not share mutable solver state, output rows are keyed and sorted, writes use
`fsync` plus atomic replacement, and the final key-set assertion prevents a
hole in the 216-cell schedule.

PyCryptoSAT and process scheduling are outside the theorem's trust base for
the four positive results.  A timeout or a locally unsatisfiable neighborhood
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
