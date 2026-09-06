# Global pair-column hull cuts for the \(M=214\) Ramsey formulation

## Result and scope

This directory gives a global all-root strengthening of the complete
\(M=214\) pseudo-Boolean formulation for a hypothetical \((5,5;43)\)-Ramsey
graph. It consumes the exact missed-pair variables introduced by the preceding
height-3274 lift.

For a selected red anchor \(uv\), its common red core \(H\), an exterior set
\(X\), and \(h\in H\), put

\[
a_h=|N_R(h)\cap H|,
\qquad
M_h=\sum_{P\in\binom X2}m_{P,h}.
\]

The exact degree equation determines the number \(b_h\) of blue exterior
neighbors from \(a_h\). Double counting gives

\[
M_h=\binom{b_h}{2}.
\]

The construction appends the complete two-dimensional convex hull of these
integer points for every core column of every one of the 389 roots. It adds
13,078 rows and no variables.

An exact rational certificate proves that these rows strictly strengthen the
LP relaxation of the *entire* height-3274 formula. The point satisfies every
old row, including all 962,598 five-set constraints and all 43 local-triangle
equations, but violates exactly 13 new hull rows by 72 each.

This is an equisatisfiable formulation strengthening and a strict LP
separation result. It is not a colored graph, SAT/UNSAT result, solved root,
Ramsey-number bound, or claim about solver runtime.

## Column-hull theorem

The red graph on \(H\) is triangle-free and has independence number at most
four. For every \(h\in H\), the equality \(R(3,4)=9\) gives

\[
c-9\leq a_h\leq4.
\]

If \(n=41-c\) and \(d_h\in\{20,21\}\) is the prescribed total red degree,
then

\[
b_h=n-d_h+2+a_h.
\]

Consequently the possible \(b_h\)-values are

\[
\begin{array}{c|c}
d_h&b_h\\ \hline
20&14,15,\ldots,27-c\\
21&13,14,\ldots,26-c.
\end{array}
\]

For integers \(L\leq b\leq U\), the convex hull of
\((b,\binom b2)\) has lower facets

\[
M\geq tb-\binom{t+1}{2},
\qquad t=L,L+1,\ldots,U-1,
\]

and upper facet

\[
2M\leq(L+U-1)b-LU.
\]

[`PROOF.md`](PROOF.md) derives the bounds, the exact hull, the guarded OPB
rows, equisatisfiability, and the strict separation certificate.

## Exact generated identity

The row counts attached to one root of core order \(9,10,11,12,13\) are

```text
45, 40, 33, 24, 26.
```

The complete strengthened formula has:

```text
variables          98,758
constraints     2,983,003
equalities              87
lines           2,983,004
bytes          511,537,255
SHA-256 9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609
```

The generated 59,694,974-byte suffix has 13,078 rows and SHA-256
`921a93d6126a66bbe73164cfb4180bab72af9e9f670347d3da7ee1977c4b20d9`.
Generated OPB, LP, and solver files are operational state and are deliberately
excluded from version control.

## Strict full-LP certificate

The rational point selects root 48,
\((\mathtt{E8},13,0,\mathtt A)\), whose core is the cyclic
\((3,5;13)\) graph. Its compact evidence consists of:

- `edge_parameters.tsv`: 20 exterior-edge orbit values;
- `triangle_orbits.tsv`: 171 triangle classes with exact rational values;
- exact McCormick-lower definitions of the 10,612 \(m\)-variables and 74,513
  \(q\)-variables, reconstructed by both checkers.

The point satisfies:

```text
five-set rows checked                    962,598
five-set red-sum range                       1..9
triangle conjunctions                     12,341
selector rows                              69,732
unary footprint rows                       11,672
projected pair rows                        74,958
local pair-cell rows                      508,986
```

For every active core column, the old McCormick relaxation permits \(M_h=6\).
The new slope-13 hull row requires \(M_h\geq78\), giving 13 violations of
slack \(-72\).

## Compact reproduction

The recorded environment used CPython 3.12.12 and GNU g++ 16.2.0. From this
directory:

```sh
set -o pipefail
python3 -B build.py --certificate /tmp/pair_column_roots.tsv \
  --suffix /tmp/pair_column_hull.opbpart | cmp - EXPECTED_RESULT.json
cmp /tmp/pair_column_roots.tsv roots.tsv
python3 -B test_build.py | cmp - EXPECTED_TEST_OUTPUT.txt
python3 -B verify_fractional.py | cmp - EXPECTED_VERIFY_OUTPUT.txt
g++-16 -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -Werror independent_check.cpp -o /tmp/pair_column_check
/tmp/pair_column_check /tmp/pair_column_roots.tsv \
  /tmp/pair_column_hull.opbpart edge_parameters.tsv triangle_orbits.tsv \
  13078 | cmp - EXPECTED_INDEPENDENT.txt
shasum -a 256 -c SHA256SUMS
```

On Linux or another installation where the executable is named `g++`, replace
`g++-16` by `g++`.

