# A four-incidence cut forced by short-clause genealogy

## Result type

**Universal leaf-genealogy theorem with a sharp local realization.**  This
note converts clause overlap into a statement about the original signed
\(K_4\) leaves.  It retains the binary resolution tree and the identities of
the leaf supports; it is neither an endpoint potential nor a selected-support
census.

For every clause descended from pure signed length-four leaves, the
opposite-color intersection graph of the leaf occurrences in its unfolded
ancestry is connected.  If the derived clause has length at most three, one
internal tree cut moreover carries

\[
  1\text{ bichromatic pivot incidence}
  \; + \;
  3\text{ label-distinct monochromatic overlap incidences}.       \tag{1}
\]

For a unit main clause in the 44-clause \(R(5,5)\) singular-DP problem, (1)
is therefore a necessary post-first leaf-support certificate.  In the
nonunit branch, every unit of the already-forced current overlap similarly
decodes to a concrete monochromatic incidence between the two parent
genealogies.

The theorem is sharp as a local statement: an explicit two-coloring of
\(K_7\) with no monochromatic \(K_5\) realizes the four-incidence cut and a
resolution ancestry ending in a ternary clause.  Thus the new condition is a
genuine global ancestry reduction, but not by itself a contradiction.

## Signed leaves and support incidences

Let every leaf clause be either pure positive or pure negative and have
length four.  Its **support** is the set of its four underlying variables.
In the Ramsey application, the two signs represent the two colors and the
leaf supports are monochromatic \(K_4\)'s in one \(K_5\)-free two-coloring.

Two opposite-color leaf supports intersect in at most one variable.  Indeed,
if a red and a blue \(K_4\) shared two vertices, the edge between those
vertices would have to have both colors.

Fix an unfolded binary resolution ancestry tree \(T\).  Leaves are
**occurrences**: if the same original clause feeds two branches of the
resolution DAG, it appears twice after unfolding.

Define two graphs on the leaf occurrences.

1. The **bichromatic intersection graph** \(B(T)\) is bipartite by leaf sign.
   A positive and a negative leaf occurrence are adjacent precisely when
   their supports intersect.  In the Ramsey setting such an edge has a unique
   support-variable label.
2. The **full support-incidence multigraph** \(J(T)\) has, for each pair of
   leaf occurrences and each variable in the intersection of their supports,
   one edge labeled by that variable.  Same-color leaf pairs may therefore
   carry several parallel edges with distinct labels.

The multigraph convention matters.  The conclusion below counts distinct
support-variable incidences, not merely distinct pairs of leaf occurrences.

## Literal provenance lemma

Let \(D\) be the clause at any node of \(T\).  Every literal \(\ell\in D\)
occurs with the same sign in at least one leaf below that node.

### Proof

At a leaf this is immediate.  At an internal node, resolution deletes only
the two complementary pivot literals and forms the union of the remaining
literals.  Hence every surviving literal is inherited from at least one
child.  Induction down that child reaches a leaf containing the same signed
literal. \(\square\)

## Theorem 1: bichromatic leaf connectivity

For every node \(z\) of an unfolded resolution ancestry, let \(T_z\) be the
subtree rooted at \(z\).  Then

\[
  B(T_z)\text{ is connected}.                          \tag{2}
\]

In particular, if \(T_z\) has \(L_z\) leaf occurrences, then

\[
  |E(B(T_z))|\ge L_z-1.                                \tag{3}
\]

### Proof

Proceed by induction on \(T_z\).  A one-leaf graph is connected.  Suppose
\(z\) resolves child clauses \(P\) and \(Q\) on variable \(x\).  After
possibly reversing the pivot polarity, \(P\) contains \(x\) and \(Q\)
contains \(\bar x\).  By the literal provenance lemma, some positive leaf
occurrence below \(P\) contains variable \(x\), while some negative leaf
occurrence below \(Q\) contains variable \(x\).  Their supports intersect,
so they give an edge of \(B(T_z)\) crossing the two child leaf sets.

By induction, the bichromatic intersection graphs inside the two child
subtrees are connected.  The crossing edge joins them, proving (2).  Bound
(3) is the standard edge lower bound for a connected graph. \(\square\)

The proof gives more than connectivity: every internal resolution node has a
bichromatic support-incidence edge crossing its two child leaf sets, labeled
by that node's pivot variable.

## Theorem 2: a four-incidence ancestry cut

Let \(C\) be a derived clause of length at most three whose unfolded ancestry
has pure signed length-four leaves.  Then some internal node \(u\) of every
such ancestry has the following properties.

- Its two child leaf sets induce connected bichromatic intersection graphs.
- Across the child cut, \(J(T)\) has an opposite-color incidence labeled by
  the pivot variable of \(u\).
