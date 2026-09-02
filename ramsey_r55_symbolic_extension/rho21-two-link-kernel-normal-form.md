# The exceptional \(\rho=21\) support projection has a two-link kernel normal form

## Result type

**Exact symbolic classification with a converse at the support-incidence
level.**  Work in the unique \(m=10,\rho=21\) branch of the exceptional
first singular fan.  Let

\[
X=N_R^G(w),\qquad Y=N_B^G(w),\qquad |X|=21,\quad |Y|=20.       \tag{1}
\]

The selected support system suppresses exactly to a pair of small marked
loopless multigraph kernels:

\[
J_X\text{ on }10\text{ clause nodes},\qquad
J_Y\text{ on }13\text{ triangle-occurrence nodes}.           \tag{2}
\]

The \(X\)-kernel has only two possible degree families,

\[
\boxed{(3,3,3,3,4,4,4,4,4,4)}                              \tag{3a}
\]

or

\[
\boxed{(2,3,3,4,4,4,4,4,4,4)},                             \tag{3b}
\]

according as the unique mixed \(3+1\) blue clause avoids or meets the
distinguished red triangle.  The \(Y\)-kernel has the single degree family

\[
\boxed{(2,3,3,3,3,3,3,3,3,3,3,3,3)}.                       \tag{4}
\]

Conversely, every marked kernel satisfying the conditions below reconstructs
an abstract selected-support incidence system with exactly the required
\(\rho=21\) degrees.  Thus (3)--(4) are a complete finite alphabet for this
projection.  They do **not** assert realizability in a two-colored
\(K_5\)-free Ramsey core.

## Imported \(\rho=21\) normal form

Orient colors so that the unique singular vertex has selected degrees

\[
(d_R^U(w),d_B^U(w))=(1,10).                                \tag{5}
\]

Write its unique selected red clause as

\[
R_0=\{w,a_1,a_2,a_3\},\qquad A=\{a_1,a_2,a_3\}\subset X.    \tag{6}
\]

The set \(A\) is a red triangle.  The ten selected blue clauses through
\(w\) are

\[
S_i=\{w\}\cup T_i,\qquad T_i\subset Y,\quad 1\le i\le10,   \tag{7}
\]

where the \(T_i\) are distinct blue triangles.  The one-flip theorem gives
three distinct selected blue witnesses

\[
D_i=\{a_i\}\cup P_i,\qquad P_i\subset Y,\quad 1\le i\le3.  \tag{8}
\]

The unique residual-deficit profile \((9,1,0,0,0)\) says that the remaining
ten blue clauses consist of nine blue \(K_4\)'s wholly in \(X\), together
with one mixed clause

\[
C_*=Q\cup\{y_*\},\qquad Q\subset X,\quad y_*\in Y,          \tag{9}
\]

where \(Q\) is a blue triangle.  Every vertex other than \(w\) has selected
blue degree exactly two.

## The \(X\)-link suppression theorem

Project the ten clauses in (9) and the nine internal clauses to \(X\).  This
gives nine 4-sets and the single 3-set \(Q\).  Equation (8) has already used
one selected-blue occurrence of every \(a_i\), so

\[
d_{\mathcal H_X}(a_i)=1\quad(i=1,2,3),\qquad
d_{\mathcal H_X}(x)=2\quad(x\in X\setminus A).              \tag{10}
\]

Moreover, a blue clique meets the red triangle \(A\) in at most one vertex.
Consequently the three degree-one incidences in (10) lie in three distinct
projected clauses.

Create one node of \(J_X\) for each projected clause.  Suppress every
\(x\in X\setminus A\) to an edge joining the two clause nodes that contain
it, and suppress every \(a_i\) to a dangling half-edge at its unique clause
node.  Then \(J_X\) has

\[
|V(J_X)|=10,\qquad |E(J_X)|=18,\qquad h(J_X)=3.             \tag{11}
\]

It is loopless.  Parallel edges are allowed, but their multiplicity is at
most three: multiplicity four would make two distinct projected 4-sets
equal, and the 3-set node has total support size three.

Let \(q=|Q\cap A|\).  Since \(Q\) is blue and \(A\) is red,

\[
q\in\{0,1\}.                                                \tag{12}
\]

Deleting the three half-edges lowers the ordinary degree of their three
distinct incident nodes by one.  If \(q=0\), the 3-set node has degree three
and three 4-set nodes also have degree three, giving (3a).  If \(q=1\), the
3-set node has ordinary degree two and two 4-set nodes have degree three,
giving (3b).  This proves that there are exactly two degree families.

### Converse for \(J_X\)

Take a loopless marked multigraph with nine 4-set nodes, one 3-set node,
three half-edges on distinct nodes, edge multiplicity at most three, and
one of (3a)--(3b) with the prescribed half-edge placement.  Give each
ordinary edge a fresh vertex and put it in the supports of its two endpoints;
give each half-edge a fresh vertex and put it in its endpoint support.
The reconstructed endpoint supports have sizes \(4^9,3^1\), the 18 ordinary
vertices have degree two, and the three half-edge vertices have degree one.
No two 4-set supports coincide, because equality would require four parallel
edges.  This proves the converse at exactly the incidence level claimed.

## The \(Y\)-link suppression theorem

All selected-blue incidence on \(Y\) comes from the ten side triangles
\(T_i\), the three witness triangles \(P_i\), and the singleton \(y_*\) in
\(C_*\).  Hence the 13 triangle occurrences form a 3-uniform multihypergraph
\(\mathcal H_Y\) satisfying

