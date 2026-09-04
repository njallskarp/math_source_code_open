# Independent full-chain review: Albertson `r=27`

## Verdict

**Accept after specific minor repairs.** Confidence: **0.91 (high)**.

I found no invalid mathematical implication in the chain ending at Discovery
Net synthesis
`bafkreihwabwrg3qtskdqujiom6wame2ixnyxmqlthcpak43mufnxv5lfta`.
In particular, the terminal planarization and sealed-pentagon argument survive
the degeneracy tests listed below. The proof does establish Albertson's
conjecture for finite simple graphs of chromatic number 27; it is not merely a
conditional or restricted-frontier theorem.

The first non-kernel-checked interface is the passage from a good drawing and
the equality classification to the five specified triangular faces. I closed
that interface directly below. The Lean files check the supplied finite face
complex but do not establish that a drawing supplies it. No acceptance node or
component review was used as authority.

The repairs are expository and evidence-labeling repairs, not changes to the
argument: isolate the drawing-to-five-face lemma; expand the planarization
simplicity/connectedness proof; state the sealed-disk entry-through-a-vertex
case; describe Lean's standard axiom dependencies exactly; and update the
synthesis provenance from its earlier `ae1fcd2...` snapshot to the assigned
history-audited snapshot `8402b180...`.

## Audited immutable inputs

- Assigned synthesis snapshot:
  `helgithorskarp/math_results`, commit
  `8402b1807cc4ab8acf44afce423a90d83e86bcdc`, directory
  `graph_theory/albertson_r27_reviewed_chain`.
- The synthesis node at height 2035 names earlier source commit
  `ae1fcd2a3f92dde67e8121644b14b2b8f7bc1386`; this is an ancestor of the
  assigned commit. The later commit adds the Git-history audit and the two
  expected chain digests, without changing the theorem's dependency manifest.
- Sadhu, arXiv:2609.01682v1, Theorem 1.3 and Section 5.
- Büngener--Kaufmann, arXiv:2409.01733v2, Theorem 6 and Propositions 21, 23.
- Pach--Radoicic--Tardos--Toth, *Discrete Comput. Geom.* 36 (2006),
  Lemmas 3.1, 3.2 and Conjecture 5.7.
- Ackerman, arXiv:1509.01932v2, Theorem 4.

## Dependency and hypothesis table

