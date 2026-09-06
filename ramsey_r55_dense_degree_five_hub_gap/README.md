# A uniform deficiency gap at dense degree-five neighborhoods

**Computer-assisted theorem.** Let G be a hypothetical 43-vertex graph with
neither a clique nor an independent set of order five. Suppose H is the red
neighborhood of a vertex r, H has 22 vertices and at least 109 red edges,
and z has degree five inside H. Then z has global red degree at most 23.
If its global red degree is 23, then

\[
e_R(N_R(z))\le115,\qquad \delta_R(z)=122-e_R(N_R(z))\ge7.
\]

This covers the **complete thirteen** dense degree-five neighborhood types.
For the three types whose five-vertex hub neighborhood is \(K_{2,3}-e\),
the stronger bound is 114 edges and deficiency at least eight. The star type
cannot have global hub degree 23 at all. Color reversal gives the same theorem
in blue.

An equivalent intrinsic edge obstruction is useful without catalogue labels.
For any red edge rz with degrees 22 and 23, respectively, and exactly five
common red neighbors,

\[
\delta_R(r)\ge6\quad\text{or}\quad\delta_R(z)\ge7,
\]

where \(\delta_R(r)=114-e_R(N_R(r))\). In particular, both endpoints cannot
simultaneously have deficiencies at most five and six, respectively. This is
a disjunction, not a bound on the sum of deficiencies.

The new finite step excludes every one of the **348 remaining interface-9
boundary cases**, keeping all **389** unfixed physical pairs free. Combined
with the explicitly imported exclusions below, all **3,132** marked type-
\(K_{2,3}\) density-116 cases are now closed. This is a conditional local
structural theorem. The lower-density degree-23 branches, lower hub degrees,
and the unrestricted order-43 Ramsey family remain undecided. No new bound
on R(5,5), whole degree-profile exclusion, or surviving Ramsey graph is claimed.

## Structural proof and complete coverage

Write \(S=N_H(z)\), so \(|S|=5\). The complete
[thirteen-interface theorem](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification)
forces \(e(H)=109\), a unique degree-five hub, and one of thirteen canonical
records. This is an imported classification theorem, not a completeness
conclusion drawn from a list of thirteen examples. Its construction imports
the complete two-graph catalogue of \(\mathcal R(4,4;16)\).

Every outside vertex red-adjacent to z is blue-adjacent to r. Those vertices
induce a graph with neither a red nor a blue four-clique. Since R(4,4)=18,
there are at most seventeen. Together with r and S, this proves
\(d_R(z)\le6+17=23\). At equality, let T be those seventeen vertices and B
the other three outside vertices. Order-17 uniqueness identifies T with the
Paley graph. Now \(J=G[N_R(z)]\) belongs to \(\mathcal R(4,5;23)\), and r
has degree five inside J with neighborhood S.

The [complete dense-hub census](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification)
classifies this pointed situation. For \(S\cong K_{2,3}\), it gives
\(e(J)\le116\), with exactly 29 rigid equality graphs, each having a unique
degree-five hub. For \(S\cong K_{2,3}-e\), it gives at most 115 edges,
24 rigid equality graphs, and excludes all 144 corresponding marked gluings
across indices 6, 7, 8. The separate star theorem excludes index 5 at degree 23.

For a fixed K2,3 interface, every equality gluing can be labeled using one of
the 29 representatives and one of **all twelve** isomorphisms from its standard
K2,3 labeling to H[S]. An isomorphism of J fixes its unique hub, maps its five
neighbors to S, and labels T as the displayed Paley graph. Relabeling T only
transports arbitrary A–T and B–T bits. It need not extend to an automorphism
of G. No symmetry of H removes a marking. The imported equality classification
already accounts for the Paley core's automorphisms; no additional quotient is
assumed here.

The nine K2,3 interfaces are partitioned as follows. Counts refer to distinct
original marked keys, with each index counted exactly once.

| Interface indices | Marked equality keys | Complete exclusion source |
|---|---:|---|
| 0 | 348 | [Interface-0 kernel](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_interface0_kernel) |
| 1, 2 | 696 | [Twenty-edge family](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_twenty_edge_kernel) |
| 3, 4 | 696 | [Sixteen-edge family](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_sixteen_edge_kernel) |
| 9 | 348 | This complete consumer |
| 10, 12 | 696 | [Twelve-edge family](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_consensus_kernel) |
| 11 | 348 | [Twenty-four-edge family](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_twenty_four_edge_kernel) |
| **Total** | **3,132** | **All nine equality cohorts** |

The last source also covers index 10, but its index-10 cases are not counted
again. Higher densities were already impossible by the local census. Closing
the equality cases proves the bound 115 for every K2,3 interface. The preceding
stronger type-62 bound and star exclusion complete the thirteen-type theorem.
For the intrinsic edge formulation, deficiency at most five at r is exactly
the hypothesis \(e(H)\ge109\); the theorem supplies the other endpoint bound.

