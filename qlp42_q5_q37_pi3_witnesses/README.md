# Full support-orbit survival at the QLP-42 `(1+i)^3` layer

## Exact intermediary theorem

Start with the 18 `q=5` and 18 `q=37` support orbits retained by exact-sum
parity in the predecessor binary-shadow frontier.  Every one of these 36
support orbits has a full assignment from the established 16-state local
table that simultaneously satisfies:

- the branch energy count (19 opposite cells for `q=5`, 3 for `q=37`);
- all four exact transformed Gaussian sums in at least one of the six
  canonical `(p,q,x,y)` cases; and
- all twenty nonzero-shift autocorrelation equations modulo
  `pi^3=(1+i)^3`.

Therefore the complete third Gaussian residue layer does **not** exclude any
parity-compatible binary-shadow support orbit in either branch.  This is an
existence theorem, proved by the 83 explicit rows in
[`witnesses.tsv`](witnesses.tsv).  It is not a complete classification of the
216 orbit/case cells: 31 `q=5` cells and 52 `q=37` cells are witnessed, while
the other 133 cells remain unclassified rather than being declared
impossible.

The witnessed case distributions are:

| branch | case 0 | case 1 | case 2 | case 3 | case 4 | case 5 | total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `q=5` | 3 | 6 | 5 | 3 | 8 | 6 | 31 |
| `q=37` | 6 | 10 | 8 | 11 | 11 | 6 | 52 |

Every support-orbit identifier `0,...,17` occurs in each branch.

## Sparse third-order derivation

Write the two original roots at a local cell as

```text
X = i^(2*x1+x0),   Y = i^(2*y1+y0).
```

For a fixed quarter-support bit `u`, the local kind condition is exactly
`y0=x0+u` in `F_2`; hence every allowed local state is represented by the
three free bits `(x0,x1,y1)`.  Equal/opposite status at a nonquarter cell is
`x1+y1`.

For a Gaussian product `z`, use its two coordinates modulo four

```text
L_plus(z)  = Re(z)+Im(z),
L_minus(z) = Im(z)-Re(z).
```

Divisibility by `pi^3` is equivalent to both coordinates vanishing modulo
four after subtracting the target.  For every pair of endpoint support bits,
component (`S` or `H`), and coordinate (`L_plus` or `L_minus`), direct
Möbius transformation of the 64-entry truth table shows:

- the low bit is one exactly for a quarter/quarter endpoint pair and is
  otherwise zero; its total is precisely the already-certified binary-shadow
  equation;
- the high bit is a quadratic algebraic-normal form in the six endpoint bits,
  with at most 13 monomials.

Thus the new residue condition is a sparse exact quadratic system over
`F_2`, supplemented by exact six-bit signed adders for the four sums and the
energy count.  [`solve_pi3_mq.py`](solve_pi3_mq.py) constructs this CNF/XOR
system.  CryptoMiniSat was used only to discover assignments; the theorem is
certified independently by direct arithmetic on the published witnesses.

## Verification

[`verify_pi3_witnesses.py`](verify_pi3_witnesses.py) uses only the Python
standard library.  It reconstructs all 16 states from the four Gaussian
roots, checks support membership and energy, recomputes the four exact sums,
and directly recomputes all 20 Gaussian PAF residuals for every row before
dividing each residual by `1+i` three times.

[`verify_pi3_witnesses.cpp`](verify_pi3_witnesses.cpp) is a separately written
C++20 definition-level verifier using fixed arrays and direct integer-pair
Gaussian arithmetic.  Release and full AddressSanitizer/UndefinedBehavior-
Sanitizer executions agree exactly.  All intermediate PAF coordinates have
absolute value below 100, so fixed-width arithmetic is far inside its bounds.

Run the complete certificate check without any solver dependency:

```bash
CXX=/opt/homebrew/bin/g++-16 ./verify_all.sh
```

The manifest SHA-256 is
`e3ddcfd764e3bd738209ff88fc52645d6593973e61b7c58a2832268833541510`.

## Generator record

The public directory retains all source used during the search:

- [`search_pi3_witness.cpp`](search_pi3_witness.cpp) is a deterministic,
  restartable simulated-annealing generator.  Its output is never trusted
  without the exact verifiers.
- [`sweep_pi3_local.py`](sweep_pi3_local.py) partitions all 216 jobs and
  records deterministic restart seeds without gaps.
- [`solve_pi3_mq.py`](solve_pi3_mq.py) is the production sparse MQ/SAT
  formulation, and [`sweep_pi3_mq.py`](sweep_pi3_mq.py) runs bounded parallel
  partitions and merges rows by the exact `(q,orbit,case)` identifier.
- [`generate_pi3_witnesses.py`](generate_pi3_witnesses.py),
  [`solve_pi3_cryptominisat.py`](solve_pi3_cryptominisat.py), and
  [`solve_pi3_z3.py`](solve_pi3_z3.py) are slower exploratory exact encodings
  retained for auditability.  Timeout/unknown results from these programs are
  not mathematical claims.

The solver environment used the exact versions in
[`requirements.txt`](requirements.txt).  Parallelism affected only which
witness was found first.  Coverage is keyed and sorted before publication,
worker failures are surfaced, and every retained row is rechecked serially.

## Scope, sources, and next step

This result neither constructs nor excludes a quaternary Legendre pair of
length 42.  It establishes only the third-order Gaussian congruences and the
four exact sums, not the next residue layer or the full integer
autocorrelations.  Its trust boundary is the established coupled transform
and 16-state table, the predecessor frontier manifest (checked SHA-256
`f1dff75420fb37a2454767a7177367045e100ab07a07a11addd5e5551407d89e`),
the elementary Gaussian arithmetic, the published witness manifest, two
verifiers, toolchains, operating system, and hardware.  Solver correctness is
not in the theorem's trust boundary because each SAT output is a witness.

Primary context is Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, <https://arxiv.org/abs/1302.0571>;
Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
<https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two constructions of
quaternary Legendre pairs of even length*, <https://arxiv.org/abs/2408.08472>;
and Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>.  A targeted primary-source and committed-
graph search found no matching `q=5,37` third-order support-orbit census.
Apparent novelty is relative to those searches, not a historical-priority
claim.

The strongest next step is to classify the remaining 133 orbit/case cells
with completed SAT/UNSAT certificates, then advance the surviving cells to
the `pi^4` layer with the exact sums imposed throughout.
