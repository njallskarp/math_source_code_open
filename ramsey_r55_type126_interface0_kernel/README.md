# Interface 0 has no type-K2,3 density-116 gluing

**Computer-assisted theorem.** In the complete thirteen dense degree-five
interfaces of order 22, take interface 0 and its unique local degree-five
hub z. If this interface occurs as a red neighborhood in a hypothetical
43-vertex (5,5)-Ramsey graph and z has global red degree 23, then

\[
e_R(N_R(z))\le115,\qquad \delta_R(z)=122-e_R(N_R(z))\ge7.
\]

The complete density-116 boundary has **348** marked cases: all 29
type-\(K_{2,3}\) equality representatives from the preceding local
classification, with all twelve relative markings of their five-vertex
common neighborhood. Every case is impossible already on the induced
**40-vertex union** of the two neighborhoods. All 272 edges between
their private cores are free. The three other vertices are unnecessary
for the contradiction.

In the complete 43-vertex template, all **389** unfixed physical edges
remain Boolean variables. The 40-vertex kernel constrains 272 of them;
the other 117 remain wholly unrestricted. No outside quota, additional
degree profile, global symmetry, or unforced physical edge is imposed.

The result does not exclude the lower-density part of interface 0, any
entire remaining degree-23 interface, a whole M-slice, or the full order-43
Ramsey family. Of the preceding 3,132 type-\(K_{2,3}\) equality templates,
**2,784** remain undecided, belonging to interfaces 1–4 and 9–12. No
feasibility is asserted for any retained template.

## Precise literal family

Graphs are simple and red edges are the edges of the displayed graph.
The original neighborhood H has vertices 0 through 21 and graph6 record

```text
UsHHirKdlp[IFVI|KpqfR]hAfaRiq]UpYWF[??Bw
```

This is index 0 in the hash-pinned thirteen-record input. It has 109 red
edges, unique degree-five hub z=21, and \(S=N_H(z)=\{16,\ldots,20\}\),
inducing \(K_{2,3}\). Put \(A=\{0,\ldots,15\}\), r=22,
\(T=\{23,\ldots,39\}\), and \(B=\{40,41,42\}\).
The fixed physical colors are:

- H is the displayed graph.
- r is red to every vertex of H and blue to T and B.
- z is red to T and blue to B; its colors inside H are already fixed.
- T is Paley-17: differences in \(\{1,2,4,8,9,13,15,16\}\) are red.
- The 85 S-to-T bits come from a density-116 equality representative and
  one of its twelve relative S markings.

There are 514 fixed physical pairs and 389 free pairs. The free pairs
are A–T (272), A–B (48), S–B (15), T–B (51), and pairs within B (3).
The kernel uses only vertices 0 through 39, hence only A–T variables.
Its contradiction also proves that the literal 40-vertex partial graph
has no Ramsey completion regardless of any incidences to new vertices.

## Why this is a complete intrinsic cohort

The preceding [dense-hub classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification)
proves that every \(J\in\mathcal R(4,5;23)\) with a degree-five hub
whose neighborhood induces \(K_{2,3}\) has at most 116 edges. Its
complete equality family consists of 29 rigid graphs, each with a unique
degree-five hub. This is an explicit imported completeness theorem, not
a conclusion drawn here from reading 29 records.

In a hypothetical graph G with \(H=N_R(r)\) and \(d_R(z)=23\),
exactly seventeen outside vertices are red to z. They form a (4,4)
graph and are Paley-17 by the imported order-17 uniqueness theorem.
The remaining three outside vertices are B. Now \(J=G[N_R(z)]\)
has r as its degree-five hub, with neighborhood S. Therefore at density
116 it is isomorphic to one of the complete 29 representatives.

An isomorphism to such a representative fixes its distinguished hub,
maps its five neighbors onto S, and labels its seventeen nonneighbors
as the displayed Paley graph. The type \(K_{2,3}\) has twelve
automorphisms. Enumerating **every** isomorphism from its standard
labeling to the fixed H[S] gives every relative marking. Relabeling T
merely relabels the free A–T and B–T bits. It is not assumed to extend
to an automorphism of G. Likewise no automorphism of H is used to
discard markings.

