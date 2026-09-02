# Symbolic one-vertex extension obstructions for \(R(5,5)\)

This directory develops exact algebraic certificates for extending a
Ramsey\((5,5,42)\) coloring by one vertex.  The first result identifies the
precise Sherali--Adams degree at which the signed \(K_4\) extension clauses
become visible.

## Clone-evaluation identities and bichromatic coverage

`bichromatic-clone-identities.md` proves exact identities obtained by
evaluating the signed extension polynomial on two clone assignments per core
vertex.  Every unsatisfiable extension subsystem must cover all core vertices
with its red clauses and with its blue clauses separately.  For an order-42
\(R(5,5)\) core, an obstruction profile \((r,b)\) must satisfy

\[
r\geq 11,\qquad b\geq 11,\qquad r+b\geq 43.
\]

The same identities give exact incidence constraints for nonnegative
rational LP certificates and a local graph-theoretic cloning criterion for
one-vertex extendibility.  No computation is required to check the proof.

## One-flip clone identities and near-\(K_5\) witnesses

The proof note `one-flip-clone-defect-identities.md` reverses one coordinate
of a clone assignment and classifies every violated clause.  The resulting
identities expose selected one-edge-defect cliques and force a complementary
near-\(K_5\) witness whenever all selected clique links through a vertex
share a common neighbor.

For a signed-\(K_4\) obstruction on 42 vertices, a vertex belonging to a
unique selected red \(K_4\) forces three distinct selected blue
one-red-edge defects; the complementary statement also holds.  Global
double counting gives exact rational inequalities whose defect terms are
the creation terms in monochromatic-\(K_5\) edge-flip derivatives.

## Deficiency-one exclusion and a 44-clause lower bound

`deficiency-one-monotone-obstruction-bound.md` combines bichromatic clone
coverage with the splitting theorem for minimally unsatisfiable CNFs of
deficiency one.  A monotone \((k,\ell)\)-CNF in \(\mathrm{MU}(1)\) has at
least

\[
\binom{k+\ell}{k}
\]

clauses.  Since signed-\(K_4\) extension subsystems are monotone
\((4,4)\)-CNFs and every minimal obstruction on a Ramsey \((5,5,42)\)-core
uses all 42 variables, a hypothetical 43-clause obstruction would belong to
\(\mathrm{MU}(1)\) but would need at least \(\binom{8}{4}=70\) clauses.  Thus
every such obstruction has at least 44 clauses; together with the certified
74-clause core for graph 0 this gives \(44\leq\mu(G_0)\leq74\).

## Deficiency-two singular normal form

The note deficiency-two-singular-dp-normal-form.md proves that every
hypothetical 44-clause obstruction is a minimally unsatisfiable CNF of
deficiency two and must contain a singular variable.  Its first singular
Davis--Putnam reduction replaces the clauses through that variable by exact
mixed six-literal resolvents with sign profile \(3+3\).  Complete singular
reduction reaches a uniquely determined canonical deficiency-two formula
\(\mathcal F_p\), while the one-flip theorem simultaneously forces
near-\(K_5\) defect witnesses at the first reduction variable.  This turns
the unresolved 44-clause case into a constrained inverse-resolution
problem rather than an arbitrary clause search.

## Inverse singular-DP classification and length barrier

`inverse-singular-dp-length-barrier.md` gives the exact common-core-split
parametrization of every one-step inverse singular-DP extension. At the
signed-`K4` leaves the final inverse step is forced to be a disjoint `3+3`
fan of arity at most 30. A resolution-ancestry argument proves that a binary
clause cannot occur before five singular reductions, excluding the canonical
terminal families `F_38`, `F_39`, `F_40`, and `F_41`. A compact JSON
certificate and standard-library checker audit the arithmetic and every
small common-core split of `F_p` for `p=2,3,4`.

`terminal-binary-proliferation-barrier.md` strengthens the ancestry argument
by tracking distinct binary clauses. The fifth singular step can create at
most one binary; on the sixth step, creating many binaries would force a
common literal, while the binary cycle of `F_p` has empty total intersection.
This excludes `F_36` and `F_37`, leaving the exact current survivor range
`2 <= p <= 35`. A compact JSON certificate and definition-level Python
checker verify the stage floors and terminal-cycle incidence calculation.

`binary-star-unit-barrier.md` classifies the complete binary-clause shape
after the sixth reduction: there are at most two binary clauses, or all of
them share one signed literal; moreover no unit clause can occur. A seventh
singular step can therefore contribute at most one member of the terminal
binary cycle, while the remaining 34 members cannot be inherited from either
sixth-stage alternative. This excludes `F_35` and leaves `2 <= p <= 34`.
The accompanying JSON certificate and standard-library checker audit the
finite cycle-incidence and arithmetic layer.

`stage-four-ternary-bottleneck.md` pushes the exact inverse chain one step
further. The common-tail rule allows at most one ternary clause in `G_4`, but
the independently verified `p=34` unit chain has two exhaustive sixth-step
parent shapes and either one pulls back to four distinct ternaries in `G_4`.
This contradiction excludes `F_34`, leaving `2 <= p <= 33`. A compact exact
checker constructs both parent patterns, replays their DP reductions, and
audits all four labeled terminal unit-fan choices.

