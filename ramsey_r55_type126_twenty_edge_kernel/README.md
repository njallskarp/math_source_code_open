# A twenty-edge neighborhood family excludes dense interfaces 1 and 2

**Computer-assisted theorem.** The partial neighborhood below has exactly
434 labeled completions in \(\mathcal R(4,5;22)\). They are precisely
the independent sets of a specified 29-edge conflict graph that meet each
of eight specified subsets. Every completion has the same unique degree-five
hub z and the same K2,3 on its five neighbors. Their densities range from
102 to 109; the two dense endpoints are the original interfaces 1 and 2.

If any of these neighborhoods H occurs as \(N_R(r)\) in a hypothetical
43-vertex (5,5)-Ramsey graph, and \(d_R(z)=23\), then

\[
e_R(N_R(z))\le115,\qquad \delta_R(z)=122-e_R(N_R(z))\ge7.
\]

The complete density-116 boundary has 348 partial templates, all refuted
on their 40-vertex neighborhood unions. Their **409 free physical edges**
include all twenty variable attachments, all 272 private-core cross edges,
and all 117 other globally free edges. The 434 local fillings are not
fixed one at a time in these refutations. This excludes all **696** original
marked equality cases of interfaces 1 and 2, with the surviving interface
left fully free in every necessary system.

With the prior accepted exclusions of interfaces 0, 10 and 12, **1,392**
original type-126 equality cases remain on interfaces 3, 4, 9 and 11.
Lower densities and lower hub degrees remain open. No entire retained
degree-23 interface, M-slice or Ramsey-number bound is settled.

## Exact local family

Red edges are graph edges. Use A={0,...,15}, S={16,...,20}, z=21.
Start with zero-based interface 1 of the hash-pinned thirteen-record input:

```text
UsHHirKdlp[IFVI|KpqfR[NABbf}?^Scy[D{??Bw
```

Delete the colors of these twenty pairs, in local variable order:

```text
1:(1,19)   2:(2,19)   3:(2,20)   4:(4,17)   5:(4,20)
6:(5,19)   7:(6,17)   8:(7,17)   9:(7,19)  10:(7,20)
11:(8,17) 12:(8,20) 13:(9,17) 14:(9,19) 15:(10,19)
16:(11,19) 17:(11,20) 18:(12,19) 19:(15,17) 20:(15,20)
```

These are exactly the color disagreements with interface 2 after swapping
vertices 19 and 20 and fixing every other vertex. The literal map and all
231 physical pairs are checked. This is just one displayed relabeling;
no group completeness, optimal alignment, or global automorphism is assumed.
All A, S and z data and 60 of the 80 A–S pairs remain fixed.

Let X be the set of local variable positions assigned red. Let F have
vertex set {1,...,20} and the following 29 edges:

```text
(1,9) (1,16) (2,15) (2,16) (3,5) (3,17)
(4,5) (4,8) (4,11) (4,18) (5,10) (5,12)
(6,14) (6,18) (7,13) (7,19) (8,10) (8,19)
(9,18) (10,17) (10,20) (11,12) (11,13) (11,19)
(12,20) (13,14) (14,16) (15,18) (19,20)
```

The eight required meeting sets are

```text
{1,2,3,14} {1,2,3,18} {2,3,9,10,12} {2,3,9,10,14}
{12,16,17} {12,18} {14,15} {15,16,17}
```

Then the exact characterization is

\[
H\in\mathcal R(4,5;22)
\quad\Longleftrightarrow\quad
X\text{ is independent in }F\text{ and meets all eight sets}.
\]

To verify both directions, append a universal red vertex and substitute
the fixed colors in every monochromatic-five prohibition. The resulting
twenty-variable CNF has 54 distinct clauses. After subsumption exactly
37 remain: one negative pair clause for each edge of F and one positive
clause for each meeting set. The universal-root condition is exactly the
absence of red K4 and blue K5 in H. All clauses and the subsumption identity
are independently checked; no local density constraint is added.

The constrained independence polynomial is

\[
t^3+17t^4+78t^5+143t^6+123t^7+55t^8+15t^9+2t^{10}.
\]

There are 99 fixed red edges, giving respectively 1,17,78,143,123,55,15,2
fillings at densities 102 through 109. All have z as their unique degree-five
vertex. The two dense masks are 318252 and 730323, with position i encoded
by bit i−1; they are exactly the original two endpoints. Counts are labeled,
without an isomorphism quotient or a claim about other partial graphs.

