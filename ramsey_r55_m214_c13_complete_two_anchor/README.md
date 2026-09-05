# A complete unpinned two-anchor counterexample at M=214 codegree 13

## Result and exact scope

The complete two-anchor local relaxation of the M=214 `E_left_8`, `c=13`
layer is satisfiable.  A 2,470-byte edge list gives an explicit 43-vertex
model satisfying simultaneously:

1. red degrees `20^13 21^30` for the intrinsic classes
   `E={0,...,12}` and `C={13,...,42}`;
2. `a_5=8` and `a_x=6` for all `x!=5`, where
   `a_x=|N_R(x) intersect E|`;
3. the standard doubly exact anchor `u=13`, with red neighbors
   `{0,...,5,14,...,28}`;
4. a central red partner `v=14` with `q_R(u,v)=13`;
5. red and blue local-triangle counts 100 at both `u` and `v`; and
6. all Ramsey constraints induced inside the four color neighborhoods of
   `u` and `v`.

Thus the red neighborhood of either anchor contains no red `K4` or blue `K5`,
and either blue neighborhood contains no red `K5` or blue `K4`.

This is a sharp counterexample to excluding `c=13` by any conjunction of
those two-anchor conditions.  It is **not** a Ramsey `(5,5;43)` graph and not a
model of the complete M=214 branch: the other 41 red-neighborhood deficiency
equalities and global five-set clauses are not part of this relaxation.  The
model contains 180 red and 513 blue `K5`s, all avoiding both anchors.  A
closing mechanism must therefore leave the two-anchor closure, for example by
coupling another anchor or imposing the omitted global conditions.

## Why the formulation covers every E-marking

Height 2755 proves that some central red neighbor of the normalized anchor has
codegree at least nine.  In the `c=13` layer, residual symmetry on the fifteen
central red neighbors safely names that partner `v=14`.

Nothing else about `v` is pinned.  Its six red neighbors in `E`, all 78 edges
of the common-red 13-set, and every other partner edge remain variables.  One
exact sum enforces

```text
sum_{w in N_R(u)-{v}} x_vw = 13.
```

The generator uses conditional clauses over all 42 other vertices for the
four partner-neighborhood Ramsey conditions.  Therefore it does not choose a
core labeling, an `(s,k)` type, or a selected pair of Ramsey cores.

`audit_reduction.py`, which does not import the generator, enumerates all
`C(13,6)=1716` partner E-neighborhoods.  They occupy all twelve `(s,k)` types.
After including compatible central choices, one formula implicitly covers
2,425,062,140 labeled partner neighborhoods.  This proves coverage of every
E-marking without a marked-core orbit census.

## CNF formulation

Variables 1--903 are red edges.  For each pair of vertices other than `v`, the
next 861 variables indicate a red triangle through `v` and another 861
indicate a blue triangle through `v`.  Bidirectional four-clause conjunctions
define them.  Balanced unary totalizers impose:

* all 43 red degrees;
* all 43 E-incidences;
* common-red codegree 13;
* both red and blue triangle counts 100 at `v`; and
* the red-edge totals 100 and 110 in the fixed red and blue neighborhoods of
  `u`.

For a four-set `S` outside `v`, conditional clauses forbid a red `K4` when
`S subset N_R(v)` and a blue `K4` when `S subset N_B(v)`.  The analogous two
families on five-sets forbid a blue `K5` in `N_R(v)` and red `K5` in
`N_B(v)`.  The fixed-anchor families are emitted directly.

The deterministic formula census is:

```text
variables                       29,611
graph variables                    903
partner triangle variables        1,722
totalizer variables              26,986
clauses                       2,492,430
conditional/fixed local clauses 1,977,864
conjunction clauses                6,888
totalizer clauses                507,636
anchor units                          42
bytes                        138,517,605
SHA-256 2ce34acd542808c44755edbd467a976abd98e16c0d6c3cadc644db6807937b93
```

`formula_manifest.json` pins the generated stream.  The 132 MB CNF is omitted
from source control and can be regenerated deterministically.

## Compact model

`model.edges` lists all 445 red edges.  The quotient cells

```text
R = both red, A = u-only, B = v-only, D = both blue
```

have sizes `(13,7,7,14)`, with E-parts `(3,3,3,4)` and C-parts
`(10,4,4,10)`.  Their exact edge data are

```text
eR=26, eA=9, eB=8, eD=45,
eRA=52, eRB=53, eAD=56, eBD=57, eRD=87, eAB=11.
```

In particular

```text
eRD+eAB = eR+eA+eB+eD+10 = 98,
```

so the height-2755 diagonal identity is met exactly.

## Reproduction and validation

Tested with CPython 3.12.12, Apple clang 17.0.0, and CaDiCaL 3.0.1 commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`.  From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit_reduction.py
PYTHONDONTWRITEBYTECODE=1 python3 generate_unpinned_two_anchor_cnf.py \
  --output /tmp/unpinned_two_anchor.cnf
shasum -a 256 /tmp/unpinned_two_anchor.cnf

PYTHONDONTWRITEBYTECODE=1 python3 check_model.py model.edges
c++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  check_model.cpp -o /tmp/check_model
/tmp/check_model model.edges
```

Concatenate the audit, Python-model, and C++-model output and compare it with
`EXPECTED_OUTPUT.txt`.  Normal and optimized Python agree.  The generated CNF
was regenerated byte-for-byte.  The C++ checker passed strict optimized,
AddressSanitizer, and UndefinedBehaviorSanitizer builds.  Both model checkers
reject a same-size one-edge swap.

CaDiCaL found the model in 56.32 seconds with peak resident memory 1.66 GB.
The solver log and assignment are discovery provenance only and are omitted;
the mathematical claim rests on direct checking of `model.edges`.

## Trust boundary

The completeness argument is the displayed residual-symmetry and conditional-
clause argument.  The Python audit independently checks the marking cover and
formula census.  The two direct model checkers do not read the CNF or trust its
auxiliary variables; they reconstruct every defining graph property and
exhaust all relevant four- and five-subsets.  Trusted are the short sources,
CPython exact integer/set semantics or the C++ compiler/standard library,
ordinary hardware, and SHA-256 collision resistance.

The M=214 interpretation inherits the complete height-2505 branch reduction,
height-2603 excess partition, and height-2755 high-codegree quotient.  No
catalogue graph, solver correctness, generated CNF, raw search dump, or claim
about the omitted all-vertex deficiency/global-K5 layer is trusted.
