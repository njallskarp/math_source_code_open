# A complete Boolean \(M=214\) partition root is impossible

The complete root with zero-based index **375**, key
`C77partition,13,0,HO`, has no Boolean completion. In the height-3160
integrated formula this proves the selector cut

\[
y_{375}=x_{13620}=0.
\]

All 903 physical edges and every intrinsic graph constraint belong to the
root being excluded. All 820 non-anchor edges, including all 78 edges of its
common red core, remain variables. The proof extracts an inconsistent weaker
16-vertex subsystem; it makes no choice of an internal core graph or an
outside completion. Consequently the exclusion applies to every full
completion of this descriptor and every Boolean strengthening of that root.

Deleting this descriptor leaves **388 candidate descriptors**, with family
counts \((60,85,70,104,69)\). These counts do not assert feasibility of the
remaining descriptors. No entire \(M\)-slice or Ramsey bound is settled.

## The complete root and the local obstruction

The parent labels are \(u=0,v=1\),
\(E=\{2,\ldots,14\}\), and
\(C=\{0,1,15,\ldots,42\}\). Adjacency types relative to the ordered anchors
are \(H=(1,1),A=(1,0),B=(0,1),O=(0,0)\), with red represented by one.

| Class | H | A | B | O |
| --- | --- | --- | --- | --- |
| E | empty | 2–7 | 8–13 | 14 |
| C without anchors | 15–27 | 28 | 29 | 30–42 |

The anomalies are \(p=15\) and \(q=30\). The edge \(uv\) is red, \(pq\)
is blue, and

\[
x_{wp}+x_{wq}=1\qquad(w\in C\setminus\{p,q\}).
\]

The full root also retains every red and blue five-clique prohibition,
degrees 20 on \(E\) and 21 on \(C\), red local triangle counts 93 on
\(E\) and 100 on \(C\), all 83 anchor units, and all 43 equations
\(a(w)=|N_R(w)\cap E|\): seven at \(p,q\), six elsewhere.
`root.json` is the complete inherited descriptor, not a completed graph.
No optional residual ordering is needed.

**Elementary lemma.** Every triangle-free graph on nine vertices has an
independent four-set. First, the usual three-neighbor argument proves
\(R(3,3)\le6\). Suppose a triangle-free nine-vertex graph had independence
number at most three. Every neighborhood is independent, so all degrees are
at most three. A vertex of degree at most two has at least six nonneighbors;
those six have neither a triangle nor an independent triple, since the latter
together with the vertex would be an independent four-set. This contradicts
\(R(3,3)\le6\). Every degree must therefore be three, contradicting the
handshake lemma on nine vertices. This proves the lemma without a catalog.

**Root exclusion.** Let \(H=N_R(u)\cap N_R(v)=\{15,\ldots,27\}\).
A red triangle in \(H\), together with \(u,v\), would be a red five-clique.
Also \(\alpha(H)\le4\). If \(p\) had at most three red neighbors in
\(H\), choose nine of its nonneighbors. The lemma supplies an independent
four-set among them; adding \(p\) gives an independent five-set. Thus
\(d_H(p)\ge4\). Four red neighbors of \(p\) are pairwise blue because
\(H\) is triangle-free. Each belongs to \(C\setminus\{p,q\}\), so the
partition makes each blue to \(q\). They and \(q\) form a blue five-clique,
a contradiction.

This argument only needs the upper partition inequalities
\(x_{wp}+x_{wq}\le1\) for \(w\in H\setminus\{p\}\). The lower halves
and the blue edge \(pq\) are retained in the replay kernel because they
are genuine root conditions; they are unnecessary for the displayed proof.
No uniqueness or classification of a thirteen-vertex core is imported.

## Compact certificate and full-formula provenance

The default reproduction is an exact, solver-free certificate audit using
Python's standard library. Its only stored proof trace is `r34.rup`:
**288 addition-only RUP steps**, 5,127 bytes, SHA-256
`d43100027074653e039bff7705e62c31c0f7fa370cda0c9a8ff52f27a33619a7`.
It ends in the empty clause. RUP checks a clause by assuming its negation and
deriving a conflict through unit propagation.

The normalized nine-vertex formula has all 84 triangle prohibitions, all
126 independent-four prohibitions, and five blue units from vertex zero to
vertices 4–8. `audit.py` proves 70 star-degree caps by RUP and checks all 93
stars of degree at most three under explicit permutations, including 3,348
edge transports and preservation of the full clause set. Thus these five
units are a complete normalization for the small lemma. They impose no
fixed core on the original root.

The physical root proof then checks:

- 286 triangle-free core clauses derived by RUP from actual five-clique
  prohibitions and anchor units;
- 495 RUP degree caps at \(p\), using the partition and blue-five clauses;
- all 220 nine-vertex nonneighbor embeddings of the small lemma, totaling
  46,200 clause checks, with explicit guarded weakening; and
- every one of the 4,096 assignments to the twelve incident core edges at
  \(p\), covered by a degree cap or a verified nine-vertex obstruction.

The weaker kernel consists of all monochromatic-five prohibitions on
\(\{0,1,15,\ldots,27,30\}\), its inherited anchor units, \(pq\) blue,
and its inherited partition equations. It has **8,794 clauses** and uses
the original physical edge identifiers in a 903-variable DIMACS namespace.
Its SHA-256 is
`f8cb7188cfe73a6c88adeb1930f0361c1022f874982bfa5b6c3d995e9724ae0f`.

