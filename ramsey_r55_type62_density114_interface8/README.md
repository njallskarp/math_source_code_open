# Interface 8 closes the complete type-62 density-114 layer

**Theorem.** Let \(G\) be a graph on 43 vertices with no red or blue five-clique.
Suppose \(H=G[N_R(r)]\) is isomorphic to original interface 8 in the thirteen-type
dense degree-five classification, and let \(z\) be its unique local degree-five
vertex. If \(d_R(z)=23\), then

\[
e_R(G[N_R(z)])\le113,\qquad
\delta_R(z)=122-e_R(G[N_R(z)])\ge9.
\]

Color reversal gives the same statement. This improves the preceding bound
eight on this entire intrinsic branch. The new computation excludes all
**3,394** marked density-114 interface-8 templates, with every remaining
physical pair free.

**Composition.** Together with the existing complete
[interface-6 exclusion and classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type62_density114_interface6)
and [interface-7 exclusion](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type62_density114_interface7),
the same bound now holds for every original type-62 interface, namely 6, 7 and 8.
Their combined density-114 layer has 10,182 marked keys; only the final 3,394
are new here. The 1,697 local graphs remain valid local objects. Their complete
gluing family to these three fixed neighborhood types is excluded.

## Complete structural reduction

The original interface H has 22 vertices and 109 red edges. Its graph6 record is