\[
d_{\mathcal H_Y}(y_*)=1,qquad
d_{\mathcal H_Y}(y)=2\quad(y\in Y\setminus\{y_*\}).         \tag{13}
\]

The incidence check is

\[
1+19\cdot2=39=13\cdot3.                                   \tag{14}
\]

Create one marked node for each triangle occurrence, retaining ten
side labels and three witness labels.  Suppress the 19 degree-two vertices
to edges and \(y_*\) to one half-edge.  The resulting loopless multigraph
\(J_Y\) has

\[
|V(J_Y)|=13,\qquad |E(J_Y)|=19,
\qquad h(J_Y)=1,                                           \tag{15}
\]

and ordinary degrees (4).  Its edge multiplicity is at most three.  The ten
side-triangle supports are pairwise distinct because the ten full side
clauses share \(w\); equivalently, no two side nodes of \(J_Y\) may be joined
by three parallel edges.  Three parallel edges involving a witness node are
allowed: witness occurrences can have the same triangle support while their
full clauses remain distinct because they contain different \(a_i\).

### Converse for \(J_Y\)

Conversely, use one fresh vertex for each ordinary edge and one for the
half-edge.  Every node reconstructs a 3-set occurrence; the half-edge vertex
has occurrence degree one and the other 19 vertices have degree two.  The
side-side triple-edge prohibition makes the ten side supports distinct.
Adding the singleton occurrence of the half-edge vertex in \(C_*\) gives
selected blue degree two at every vertex of \(Y\).  This is precisely (13)
and proves the converse.

## Why this is a useful global compression

The prior intersection-number frontier left a 21-vertex red link and a
20-vertex blue link with labeled support choices.  The suppression theorem
replaces those raw choices by two bounded kernels:

| link | raw support vertices | kernel nodes | ordinary edges | half-edges | degree families |
|---|---:|---:|---:|---:|---:|
| \(X=N_R(w)\) | 21 | 10 | 18 | 3 | 2 |
| \(Y=N_B(w)\) | 20 | 13 | 19 | 1 | 1 |

Future support-aware SAT or rewrite work can enumerate marked kernels up to
multigraph isomorphism and only then impose the missing graph-color
constraints.  The normalization preserves which occurrence nodes are the
nine internal \(K_4\)'s, the mixed triangle, the ten side triangles, and the
three one-flip witnesses, so a decoded kernel retains the structure needed
for \(K_5\)-freeness tests and singular-DP ancestry.

The certificate includes a simple (multiplicity-one) representative of each
of the two \(X\)-families and of the \(Y\)-family.  Therefore the abstract
incidence projection is nonempty: incidence arithmetic alone cannot exclude
\(\rho=21\).

## Exact certificate and checker

Run the standard-library checker:

~~~bash
python3 ramsey_r55_symbolic_extension/verify_rho21_two_link_kernels.py \
  ramsey_r55_symbolic_extension/rho21-two-link-kernel-certificate.json
~~~

The checker derives the two \(X\)-degree sequences from \(q\in\{0,1\}\),
checks every kernel axiom, reconstructs all endpoint supports, verifies the
converse incidence degrees and side-support distinctness, and validates an
explicit member of every abstract family.  It uses no solver or external
package.

## Novelty assessment

Discovery Net was searched through indexed height 1151 for “two-link,”
“suppression kernel,” “triangle cover,” “\(\rho=21\),” and related support
language.  No contribution with (3)--(4) or the two converse kernel grammars
was found.  Targeted searches of the primary Ramsey extension and
singular-DP literature likewise found no matching reduction.

The claimed new content is the Ramsey-specific suppression of the unique
exceptional link profile to two exact marked-multigraph alphabets, including
the converse.  This is an apparent novelty assessment relative to the
searched graph and sources, not a historical-priority claim.

## Scope and trust boundary

The result imports the exceptional \(m=10\) incidence state, its unique
\(\rho=21\) deficit profile, and the one-flip witness decomposition.  The
new theorem is elementary incidence geometry plus an exact converse.

It does **not** assert that every abstract kernel is realizable as blue
cliques inside a red/blue \(K_5\)-free graph, that the red and blue link
graphs exist, or that a kernel lifts through a complete singular-DP history.
Those are deliberately isolated as the next proof obligations.  The checker
audits the integer grammar and representatives; the universal reduction and
converse are the proof above.

## Public source and provenance

The reader-facing source is
[rho21-two-link-kernel-normal-form.md](https://github.com/njallskarp/math_source_code_open/blob/main/ramsey_r55_symbolic_extension/rho21-two-link-kernel-normal-form.md).
Immutable source commit:
[`238c34295760a13b886c2200d0ca59b55a41e890`](https://github.com/njallskarp/math_source_code_open/tree/238c34295760a13b886c2200d0ca59b55a41e890/ramsey_r55_symbolic_extension).

- Initial research-note SHA-256:
  `e5245b80b8a3b5bd37d118fef89756908fefcb004478cc6d84ba8d2dbd4fc8d3`.
- Exact-certificate SHA-256:
  `7add789c51f14e503297295e332fb2d3f76a4e451741fba17363a80cc15b4184`.
- Checker SHA-256:
  `025adfbb885cb1819f47fcd4683870ca521a9420fec61cc1aea8bde1876b4fb9`.
