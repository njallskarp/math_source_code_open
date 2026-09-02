# A terminal binary-proliferation barrier excludes \(\mathcal F_{36}\) and \(\mathcal F_{37}\)

## Result type

**Exact symbolic Ramsey-extension lemma.**  Starting from the previously
proved common-core description of inverse singular Davis--Putnam steps, this
note controls not only when a binary clause can first appear, but how many
distinct binary clauses can appear in the next step.

If a hypothetical 44-clause signed-\(K_4\) extension obstruction \(U\) on a
Ramsey \((5,5,42)\)-core has canonical nonsingular terminal form
\(\mathcal F_p\), then

\[
\boxed{2\le p\le35}.                                  \tag{1}
\]

Thus \(\mathcal F_{36}\) and \(\mathcal F_{37}\) join the already excluded
families \(\mathcal F_{38},\ldots,\mathcal F_{41}\).  This remains a
structural restriction on a hypothetical 44-clause obstruction; it does not
prove that any surviving lift exists and does not yet raise the universal
44-clause lower bound.

## Setup and imported facts

Write a complete singular-DP sequence as

\[
U=G_0\longrightarrow G_1\longrightarrow\cdots
\longrightarrow G_s=\mathcal F_p,
\qquad s=42-p.                                         \tag{2}
\]

The following facts have already been proved and independently reviewed.

1. Every clause of \(G_0=U\) is a pure signed clause of length four.
2. Two original clauses which can resolve have opposite signs.  Their
   red/blue \(K_4\) supports share the pivot and no other variable, so their
   resolvent has exactly six literals.
3. If a clause \(C\) is a parent of a later non-tautological resolvent \(R\),
   then
   \[
   C\setminus\{\text{pivot literal}\}\subseteq R,
   \qquad |R|\ge |C|-1.                               \tag{3}
   \]
4. In a singular step with main clause \(xA\), every new resolvent has the
   common-core form
   \[
   Q_i=A\cup B_i.                                     \tag{4}
   \]
   The resolvents in a minimally unsatisfiable singular reduction are
   distinct.
5. The terminal formula is
   \[
   \mathcal F_p=
   \{\{\neg y_i,y_{i+1}\}:i\in\mathbb Z/p\mathbb Z\}
   \cup\{\{y_1,\ldots,y_p\},\{\neg y_1,\ldots,\neg y_p\}\}.
                                                               \tag{5}
   \]

No solver or enumeration is imported.

## Lemma 1: stagewise clause-length floor

For \(0\le t\le5\), every clause of \(G_t\) has length at least

\[
L_t=\min(4,7-t),
\qquad (L_0,\ldots,L_5)=(4,4,4,4,3,2).                \tag{6}
\]

### Proof

An original clause has length four unless it is removed.  For a derived
clause \(D\in G_t\), choose an earliest derived ancestor \(D_0\), created at
step \(j\ge1\).  Both parents of \(D_0\) are original, so the signed-\(K_4\)
intersection rule gives \(|D_0|=6\).  A path from \(D_0\) to \(D\) contains
at most \(t-j\) later resolutions.  Applying (3) along this path gives

\[
|D|\ge6-(t-j)\ge6-(t-1)=7-t.                         \tag{7}
\]

Taking the minimum with the unchanged original length four proves (6).
\(\square\)

## Lemma 2: at most one binary clause after five reductions

The formula \(G_4\) contains no binary clause, and \(G_5\) contains at most
one binary clause.

### Proof

Equation (6) gives \(|C|\ge3\) for every \(C\in G_4\), so no binary clause
is already present.  Consider the fifth singular step and write its main
clause as \(xA\).  Then \(|A|\ge2\).  If a new resolvent
\(Q_i=A\cup B_i\) is binary, necessarily

\[
|A|=2,
\qquad Q_i=A.                                         \tag{8}
\]

All binary resolvents of this step would therefore be the same clause.
Clause-set semantics and collision-freedom permit at most one distinct such
resolvent.  Hence \(G_5\) has at most one binary clause. \(\square\)

## Proposition 1: \(p=37\) is impossible

If \(p=37\), then (2) has five steps and \(G_5=\mathcal F_{37}\).  Formula
\(\mathcal F_{37}\) contains 37 distinct binary cycle clauses, contradicting
Lemma 2.  Therefore

\[
\boxed{p\ne37}.                                       \tag{9}
\]

This strengthens the equality-chain observation
\(6\to5\to4\to3\to2\): equality of lengths is not enough, because the common
main tail prevents the last step from proliferating 37 different binaries.

