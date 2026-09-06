# Quota-free fixed-core completion theorem

## Exact statement

Let \(G\) be a red-blue coloring of the pairs of
\(\{0,\ldots,42\}\) extending [PARTIAL.json](PARTIAL.json). Assume red
degree 22 at vertex 0, red degree 21 or 22 at vertices 1 through 22, and red
degree 20 or 21 at vertices 23 through 42. Then \(G\) contains a monochromatic
\(K_5\).

All 400 unspecified pairs remain free. No cell quota, total-edge equation,
local neighborhood edge-count equation, symmetry restriction, or edit bound
is imposed. The 503 literal fixed colors and the degree intervals are genuine
hypotheses. This is not an exclusion of all cores of degree 22, all
deficiency-six cores, or all graphs of any given degree multiset.

## Graph-to-base reduction

Number the 400 free pairs lexicographically. A primary variable is true exactly
when its pair is red. For every five-set, prohibit all ten pairs being red and
prohibit all ten being blue, substituting the fixed colors. A fixed pair of
the opposite color discharges a prohibition. Deduplication leaves exactly
51,624 clauses. The independent-of-producer auditor reconstructs this set
using possible-color clique recursion instead of scanning five-subsets.

Subtract fixed red incidences from each vertex's degree interval. Upper bounds
become cardinality constraints on the free incident variables; a lower bound
becomes an upper bound on their negations. Exactly 80 nonvacuous bounds remain,
with 15,760 threshold-grid clauses. There are no other blocks.

For signed Boolean literals \(y_0,\ldots,y_{n-1}\) and bound
\(\sum_i y_i\le t\), use grid variables \(s_{k,j}\) with
\(0\le k<t\) and \(0\le j<n-t\). The clauses assert the first-row
implications \(y_j\Rightarrow s_{0,j}\), horizontal implications
\(s_{k,j}\Rightarrow s_{k,j+1}\), interior implications

\[
(s_{k,j}\wedge y_{j+k+1})\Rightarrow s_{k+1,j},
\]

and the last-row prohibitions \(\neg(s_{t-1,j}\wedge y_{j+t})\).
The obvious index restrictions apply. Bounds zero and \(n-1\) use negative
units and one all-negative clause, respectively; bounds at least \(n\) are
vacuous.

Every assignment meeting the bound extends these clauses by setting

\[
s_{k,j}=1\quad\Longleftrightarrow\quad
\sum_{i=0}^{j+k}y_i\ge k+1.
\]

The implication clauses follow from prefix counting. A violated last-row
clause would require at least \(t+1\) true literals. Distinct blocks have
disjoint auxiliary variables. Thus every hypothetical clique-free graph in
the stated family extends to a model of the base formula \(F\).

The auditor reconstructs the exact literal multiset, signs, and variable
allocation of \(F\): 8,320 variables and 67,384 clauses. In particular,
no undocumented restriction can hide in an extra clause.

## Conservative definitions and modular refutation

The successful search introduces 109,974 fresh gate variables. Every gate is
a complete definition

\[
z\;\longleftrightarrow\; ((x\wedge h)\vee(\neg x\wedge l)),
\]

where \(x\) is a primary variable and each cofactor is a constant or an
earlier variable. The definition is expressed by the four clauses

\[
(\neg z\vee\neg x\vee h),\quad
(\neg z\vee x\vee l),\quad
(z\vee\neg x\vee\neg h),\quad
(z\vee x\vee\neg l),
\]

with true clauses discharged and false literals removed. Let \(D\) be these
411,332 gate clauses. The interface auditor parses the actual clause suffix,
checks both directions of every definition, and verifies the fresh acyclic
allocation. Therefore every assignment of the variables of \(F\) extends
to one satisfying \(D\), simply by evaluating the gates in order.

There are twenty designated positive gate-root units \(r_b\), one for each
column \(b=23,\ldots,42\). They are **not assumed without proof**.
For each \(b\), a local formula \(L_b\) consists solely of clauses from
\(F\cup D\), followed by the single unit \(\neg r_b\). Literal subset
checking enforces that interface. Each of the twenty \(L_b\)'s has its own
RUP-only refutation, independently replayed by DRAT-trim. Hence

\[
F\wedge D\models r_b\qquad (23\le b\le42).
\]

Finally, a separate RUP-only trace refutes exactly

\[
F\wedge D\wedge\bigwedge_{b=23}^{42}r_b.
\]

If \(F\) had a model, its conservative extension to \(D\) would satisfy
all twenty roots by the checked local implications, contradicting this global
refutation. Consequently \(F\) is unsatisfiable, proving the theorem.

This proof composition is ordinary propositional logic. It uses 21 checked
RUP refutations and the literal gate/subset audits. It does not rely on a
solver verdict, completeness of a domain enumeration, decision-diagram
semantics inferred from sampling, a flattened DRAT trace, or height 3003's
earlier exclusion. Fresh full regeneration repeats all 21 replays.

## Scope and trust

The independent review of height 3003 remains absent. This theorem does not
assume that claim: it starts from the literal input and supplies a new proof
of the larger family. It generalizes the earlier statement by removing all
36 cell quotas jointly, but does not establish a general Ramsey bound.

Trust remains in the unformalized graph-to-counter extension and modular
composition arguments, the short exact auditors, RUP checking, interpreter,
input identity and hardware. These are author-written checks, not independent
peer review or proof-assistant formalization. The earlier fractional
limitation remains valid; it is not a Ramsey graph.