| Step | Implication | Scope and hypotheses checked | Result |
|---|---|---|---|
| 1 | A counterexample `G` contains a 27-critical counterexample `H`. | Finite simple graph; take a 27-critical subgraph. Crossing number is monotone under subgraphs, so `cr(H)<=cr(G)<cr(K27)`. | Sound. |
| 2 | Sadhu Theorem 1.3 reduces `H` to orders 53 or 54 and connected complement. | The theorem is explicitly about 27-critical `H` with strict `cr(H)<cr(K27)`. The complement conclusion is not silently used later. | Sound. |
| 3 | Sadhu Section 5 leaves exactly four `(n,m)` rows. | The no-subdivision critical-edge floors are 713 at `n=53` and 726 at `n=54`. Equation (1) first exceeds `Z(27)` at 716 and 727, respectively. Hence the exhaustive rows are `(53,713..715)` and `(54,726)`. Sadhu's 72-check companion verifier also covers every excluded order 32--96. | Sound; strict/weak endpoints checked. |
| 4 | It suffices to reach 6084 in each row. | `Z(27)=13*13*12*12/4=6084` and the standard drawing gives `cr(K27)<=Z(27)`. Thus `cr(H)>=6084` is enough even though `cr(K27)` is unknown. | Sound. |
| 5 | The order-54 row has crossing number at least 6084. | Universal over all simple 54-vertex graphs with at least 726 edges; no criticality or complement condition is needed. Integer ceiling of `218768121/35960` is 6084. | Sound. |
| 6 | The 714- and 715-edge order-53 rows exceed 6084. | Recursive convex induced sampling gives the universal 50-vertex line `cr>=26q-11706`; direct 50-to-53 sampling gives ceilings 6100 and 6129. | Sound. |
| 7 | The final row follows from `cr(24,132)>=165`. | The local endpoint, the rounded `37/9` line below 132, and Ackerman deletion above 132 give `cr(24,q)>=5q-495` for every integer `q`. No density hypothesis is attached to the `37/9` line. | Sound conditional implication. |
| 8 | A counterexample to the local endpoint has one of two profiles. | Start with a crossing-minimal good drawing of a simple `(24,132)` graph with at most 164 crossings. Büngener--Kaufmann deletion plus PRTT and Propositions 21, 23 give the displayed nonnegative integer system. A new search ranging over actual `x2` leaves only A and B, so equality is forced rather than assumed. | Sound. |
| 9 | Equality restricts the crossing graph of `D2` to `C5` and `K2` components. | PRTT Case 1 excludes degree at least 3; Case 3 excludes path components on at least three vertices; Case 4.2 excludes `C3`; the Case 4.1 defect identity excludes all cycles except `C5` (the `C4` creates two distinct triangles). Equality in the separation reduction forces order-two additive pieces, so there is no cross-block leakage. | Sound, but should be stated as a standalone lemma. |
| 10 | Exactly one `C5` is non-full. | Equality in the terminal 1-planar bound gives `q5=(2e2-8(24-2))/3`, hence `(q5,q2,free)=(10,7,39)` or `(12,4,38)`. Since `p=9` or 11, `q5=p+1`. | Sound. |
| 11 | Deleting `b,c` in every crossing `C5` yields terminal `(e,x)=(83,17)` or `(82,16)`. | Each deletion removes two edges and the four distinct crossings incident with them; different crossing components share no crossing. Every remaining edge is crossed at most once. | Sound. |
| 12 | The planarization is a simple connected triangulation. | Simplicity: original-original segments cannot duplicate because the graph is simple; original-crossing segments cannot duplicate because a good crossing has four distinct endpoints; crossing-crossing segments cannot occur because `T` is 1-planar. With `E=3V-6`, a disconnected simple plane graph has strict slack, hence the planarization is connected and maximally planar. Its faces are genuine 3-cycles, so there are no bridges or repeated face-boundary vertices. | Sound; current prose is too compressed. |
| 13 | The deleted arcs force `d=zr,f=wt,c=ut,b=ur`. | The open middle subarc of `c` is disjoint from `T`, so it lies in one face whose closure meets interiors of `a` and a segment of `d`. In a triangular face those sides share an endpoint, making `a=zw` a terminal-kite side. Crossing the adjacent sides then forces the third vertices `t` and `r`. The non-kite side of `zw` has one third vertex `u` for both arcs. | Sound. |
| 14 | The five faces form a disk with boundary `u-z-t-r-w-u`. | The oriented faces shell successively along exact connected boundary arcs. Internal orientations cancel, the boundary is one nonrepeating cycle, vertex links are intervals except for the circular link at `x`, and `V-E+F=1`. The four kite endpoints are distinct; `u=z,w` violates goodness and `u=r,t` would make `b,c` loops. | Sound. |
| 15 | Other full pentagons cannot supply an exceptional boundary side. | `m0=0` means the geometric boundary edge of every forbidden configuration is present and crossing-free. A full pentagon plus that boundary is a vertex-empty drawn `K5`. Entry through a side is impossible because the side is uncrossed; entry and exit through boundary vertices is impossible unless an edge repeats one of the ten existing vertex pairs, forbidden by simplicity. A survivor diagonal therefore has both incident faces inside its own sealed disk. | Sound; the boundary-vertex case should be explicit. |
| 16 | The exceptional `C5` is full, contradiction. | The five restored crossed edges are `zw,ur,ut,zr,wt`, exactly the complementary diagonals of the uncrossed vertex-empty pentagon. Their inherited crossing graph is `C5`. This contradicts `q5=p+1`. | Sound. |
| 17 | The last global row has `cr(53,713)>=6089`. | The universal order-52 line is `5F52(q)>=136q-65166`. Across the 53 vertex deletions, every crossing survives exactly 49 times and edge counts sum to `51*713=36363`. Thus `49cr(G)>=298314=49*6088+2`, and integrality gives 6089. | Sound. |
| 18 | Albertson `r=27` follows. | Every possible critical counterexample lies in one of the four rows, each has crossing number at least 6084, and `cr(K27)<=6084`. This contradicts the initial strict inequality. | Sound. |