```text
UsHHirKdlp[IFVI|KpqfRUEYUfBFs\Y`z~?G??Bw
```

The hub is \(z=21\), with neighbors \(S=\{16,17,18,19,20\}\). They induce
the standard type-62 graph \(K_{2,3}-e\), with red edges 02,03,04,12,13 under
the displayed order. Its two markings into S are (16,17,18,19,20) and
(16,17,19,18,20). Put \(A=\{0,\ldots,15\}\) and \(r=22\).

If the global red degree of z is 23, it has seventeen outside red neighbors
\(T=\{23,\ldots,39\}\) and three other outside vertices \(B=\{40,41,42\}\).
The graph induced by T belongs to \(\mathcal R(4,4;17)\): a red four-clique
would join z and a blue four-clique would join r. The imported uniqueness
theorem identifies T with Paley-17.

Write \(J=G[N_R(z)]\). Then \(J\in\mathcal R(4,5;23)\); its vertex r has
degree five with neighborhood S. The existing dense-hub theorem and complete
density-115 consumer give \(e_R(J)\le114\). At equality, h3653 supplies exactly
1,697 possible local isomorphism classes. Each is rigid and has a unique
degree-five hub. Each consists of five actual Paley attachment columns with
total cardinality 36. No column is replaced by a maximal superset.

The classification uses the full 136-element Paley automorphism group and the
two automorphisms of the five-vertex type-62 graph. Its complete 461,584 labeled
column tuples are partitioned into 1,697 disjoint orbits of size 272. A second
enumeration uses no affine normalization; its complete labeled stream agrees
entry by entry with the expanded canonical orbits. The full finite group and
physical representative checks are rerun by this package's reproduction.

For each class, keep both isomorphisms into H[S]. The precise new key set is

\[
\{(8,62,j,k):0\le j<1697,\ 0\le k<2\}.
\]

Every graph in the stated branch maps to some key: the unique local hub fixes
the pointed correspondence, a Paley relabeling moves its T to the chosen
coordinates, and both S markings are retained. Relabeling T transports all
unfixed A–T and B–T bits bijectively. It is not assumed to extend to a global
automorphism. No automorphism of H is used to discard a marking.

## All remaining pairs stay free

Fix only H, both anchor stars, Paley-17 on T, and the chosen 85 S–T colors.
Exactly **389** physical pairs are Boolean variables:

| Pairs | Count |
|---|---:|
| A–T | 272 |
| A–B | 48 |
| S–B | 15 |
| T–B | 51 |
| B–B | 3 |

The necessary formula forbids both monochromatic five-cliques on the
forty-vertex union H union J, which is exactly vertices 0 through 39.
Variables are numbered on all 389 free pairs, but precisely the 272 A–T
variables occur in clauses. All **117** other variables remain unrestricted.
No auxiliary variables, outside degree quotas, separator inequalities,
cut-rank assumptions or global symmetry conditions enter the formula.

Every full Ramsey43 completion would satisfy this weaker system. Therefore
its checked contradiction excludes every assignment to the full 389-pair
interface, including every choice involving B. This direction does not apply
a theorem about 43 vertices to an arbitrary forty-vertex coloring.

## Independent checks and certificates

The producer decodes graph6 as a bit string and builds a dictionary of fixed
pairs. The independent physical auditor uses integer decoding and a symmetric
matrix, testing all ten pairs of S. Their entire 903-pair specifications agree
for every key.

The Python encoder recursively visits compatible five-cliques. The C++ auditor
literally scans all 658,008 five-sets, substitutes the physical matrix and
deduplicates the resulting clauses. Their complete CNFs agree byte for byte
for every case. Every one of the 3,394 native Kissat UNSAT proofs is accepted
by drat-trim. The full public-command replay regenerates every formula and
proof and checks them again; an author status log alone is never an acceptance
path.

The formulas contain 19,150 through 19,352 clauses,
65,279,286 in total. All 3,394 matrices and all 3,394 CNFs are
pairwise distinct. The complete ordered matrix/formula manifest SHA-256 is
`fd983b33f500c896939d566c7ef87731545e85c6e68ed4879310c2966b65c577`.
The independently reconstructed marked-template stream SHA-256 is
`14f68e5f54aff43826d29057fc543b7db09a535aab910c3026680cd8e6995e25`.
The full labeled classification stream SHA-256 is
`84f53e3e52093fd4a466251c12f3ae2e937f5f1166eeb372c08b52b9851fdec8`.

Controls exhaust 32 small formulas and 32,768 physical assignments, including
32,243 satisfying assignments. They reject nineteen malformed or altered
inputs, foreign cohort keys and scope changes. An omitted-vertex example
checks that the kernel is a proper relaxation. All 3,394 distinct templates
pass 3,064,782 scrambled-label pair checks with arbitrary free assignments.
The general transport proof, rather than these finite controls, establishes
relabeling coverage. An empty proof for key (8,62,0,0) is rejected by drat-trim.

Normal controls and optimized Python with a Clang address/undefined-behavior
sanitized auditor agree. Sanitizers cover the 32 small native formulas and
seven malformed native inputs; the full native cohort uses the release build.
The imported classification controls additionally check 35,049 small physical
configurations and reject five damaged classifications and five malformed
graph6 records.

## Reproduction and resource boundary

Use a full repository checkout, Python 3.10+, a C++20 compiler, Kissat and
drat-trim, with a new scratch directory outside the source checkout:

```sh
python3 -B ramsey_r55_type62_density114_interface8/reproduce.py /tmp/fresh-r55-interface8-114 --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected final status:
`VERIFIED_COMPLETE_INTERFACE8_TYPE62_DENSITY114_EXCLUSION`.

The command checks all nine pinned classification files, derives the compact
certificate, reruns both complete enumerations, compares their entries,
checks the full orbits and representatives, runs the controls, derives both
CNFs and verifies every new refutation. It does not rerun the old interface-6
or interface-7 consumers. A missing, undecided or unverified case fails.

The production cohort completed in **1283.917107 seconds**.
The checked traces totaled 162,683,102 bytes before cleanup. Aggregate
solver and checker wall times were 236.728781 and
328.209931 seconds; the longest solve took
0.244738 seconds. A separate fresh run of the entire
public command passed in **1466.071976 seconds**,
including both classification enumerations and every new refutation. Every
matrix, CNF and native proof hash matched production. Observed child peak RSS
was 564,903,936 bytes in the fresh run on macOS;
these are measured costs, not resource guarantees.

