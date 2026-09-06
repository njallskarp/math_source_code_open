# Independent review of full Ramsey lifting through three degree matrices

## Review verdict

Accepted within its stated conditional domain: height 3311's general
support/gluing theorem, complete guarded H92 interface, and physical
counterexample to pairwise nonemptiness. The actual generated interface
is checked entrywise, including every visible guard and hidden literal.
The two physical fixtures are checked independently on all 8,192 hidden
colorings, and the oracle's actual outputs are checked for both fixtures.

Target:
bafkreicb3qhheg2qpddyu4sxzvobd6l7vkkfk4nagk3lxf4drz3sowun34.
[Author source](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_antipodal_block_gluing),
commit 815b79be8f879d2bff7baa52b1132f9a0e115e64.

This pass had independently derived the same structural interface before
that contribution appeared in the committed graph. The new result
triggered a change to independent review; this package does not claim
another original theorem. The proof below is the reviewer's self-contained
restatement. The author's physical obstruction is stronger than the
abstract quantifier example initially used by the reviewer.

The generic oracle and H92 adapter were read, but their complete software
contracts and all malformed-input/termination paths are not certified by
these two fixture runs. The author's separate regression and negative-control
suites are not rerun or adopted wholesale. No H92 satisfiability result
or whole-branch coverage follows.

## Result and exact scope

For the fixed H92 core and three root stars used by the reviewed
104-edge projection, full Ramsey lifting has an exact binary
compatibility interface. Every retained assignment extends to a
43-vertex Ramsey \((5,5)\) coloring with the specified degrees and
densities if and only if:

1. Its retained-only degree, density, and global five-set conditions hold.
2. There is a triangle in a specified tripartite compatibility graph
   whose vertices are individually admissible labeled degree matrices.

The three matrices need not be enumerated to state or prove this
criterion. Every unknown-edge monochromatic-five-set condition touches
at most two matrices. A one-matrix condition has at most six literals;
a two-matrix condition has at most three. All three pairs of matrices
actually occur in the literal H92 constraint system.

This supplies a complete full-\(K_5\) interface, not just more local
necessary conditions. It does not prove that the interface is
satisfiable, faster to solve, or semantically irreducible. No solution
of the previous subsystem, family exclusion, or Ramsey graph is
claimed. The H92/core/star/degree/density assumptions are still a
conditional family, not a proved cover of an entire \(M=214\) branch.

## Fixed labeled domain

Use \(V=\{0,\ldots,42\}\), red \(=1\), blue \(=0\), and the exact
92-edge graph on \(H=\{0,\ldots,19\}\) in [H92.json](H92.json).
Its upstream byte SHA-256 is
926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466.
Set

\[
W=\{2,\ldots,9\},\quad D_0=\{10,\ldots,13\},\quad
D_1=\{14,\ldots,17\},\quad D_{01}=\{18,19\},
\]

\[
X=\{20,\ldots,28\},\quad Y=\{29,\ldots,37\},\quad
Z=\{39,\ldots,42\}.
\]

Prescribe the red root neighborhoods

\[
N_R(0)=D_0\cup D_{01}\cup Y\cup Z\cup\{38\},\quad
N_R(1)=D_1\cup D_{01}\cup X\cup Z\cup\{38\},\quad
N_R(38)=H.
\]

All other root incidences are blue. Together with H92 these give
276 fixed pairs. Partition the other 627 pairs into

\[
E_0=Z\times W,\qquad E_1=D_0\times X,\qquad E_2=D_1\times Y
\]

and the retained set \(E_*\). Unordered pairs are understood;
the three block vertex sets are disjoint. The block sizes are
32, 36, 36, leaving \(|E_*|=523\).

Fix any assignment \(x\in\{0,1\}^{E_*}\), without assuming it solves
the previous subsystem. Each matrix \(M_i\in\{0,1\}^{E_i}\) uses the
displayed physical row and column labels. No row/column sorting,
automorphism, canonical representative, profile quota, or additional
fixed graph is imposed.

Let \(d^*(v)=20\) at \(0,1,38\) and \(21\) elsewhere, and define

\[
r_x(v)=d^*(v)-\sum_{\substack{e\text{ fixed}\\v\in e}}c_e
                  -\sum_{\substack{e\in E_*\\v\in e}}x_e.
\]

Write \(D(x)\) for both of the following requirements:

- \(r_x(v)=0\) for \(v\in\{0,1,18,19,38\}\).
- The blue neighborhoods of roots 0 and 1 each have 124 red edges.

The latter counts depend only on fixed colors and \(x\): every
removed edge joins complementary root signatures and therefore
belongs to neither blue neighborhood's induced graph.

## Complete physical case partition

