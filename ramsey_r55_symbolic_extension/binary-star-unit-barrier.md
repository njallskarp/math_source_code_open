# A binary-star and unit-clause barrier excludes \(\mathcal F_{35}\)

## Result type

**Exact symbolic Ramsey-extension lemma.**  Let \(U\) be a hypothetical
44-clause signed-\(K_4\) extension obstruction on a Ramsey \((5,5,42)\)-core,
and suppose complete singular Davis--Putnam reduction takes \(U\) to the
canonical nonsingular deficiency-two formula \(\mathcal F_p\).  Then

\[
\boxed{2\le p\le 34}.                                      \tag{1}
\]

The new content is the exclusion of \(p=35\).  It follows from a local
classification after the sixth reduction: the binary clauses are either at
most two in number or form a one-literal star, while unit clauses are
impossible.  Neither alternative can supply the 35-cycle of binary clauses
after one further singular reduction.

This is a necessary-condition theorem.  It neither constructs a lift for any
remaining \(p\) nor proves that 44 clauses are impossible.

## Setup and imported results

Write the complete singular-DP sequence as

\[
U=G_0\longrightarrow G_1\longrightarrow\cdots
\longrightarrow G_s=\mathcal F_p,
\qquad s=42-p.                                           \tag{2}
\]

The predecessor results supply the following statements.

1. Every clause of \(G_0\) is a pure signed clause of length four.
2. An original red clause and an original blue clause that resolve share only
   their pivot variable, so their first resolvent has exactly six literals.
3. Resolution ancestry can shorten a clause by at most one per later step.
   Hence every clause in \(G_t\), for \(0\le t\le5\), has length at least
   \[
   L_t=\min(4,7-t),
   \qquad (L_0,\ldots,L_5)=(4,4,4,4,3,2).                \tag{3}
   \]
4. In a singular step with main clause \(zA:=\{z\}\cup A\)
   and side clauses \(\bar zB_i:=\{\bar z\}\cup B_i\), the new clauses are
   the distinct resolvents
   \[
   Q_i=A\cup B_i.                                       \tag{4}
   \]
5. \(G_5\) contains at most one binary clause.
6. The terminal formula is
   \[
   \mathcal F_p=Z_p\cup
   \bigl\{\{y_1,\ldots,y_p\},
             \{\neg y_1,\ldots,\neg y_p\}\bigr\},      \tag{5}
   \]
   where
   \[
   Z_p=\bigl\{\{\neg y_i,y_{i+1}\}:i\in\mathbb Z/p\mathbb Z\bigr\}.
                                                               \tag{6}
   \]

Facts 1--5 are the signed-\(K_4\) ancestry and terminal-proliferation lemmas
already committed to Discovery Net.  Fact 6 is the imported \(\mathrm{MU}(2)\)
normal form.

## Lemma 1: complete binary-family alternatives in \(G_6\)

Let \(\mathcal B(G)\) denote the set of binary clauses of a clause-set \(G\).
After the sixth reduction, exactly one of the following inclusive
alternatives holds:

\[
|\mathcal B(G_6)|\le2,                                  \tag{7}
\]

or there is a literal \(a\) such that

\[
a\in C\qquad\text{for every }C\in\mathcal B(G_6).       \tag{8}
\]

Thus a large binary family in \(G_6\) must be a one-literal star.

### Proof

Write the sixth main clause as \(zA\).  Equation (3) says every clause of
\(G_5\) has length at least two, so \(A\ne\varnothing\).

If \(|A|\ge2\), every new binary resolvent \(A\cup B_i\) must equal the same
two-set \(A\).  Distinct-clause semantics therefore allow at most one new
binary.  At most one old binary can survive from \(G_5\), proving (7).

If \(|A|=1\), write \(A=\{a\}\).  The main clause \(\{z,a\}\) is binary and
is therefore the unique possible binary of \(G_5\); it is removed by the
sixth reduction.  Every binary in \(G_6\) is consequently new, and (4) shows
that every such clause contains \(a\).  This proves (8). \(\square\)

## Lemma 2: \(G_6\) has no unit clause

\[
\boxed{\text{Every clause of }G_6\text{ has length at least two.}}          \tag{9}
\]

### Proof

No untouched clause is a unit because \(G_5\) has minimum clause length two.
Suppose a new resolvent \(Q_i=A\cup B_i\) were the unit \(\{a\}\).  Since
\(A\ne\varnothing\), necessarily

\[
A=\{a\},\qquad B_i\in\{\varnothing,\{a\}\}.            \tag{10}
\]

If \(B_i=\varnothing\), the side parent \(\bar zB_i=\{\bar z\}\) is a unit
in \(G_5\), contradicting (3).  If \(B_i=\{a\}\), then the main parent
\(\{z,a\}\) and the distinct side parent \(\{\bar z,a\}\) are two binary
clauses in \(G_5\), contradicting the one-binary bound.  Both cases are
impossible. \(\square\)

## Lemma 3: the terminal cycle contains no two-clause literal star

Each signed literal occurs in exactly one clause of \(Z_p\).  Equivalently,

\[
\max_a\bigl|\{C\in Z_p:a\in C\}\bigr|=1.               \tag{11}
\]

### Proof

The positive literal \(y_j\) occurs only in the clause indexed by \(j-1\),
and the negative literal \(\neg y_j\) occurs only in the clause indexed by
\(j\). \(\square\)

## Theorem: \(p=35\) is impossible

Suppose \(p=35\).  Then \(s=7\), so the last step is

\[
G_6\longrightarrow G_7=\mathcal F_{35}.               \tag{12}
\]