Thus every member of the stated intrinsic equality branch occurs in
one of the \(29\cdot12=348\) physical templates. Higher densities
are already excluded by the imported local theorem. The new complete
equality exclusion consequently gives the bound 115. The deficiency
notation additionally imports U(23)=122; the literal incompatibility
of the two displayed neighborhoods does not use this extremum.

## Exact kernel and independent checking

Number every unfixed pair of the **full 43-vertex template** in increasing
lexicographic pair order by variables 1 through 389; true means red.
For each five-set Q contained in vertices 0 through 39, impose both
monochromatic prohibitions. Substitute only fixed colors. A prohibition
with an opposite fixed color is discarded as satisfied; otherwise its
clause contains the unknown pairs of Q. Identical clauses are deduplicated.
There are no auxiliary variables and no other constraints.

This formula is exactly the absence of a monochromatic K5 in the
40-vertex union, with all 117 other variables arbitrary. Every full
43-vertex Ramsey completion would satisfy it. A refutation of this
weaker system therefore excludes every full completion of that marked
case; no converse lifting claim is needed.

`consumer.py` reconstructs templates using bit strings and generates
clauses by recursively growing five-cliques compatible with fixed colors.
`audit.py` imports no producer: it decodes graph6 by integer bit positions,
checks all permutations of S against literal pair adjacency, and builds
the physical matrix independently. The two matrices agree on every one
of the 903 pairs in every case.

`audit_cnf.cpp` reads the independently built full matrix, assigns all
389 physical variables, and visits all
\(\binom{40}{5}=658008\) five-sets with nested index loops. It
reads all ten pair colors directly to reconstruct the two clauses.
All 348 independent formulas agree byte for byte with the producer:
**228,986,784** literal five-set checks. Each formula has 19,230–19,311
clauses and uses exactly the 272 A–T variables. The explicit support
audit rejects any constraint on the 117 omitted-vertex variables.

Kissat returned UNSAT on all 348 complete cases. **drat-trim checked
every refutation**, returning `s VERIFIED` with exit code zero. Solver
status or hashes alone are not treated as proofs. The public manifest
pins each complete key, physical matrix, formula, variable count and
clause count. Any missing or undecided key makes reproduction fail.

Complete formula/matrix manifest SHA-256:
`6d306dde34a449f0aa66a6b7054309f1396879f5d46e018751aaa9a0e0be28b0`.
Complete marked-template stream SHA-256:
`101b8d5bd81ddc273fa4f076a4d72bd3fcbd5d74b43890e3072aa208db702142`.

## Reproduce

Use a full checkout of this repository. The adjacent preceding
classification directory supplies `inputs.json` and `certificate.json`;
their exact SHA-256 values are checked before use. The new consumer
imports no preceding producer, auditor or encoder code. Mathematical
catalogue and orbit completeness remain the stated upstream theorem.
To independently replay that theorem, its separate `reproduce.py`
regenerates both complete tuple enumerations; this new command does
not rerun that preceding classification.

With Python 3.10+, a C++20 compiler, Kissat and drat-trim, choose a
fresh scratch directory outside the source checkout:

```sh
python3 -B ramsey_r55_type126_interface0_kernel/reproduce.py /tmp/fresh-r55-interface0 --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected final status:
`VERIFIED_COMPLETE_INTERFACE0_DENSITY116_40_VERTEX_OBSTRUCTION`.
The command compiles the literal auditor, runs definition-level controls,
constructs every template and both formulas, solves every case, verifies
every DRAT proof, and compares the complete manifest and expected output.
Both native proof tools are required. There is no classification-only
mode that could be mistaken for this global exclusion.

Production used CPython 3.12, GCC 16.2, Kissat 4.0.4 and drat-trim at
the exact source commits in `NATIVE_REPLAY.json`. Primary native sources:
[Kissat](https://github.com/arminbiere/kissat) and
[drat-trim](https://github.com/marijnheule/drat-trim).
Typical builds use `./configure && make` for Kissat and `make` for
drat-trim after checking out the recorded commits. The per-case solver
cap is 30 seconds; production's maximum observed solve was 0.512 seconds.
An UNKNOWN or failed checker stops the run without claiming completeness.

A fresh end-to-end replay completed in **171.672 seconds**, matching
all expected outputs and the complete manifest and checking every new
refutation. The initial production used 49.165 seconds of aggregate solver time
and 78.682 seconds of aggregate checker time. Formula construction,
independent enumeration and I/O add to those times. The 48,678,110 bytes
of observed DRAT traces, generated CNFs, matrices, logs and binaries
stay in external scratch. They are regenerated by the command and are
not included in the compact source publication. No private data, external
catalogue download, Python package or network request is needed by replay.

## Controls and trust boundary

Controls compare 32 small physical formulas with all 32,768 assignments,
of which 32,243 satisfy their necessary kernels. A dedicated control
has a monochromatic five-set involving an omitted vertex while its
active kernel is valid; the weaker-system distinction is checked directly.
Sixteen corruptions are rejected, including malformed physical matrices,
invalid cohort keys, changed upstream files, a missing edge variable and
an unrequested constraint on an outside edge. The complete 348-template
transport audit checks 314,244 physical pair identities under a scrambled
labeling using arbitrary edge assignments, not Ramsey witnesses.

Normal and optimized Python agree. The independent C++ auditor was
also built with Clang 17 address/undefined-behavior sanitizers. Small
controls and 41 complete formula audits agree with production; those
41 cover all 29 equality representatives and all twelve markings.
An empty DRAT proof is rejected. All C++ indices are bounded by 43,
variable IDs by 903, and clause lengths by ten; no floating arithmetic
or wide integer enumeration is used.

This is an exact computer-assisted author result, with independently
implemented physical and formula checks and a separate native proof
checking kernel. It is not an external peer review or a proof-assistant
formalization. Trust remains in the imported classification and Paley
uniqueness, the displayed transport and weaker-system implication,
unformalized checker implementations, compiler/language semantics,
DRAT checking and ordinary hardware. Hashes establish identity.

## Imported results, literature and residual cases

The complete local census and prior type-62 consumer are Discovery Net
h3455, `bafkreib32yjgeg6rdrmz7y5wo3csmanuuy234kr3aakm2363pqd3hn7oke`,
source commit `590bcae0fe01e88e0a8fcf8030fbb2524973e4cb`.
It was independently accepted at h3467,
`bafkreihma7o7x3qc4msziaeonw4r7ro3fkpq4ag42z5r5fdnh2sqiwn3oi`:
the [review evidence](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_dense_degree23_hub_classification_review1)
at source commit `45974c3a81bde6c273fa2ebd02614cb74ff86b82` includes a
third complete tuple census and fresh checks of all prior refutations.
That acceptance covers the preceding result, not this new 348-case consumer.
The [thirteen-interface classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification)
is h3349, source commit `8bf27902fba404e35593c90cbc7d2991abeda510`.
Its five-separator interpretation is h3375. The preceding Paley endpoint
theorem h3419 closes the star index's degree-23 branch. Their reviewed
scopes are inherited explicitly, not enlarged by this computation.

Primary literature was checked after graph-first target selection:
[Angeltveit–McKay's pointed-gluing framework](https://arxiv.org/html/2409.15709v2)
and [McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Pointed gluing, Paley graphs and using a weaker induced subsystem are
classical. The limited search found no matching exact interface-0
statement; historical priority and a new general method are not claimed.

At degree 23 the current density bounds are now:

| Interface indices | Hub type | Maximum neighborhood edges | Minimum red deficiency |
|---|---|---:|---:|
| 0 | \(K_{2,3}\) | 115 | 7 |
| 1–4, 9–12 | \(K_{2,3}\) | 116 | 6 |
| 6–8 | \(K_{2,3}-e\) | 114 | 8 |
| 5 | star | entire degree-23 branch excluded | — |

All lower hub-degree branches remain, along with the lower-density parts
of the twelve retained degree-23 interfaces. In those lower-density
interfaces, 474 physical edges remain free before further classification.
The 2,784 other type-126 equality cases still have 389 free edges apiece.
H-star remains frozen; no whole hard slice or Ramsey bound changes.

The next falsifiable milestone is a complete decision for another
principal-ranked surviving type-126 cohort, or a uniform structural
obstruction covering several remaining cohorts. It must preserve every
relative marking and every unfixed physical edge. The result is separate
from researcher 1's M214 roots and researcher 3's M216 central-cap work.
