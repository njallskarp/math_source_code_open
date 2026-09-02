# Independent audit of the singular-DP excess-contraction law

## Verdict

**ACCEPT, with two expository repairs before graph publication.**  The local
potential identity, global telescoping law, concentration bound, and all three
refined thresholds are correct.  The repairs below do not change the theorem.

The audited producer source is immutable commit
`8b7abff2623c1811318b3ec7f64489fb92a974e0`.

## Independent derivation

Let the main clause be (C=\{x\}\cup A), and write the side clauses as
(D_i=\{\bar x\}\cup B_i).  Kullmann--Zhao Lemma 3(a)--(c) gives the exact
set-CNF guard needed here: (A\cup B_i) is a clause for every (i), these
resolvents are pairwise distinct, and none equals an unaffected clause.  Thus
the step replaces (m+1) clauses by exactly (m) clauses.  Moreover, there
is no nonpivot complementary pair between (A) and (B_i), so with
(c_i=|A\cap B_i|),

\[
 |A\cup B_i|=(a-1)+(b_i-1)-c_i=a+b_i-2-c_i.
\]

The changing contribution to the potential before the step is

\[
 (a-2)+\sum_i(b_i-2),
\]

and afterward is

\[
 \sum_i(a+b_i-4-c_i).
\]

Their difference is exactly

\[
 \sum_i c_i-(m-1)(a-2).
\]

At the endpoints, the 44 length-four clauses have potential (88), while
(F_p), with (p) binary clauses and two length-(p) clauses, has potential
(2p-4).  Hence the total charge is (92-2p).  The disjoint (3+3) first
fan has charge (-2(m-1)), leaving (41-p) steps with total charge
(90+2m-2p).  The average is

\[
 2+\frac{2m+8}{41-p}>2.
\]

For an integer maximum (M), the condition (M\ge k) follows precisely
when this average is (>k-1).  For (k=4,5,6), clearing the positive
denominator gives, respectively,

\[
 p+2m>33,\qquad p+m>37,\qquad 3p+2m>115.
\]

The proof only needs (p\le40) for a nonempty post-first tail.  The imported
(p\le33) result is therefore **contextual**, restricting the currently live
Ramsey parameter range; it is not a logical dependency of the local identity,
telescoping equation, or concentration argument.  If the graph body advertises
the phrase "every currently possible (p)", that earlier bound should be
cited for provenance, but it need not be presented as an algebraic premise.

For a unit main clause, (a=1).  Even when every (c_i=0), the charge is
(m-1).  Thus positive charge need not mean overlap.  The charge inequalities
are necessary conditions on an ancestry, never sufficient conditions for the
existence or Ramsey realizability of one.

## Exact repairs

1. Replace the draft's deficiency-only collision paragraph by an explicit
   citation to Kullmann--Zhao Lemma 3(a)--(c).  Deficiency preservation alone,
   phrased merely as "one variable is deleted", does not by itself establish
   the three set-CNF facts being used.  The lemma directly proves that all
   (m) resolvents are non-tautological, pairwise distinct, and absent from
   the unaffected clause-set.  Also remove "subsumption deletion" or state
   explicitly that the standard DP operation used here performs no
   subsumption minimization.

2. Add the source/ref for the imported (p\le33) frontier to provenance and
   label it contextual.  The mathematically sharp denominator condition is
   (p\le40).  A `CITES` relation is sufficient for the frontier statement;
   a `DEPENDS_ON` relation is needed only if "currently possible" is treated
   as part of the advertised theorem rather than context.

The source note is substantive Markdown.  Outside code spans/fences it uses no
raw dollar delimiters, its inline delimiters `\(` and `\)` balance, its display
delimiters `\[` and `\]` balance, and its `aligned`/`array` environments occur
inside display delimiters.

## Reproduction

From the root of `math_source_code_open`, run:

~~~bash
python3 singular_dp_excess_contraction_independent_audit/independent_verify.py
~~~

The program does not import, execute, or read the producer checker or
certificate.  Its mathematical evidence consists of:

- exact coefficient comparison for the one-step identity;
- exhaustive reconstruction of all minimally unsatisfiable clause-sets on at
  most three variables in clause-count range (n+1\) through (n+3), followed
  by a direct audit of every singular pivot's collision conditions, deficiency,
  minimal unsatisfiability, and potential identity;
- exact integer verification over every pair (2\le p\le40),
  (1\le m\le40).

The small-clause-set enumeration is corroborative finite evidence, not the
universal proof.  Universality of the collision guard is inherited from
Kullmann--Zhao Lemma 3; universality of the charge law is the displayed
coefficient derivation above.  Blob-hash and Markdown checks are source
inspection rather than mathematical evidence.

Primary imported source: O. Kullmann and X. Zhao, *On Davis--Putnam
reductions for minimally unsatisfiable clause-sets*, Theoretical Computer
Science 492 (2013), 70--87, arXiv:1202.2600, Lemma 3 and Corollary 2.
