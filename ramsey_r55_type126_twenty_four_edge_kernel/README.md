# A complete 24-edge family excluding the interface-11 equality boundary

**Computer-assisted theorem.** The partial 22-vertex graph below has exactly
995 labeled completions in \(\mathcal R(4,5;22)\). They are exactly the
independent sets of a displayed 30-edge conflict graph meeting ten specified
sets. Every completion has the same unique degree-five vertex z and induces
K2,3 on its five neighbors. The densities are 102 through 109; the two
109-edge completions are the original interfaces 10 and 11.

If any such H occurs as \(N_R(r)\) in a hypothetical 43-vertex (5,5)-Ramsey
graph, and \(d_R(z)=23\), then

\[
e_R(N_R(z))\le115,\qquad \delta_R(z)=122-e_R(N_R(z))\ge7.
\]

The complete density-116 boundary is covered by 348 partial templates,
each refuted on its 40-vertex neighborhood union with all **413 free
physical edges** retained. Exactly 296 variables occur in the necessary
kernel; 117 outside edges are arbitrary. All 24 local bits stay free
throughout. The endpoint transport covers 696 marked cases, but precisely
**348 exclusions are new**, all of interface 11. Interface 10 was already
excluded by the earlier twelve-edge family. The intrinsic application
imports the stated catalogues and Paley-17 uniqueness; the literal local
classification has no catalogue-completeness premise.

## Exact local characterization

Red edges are graph edges. Set A={0,...,15}, S={16,...,20}, z=21. Start
with zero-based interface 10 in the thirteen-record input:

