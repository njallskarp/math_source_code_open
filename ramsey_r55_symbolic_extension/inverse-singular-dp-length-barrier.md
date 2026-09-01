# Inverse singular-DP lifts are common-core splits, and \(F_{38},\ldots,F_{41}\) cannot lift to a 44-clause Ramsey obstruction

## Result type

**Exact symbolic classification and Ramsey-specific exclusion lemma.**  The
classification below describes every one-step inverse singular
Davis--Putnam extension of a minimally unsatisfiable clause-set.  Its
specialization to signed \(K_4\) extension clauses gives a unique final-step
shape and a clause-length ancestry obstruction.

The consequence is

\[
U\xrightarrow{\mathrm{sDP}}_{\!*}\mathcal F_p
\quad\Longrightarrow\quad 2\le p\le 37                  \tag{1}
\]

for every hypothetical 44-clause signed-\(K_4\) obstruction \(U\) on a
Ramsey \((5,5,42)\)-core.  Thus the four canonical terminal families
\(\mathcal F_{38},\mathcal F_{39},\mathcal F_{40},\mathcal F_{41}\) are
excluded.

This does **not** exclude every 44-clause obstruction.  The surviving
terminal range is exactly \(2\le p\le37\) at the level of the present
argument.

## Clause conventions

A literal is a signed variable, a clause is a finite clash-free set of
literals, and a clause-set is a finite set of clauses.  If \(x\) is fresh,
write

\[
xA:=\{x\}\cup A,\qquad \bar xB:=\{\bar x\}\cup B.       \tag{2}
\]

For a singular variable \(x\), choose its polarity so that \(x\) occurs in
the unique **main clause** \(xA\), while \(\bar x\) occurs in the nonempty
family of **side clauses** \(\bar xB_1,\ldots,\bar xB_m\).  Davis--Putnam
elimination replaces these clauses by

\[
Q_i=A\cup B_i\qquad(1\le i\le m).                     \tag{3}
\]

In a singular reduction inside \(\mathrm{MU}\), the resolvents in (3) are
non-tautological and distinct and do not collide with an untouched clause;
equivalently the step removes one variable and one clause.

## Proposition 1: complete one-step inverse classification

Let \(G\in\mathrm{MU}\).  Every singular inverse-DP extension \(H\) with
\(\operatorname{DP}_x(H)=G\), up to reversing the polarity of the fresh
variable \(x\), has the following form.

Choose a nonempty set of distinct clauses

\[
\mathcal Q=\{Q_1,\ldots,Q_m\}\subseteq G,              \tag{4}
\]

a common subclause

\[
A\subseteq\bigcap_{i=1}^m Q_i,                         \tag{5}
\]

and, independently for every \(i\), an overlap subclause \(O_i\subseteq A\).
Put

\[
B_i=(Q_i\setminus A)\cup O_i.                          \tag{6}
\]

Then

\[
H=(G\setminus\mathcal Q)
  \cup\{xA\}
  \cup\{\bar xB_i:1\le i\le m\}.                     \tag{7}
\]

Conversely, every singular inverse-DP extension with no resolvent collision
is represented uniquely by (4)--(7) after fixing the singular polarity and
taking \(A\) to be the main-clause tail.  In particular, (4)--(7) are the
complete allowable one-step **syntactic types**; no solver search is needed
to enumerate an additional kind of inverse step.

### Proof

For a given singular extension, remove \(x\) and \(\bar x\) from the main
and side clauses.  Equation (3) gives \(Q_i=A\cup B_i\).  Hence
\(A\subseteq Q_i\), \(Q_i\setminus A\subseteq B_i\subseteq Q_i\), and
\(O_i=A\cap B_i\) yields (6).  This proves necessity and uniqueness.

Conversely, (5)--(6) give \(A\cup B_i=Q_i\), so eliminating \(x\) in (7)
recovers \(G\) exactly.  It remains useful to record that (7) is again
minimally unsatisfiable, rather than merely an inverse image under
resolution.

It is unsatisfiable because every assignment satisfying \(H\) would satisfy
all resolvents \(Q_i\) and all clauses of \(G\setminus\mathcal Q\), hence
would satisfy \(G\).  For minimality:

* after deleting the main clause, satisfy \(G\setminus\mathcal Q\) and set
  \(x=0\);
* after deleting the side clause \(\bar xB_j\), take a satisfying assignment
  of \(G\setminus\{Q_j\}\).  If it satisfies \(A\), set \(x=0\); otherwise
  it satisfies every \(B_i\) for \(i\ne j\), so set \(x=1\);
* after deleting an untouched clause \(E\), take a satisfying assignment of
  \(G\setminus\{E\}\).  If it satisfies \(A\), set \(x=0\); otherwise it
  satisfies all \(B_i\), so set \(x=1\).

Thus every clause deletion is satisfiable.  Also

\[
c(H)=c(G)+1,\qquad v(H)=v(G)+1,\qquad\delta(H)=\delta(G). \tag{8}
\]

This proves the classification. \(\square\)

## Proposition 2: the signed-\(K_4\) final inverse step

Let \(U\) be a hypothetical 44-clause signed-\(K_4\) extension obstruction,
and let \(x_w\) be any singular variable in \(U\).  The inverse of the first
forward reduction \(U\to\operatorname{DP}_{x_w}(U)\) is, up to color
exchange, exactly the specialization

\[
A=\{x_a,x_b,x_c\},\qquad
B_i=\{\neg x_{r_i},\neg x_{s_i},\neg x_{t_i}\},
\qquad O_i=\varnothing,                                \tag{9}
\]

where the triples underlying \(A\) and \(B_i\) are disjoint and the
\(B_i\)'s are distinct.  Hence the selected clauses in the reduced formula
are the common-core fan