For every five-set \(S\subseteq V\) and color \(c\in\{0,1\}\), first
discard the record \((S,c)\) if a fixed pair of \(S\) has color \(1-c\).
Such a monochromatic set is already impossible.

For every remaining record put

\[
T_*(S)=\binom S2\cap E_*,\qquad
T_i(S)=\binom S2\cap E_i,\qquad
I(S)=\{i:T_i(S)\ne\varnothing\}.
\]

It is enabled at \(x\) if \(x_e=c\) for every \(e\in T_*(S)\).
An enabled record requires exactly

\[
\bigvee_{i\in I(S)}\ \bigvee_{e\in T_i(S)}(M_i(e)\ne c).
\]

An empty disjunction is false. Thus a zero-block record is not
automatically satisfied: it is a condition on \(x\) itself.
Let \(Q(x)\) mean that no zero-block record is enabled.

The record partition is defined directly on every physical five-set
and both colors. It is not a deduplicated CNF, an isomorphism census,
or a count of constraints remaining after specializing \(x\).

## General support-arity lemma

Suppose the still-uncolored pairs are precisely the union of
vertex-disjoint complete bipartite blocks. A five-set can contain pairs from at most two blocks:
each touched block needs at least two of its vertices, so three blocks
would require at least six vertices.

Within block \(L_i\times R_i\), the unknown pairs of \(S\) form exactly
the rectangle

\[
(S\cap L_i)\times(S\cap R_i).
\]

For a one-block record, if these side sizes are \(a,b\), then
\(a+b\leq5\) and \(ab\leq6\). The possible positive widths are
1, 2, 3, 4, and 6, not 5.

For a two-block record, the occupied block-vertex counts are either
\((2,2)\), with a possible fifth vertex outside those two blocks,
or \((3,2)\) in some order. The corresponding unknown-edge counts are
\((1,1)\) or \((2,1)\). In the latter case the two pairs within one
block share an endpoint. Therefore every cross-block clause is a
monotone clause of width two or three after \(x\) is fixed.

The proof uses vertex-disjointness, not merely disjoint edge sets.
It also specifically uses five vertices: a six-set can touch three
disjoint blocks. More generally a \(k\)-set touches at most
\(\lfloor k/2\rfloor\) such blocks.

The width bounds are sharp at the literal H92 level. The red record
\(\{2,3,4,39,40\}\) has six unknown pairs in \(E_0\); the red record
\(\{2,3,15,29,39\}\) has two in \(E_0\) and one in \(E_2\).
Neither is blocked by the fixed colors. These are individual record
witnesses, not retained assignments satisfying all other constraints.

## The compatibility-triangle theorem

For the given \(x\), let \(\mathcal F_i(x)\) consist of all labeled
binary matrices on \(E_i\) such that:

- Each row and column sum is the corresponding \(r_x(v)\).
- Every enabled record with \(I(S)=\{i\}\) is satisfied.

Margins outside their feasible range simply make this set empty.
This domain is a subset of the degree-only matrix domain. Strictness
for a feasible H92 retained assignment is not asserted here.

For \(i<j\), put an edge between \(M_i\in\mathcal F_i(x)\) and
\(M_j\in\mathcal F_j(x)\) exactly when they satisfy every enabled
record with \(I(S)=\{i,j\}\). This defines a labeled tripartite
compatibility graph \(\Gamma_x\).

**Theorem.** The full colorings extending the fixed pairs and \(x\),
having the prescribed degrees and the two densities, and containing
no monochromatic \(K_5\), are in bijection with the triangles of
\(\Gamma_x\) if \(D(x)\wedge Q(x)\) holds. If either condition
fails, there are no such colorings. In particular,

\[
x\text{ has a full admissible Ramsey lift}
\quad\Longleftrightarrow\quad
D(x)\wedge Q(x)\wedge\bigl(\Gamma_x\text{ contains a triangle}\bigr).
\]

**Proof.** Every completion gives exactly one matrix on each physical
block. Its degrees and marked densities imply the row/column margins and
\(D(x)\). Every possible monochromatic five-set is in exactly one
of the zero-, one-, or two-block record classes by the support lemma.
Avoidance of these classes respectively gives \(Q(x)\), membership
in each \(\mathcal F_i(x)\), and all three compatibility edges.
Thus the matrices form a triangle.

Conversely, fix such a triangle and assemble its three matrices
with the fixed coloring and \(x\). There is no conflicting physical
edge because the pair sets are disjoint. The margins and \(D(x)\)
give every degree and density. A monochromatic five-set cannot have
a wrong-color fixed pair or a wrong-color retained pair. Its enabled
record would therefore violate \(Q(x)\), a matrix's unary condition,
or a triangle edge, exhausting all cases. None exists. Matrix entries
are precisely the remaining physical edges, proving the bijection.

