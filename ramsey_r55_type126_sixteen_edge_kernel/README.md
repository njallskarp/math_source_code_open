# A sixteen-edge Ramsey family with essential triple obstructions

**Computer-assisted theorem.** The partial 22-vertex graph below has exactly
181 labeled completions in \(\mathcal R(4,5;22)\). They are exactly the
independent sets of a displayed hypergraph that meet three specified pairs.
Twenty forbidden pairs and three forbidden triples are needed; each triple
has an explicit witness showing that it cannot be omitted. Every valid
completion has the same unique degree-five vertex z and induces K2,3 on
its five neighbors. The densities are 104 through 109. The two dense
completions are precisely the original interfaces 3 and 4.

If any such H occurs as \(N_R(r)\) in a hypothetical 43-vertex (5,5)-Ramsey
graph, and \(d_R(z)=23\), then

\[
e_R(N_R(z))\le115,\qquad \delta_R(z)=122-e_R(N_R(z))\ge7.
\]

The complete density-116 boundary is covered by 348 partial templates,
each refuted on its 40-vertex neighborhood union with all **405 free
physical edges** retained. Exactly 288 variables occur in the necessary
kernel; 117 outside edges are arbitrary. The sixteen local bits stay free
in every refutation. This excludes all **696 original marked cases** of
interfaces 3 and 4. The intrinsic application has explicit catalogue and
Paley-17 uniqueness imports; the literal local classification has none.

## Exact local characterization

Red edges are graph edges. Set A={0,...,15}, S={16,...,20}, z=21. Start
with zero-based interface 3 of the thirteen-record input:

```text
UsHHirKdlp[IFVI|KpqfROjqDXf}?XVgzsB[??Bw
```

Leave exactly these sixteen pairs free, in local variable order:

```text
1:(0,17)   2:(2,17)   3:(2,19)   4:(3,19)
5:(5,17)   6:(5,19)   7:(6,19)   8:(8,17)
9:(8,19)  10:(10,17) 11:(10,19) 12:(12,17)
13:(13,17) 14:(14,19) 15:(15,17) 16:(15,19)
```

All other colors are fixed. These are exactly the disagreements with
interface 4 after the following involution, written as the images of
vertices 0 through 21:

```text
3 7 6 0 5 4 2 1 12 10 9 15 8 14 13 11 17 16 18 20 19 21
```

It preserves A, S and z. Every physical pair is compared, including fixed
colors within A and S. This is one explicit relabeling, with no claim of
optimality, complete automorphism-group enumeration, or extension to a
global automorphism. Exactly 64 of the 80 A–S colors remain fixed.

Let X be the red local positions, a subset of {1,...,16}. Forbid inclusion
of each of these twenty pairs:

```text
{1,2} {1,8} {2,10} {2,13} {3,11} {3,14} {4,7} {4,16}
{5,6} {5,8} {5,12} {6,7} {6,9} {8,9} {8,13} {9,11}
{10,12} {10,15} {13,15} {15,16}
```

Also forbid inclusion of these three triples:

```text
{7,14,16} {10,11,14} {11,14,16}
```

Require X to meet all three pairs:

```text
{1,15} {2,5} {9,14}
```

These 26 conditions are **equivalent** to
\(H\in\mathcal R(4,5;22)\). For a direct finite proof, append a universal
red root to H and substitute fixed colors into every monochromatic-five
prohibition. This gives 49 distinct clauses. Subsumption leaves exactly
the 23 negative clauses and three positive clauses displayed above.
The universal-root construction is equivalent to absence of a red K4
and a blue K5 in H. Both full encodings and the subsumption identity are
checked; no density constraint is imposed.

The constrained independence polynomial is

\[
6t^3+35t^4+69t^5+54t^6+15t^7+2t^8.
\]

There are 101 fixed red edges. Thus the counts at densities 104 through
109 are 6,35,69,54,15,2. All 181 fillings have z as their unique degree-five
vertex. The two dense masks, encoding position i by bit i−1, are 27818
and 37717. They are exactly the two input endpoints after the displayed
relabeling. Counts are labeled; no isomorphism quotient is used.

`local_classification.py` uses include/exclude recursion. A branch is
pruned only if it already contains a forbidden hyperedge, or a meeting
pair cannot be hit even using all available positions. This is exhaustive
by the include/exclude dichotomy at each next position.
`audit_local.cpp` instead reads only the literal 22-vertex matrix,
enumerates its physical red-four and blue-five subsets, and checks **all
65,536 assignments**. It imports no producer, CNF, or hypergraph. The
complete sorted model streams agree byte for byte. A separate Python
clique search checks every surviving physical graph and its unique hub.

