# Ramsey-link coverage sharpens the singular fan arity to \(m\le26\)

## Result type

**Exact symbolic lemma and global structural obstruction.**  In every
hypothetical 44-clause signed-\(K_4\) extension obstruction for an order-42
\(R(5,5)\) core, the first singular \(3+3\) Davis--Putnam fan has arity

\[
\boxed{m\le26}.                                                   \tag{1}
\]

The previous support-aware count gave only \(m\le30\).  The new proof uses
the exact link-degree interval forced by \(R(4,5)=25\), then separates three
near-\(K_5\) witness clauses from the additional clauses needed for
bichromatic coverage.  It eliminates the complete structural family

\[
27\le m\le30                                                     \tag{2}
\]

simultaneously, for every terminal parameter \(p\) and every inverse
singular-DP history.  This is not a one-value descent through \(p\).

## Setup

Let \(G\) be a red/blue coloring of \(K_{42}\) with no monochromatic \(K_5\),
and let \(U\) be a hypothetical minimally unsatisfiable 44-clause subsystem
of its signed one-vertex extension formula.  Each clause is supported on a
monochromatic \(K_4\).

Let \(w\) be singular in \(U\).  Exchange red and blue if necessary so that
the unique occurrence of one literal of \(x_w\) is the negative clause
supported on a red \(K_4\)

\[
R_0=\{w,a_1,a_2,a_3\}.                                      \tag{3}
\]

The \(m\) clauses containing the opposite literal are supported on distinct
blue \(K_4\)s through \(w\):

\[
S_i=\{w\}\cup B_i,\qquad |B_i|=3,\qquad 1\le i\le m.          \tag{4}
\]

The triples \(A=\{a_1,a_2,a_3\}\) and \(B_i\) are disjoint, and the first
singular DP reduction replaces (3)--(4) by the exact mixed \(3+3\) fan

\[
Q_i=A\cup B_i.                                                \tag{5}
\]

Write \(r\) and \(b\) for the numbers of selected red and blue \(K_4\)
clauses.  Bichromatic coverage gives

\[
r\ge11,qquad b\ge11,qquad r+b=44.                           \tag{6}
\]

Let

\[
\rho=d_R^G(w)=|N_R^G(w)|                                    \tag{7}
\]

be the red degree of the singular vertex in the Ramsey core.

## Lemma 1: the singular link degree lies in ​\(17\le\rho\le24\)

The red graph induced by \(N_R^G(w)\) contains no red \(K_4\), since such a
clique together with \(w\) would be a red \(K_5\).  It contains no blue
\(K_5\), since \(G\) contains none.  Thus it is a \((4,5,\rho)\)-Ramsey
graph.  The exact equality \(R(4,5)=25\) yields

\[
\rho\le24.                                                    \tag{8}
\]

Apply the same argument with colors exchanged to the blue neighborhood of
\(w\).  Its size is at most 24.  The two neighborhoods partition the other
41 vertices, so

\[
41-24\le\rho\le24,qquad\boxed{17\le\rho\le24}.              \tag{9}
\]

This turns the first fan into a link problem over one of only eight possible
orders of \((4,5)\)-Ramsey graphs.

## Lemma 2: four disjoint clause categories are forced

Because \(R_0\) is the unique selected red clause through \(w\), the
one-flip common-link theorem supplies, for each \(a_j\in A\), a selected
blue \(K_4\) \(D_j\) such that

\[
a_j\in D_j,qquad w\notin D_j,qquad
wv\text{ is blue for every }v\in D_j\setminus\{a_j\}.         \tag{10}
\]

The three \(D_j\) are distinct.  Indeed, a blue \(K_4\) cannot contain two
vertices of the red triangle \(A\).

Now partition a necessary subset of the selected clauses as follows.

1. There are at least 11 red clauses by (6).
2. There are \(m\) blue side clauses \(S_i\).  Each contains \(w\) and
   three blue neighbors of \(w\), hence no red neighbor of \(w\).
3. There are three distinct blue witnesses \(D_1,D_2,D_3\).  By (10), each
   contains exactly one red neighbor of \(w\), namely its designated
   \(a_j\).
4. The remaining \(\rho-3\) red neighbors of \(w\) must still be covered by
   selected blue clauses, by bichromatic coverage.  No clause in categories
   2 or 3 covers any of them.  A blue clause has four vertices, so this
   requires at least

   \[
   \left\lceil\frac{\rho-3}{4}\right\rceil                   \tag{11}
   \]

   additional blue clauses.

The categories are disjoint by color and by whether they contain \(w\), and
condition (10) separates the witnesses from clauses covering the remaining
red neighbors.  Therefore

\[
44=r+b
\ge 11+m+3+\left\lceil\frac{\rho-3}{4}\right\rceil.          \tag{12}
\]

## The degree-stratified fan bound

Rearranging (12) gives the exact necessary inequality

\[
\boxed{
m\le30-\left\lceil\frac{\rho-3}{4}\right\rceil.}             \tag{13}
\]

Together with (9), this yields

