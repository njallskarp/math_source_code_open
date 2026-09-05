# Three complementary blocks require a consistent triangle of realizations

## 1. Exact translation from visible preflight to block relations

Fix three anchors \(E\) in a red/blue complete graph on any finite vertex
set. Every other vertex has a proper three-bit signature: neither
\(000\) nor \(111\). A *visible skeleton* fixes every pair except those
joining complementary signature classes. Thus the unknown pairs form
three disjoint complete bipartite blocks

\[
B_0=C_1\times C_6,\qquad
B_1=C_2\times C_5,\qquad
B_2=C_4\times C_3.
\]

The subscript on a cell is its signature mask, with anchor \(0\) in
the least significant bit. Empty cells are allowed.

Assume the root degrees are correct and the complete visible preflight
passes: all six full root-neighborhood tests and both extra proper-signature
stratum tests of
[Helgi's kernel](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_two_stratum_kernel).
The full neighborhood test forbids a same-color \(K_4\) and an
opposite-color \(K_5\). The extra tests forbid a red \(K_5\) in
\(C_1\cup C_2\cup C_4\) and a blue \(K_5\) in \(C_3\cup C_5\cup C_6\).
These are the proper-signature specialization of the complete visible
interface identified by
[R2's cube classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_cube_mixed_orbits).
They exclude exactly the fully fixed monochromatic five-sets.

For each central vertex, prescribe its total red degree and subtract its
fixed red degree. The remaining degree is a margin in its unique block.
Let \(\mathcal D_i\) be the finite set of all Boolean matrices on \(B_i\)
with these individual row/column margins that satisfy every colored
\(K_5\) prohibition involving unknown edges only from \(B_i\).
There is no claim that enumerating these domains is cheap.

For \(i<j\), define
\(R_{ij}\subseteq\mathcal D_i\times\mathcal D_j\) by requiring every
colored \(K_5\) clause whose unknown pairs occur in exactly those two
blocks. Other vertices of such a five-set may lie anywhere in the skeleton.

**Gluing theorem.** The degree-constrained Ramsey completions are in
bijection with

\[
\{(d_0,d_1,d_2):
d_i\in\mathcal D_i,\quad
(d_0,d_1)\in R_{01},\quad
(d_1,d_2)\in R_{12},\quad
(d_0,d_2)\in R_{02}\}.
\]

If \(A_{ij}\) is the zero/one matrix of \(R_{ij}\), their number is

\[
\operatorname{tr}(A_{01}A_{12}A_{02}^{\mathsf T}).
\]

**Proof.** A five-set with an unknown pair from each of three blocks
would need at least six vertices, because the three blocks have disjoint
vertex sets. Hence a colored \(K_5\) clause involves zero, one, or two
blocks. Preflight handles zero; the domains handle one; the relations
handle two. The blocks partition the unknown pairs and the degree
conditions, so choices of three matrices correspond uniquely to complete
colorings with the required degrees. Expanding the trace counts exactly
the compatible triples. \(\square\)

This theorem covers degree constraints and all \(K_5\) prohibitions.
Root-neighborhood edge counts are already fixed by the skeleton.
Other global conditions, such as additional triangle-count equations,
must not be silently discarded or assumed to factor into these domains.

## 2. Binary fibers: the exact consistency obstruction

Say the relation network is *arc-consistent* if every domain is nonempty
and every value has a compatible partner in each other domain. Nonempty
two-block relations alone are weaker.

**Binary classification.** Suppose all three domains have two states
and the network is arc-consistent. Its three-way join is empty if and
only if all three relations are bijections and their composition around
the triangle swaps the two states.

**Proof.** A binary relation with both coordinate projections full has
either two, three or four entries. If it has two entries, it is a
bijection. Every such full-projection relation contains a bijection.
If one relation has at least three entries, select bijections in the
other two. Their composition supplies a two-entry matching on the
remaining pair of domains, which must intersect the relation of size
at least three. That intersection gives a compatible triple.

It remains to consider three bijections. After labeling each domain
\(\{0,1\}\), write the pair constraints as

\[
x_i\oplus x_j=\epsilon_{ij}.
\]

The three equations are consistent exactly when
\(\epsilon_{01}\oplus\epsilon_{12}\oplus\epsilon_{02}=0\).
Thus the inconsistent case has odd parity. \(\square\)

There are seven full-projection binary relations and \(7^3=343\)
labeled networks. Exactly four have empty join: the four odd-parity
choices of the equality/disequality bijections. The two checkers compare
the complete 343-row table by different methods.

The missing invariant is therefore not another individual margin or
pairwise support count. It is agreement around the triangle. Here
relation composition is written in path order: a pair belongs to
\(R_{01}\circ R_{12}\) when it has an intermediate state in
\(\mathcal D_1\). In the example below,

\[
R_{02}\cap(R_{01}\circ R_{12})=\varnothing.
\]

Relation composition and the arc/path-consistency distinction are
classical; see Mackworth,
[*Consistency in Networks of Relations*](https://www.cs.ubc.ca/~mack/Publications/AI77.pdf).
No new general constraint-satisfaction algorithm or historical priority
is claimed here.

## 3. A literal Ramsey realization of the odd triangle

The complete labeled partial matrix and degree targets are in
[fixture.json](fixture.json). A dot is an unknown pair, zero is blue,
one is red, and a dash marks the diagonal. Anchors \(0,1,2\) form a
red triangle.

| Block | Left vertices | Right vertices | Signatures |
|---|---|---|---|
| \(B_0\) | \(3,4\) | \(5,6\) | \(1,6\) |
| \(B_1\) | \(7,8\) | \(9,10\) | \(2,5\) |
| \(B_2\) | \(11,12\) | \(13,14\) | \(4,3\) |

All 93 other pairs are fixed. The target red degrees, in vertex order,
are

\[
(8,8,8,5,5,7,7,6,4,5,6,6,6,5,6).
\]

Each nonanchor needs exactly one additional red neighbor. Each block
therefore has exactly two realizations: its two perfect matchings.
State \(0\) is the diagonal matching in the displayed vertex orders;
state \(1\) is the off-diagonal matching.

All six full root-neighborhood tests and both mixed-stratum tests pass.
After restricting to the two-state degree fibers, no zero- or one-block
\(K_5\) obstruction remains. Ten colored five-sets remain active, all
blue. Their exact two-block relations are

\[
R_{01}=R_{12}=R_{02}=\{(0,1),(1,0)\}.
\]

Every state thus has support in each neighboring block; every pair has
two solutions. Yet all three states cannot be pairwise different.

Six literal blue-\(K_5\) clauses suffice for the contradiction:

| Pair | Prohibited equal state | Blue five-set |
|---|---:|---|
| \(0,1\) | \(0\) | \(\{3,6,8,9,12\}\) |
| \(0,1\) | \(1\) | \(\{3,5,8,10,14\}\) |
| \(0,2\) | \(0\) | \(\{3,6,8,12,13\}\) |
| \(0,2\) | \(1\) | \(\{3,5,8,12,14\}\) |
| \(1,2\) | \(0\) | \(\{3,8,9,12,13\}\) |
| \(1,2\) | \(1\) | \(\{4,7,9,11,13\}\) |

In each row the eight fixed pairs are blue and the two unknown pairs
are blue exactly at the indicated equal state. Together the rows say
\(x_0\ne x_1\), \(x_1\ne x_2\), and \(x_0\ne x_2\).
Their parity sum is the contradiction \(0=1\).

This six-row state system is deletion-minimal with the degree fibers
retained: remove the row forbidding \(x_i=x_j=s\), and choose
\(x_i=x_j=s\), \(x_k=1-s\). It satisfies the other five rows.
The primary checker verifies all six models. This is minimality of the
selected six-row certificate, not deletion-minimality in the full
ten-row system, where duplicate state prohibitions remain.

The separate literal checker visits all \(2^{12}=4096\) assignments of
the unknown pairs. Exactly eight meet the degrees, and none is Ramsey.
Without the degree requirements, 648 assignments are Ramsey, including
the all-red assignment on the unknown pairs. Thus the obstruction is
genuinely caused by composing degree realization with clique avoidance,
not by an already inconsistent fixed skeleton.

## 4. Sharp vertex bound for this separation

**Minimality theorem.** Fifteen is the minimum number of vertices in
a proper-three-anchor visible skeleton for which the domains and
two-block relations just defined are arc-consistent but have empty
three-way join.

**Proof.** If one domain is a singleton, arc consistency makes its
single value compatible with every value in each other domain. Any
pair allowed by the remaining nonempty relation then gives a global
triple. Hence all three domains must have at least two elements.

Two different zero/one bipartite matrices with identical individual
margins differ along an alternating cycle. Such a cycle has length
at least four, requiring at least two vertices on each side.
Thus every nontrivial block needs at least four vertices. The blocks
are disjoint, so three nontrivial domains need at least twelve
nonanchors, plus the three anchors. The displayed fixture attains
fifteen. \(\square\)

The claim is restricted to this three-complementary-block,
individual-degree, arc-consistency framework. It is not a minimum-order
Ramsey graph, a smallest arbitrary partial-coloring obstruction, or
an exclusion of a 43-vertex profile.

## 5. Conditional transfer and next boundary

The six-clause parity certificate transfers to any larger instance
whose remaining degree fibers are the three displayed two-state
switches and whose fixed edges supply the six listed monochromatic
clause patterns. Additional constraints cannot restore feasibility.
The full 15-vertex matrix need not occur literally if those six
patterns and the exact two-state fibers have other witnesses.

No such face is identified in the current 43-vertex survivors here.
The next falsifiable test is to locate a degree-preserving binary
face in an available proper-signature skeleton and determine its
exact three pair relations. An odd composition gives a compact
exclusion; an even composition gives two joint switch states to
check against the remaining obligations. Without an actual face
or a uniform reduction, enumerating more small fixtures is not
further progress.
