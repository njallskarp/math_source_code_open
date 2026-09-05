# An exact aggregate pseudomodel for the R(5,5;43) M=214 branch

## Result

The currently committed scalar/profile, exceptional-signature, capacity, and
common-neighborhood union-cut relaxation does **not** exclude the hard-branch
cross total `M=214`.  `PSEUDOMODEL.json` gives an exact integral count witness.
It uses the Paley graph on 13 exceptional degree-20 vertices and 30 explicit
exceptional-neighborhood signatures for the degree-21 vertices.  All 4,043
rooted union cuts and every exact marginal equation pass.

This is deliberately a limitation theorem, not a Ramsey graph construction.
The certificate also gives a simple 43-vertex degree/signature realization and
scalar local-edge variables, but those scalar variables are not the actual
induced-neighborhood edge counts of that realization.  The checker exhibits a
monochromatic `K5` and reports the profile mismatch.  Thus a closing argument
must couple central-cell edges to the local triangle counts (or use an equally
strong non-scalar invariant); summing the existing reanchored inequalities is
insufficient.

## Exact reduction at M=214

Let `E` be the 13 vertices of degree 20 and put

`a(v) = |N_R(v) intersect E|`.

The committed deficiency identities give red local counts 93 at `E` and 100
at all 30 degree-21 vertices.  The degree-neighborhood identity then gives
`a(v) >= 6` for every vertex.  Double counting incidences at `E` gives

`sum_v a(v) = sum_{e in E} d(e) = 13*20 = 260 = 43*6 + 2`.

If `F=G[E]`, this forces `39 <= e(F) <= 40`.  The witness chooses the
6-regular Paley core, so `e(F)=39`; every exceptional vertex has `a=6`, while
28 central signatures have size six and two have size seven.  Each exceptional
vertex lies in exactly 14 signatures.  Consequently the global degrees are
`20^13 21^30`, the class-count variable is `q_20,20=39`, the red and blue
triangle scalars are 1403 and 1463, and exactly 28 degree-21 vertices are
doubly exact.

The 30 masks are subsets of `{0,...,12}`, encoded by bit `i` for exceptional
vertex `i`.  The checker reconstructs rather than imports:

- signature admissibility and the binomial capacity bound;
- the parity-improved Ramsey upper table through `(5,5)`;
- every disjoint red-clique/blue-clique rooted union cut;
- all degree, deficiency, triangle, class-incidence, and reanchoring totals;
- the M=214 exact-anchor backbone bounds and deletion-connectivity checks.

The auxiliary central graph is the circulant on `Z/30Z` with red cyclic
distances `1,...,7,15`, with edge `{28,29}` deleted.  Its first 28 vertices are
the size-six (doubly exact) pseudotypes.  Their induced red/blue backbones have
minimum degrees 13/12, diameters 2/3, and vertex connectivities at least 4/2.

## Reproduce

Requires CPython 3.11 or newer and only the standard library.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_pseudomodel.py
PYTHONDONTWRITEBYTECODE=1 python3 test_verify.py
shasum -a 256 PSEUDOMODEL.json verify_pseudomodel.py test_verify.py README.md EXPECTED_OUTPUT.txt
```

The first command exhaustively checks 3,432 admissible size-six/seven
signatures and 4,043 rooted union inequalities.  Expected output is committed
in `EXPECTED_OUTPUT.txt`; hashes are in `SHA256SUMS`.

The certificate was discovered with SciPy 1.15.3 / HiGHS 1.8.0 as a zero-
objective MILP with 3,432 integer variables and 4,043 union rows.  That solver
run is discovery only.  The verifier uses no solver, floating point, NumPy, or
external data.

## Provenance and literature boundary

The graph reductions audited here are the committed Discovery Net chain at
heights 2099, 2105, 2115, 2119, 2123, 2127, 2135, 2137, 2141, 2145, 2149,
and the later degree-neighborhood/signature refinements through height 2497.
Height 2505 independently packages the full 903-edge branch as an OPB formula;
this directory instead determines the limitation of the much smaller aggregate
relaxation and does not duplicate that formula.

Primary-source status: Angeltveit and McKay prove `R(5,5) <= 46` and report the
still-best lower bound 43; their proof combines linear programming with large
case checks.  McKay and Radziszowski prove `R(4,5)=25`, the source of the basic
degree interval.  McKay's public Ramsey-data page states that known
`R(5,5,42)` graphs do not settle orders 43--47 and provides the extremal
`R(4,5)` catalogues used upstream.

- https://arxiv.org/abs/2409.15709
- https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf
- https://users.cecs.anu.edu.au/~bdm/data/ramsey.html

## Trust boundary

The exact certificate proves feasibility only for the explicitly stated
aggregate relaxation.  It inherits the committed graph-to-relaxation proofs
and the `R(4,5)` extremal inputs.  Its direct computation trusts CPython integer
arithmetic, the small checker, ordinary hardware, and SHA-256 for provenance.
It does not trust the exploratory MILP solver.  Most importantly, it does not
couple the scalar `t_R,t_B` values to the actual edges within and between
central signature cells; that omitted compatibility is precisely the witnessed
limitation and the next mathematical boundary.