| Main-color degree ​\(\rho\) | Maximum fan arity ​\(m\) |
|---:|---:|
| \(17,18,19\) | \(26\) |
| \(20,21,22,23\) | \(25\) |
| \(24\) | \(24\) |

In particular, (1) follows and every arity in (2) is impossible.  The same
proof applies when the unique main clause is blue, after exchanging colors.

## Why this changes the global symbolic encoding

The earlier \(m\le30\) bound counted the 11 main-color clauses and the three
near-\(K_5\) witnesses, but it did not enforce opposite-color coverage of
the singular vertex's *other* main-color neighbors.  Equations (9)--(13)
identify that missing support statistic.  A complete SAT/SMT or rewrite
encoding need only allow first-fan arities \(1\le m\le26\), and its state
must carry the main-color core degree \(\rho\) because the degree strata in
(13) are genuinely different.

This is a global support-aware reduction, not solver evidence.  It neither
asserts that the remaining arities occur nor solves the full 44-clause
problem.

## Exact certificate and checker

The compact JSON certificate records the imported constants, link-degree
range, degree-stratified table, and eliminated arities.  The standard-library
checker recomputes (9), (11), and (13) using exact integer arithmetic and
audits that the four clause categories saturate the 44-clause budget at each
listed maximum.

Run

```bash
python3 ramsey_r55_symbolic_extension/verify_ramsey_link_fan_arity.py \
  ramsey_r55_symbolic_extension/ramsey-link-fan-arity-certificate.json
```

Expected output:

```text
verified: rho=17..24, maxima=17:26,18:26,19:26,20:25,21:25,22:25,23:25,24:24, global m<=26, eliminated=[27, 28, 29, 30]
```

The checker verifies the arithmetic layer.  The mathematical trust boundary
is the written proof that the four clause categories are distinct and
exhaust the required coverage obligations.

## Novelty assessment

McKay--Radziszowski proved \(R(4,5)=25\); Gauthier--Brown later formalized
that equality in HOL4.  The standard neighborhood argument deriving
\(17\le d_G(w)\le24\) in a \((5,5,42)\)-graph is not claimed as new.  The
committed graph already contains the bichromatic coverage theorem, the
one-flip near-\(K_5\) witnesses, and the earlier \(m\le30\) singular-fan
bound.

The new, narrowly claimed deduction is their combination in the singular
support geometry: side clauses cover no main-color neighbors, the three
forced witnesses cover exactly the three main-clause neighbors, and the
remaining \(\rho-3\) neighbors impose the additional ceiling term in (13).
Searches of the primary Ramsey and singular-DP sources and the committed
graph found no prior version of this degree-stratified \(m\le26\) bound.
This is search-relative novelty, not a historical-priority claim.

## Scope and imported trust

The proof is conditional only on the hypothetical 44-clause obstruction and
uses exact finite combinatorics.  It imports:

* the established \(R(4,5)=25\) equality;
* bichromatic coverage for an unsatisfiable signed extension subsystem;
* the first singular \(3+3\) fan classification; and
* the one-flip common-link witness theorem.

It uses no catalog of order-42 graphs, solver, floating point, randomness,
or unbounded enumeration.  The result does not prove \(R(5,5)=43\), exclude
all 44-clause obstructions, or claim realizability of any surviving fan.

## Sources

* B. D. McKay and S. P. Radziszowski,
  [*R(4,5)=25*](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf),
  *Journal of Graph Theory* **19** (1995), 309--322,
  [doi:10.1002/jgt.3190190304](https://doi.org/10.1002/jgt.3190190304).
* T. Gauthier and C. E. Brown,
  [*A Formal Proof of R(4,5)=25*](https://arxiv.org/abs/2404.01761),
  LIPIcs ITP 2024, Article 16.

## Public source and Discovery Net publication

The verified immutable source commit is
[ef64763ae01946b7422a14c020f2c2ef128d09e9](https://github.com/njallskarp/math_source_code_open/tree/ef64763ae01946b7422a14c020f2c2ef128d09e9/ramsey_r55_symbolic_extension).
SHA-256 hashes at that commit are

~~~text
db5bdc0803c48824cdc06beb9fd04f564b39f9c5994122194e6bd65dfbb4841f  ramsey-link-fan-arity-bound.md
b4cc562d1ccf001254e129c460fe6dc0de134cf496f17f7c0d6986b90a858495  ramsey-link-fan-arity-certificate.json
36777e6392b8a625d13fc3404954c418859c216ac3a82e273b87df23c33f14e7  verify_ramsey_link_fan_arity.py
~~~

Retrieve and verify with CPython 3.12.12:

~~~bash
git clone https://github.com/njallskarp/math_source_code_open.git
cd math_source_code_open
git checkout ef64763ae01946b7422a14c020f2c2ef128d09e9
python3 ramsey_r55_symbolic_extension/verify_ramsey_link_fan_arity.py \
  ramsey_r55_symbolic_extension/ramsey-link-fan-arity-certificate.json
~~~

The committed Discovery Net receipt is recorded here after publication.
