# A four-unit triangle gap excludes complete M214 root 376

The full Boolean root with zero-based index **376**, key
`C77partition,13,0,AB`, has no completion. Its incidence conditions imply

\[
t_R(u)+t_R(v)\le196,
\]

whereas the intrinsic \(M=214\) branch requires both totals to equal 100.
This proves the Boolean selector cut \(x_{13621}=0\) in the height-3160
integrated formula. The inequality is a necessary bound, not a claim that
196 is attainable. Using the inherited \(U(21)=107\) terminology, it gives
\(\delta_R(u)+\delta_R(v)\ge18\), contradicting the required sum 14.
The literal triangle contradiction does not need that catalog extremum.

Every full graph constraint and all 903 physical edges belong to the root
being excluded. All 820 non-anchor edges, including all 78 common-core edges,
remain variables. No core graph, attachment, symmetry representative, or
outside completion is chosen. A contradiction in necessary consequences
therefore excludes every complete realization of the descriptor.

Together with the independently accepted
[root 375 exclusion](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_partition_root375_exclusion),
this closes **both** patterns in the complete `C77partition,c=13,k=0`
parameter case. There are **387 remaining candidate descriptors**, with
family counts \((60,85,70,104,68)\). These are candidate counts; their
feasibility is not established. No complete \(M\)-slice or Ramsey bound changes.

## Physical root and exact identity

Use \(u=0,v=1\), \(E=\{2,\ldots,14\}\), and
\(C=\{0,1,15,\ldots,42\}\). Red is one. The eight anchor cells are:

| Class | Common red H | u-only A | v-only B | Common blue O |
| --- | --- | --- | --- | --- |
| E | empty | 2–7 | 8–13 | 14 |
| C without anchors | 15–27 | 28 | 29 | 30–42 |

Write \(H=\{15,\ldots,27\}\), \(p=28\), \(q=29\), and \(z=14\).
The whole off-diagonal cells are
\(A=\{2,\ldots,7,p\}\) and \(B=\{8,\ldots,13,q\}\), each of size seven.
The root makes \(uv\) red and \(pq\) blue, and requires

\[
x_{wp}+x_{wq}=1\quad(w\in C\setminus\{p,q\}).
\]

It also has all red/blue five-clique prohibitions, degrees 20 on \(E\) and
21 on \(C\), red local triangle counts 93 on \(E\) and 100 on \(C\),
and all equations for \(a(w)=|N_R(w)\cap E|\): seven at \(p,q\), six
elsewhere. `root.json` is this complete inherited descriptor.

Let \(e_A,e_B,e_H\) count red edges in the indicated cells and put
\(s=|N_R(z)\cap H|\). The thirteen core vertices all have \(a(h)=6\), so
there are 78 red edges from \(H\) to \(E\). Hence the contribution from
\(H\) to the twelve exceptional vertices in \(A\cup B\) is \(78-s\).
All core vertices are central, so the anomaly partition contributes exactly
13 red edges from \(H\) to \(\{p,q\}\). Consequently

\[
e_R(H,A\cup B)=91-s.
\]

The red neighborhoods of \(u,v\) are respectively
\(\{v\}\cup H\cup A\) and \(\{u\}\cup H\cup B\). The red edge
\(uv\) and the common core contribute thirteen triangles at each anchor.
Adding the two triangle totals gives the exact physical identity

\[
t_R(u)+t_R(v)=2e_H+117-s+e_A+e_B.
\]

No arbitrary external edge or local triangle equation has been dropped from
the complete root: most are simply unnecessary for this implication.

## Three elementary bounds

**Common-core degree bound.** A red triangle in \(H\) together with the
anchors is a red five-clique, so \(H\) is triangle-free. The red neighbors
of any core vertex are independent; there can be at most four, since the
whole graph has no independent five-set. Summing thirteen degrees gives
\(2e_H\le52\). Core regularity or uniqueness is unnecessary.

