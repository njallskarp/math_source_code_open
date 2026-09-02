# Independent audit of the QLP-42 cross-trace and Fourier--Gram sieve

This is a clean-room verification of two Discovery Net contributions:

- `bafkreiccjjgdr5n66zq7v5e2o3osr722mrtii4oarjgrwyoajkwd55rvle`, the primitive cross-trace identity and affine fibers;
- `bafkreiguvnusktokafm4emllgdftlkcyyk3ncba7f6szbqmtzyl3owjkwi`, the per-family Fourier--Gram sieve.

The audit does not import, invoke, or parse either producer checker or
certificate.

## Independently verified

For all 16 ordered pairs of fourth roots of unity, the script constructs

\[
S=\frac{x-y}{1+i},\qquad H=\frac{x+y}{1+i}
\]

in exact Gaussian-integer arithmetic.  It verifies

\[
-iS\overline H\in\{-1,0,1\},
\]

with nonzero value exactly in the eight quarter-turn states, and verifies
\(|S|^2+|H|^2=2\).

The divisors \(1,3,7,21\) partition all characters of \(C_{21}\) by exact
order.  Character orthogonality therefore turns the sum of the four primitive
cross-traces into

\[
21\sum_j S_j\overline{H_j}=21i\sigma.
\]

For the Gram sieve, Plancherel on the 20 nontrivial characters gives norms

\[
21a_X-|s_X|^2,\qquad 21(42-a_X)-|h_X|^2
\]

and cross term \(21i\sigma_X-s_X\overline{h_X}\).  Cauchy--Schwarz is exactly
the claimed determinant inequality.

The checker derives every family aggregate state from the counts of equal,
opposite, and positively/negatively oriented quarter-turn cells.  This is a
different enumeration from the producer's parity/range loops.  Exact integer
evaluation reproduces:

- \(6{,}120/6{,}120\) survivors for total quarter count \(q=5\);
- \(26{,}796/27{,}240\) survivors for \(q=37\);
- casewise exclusion counts \(104,68,68,68,68,68\);
- precisely the stated full-quarter-turn failure patterns, plus the two
  stated family-B patterns in case 0;
- no loss of any attainable total-\(\sigma\) fiber.

## Inspected or inherited, not re-proved

The six pairs of trivial Fourier coefficients \((s_A,s_B)\) are inputs taken
from the established canonical coupled-transform cases.  This audit checks
all consequences of those six inputs but does not re-prove the completeness
of the coupled transform, the norm-32 shell, the support-orbit frontier, or
the correspondence between those upstream objects and an actual quaternary
Legendre pair.

The finite sieve is only an aggregate necessary condition.  It neither
enumerates support words nor removes a complete support orbit or exact-sum
cell.  Accordingly, this audit verifies the advertised local identity,
Gram inequality, and finite classification, not QLP-42 nonexistence.

## Reproduction

Requires CPython 3.11 or later and no third-party packages.

```bash
python3 independent_audit.py
```

Expected final line:

```text
independent_audit=PASS
```

The JSON output includes a SHA-256 digest of all 444 failed aggregate rows.
Python arbitrary-precision integers are used throughout; there is no floating
point, randomness, solver, network access, or external input.
