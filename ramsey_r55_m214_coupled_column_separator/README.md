# An exact interval survives the coupled-column relaxation at \(M=214\)

The complete height-3323 LP formulation is feasible. Its 98,758 coordinates
admit the explicit rational family in this directory precisely for

\[
\frac{3}{14}\leq\rho\leq1.
\]

A new, universally valid coupled-column inequality cuts off \(\rho=1\):
26 inequalities have slack \(-42\). After adding **all 21,762 instances**
of this inequality over the full 389-root cover, the same family is feasible
precisely for

\[
\frac{3}{14}\leq\rho\leq\frac{6}{13}.
\]

Thus the new inequality strictly strengthens the entire preceding LP, and
the strengthened LP still cannot exclude the \(M=214\) branch. These are
rational pseudomodels, not graphs or Boolean satisfying assignments. No root
is excluded and no Ramsey-number bound changes.

## The exact relaxation

Use the [height-3323 column-hull
formulation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_column_hull),
with full generated OPB SHA-256

```text
9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609
```

It has 2,983,003 constraints, including 87 equalities, and 98,758 variables.
Its 511,537,255-byte stream includes both inequalities for every five-set,
all triangle conjunctions and local red-triangle totals, all prescribed
degrees and exceptional incidences, the complete selector interface,
footprint constraints, shared pair-cell variables, and scalar column hulls.
All Boolean variables are relaxed to the closed interval \([0,1]\).

The word *complete* refers to this pinned full graph formulation and its
specified suffixes. It does not mean the convex hull of Ramsey graphs or
the conjunction of every lemma ever posted to Discovery Net. In particular,
the separate third-anchor quotient is not silently imported as another
formula suffix.

## Coupled-column theorem

Let a graph in the intrinsic \(M=214\) branch select a red anchor edge
\(uv\), with common red core \(H\) of order \(c\in\{9,\ldots,13\}\).
Write \(X=V\setminus(\{u,v\}\cup H)\), so \(|X|=41-c\).
For \(i\in H\), let \(d_i\in\{20,21\}\) be its prescribed total red
degree and \(a_i\) its red degree inside \(H\). Use the existing variables