- Across the same cut, \(J(T)\) has at least three same-color incidences with
  distinct nonpivot-variable labels.
- The pivot label is distinct from all three nonpivot labels.

Consequently that cut has at least four support incidences with the exact
color-type pattern in (1).

"Same-color" is edgewise here: every one of the three incidences joins two
leaves of one color, although different incidences may use different colors.

### Proof

For an internal node \(v\), let \(c_v\) be the number of common same-signed
nonpivot literals in its two parent clauses.  The exact clause-genealogy
overlap-debt identity is

\[
  \sum_{v\in I(T)}(c_v-2)=4-|C|.                       \tag{4}
\]

When \(|C|\le3\), (4) forces some internal node \(u\) with \(c_u\ge3\).
Choose three distinct common nonpivot literals

\[
  \ell_1,\ell_2,\ell_3.                                \tag{5}
\]

For each \(\ell_j\), apply literal provenance separately in the two child
subtrees.  This produces one leaf occurrence on each side having the sign of
\(\ell_j\), and both supports contain the underlying variable of
\(\ell_j\).  The two leaves have the same color, so they give a monochromatic
edge of \(J(T)\) crossing the cut.  The three labels are distinct because the
literals in a clause are a set.

The two pivot literals similarly descend to opposite-color leaves on the two
sides.  They give a bichromatic crossing incidence labeled by the pivot
variable.  A nonpivot literal cannot use the pivot variable, so this fourth
label is different from the labels in (5).  Finally, Theorem 1 applied to
each child subtree proves the two internal connectivity assertions.
\(\square\)

## Corollary: leaf-level U/O dichotomy for the Ramsey ancestry

The committed global clause-excess theorem guarantees a post-first pivot
with

\[
  \sigma
  =\sum_{i=1}^{m}c_i-(m-1)(a-2)\ge3,                 \tag{6}
\]

where \(a\) is its main-clause length.

### Branch U: unit main

If \(a=1\), Theorem 2 applied to the main unit gives a prior internal cut
with the four-incidence pattern (1).  The first Ramsey fan has zero nonpivot
overlap, so this cut is necessarily post-first.

At the current fan, (6) also reads

\[
  \sum_{i=1}^{m}c_i\ge4-m.                             \tag{7}
\]

Thus a unit-main fan with \(m\le3\) already has current nonpivot overlap.
The only unit-main loophole in which current overlap can vanish has
\(m\ge4\); the genealogical cut closes precisely that loophole.

### Branch O: nonunit main

If \(a\ge2\), then

\[
  \sum_{i=1}^{m}c_i
  \ge(m-1)(a-2)+3.                                     \tag{8}
\]

For every literal counted by a \(c_i\), literal provenance in the main and
the corresponding side-clause ancestry decodes that overlap into a concrete
same-color leaf-support incidence across the parent-genealogy cut.  Thus (8)
is not merely a scalar obligation: every counted unit must have an explicit
leaf-support witness.  The witnesses need not be distinct across different
side clauses, so (8) is deliberately not presented as a simple-edge count.

This gives a complete ancestry-level dichotomy: Branch U contains one marked
\(1+3\) cut, while Branch O contains a fan-indexed family of concrete
monochromatic leaf incidences satisfying (8).

## Sharp local realization

The four-incidence conclusion cannot be turned into a local contradiction
using only \(K_5\)-freeness.  Let

\[
  A=\{1,2,3\},\qquad X=\{4,5,6,7\}.                   \tag{9}
\]

Color every edge inside \(A\) and between \(A\) and \(X\) red, and every
edge inside \(X\) blue.  This is a complete two-coloring of \(K_7\) with no
monochromatic \(K_5\).  It has four red \(K_4\)'s

\[
  A\cup\{j\}\quad(j\in X)                             \tag{10}
\]

and one blue \(K_4\), namely \(X\).  Every red support meets the blue support
in exactly one variable.

Use the corresponding pure clauses

\[
\begin{aligned}
  R_j&=\{1,2,3,j\} &&(j=4,5,6,7),\\
  B&=\{\bar4,\bar5,\bar6,\bar7\}.
\end{aligned}                                         \tag{11}
\]

Successively resolving on \(4,5,6,7\) gives

\[
\begin{aligned}
 Q_4&=\operatorname{Res}_4(R_4,B)
     =\{1,2,3,\bar5,\bar6,\bar7\},\\
 Q_5&=\operatorname{Res}_5(Q_4,R_5)
     =\{1,2,3,\bar6,\bar7\},\\
 Q_6&=\operatorname{Res}_6(Q_5,R_6)
     =\{1,2,3,\bar7\},\\
 C&=\operatorname{Res}_7(Q_6,R_7)
   =\{1,2,3\}.                                       \tag{12}
\end{aligned}
\]

