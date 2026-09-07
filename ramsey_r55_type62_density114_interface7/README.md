# Interface 7 excludes the complete type-62 density-114 layer

**Theorem.** Let \(G\) be a graph on 43 vertices with no red or blue five-clique.
Suppose \(H=G[N_R(r)]\) is isomorphic to original interface 7 in the reviewed
thirteen-type dense degree-five classification. Let z be its unique
local degree-five vertex. If \(d_R(z)=23\), then

\[
e_R(G[N_R(z)])\le113,\qquad \delta_R(z)=122-e_R(G[N_R(z)])\ge9.
\]

The statement also holds with the colors reversed. It improves the previous
lower bound eight for this entire intrinsic branch. All 1,697 classes of the
possible density-114 hub neighborhood, with both relative markings, are
excluded. This is a new consumer of an existing complete classification;
its construction and 1,697-class count are not new results of this package.

## Exact family and coverage

The pinned original interface H has 22 vertices, 109 red edges, and unique
local degree-five hub z=21. Its graph6 record is

```text
UsHHirKdlp[IFVI|KpqfROjqNKRiq\pDz~?G??Bw
```

Its hub neighbors are \(S=\{16,17,18,19,20\}\), inducing \(K_{2,3}-e\) (type 62).
Set \(A=\{0,\ldots,15\}\), \(r=22\). If \(d_R(z)=23\), z has seventeen red neighbors
\(T=\{23,\ldots,39\}\) outside H and three other outside vertices \(B=\{40,41,42\}\).
The induced graph on T belongs to \(\mathcal R(4,4;17)\): a blue four-clique would join r,
which is blue to every outside vertex, to make a blue five-clique; a red
four-clique would join z to make a red five-clique. The imported uniqueness
theorem therefore identifies T with Paley-17.

Let \(J=G[N_R(z)]\). Then J belongs to \(\mathcal R(4,5;23)\), and r is a degree-five vertex
of J whose neighborhood is S. The earlier dense-hub theorem gives \(e_R(J)\le114\)
for this branch, having excluded every density-115 possibility. At equality,
the [complete density-114 classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type62_density114_interface6)
provides exactly 1,697 isomorphism classes. The source commit is
`607d56027ae008e1b02ee1d351e8f9cf9757b752`; its compact certificate SHA-256 is
`39491fe6f15eb2ff887c0985cbbe50cced364a27047b7ead39427125f5b86cf8`.
Every representative has a unique degree-five hub and trivial automorphism
group. Each consists of five actual Paley attachment columns with total size
36, so no maximal-column substitution or saturation assumption is made.

The classification covers every labeled realization using the full
136-element Paley automorphism group and the two automorphisms of the
standard five-vertex graph with red edges 02,03,04,12,13. Its 461,584 labeled
column tuples split into 1,697 disjoint orbits of size 272. A second enumeration
uses no affine normalization and agrees entry by entry with the entire expanded
tuple stream, not merely its size.

For each representative, retain both isomorphisms of the standard five-vertex
graph to H[S]. This gives the complete key set

\[
\{(7,62,j,k):0\le j<1697,\ 0\le k<2\},
\]

with exactly 3,394 marked templates. The uniqueness of the local hub makes the
pointed correspondence compulsory. Relabeling T transports arbitrary A–T and
B–T colors bijectively. No such relabeling is assumed to be an automorphism
of the full graph. No automorphism of H is used to discard a marking.

## The free interface and the weaker contradiction

Fix only H, the two anchor stars, Paley-17 on T, and the 85 S–T bits specified
by the chosen representative and marking. Every one of the remaining **389**
physical pairs is a Boolean variable: A–T (272), A–B (48), S–B (15),
T–B (51), and B–B (3). There are no auxiliary variables, degree quotas,
global deficiency restrictions, separator inequalities, or global symmetry
constraints.

On the forty-vertex union H union J, impose the two monochromatic prohibitions
for every five-set, substituting only the fixed colors. Variables are numbered
lexicographically on all 389 full-template free pairs. Exactly the 272 A–T
variables occur in the formula; the other **117** remain completely arbitrary.
Consequently every full Ramsey43 completion would satisfy this weaker formula.
A checked contradiction in the formula excludes every possible assignment to
the whole 389-pair interface, including all choices involving B.