## Independent arithmetic and finite replay

`independent_audit.py` imports no target code and uses only CPython integers,
`fractions.Fraction`, finite sets, and SHA-256. Its recursive table builder
uses a Jarvis/gift-wrapping lower hull, distinct from the supplied
monotone-chain/PAVA and QuickHull implementations. It reproduces:

- the exact four-row Sadhu frontier;
- the order-54 fraction `218768121/35960` and ceiling 6084;
- unconditional recursive-table digest
  `55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43`;
- conditional recursive-table digest
  `79e615e691c84d697b2dbc3d6fded0d9657c37d3f91f4bebc1a61097fb39f7f6`;
- order-53 row bounds 6100, 6129, and conditional 6089;
- the deletion sum `298314`, including the remainder 2 modulo 49;
- only the two residual profiles even when `x2` ranges over every actual
  value at least its PRTT floor;
- terminal profiles `(C5,K2,free,eT,xT)=(10,7,39,83,17)` and
  `(12,4,38,82,16)`; and
- the finite shell boundary and Euler characteristic.

Reproduction:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_audit.py \
  | diff -u EXPECTED_OUTPUT.txt -
```

Expected independent certificate:

```text
9e59de37b4ae54c496d84c32dddd7ef0fd8e71b9a5a7e8c1b590a304c72ef5bf
```

At the assigned source commit I also ran `verify_chain.py`,
`verify_git_history.py`, both top-level unittest suites, and all nine pinned
source/review verifiers. All passed. The required aggregate digests were:

```text
1d21c61a84c4357c1062d60a105d99284195c7235e1e5b2a79dbef0a128a8be2
c421c281d6b37b91a95015cf1b48f2aeeee5632ba5ba04fc20d6659a982517cb
```

This establishes replay and provenance, not the external topology by itself.

## Lean theorem/evidence alignment

All five exact commits build with Lean 4.33.1, match their expected output,
and pass their `SHA256SUMS` manifests.

| Height | Artifact / source commit | Kernel-checked content | External interface |
|---:|---|---|---|
| 2055 | `bafkreicp56...`, `5c71483...` | The supplied five-face incidence list, K5 complement, the two supplied terminal profiles, and final integer arithmetic. Four finite theorems report no axioms. | Does not derive the face list, distinctness, sealing, or profile completeness. |
| 2059 | `bafkreicsjf...`, `6581869...` | Adds exact vertex links and degree signatures for the supplied complex. Five theorems report no axioms. | Does not prove that these links arise from every admissible drawing or invoke a general disk theorem. |
| 2061 | `bafkreiavlsa...`, `bf54d4a...` | Adds face-dual connectivity and the single nonrepeating boundary cycle. Six theorems report no axioms. | Drawing-to-complex and topology remain external. |
| 2069 | `bafkreihufw...`, `ba7b8c9...` | Adds an exact five-step shelling witness, including full shared-edge/shared-vertex checks. Seven theorems report no axioms. | The elementary triangle-gluing theorem and the geometric face trace remain external. |
| 2073 | `bafkreiez6q...`, `2675bc9...` | Universally exhausts every natural-valued record satisfying `FeasibleDeletionProfile`, not just the two instances. The finite certificates are axiom-free. The universal `omega` lemmas expose `propext`, `Quot.sound`, and for exhaustion `Classical.choice`. | Validity and completeness of the mathematical encoding, PRTT equality classification, and all drawing topology remain external. |

Thus no Lean artifact quantifies over drawings or proves that every admissible
drawing maps to the face complex. Height 2073 does quantify over every encoded
arithmetic profile; the mapping from a drawing to that predicate is a
mathematical interface. Describing the whole height-2073 development simply
as “axiom-free” would be inaccurate under a strict `#print axioms` reading,
although it uses no custom axiom or oracle.