The first overlap is zero and each of the final three overlaps is exactly
three.  The bichromatic leaf-intersection graph is the four-edge star with
center \(B\), and every later resolution cut has one blue-red pivot incidence
plus the three red-red incidences labeled \(1,2,3\).  Thus both (2) and (1)
are attained in a genuine local Ramsey coloring.

## Exact certificate and checker

Run:

~~~bash
python3 ramsey_r55_symbolic_extension/verify_genealogical_four_incidence_cut.py \
  ramsey_r55_symbolic_extension/genealogical-four-incidence-cut-certificate.json
python3 -m unittest -v \
  ramsey_r55_symbolic_extension/test_genealogical_four_incidence_cut.py
~~~

The standard-library checker reconstructs every clause in (11)--(12), checks
that each resolution has exactly one complementary pivot and no nonpivot
clash, unfolds all leaf occurrences, verifies connectivity at every subtree,
extracts every four-incidence cut, reconstructs the complete two-coloring of
\(K_7\), and exhaustively checks all five-vertex subsets for monochromatic
\(K_5\)'s.  Mutation tests reject a broken resolution and an opposite-color
support intersection of size two.

The checker validates the compact sharpness certificate and the decoding
conventions.  Theorems 1 and 2 are established by the written induction and
provenance arguments, not by finite enumeration.

## Novelty assessment and literature positioning

Kullmann and Zhao provide the singular-DP collision and preservation facts.
The existing Ramsey ancestry work provides the zero-overlap first fan and the
global charge-three pivot.  Searches of the primary singular-DP literature
and Discovery Net through height 1403 found no leaf-support connectivity
statement or four-incidence cut theorem corresponding to (2) and (1).

The novelty claimed here is narrow and search-relative: the connected
bichromatic leaf-intersection invariant, its combination with exact overlap
debt, and the resulting leaf-level U/O dichotomy.  The sharp \(K_7\)
realization is included to prevent overinterpreting this necessary condition
as a local impossibility theorem.

Primary reference:

- O. Kullmann and X. Zhao, *On Davis--Putnam reductions for minimally
  unsatisfiable clause-sets*, Theoretical Computer Science 492 (2013),
  70--87, DOI `10.1016/j.tcs.2013.04.020`, arXiv:1202.2600.

## Scope and trust boundaries

The connectivity theorem applies to an unfolded ancestry tree, so repeated
uses of one DAG ancestor are represented by distinct occurrences.  It does
not assert that all leaf supports are distinct.  The four same/pivot incidence
labels in Theorem 2 are distinct, but the three same-color witnesses may use
the same pair of leaf occurrences.

The theorem does not exclude a 44-clause obstruction, reconstruct a complete
singular-DP history, or determine \(R(5,5)\).  Its local condition is
explicitly realizable.  Future progress must constrain how many marked cuts
can coexist and reuse the 44 original signed \(K_4\)'s across the complete
ancestry; repeating this one-cut projection would not be sufficient.

The Ramsey corollary imports the global charge theorem and the pending exact
overlap-debt theorem at mathematical source commit
`c795573c19dd41f18a41252dd2ab748d9d61c5f2`.  That parent theorem's independent
review and Discovery Net publication were explicitly deferred.  This result
must therefore remain a source-level theorem until the dependency is reviewed
and published in topological order.

## Immutable provenance

- Mathematical source commit:
  [`8bbd432ff18d6c875658a4a63c368b42e196c5e8`](https://github.com/njallskarp/math_source_code_open/tree/8bbd432ff18d6c875658a4a63c368b42e196c5e8/ramsey_r55_symbolic_extension).
- Prepublication note SHA-256:
  `9c25570ead523e5860b4d003b97f1d51eedacc432725de0d7e65ee73ddfe51ea`.
- Certificate SHA-256:
  `534b16b1f70420a7cd242bd4f09e5565b3933a1fe6df0fce7f2c1885b4b6d7dd`.
- Checker SHA-256:
  `2f1506a2631a5963ea9bee2318b930fbb920c12679dd01194521dfabbdf83bbc`.
- Test SHA-256:
  `6fcb9162a917a9d77aa3349680a048d5f82b020e9b80e8fb64376e313c26dfa2`.
- Parent overlap-debt source commit:
  `c795573c19dd41f18a41252dd2ab748d9d61c5f2`.
- Global excess-contraction theorem: Discovery Net
  `bafkreib5av4yfin6zt4x66756sfddvvu5qiy62wd2ch5v2kg2mtq346e7q`.

## Discovery Net receipt

Deferred.  The parent overlap-debt theorem and this dependent theorem require
independent review and topologically ordered graph publication before either
can be relied upon as committed Discovery Net knowledge.