`local_classification.py` enumerates independent sets by include/exclude
recursion, pruning a branch only when a required set cannot be met.
`audit_local.cpp` reads only a literal 22-vertex matrix and imports no
conflict graph, CNF or producer. It directly visits all red-four and
blue-five subsets, then checks **every one of the 1,048,576 assignments**.
Its complete sorted model stream equals the Python stream byte for byte.
A separate Python clique search also checks every surviving physical graph.
The independent C++ five-set encoder verifies the full 23-vertex CNF.

The sorted decimal model stream, one mask per line, has SHA-256
`99b93296ab9aa6ded652b5f24509465d25cb7810c196a71b22055d5194d06dcd`.
`LOCAL_CERTIFICATE.json` supplies the twenty pair positions, conflict edges,
meeting sets, all 434 models and density counts.

## Complete intrinsic gluing and physical transport

Append r=22, T={23,...,39} and B={40,41,42}. Fix r red to H and blue to
T and B. Fix z red to T and blue to B. Fix T to Paley-17, with red
differences {1,2,4,8,9,13,15,16}. Use each of the 29 type-126 density-116
representatives of the reviewed
[dense-hub classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification)
for the 85 S–T bits, with all twelve relative K2,3 markings.

There are 494 fixed and **409 free** pairs in the full 43-vertex template:
twenty A–S, 272 A–T, 48 A–B, 15 S–B, 51 T–B and three within B.
The first 292 belong to the 40-vertex union; the other 117 do not occur
in any kernel clause. No original free pair is pinned. No outside quota,
extra degree profile, H-density constraint or auxiliary variable is used.

To prove complete intrinsic coverage, take H=N_R(r) and d_R(z)=23.
Exactly seventeen outside vertices are red to z. They form a (4,4;17)
graph and are Paley-17 by the explicit imported uniqueness theorem.
In J=G[N_R(z)], the root r has the five neighbors S, inducing K2,3.
The imported local theorem gives e(J)≤116 and exactly 29 equality classes,
each with a unique degree-five hub. An isomorphism labels that hub as r,
its five neighbors as S, and its seventeen nonneighbors as T. Every one
of the twelve relative S markings is retained. Relabeling T transports
its arbitrary free incidences and need not be an automorphism of G.
Thus all 348 templates cover every local filling at equality.

For each original endpoint, `audit.py` independently constructs all
29×12 physical matrices and transports the appropriate S marking through
the identity or the swap 19↔20. Every target key has exactly two original
preimages. All **628,488 physical pair transports** are checked: every
target fixed bit is implied, and every formerly free edge remains free.
The 348 target matrices are distinct. They cover 434×29×12=151,032 labeled
pointed local pairings; this is a coverage count, not a realizable-graph count.

## Exact necessary kernel and refutations

All unfixed pairs of the full 43-vertex matrix are numbered 1 through 409
in lexicographic pair order. For each five-set in vertices 0 through 39,
impose both monochromatic prohibitions after substituting fixed colors;
discard satisfied clauses and deduplicate. This is exactly the absence of
a monochromatic K5 in the 40-vertex union. Every full Ramsey completion
would satisfy this necessary system, with the other 117 variables arbitrary.

The producer uses bit-string graph6 decoding and recursive compatible-clique
growth. `audit.py` imports no producer and reconstructs physical matrices
with integer graph6 decoding and literal marking tests. `audit_cnf.cpp`
reads those independent matrices and loops over every five-set directly.
All 348 full matrices and every CNF agree byte for byte, giving
228,986,784 literal five-set checks. The exact support audit checks that
all 292 kernel variables occur and no outside variable occurs.

Kissat returns UNSAT on every case and drat-trim accepts every refutation.
This refutes the complete equality boundary; the imported ceiling 116
then gives the new bound 115. U(23)=122 is an additional import only for
the deficiency statement. No solver status or hash alone is counted as proof.
`MANIFEST.json` records every key, physical matrix hash, formula hash,
variable count and clause count. Missing or undecided keys fail reproduction.

The encoder, transport scaffold and controls adapt the previously accepted
[twelve-edge package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_consensus_kernel).
The new twenty-edge matrix, local transversal characterization and complete
assignment checker are specific to this contribution. No old refutation is
substituted for a new one.

Complete formula/matrix manifest SHA-256:
`fe9e7cbb7847ff5c5bff24ff11560d0957bc3b2d74a1c657900fe6bdd92f538f`.
Marked-template stream SHA-256:
`3b98404db867f4f8fbd090c7c4ea40a464dcb8382bf8bd72e093033ae63f7a7c`.

## Reproduce and controls

From a full checkout, with Python 3.10+, C++20, Kissat and drat-trim, choose
a new scratch directory outside the source checkout:

```sh
python3 -B ramsey_r55_type126_twenty_edge_kernel/reproduce.py /tmp/fresh-r55-twenty --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected final status:
`VERIFIED_COMPLETE_TWENTY_EDGE_FAMILY_AND_TWO_COHORT_EXCLUSION`.
Both native proof tools are required. The command builds two independent
C++ checkers, verifies the complete local family and transport cover,
runs controls, regenerates both encodings, solves every case and checks
every DRAT proof. It compares all expected outputs and the full manifest.
The adjacent dense-hub classification supplies two hash-pinned JSON files;
its implementation is not imported. Its completeness is an explicit theorem
premise, not an inference from reading canonical records.

Production uses CPython 3.12, GCC 16.2, Kissat 4.0.4 at
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim at
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Native sources are
[Kissat](https://github.com/arminbiere/kissat) and
[drat-trim](https://github.com/marijnheule/drat-trim); ordinary builds after
checking out those versions are `./configure && make` and `make`.
The per-case solve cap is 30 seconds; UNKNOWN or a failed checker aborts
the complete claim. `NATIVE_REPLAY.json` records observed timings and sizes.
The fresh end-to-end publication-checkout replay passed in 487.644 seconds.
Production formulas have 21,822–22,062 clauses; the 348 checked traces total
422,549,573 bytes. Production solver and checker totals are respectively
223.313 and 210.054 seconds, with a maximum solve of 5.253 seconds.
Large traces, formulas, matrices, logs and binaries stay in external scratch
and are regenerated by replay. No Python package, network request, private
data, catalogue download or online ledger is needed by reproduction.

Controls exhaust 32 small formulas and 32,768 assignments, of which 32,243
satisfy their active kernels. A separate physical example checks that an
omitted vertex's forbidden five-set is intentionally absent from the weaker
kernel. Thirty corruptions are rejected, including false local certificates,
invalid matrix inputs, changed upstream bytes, false relabeling, missing
free pairs and constraints on outside edges. Normal and optimized Python
agree. Both C++ programs also pass Clang 17 address/undefined-behavior
sanitizer controls; the global checker has 41 additional complete formula
audits spanning all classes and markings. An empty proof is rejected.

## Imports, trust and remaining frontier

The complete degree-23 equality catalogue is h3455, public commit
`590bcae0fe01e88e0a8fcf8030fbb2524973e4cb`, independently accepted at
h3467. The thirteen-interface census is h3349, public commit
`8bf27902fba404e35593c90cbc7d2991abeda510`, independently accepted at h3355,
in [its source directory](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification).
The current result does not re-enumerate those catalogues or Paley uniqueness.
The local twenty-edge classification alone is catalogue-free.

The cumulative count imports the accepted interface-0 theorem h3469/h3483
and the twelve-edge theorem h3505, canonically accepted at h3519. The latter
[independent review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_consensus_kernel_review2),
commit `dbe13e5508e43099c24ed4e39ee6d9476e4498ab`, checks every preceding
refutation and the complete local/transport statements; it does not review
this new contribution. The star summary imports h3419/h3431. External review
of the present result is pending.

This is author-checked exact computation with independent enumerations,
physical encodings and proof checking. It is not proof-assistant formalization.
Trust remains in the explicit catalogue premises, the displayed coverage and
weaker-system argument, unformalized checkers, language/compiler semantics,
DRAT checking and ordinary hardware. Hashes establish identity.

Primary literature was checked after graph-first selection:
[Angeltveit–McKay](https://arxiv.org/html/2409.15709v2) and
[McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Pointed gluing, partial-template relaxation and independent transversals are
classical. A limited search found no matching exact twenty-edge statement;
historical priority is not claimed.

The cumulative degree-23 bounds on the original dense interfaces are:

| Interface indices | Maximum neighborhood edges | Minimum red deficiency |
|---|---:|---:|
| 0,1,2,10,12 | 115 | 7 |
| 3,4,9,11 | 116 | 6 |
| 6–8 | 114 | 8 |
| 5 | entire degree-23 branch excluded by h3419 | — |

Exactly covered here: all 434 labeled fillings at global hub degree 23
and complete J density 116, including both dense endpoint cohorts. The
other 432 local fillings have H density 102–108; they are a stated partial
family, not all neighborhoods at those densities. All lower J densities,
all lower hub degrees, every retained whole interface and all 1,392 remaining
original equality templates stay open. No remaining key is asserted feasible.
H-star remains frozen. R1's M214 certificate work and r3's hard cut/rank
composition work are separate.

Next falsifiable milestone: a complete decision for another principal-ranked
surviving cohort, or a common partial template covering several of the four
remaining cohorts while keeping every relative marking and free edge.