## Lemma 3: the binary cycle of \(\mathcal F_p\) has empty total intersection

For every \(p\ge3\), let

\[
Z_p=\{\{\neg y_i,y_{i+1}\}:i\in\mathbb Z/p\mathbb Z\}.
\tag{10}
\]

Then

\[
\bigcap_{Q\in Z_p}Q=\varnothing.                      \tag{11}
\]

### Proof

Each positive literal \(y_j\) occurs in exactly the single cycle clause
indexed by \(j-1\), and each negative literal \(\neg y_j\) occurs in exactly
the single clause indexed by \(j\).  Since \(p\ge3\), no literal belongs to
every member of \(Z_p\). \(\square\)

## Proposition 2: \(p=36\) is impossible

Suppose \(p=36\).  Then \(s=6\), so the last step reduces \(G_5\) to
\(G_6=\mathcal F_{36}\).  By Lemma 2, \(G_5\) has at most one binary clause.
Write the last main clause as \(xA\).

There are three exhaustive cases.

### Case 1: \(|A|\ge2\)

Every new binary resolvent contains \(A\).  If \(|A|=2\), it must equal
\(A\), so there is at most one distinct new binary clause; if \(|A|>2\),
there are none.  Together with at most one untouched old binary clause,
\(G_6\) has at most two binaries, not the 36 required by
\(\mathcal F_{36}\).

### Case 2: \(|A|=1\)

The main clause \(xA\) is binary.  It must be the unique possible binary
clause in \(G_5\), and the last DP step removes it.  Consequently all 36
terminal binary clauses must be new resolvents.  Equation (4) makes all of
them contain the single literal in \(A\), contradicting (11).

### Case 3: \(|A|=0\)

The main clause is a unit clause, impossible because (6) gives minimum
clause length two in \(G_5\).

All cases contradict \(G_6=\mathcal F_{36}\).  Hence

\[
\boxed{p\ne36}.                                       \tag{12}
\]

Combining (9), (12), and the previous \(p\le37\) barrier proves (1).

## Compact exact checker

`terminal-binary-proliferation-certificate.json` records the stage floors,
binary-count bounds, and survivor range.  The standard-library checker
`verify_terminal_binary_proliferation.py` verifies the integer deductions,
constructs the terminal cycle clauses directly, checks distinctness and
literal frequencies, and confirms their empty total intersection for both
\(p=36\) and \(p=37\).

Run

```bash
python3 ramsey_r55_symbolic_extension/verify_terminal_binary_proliferation.py \
  ramsey_r55_symbolic_extension/terminal-binary-proliferation-certificate.json
```

Expected output:

```text
verified: stage_floors=[4, 4, 4, 4, 3, 2], excluded=[36, 37], surviving_p=2..35
```

The checker is a definition-level audit of the compact certificate.  The
universal statement rests on Lemmas 1--3 and Propositions 1--2, not on a
solver result.

## Novelty assessment

Kullmann--Zhao establish the general singular-DP preservation and confluence
framework, and Kleine Büning supplies the deficiency-two terminal family.
The committed predecessor established the signed-\(K_4\) six-literal
ancestry barrier.  Searches of the primary SAT sources and the committed
graph did not locate the terminal **multiplicity** argument here: the common
main tail limits distinct binary proliferation, while the cycle clauses of
\(\mathcal F_p\) have empty total intersection.

The new claim is therefore the narrow Ramsey-specific exclusion of
\(p=36,37\), not a new general classification of minimally unsatisfiable
formulas and not a historical-priority claim beyond the searched sources.

## Sources and trust boundary

* O. Kullmann and X. Zhao,
  [*On Davis--Putnam reductions for minimally unsatisfiable clause-sets*](https://arxiv.org/abs/1202.2600v5),
  Theoretical Computer Science 492 (2013), 70--87.
* H. Kleine Büning,
  [*On subclasses of minimal unsatisfiable formulas*](https://doi.org/10.1016/S0166-218X(00)00245-6),
  Discrete Applied Mathematics 107 (2000), 83--98.

The imported non-elementary facts are the \(\mathrm{MU}(2)\) terminal
classification and singular-DP confluence/preservation theorem.  The new
deduction uses elementary set resolution, the already verified signed-clique
intersection property, and the predecessor's common-core classification.
The checker uses exact Python integers and finite sets, with no external
package, SAT solver, floating point, or generated search frontier.

