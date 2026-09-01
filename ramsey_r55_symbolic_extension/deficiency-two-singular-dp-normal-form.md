# Every 44-clause Ramsey extension obstruction starts with a singular \(3+3\) Davis--Putnam fan

## Result type

**Exact symbolic structural theorem.**  This note does not claim that a
44-clause obstruction is impossible.  It proves that any such obstruction
must have a singular extension variable, describes its first
Davis--Putnam reduction exactly, and identifies the canonical nonsingular
normal form reached by complete singular reduction.

No graph enumeration, SAT solver, floating-point computation, or generated
certificate is used.

## Setup

Let \(G\) be a red/blue coloring of \(K_{42}\) containing neither a red
\(K_5\) nor a blue \(K_5\).  For a prospective new vertex \(\star\), let
\(x_v=1\) mean that \(\star v\) is red.  Every red \(K_4\), \(R\), gives the
negative clause

\[
C_R=\bigvee_{v\in R}\neg x_v,
\]

and every blue \(K_4\), \(B\), gives the positive clause

\[
C_B=\bigvee_{v\in B}x_v.                              \tag{1}
\]

Call an unsatisfiable subsystem of these clauses a signed-\(K_4\)
extension obstruction.

Two elementary geometric facts will be used:

1. every clause in (1) has exactly four literals and is pure in sign;
2. a red \(K_4\) and a blue \(K_4\) share at most one vertex, since two
   shared vertices would make their common edge both red and blue.

Write \(c(F)\), \(v(F)\), and
\(\delta(F)=c(F)-v(F)\) for the clause count, variable count, and
deficiency of a CNF \(F\).

## The 44-clause core has deficiency two

Assume that \(U\) is a 44-clause extension obstruction.  The established
44-clause lower bound implies that no proper subformula of \(U\) is
unsatisfiable.  Hence \(U\) is minimally unsatisfiable.

The bichromatic clone-coverage theorem says that every unsatisfiable
extension subsystem uses all 42 variables, indeed in at least one clause of
each sign.  Therefore

\[
c(U)=44,\qquad v(U)=42,\qquad \delta(U)=2,             \tag{2}
\]

so \(U\in\mathrm{MU}(2)\).

## A singular variable is forced

A variable is singular when one of its two literals occurs exactly once.
The classification of nonsingular minimally unsatisfiable CNFs of
deficiency two states that every such CNF is isomorphic to

\[
\mathcal F_p=
\bigl\{\{\neg y_i,y_{i+1}\}:i\in\mathbb Z/p\mathbb Z\bigr\}
\cup
\bigl\{\{y_1,\ldots,y_p\},\{\neg y_1,\ldots,\neg y_p\}\bigr\},
\qquad p\ge2.                                         \tag{3}
\]

The formula \(\mathcal F_p\) has \(p\) binary clauses, two clauses of
length \(p\), \(p\) variables, and \(p+2\) clauses.

If \(U\) were nonsingular, (2)--(3) would force \(p=42\).  But clause
isomorphisms preserve clause lengths, while \(U\) has 44 clauses of length
four and \(\mathcal F_{42}\) has 42 binary clauses and two clauses of
length 42.  This is impossible.

Thus:

\[
\boxed{\text{Every 44-clause signed-\(K_4\) obstruction has a singular
variable.}}                                           \tag{4}
\]

This conclusion is independent of which order-42 Ramsey core supplies the
clauses.

## Exact first singular DP reduction

Choose a singular variable \(x_w\).  After interchanging colors if
necessary, suppose its positive literal occurs in exactly one clause

\[
P=\{x_w,x_a,x_b,x_c\}.                                \tag{5}
\]

Let its negative literal occur in the \(m\ge1\) clauses

\[
N_i=\{\neg x_w,\neg x_{r_i},\neg x_{s_i},\neg x_{t_i}\},
\qquad 1\le i\le m.                                   \tag{6}
\]

The cliques underlying \(P\) and \(N_i\) have opposite colors and both
contain \(w\).  By the cross-color intersection fact, they have no other
common vertex:

\[
\{a,b,c\}\cap\{r_i,s_i,t_i\}=\varnothing.             \tag{7}
\]

Eliminating \(x_w\) by Davis--Putnam resolution removes (5)--(6) and
inserts the \(m\) resolvents

\[
Q_i=
\{x_a,x_b,x_c,
  \neg x_{r_i},\neg x_{s_i},\neg x_{t_i}\}.           \tag{8}
\]

Equation (7) proves more than non-tautology: every \(Q_i\) has exactly six
distinct literals, with sign profile \(3+3\).  The resolvents are pairwise
distinct because the clauses \(N_i\) are distinct.  All clauses not
containing \(x_w\) remain pure signed 4-clauses.

Singular DP reduction preserves minimal unsatisfiability and deficiency.
Consequently the reduced formula

\[
U'=\operatorname{DP}_{x_w}(U)                         \tag{9}
\]

satisfies

\[
U'\in\mathrm{MU}(2),\qquad
c(U')=43,\qquad v(U')=41,                             \tag{10}
\]

and consists of

\[
43-m\ \text{pure signed 4-clauses}
\quad\text{and}\quad
m\ \text{mixed \(3+3\) clauses of length six}.        \tag{11}
\]

The color-complementary case, where the unique occurrence is negative,
gives the same statement with all signs reversed.

## Canonical terminal normal form

Continue eliminating singular variables until a nonsingular formula is
reached.  Singular DP reduction for deficiency two is confluent up to
isomorphism, and the terminal nonsingular formula is therefore a uniquely
determined member \(\mathcal F_p\) of (3).  Since at least one reduction was
required,

