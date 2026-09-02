# Complete QLP-42 `(1+i)^3` orbit/case census

## Exact result

The earlier support-level result is strengthened to a complete classification
of the third Gaussian residue layer.  For each branch `q=5,37`, each of the 18
canonical parity-compatible support orbits, and each of the six canonical
exact-sum cases, there is a full assignment from the established 16-state local
table satisfying simultaneously:

- the branch energy count;
- all four required exact transformed Gaussian sums; and
- all twenty nonzero-shift autocorrelation equations modulo
  `(1+i)^3`.

Thus **all 216 canonical orbit/case cells survive**.  The `q=5` and `q=37`
branches each contribute 108 witnesses, and every case occurs 18 times in each
branch.  This proves that the complete third Gaussian residue layer has zero
pruning power even after the exact sums are imposed cell by cell.  It does not
construct a quaternary Legendre pair of length 42 and does not impose the next
Gaussian residue bit or the full integer autocorrelation equations.

[`full_witnesses.tsv`](full_witnesses.tsv) contains one exact witness for every
key `(q,orbit,case)`.  Its SHA-256 is
`283779dc06d031bf2a5f333dbb32c9cfa540313db8e4a82886caf7134fe8e8eb`.

## Verification

Run the solver-independent certificate check:

```bash
CXX=/opt/homebrew/bin/g++-16 ./verify_full_census.sh
```

[`verify_pi3_full_census.py`](verify_pi3_full_census.py) checks exact key
coverage and invokes the dependency-free definition-level Gaussian arithmetic
for every row.  [`verify_pi3_full_census.cpp`](verify_pi3_full_census.cpp) is a
separately written C++20 verifier using fixed arrays and direct integer-pair
arithmetic.  Release, AddressSanitizer, and UndefinedBehaviorSanitizer builds
produce exactly `full_expected_summary.txt`.

The theorem depends on the published witness rows and the two direct verifiers,
not on any SAT solver.  Solver outputs are accepted only after decoding to a
row and passing both definition-level checks.

## Complete and restartable sweep

[`sweep_pi3_hints.py`](sweep_pi3_hints.py) partitions the unresolved domain by
the exact `(q,orbit,case)` key, derives deterministic seeds from that key and a
batch identifier, tries an explicit sequence of free-cell neighborhoods, and
atomically checkpoints the canonical sorted manifest.  It asserts that every
scheduled key completes exactly once and propagates worker failures.

The stages recorded in [`full_census_manifest.json`](full_census_manifest.json)
grew the witness set from 83 to 215.  Parallelism changed only discovery order;
the output was sorted by key and verified serially after major checkpoints.
Timeouts were always recorded as unknown and never interpreted as UNSAT.

The last cell, `(q,orbit,case)=(5,0,0)`, was solved through a pure-CNF route.
[`export_pi3_cnf.py`](export_pi3_cnf.py) records the already validated sparse
MQ formula, expands every native XOR through explicit truth-table-checked
Tseitin parity gates, and writes deterministic DIMACS plus a variable map.
[`decode_pi3_cadical.py`](decode_pi3_cadical.py) decodes a SAT model back to
the 16-state table.  The final formula has 17,442 variables and 65,170 clauses,
with SHA-256
`5633d505ac9508683160fd7eaedcc8a74343e26b7b18c23686e01e838bde2b01`.
CaDiCaL commit `c60730422e758ef1cebe7aeddf2dda31c996bf04` returned SAT in 2.98
wall-seconds; the decoded row then passed the direct verifier.  A separate
known-SAT export `(5,0,3)`, SHA-256
`b7137b4fd7983ff115e6257b8cd0e783df94776eabac568b251e534d29f14dfa`,
was also decoded and checked to validate the export/decode path before the
final run.

The generated 1.1 MB DIMACS files, solver logs, temporary models, and build
products are intentionally omitted.  They are reproducible from the compact
source and are not required to check the 216-row theorem.

## Mathematical interpretation and next step

An independent exact dynamic program found that all 216 cells already satisfy
the exact-sum and energy layer before autocorrelation congruences are imposed.
The full witness census now shows that adding the third Gaussian residue bit
still eliminates none of them.  Consequently, completing more search at this
same layer cannot improve the frontier: the next useful computation is the
complete `(1+i)^4` census on these 216 witnessed cells, keeping the exact sums
throughout and recording the first layer at which any orbit/case cell is
actually removed.

Primary context remains Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, <https://arxiv.org/abs/1302.0571>;
Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
<https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two constructions of
quaternary Legendre pairs of even length*, <https://arxiv.org/abs/2408.08472>;
and Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>.