For every input clause, the auditor locates its actual row in the complete
height-3160 OPB, substitutes \(x_{13620}=1\), and checks the exact
coefficients and right-hand side. It checks all 8,794 such rows and hashes
the entire 2,044,421-row, 172,788,992-byte parent stream:
`469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f`.
This supplies the implication from the full selected formula to the weaker
inconsistent kernel. The new auditor does not independently reconstruct
every unused parent row; the inherited C++ semantic checker was separately
rebuilt and passed on the complete regenerated stream.

`build.py` uses the pinned parent root generator. `audit.py` imports neither
that generator nor an inherited decoder: it reconstructs the descriptor,
physical indices, source-row positions, and proof obligations separately.
`check_rup.py` is the separate small proof interpreter. Normal and optimized
Python runs agreed. Controls rejected nine damaged proof/scope inputs,
checked eight selector truth-table cases, and compared 1,000 small RUP
instances against exhaustive Boolean semantics.

## Reproduction

Use a full checkout of this repository and CPython 3.12, standard library
only. From the repository root, choose a new work directory outside the
checkout:

```sh
python3 -B ramsey_r55_m214_partition_root375_exclusion/reproduce.py \
  /tmp/r55-root375-replay
```

The default run generates the full parent OPB and the kernel, executes the
controls, replays the compact proof, and compares exact output with
`EXPECTED_RESULT.json` and `EXPECTED_CONTROLS.json`. The observed fresh run
took about 21 seconds. It uses about 174 MB of generated disk state. The
principal expected fields are:

```text
status = EXACT_COMPLETE_M214_ROOT375_EXCLUSION
root_index = 375
root_core_variables_fixed = 0
source_rows_verified = 8794
r34_rup_rows = 288
incident_star_assignments_covered = 4096
remaining_root_descriptors = 388
```

`cut.opbpart` contains `-1 x13620 >= 0 ;`. To append it to an OPB, also
increase that OPB's constraint count by one; the suffix alone is not a
standalone formula. This cut is justified for Boolean models, with no claim
that the same inference holds for the earlier fractional moment relaxation.

## Separate native proof replay

A second proof route generated a standard ASCII DRAT refutation of the
same physical kernel using [CaDiCaL](https://github.com/arminbiere/cadical)
3.0.1, source commit `c60730422e758ef1cebe7aeddf2dda31c996bf04`.
[drat-trim](https://github.com/marijnheule/drat-trim), source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, verified it with `-U`
(zero RAT lemmas) and converted it to LRAT. Its separate `lrat-check`
executable also returned `VERIFIED`. The solver used `--plain --no-binary`;
the observed run additionally used a 120-second limit and finished in
77.24 seconds. DRAT and LRAT replay took 98.271 and 6.59 seconds.

To regenerate and check this optional second route, build those tools from
their primary source repositories outside this source checkout, then run:

```sh
python3 -B ramsey_r55_m214_partition_root375_exclusion/reproduce.py \
  /tmp/r55-root375-native-replay \
  --cadical /absolute/path/to/cadical/build/cadical \
  --drat-trim /absolute/path/to/drat-trim/drat-trim \
  --lrat-check /absolute/path/to/drat-trim/lrat-check
```

The wrapper requires the solver's UNSAT exit code and successful verdicts
from both proof checkers. It uses no time limit. `NATIVE_REPLAY.json`
records the observed tool commits, verdicts, times, and large-trace hashes.
The 497 MB DRAT trace and 327 MB LRAT trace are deliberately excluded from
publication, along with generated formulas and binaries. Optional replay
recreates them from public source and needs roughly 1 GB of free space.
Another platform may produce a different valid trace; the stored hashes
identify the observed traces, rather than being required output hashes.
The compact default certificate is complete without these omitted traces.

## Boundary fixtures, dependencies, and review status

The two small fixtures have no monochromatic five-clique, checked over all
3,003 and 4,368 five-sets. One has a twelve-vertex core and a degree-three
marked vertex. The other has a thirteen-vertex core and one allowed common
red neighbor of \(p,q\). They show why the core-size threshold and full
disjoint-star hypothesis matter to this local argument. They are graphs on
15 and 16 vertices, **not** full \(M=214\) models or witnesses for any
remaining root.

The descriptor belongs to the
[height-3148 normalization](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_normalization),
source commit `9a9d4c3234d3fbe196ff4b413df831c587bd7653`. Its selector and
physical formula are from the
[height-3160 integrated system](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_integrated_pair_roots),
source commit `2f9f6cd51ab620f4d19063c541a38ccb8e8a7f7b`.
The source files and root table are hash-pinned in the code. Deleting this
impossible root preserves the parent's existential cover even when other
anchor choices give the same graph a different descriptor.

The literal sixteen-vertex obstruction and the selected-formula exclusion
do not require upstream catalog completeness. Applying the remaining-root
cover to every graph in the intrinsic hard branch still depends on the
upstream selection and normalization theorem, including its sensitive
\(U(14)=60\) premise. This work does not independently review that theorem.

Primary literature was checked after selecting this graph-grounded target:
[Angeltveit–McKay](https://arxiv.org/html/2409.15709v2) and
[McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
The small Ramsey lemma and proof-certificate methods are classical. The
contribution is their exact application to this complete marked root, with
physical formula provenance; no historical priority is claimed for the
generic obstruction. The global bound remains \(43\le R(5,5)\le46\).

This is author-checked mathematical and computational evidence, awaiting
external review. The displayed proof, normalization/embedding composition,
Python and native checker implementations, ordinary hardware, and hashes
for identity remain trust boundaries. Neither proof route is a
proof-assistant formalization. Independent implementations and native
replay are cross-checks, not independent peer review.

The next falsifiable milestone is a complete decision of another surviving
marked Boolean root with its core unrestricted. Reassess this mechanism
after two passes with no complete-family effect, strict separator, or exact
admissible survivor, or if live review exposes a coverage/provenance defect.