`exact-p34-unit-fan-classification.md` closes the scope caveat in that last
checker. Although an unrestricted inverse unit extension of `F_34` can select
any nonempty subset of its 36 clauses, the exact `G_6` binary pair forces all
34 cycle clauses to be selected. The two long clauses remain independently
optional, yielding exactly four labeled fans and three isomorphism classes.
The new checker derives completeness, verifies deletion witnesses and both DP
steps, and checks the complement-reversal symmetry.

`unit-fan-universality-counterexample.md` then stops the one-value-at-a-time
descent and tests the proposed global binary-profile mechanism. For every
`p >= 3` and every subset `R` of the terminal binary cycle it constructs a
two-step inverse singular lift in `MU(2)` whose binaries are exactly a fresh
two-clause unit split together with `R`. Binary count is therefore
nonmonotone, the global-star flag is arbitrary, and an exact incidence state
space modulo terminal symmetry has at least `ceil(2^p/(2p))` states. The
result redirects the program to Ramsey-support-aware symbolic certificates.

`ramsey-link-fan-arity-bound.md` is the first Ramsey-support-aware global
obstruction after that pivot. The exact link interval `17 <= rho <= 24`,
three near-`K5` witnesses, bichromatic coverage of the remaining
main-color neighbors, and the 44-clause budget combine to give

```text
m <= 30 - ceil((rho - 3)/4) <= 26.
```

Thus all first-fan arities 27 through 30 are eliminated simultaneously,
independently of the terminal parameter and inverse-DP history.

`incidence-budget-first-fan-normalization.md` supplies a complementary
global compression with a stronger existential quantifier. The exact 176
signed-literal occurrences, bichromatic coverage, singular existence, and
divisibility of each color-incidence sum by four prove that some legal first
pivot has `m <= 10`. If no pivot has `m <= 9`, the incidence relaxation has
only one profile up to color exchange: one vertex of degrees `(1,10)`, one
of degrees `(3,2)`, forty of degrees `(2,2)`, and clause split `(21,23)`.
The standard-library checker exhausts every possible placement of the single
incidence slack; it does not assert Ramsey-support realizability.

`exceptional-m10-link-incidence-frontier.md` couples the sole `m=10`
incidence state to the actual red/blue neighborhood partition at its pivot.
Three forced one-flip witnesses and the remaining ten off-pivot blue clauses
give `2*rho <= 43`, excluding `rho=22,23,24`.  The surviving strata
`rho=17,...,21` have exactly 39 canonical residual link-deficit profiles,
with a unique profile at `rho=21`; the compact checker independently
enumerates and hashes the full profile list.

`rho21-two-link-kernel-normal-form.md` resolves the abstract support-incidence
geometry of that unique top stratum.  Suppressing degree-two support vertices
turns its red-neighborhood projection into a 10-node marked multigraph with
exactly two degree families and its blue-neighborhood triangle system into a
13-node marked multigraph with one degree family.  Exact converses show that
these kernels are a complete finite alphabet for the incidence projection;
the remaining question is their realizability inside an actual two-colored
`K5`-free Ramsey core.

`rho21-global-blue-k5-kernel-criterion.md` glues those two link kernels into
one 23-node blue-clause multigraph.  A pairwise-intersecting-edge
classification gives three exact forbidden patterns: a weighted triangle of
weight at least five, a weight-four triangle containing at least two side
nodes, or a non-side four-star into the side set.  Their absence is equivalent
to the selected blue supports not already forcing a blue `K5`.  Explicit
members of both abstract link families pass this filter, precisely locating
the next missing information in red-support and completion constraints.

`rho21-bichromatic-matching-cover-normal-form.md` adds the selected red
supports exactly. Opposite-color intersection at most one turns every red
`K4` avoiding the pivot into a four-edge matching of the blue-clause kernel.
The exceptional degree profile gives exactly two possible demand vectors, so
the full selected-support problem is a `41 x 20` binary matching-cover system
with a proved converse. Exact covers for both marked kernel families and both
demand cases force no monochromatic `K5`; completion of unspecified core
edges or deeper singular-DP ancestry is therefore genuinely necessary.

## Reproduce

```bash
python3 derive_sa_visibility.py
python3 verify_sa_visibility.py
python3 test_sa_visibility.py
```

Both implementations use `fractions.Fraction`; no graph enumeration,
floating-point solver, or external package is involved.  The derivation uses
multilinear polynomial arithmetic.  The verifier instead uses conditional
expectations and a 16-row truth table.

The checked output is recorded in `sa-visibility-certificate.json`.

## A 74-clause subset-minimal extension obstruction

`signed-k4-mus.json` isolates 74 of the 2,313 signed \(K_4\) clauses for
authoritative order-42 graph 0.  The core contains 37 red and 37 blue clauses,
uses all 42 variables, and is subset-minimal unsatisfiable.  Its certificate
contains a 41-addition DRUP refutation and 74 distinct single-clause-deletion
witnesses.

Download the authoritative input, generate the certificate with the pinned
solver version, and check it without solver dependencies:

```bash
curl -fsS https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6 -o r55_42some.g6
python3 -m pip install -r requirements-mus-generation.txt
python3 generate_signed_k4_mus.py r55_42some.g6 > regenerated.json
python3 verify_signed_k4_mus.py r55_42some.g6 signed-k4-mus.json
python3 test_signed_k4_mus.py r55_42some.g6 signed-k4-mus.json
```

The verifier reconstructs the graph and all signed \(K_4\) clauses directly,
checks every DRUP addition by unit propagation, and checks every deletion
witness against the retained clauses.