For an \(x\) satisfying the complete projected subsystem at height
3256, its degree-only lifts exist and \(D(x)\) already holds. Its
full-Ramsey lifting test is still \(Q(x)\) and a triangle of the
unary-constrained, mutually compatible domains above. A valid full lift also
satisfies all six root-neighborhood constraints automatically:
a same-color four-clique combines with the root, and an opposite-color
five-clique is already globally forbidden.

The theorem does not authorize replacing triangle existence by
nonemptiness of each of three pair relations. The elementary abstract
example \(M_0=M_1\), \(M_0=M_2\), \(M_1\ne M_2\) on two-element
domains has support for every state on every edge but no joint
triple. This is a quantifier warning, not a claimed realization by
H92 matrices or a counterexample to feasibility of its subsystem.

## Independently regenerated finite support certificate

[verify.py](verify.py) imports no upstream executable code and uses
only the bundled literal H92 data and the standard library.
One generator scans all 962,598 five-sets and their ten pairs.
The other enumerates possible cliques by bit-intersection recursion
and recovers block support by complementary root-signature
occupancies rather than the first generator's block-edge dictionary.
The complementary-signature construction also reproduces the complete
pair-to-block mapping, checking the literal ownership of all 903 pairs.
Outside residual vertices and density independence are checked directly.

Every physical color record is compared entrywise, including rejected
records. The colexicographic address of
\(S=\{s_0<\cdots<s_4\}\) and color \(c\) is

\[
2\sum_{j=0}^4\binom{s_j}{j+1}+c.
\]

The direct scan independently checks that these addresses cover the
whole range without collisions. Each byte is zero for a discarded
record, or \(8+\text{block mask}+16\,\text{unknown-pair count}\).
The exact atlas has 1,925,196 bytes; it is regenerated in memory,
not published.

| Touched blocks | Blue records | Red records |
|---|---:|---:|
| None | 107186 | 112419 |
| 0 | 56310 | 63076 |
| 1 | 53736 | 53016 |
| 2 | 55764 | 51006 |
| 0, 1 | 11016 | 8532 |
| 0, 2 | 10566 | 8982 |
| 1, 2 | 8829 | 10611 |

There are 611,049 possible-color records: 219,605 zero-block,
332,908 one-block, and 58,536 two-block. Of the latter, 32,346
have width two and 26,190 width three. All three block pairs occur.
This is syntactic occurrence before assigning \(x\), not a proof
that each pair relation remains nontrivial on feasible domains.

Atlas SHA-256:
c76942bd898e56b3a4f633d12267f1d165a2b374bc1bf1d459c45c57dfc07f50.

All 20,784 local truth assignments over the 27 occurring
retained/unknown support shapes agree with the enabled-record rule.
All 4,096 abstract binary-relation triangles on two-element domains
agree with a separate common-neighbor test. Five negative controls
reject omitted/extra records, changed support, changed width, and
overlapping blocks. These validate the implementation; the universal
lifting proof is the argument above, not an inference from a table.

## Exact interface and physical-obstruction review

[review.py](review.py) downloads five hash-pinned, inspected producer/input
files into a temporary directory and executes the producer in a separate
process. The independent review process imports no upstream executable
module. It reconstructs every schema field, including all physical pairs,
row-major local edge labels, residual equations, targets, and densities.
It unpacks every actual JSONL record and compares the complete unique
physical clause set. Extra, duplicate, out-of-order, or missing clauses
fail the comparison; visible guard literals are not discarded.

The distinction between the independent physical-record atlas and the
author's unique-clause stream is exactly 267 duplicate occurrences.
There are 610,515 clauses represented once and 267 represented twice;
every duplication is in the zero-block class. Thus both counts agree:
611,049 physical records and 610,782 unique clauses. This is not a
correction to the author, who explicitly reports unique clauses.

The complete 30,487,019-byte generated interface matches SHA-256
2192a68adb96d80cee3ded6c7503b5c96a81b771299500c9e3c58e594519f6b6.
Its independently reconstructed full schema matches SHA-256
ee1fa61df8ca667e348f3d3acf99136a26f0b96705e19f035dd18f86c05d15f2.
Neither generated file is published in this review.

The bundled [negative fixture](negative.json) and
[positive fixture](positive.json) are byte-identical to the author's.
They have 12 vertices and holes
\(\{0,1\}\times\{2,3\}\), \(\{4,5\}\times\{6,7\}\), and
\(\{8,9\}\times\{10,11\}\). All row and column margins are one,
so the margin-correct block states are row-major masks 6 and 9.
The independent physical checker obtains

\[
\mathcal F_0=\mathcal F_1=\{6,9\},\qquad \mathcal F_2=\{6\},
\]