```text
Uv?IXZIhlRWjUXL[iphstCjRDY`slYrgyeF[??Bw
```

Leave exactly these 24 pairs free, in local variable order:

```text
1:(0,16)   2:(1,17)   3:(1,18)   4:(1,19)
5:(1,20)   6:(3,17)   7:(3,19)   8:(4,16)
9:(4,17)  10:(4,19)  11:(5,16)  12:(6,16)
13:(7,17) 14:(7,18) 15:(7,19) 16:(7,20)
17:(10,16) 18:(10,19) 19:(11,20) 20:(12,18)
21:(12,19) 22:(13,20) 23:(14,18) 24:(15,16)
```

All other colors are fixed. These are exactly the disagreements with
interface 11 after swapping 16 with 17 and 19 with 20, fixing every other
vertex. The complete second-to-first map is

```text
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 16 18 20 19 21
```

It preserves A, S and z. Every physical pair is compared, including
colors within A and S. This is one explicit relabeling; no optimality,
automorphism-group completeness or global automorphism is assumed.
Exactly 56 of the 80 A–S colors remain fixed.

Let X be the red local positions, a subset of {1,...,24}. Forbid inclusion
of each of these thirty pairs:

```text
{1,17} {1,19} {2,5} {2,6} {3,20} {3,23}
{4,21} {5,19} {6,20} {6,23} {7,21} {7,24}
{8,10} {8,12} {8,17} {9,13} {9,20} {10,18}
{10,21} {11,12} {11,19} {11,22} {12,24} {13,16}
{14,20} {15,18} {15,21} {16,19} {16,22} {17,18}
```

Require X to meet each of these ten sets:

```text
{2,8,9} {2,13,24} {3,4,5,14,15,16} {3,4,18} {3,5,22}
{4,5,10,22} {14,15,23} {14,16,23} {18,22} {20,21}
```

These forty conditions are **equivalent** to
\(H\in\mathcal R(4,5;22)\). Append a universal red root to H and
substitute fixed colors into every monochromatic-five prohibition. The
75 distinct clauses reduce by subsumption to exactly the thirty negative
pairs and ten positive clauses displayed above. The universal-root
construction is equivalent to absence of a red K4 and a blue K5 in H.
Both full encodings and this subsumption identity are checked. No density
constraint is imposed; no claim of logically minimum CNF size is made.

The constrained independence polynomial is

\[
3t^5+44t^6+190t^7+343t^8+284t^9+109t^{10}+20t^{11}+2t^{12}.
\]

There are 97 fixed red edges. Thus densities 102 through 109 have counts
3,44,190,343,284,109,20,2. All 995 fillings have z as their unique
degree-five vertex. The two dense masks, encoding position i by bit i−1,
are 7166538 and 9610677. They are exactly the two endpoints after the
relabeling. Counts are labeled; no isomorphism quotient is used.

`local_classification.py` uses include/exclude recursion, pruning only
when a forbidden pair is contained or a required set cannot be hit using
the remaining positions. This is exhaustive by the include/exclude
dichotomy. `audit_local.cpp` reads only the physical 22-vertex matrix,
enumerates its literal red-four and blue-five subsets, and checks **all
16,777,216 assignments**. It imports no producer, CNF, conflict graph or
meeting sets. The complete sorted model streams agree byte for byte.
A separate Python clique search checks every surviving graph and its hub.

The sorted decimal mask stream, one mask per line, has SHA-256
`272dc97a9946ae31e6e032511e0af7c621bd526fc351c3cc620db776151dfe54`.
`LOCAL_CERTIFICATE.json` supplies the conditions, all 995 models, and density
counts. The 993 fillings below density 109 belong to this explicitly fixed
partial family; they are not a census of every lower-density neighborhood.

## Complete intrinsic gluing and physical transport

Append r=22, T={23,...,39} and B={40,41,42}. Fix r red to H and blue to
T and B. Fix z red to T and blue to B. Fix T to Paley-17, with red
differences {1,2,4,8,9,13,15,16}. For the 85 S–T colors use each of the
29 type-126 density-116 representatives of the reviewed
[dense-hub classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification),
retaining all twelve relative K2,3 markings.

There are 490 fixed and 413 free pairs among the 903 physical pairs:
twenty-four A–S, 272 A–T, 48 A–B, 15 S–B, 51 T–B, and three within B.
The first 296 belong to the 40-vertex union. No outside quota, extra degree
profile, H-density condition or auxiliary variable is used. Every original
free pair remains free.

To establish intrinsic completeness, suppose H=N_R(r) and d_R(z)=23.
Exactly seventeen red neighbors of z lie outside H and r. They have no
red K4 (adjoin z) or blue K4 (adjoin r), so form a (4,4;17) graph.
The explicit uniqueness import makes this Paley-17. In J=G[N_R(z)], the
root r has precisely the five neighbors S, inducing K2,3. The imported
h3455 theorem gives e(J)≤116 and exactly 29 equality representatives,
each with a unique degree-five hub. An isomorphism sends that hub to r,
its five neighbors to S, and its seventeen nonneighbors to T. All twelve
relative S markings are retained. Relabeling T transports arbitrary free
incidences; it need not extend to an automorphism of the full graph.

Thus all 348 partial templates cover every one of the 995 local fillings
at equality. They cover 995×29×12=346,260 labeled pointed local pairings;
this is a coverage count, not a realizable-graph count.

For the two dense endpoints, `audit.py` independently builds all 696
original full physical matrices and transports each through the identity
or the displayed involution. Every target key has exactly two preimages.
All 628,488 pair transports are checked: every target fixed bit is implied,
and every formerly free pair remains free. The 348 target matrices are
distinct. No symmetry quotient of the global graph is assumed.

## Necessary kernels and checked refutations

Number all 413 free physical pairs in lexicographic order. For each
five-set on vertices 0 through 39, forbid both monochromatic colors after
substituting fixed bits; discard satisfied clauses and deduplicate. These
are precisely the monochromatic-five prohibitions on the 40-vertex union.
Every full Ramsey completion satisfies this necessary system; the 117
outside variables are unrestricted.

The producer uses bit-string graph6 decoding and recursive compatible-clique
growth. The independent audit uses integer graph6 decoding and literal
physical marking tests. The separate C++ encoder reads those independent
matrices and loops directly over every five-set. All 348 physical matrices
and all 348 full CNFs agree byte for byte, covering 228,986,784 direct
five-set checks. The support audit verifies that exactly the 296 union
variables occur and that no outside variable occurs.

Kissat gives UNSAT for every case and drat-trim accepts every generated
refutation. This excludes the complete equality boundary. The imported
ceiling 116 then gives 115; the separate U(23)=122 import yields deficiency
at least seven. Solver status or hashes alone are not a proof premise.

`MANIFEST.json` records every key, matrix hash, CNF hash, variable count and
clause count. Missing or undecided keys fail reproduction. The complete
manifest SHA-256 is `42e4692b75d87d3a34345238da60502d77c1b62b6ce20699473ff4e24f9c0a00`.
The marked-template stream SHA-256 is
`150825996e25f472914c89da7fb467ad44e49345597f51455580082e368216f4`.

## Reproduction and validation

From a full checkout, with Python 3.10+, C++20, Kissat and drat-trim, choose
a new scratch directory outside the source checkout:

```sh
python3 -B ramsey_r55_type126_twenty_four_edge_kernel/reproduce.py /tmp/fresh-r55-twenty-four --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected status:
`VERIFIED_COMPLETE_TWENTY_FOUR_EDGE_FAMILY_AND_TWO_COHORT_EXCLUSION`.
The two-cohort status names the endpoint coverage; only interface 11 is a
new exclusion. The command compiles both C++ checkers, runs the complete
local classification, transport and controls, regenerates both encodings
for every template, solves all 348 systems, checks every DRAT proof, and
compares every expected output and the full manifest. Both native proof
tools are required. Only two hash-pinned JSON files from the adjacent
`ramsey_r55_dense_degree23_hub_classification` supply imported data; no
upstream implementation is imported. Catalogue completeness is a theorem
premise, not an inference from the presence of records.

Production uses CPython 3.12, GCC 16.2, Kissat 4.0.4 at
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim at
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Native sources:
[Kissat](https://github.com/arminbiere/kissat) and
[drat-trim](https://github.com/marijnheule/drat-trim).
After checking out these versions, ordinary builds are `./configure && make`
and `make`, respectively. Each solve has a 30-second internal cap and a
45-second external deadline; each proof check has a 120-second deadline.
UNKNOWN aborts the complete claim. Proofs and diagnostic logs are regenerated
in external scratch; they are omitted from the compact public package.

The fresh end-to-end publication-checkout replay passed in 1588.305 seconds,
regenerating and checking all 348 proofs and matching every expected output
and manifest entry. Production clause counts are 22,408–22,604; its traces
total 1,628,429,698 bytes. Solver and checker wall-time totals
are 819.785 and 696.515 seconds;
the maximum solve took 15.788 seconds. The two complete
runs used separate scratch directories and overlapped in wall time.
Their per-case proof hashes also agree. Native versions, limits and observed
costs are in `NATIVE_REPLAY.json`.

Controls exhaust 32 small formulas and 32,768 assignments, with 32,243
satisfying assignments. A literal example checks the omitted-vertex
relaxation. Thirty corruptions are rejected, including changed imports,
marking maps, outside support, local clauses and model certificates.
Normal and optimized Python outputs agree byte for byte with Clang 17
address/undefined-behavior sanitizer controls. An empty proof is rejected.
The local masks fit within unsigned 32-bit integers. README edge positions,
relabeling and all forty conditions are checked against the certificate.


## Imported theorems, novelty and remaining cases

The intrinsic theorem imports the complete pointed type-126 census and
Paley-17 uniqueness from the
[dense-hub classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification),
commit `590bcae0fe01e88e0a8fcf8030fbb2524973e4cb`, independently accepted
at graph height 3467. Its type-126 ceiling is 116 with exactly 29 equality
representatives; the higher-level interpretation uses all relative markings.
The two data pins checked by `audit.py` are

```text
inputs.json       8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2
certificate.json  f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02
```

The complete thirteen dense degree-five neighborhoods are from the
[degree-five classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification),
commit `8bf27902fba404e35593c90cbc7d2991abeda510`, accepted at height 3355.
For deficiency notation only, the neighborhood maximum U(23)=122 is a
separate imported extremum. Neither imported catalogue is regenerated here.
The literal partial-family and fixed-template claims require only the
specified physical graphs and encodings; their intrinsic Ramsey application
requires the stated completeness imports.

This package extends the same necessary-kernel proof framework used in the
[interface-0 kernel](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_interface0_kernel),
[twelve-edge family](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_consensus_kernel),
[twenty-edge family](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_twenty_edge_kernel), and
[sixteen-edge family](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_sixteen_edge_kernel).
The twelve-edge result already excludes interface 10. Its acceptance at
height 3519 checks all physical matrices and DRAT proofs, with twelve
independent clause audits and three LRAT checks; it does not provide a
complete independent clause replay of that earlier package. Here the
author's two clause implementations agree on every one of the 348 cases.
External review of this new result is not claimed.

After this result the cumulative original type-126 equality coverage is
**2784 of 3132 keys**, on interfaces 0,1,2,3,4,10,11,12. Only interface 9
remains at density 116, with 348 markings. Interface 5's degree-23 branch
was already excluded entirely. Interfaces 6,7,8 have density at most 114;
all other surviving degree-23 branches and lower densities/degrees remain
open. Raising the second hub's deficiency does not exclude the original
dense neighborhood or an entire M-slice.

Graph-first selection used the full committed root neighborhood through
height 3574. Subsequent primary-literature checks place this in the classical
pointed-neighborhood gluing framework of Angeltveit–McKay
([2018](https://arxiv.org/abs/1703.08768),
[2025 version](https://arxiv.org/html/2409.15709v2)). Their 2025 paper's
main density-22 catalogue starts at 113 edges; this fixed family lies at
102–109 edges. That distinction does not establish historical priority.
The [formal proof of R(4,5)=25](https://arxiv.org/abs/2404.01761) is relevant
context for checked gluing, not a formal verification of this package.
The potential novelty is this exact 995-member family and its complete
marked consumer; no novelty is claimed for gluing, SAT, DRAT or the general
conflict-graph reduction. Limited searches found no matching published
family theorem and do not prove priority.

Remaining trust includes the specified imported completeness results,
the finite mathematical reductions, two unformalized implementations by
the same author, the DRAT checker, compiler/interpreter semantics and
ordinary hardware. Solver status and hashes alone do not establish
infeasibility. This is reproducible computer-assisted evidence, not a
proof-assistant theorem. It changes no Ramsey-number bound.