**Outside footprint bound.** The classical elementary inequality
\(R(3,4)\le9\) implies \(s\ge5\). Otherwise nine core vertices blue to
\(z\) contain an independent four-set, which together with \(z\) is a
blue five-clique. To recall a self-contained proof of the small bound:
\(R(3,3)\le6\) follows from three same-color neighbors. A triangle-free
graph on nine vertices with independence number at most three has degrees
at most three. A degree at most two leaves six nonneighbors, containing an
independent triple and thus an independent four-set with the original
vertex. Every degree would therefore be three, contradicting parity.

**Off-diagonal edge bound.** Both \(A\) and \(B\) are \(K_4\)-free,
since a red four-clique extends through its anchor. A \(K_4\)-free graph
on seven vertices has at most sixteen edges. If it contains a triangle,
there are at most eight edges from that triangle to the other four vertices,
and at most five edges among those four; the total is at most \(3+8+5=16\).
If it is triangle-free, choose an edge: the other five vertices contribute
at most five incident edges to its endpoints and at most ten internal edges,
again at most sixteen. The edgeless case is immediate. Thus
\(e_A+e_B\le32\).

Substituting gives

\[
t_R(u)+t_R(v)\le52+117-5+32=196<200.
\]

This is a complete-root contradiction using triangle aggregation. No
classification of core graphs or external catalog payload is used.

## Exact certificate and its checker

`certificate.json` is an exact integer Farkas certificate on the four scalar
coordinates \((e_A,e_B,2e_H,s)\). The four inequalities are

\[
e_A\le16,\quad e_B\le16,\quad 2e_H\le52,\quad -s\le-5.
\]

The root's required triangle sum and the physical identity give

\[
e_A+e_B+2e_H-s=83.
\]

The 1,110-byte scalar certificate has SHA-256
`21e4db1f231bbde4697d571014495703e9cc2ff33cafce058ef3934b9812fb80`.
Adding all four inequalities and subtracting the equality yields
\(0\le-4\). The checker validates all multipliers, nonnegativity, physical
coefficients, and exact cancellation using integers. No numerical LP solver
or floating-point reconstruction is involved.

The finite justifications are replayed independently of root generation:

- 286 core triangle prohibitions, 10,296 five-neighbor degree caps, and
  70 off-diagonal four-clique prohibitions pass reverse unit propagation
  against actual physical five-clique clauses and anchor units.
- The seven-vertex edge bound is checked on every graph with at least
  seventeen edges: exactly 7,547 graphs, specified by their at most four
  missing edges. Every one has a four-clique. A sixteen-edge complete
  tripartite graph with part sizes \(3,2,2\) verifies the sharp boundary.
- The 5,127-byte `r34.rup` proof, reused unchanged from the reviewed root375
  package, has 288 addition-only RUP steps. The checker separately verifies
  all 70 degree caps and 93 star normalizations needed to make that small
  lemma cover every nine-vertex graph, not a chosen core.
- All 715 physical nine-vertex embeddings in \(H\), totaling 150,150
  triangle/four-set clause checks, justify the footprint bound. Every one of
  the 8,192 footprint assignments is covered; all 4,096 assignments to a
  twelve-bit core star are covered by the degree caps.

The RUP trace SHA-256 is
`d43100027074653e039bff7705e62c31c0f7fa370cda0c9a8ff52f27a33619a7`.
Its small interpreter is in `check_rup.py`. The new proof uses this complete
public trace and the displayed exact finite arguments; no omitted native
UNSAT trace is needed.

## Full parent provenance and reproduction

`audit.py` imports no producer or inherited graph decoder. It independently
reconstructs the complete descriptor, physical edge and triangle indices,
source-row locations, scalar identity, local proofs, and exact Farkas sum.
It checks **9,220 required rows** in the full height-3160 OPB:
2,358 five-clique clauses, 83 anchor units, 26 core-incidence guard rows,
26 partition guard rows, 6,724 triangle-product rows for 1,681 triples,
two anchor triangle-total equations, and the selector exactly-one row.
The four product inequalities are checked on all sixteen Boolean states;
their physical substitution reduces all anchor triangle variables exactly.

