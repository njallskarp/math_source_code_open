# Length-21 half-difference projection of the norm-32 shell

For each length-42 fourth-root sequence `X`, use the CRT coordinates

```text
x_j = X_(22*j mod 42),
y_j = X_(22*j+21 mod 42),
R_X(j) = x_j-y_j.
```

Every entry of `R_X` belongs to the nine-point Gaussian alphabet

```text
{0, 2, -2, 2i, -2i, 1+i, 1-i, -1+i, -1-i}.
```

The exact paired-lag identity

```text
PAF(X,s)-PAF(X,s+21) = (-1)^s PAF(R_X,s)
```

turns the representative norm-32 combined target into the necessary
length-21 equations

```text
PAF(R_A,0)+PAF(R_B,0) = 86,
PAF(R_A,s)+PAF(R_B,s) = -4  for s in {4,17},
PAF(R_A,s)+PAF(R_B,s) =  4  for s in {10,11},
PAF(R_A,s)+PAF(R_B,s) =  0  otherwise.
```

The sums of `R_A` and `R_B` are fixed by the six canonical order-two
compression representatives `(p,q,x,y)`:

```text
sum(R_A) = 2p+2qi,
sum(R_B) = (2x-1)+(2y-1)i.
```

Thus every realization of the shortest residual shell must first solve one of
six much smaller finite-domain autocorrelation problems.  A solution would be
only a necessary projection and would still need lifting to two length-42
fourth-root sequences.

`solve_norm32_half_difference_ortools.py` encodes this projection using exact
integer variables, table constraints for the alphabet, and multiplication
equalities for Gaussian autocorrelation.  Independent 120-second runs with
two workers returned `UNKNOWN` for all six compression cases.  A 300-second,
eight-worker case-3 run, seeded from the nearest deterministic full-sequence
heuristic state, also returned `UNKNOWN` after 1,239,958 conflicts and
2,824,528 branches.  These bounded outcomes prove neither satisfiability nor
unsatisfiability and are not used in a Discovery Net contribution.

Example:

```bash
uv run --with ortools==9.14.6206 \
  python solve_norm32_half_difference_ortools.py \
  --case 3 --seconds 300 --workers 8
```

The strongest next step is a proof-producing SAT encoding of this projection,
with cyclic symmetry breaking and the six sum cases split into independent
instances.

`HALF_DIFFERENCE_PARITY.md` proves an additional mod-4 defect-count
restriction.  `solve_norm32_half_difference_scaled_ortools.py` implements the
equivalent scaled ternary grid, the exact 43-coordinate support equation,
full independent cyclic lex-leader constraints, finite ternary product
tables, and that mod-4 restriction.  A 60-second, eight-worker case-0 run
remained `UNKNOWN` after 19,490 conflicts and 469,931 branches; bounded solver
outcomes are not mathematical evidence.

`search_norm32_half_difference_scaled.cpp` is a deterministic
simulated-annealing companion that preserves all sums, the support count, and
the mod-4 restriction.  Its near misses are also not evidence; it prints an
exact witness only after direct verification.