## Counterexample and degeneracy attempts

- **Loops / adjacent crossings / repeated crossings / triple points:** excluded
  by crossing-minimal good-drawing normalization and inherited by deletion.
- **Parallel planarization edges:** excluded separately for each possible pair
  of endpoint types; 1-planarity rules out a segment joining two crossing
  vertices.
- **Disconnected planarization / bridges / non-cellular face walks:** equality
  at the simple planar maximum forces connected maximal planarity, hence
  3-connectedness for these orders and triangular 3-cycle faces.
- **Repeated kite or pentagon vertices:** four kite endpoints are distinct;
  every possible identification of `u` violates goodness or creates a loop.
- **Coincident crossings:** excluded by the good drawing; all five crossing
  incidences remain pairwise distinct.
- **Orientation/gluing failure:** opposite internal darts cancel; every shell
  attachment meets the prior complex in exactly one connected proper boundary
  arc, including the final two-edge arc.
- **A survivor from another `C5` used as an exceptional side:** impossible by
  the sealed full-pentagon disk, including the boundary-vertex entry case.
- **A `K2` component becoming a free side:** neither of its edges is deleted,
  so both remain crossed in `T`.

No attempted degeneration survives all hypotheses.

## Trust boundary and evidence classification

Independently established in this review: primary-statement alignment;
frontier endpoint arithmetic; a fourth recursive convex-table computation;
actual-`x2` profile enumeration; deletion multiplicities; both terminal
planarizations; local shell incidence; the drawing-to-face trace; vertex
distinctness; and the sealed-disk provenance argument.

Inherited mathematical inputs: the full proofs of Sadhu Theorem 1.3,
Büngener--Kaufmann Theorem 6 and Propositions 21/23, PRTT Lemmas 3.1/3.2, and
Ackerman Theorem 4; standard good-drawing normalization; and the standard
two-circle drawing of `K27`. Relevant proof passages and hypotheses were
checked against the primary texts, but those long published/preprint proofs
were not re-formalized.

Executable trust: CPython 3 arbitrary-precision arithmetic and hashing; Lean
4.33.1 and its kernel/standard library; and Git object/hash/ancestry semantics.
The supplied Python and Lean programs do not prove Jordan separation or the
mapping from drawings to encoded objects.

## Literature overlap and publishability

The live primary-literature search found Sadhu's September 2026 paper, whose
stated frontier stops at orders 53/54, and earlier results through `r<=24` or
`r<=26`; it found no primary paper claiming `r=27` or `cr(24,132)>=165`.
PRTT Conjecture 5.7 specializes at `(v,e)=(24,132)` to exactly 165, so the
local endpoint is also a new finite case of that published conjecture.
This supports search-relative novelty, not a historical-priority guarantee.

- **Correctness:** high confidence after full-chain audit.
- **Novelty/importance:** potentially strong; it advances the current
  primary-literature boundary from 26 to 27 and proves a nontrivial endpoint
  case of PRTT Conjecture 5.7.
- **Exposition:** not yet journal-ready. The proof is distributed over many
  artifacts, and the decisive topology is too compressed.
- **Reproducibility:** strong for arithmetic, hashes, history, and finite Lean
  objects; intentionally incomplete for drawing topology.
- **Required repairs:** consolidate the chain into a paper-style proof; add a
  labeled rotation/face diagram; state and prove the planarization-simplicity,
  drawing-to-five-face, and sealed-disk lemmas; give the exact `E0/m0`
  definition from Büngener--Kaufmann; state “finite simple graph” in the main
  theorem; and report Lean axioms/interface boundaries precisely.

Subject to those specific repairs, the result is suitable for specialist
peer review and submission. Because of its significance and the external
topological interface, a second referee specializing in topological graph
drawing would still be prudent.