\[
m_{\{z,z'\},i}=(1-x_{zi})(1-x_{z'i}),
\qquad
q_{\{z,z'\},ij}=x_{ij}m_{\{z,z'\},i}m_{\{z,z'\},j}.
\]

For distinct \(i,j\in H\), put

\[
K_{ij}=64-c-d_i-d_j,
\qquad B_{ij}=\binom{K_{ij}}2,
\qquad Q_{ij}=\sum_{P\in\binom X2}q_{P,ij}.
\]

Then

\[
Q_{ij}\leq B_{ij}x_{ij}.
\]

Proof. Suppose \(ij\) is red. Its common red neighborhood contains no red
triangle and no independent five-set, and has at most 13 vertices. For
completeness, the elementary upper bound \(R(3,5)\leq14\) follows from
\(R(3,4)\leq9\): a triangle-free graph on 14 vertices without an independent
five-set has maximum degree four, leaving at least nine nonneighbors of any
vertex and hence an independent four-set there. Adjoining the vertex is a
contradiction. The bound \(R(3,4)\leq9\) follows from \(R(3,3)\leq6\):
a triangle-free nine-vertex graph without an independent four-set must have
every degree three, contrary to handshaking. The usual six-vertex
three-neighbor argument proves \(R(3,3)\leq6\).

Both anchors belong to the common red neighborhood of \(i,j\), so their
common red exterior neighborhood has order \(t\leq11\). Also \(H\) is
triangle-free with independence number at most four, giving
\(a_i,a_j\leq4\). Their red exterior degrees are
\(d_i-2-a_i\) and \(d_j-2-a_j\). Their common blue exterior neighborhood
therefore has size

\[
s=41-c-(d_i-2-a_i)-(d_j-2-a_j)+t
  \leq64-c-d_i-d_j=K_{ij}.
\]

Direct pair counting gives \(Q_{ij}=\binom{s}{2}\). The stated bound follows.
If \(ij\) is blue, every \(q_{P,ij}=0\), proving the other case.
This proof uses no graph catalog or conjectured structural classification.

For a selector \(y_r\) and \(p=\binom{41-c}{2}\), the valid guarded form is

\[
Q_{ij}\leq B_{ij}x_{ij}+(p-B_{ij})(1-y_r).
\]

When \(y_r=0\), it follows from the existing inequalities
\(q_{P,ij}\leq x_{ij}\) and \(0\leq x_{ij}\leq1\). When \(y_r=1\), it
is the theorem. Thus inactive guards remain valid even on fractional
coordinates. These rows introduce no variables and retain every Boolean
solution of the old formula. There are 21,762 root/core-pair instances.

## The rational family

Select only root 48, \((\mathtt{E8},13,0,\mathtt A)\), using zero-based
root indices. Its anchors are 0 and 1, exceptional set is
\(E=\{2,\ldots,14\}\), and common core is \(H=\{15,\ldots,27\}\).
The red core has cyclic differences \(\{1,5,8,12\}\) modulo 13. All its
vertices have red degree four inside the core and prescribed total degree 21.
The exterior consists of the 13 exceptional vertices and 15 central vertices.

Retain exactly the published 20 edge parameters and 171 triangle-class
values from the height-3323 certificate. In particular, red incidences from
an exterior vertex to any core vertex are \(6/13\) for exceptional vertices
and \(3/5\) for central vertices. The complete edge and triangle data are
pinned by SHA-256 in `witness.py`; they are not rediscovered numerically.

For every active core column, set the missed-pair coordinate to

\[
m_{P,h}=\begin{cases}
7/26,&P\subseteq E,\\
14/65,&|P\cap E|=1,\\
1/7,&P\cap E=\varnothing.
\end{cases}
\]

These are the pair moments of a uniform seven-subset of the exceptional
exterior and an independent uniform six-subset of the central exterior.
Each column has the exact required moment

\[
\binom{13}{2}\frac7{26}+13\cdot15\frac{14}{65}
 +\binom{15}{2}\frac17=21+42+15=78.
\]

For other missed coordinates take the McCormick lower value
\(\max(0,1-x_{zh}-x_{z'h})\). For active pairs \(i,j\in H\) and exterior
\(P\), set

\[
q_{P,ij}=\rho\,x_{ij}m_{P,i}.
\]

Here \(m_{P,i}=m_{P,j}\) and \(x_{ij}\in\{0,1\}\). For all remaining
\(q\) coordinates, use \(\min(m_{P,i},m_{P,j},x_{ij})\). This specifies
every coordinate; exactly 9,828 coordinates vary with \(\rho\).

The OPB checker verifies **every old row at both endpoints**
\(\rho=3/14\) and \(\rho=1\), together with all variable bounds. Since
all coordinates are affine in \(\rho\), the whole intervening interval
is feasible. The active exterior pair \(P=\{2,14\}\) is blue, has missed
cardinality \(13(7/26)=7/2\), and induced-red-edge moment \(7\rho\).
Its old pair-cell row requires

\[
7\rho\geq\frac72-2=\frac32,
\]

so \(\rho\geq3/14\) is necessary. The old conjunction upper bound
\(q_{P,ij}\leq m_{P,i}\) forces \(\rho\leq1\). This proves the exact
old feasible interval for this specified affine family.

For each of the 26 active red core edges, the new bound is 36 and

\[
Q_{ij}=78\rho.
\]

At \(\rho=1\), these 26 rows have slack \(36-78=-42\); every other new
row passes. At \(\rho=6/13\), they are tight. The independent checker
evaluates every new row at \(3/14\) and \(6/13\), proving feasibility of
the entire shorter interval and necessity of its upper endpoint.

The independent per-column subset interpretation is only a way to derive
the three rational moments. No jointly realizable distribution of whole
graphs, consistent higher moments, or individual exterior edge coloring is
asserted.

## Reproduction and evidence

Requirements: CPython 3.12.12 was used; Python 3.11 or newer and the standard
library suffice. Use a checkout containing the pinned predecessor
directories. From the repository root:

```sh
python3 -B ramsey_r55_m214_coupled_column_separator/test_verify.py
python3 -B ramsey_r55_m214_coupled_column_separator/reproduce.py \
  /tmp/m214-coupled-column-run
```

The work directory must not already exist and must lie outside the source
repository. Intermediate formulas, the full rational vector, and the final
formula remain local generated state. Allow 1.2 GB of temporary
disk space; none belongs in version control. The script removes only its
own completed predecessor formulas.

The final output must equal `EXPECTED_RESULT.json`: both endpoints satisfy
all 2,983,003 old rows, and all 21,762 new rows admit the exact interval
\([3/14,6/13]\), with 26 violations of slack \(-42\) at \(\rho=1\).
The common scaling denominator is 44,717,400. Verification converts the
rational vector to arbitrary-precision integers and reads every OPB row
through EOF while checking its byte count, row count, equality count and
SHA-256. The complete checker took 38.831 seconds with peak resident memory
64,012,288 bytes on the author's macOS machine. No optimization solver is used.

`verify.py` imports no producer or predecessor Python module. The candidate
generator reuses the pinned source data, but its correctness is not assumed
by the direct OPB evaluator. The separator audit separately reconstructs
the physical root, edge, missed-coordinate and edge-pair support conventions.
This supplies an independent check against the actual complete formula;
it is an author-run audit, not external peer review or a formal proof.

Small controls directly check 6,721 subset distributions, 5,461 common-pair
identities, 125 comparisons with Fraction arithmetic, and 133 rejected rows.
The earlier semantic prototype also checked the full old constraint families
at \(\rho=1\) independently of OPB parsing. Small checks are diagnostics,
not the proof of the universal inequality or full formula coverage.

## Context and limits

Graph selection used indexed height 3336, inspecting the Ramsey neighborhood
from all signers rather than only the current team. Principal and peer report
directories were empty on inspection. The key source chain is local
deficiency 2099 (independently reviewed at 2285), M214 red deficiency seven
2127, complete roots 3148, selector formula 3160 (semantic reproduction
3170), footprint rows 3228/3254, pair lift 3274, and scalar hull 3323.
The semantic reproduction does not independently review its author's
upstream coverage proof. The new work and height 3323 had no committed
external review at the initial cutoff.

The [Angeltveit--McKay primary paper](https://arxiv.org/abs/2409.15709v2)
proves \(R(5,5)\leq46\), using LP and extensive computational case checks;
the [official Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
provides the historical neighborhood catalogs and known order-42 graphs.
The data page's old 43--47 wording is superseded by the paper. No priority
claim is made for elementary common-neighbor counting or binomial moments.

Trust boundaries are the unformalized graph-to-formula reductions when
interpreting the LP in Ramsey terms, the displayed proof of the new bound,
the pinned physical variable conventions, exact Python arithmetic, hashing,
and ordinary hardware. Historical catalog completeness enters the upstream
hard-branch reduction, but not the new common-neighbor argument or the
literal LP feasibility check. No solver status is treated as evidence.

Covered: every row of the named complete M214 LP and every new guarded
core-edge moment inequality over all 389 roots. Uncovered: Boolean
feasibility of any root, other M-slices, the deficiency-at-most-six branch,
and the general order-43 Ramsey problem.

The next falsifiable milestone is an exact certificate or survivor after
adding consistency between moments for different exterior pairs or actual
core-neighborhood configurations. This pass demonstrates that the current
scalar column hull plus all of these coupled-column upper bounds is
insufficient. Repeating its rows, increasing instance size, or reporting an
unproved solver verdict is not a continuation milestone.
