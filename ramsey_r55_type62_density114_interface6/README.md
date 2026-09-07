# The complete type-62 density-114 family and interface 6

**Exact classification.** There are exactly **1,697 isomorphism classes** of
\(J\in\mathcal R(4,5;23)\) with 114 edges and a degree-five vertex h whose
neighborhood induces \(K_{2,3}-e\). Here \(\mathcal R(4,5;23)\) means no
red four-clique and no blue five-clique. Every member has a unique degree-five
vertex and trivial automorphism group. The compact certificate contains every
canonical representative as five actual attachment columns.

**Complete consumer.** Every one of the **3,394** marked gluings of this
family to original interface 6 is impossible, even on the forty-vertex union
of the two neighborhoods. Consequently, if a hypothetical Ramsey43 graph has
\(N_R(r)\) isomorphic to original interface 6, with degree-five hub z and
\(d_R(z)=23\), then

\[
e_R(N_R(z))\le113,\qquad \delta_R(z)=122-e_R(N_R(z))\ge9.
\]

This improves the previous bound eight for this complete intrinsic branch.
The statement also holds after reversing colors.

The classification and its consumer form one result. A valid local neighborhood
alone is not a global completion. All **389** remaining physical pairs stay free
in every marked template. The necessary 40-vertex subsystem constrains the
272 private-core pairs; the other 117 pairs remain wholly unrestricted.

The general classification imports uniqueness of the order-17 (4,4) graph.
The literal computation on the displayed Paley core uses no external catalogue.
Interpreting original interface 6 imports the reviewed thirteen-type dense
neighborhood theorem. The previous density-115 exclusion is a separate,
explicit premise of the improved global bound.

## Complete local reduction

Take \(T=\mathbb Z_{17}\) with red nonzero differences
\(\{1,2,4,8,9,13,15,16\}\). Add \(S=\{s_0,\ldots,s_4\}\) with red
edges \(02,03,04,12,13\), and a hub h red to S and blue to T. The five
columns \(X_i=N_R(s_i)\cap T\) are actual subsets, with no replacement by
maximal or saturated columns. The following conditions are necessary and
sufficient for the resulting graph to belong to \(\mathcal R(4,5;23)\):

1. Each \(X_i\) is triangle-free in T.
2. For every red S-pair ij, \(X_i\cap X_j\) is independent in T.
3. For every blue S-pair ij, \(T\setminus(X_i\cup X_j)\) has no independent triple.
4. \(T\setminus(X_2\cup X_3\cup X_4)\) is a red clique.

Indeed, S is triangle-free, has no independent four-set and has exactly one
independent triple, 234. A red four-clique meeting S uses one or two S vertices;
a blue five-clique meeting S uses two or three, since T has no independent
four-set. The hub introduces no other forbidden configuration: a red clique
through it would require a triangle in S, and a blue five through it would
require an independent four-set in T. This exhausts all physical forbidden sets.

Conversely, in any J in the stated family the seventeen nonneighbors of h
form a (4,4) graph: a blue four-set there would join h to a blue five-set.
They are therefore Paley-17 by the imported uniqueness theorem. Every member
of the abstract family has the displayed representation.

Since T has 68 edges and S has five,

\[
e_R(J)=78+\sum_{i=0}^4|X_i|.
\]

Density 114 is exactly column sum 36. Complete triangle-free subset generation
gives maximum size eight, so each column has size at least four. The entire
allowed column domain has **7,225** members: 1,632 of size four, 2,550 of size
five, 2,176 of size six, 816 of size seven and 51 of size eight. None is silently
omitted; repetitions are allowed by the search and rejected only by actual
compatibility conditions.

The full exact-sum enumeration gives **461,584 labeled tuples**. After canonical
classification their unordered column-size profiles are:

| Column sizes | Isomorphism classes |
|---|---:|
| 5,7,8,8,8 | 51 |
| 6,6,8,8,8 | 86 |
| 6,7,7,8,8 | 795 |
| 7,7,7,7,8 | 765 |
| Total | 1697 |

In particular, the allowed size-four column never occurs in a valid tuple of
sum 36. This exclusion follows from the complete compatibility computation;
it is not used to prune either enumeration.

## Canonicalization and independent completeness checks

`derive.py` computes independent-set and triangle-free tables on all subsets
of T, builds compatibility bit sets, and searches column positions in order
0,2,1,3,4. It uses only the four exact conditions and the maximum remaining
size bound. The first column is normalized under the 136 affine maps
\(v\mapsto av+b\), with a a nonzero square modulo 17. All **63** first-column
orbits are retained. This produces 3,854 normalized tuples of exact sum 36;
expanding them gives the full labeled tuple set.

`audit_dense.cpp` imports no producer, generated domain or symmetry list. It
grows triangle-free subsets by literal edge tests, derives pair compatibility
from physical red edges and blue triples, then enumerates a compatible C4:
first \((X_0,X_1)\), then \((X_2,X_3)\), then \(X_4\). It performs **no affine
orbit pruning**. The interchangeable positions 2 and 3 are considered in
increasing column order and both ordered tuples are emitted. Equality of those
columns is forbidden by the blue-pair condition: their common blue set would
have at least nine vertices, exceeding the independently checked triangle-free
maximum eight in the complementary Paley graph. The exact density filter is
applied to actual column sizes.

