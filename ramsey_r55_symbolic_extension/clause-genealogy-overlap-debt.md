# Clause-genealogy overlap debt forces a genuine nonpivot event

## Result type

**Universal clause-genealogy identity and Ramsey-ancestry consequence.**
This note retains information that is erased by endpoint potentials and support
projections: for one particular derived clause, it unfolds the complete binary
resolution tree back to the original pure length-four clauses and records the
nonpivot overlap at every internal node.

The exact identity is

\[
  \sum_{u\in I(T)}\bigl(c_u-2\bigr)=4-|C|.             \tag{1}
\]

Here \(T\) is an unfolded resolution ancestry of a clause \(C\), \(I(T)\)
is its set of internal occurrences, and \(c_u\) is the number of common
same-signed nonpivot literals in the two parents resolved at \(u\).

Consequently every clause of length at most three descended from the pure
length-four leaves has an actual ancestor resolution with \(c_u\ge 3\).  When
this is combined with the committed global excess-contraction law, every
hypothetical 44-clause signed-\(K_4\) ancestry has a post-first genuine
nonpivot-overlap event.  In particular, the unit-main branch cannot satisfy
the required positive charge merely through fan arity: the unit itself has a
prior resolution ancestor whose two parents share at least three nonpivot
literals.

This is a necessary full-ancestry constraint.  It does not by itself exclude
all 44-clause extension obstructions.

## Clause and history conventions

A literal is a signed variable, a clause is a finite clash-free set of
literals, and a clause-set is a finite set of clauses.  Consider a singular
Davis--Putnam history

\[
  G_0\longrightarrow G_1\longrightarrow\cdots
      \longrightarrow G_s,                            \tag{2}
\]

where every clause of \(G_0\) has length four.  At a singular step, choose
the pivot polarity so that the unique main clause is \(P=A\cup\{x\}\) and a
side clause is \(Q=B\cup\{\bar x\}\).  Its resolvent is

\[
  R=A\cup B.                                           \tag{3}
\]

For singular DP inside a minimally unsatisfiable clause-set, the standard
collision guard is the full Kullmann--Zhao singular-DP lemma: the parents are
resolvable only on the pivot, the resulting resolvents are pairwise distinct,
and no resolvent equals an unaffected clause.  Standard DP here performs no
subsumption-minimization pass.  Thus every derived clause has a well-defined
creation step, and its two parents contain no complementary nonpivot pair.

Define the **nonpivot overlap** of this parent occurrence by

\[
  c(P,Q;x)=|A\cap B|.                                  \tag{4}
\]

Because there is no complementary nonpivot pair, (4) counts common literals,
not merely common underlying variables.

## Unfolded clause genealogy

Fix a clause \(C\) present at some stage.  Trace it backward through every
step at which it is unaffected.  At its creation step, replace it by its two
resolution parents and continue recursively.  If one earlier clause feeds
two branches, duplicate that occurrence.  The result is a finite full binary
tree \(T\):

- the root is the chosen occurrence of \(C\);
- every internal occurrence is labeled by one actual resolution step and its
  overlap \(c_u\);
- every leaf occurrence is a clause of \(G_0\), hence has length four.

The unfolding records multiplicity.  Two leaves may therefore be occurrences
of the same original clause; the theorem neither assumes nor requires
read-once resolution.

Let \(L(T)\) be the number of leaf occurrences.  A full binary tree with
\(L(T)\) leaves has \(L(T)-1\) internal occurrences.

## The local length recurrence

At one internal occurrence, inclusion--exclusion in (3) gives

\[
  |R|=|P|+|Q|-2-c(P,Q;x).                              \tag{5}
\]

Equivalently, after centering clause length at two,

\[
  |R|-2=(|P|-2)+(|Q|-2)-c(P,Q;x).                     \tag{6}
\]

This recurrence is local: it retains which clause is being traced and which
two parents created it.  It is not the endpoint potential obtained by summing
over an entire clause-set.

## Theorem: exact overlap debt of one clause