Kissat has a thirty-second limit per case, with a forty-five-second outer
limit and 120 seconds for each proof check. The native implementations are
[Kissat](https://github.com/arminbiere/kissat) and
[drat-trim](https://github.com/marijnheule/drat-trim). Exact tested versions,
source commits, compiler flags and timings appear in `NATIVE_REPLAY.json`.
Python arithmetic is exact. The native scanner handles at most 43 vertices,
903 variables and ten literals per clause, within signed 32-bit bounds.
No floating-point verdict enters the proof.

Large tuple streams, matrices, formulas, proofs, logs and binaries stay in
external scratch. By default each formula pair and proof is deleted only
after formula agreement, actual proof acceptance and an atomic hash checkpoint.
Use `--keep-native` to retain them all. The public command regenerates and
checks the proof bytes; hashes establish identity and do not replace proofs.
No network, private input, stored author acceptance log or omitted proof file
is required during reproduction.

Storage guards wait for 256 MiB of scratch headroom before new stages, cases
and saved outputs. ENOSPC checkpoint/output writes retry with the computed
result and checked proof retained. These waits do not extend solver limits or
change formulas. They are included in the reported elapsed times.

## Imported premises and scope

The intrinsic theorem imports order-17 (4,4) uniqueness, the
[thirteen-interface classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification)
(h3349, reviewed h3355; commit `8bf27902fba404e35593c90cbc7d2991abeda510`),
and the [dense-hub classification and density-115 exclusion](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification)
(h3455, reviewed h3467; commit `590bcae0fe01e88e0a8fcf8030fbb2524973e4cb`).
The Paley bridge is h3419, reviewed h3431; U(23)=122 is imported to express
deficiency. The thirteen-interface classification itself imports the complete
two-graph \(\mathcal R(4,4;16)\) catalogue, whose completeness is not rederived.

The density-114 classification is h3653, public commit
`607d56027ae008e1b02ee1d351e8f9cf9757b752`. Its certificate SHA-256 is
`39491fe6f15eb2ff887c0985cbbe50cced364a27047b7ead39427125f5b86cf8`.
`IMPORTED_CLASSIFICATION.json` pins its nine reused source/evidence files.
The earlier `inputs.json` and `certificate.json` are separately pinned to
`8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2` and
`f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02`.
The older 24-row density-115 list is not substituted for the new class list.

The combined three-interface corollary additionally imports the already
committed interface-6 and interface-7 exclusions. The latter is h3695,
commit `65f3bb69ccba42a11b29d812cabc3e674fdbe0f9`.
Review status at committed cutoff 3722: h3653 external review pending through3722. h3695 external review pending through3722.
The present fresh replay is reproducibility evidence. Independence comes
from distinct physical/encoding algorithms, the two classification
enumerations and the native proof checker; it is not an external review.

After graph-first selection, primary literature was checked at
[Angeltveit–McKay](https://arxiv.org/html/2409.15709v2) and
[McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Pointed gluing and the column decomposition are established methods. A limited
search found no matching exact interface-8 consequence; no priority claim or
new general gluing method is asserted.

Trust remains in imported theorem statements, the written unformalized
reductions, complete group action, exact enumeration and encoding programs,
compiler/interpreter semantics, drat-trim and ordinary hardware. Literal
contradictions for the fixed matrices need no catalogue-completeness premise;
coverage of the intrinsic branch does.

No density-114 type-62 key remains among interfaces 6, 7 and 8. Lower densities
in all three interfaces remain open, as do all twelve surviving full degree-23
interface families, lower hub degrees and the other low/hard branches.
No Ramsey-number bound changes. The frozen H-star run is not reopened.
After the required delay, reassess global applicability before another density
descent. The next falsifiable milestone must be a complete
remaining structural-family decision or a forcing theorem changing its scope,
selected against refreshed principal direction; this package starts no
unconsumed lower-density census.
