# Canonical width-four Lucas Schur positivity

This directory contains the complete unpacked source for the canonical
`b=4` slice of the Lucas--Bergeron--Vessenes conjecture. With
`F_(n+1)=e1 F_n+e2 F_(n-1)`, all nontrivial canonical cases have
`a=1,2,3`.

- [`a2/`](a2/) proves `{2c+2 choose 2}_F-{c+4 choose 4}_F` is
  Schur-positive for every `c>=4`, by an exact six-step KOH recurrence and
  adjacent-layer pairing.
- [`a3/`](a3/) proves `{3k+4 choose 4}_F-{4k+3 choose 3}_F` is
  Schur-positive for every `k>=2`, and contains the exhaustive case split
  completing the width-four slice. It also displays the elementary-positive
  even-shift KOH expansion for `a=1`.

The principal graph artifacts are the `(2,4)` theorem
`bafkreih237ln667nxhs2twfjttf6q6np4lqktllvtbflhibr3erwkqouzy`
at height 1491 and the complete `b=4` theorem
`bafkreifu7ctg6ycgzswu3vdfnxphov7opvyr5gyatdzadzhkibgkzew6ta`
at height 1515. Corrected independent reviews accepted these results at
heights 1513 and 1525.

## Reproduction

Run from the repository root under CPython 3.12.12:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b4/a2/verify_recurrence.py --max-c 60
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b4/a2/verify_schur_kernel.py --max-c 300 --explicit-max-c 50
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b4/a2/verify_pairing.py --max-c 300
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b4/a3/verify_pairing.py --max-k 100
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b4/a3/verify_sparse.py --max-k 40
(cd lucas_schur_b4 && sha256sum -c SHA256SUMS)
```

Expected: all five programs exit zero. Their first lines report exact
`Z[e1,e2]` recurrence verification, independent q-Pascal/Delannoy/Pieri
verification, adjacent-layer pairing verification, exact q-Pascal/Schur-layer
verification, and independent sparse `Z[e1,e2]` verification.

## Trust boundary

The universal claims rest on the written KOH identities, quasipolynomial
bounds, and Schur-layer pairing arguments in the two subdirectory READMEs.
The programs use arbitrary-precision integer arithmetic and audit formulas,
base cases, endpoint regimes, and coefficient extraction. There is no
floating point, randomness, solver, modular reconstruction, or external proof
data.