## The new literal interface-9 family

Interface 9 in the pinned input is the graph6 record

```text
Uv?IXZIhlRWjUXL[iphstSuAhcpht]OvWUl[??Bw
```

It has vertex set 0 through 21, 109 red edges, unique degree-five hub z=21,
and \(S=\{16,17,18,19,20\}\) inducing K2,3. Put
\(A=\{0,\ldots,15\}\), r=22, \(T=\{23,\ldots,39\}\), and
\(B=\{40,41,42\}\). Fix precisely these colors:

- H is the displayed graph.
- r is red to H and blue to T and B.
- z is red to T and blue to B; H already fixes its other incidences.
- T is Paley-17, with red nonzero differences \(\{1,2,4,8,9,13,15,16\}\).
- All 85 S–T bits come from one equality representative and one relative marking.

The full 43-vertex template has 514 fixed pairs and 389 free pairs:
272 A–T, 48 A–B, 15 S–B, 51 T–B, and three pairs within B. There are no
additional degrees, outside quotas, or symmetry constraints. Every completion
of each physical template is included.

The kernel uses the induced 40-vertex union \(H\cup J\), vertices 0 through
39. Number every unfixed pair in the **full** template lexicographically by
variables 1 through 389, with true meaning red. For each five-set in the union,
substitute the fixed colors in both monochromatic prohibitions. Discard a
prohibition if an opposite fixed color satisfies it; otherwise keep the clause
of unknown pairs. Deduplicate identical clauses. No auxiliary variables occur.
This formula is exactly five-clique avoidance on the union, using precisely
the 272 A–T variables. All other 117 variables stay unconstrained.

Every full Ramsey completion must satisfy this weaker system. Thus its
refutation excludes every completion of the original marked case, without any
converse lifting assumption. The literal partial 40-vertex graph itself has
no Ramsey completion, regardless of additional vertices.

## Independent implementations and proof checks

`consumer.py` decodes graph6 into a bit string, builds the physical pins by
pair membership, and grows five-cliques compatible with fixed colors using
bit sets. `audit.py` imports no producer: it decodes the graph6 integer by bit
positions, checks every permutation of S against all ten literal adjacencies,
and builds an independent symmetric matrix. Every one of the 903 physical
pairs agrees in all 348 cases.

`audit_cnf.cpp` reads that independent matrix and visits all
\(\binom{40}{5}=658008\) five-sets using nested index loops and direct pair
colors. All 348 independently generated formulas agree byte for byte with the
producer, for **228,986,784** literal five-set checks. An explicit support
audit requires all and only the 272 A–T variables to occur. The manifest pins
the entire ordered key set, each matrix and formula, and their sizes.

Kissat returned UNSAT for every case. The separate drat-trim checker verified
every refutation with exit zero and `s VERIFIED`. Neither solver status nor
hash identity substitutes for checking a proof. A missing, undecided, or
unverified case makes the complete reproduction fail.

Complete matrix/formula manifest SHA-256: `1488ce29cca3576c6afc8398d6fed0ea4c814d38a06fa4a512f1157df75567d2`.
Complete marked-template stream SHA-256:
`ebd7ebcf2e998665502e53d3a1ff25f998deb14782cd5d6924334513b3e9caec`.
Clause counts range from 19,367 to 19,487. Resource observations and exact native
source versions are recorded in `NATIVE_REPLAY.json`.

## Reproduction and controls

Use a full checkout of this repository. The adjacent dense-hub classification
supplies exactly two data inputs, verified before use:

| File | SHA-256 |
|---|---|
| `inputs.json` | `8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2` |
| `certificate.json` | `f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02` |

With Python 3.10+, a C++20 compiler, Kissat and drat-trim, run from the repository
root using a new scratch directory outside the checkout:

```sh
python3 -B ramsey_r55_dense_degree_five_hub_gap/reproduce.py /tmp/fresh-r55-hub-gap --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected final status:
`VERIFIED_COMPLETE_INTERFACE9_DENSITY116_40_VERTEX_OBSTRUCTION`.
The command compiles the independent auditor, checks controls, generates every
physical matrix and both formulas, solves all 348 cases, verifies all proofs,
and compares the complete manifest and expected output. It reproduces the new
interface-9 consumer; the other eight cohorts and catalogue completeness are
explicit imported theorems, not rerun by this command. Each linked source has
its own complete reproduction command.

The native solver cap is 30 seconds per case, with a 45-second outer process
limit and a 120-second proof-check limit. Any failure stops the run without a
complete claim. Native sources are [Kissat](https://github.com/arminbiere/kissat)
and [drat-trim](https://github.com/marijnheule/drat-trim); their exact commits
are in `NATIVE_REPLAY.json`. No external Python package, private input, catalogue
download, or network request is needed during replay. Large generated formulas,
matrices, proofs, logs and executables remain in external scratch and are
regenerated, not published.

Controls exhaust 32 small formulas over 32,768 assignments (32,243 satisfying).
A dedicated example has a monochromatic five-set involving an omitted vertex
while its active kernel is valid. Eighteen corruptions are rejected, including
malformed matrices, invalid keys, changed input pins, a missing physical variable,
and an added outside-edge constraint. All 348 templates also undergo 314,244
pair-transport checks under one fixed scrambled labeling with arbitrary edge
assignments. Those are controls; the general relabeling bijection is the
mathematical argument above, not inferred from sampled assignments.

A fresh end-to-end replay completed in 159.928 seconds, matched all
expected outputs and every matrix/formula hash, and checked all 348 new proofs.
Every fresh proof hash matched production. Production used 41.976 seconds
of aggregate solver time and 54.588 seconds of checker time; its largest
solve took 0.452 seconds. It generated 40,221,076 bytes of DRAT
traces, all kept outside the public source. Normal and optimized Python controls
agree; a Clang 17 address/undefined-behavior sanitizer build agrees on the
controls and 40 complete formulas spanning all representatives and markings.
All 348 formulas are independently audited with the normal GCC build.
An empty DRAT proof is rejected. The exact checker uses bounded pair indices
and clauses of length at most ten; Python integer and bit-set operations are exact.

## Provenance, reviews and limits

The imported results have these separate source commits and Discovery Net
heights. Commits identify the premises; hashes are not proof certificates.

| Premise | Height | Source commit |
|---|---:|---|
| Thirteen dense interfaces | 3349 | `8bf27902fba404e35593c90cbc7d2991abeda510` |
| Star degree-23 exclusion | 3419 | `cfb1dee2e76cc3c786b566b6d0c27bc734d80ab0` |
| Complete dense-hub census and type-62 consumer | 3455 | `590bcae0fe01e88e0a8fcf8030fbb2524973e4cb` |
| Interface 0 | 3469 | `ccc1580ba01738757795afa24f74e55af05f2aff` |
| Interfaces 10, 12 | 3505 | `1613d62eed08e2295cf5dda30b57a095e56c9eef` |
| Interfaces 1, 2 | 3537 | `2b888182cc68c44226605188eae0c219098aa9d7` |
| Interfaces 3, 4 | 3561 | `d44c07a4c85ca269be14bce193507655a6be3ddd` |
| Interface 11 through the 10/11 family | 3587 | `92335c457b35f47ead428ba79a834ded1637233e` |

The first four premises have independent acceptances at heights 3355, 3431,
3467, and 3483. The twelve-edge family has canonical acceptance at 3519;
that review independently reconstructed all matrices and checked all proofs,
but independently compared only twelve stratified complete clause sets and
three LRAT conversions. The twenty-four-edge result was independently accepted at h3597, with all
348 matrices and 628,488 transports reconstructed, five stratified CNFs
independently rebuilt, and all 348 author-generated proofs freshly checked.
Its [review source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type126_twenty_four_edge_review1)
has commit `f206fc019dffaf81fc9eece7506b027b12c000ee`. This distinguishes
independent reconstruction from the full author replay. The twenty- and
sixteen-edge results remain author computations with separate physical/formula
implementations and native proof checks; external review remains pending
through intake height 3602. This new result is also an author computation,
not an external review or a proof-assistant formalization.

Reader-link correction: the h3561 graph body accidentally uses `type-126`
in three public directory paths. The correct directories use `type126`, as
in the twenty-edge, sixteen-edge, and twelve-edge links in the coverage table
above. The source commits and mathematical claims are unchanged.

Trust includes the imported thirteen-type and equality catalogues, Paley-17
uniqueness, prior complete gluing theorems, the transport and weaker-system
arguments, unformalized implementations, compiler/language semantics, the
native DRAT checker, and ordinary hardware. U(22)=114 and U(23)=122 are needed
only for the stated deficiency notation.

Primary literature was checked after graph-first selection:
[Angeltveit and McKay's pointed-gluing framework](https://arxiv.org/html/2409.15709v2)
uses complete pointed families and common-neighborhood automorphisms. Those
methods are classical. Its principal order-22 dense catalogue starts at 113
edges; the present conditional degree-five boundary is 109. A limited search
found no matching uniform edge-deficiency statement. Historical priority,
a new gluing method, and optimality of the resulting bound are not asserted.

The surviving complete cases are lower hub degrees in all thirteen interfaces,
and degree 23 with density at most 114 in indices 6–8 or at most 115 in the nine
K2,3 indices. Their 389-variable equality templates have all been excluded;
the more general degree-23 interfaces have 474 free edges before choosing the
hub-neighborhood representative and remain open. The next falsifiable target
is a **complete next-density marked family together with a complete gluing
consumer**, beginning with type-62 density 114 or type-126 density 115 according
to the next committed principal ranking. No unconsumed local census is a closure.