The stream of sorted decimal masks, one per line, has SHA-256
`5c5f82175ea41fd9b54aa3d31a39597f415890eada945192c6b011500ad954f9`.
`LOCAL_CERTIFICATE.json` supplies every condition, all 181 models, density
counts and the following witnesses.

## Why pair constraints alone fail

The twenty forbidden pairs and three meeting requirements admit 203
assignments. The forbidden triples reduce this to 181. Pair-only recursive
enumeration is independently compared with a set-based scan of all 65,536
subsets; this auxiliary count is separate from the literal Ramsey census.

Each triple is independently necessary even after retaining the other two:

| Omitted triple | Red positions X | A physical red K4 |
|---|---|---|
| {7,14,16} | {1,5,7,14,16} | {6,14,15,19} |
| {10,11,14} | {1,5,10,11,14} | {10,14,17,19} |
| {11,14,16} | {1,5,11,14,16} | {10,14,15,19} |

Set all other local positions blue and retain the original fixed colors.
Each row satisfies all other 25 minimal conditions, yet the four physical
vertices displayed have all six edges red. The witness masks are 41041,
9745 and 42001, respectively. Their five red positions are minimum: each
omitted triple is disjoint from both meeting pairs {1,15} and {2,5},
requiring two further positions. Enumeration also checks the selected
minimum masks and all single-triple exception counts, respectively 8,6,2.

The first and third triples are red stars at vertex 19 over fixed red
triangles {6,14,15} and {10,14,15} in A. For the middle triple, the
three fixed red edges are (10,14), (14,17), and (17,19); its variable
edges (10,17), (10,19), and (14,19) complete the four-set
{10,14,17,19}. Thus each condition comes from a specific physical K4
whose other three edges are fixed red.

This falsifies the particular rule obtained by keeping only this family's
minimal pair prohibitions and meeting pairs. It does not prove that every
possible alternative graph encoding fails. The missing conditions here
are precisely the three displayed triple obstructions.

## Complete intrinsic gluing and physical transport

Append r=22, T={23,...,39} and B={40,41,42}. Fix r red to H and blue to
T and B. Fix z red to T and blue to B. Fix T to Paley-17, with red
differences {1,2,4,8,9,13,15,16}. For the 85 S–T colors use each of the
29 type-126 density-116 representatives of the reviewed
[dense-hub classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification),
retaining all twelve relative K2,3 markings.

There are 498 fixed and 405 free pairs among the 903 physical pairs:
sixteen A–S, 272 A–T, 48 A–B, 15 S–B, 51 T–B, and three within B.
The first 288 belong to the 40-vertex union. No outside quota, extra degree
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

Thus all 348 partial templates cover every one of the 181 local fillings
at equality. They cover 181×29×12=62,988 labeled pointed local pairings;
this is a coverage count, not a realizable-graph count.

For the two dense endpoints, `audit.py` independently builds all 696
original full physical matrices and transports each through the identity
or the displayed involution. Every target key has exactly two preimages.
All 628,488 pair transports are checked: every target fixed bit is implied,
and every formerly free pair remains free. The 348 target matrices are
distinct. No symmetry quotient of the global graph is assumed.

## Necessary kernels and checked refutations

Number all 405 free physical pairs in lexicographic order. For each
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
five-set checks. The support audit verifies that exactly the 288 union
variables occur and that no outside variable occurs.

Kissat gives UNSAT for every case and drat-trim accepts every generated
refutation. This excludes the complete equality boundary. The imported
ceiling 116 then gives 115; the separate U(23)=122 import yields deficiency
at least seven. Solver status or hashes alone are not a proof premise.

`MANIFEST.json` records every key, matrix hash, CNF hash, variable count and
clause count. Missing or undecided keys fail reproduction. The complete
manifest SHA-256 is `31a12430849216fbf8673dd820f688d0a6008d3d6e88898299a33989d3fc77f3`.
The marked-template stream SHA-256 is
`2edb1da04cd2101cabd288a9d2d93e85a72809071169a1798333454f783e7f1d`.

## Reproduction and validation

From a full checkout, with Python 3.10+, C++20, Kissat and drat-trim,
choose a new scratch directory outside the source checkout:

```sh
python3 -B ramsey_r55_type126_sixteen_edge_kernel/reproduce.py /tmp/fresh-r55-sixteen --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected status:
`VERIFIED_COMPLETE_SIXTEEN_EDGE_FAMILY_AND_TWO_COHORT_EXCLUSION`.
The command compiles both C++ checkers, runs complete local and transport
checks and controls, regenerates both encodings for every template, solves
all 348 systems, checks every DRAT proof, and compares expected outputs
and the full manifest. Both native proof tools are required. Two hash-pinned
JSON files from the adjacent dense-hub directory supply the imported data;
its implementation is not imported. Catalogue completeness remains an
explicit theorem premise, not an inference from the presence of records.

Production uses CPython 3.12, GCC 16.2, Kissat 4.0.4 at
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim at
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Native sources:
[Kissat](https://github.com/arminbiere/kissat) and
[drat-trim](https://github.com/marijnheule/drat-trim).
After checking out the stated versions, ordinary builds are
`./configure && make` and `make`, respectively. Each solve has a 30-second
internal cap and 45-second external deadline; proof checking has a
120-second external deadline. UNKNOWN aborts the complete claim.

The fresh end-to-end publication-checkout replay passed in 484.764 seconds,
regenerating and checking all 348 proofs and comparing every expected output
and manifest entry. Production clause counts are 21,279–21,566; its traces
total 393,307,542 bytes. Solver and checker time totals are 208.678 and
196.450 seconds, with a maximum solve of 3.873 seconds. Native versions,
limits and observed resource costs are recorded in `NATIVE_REPLAY.json`.

Controls exhaust 32 small formulas and 32,768 assignments, with 32,243
satisfying assignments. A literal example checks the omitted-vertex
relaxation. Thirty-three corruptions are rejected, including changed
imports, marking maps, outside-edge support, local clauses, models and
triple-necessity witnesses. Normal and optimized Python outputs agree.
Both C++ programs pass Clang 17 address/undefined-behavior sanitizer controls;
41 additional distinct global formula audits span all 29 classes and all
twelve markings. An empty proof is rejected. All local bit arithmetic fits
within sixteen-bit masks stored in unsigned 32-bit integers.

Large formulas, matrices, traces, binaries, logs and exploratory scripts
remain in external scratch. Replay regenerates them; no network, private
data, online ledger, extra Python package or catalogue download is needed.

## Provenance, trust and remaining scope

The complete J catalogue is h3455, independently accepted at h3467.
The thirteen-interface census is h3349, independently accepted at h3355;
its [source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification)
supplies the original dense-family interpretation. Paley-17 uniqueness
and catalogue completeness are imported, not re-enumerated here.
U(23)=122 is h2099. The local sixteen-edge theorem is catalogue-free.

The encoder and transport scaffold adapt the previous
[twenty-edge package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_twenty_edge_kernel),
h3537. Its predecessor, the
[twelve-edge package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_consensus_kernel),
h3505, was independently accepted at h3519. The present hypergraph theorem,
essential-triple witnesses and every refutation are newly checked. No old
trace is substituted. Existing reviews do not review this new result.

This is author-checked exact computation with different enumerations,
physical encodings and proof checking. External review is pending.
Trust remains in the stated imports, coverage and weaker-system argument,
unformalized checkers, language/compiler semantics, DRAT checking and
ordinary hardware. Hashes establish identity. This is not proof-assistant
formalization or a claim that publication itself proves the theorem.

Primary literature was checked after graph-first selection:
[Angeltveit–McKay](https://arxiv.org/html/2409.15709v2) and
[McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Pointed gluing, partial-template relaxation and forbidden-hypergraph
descriptions are classical. A limited search found no matching exact
sixteen-edge statement; no historical priority is claimed.

With earlier h3469, h3505 and h3537 exclusions, 2,436 of the original
3,132 type-126 equality markings are excluded. Exactly **696** remain
on interfaces **9 and 11**. This cumulative count imports those earlier
consumers; h3469 and h3505 have external acceptances h3483 and h3519,
while h3537 has author validation and awaits review at this pass's wake.

| Interface indices | Maximum J edges at global hub degree 23 | Minimum deficiency |
|---|---:|---:|
| 0,1,2,3,4,10,12 | 115 | 7 |
| 9,11 | 116 | 6 |
| 6–8 | 114 | 8 |
| 5 | entire degree-23 branch excluded by h3419/h3431 | — |

Exactly covered here: all 181 local fillings at global hub degree 23 and
complete J density 116, including both dense endpoint cohorts. The other
179 fillings have H densities 104–108 within this stated family; they are
not all neighborhoods at those densities. All lower J densities, lower
hub degrees, retained whole degree-23 interfaces, full M-slices and the
Ramsey target remain open. No remaining key is asserted feasible.

H-star remains frozen. R1's anchor-linked M214 relaxation and r3's
vertex-connectivity/rank composition remain separate. The next falsifiable
milestone is a complete remaining interface-9 or interface-11 cohort
decision, or a complete shared partial family with all markings retained,
after fresh graph and principal inspection. Equality exhaustion or the
two-unchanged-pass gate moves to a complete next-density family plus a
consumer, rather than an unconsumed census.
