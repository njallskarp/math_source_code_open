# The individual pairwise c=13 interface still admits an exact witness

## Claim and scope

This directory gives an exact 43-vertex colored graph satisfying the complete
individual-degree and one/two-outside-vertex interface currently isolated in
the `M=214,c=13` two-anchor branch.  It has

```text
red degrees                 20^13 21^30,
red E-incidences            6^42 8^1,
anchor triangle counts      100,100 in both colors at both anchors,
monochromatic K5s with <=2 outside vertices   0.
```

Consequently, adding every individual outside degree and `E`-incidence
equation to the height-2943 pairwise aggregate system still does not eliminate
the cell.  This is a counterexample to the sufficiency of that relaxation.

It is emphatically **not** a Ramsey graph or an exclusion of `M=214,c=13`.
Thirty-nine vertices fail their required red/blue triangle counts, and direct
enumeration finds 335 red and 531 blue `K5`s, all containing at least three
outside vertices.  The next missing interface is therefore the all-red
deficiency-seven condition at every vertex together with the three-, four-,
and five-outside monochromatic-five-set constraints.

## Normalization and certificate

Normalize the red anchor edge as `uv`.  Its thirteen common red neighbors form
the cyclic `(3,5;13)` graph `H` on `Z/13Z`, with

```text
i ~ j  iff  i-j is in {1,5,8,12} modulo 13.
```

The 28 outside vertices are ordered as `A[0..6],B[0..6],O[0..13]`, where
`A` is red only to `u`, `B` red only to `v`, and `O` blue to both.  The
13-bit footprint of an outside vertex records its red core neighbors.
`certificate.json` records all 28 footprints, the thirteen marked outside
vertices, the exceptional pivot `D0`, and the 183 outside red edges.

The certificate uses the `k=0` marking: the first six A vertices, first six B
vertices, and first O vertex form `E`.  Each core column has total 15 and
marked total 6.  The cell footprint incidences and outside red-edge counts are

```text
I_A=49, I_B=47, I_O=99,
m_A=12, m_B=14, m_O=55,
m_AB=18, m_AO=43, m_BO=41.
```

For every outside pair `x,y`, blue is forbidden when
`H \\ (S_x union S_y)` contains an independent triple.  For pairs sharing A
or sharing B, red is forbidden when `H[S_x intersection S_y]` contains a red
edge.  The recorded outside edge coloring obeys every such forced color.

## Individual-factor mechanism and discovery

For fixed footprints and marks, let `d_x` be the required outside red degree
of vertex `x`, and let `e_x` be its required number of red neighbors among the
marked outside vertices.  With `k=0`,

```text
d_x = 21 - mark(x) - anchorRed(x) - |S_x|,
e_x = 6 + 2 [x is the pivot].
```

The edge variables split into marked-marked, marked-unmarked, and
unmarked-unmarked factor blocks.  The anchor triangle equations couple their
six cell-pair edge totals.  A useful necessary load cut follows immediately:
for marked `x` in A or B, forced marked neighbors outside its cell plus the
minimum number of marked neighbors required to realize the cell's internal
edge total cannot exceed `e_x`.  The height-2943 selection violates such a cut
by two at one B vertex, explaining its continuous-LP infeasibility without an
integer search.

`search_individual_projection.cpp` uses these factor-capacity and vertex-load
cuts inside column-preserving footprint trades.  Every move redistributes each
core bit among two to four rows with the same mark status, so all total and
marked column equations remain exact.  GNU g++ 16.2.0 with seed `49100`
reaches the recorded 28 footprints at step 11,391,779.  The compact 378-edge
MILP emitted by `generate_edge_lift.py` then finds an individual edge lift.
The solver is discovery machinery, not part of the proof trust boundary.

## Exact validation

The Python checker parses the certificate and reconstructs the 43-vertex
coloring from definitions.  It enumerates the 26 core edges, 78 independent
core triples, 39 independent core four-sets, all 3,459 legal footprints, every
vertex degree and `E`-incidence, both anchor triangle colors, and all
962,598 five-subsets.  Five deterministic corruptions are rejected.

The source-independent C++20 checker embeds the footprints and outside
adjacency as fixed-width masks.  It independently reconstructs the graph with
nested loops, checks every equation and pair rule, and reproduces the complete
five-set census.  It shares no JSON parser, Python combination machinery,
MILP generator, or solver assignment.

The fixed certificate's monochromatic-five-set census by number of outside
vertices is

```text
outside vertices     0   1   2    3    4    5
red K5               0   0   0  181  123   31
blue K5              0   0   0   42  321  168
```

## Reproduction

The recorded environment used CPython 3.12.12, GNU g++ 16.2.0, SCIP 10.0.3,
and SoPlex 8.0.2.  Verification of the mathematical claim needs no solver:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 check_certificate.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O check_certificate.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_certificate.py \
  | cmp - EXPECTED_TEST_OUTPUT.txt
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  independent_check.cpp -o /tmp/r55_individual_check
/tmp/r55_individual_check | cmp - EXPECTED_INDEPENDENT.txt
shasum -a 256 -c SHA256SUMS
```

The discovery path is reproducible separately:

```bash
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  search_individual_projection.cpp -o /tmp/r55_individual_search
/tmp/r55_individual_search 49100 12000000 2>/dev/null \
  | cmp - EXPECTED_SEARCH.txt
PYTHONDONTWRITEBYTECODE=1 python3 generate_edge_lift.py certificate.json \
  --output /tmp/r55_individual.lp | cmp - EXPECTED_GENERATOR.txt
scip -q -c 'read /tmp/r55_individual.lp' -c optimize \
  -c 'write solution /tmp/r55_individual.sol' -c quit
PYTHONDONTWRITEBYTECODE=1 python3 extract_edge_lift.py certificate.json \
  /tmp/r55_individual.sol --output /tmp/r55_individual_replay.json
PYTHONDONTWRITEBYTECODE=1 python3 check_certificate.py \
  /tmp/r55_individual_replay.json
```

SCIP may select a different valid 183-edge lift; the replayed certificate is
checked from definitions rather than compared byte-for-byte with the included
one.  The generated 21,894-byte LP has 378 binary variables, 129 constraints,
53 forced-red edge equations, 16 forbidden-red edge equations, and SHA-256
`5c9afda3e7157431dca69959d9a63266b6b7624521e857f9f520a6f769fd4615`.

## Trust boundary

Trusted are the accepted normalized `c=13` anchor quotient and individual
equations; the displayed cyclic core definition; the 1,643-byte certificate;
the short Python and C++20 checkers; language semantics; ordinary hardware;
and SHA-256 collision resistance.  The claim does not trust SCIP, SoPlex,
floating-point feasibility, the heuristic search, a generated LP, raw solver
output, a private database, catalogue file, binary, or credential.  The cyclic
core representative inherits the catalog-uniqueness trust boundary already
recorded at height 2823.
