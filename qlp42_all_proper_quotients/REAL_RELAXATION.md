# Real Gray-component relaxation for the norm-32 shell

For a quaternary symbol encoded by two bits `u,v`, put

```text
a = (1+i)/2 * (-1)^u + (1-i)/2 * (-1)^v.
```

Writing `C_u(s)` for the periodic binary-sign autocorrelation gives the exact
identity

```text
Re PAF(a,s) = (C_u(s) + C_v(s))/2.
```

The balance normalization for a QLP-42 candidate makes the four component
weights `(21,21,20,21)`.  For the representative shortest residual

```text
e_s = -2 at s in {4,11,31,38},
e_s =  2 at s in {10,17,25,32},
e_s =  0 otherwise,
```

its real equations are therefore equivalent to requiring the total number of
cyclic bit differences over the four components to equal `86-e_s`.  In terms
of intersections of one-sets with their shifts, the corresponding totals are
39, 40, and 41 when `e_s` is -2, 0, and 2, respectively.

This is a necessary relaxation only: the imaginary cross-correlation equations
that couple `u` and `v` have been omitted.  A proof of unsatisfiability here
would exclude the entire norm-32 shell; a satisfying assignment would merely
seed the remaining coupled problem.

## Reproducibility and current status

The deterministic heuristic supports a `real-only` mode:

```bash
c++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  search_norm32_residual.cpp -o search_norm32_residual
./search_norm32_residual 20 1000000 real-only
```

It reached squared real residual 32, but not zero.  The closest state was

```text
A=j1j-ij--ij1-1i1jji1j1--1--iii111jiiiij-jj-
B=1j--iij1-iiiji-1i1jj11-i11-j-jji11-1ji--1-
```

Its four nonzero real discrepancies on shifts 1 through 21 are `+2` at 3 and
16 and `-2` at 11 and 19.  The exact PySAT model and the independently written
OR-Tools CP-SAT model encode the same relaxation.  A 300-second OR-Tools run
with 8 workers returned `UNKNOWN` after 40,206 conflicts and 260,876 branches.
The initial CaDiCaL run also remained unresolved in its allotted research
window.  These outcomes are not evidence for satisfiability or
unsatisfiability and are not used in a graph contribution.

Example commands:

```bash
uv run --with python-sat python solve_norm32_real_pysat.py \
  --solver cadical195 --encoding kmtotalizer
uv run --with ortools==9.14.6206 python solve_norm32_real_ortools.py \
  --seconds 300 --workers 8
```

The algebraic reduction and any decoded witness are checked using exact
integer arithmetic.  Solver `UNKNOWN` and heuristic non-discovery remain
outside the theorem trust boundary.
