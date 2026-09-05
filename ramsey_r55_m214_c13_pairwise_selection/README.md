# Pairwise core compatibility still admits an exact aggregate c=13 selection

## Claim and scope

This directory gives an exact 28-row witness for the complete pairwise
core-interface relaxation of the `M=214,c=13` two-anchor cell.  It repairs both
pairwise defects in the aggregate witness at Discovery Net height 2869: no two
rows in either seven-vertex off-diagonal anchor cell form a no-color pair, and
the required red-edge count of every one of the six cell-pair categories lies
between its forced-red and red-allowed capacities.

Consequently, adding every one- and two-outside-vertex monochromatic-`K5`
condition to the height-2869 aggregate equations does **not** eliminate this
cell.  This is a counterexample to the sufficiency of that relaxation.  It is
not a 43-vertex Ramsey graph and not an exclusion of the `c=13` branch:
individual outside degrees, individual outside `E`-incidences, and
monochromatic five-sets containing at least three outside vertices are not
claimed.  Those are the next missing interface.

## Exact quotient and pair rules

Normalize the red anchor edge as `uv`.  Its thirteen common red neighbors form
the cyclic `(3,5;13)` graph `H` on `Z/13Z`, where

```text
i ~ j  iff  i-j is in {1,5,8,12} modulo 13.
```

The remaining vertices split into `A,B,O` of sizes `7,7,14`: vertices in `A`
are red only to `u`, vertices in `B` red only to `v`, and vertices in `O` blue
to both anchors.  The 13-bit mask `S_x` records the red neighbors of outside
vertex `x` in `H`.  Every row must hit all 39 independent four-sets of `H`.
There are exactly 3,459 such transversal masks.

For each outside pair `x,y`:

1. blue `xy` is forbidden if `H \\ (S_x union S_y)` contains an independent
   triple;
2. when `x,y` lie together in `A` or together in `B`, red `xy` is forbidden
   if `H[S_x intersection S_y]` contains a red edge.

A same-cell pair is inadmissible if both colors are forbidden.  These rules
are exactly the monochromatic-five-set constraints that use two outside
vertices and otherwise only core/anchor vertices.

## The compact selection

`certificate.json` orders its 28 masks by `A[0..6], B[0..6], O[0..13]`.  It
uses the `k=0` marking: the first six rows of `A`, the first six rows of `B`,
and the first row of `O` are marked, and `A0` is the exceptional marked pivot.
Every core column has total 15 and marked total 6.  The cell incidences and
the resulting red-edge targets are

```text
I_A=50, I_B=48, I_O=97,
m_A=11, m_B=13, m_O=47,
m_AB=10, m_AO=52, m_BO=50.
```

Within `A` and `B`, respectively, 10 and 8 pairs forbid red, no pair forbids
blue, and hence exactly 11 and 13 pairs allow red.  Thus both internal targets
are sharp.  In `O,AB,AO,BO`, respectively, `5,10,17,21` pairs force red; all
red-edge targets meet those lower capacities, with the `AB` target again
sharp.  The checker constructs an explicit outside edge coloring: take every
forced-red pair and then the lexicographically first additional red-allowed
pairs until each target is reached.  The resulting outside graph has 183 red
edges.

Direct enumeration of all five-subsets confirms that the constructed partial
lift has no monochromatic `K5` containing zero, one, or two outside vertices.
The checker also verifies all 13 transversal, total-column, marked-column,
anchor-triangle, cell degree-sum, and aggregate edge-interval equations.

## Discovery method

`search_selection.cpp` starts from the exact height-2869 aggregate rows.
Every search move redistributes each bit among two or three rows with the same
mark status while preserving that bit's multiplicity.  Thus all total and
marked column equations remain exact at every step; candidates that cease to
be transversals are rejected.  A fixed-seed min-conflicts/annealing objective
then removes no-color pairs and closes the six edge-capacity intervals.  With
GNU g++ 16.2.0, seed `48001` first reaches the included witness at step
8,788,818.  The search is discovery code, not part of the proof trust boundary.

## Reproduction

The recorded environment used CPython 3.12.12 and GNU g++ 16.2.0.  From this
directory run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 check_certificate.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O check_certificate.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_certificate.py \
  | cmp - EXPECTED_TEST_OUTPUT.txt
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  independent_check.cpp -o /tmp/r55_pairwise_selection_check
/tmp/r55_pairwise_selection_check | cmp - EXPECTED_INDEPENDENT.txt
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  search_selection.cpp -o /tmp/r55_pairwise_selection_search
/tmp/r55_pairwise_selection_search 48001 9000000 2>/dev/null \
  | cmp - EXPECTED_SEARCH.txt
shasum -a 256 -c SHA256SUMS
```

The Python checker reads the compact certificate and builds its deterministic
edge lift.  The independent C++20 checker embeds the 28 rows, reconstructs the
cyclic core and all masks with fixed-width bit operations and nested loops,
independently rebuilds the edge lift, and rechecks the five-sets.  It shares no
certificate parser or Python combination machinery.

## Trust boundary

Trusted are the normalized `c=13` anchor quotient and aggregate equations from
the accepted dependencies; the displayed cyclic core definition; the compact
certificate; the short Python and C++20 checkers; language semantics; ordinary
hardware; and SHA-256 collision resistance.  The claim does not trust the
stochastic search, a SAT/MILP solver, a raw log, a generated model, a database,
or a private graph state.  The use of the cyclic representative inherits the
catalog uniqueness trust boundary already stated at height 2823.