The entire 172,788,992-byte, 2,044,421-row parent stream is identity-checked
with SHA-256
`469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f`.
Unused parent rows are hashed, not independently semantically rederived by
this new auditor. Every necessary row used by the proof is reconstructed and
matched. The scalar identity has 133 nonzero physical edge coefficients.

Use CPython 3.12 and its standard library. From a full source checkout, choose
a new scratch directory outside the checkout:

```sh
python3 -B ramsey_r55_m214_partition_root376_triangle_certificate/reproduce.py \
  /tmp/r55-root376-replay
```

The command regenerates the complete parent OPB and root descriptor, runs
controls, checks the whole proof, compares exact expected outputs, and emits
`cut.opbpart`. The observed fresh replay took about 17 seconds and used about
173 MB of generated disk state. No solver, catalog download, external data,
binary, private run state, or large certificate is required.

```text
status = EXACT_COMPLETE_M214_ROOT376_TRIANGLE_EXCLUSION
root_index = 376
root_core_variables_fixed = 0
source_rows_verified = 9220
anchor_triangle_upper_bound = 196
required_anchor_triangle_sum = 200
farkas_rhs = -4
remaining_root_descriptors_with_reviewed_root375_cut = 387
```

The cut is `-1 x13621 >= 0 ;`. Appending it to an OPB also requires increasing
the header's constraint count by one; the suffix is not a standalone formula.
The two-pattern census is checked against all 389 table rows. Counting 387
uses the previously reviewed root375 cut as an explicit additional premise;
the new certificate alone excludes root376.

Normal and optimized Python outputs agree. Controls check the identity on
256 full physical assignments with only inherited anchor units fixed, check
44 selector guard cases, and reject nine certificate/scope corruptions.
Additional source controls rejected an altered required OPB clause and a
truncated parent stream. The random full assignments are algebra controls,
not Ramsey witnesses.

## Dependencies, literature, and review status

The [height-3148 root normalization](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_normalization),
source commit `9a9d4c3234d3fbe196ff4b413df831c587bd7653`, fixes the descriptor.
The [height-3160 integrated formula](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_integrated_pair_roots),
source commit `2f9f6cd51ab620f4d19063c541a38ccb8e8a7f7b`, fixes the Boolean
physical system. The root generator, table, and parent generator are
hash-pinned. Root375's source commit is
`c433b0278afc99e20e2a4862961055c5c63f95f5`; its independent acceptance is
Discovery Net h3453. That review does not review this new root376 certificate.

The literal obstruction needs no catalog completeness. Applying the reduced
root cover to every intrinsic \(M=214\) graph still imports the h3062/h3130
selection and h3148 normalization theorem, including the separately stated
\(U(14)=60\) premise. This package does not reprove that coverage theorem.
The optional deficiency wording also imports \(U(21)=107\); the triangle
proof itself does not.

Primary literature was checked after graph-grounded selection, including
[Angeltveit–McKay's LP and pointed-gluing proof](https://arxiv.org/html/2409.15709v2).
The small Ramsey bound, Turán bound, triangle double count, and Farkas method
are classical. This is their exact application to the complete marked root;
no general-method or historical priority claim is made.

Evidence is author-checked exact mathematics, finite certificate replay,
physical source reconstruction, and definition-level cross-checks. External
review of this result is pending. The displayed proof composition, Python
implementations and integer/text semantics, ordinary hardware, and hashes
for identity remain trust boundaries. This is not a proof-assistant theorem.

Covered: all full completions of root376, and, with the reviewed prior result,
both partition patterns at \(c=13,k=0\). Uncovered: the other 387 candidate
roots, every full hard \(M\)-slice, and the low-deficiency branch. The next
milestone is a complete surviving-root decision or a further strict
triangle/deficiency separator with a complete-family effect. Two subsequent
passes yielding only incremental rows or no exact qualifying outcome trigger
reassessment and the next principal-ranked target.