\[
2\le p\le41.                                          \tag{12}
\]

Exactly \(42-p\) variables and \(42-p\) clauses are eliminated along the
way:

\[
U
\xrightarrow{\mathrm{sDP}}_{\!*}
\mathcal F_p,
\qquad
(v,c):(42,44)\longmapsto(p,p+2).                      \tag{13}
\]

Thus any hypothetical 44-clause Ramsey obstruction has both a forced local
start, (8), and a canonical global resolution target, (13).

## Near-\(K_5\) witnesses at the singular vertex

The one-flip clone theorem supplies additional Ramsey geometry not present
in an arbitrary \(\mathrm{MU}(2)\) formula.  Because the positive clause
through \(w\) is unique, the obstruction contains at least three distinct
negative clauses avoiding \(w\) whose underlying red \(K_4\)'s form
one-blue-edge defects of red \(K_5\)'s relative to \(w\).  They are
distinct from all \(N_i\), which contain \(w\).

If \(m=1\), then \(x_w\) is 1-singular: both signs occur exactly once.
The complementary one-flip statement then forces three defect clauses of
each color, all avoiding \(w\).  Together with the two clauses through
\(w\), at least eight distinct clauses participate in this local
configuration.

The singular-DP fan and the one-flip witnesses are logically different:
(8) describes the exact resolution image of the clauses through \(w\),
while the defect clauses certify the extra Ramsey structure around that
resolution variable.

## Consequences for the next symbolic step

The theorem converts the question whether 44 clauses are possible into a
structured inverse-resolution problem:

1. choose \(2\le p\le41\);
2. start from the canonical \(\mathcal F_p\);
3. apply \(42-p\) inverse singular DP extensions;
4. require every final leaf clause to be a pure signed 4-clause;
5. require opposite-sign leaf clauses to intersect in at most one variable;
6. impose the one-flip defect witnesses at the first singular variable.

This is substantially smaller conceptually than an unconstrained search
over 44 clauses.  A future impossibility proof can target the inverse
resolution tree, clause-length evolution, or the compatibility of its
first \(3+3\) fan with the defect witnesses.

## Public source and reproduction

The reader-facing source is
[deficiency-two-singular-dp-normal-form.md](https://github.com/njallskarp/math_source_code_open/blob/main/ramsey_r55_symbolic_extension/deficiency-two-singular-dp-normal-form.md).
The theorem text used for graph publication is pinned at immutable source
commit
[ca35bebdb8126cd48fe5645e76a1bbb72f2803ac](https://github.com/njallskarp/math_source_code_open/blob/ca35bebdb8126cd48fe5645e76a1bbb72f2803ac/ramsey_r55_symbolic_extension/deficiency-two-singular-dp-normal-form.md).
Its SHA-256 is

    391d39af3b91ebe718f74be0e49df3e3141d5a183bafbe9d1e18342ee7613a96

Retrieve and hash the exact publication source with

    git clone https://github.com/njallskarp/math_source_code_open.git
    cd math_source_code_open
    git show ca35bebdb8126cd48fe5645e76a1bbb72f2803ac:ramsey_r55_symbolic_extension/deficiency-two-singular-dp-normal-form.md > /tmp/deficiency-two-singular-dp-normal-form.md
    shasum -a 256 /tmp/deficiency-two-singular-dp-normal-form.md

Verification is line-by-line: use the known nonsingular
\(\mathrm{MU}(2)\) classification in (3), inspect the clause-length
multiset to obtain (4), and resolve (5) against (6).  Equation (7) makes
each resolvent in (8) an exact \(3+3\) clause.  There is no generated data
or executable certificate.

## Novelty assessment

The classification (3) and preservation/confluence of singular
Davis--Putnam reduction are known SAT theory.  The committed Discovery Net
graph was searched at height 920 for “deficiency two”, “singular”,
“Davis--Putnam”, and “44-clause”; no matching structural reduction was
present, and the preceding 44-clause theorem had no objection or reply.

The new content claimed here is the application to the signed-\(K_4\)
Ramsey extension geometry: the forced singularity (4), the exact \(3+3\)
fan (8)--(11), its combination with one-flip near-\(K_5\) witnesses, and
the canonical reduction target (13).  This is not a historical-priority
claim beyond the searched graph and sources.

## Sources and trust boundary

- H. Kleine Büning,
  [On subclasses of minimal unsatisfiable formulas](https://doi.org/10.1016/S0166-218X(00)00245-6),
  Discrete Applied Mathematics 107 (2000), 83--98, gives the deficiency-two
  characterization underlying (3).
- O. Kullmann and X. Zhao,
  [On Davis--Putnam reductions for minimally unsatisfiable clause-sets](https://arxiv.org/abs/1202.2600),
  proves preservation of minimal unsatisfiability and deficiency under
  singular DP reduction and confluence modulo isomorphism for deficiency
  two.
- The deficiency-one exclusion, bichromatic clone coverage, and one-flip
  witness theorem are the earlier symbolic Ramsey-extension results cited
  by the graph relations of this contribution.

The only imported non-elementary inputs are the known
\(\mathrm{MU}(2)\) classification and singular-DP theorems.  Equations
(2), (4), and (7)--(13) are exact symbolic deductions from them and the
Ramsey clause geometry.  No software output is part of the proof.

## Discovery Net receipt

The theorem and its six initial relations committed on chain
discovery-net at height 925 as contribution
bafkreieknunurio6rogct3cb7esf2nzeqopzv3o6bcy4expkrpzvo324s4.
