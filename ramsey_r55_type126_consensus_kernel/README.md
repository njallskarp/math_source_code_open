# A twelve-edge family closes two dense Ramsey interface cohorts

**Computer-assisted theorem.** The partial 22-vertex neighborhood defined
below has exactly **110 labeled completions** with no red K4 and no blue
K5. They are characterized by independent sets of an explicit 18-edge
conflict graph meeting a prescribed pair. Their edge counts are 104–109.
Every completion has the same unique degree-five hub z.

If any of these neighborhoods occurs as the red neighborhood of a vertex
r in a hypothetical 43-vertex (5,5)-Ramsey graph, and z has global red
degree 23, then

\[
e_R(N_R(z))\le115,\qquad \delta_R(z)=122-e_R(N_R(z))\ge7.
\]

The complete density-116 boundary reduces to **348 partial templates**,
each retaining all twelve local attachment bits, all 272 private-core
cross edges, and all 117 other globally free edges. Every template is
refuted already on its 40-vertex neighborhood union. All 348 DRAT proofs
are checked. The 110 local fillings are classified for interpretation;
they are **not fixed individually** when producing these refutations.

The two 109-edge local fillings are exactly interfaces **10 and 12** of
the previously reviewed thirteen-interface census, after the displayed
relabeling. Consequently all **696** marked equality cases of these two
cohorts are excluded. Together with the prior interface-0 result, **2,088**
of the original 3,132 type-K2,3 equality templates remain undecided, on
interfaces 1–4, 9 and 11. No whole retained degree-23 interface, M-slice,
or Ramsey-number bound is settled.

## Literal partial neighborhood and complete local classification

Graphs are simple; true means red. Use A={0,...,15}, S={16,...,20},
and z=21. The two original graph6 records, at zero-based indices 10 and
12 of the hash-pinned thirteen-record input, are respectively:

```text
Uv?IXZIhlRWjUXL[iphstCjRDY`slYrgyeF[??Bw
Uv?IXZIhlRWjUXL[iphstKMgElTSNYqizDQ{??Bw
```

Map the second record to the first coordinates by the following vertex
permutation, whose entries are the images of 0 through 21:

```text
4 6 7 5 0 3 1 2 8 12 10 15 9 13 14 11 17 16 19 20 18 21
```

Keep every pair on which the two colored graphs agree and leave every
disagreement free. Equivalently, delete these twelve pins from interface
10, in the following variable order:

```text
1:(0,17)  2:(0,19)  3:(1,16)  4:(1,17)
5:(3,19)  6:(6,16)  7:(8,17)  8:(8,19)
9:(11,19)  10:(13,19)  11:(14,19)  12:(15,16)
```

Thus A, S, all incidences of z, and 68 of the 80 A–S pairs are fixed.
In particular N_H(z)=S and H[S] is K2,3. The literal permutation and all
231 pair comparisons are checked; no automorphism search, optimality,
group completeness, or extension to a global automorphism is a premise.

Let X be the subset of the twelve variables assigned red. Define a graph
F on {1,...,12} with edge set

```text
(1,2) (1,7) (2,5) (2,8) (2,9) (3,5) (3,6) (3,8) (3,9)
(4,7) (4,11) (5,10) (5,11) (5,12) (6,12) (7,8) (8,10) (9,11)
```

The same pair arrays are in `LOCAL_CERTIFICATE.json`. The exact characterization is

\[
H\in\mathcal R(4,5;22)
\quad\Longleftrightarrow\quad
X\text{ is independent in }F\text{ and }X\cap\{3,4\}\ne\varnothing.
\]

To check this directly, append a vertex red to all 22 vertices and form
all monochromatic-five prohibitions. Their substituted CNF on the twelve
variables has 25 distinct clauses. Deleting clauses subsumed by others
leaves exactly the eighteen clauses \(\neg x_i\lor\neg x_j\) for
\(ij\in E(F)\), and \(x_3\lor x_4\). The appended-root condition
is precisely no red K4 and no blue K5 in H. This proves both directions.

The constrained independence polynomial is

\[
\sum_{X}t^{|X|}=2t+15t^2+37t^3+38t^4+16t^5+2t^6.
\]

There are 103 already-fixed red pairs in H, so this gives respectively
2, 15, 37, 38, 16 and 2 fillings at edge counts 104 through 109.
Every one has z as its unique degree-five vertex. The two dense fillings
are masks 441 and 3654, with variable i represented by bit i−1; they are
exactly the original two endpoints. These are labeled counts, without an
isomorphism quotient or a classification claim beyond this partial graph.

The complete sorted decimal model stream, one mask per line, has SHA-256
`f886a266f5d70846d52afe5dc79443d38f6b1502cb82eac23d9785dd31ad872a`.
All 4,096 masks are independently checked against literal red-four and
blue-five clique searches, the full CNF, and the conflict description.
The independent C++ five-set auditor reconstructs the local CNF exactly.

## Complete gluing family and transport

Append r=22, T={23,...,39}, B={40,41,42}. Fix r red to H and blue to
T and B; fix z red to T and blue to B. Fix T to Paley-17, with red
differences {1,2,4,8,9,13,15,16}. For the 85 S–T bits use each of the
29 type-126 density-116 representatives in the preceding
[dense-hub classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification),
with each of the twelve isomorphisms of its standard K2,3 onto H[S].
Keep all other pins of the partial H just defined.

There are 502 fixed pairs and **401 free physical pairs**: twelve A–S,
272 A–T, 48 A–B, 15 S–B, 51 T–B, and three within B. Only the first
284 appear in the necessary 40-vertex subsystem. The remaining 117 are
unrestricted. No density quota on H, extra degree profile, outside quota,
auxiliary variable, or unforced physical pin enters a refutation.

Here is why the 348 templates cover the intrinsic branch. Given
H=N_R(r) and d_R(z)=23, z has exactly seventeen outside red neighbors T.
They form a (4,4;17) graph, hence the unique Paley graph by the explicit
imported uniqueness theorem. The other three outside vertices form B.
In J=G[N_R(z)], r has exactly the five neighbors S, which induce K2,3.
The imported complete local theorem gives e(J)≤116 and exactly 29
isomorphism classes at equality, with the distinguished hub unique.

An isomorphism to a representative fixes that hub, maps its five
neighbors to S, and labels T as the displayed Paley graph. All twelve
relative S markings are enumerated. Relabeling T also relabels arbitrary
A–T and B–T edges. There is no assumption that it is an automorphism
of G, and no markings are discarded using an automorphism of H.
Thus every equality instance is represented, for every local filling.
Excluding equality and importing the ceiling 116 gives the bound 115.
The deficiency notation additionally imports U(23)=122.

For the original two dense cohorts, `audit.py` independently constructs
all 696 physical matrices. Extend the displayed permutation by fixing
r, T and B, and transport each of the twelve H12 markings to an H10
marking. Each target key has exactly two original preimages. All
**628,488** physical pair transports are checked: each target fixed bit
is implied by the original, and every original free pair remains free.
The 348 target matrices are distinct. The 110×29×12=38,280 labeled
pointed local pairings are therefore covered by the same 348 relaxed
systems; this is a coverage count, not a count of realizable graphs.

## Exact refutations and independent implementations

Variables 1 through 401 number every unfixed pair of the full 43-vertex
template in lexicographic pair order. For every five-set in vertices
0 through 39, include both monochromatic prohibitions after substituting
fixed colors; discard already-satisfied clauses and deduplicate.
This is exactly the absence of a monochromatic K5 in that induced union.
Every full Ramsey completion would satisfy this weaker system.

The encoder, literal auditor and small-control scaffolding are adapted
from the cited h3469 interface-0 package. The new partial template, complete
transport and local classification are checked here.

`consumer.py` decodes graph6 as bit strings and recursively grows
compatible five-cliques. The producer-free `audit.py` uses integer
bit positions, literal S permutations and an independent physical matrix.
The matrices agree on all 903 pairs for all 348 cases. `audit_cnf.cpp`
then reads those independent matrices and directly visits all
\(\binom{40}{5}=658008\) five-sets using nested index loops.
Every independently generated CNF agrees byte for byte with the producer,
giving 228,986,784 literal five-set checks. Exact support checks establish
that all 284 kernel variables occur and none of the 117 outside variables
occurs. These checks concern the full family, not a formula sample.

Kissat returns UNSAT on every case; drat-trim checks every refutation with
exit zero and `s VERIFIED`. Solver status or hashes alone receive no
proof credit. `MANIFEST.json` fixes every key, physical matrix hash,
formula hash, variable count and clause count. Missing keys, timeouts,
UNKNOWN, mismatches or failed proof checking stop reproduction.

Complete formula/matrix manifest SHA-256:
`263fc40472bcf4e4950452ce8bc1e3ad9207c121bd7ed2d489c6656f6e48bb00`.
Complete marked-template stream SHA-256:
`cc604bc250243288b5f4002c30f8b2315b885d6204f1064f28aa079681e2e528`.

## Reproduce and trust boundary

From a full checkout of this repository, with Python 3.10+, a C++20
compiler, Kissat and drat-trim, choose a new scratch directory outside
the source checkout:

```sh
python3 -B ramsey_r55_type126_consensus_kernel/reproduce.py /tmp/fresh-r55-consensus --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected final status:
`VERIFIED_COMPLETE_CONSENSUS_FAMILY_AND_TWO_COHORT_EXCLUSION`.
The command compiles the independent auditor, checks the complete local
classification and transport cover, runs controls, regenerates both
encodings, solves and proof-checks all 348 cases, and compares the public
manifest and expected output. Native proofs are mandatory. The adjacent
preceding classification supplies two hash-pinned JSON files; its source
code is not imported. Its mathematical completeness is a stated premise,
not inferred from the presence of 29 records.

Production uses CPython 3.12, GCC 16.2, Kissat 4.0.4 and drat-trim at the
exact source commits in `NATIVE_REPLAY.json`. Native primary sources are
[Kissat](https://github.com/arminbiere/kissat) and
[drat-trim](https://github.com/marijnheule/drat-trim). After checking out
the recorded versions, their ordinary builds are `./configure && make`
and `make`. The per-case solver cap is 30 seconds. Generated formulas,
proofs, matrices, logs and binaries remain in external scratch and are
regenerated by replay. No Python package, private input, online database,
network access or catalogue download is required by reproduction.

A fresh end-to-end replay completed in **370.890 seconds**, matching
every expected output and the complete manifest and checking every newly
generated refutation. Production used 145.889 seconds of solver time and
146.870 seconds of checker time; its largest solve was 1.030 seconds.
Each formula has 20,804–20,972 clauses. The observed DRAT traces total
238,785,368 bytes and are omitted from the compact publication.

Definition-level controls exhaust 32 small formulas and 32,768 assignments,
of which 32,243 satisfy their active kernels. A separate example checks
that a forbidden five-set using an omitted vertex is intentionally absent
from the weaker formula. Twenty-four corruptions are rejected, including
invalid keys, changed input bytes, missing variables, constraints on outside
edges, a false permutation, a missing free edge and false local certificates.
Normal and optimized Python agree. Clang 17 address/undefined-behavior
sanitizer checks cover the controls and 41 complete formulas spanning all
29 representatives and all twelve markings. An empty proof is rejected.

The literal local theorem needs no external catalogue. The complete
intrinsic degree-23 application imports the reviewed 29-class theorem
and its Paley-17 uniqueness premise. Applying the dense-interface labels
to the complete thirteen-interface branch imports that earlier census.
Deficiency language imports U(23)=122. Trust otherwise lies in the
displayed transport and weaker-system argument, independent but unformalized
checkers, compiler/language semantics, DRAT checking and ordinary hardware.
This is an author-checked result; external review of the new theorem is
pending, and no proof-assistant formalization is claimed.

## Imports, novelty and residual cases

The complete dense degree-23 classification is Discovery Net h3455,
`bafkreib32yjgeg6rdrmz7y5wo3csmanuuy234kr3aakm2363pqd3hn7oke`,
public commit `590bcae0fe01e88e0a8fcf8030fbb2524973e4cb`.
Its independent acceptance h3467 includes a third complete tuple census
and all preceding type-62 proof replays, in
[the review evidence](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_dense_degree23_hub_classification_review1),
commit `45974c3a81bde6c273fa2ebd02614cb74ff86b82`.

The thirteen-interface census is h3349, public commit
`8bf27902fba404e35593c90cbc7d2991abeda510`, in
[its source directory](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification).
The cumulative remaining count also imports the accepted h3469
[interface-0 exclusion](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_interface0_kernel),
commit `ccc1580ba01738757795afa24f74e55af05f2aff`.
That result was independently accepted at h3483 in
[review source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_interface0_review1),
commit `34dc816dd9150329f31512fac01abd93884e5625`.
These acceptances do not review the present result.

Primary literature was checked after graph-first selection:
[Angeltveit–McKay's pointed-gluing work](https://arxiv.org/html/2409.15709v2)
and [McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Pointed gluing, local relabeling, partial-template relaxation and conflict
graphs are classical. A limited search found no matching exact twelve-bit
classification and two-cohort statement; historical priority is not claimed.

At global hub degree 23 the cumulative dense-interface bounds are:

| Interface indices | Maximum neighborhood edges | Minimum red deficiency |
|---|---:|---:|
| 0, 10, 12 | 115 | 7 |
| 1–4, 9, 11 | 116 | 6 |
| 6–8 | 114 | 8 |
| 5 | entire degree-23 branch excluded by h3419 | — |

The exact new covered family is the 110 labeled partial-H fillings with
hub degree 23 at the complete J density-116 boundary, including both
original dense cohorts. Lower J densities remain open. All lower global
hub-degree branches remain, as do every other lower-density local family
and the 2,088 remaining original equality templates. H-star is frozen.
Researcher 1's M214 roots and researcher 3's M216 central-cap work are
separate; no global certificate or whole-profile closure is claimed here.

Next falsifiable milestone: a complete checked decision for interface 1,
the latest principal default, or a common partial template that covers several
remaining cohorts with all relative markings and free physical edges
retained. The displayed twelve-edge map is not claimed optimal.