This second enumeration visits 793,798 outer pairs and 194,750,300 C4 pairs.
Its complete sorted stream agrees **entry for entry** with the first enumeration's
orbit expansion. Counts or sampled representatives alone are not the check.
The tuple format is five decimal masks separated by spaces and a newline.
The full stream SHA-256 is

`84f53e3e52093fd4a466251c12f3ae2e937f5f1166eeb372c08b52b9851fdec8`.

`audit_classification.py` imports neither enumerator. It reconstructs the full
Paley automorphism group: all 8! permutations of the neighborhood of zero give
16 local automorphisms, exactly eight of which lift to T; the other eight
vertices have distinct neighborhood signatures, so the lift is forced.
Translations give all 136 automorphisms. All 5! permutations of S give its two
automorphisms. The checker verifies every representative physically, takes the
least tuple under the full product action, and expands disjoint complete orbits.
Every orbit has size \(136\cdot2=272\), explaining
\(1697\cdot272=461584\).

The hub is unique even before the final physical check: every T vertex has
at least eight neighbors, and every S vertex has at least four column neighbors,
one S neighbor and h. Hence any isomorphism must preserve h and its S/T
partition. The product action therefore captures the full graph isomorphism
relation, and full orbit size proves rigidity of the whole 23-vertex graph.
No rigidity assumption is made by either enumeration.

## Complete original interface-6 cohort

Interface 6 is the pinned order-22, 109-edge graph in the preceding
[dense-hub package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification).
Its original degree-five hub is z=21, with S={16,17,18,19,20}, and its graph6 is

```text
UsHHirKdlp[IFVI|KpqfR[NA[DuUp\NCz~?G??Bw
```

If this H occurs as \(N_R(r)\) in a hypothetical Ramsey43 graph and
\(d_R(z)=23\), its seventeen outside red neighbors T are Paley-17; the other
three outside vertices are B. In \(J=G[N_R(z)]\), r is the degree-five hub
and its neighborhood is the same S. At density 114, J must be one of the
1,697 classified graphs. Every one of the **two** isomorphisms of the standard
S to H[S] is retained. Thus every member of this intrinsic branch occurs in
one of the **3,394** physical templates.

Use A=0..15, S=16..20, z=21, r=22, T=23..39, B=40..42. Fix only H, both
anchor stars, the Paley graph on T and the 85 S–T bits from the representative
and marking. Relabeling T transports arbitrary A–T and B–T bits. It need not
extend to an automorphism of G or H. No original-H symmetry removes a marking.
The 389 free pairs are A–T (272), A–B (48), S–B (15), T–B (51) and B–B (3).

For each five-set within H union J, vertices 0..39, impose both monochromatic
prohibitions and substitute only fixed colors. The CNF uses lexicographic
variable numbering on all 389 full-template free pairs, no auxiliary variables,
and no other constraints. Only the 272 A–T variables occur. This is exactly
five-clique avoidance on the forty-vertex union, leaving all other variables
arbitrary. Every full Ramsey43 completion would satisfy it, so a refutation
of the weaker system soundly excludes the entire marked completion family.

The bit-string physical construction in `consumer.py` agrees on all 903 pairs
with the independent integer-decoder/matrix construction in `audit.py` for every
key. Compatible-clique recursion produces one CNF, while `audit_cnf.cpp` scans
all 658,008 five-sets literally to produce the other. All **3,394** complete
formula comparisons pass, with 19,126 through 19,340 clauses
per case and 65,215,510 clauses in total. Kissat produces a refutation
for every key, and drat-trim verifies all of them. The complete ordered
per-case matrix/formula manifest SHA-256 is

`3834410d2a6bd7793f1306db96a34cd6501e6aa39b389e1fd925df31e70b2506`.

## Reproduction, compact evidence and controls

Use Python 3.10+, a C++20 compiler, Kissat and drat-trim in a full repository
checkout. Choose a new scratch directory outside the source checkout:

```sh
python3 -B ramsey_r55_type62_density114_interface6/reproduce.py /tmp/fresh-r55-type62-114 --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected final status:
`VERIFIED_TYPE62_DENSITY114_CLASSIFICATION_AND_INTERFACE6_EXCLUSION`.

The command regenerates the compact certificate byte for byte, compiles and
runs the full independent labeled enumeration, checks all canonical orbits and
physical representatives, runs the controls, reconstructs both formulas for
every marking, solves the entire cohort and checks every native refutation.
There is no census-only mode that could be mistaken for the global exclusion.
Native solver and checker binaries are required. Any missing, undecided or
unverified key makes the command fail.

The complete new 1,697-row certificate is published. The larger expanded tuple
stream and per-case matrix/formula manifest regenerate in scratch; their ordered
hashes and expected results are published. Every case is checked before the
manifest hash is credited. Matrices, checker logs, executables and timing output remain in scratch.
By default, each CNF pair and native proof is deleted only after both formulas
match, the refutation passes drat-trim, and its hashes enter the saved case
record. This keeps native storage to one active case. Supply `--keep-native`
to retain every CNF and proof for a separate checker run; none enters Git. No private input or network download is
needed during reproduction.

The upstream `inputs.json` and `certificate.json` are checked against SHA-256
`8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2` and
`f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02`.
Only the original interface record enters the new matrices; the 24 old
representatives are not substituted for the new density-114 family. The new
certificate is independently regenerated and audited in this command.

Local reduction controls exhaust 35,049 small physical configurations, of
which 27,027 satisfy the exact four conditions, and compare directly with
red-four/blue-five avoidance. Five damaged classifications and five malformed
graph6 inputs are rejected. Kernel controls exhaust 32 formulas and all 32,768
assignments (32,243 satisfying), reject eighteen input/scope corruptions, and
check an omitted-vertex example. All 3,394 templates undergo 3,064,782
scrambled-label pair checks with arbitrary free assignments. Those are controls;
the general transport bijection is the mathematical argument above.

A fresh complete public-command replay passed in **1395.005426 seconds**,
including both complete enumerations, every orbit/physical check, the controls
and all 3,394 independently reconstructed and refuted kernels. Its certificate,
ordered matrix/formula manifest and every native proof hash match production.
The recorded verified production cases used 233.712720 aggregate solver
seconds and 313.500504 checker seconds; the slowest solve took
0.202875 seconds. The checked production traces totaled
152,151,217 bytes before per-case cleanup. These are observed costs,
not resource guarantees. Normal and optimized controls match, including kernel
controls with a Clang 17 address/undefined-behavior build of the independent
CNF auditor. An empty native proof and a malformed C++ type argument are rejected.

The per-case cap is 30 seconds, with an outer solver limit of 45 seconds and
a proof-check limit of 120 seconds. Primary native sources are
[Kissat](https://github.com/arminbiere/kissat) and
[drat-trim](https://github.com/marijnheule/drat-trim). Exact source commits,
compiler settings and observed costs are in `NATIVE_REPLAY.json`. Hashes provide
identity, not a substitute for exhaustive coverage or a checked proof.

## Dependencies, novelty and residual cases

The literal Paley-column classification and literal 40-vertex contradictions
use no external graph-catalogue completeness. Their intrinsic application
imports order-17 (4,4) uniqueness and the
[thirteen dense degree-five interface theorem](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification),
source commit `8bf27902fba404e35593c90cbc7d2991abeda510`, accepted at h3355.
The Paley degree-23 bridge is h3419, accepted h3431. The prior complete
[type-62 density-115 classification and consumer](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification)
is h3455, source commit `590bcae0fe01e88e0a8fcf8030fbb2524973e4cb`, independently
accepted h3467. It excludes all higher-density possibilities for interface 6;
this new consumer excludes the next complete layer. U(23)=122 is imported only
to express the resulting deficiency. These imported theorems are not silently
reproved by reading their input records.

The preceding [uniform thirteen-type theorem](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree_five_hub_gap),
h3607 and source commit `eebedd0617abb53088e1af52b0e66fe36ac9882a`, completed all
3,132 type-126 density-116 keys. The present density-114 type-62 result has a
disjoint scope and does not recount those cases. H3631 has independently
accepted h3607 and its formerly unreviewed twenty- and sixteen-edge dependencies:
[review evidence](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_dense_degree_five_hub_gap_review1),
source commit `82a4cb7a5f72c60e2b16e7f2b45a8c42ade6d4fd`. This package does not
repeat that review and does not require those type-126 consumers for its new
type-62 implication.

Primary literature was checked after graph-first selection:
[Angeltveit and McKay's pointed-gluing framework](https://arxiv.org/html/2409.15709v2)
and [McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
The column decomposition and pointed gluing are classical. A limited search
found no matching exact 1,697-class layer or interface-6 consequence; historical
priority, a new gluing method and optimality are not claimed.

Trust remains in the stated external uniqueness/classification premises, the
finite reduction and complete group action, two unformalized exact enumeration
and encoding implementations, compiler/interpreter semantics, the native DRAT
checking kernel, and ordinary hardware. This is author evidence with independent
implementations, not external acceptance or proof-assistant formalization.

The precise new exclusion is interface 6, global hub degree 23, local type 62
and density 114, with all 1,697 representatives, both markings and every
remaining physical edge free. Interfaces 7 and 8 still have **6,788** unconsumed
density-114 keys in this same classification. Lower density at interface 6
remains possible under this result. None of the twelve surviving full
degree-23 interface families is closed, and no Ramsey-number bound changes.

The next falsifiable structural milestone is a complete original-interface-7
consumer of this same layer, subject to refreshed principal and ledger evidence.
There is no larger-timeout restart of the frozen H-star route. Global moment
certificates and publication audits remain the other researchers' lanes.