\[
R_{01}=\{(6,9),(9,6),(9,9)\},\qquad
R_{02}=R_{12}=\{(6,6)\}.
\]

Every domain and pair relation is nonempty, but the two latter relations
force a pair absent from the first. Every one of the eight margin-correct
full graphs has an explicitly checked blue \(K_5\). Changing only visible
edge \(\{0,4\}\) from blue to red produces exactly five valid lifts:

\[
(6,9,6),\ (6,9,9),\ (9,6,6),\ (9,9,6),\ (9,9,9).
\]

For both fixtures the checker enumerates all 4,096 hidden colorings,
compares their literal full-graph truth values to the factored constraints,
and checks every domain, pair relation, and margin-correct lift. It also
compares the actual author's oracle outputs, decodes its positive graph
edge by edge, and verifies that budget zero returns INCOMPLETE rather
than an exclusion. These tests make no claim about global minimality,
43-vertex realizability, or a counterexample to arc consistency.

## Reproduction and trust boundary

Use CPython 3.12.12 and its standard library. The structural atlas is
fully offline. The entrywise author-interface replay downloads the five
pinned upstream files and automatically cleans its temporary generated
state. No solver, randomness, or external graph package is used.
From this directory:

~~~bash
set -o pipefail
python3 -B verify.py | cmp - EXPECTED.json
python3 -O -B verify.py | cmp - EXPECTED.json
python3 -B review.py | cmp - EXPECTED_REVIEW.json
python3 -O -B review.py | cmp - EXPECTED_REVIEW.json
shasum -a 256 -c SHA256SUMS
~~~

[EXPECTED.json](EXPECTED.json) and
[EXPECTED_REVIEW.json](EXPECTED_REVIEW.json) are the compact outputs.
The source verifies the exact bundled input identity before use.
No H92 matrix domain, complete 523-bit assignment, or canonical Ramsey
family is enumerated. The two atlas algorithms were written and run by
the same reviewer and are internal cross-checks. This package supplies
external review of the different author's height-3311 contribution,
not formal verification.

The displayed proof, faithful physical definitions, CPython integer
and iteration semantics, parsing, hashes, and ordinary hardware
remain trust boundaries. No speedup, practical domain-size bound,
or SAT/UNSAT statement follows from the certificate.

## Provenance, prior art, and coverage boundary

The exact H92 input and the three-block projection are from
[Helgi's public projection](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_antipodal_degree_projection),
commit 40a6cd7ffbe45892bd52e3dfcdbb086f1b5afbfd, graph height 3256,
bafkreidufm26hzufnaopoyiorhpdgiwei7pk6uuv56cpewvjlqrofir6fq.
Its full proof, model, and input were inspected. That result correctly
limits its independent flows to the degree-only subsystem; this
contribution does not allege an error in it.

The physical projection was independently accepted at height 3266:
[review source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_antipodal_projection_review),
commit 31e969ac6b6d78f9dc0f50ab53242ea863496ea3,
bafkreihowil3ijiqegbezgvnvpror7gbgxjrkwp7l5poqg3qhtxcugdshe.
The auxiliary backend was accepted at height 3287:
[backend review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_antipodal_backend_review),
commit 7e2118e9a77a64d264a14bc81e1c220905bb06ee,
bafkreidtocs6ibmkqbtfx4rslzkpjmo72ou7jehctrgtnd76cgvea5p7pq.
Neither audit nor the producer's UNKNOWN is imported as a solver
verdict here.

Relational compatibility and the difference between local and global
consistency are classical; compare
[Dechter and Pearl's primary constraint-clustering paper](https://cdn.aaai.org/AAAI/1988/AAAI88-027.pdf).
Ramsey gluing with all forbidden-five-set constraints is also standard;
see [Angeltveit and McKay, Sections 2 and 5–7](https://arxiv.org/html/2409.15709v2).
No priority is claimed for binary constraint networks, elementary
support counting, or gluing. The contribution here is independent
acceptance and exact reproduction of this team's specific full-lift
interface and its physical obstruction, not a new general theorem.

Covered: all retained assignments and all full physical lifts in
the explicitly fixed H92/star/degree/density family.
Uncovered: existence in that family and any proof that this family
captures every coloring in a complete \(M=214\) branch. The working
bound remains \(43\leq R(5,5)\leq46\).

This is separate from slots 1/2's direct search and enlargement,
slot 5's inter-lane composition, and Helgi's construction experiments.
The next falsifiable consumer test is to feed an actual projected
subsystem solution into this exact interface and produce either a
full physical lift or a checkable incompatibility certificate covering
all three labeled matrix domains. Until such a solution or a new
complete branch normalization is available, do not replace this
missing input by more support or margin tables.