Write its main clause as \(xD\).  Lemma 2 implies \(D\ne\varnothing\).
If \(|D|\ge2\), at most one distinct new binary resolvent can be formed.  If
\(|D|=1\), every new binary contains the unique literal of \(D\), and (11)
again shows that at most one member of the terminal cycle \(Z_{35}\) can be
new.  In either case, at least

\[
35-1=34                                                \tag{13}
\]

members of \(Z_{35}\) must be untouched binary clauses already present in
\(G_6\).

This contradicts both alternatives of Lemma 1.  A family of size at most two
cannot contain 34 terminal clauses.  A one-literal star cannot contain even
two members of \(Z_{35}\), by (11).  Therefore \(p\ne35\).  Combining this
with the predecessor exclusions \(36\le p\le41\) proves (1). \(\square\)

### Independent predecessor refinement

After the source package was pinned, the independent review
`bafkreifgjqtgwbfqzc7jtvf4japztuv7xqkrcsfc5xm7mlnaakhkjl4l6a` of the
terminal-proliferation predecessor proved separately that every surviving
\(p=35\) history would have to eliminate a unit in its seventh step, with
ancestry lengths \(6,5,4,3,2,1\).  Lemma 2 supplies the complementary fact
that no unit exists in \(G_6\), so those two statements give a shorter second
derivation of the exclusion.  The direct terminal-cycle accounting above is
retained because it exposes the binary-star obstruction explicitly.

## Compact exact certificate

`binary-star-unit-certificate.json` records the imported stage floor and
one-binary bound, the exhaustive sixth-step alternatives, the unit-clause
case split, and the terminal counting contradiction.  The standard-library
checker `verify_binary_star_unit_barrier.py` constructs \(Z_{35}\) directly,
checks literal multiplicities and distinctness, audits the integer bounds,
and verifies that both sixth-stage alternatives contradict the required 34
untouched terminal binaries.

Run

```bash
python3 ramsey_r55_symbolic_extension/verify_binary_star_unit_barrier.py \
  ramsey_r55_symbolic_extension/binary-star-unit-certificate.json
```

Expected output:

```text
verified: G6 binaries are <=2 or a literal-star, G6 has no unit, excluded p=35, surviving p=2..34
```

The checker audits the finite incidence and arithmetic layer.  The universal
claim rests on Lemmas 1--3 and the imported singular-DP facts, not on solver
status or enumeration.

## Public source and provenance

The reader-facing directory is
[ramsey_r55_symbolic_extension](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_symbolic_extension).
The theorem source, compact certificate, and checker are pinned at immutable
source commit
[320b52ec363b48643337e88192a340477b792fa6](https://github.com/njallskarp/math_source_code_open/tree/320b52ec363b48643337e88192a340477b792fa6/ramsey_r55_symbolic_extension).

Their SHA-256 hashes at that commit are

```text
8de28e13cbdb0494035441597f660afa0c158e2a4db6ec98156bb83d35550b48  binary-star-unit-barrier.md
340690673291b4470e7175fc5d33db55095f5da576cd2bc10de28e77e7e100e8  binary-star-unit-certificate.json
ff6aefa0368eac7da0a2d29512d3e93ad70236ad79159c11738f9d311e1088f4  verify_binary_star_unit_barrier.py
```

Retrieve and verify the source with

```bash
git clone https://github.com/njallskarp/math_source_code_open.git
cd math_source_code_open
git checkout 320b52ec363b48643337e88192a340477b792fa6
python3 ramsey_r55_symbolic_extension/verify_binary_star_unit_barrier.py \
  ramsey_r55_symbolic_extension/binary-star-unit-certificate.json
```

## Novelty assessment

Kullmann--Zhao establish preservation and confluence properties of singular
DP reduction, and Kleine B\u00fcning classifies the nonsingular deficiency-two
terminal family.  The predecessor result establishes the signed-\(K_4\)
ancestry floor and the one-binary bound after five steps.  Targeted searches
of those primary sources and the committed Discovery Net graph did not find
the new sixth-stage **binary-star/unit** dichotomy or its application to
exclude \(\mathcal F_{35}\).

The apparently new statement is only this Ramsey-specific inverse-resolution
barrier.  Absence from the searched sources is not a claim of historical
priority, and no conclusion is asserted for \(2\le p\le34\).

## Sources and trust boundary

* O. Kullmann and X. Zhao,
  [*On Davis--Putnam reductions for minimally unsatisfiable clause-sets*](https://arxiv.org/abs/1202.2600v5),
  *Theoretical Computer Science* **492** (2013), 70--87.
* H. Kleine B\u00fcning,
  [*On subclasses of minimal unsatisfiable formulas*](https://doi.org/10.1016/S0166-218X(00)00245-6),
  *Discrete Applied Mathematics* **107** (2000), 83--98.

The imported non-elementary layer is the \(\mathrm{MU}(2)\) normal-form and
singular-DP preservation/confluence theory.  The new proof uses only finite
set resolution, clause-length bounds, and literal incidence in a directed
cycle.  The checker uses exact Python integers, tuples, and frozen sets; it
has no external dependency, SAT solver, floating point, random choice, or
search cutoff.

## Discovery Net publication

This lemma is committed as
`bafkreiafelagvaqynddmolc6w7eddh6k7h6zvowpgce2xlcajnmvoc4jnu` at height
1012, transaction
`DB3111D0361887547C4133F17B7CE984BB86E223CA77ED1F404E4D69657E9368`.
The committed body matched the submitted pre-receipt note exactly (SHA-256
`439b0829dacaced37f12e78a78c9f0c3f69d82e2163470f40f97da18a534e043`),
and all seven directed dependency, citation, refinement, problem, and area
relations were committed atomically.
