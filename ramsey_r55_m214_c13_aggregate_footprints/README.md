# Aggregate footprints do not close the M=214, c=13 cell

## Claim and scope

Let `uv` be the normalized red anchor pair of common-red codegree thirteen in
the `M=214`, `E_left_8` branch, let `C` be its common-red core, and partition
the other 28 vertices into

```text
A = red to u only,     |A|=7,
B = red to v only,     |B|=7,
O = red to neither,    |O|=14.
```

This directory establishes two precise facts.

1. The natural all-marking integer relaxation made from every admissible
   core-footprint row, all core column sums, all core E-incidences, both
   anchors' red/blue triangle equations, the three outside degree-sum
   equations, and induced-subset Turan bounds is feasible.  A 28-row, 24-type
   exact certificate witnesses feasibility at `k=|E intersect C|=0`.
2. The witness pinpoints the first omitted coupling.  One `A` row has the full
   core as its footprint.  Such a row must be isolated in the red graph on
   `A`, so seven vertices can support at most 15 internal red edges; the
   aggregate certificate requires 16.  Thus the relaxation cannot decide the
   `c=13` cell without pairwise footprint compatibility.

This is a counterexample to sufficiency of the stated aggregate relaxation,
not a graph in the `M=214` branch, not an exclusion of `c=13`, and not a new
Ramsey-number bound.  No generated MILP, raw solution, solver log, binary, or
private graph state is published.

## The all-marking relaxation

Use the cyclic `(3,5;13)` core on `Z/13Z`, with red edge `ij` exactly when

```text
i-j is in {1,5,8,12} mod 13.
```

It has 39 independent four-sets.  A footprint `S subset C` is admissible when
it hits all 39; all 3,459 admissible masks are used, not only selected minimal
patterns.  For `X in {A,B,O}`, mark bit `q in {0,1}`, and admissible mask `S`,
the nonnegative integer variable `n[X,q,S]` counts rows of that type.

Let `e_i` mark core membership in the intrinsic degree-20 set `E`, let
`k=sum e_i`, and let `p_i` or `p_A` locate the unique E-incidence-eight vertex.
Every actual graph in the cell satisfies

```text
|E intersect A| = |E intersect B| = 6-k,
|E intersect O| = 1+k,
sum_{X,q,S: i in S} n[X,q,S] = 15-e_i,
sum_{X,S: i in S} n[X,1,S] + sum_{j~i} e_j = 6+2p_i.
```

The first two equations come from the anchors' E-incidence six and
`|E|=13`.  The third comes from a core vertex's known six red neighbors—both
anchors and its four core neighbors—and degree `21-e_i`.  The last is its own
E-incidence equation.  The pivot lies either at a marked core vertex or in
`E intersect A`.

Write `I_A,I_B` for the total footprint incidences from `A,B`; write
`m_A,m_B,m_O,m_AB,m_AO,m_BO` for red edge counts within and between the three
outside cells.  The anchor triangle equalities are

```text
m_A + I_A = 61,              m_B + I_B = 61,
m_B + m_O + m_BO = 110,      m_A + m_O + m_AO = 110.
```

For a row in cell `X`, its required number of red neighbors among the 28
outside vertices is

```text
21 - q - a_X - |S|,          a_A=a_B=1, a_O=0.
```

Summing these values in each cell gives `d_A,d_B,d_O`, constrained by

```text
d_A = 2m_A + m_AB + m_AO,
d_B = 2m_B + m_AB + m_BO,
d_O = 2m_O + m_AO + m_BO.
```

Finally, every induced subgraph is both `K5`-free and independent-5-free.
Turan's theorem gives complementary edge intervals `3..18`, `18..73`, and
`84..294` on 7, 14, and 28 vertices.  Because `A` and `B` lie in red
neighborhoods, they are red-`K4`-free and the sharper upper bound 16 is used.
The MILP applies these bounds to `A`, `B`, `O`, `A union B`, and all 28 outside
vertices.

The generator emits one model with 20,754 row variables and every marking
represented simultaneously.  It does not enumerate core markings or selected
core pairs.

## Exact certificate

The certificate has `k=0`, so the core is unmarked, six vertices in each of
`A,B` are marked, one vertex in `O` is marked, and the exceptional marked
vertex lies in `A`.  Its 24 nonzero row types expand to 28 admissible masks.
The principal aggregates are