`consumer.py` decodes graph6 as a bit string and constructs fixed pairs directly.
The separate `audit.py` uses integer graph6 decoding, all ten S-pair tests,
and a symmetric matrix construction. Their full 903-pair specifications agree
for every key. Compatible-five-clique recursion generates one CNF;
`audit_cnf.cpp` independently scans all 658,008 five-sets literally to generate
the other. Both complete formulas agree byte for byte for every key.

Every one of the 3,394 formulas has a Kissat UNSAT trace accepted by drat-trim.
The resulting density-114 exclusion, together with the imported exclusion of
all higher densities, proves \(e_R(J)\le113\). \(U(23)=122\) is imported only to express
the resulting deficiency bound.

The formulas have 19,141 through 19,391 clauses each,
65,281,067 clauses in total. All 3,394 matrices and all 3,394 CNFs are
pairwise distinct. The complete ordered matrix/formula manifest SHA-256 is

`897ad1057ba5b1e492ac50944afb4895c476b2709f57454b474ccbed9a1ffeef`.

The independently reconstructed marked-template stream SHA-256 is
`6f4ba3b05d524e0d2fe1f537026c1dc09ef9bc5dc47d686162805529e66a373a`.
The empty-proof negative control on key (7,62,0,0) is rejected by drat-trim.

## Reproduction and controls

Use a full repository checkout, Python 3.10+, a C++20 compiler, Kissat, and
drat-trim. Select a new scratch directory outside the source checkout:

```sh
python3 -B ramsey_r55_type62_density114_interface7/reproduce.py /tmp/fresh-r55-interface7-114 --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected final status:
`VERIFIED_COMPLETE_INTERFACE7_TYPE62_DENSITY114_EXCLUSION`.

The command checks every pinned classification source byte, regenerates its
compact certificate, repeats both complete enumerations and their entrywise
comparison, checks all canonical orbits and physical representatives, runs the
controls, constructs both formulas for all 3,394 new keys, solves every case,
and checks every refutation. It does not rerun or take credit for the old
interface-6 consumer. Any missing, undecided, or unverified new case fails the
command. Imported theorem statements are distinct from replayed finite data.

`IMPORTED_CLASSIFICATION.json` pins the nine reused source and evidence files.
The earlier dense-hub `inputs.json` and `certificate.json` are additionally
pinned at `8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2`
and `f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02`.
Only its original interface record enters the new matrices. Its old 24-row
family is not substituted for the density-114 classification.

Kernel controls exhaust 32 small formulas and all 32,768 assignments, including
32,243 satisfying assignments, against literal five-clique avoidance. They
reject nineteen malformed or altered input/scope cases, including a changed
classification certificate and a foreign original interface. An omitted-vertex
example checks that the forty-vertex system is genuinely weaker than the full
system. All 3,394 templates pass 3,064,782 scrambled-label pair checks with
arbitrary free assignments. These finite controls supplement the general
transport argument, rather than proving it by sampling.

Normal controls and optimized Python controls with a Clang 17 address/undefined
behavior sanitized CNF checker have identical output. Sanitizer coverage is
all 32 small native formulas and seven malformed native inputs; the whole
3,394-case native cohort is checked in the release build. The imported local
classification controls additionally exhaust 35,049 small configurations and
reject five damaged classifications and five malformed graph6 inputs.

The production cohort completed in **1205.672944 seconds**.
The checked traces totaled 88,359,373 bytes before cleanup. Aggregate
solver and checker wall times were 230.663290 and
306.017597 seconds; the longest solve took
0.245089 seconds. A separate fresh run of the entire
public command passed in **1386.431504 seconds**,
including both classification enumerations and every new refutation. Every
matrix, CNF and native proof hash matched production. Observed child peak RSS
was 555,778,048 bytes in the fresh run on macOS;
these are measured costs, not resource guarantees.

The native solver limit is thirty seconds per case, with a forty-five-second
outer limit and a 120-second proof-check limit. Native sources are
[Kissat](https://github.com/arminbiere/kissat) and
[drat-trim](https://github.com/marijnheule/drat-trim); exact versions, source
commits and observed resource costs are in `NATIVE_REPLAY.json`.
Python arithmetic is exact. The CNF auditor uses arrays for at most 43 vertices,
at most 903 variables, and clauses of at most ten literals; its integer bounds
are far below signed 32-bit limits. No floating-point verdict enters the proof.

Large tuple streams, per-case matrices, CNFs, proofs, logs, executables and
checkpoints stay in external scratch. By default each CNF pair and native
proof is deleted only after the formulas match, the proof is accepted, and its
hash is recorded in an atomic case checkpoint. Supply `--keep-native` to retain
every native artifact. The ordered manifest and all traces regenerate from the
published source. No private input or network download is needed during replay.
The consumer waits for 256 MiB of available scratch space before a new case
and before saving a checkpoint. A checkpoint write that reports ENOSPC is
retried with the already checked proof retained; no solver call is extended.
These are storage guards and do not change any mathematical case or formula.

An earlier fresh attempt stopped after 2,485 recorded keys while writing the
next checkpoint. Its next physical matrix, both formulas and native proof all
match production, and that proof was checked again. The next checkpoint was
empty. Transient disk exhaustion is strongly indicated, but the old wrapper
had not preserved the child error text, so the exact errno is not claimed.
That partial attempt is not credited as a complete replay. A subsequent
attempt confirmed ENOSPC while saving the kernel-control output, before the
native cohort began; its exit-record write also failed. The replay wrapper
now retains completed child output and retries storage writes when necessary.
The recorded full replay uses another new scratch directory and both storage
guards. Every canonical key is regenerated in the original order. Adequate
scratch space is an operational requirement; storage waits are included in
the full observed elapsed time.

Hashes establish identity; they do not replace complete enumeration or proof
checking.

## Imported premises, novelty and residual cases

The intrinsic interpretation imports the order-17 (4,4) uniqueness theorem,
the [thirteen dense degree-five interfaces](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification)
(h3349, reviewed h3355; source `8bf27902fba404e35593c90cbc7d2991abeda510`),
and the [dense-hub classification and density-115 consumer](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification)
(h3455, reviewed h3467; source `590bcae0fe01e88e0a8fcf8030fbb2524973e4cb`).
The thirteen-interface theorem in turn imports the complete two-graph
\(\mathcal R(4,4;16)\) catalogue; that catalogue completeness is not re-enumerated
here. The degree-23 Paley bridge is h3419, reviewed h3431. The literal new forty-vertex
refutations use only the pinned matrices and have no external catalogue
completeness premise. General completeness of the density-114 family imports
h3653 and its stated uniqueness premise; the finite two-implementation
classification is replayed here. Its external review status was pending at
height 3677. This package is new author evidence with independent implementations,
not an independent external review of h3653.

Primary literature was checked after graph-first selection:
[Angeltveit and McKay's pointed-gluing framework](https://arxiv.org/html/2409.15709v2)
and [McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Pointed gluing and the column decomposition are classical. A limited search
found no matching exact interface-7 consequence; neither historical priority
nor a new general gluing method is claimed.

Trust remains in the imported theorems, the unformalized finite reductions,
complete group action, exact enumeration and encoding implementations,
compiler/interpreter semantics, the native DRAT checker and ordinary hardware.
No new bound on \(R(5,5)\) follows from this local branch exclusion.

The new covered family is original interface 7, global hub degree 23,
type-62 hub neighborhood of density 114, all 1,697 classes, both markings, and
all remaining physical edges free. Interface 6 was already excluded and is not
recounted. Interface 8 still has **3,394** unconsumed density-114 keys. Lower
density at interfaces 6 and 7 remains open. All twelve surviving full degree-23
interface families remain open; the H-star computation stays frozen. The global
moment-certificate and publication-audit lanes are unchanged.

The next falsifiable milestone is to finish the same complete density-114 layer
at original interface 8, subject to refreshed principal ranking. The protected
cold-M216 or global-interface opportunity remains available after the active
structural trial.