For sanitizer replay:

```sh
g++-16 -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -Werror -fsanitize=address,undefined -fno-omit-frame-pointer \
  independent_check.cpp -o /tmp/pair_column_check_san
/tmp/pair_column_check_san /tmp/pair_column_roots.tsv \
  /tmp/pair_column_hull.opbpart edge_parameters.tsv triangle_orbits.tsv 13078
```

## Re-deriving the fractional certificate

SoPlex is discovery machinery only. Version 8.0.3 was used in exact-rational
read and solve modes:

```sh
python3 -B derive_edge_parameters.py --lp /tmp/pair_column_edges.lp
soplex --readmode=1 --solvemode=2 --int:checkmode=2 \
  --int:ratfac_minstalls=0 --bool:ratfacjump=true \
  --real:feastol=1e-30 --real:opttol=1e-30 --real:fpfeastol=1e-30 \
  -s0 -g0 -v3 -X=/tmp/pair_column_edges.sol /tmp/pair_column_edges.lp
python3 -B derive_edge_parameters.py \
  --solution /tmp/pair_column_edges.sol --output /tmp/edge_parameters.tsv
cmp /tmp/edge_parameters.tsv edge_parameters.tsv

python3 -B derive_fractional_certificate.py --lp /tmp/pair_column_orbits.lp
soplex --readmode=1 --solvemode=2 --int:checkmode=2 \
  --int:ratfac_minstalls=0 --bool:ratfacjump=true \
  --real:feastol=1e-30 --real:opttol=1e-30 --real:fpfeastol=1e-30 \
  -s0 -g0 -v3 -X=/tmp/pair_column_orbits.sol /tmp/pair_column_orbits.lp
python3 -B derive_fractional_certificate.py \
  --solution /tmp/pair_column_orbits.sol --output /tmp/triangle_orbits.tsv
cmp /tmp/triangle_orbits.tsv triangle_orbits.tsv
```

Neither solver output is trusted: both published rational tables are verified
directly against every claimed row.

## Full formula replay

After regenerating the pinned height-3274 formula as
`/tmp/m214_height3274.opb`, run:

```sh
python3 -B build.py --certificate /tmp/pair_column_roots.tsv \
  --suffix /tmp/pair_column_hull.opbpart \
  --prior-opb /tmp/m214_height3274.opb \
  --output-opb /tmp/m214_pair_column_hull.opb \
  | cmp - EXPECTED_FULL_RESULT.json
/tmp/pair_column_check /tmp/pair_column_roots.tsv \
  /tmp/pair_column_hull.opbpart edge_parameters.tsv triangle_orbits.tsv \
  13078 /tmp/m214_height3274.opb /tmp/m214_pair_column_hull.opb \
  | cmp - EXPECTED_INDEPENDENT.txt
shasum -a 256 /tmp/m214_pair_column_hull.opb
```

The public predecessor is the [height-3274 exact pair-cell
lift](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_cell_c5_lift).

## Validation and trust boundary

- Python and independently implemented C++20 enumerate all 389 roots, rebuild
  the shared missed-variable support, and compare every one of the 13,078
  generated rows byte for byte.
- Both checkers reconstruct the rational edge, triangle, \(m\), and \(q\)
  values and verify the strict full-LP separation exactly.
- Normal and optimized CPython generation are compared byte for byte.
- Strict warnings, AddressSanitizer, and UndefinedBehaviorSanitizer cover the
  C++ checker; malformed compact inputs are rejected.
- The C++ checker also compares every prior and appended row in the full
  511,537,255-byte formula stream.

The core-degree lower bound uses Greenwood and Gleason's classical equality
\(R(3,4)=9\): R. E. Greenwood and A. M. Gleason,
[Combinatorial Relations and Chromatic Graphs](https://doi.org/10.4153/CJM-1955-001-4),
*Canadian Journal of Mathematics* 7 (1955), 1--7. The column-hull calculation
is proved directly here; no priority claim is made for the abstract
cardinality-constrained Boolean-quadric polytope.

Trusted are the accepted height-3148 complete root cover, independently
accepted height-3160 selector semantics, the pinned height-3274 formula and
variable mapping, the displayed elementary proof, exact language semantics,
ordinary hardware, and SHA-256. The implementations are author-run
cross-checks rather than external review or formal proof. SoPlex, its logs,
generated LP/OPB files, raw solver state, binaries, databases, caches, and
credentials are outside the proof evidence and are not published.

## Stopping condition and next step

This completes the scalar pair-column projection and proves that it is a
strict global LP strengthening. Additional scalar column facets would be
duplicate work: \((5)\)--\((6)\) are the complete hull.

The complete \(M=214\) branch remains undecided. The next falsifiable step
must couple two or more core columns or aggregate the \(q_{P,ij}\) variables
over core edges, producing either a new strict full-LP separator or a compact
full-LP survivor for that higher-order projection. A solver timeout, another
local pair inequality, or a redundant column facet is not progress.