\[
Q_i=A\cup B_i,qquad |Q_i|=6,                          \tag{10}
\]

with sign profile \(3+3\).

Moreover its arity is bounded by

\[
1\le m\le30.                                           \tag{11}
\]

### Proof

Every leaf clause of \(U\) is pure and has length four.  The main and side
clauses containing opposite literals of \(x_w\) therefore have opposite
signs.  Their underlying red and blue \(K_4\)'s both contain \(w\), and
cannot share another vertex.  Deleting the pivot gives the disjoint signed
triples (9), proving (10).

For (11), bichromatic coverage forces at least

\[
\left\lceil\frac{42}{4}\right\rceil=11                \tag{12}
\]

clauses of the main-clause sign.  The one-flip near-\(K_5\) theorem forces
at least three clauses of the side-clause sign which avoid \(w\); these are
distinct from the \(m\) side clauses through \(w\).  Therefore

\[
44\ge 11+(m+3),
\]

which is equivalent to \(m\le30\). \(\square\)

## Proposition 3: the five-step binary-clause barrier

In every singular-DP sequence starting from \(U\), a derived binary clause
can first occur only after at least five reductions.

### Proof

Call the 44 pure length-four clauses of \(U\) **original**, and every
resolvent subsequently inserted **derived**.  Consider a derived clause
\(D\) and its resolution ancestry.  An earliest derived ancestor \(D_0\)
is the resolvent of two original clauses: otherwise one of its parents would
already be derived.  Those original clauses contain opposite literals of
the eliminated variable, so they have opposite signs.  The signed-\(K_4\)
intersection rule says their supports meet only in the pivot.  Consequently

\[
|D_0|=(4-1)+(4-1)=6.                                  \tag{13}
\]

If a clause \(C\) is a parent of a later non-tautological resolvent \(R\),
then

\[
C\setminus\{\text{pivot literal}\}\subseteq R,
\qquad |R|\ge |C|-1.                                  \tag{14}
\]

Thus a descendant of \(D_0\) can lose at most one literal per later
resolution on its ancestral path.  Reaching length two from length six
requires at least four later resolutions.  Including the step that created
\(D_0\), any derived binary clause requires at least five sequential
singular-DP steps.  An original clause has length four and cannot be a
terminal binary clause without becoming derived, so the conclusion applies
to every binary clause. \(\square\)

## Corollary: exclusion of \(p=38,39,40,41\)

The canonical nonsingular formula

\[
\mathcal F_p=
\{\{\neg y_i,y_{i+1}\}:i\in\mathbb Z/p\mathbb Z\}
\cup\{\{y_1,\ldots,y_p\},\{\neg y_1,\ldots,\neg y_p\}\}
\tag{15}
\]

contains \(p\ge2\) binary clauses.  A reduction

\[
U\xrightarrow{\mathrm{sDP}}_{\!*}\mathcal F_p
\]

has exactly \(42-p\) steps.  Proposition 3 therefore gives

\[
42-p\ge5,
\qquad\boxed{p\le37}.                                 \tag{16}
\]

This eliminates the nontrivial interval \(38\le p\le41\).  The exact
survivor range after this lemma is

\[
\boxed{2\le p\le37}.                                  \tag{17}
\]

## Compact exact checker

The file `inverse-dp-length-barrier-certificate.json` records the integer
parameters in (11)--(17).  The standard-library checker
`verify_inverse_dp_length_barrier.py` verifies all arithmetic and also
performs an exact truth-table audit of Proposition 1 for every common-core
split of \(\mathcal F_p\) with \(p=2,3,4\), including every allowed overlap
choice \(O_i\subseteq A\).

Run

```bash
python3 ramsey_r55_symbolic_extension/verify_inverse_dp_length_barrier.py \
  ramsey_r55_symbolic_extension/inverse-dp-length-barrier-certificate.json
```

The expected final line is

```text
verified: inverse-step classification samples, m<=30, p<=37, excluded=[38, 39, 40, 41]
```

The finite audit is regression evidence for the exact inverse constructor;
it is not substituted for the universal proof above.

## Novelty assessment

The imported SAT facts are that singular DP reduction preserves minimal
unsatisfiability and deficiency and that complete singular reduction in
\(\mathrm{MU}(2)\) is confluent up to isomorphism.  Kullmann--Zhao discuss
inverse singular reduction and give the general preservation criteria, but
the searched primary sources do not connect inverse steps to signed
Ramsey-clique intersection geometry.

The new content claimed here is narrowly Ramsey-specific: the common-core
split formulation (4)--(7) as the exact search alphabet, its forced
disjoint \(3+3\) specialization and arity bound \(m\le30\), and the
resolution-ancestry length barrier excluding \(\mathcal F_{38}\) through
\(\mathcal F_{41}\).  This is not a historical-priority claim beyond the
searched sources and committed graph.

## Sources and trust boundary

* O. Kullmann and X. Zhao,
  [*On Davis--Putnam reductions for minimally unsatisfiable clause-sets*](https://arxiv.org/abs/1202.2600v5),
  Theoretical Computer Science 492 (2013), 70--87.
* H. Kleine Büning,
  [*On subclasses of minimal unsatisfiable formulas*](https://doi.org/10.1016/S0166-218X(00)00245-6),
  Discrete Applied Mathematics 107 (2000), 83--98.

The only non-elementary imported inputs are the established
\(\mathrm{MU}(2)\) normal-form and confluence theorems.  Proposition 1 is a
direct clause-set argument; Propositions 2--3 use only the previously
proved bichromatic coverage, one-flip witness theorem, and red/blue
\(K_4\)-intersection rule.  The Python checker uses exact finite sets and
Boolean truth tables and has no solver, floating-point, or external-data
dependency.