Let \(C\) be any derived clause in (2), and let \(T\) be any unfolded
resolution ancestry of \(C\) whose leaves lie in \(G_0\).  Then

\[
  |C|-2
  =2L(T)-\sum_{u\in I(T)}c_u,                         \tag{7}
\]

or, equivalently,

\[
  \boxed{
  \sum_{u\in I(T)}c_u=2L(T)+2-|C|
  }                                                     \tag{8}
\]

and

\[
  \boxed{
  \sum_{u\in I(T)}(c_u-2)=4-|C|.
  }                                                     \tag{9}
\]

### Proof

Apply (6) at every internal occurrence of \(T\).  Every internal child term
appears once with a positive sign and once as the left-hand side at the next
node, so all internal clause-length terms cancel.  The remaining positive
terms come from the leaves.  Every leaf has length four and therefore
contributes \(4-2=2\).  This proves (7) and (8).  Since a full binary tree has
\(L(T)-1\) internal occurrences, subtracting \(2(L(T)-1)\) from (8) gives
(9). \(\square\)

The same calculation for uniform leaf length \(k\) is

\[
  \sum_{u\in I(T)}c_u=(k-2)L(T)+2-|C|,                \tag{10}
\]

but only the pure length-four specialization is used here.

## Corollary: short clauses force overlap at least three

If \(|C|\le3\), then some internal occurrence \(u\) of every unfolded
ancestry satisfies

\[
  c_u\ge3.                                             \tag{11}
\]

Indeed, if all \(c_u\le2\), then

\[
  \sum_{u\in I(T)}c_u
  \le2(L(T)-1)=2L(T)-2,                               \tag{12}
\]

whereas (8) and \(|C|\le3\) give

\[
  \sum_{u\in I(T)}c_u
  =2L(T)+2-|C|\ge2L(T)-1.                             \tag{13}
\]

The contradiction proves (11).  More precisely, the total overlap surplus
above the baseline two is three for a unit, two for a binary clause, and one
for a ternary clause:

\[
  |C|=1,2,3
  \quad\Longrightarrow\quad
  \sum_{u\in I(T)}(c_u-2)=3,2,1.                     \tag{14}
\]

## Ramsey consequence: the charge loophole closes genealogically

Consider any complete singular-DP reduction of a hypothetical minimally
unsatisfiable 42-variable, 44-clause signed-\(K_4\) extension formula to a
canonical deficiency-two terminal formula.  The committed excess-contraction
theorem proves that some post-first pivot has charge

\[
  \sigma
  =\sum_{i=1}^{m}c_i-(m-1)(a-2)\ge3,                \tag{15}
\]

where \(a\) is the main-clause length, \(m\) is the side-fan arity, and
\(c_i\) are the current parent overlaps.

Choose such a pivot.  Exactly one of the following alternatives holds.

### Branch O: nonunit main

If \(a\ge2\), (15) implies

\[
  \sum_{i=1}^{m}c_i
  \ge(m-1)(a-2)+3
  \ge3.                                                \tag{16}
\]

Thus the high-charge fan itself contains genuine nonpivot overlap.  If its
main clause has length two or three, the stronger short-clause corollary also
places a single overlap \(c_u\ge3\) somewhere in that main clause's earlier
genealogy.

### Branch U: unit main

If \(a=1\), the main clause is a derived unit.  Formula (14) applied to its
unfolded ancestry gives

\[
  \sum_{u\in I(T)}(c_u-2)=3,                           \tag{17}
\]

so some earlier ancestor resolution has \(c_u\ge3\).  This conclusion is
independent of the fan arity in (15).  It therefore removes the precise
loophole exploited by abstract unit-main histories in which the positive
charge comes from the term \(m-1\) while every current \(c_i\) is zero.

The first Ramsey fan has overlap zero: its opposite-color pure signed
length-four parents meet only in the pivot.  Hence the overlap event supplied
by either (16) or (17) is necessarily post-first.

We have proved the following universal statement.

> **Every complete 44-clause signed-\(K_4\) Ramsey-extension ancestry contains
> a post-first resolution whose two parents have a common same-signed
> nonpivot literal.  In the unit-main branch, some such parent pair shares at
> least three nonpivot literals.**