```text
I_A=45, I_B=54,
m_A=16, m_B=7, m_O=37,
m_AB=0, m_AO=57, m_BO=66,
d_A=89, d_B=80, d_O=197.
```

Both independent checkers reconstruct the 39 independent four-sets and 3,459
transversals, then verify every row count, column equation, marking equation,
anchor equation, degree sum, edge capacity, and Turan interval with exact
integers.

## Pairwise obstruction and reusable cut

Suppose `a in A` is red to every vertex of `C`.  Every other `b in A` has an
admissible footprint `S_b`.  Since the core has independence number four and
`|S_b|>=5`, the set `S_b` contains a red core edge `xy`.  If `ab` were red,
then `{u,a,b,x,y}` would be a red `K5`.  Hence `a` is blue to every other
vertex of `A`.  The same argument holds in `B`, using anchor `v`.

More generally, if `f_X` rows in `X in {A,B}` have full footprints, all are
red-isolated in `G[X]`, so

```text
m_X <= binom(7-f_X,2).
```

The certificate has `f_A=1`, hence `m_A<=15`, but its aggregate equations
require `m_A=16`.  The one-edge gap proves exactly why the aggregate system is
feasible yet nonliftable.  The next useful mechanism is the complete
compatibility graph on footprint types, not another aggregate count or SAT
encoding variant.

## Reproduction and validation

The recorded environment used CPython 3.12.12, SCIP 10.0.3 with SoPlex 8.0.2,
and Apple clang 17.0.0.  From this directory run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 generate_milp.py \
  --output /tmp/r55_m214_c13_aggregate.lp
scip -q \
  -c 'read /tmp/r55_m214_c13_aggregate.lp' \
  -c optimize \
  -c 'write solution /tmp/r55_m214_c13_aggregate.sol' \
  -c quit
PYTHONDONTWRITEBYTECODE=1 python3 check_certificate.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O check_certificate.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_certificate.py \
  | cmp - EXPECTED_TEST_OUTPUT.txt
xcrun clang++ \
  -isystem /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1 \
  -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  independent_check.cpp -o /tmp/r55_c13_aggregate_check
/tmp/r55_c13_aggregate_check | cmp - EXPECTED_INDEPENDENT.txt
shasum -a 256 -c SHA256SUMS
```

On a normal Linux C++ installation, omit the explicit macOS SDK include path.
The independent C++ checker uses fixed-size bitmasks and nested loops rather
than Python sets/combinations or the generated MILP.  It also passed
AddressSanitizer and UndefinedBehaviorSanitizer.  Five deterministic corrupted
certificates are rejected.

The canonical generated LP has 20,754 row variables, 27 binary variables,
20,766 general integer variables, 64 constraints, 4,829,321 bytes, and SHA-256
`6f28eb0951cb87d3c25ddabf1620fdedfe4ea243a3743f5183e355bb097d0c40`.
The compact certificate SHA-256 is
`8b8454e0924238e08561cd2d456b5f15940b9e45bfc1af5a46e3c172657d734f`.
SCIP reports an optimal feasibility witness at objective `k=0`, but SCIP is
not in the proof trust boundary because both checkers validate the witness
directly.

## Trust boundary and sources

The universal footprint theorem and aggregate reduction inherit the accepted
`M=214`, `E_left_8,c=13` reductions.  Moving an arbitrary `(3,5;13)` core to
the cyclic representative trusts Brendan McKay's complete catalog, whose
Ramsey-data page records one graph at order 13:
<https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>.  The exact record is
<https://users.cecs.anu.edu.au/~bdm/data/r35_13.g6>.

The edge intervals use P. Turan, *On an extremal problem in graph theory*,
Matematikai es Fizikai Lapok 48 (1941), 436--452.  The numeric bounds are also
recomputed directly from the balanced complete multipartite part sizes.

Trusted are the short certificate and checkers, CPython/C++ language semantics,
ordinary hardware, the cited core classification, the elementary reduction,
and SHA-256 collision resistance.  The mathematical claim does not trust
SCIP floating-point optimality, the generated LP, a raw solution, or a solver
infeasibility assertion.  No novelty claim is made for Turan's theorem, the
core catalog, or the abstract footprint notion.