This statement quantifies over every support survivor, every terminal
parameter, and every legal singular-DP order covered by the imported global
charge theorem.

## What this rules out

The result excludes the entire family of purported full ancestries in which
all post-first parent pairs have zero nonpivot overlap, even if unit-main fans
match every aggregate endpoint potential and clause count.  More generally,
it excludes any history containing a derived clause of length at most three
whose entire unfolded ancestry has overlap at most two at each internal node.

The constraint is suitable for a genealogy-aware rewrite system: whenever a
short clause is introduced, a checker may demand a concrete ancestor node
with overlap at least three, rather than retaining only its current length or
the total charge of the containing formula.

## Exact checker and certificate

Run:

~~~bash
python3 ramsey_r55_symbolic_extension/verify_clause_genealogy_overlap.py \
  ramsey_r55_symbolic_extension/clause-genealogy-overlap-certificate.json
python3 -m unittest -v \
  ramsey_r55_symbolic_extension/test_clause_genealogy_overlap.py
~~~

The dependency-free checker performs four audits:

1. exhaustive definition-level verification of (5)--(6) for every compatible
   pair of clause tails on five nonpivot variables;
2. exact recurrence checks on every ordered full binary-tree shape with at
   most ten leaves, using four independently generated overlap labelings;
3. the short-clause threshold calculation for every \(2\le L\le512\) and
   \(|C|\in\{1,2,3\}\);
4. the high-charge U/O arithmetic for every \(3\le p\le40\),
   \(1\le m\le10\), and representative main lengths.

These finite checks audit definitions, signs, tree multiplicity, and boundary
arithmetic.  The universal result is the cancellation proof (5)--(13), not
the bounded enumeration.

## Novelty assessment and literature positioning

Kullmann and Zhao supply the singular-DP collision and preservation facts
used to make the clause genealogy unambiguous.  The previously committed
Ramsey results supply the pure disjoint first fan and the global existence of
a post-first charge-three pivot.  Searches of that primary SAT literature and
the committed Discovery Net graph found clause-length barriers and global
potential identities, but not the per-clause unfolded-tree identity (9) or
the U/O consequence (16)--(17).

The claimed novelty is therefore narrow: the exact overlap-surplus identity
for one derived clause and its use to force genuine post-first overlap in the
44-clause Ramsey ancestry.  No priority claim is made beyond the literature
and graph searches described here.

Primary reference:

- O. Kullmann and X. Zhao, *On Davis--Putnam reductions for minimally
  unsatisfiable clause-sets*, Theoretical Computer Science 492 (2013),
  70--87, DOI `10.1016/j.tcs.2013.04.020`, arXiv:1202.2600.

## Scope and trust boundary

The theorem is an exact necessary condition, not an impossibility proof for
the 44-clause obstruction and not a determination of \(R(5,5)\).  It does not
show that overlap at least three is itself incompatible with signed-\(K_4\)
leaf supports, nor that every nonunit high-charge fan contains one pair with
overlap three.  In Branch O, equation (16) is a total-overlap statement and
the overlap may be distributed among several side clauses.

The proof imports three established facts: singular-DP collision-freedom in
minimal unsatisfiability, the zero-overlap first Ramsey fan, and the global
post-first charge-three theorem.  It independently proves the per-clause
genealogy identity and the U/O consequence.  The checker does not establish
the imported results and is not a substitute for the universal proof.

## Immutable provenance

Mathematical source commit: `SOURCE_COMMIT_PLACEHOLDER`.

Files:

- `ramsey_r55_symbolic_extension/clause-genealogy-overlap-debt.md`;
- `ramsey_r55_symbolic_extension/clause-genealogy-overlap-certificate.json`;
- `ramsey_r55_symbolic_extension/verify_clause_genealogy_overlap.py`;
- `ramsey_r55_symbolic_extension/test_clause_genealogy_overlap.py`.

File hashes and the immutable GitHub links are filled in by the provenance
commit after the mathematical-source commit is fixed.
