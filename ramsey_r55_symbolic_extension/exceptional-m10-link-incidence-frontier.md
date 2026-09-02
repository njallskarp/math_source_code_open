# The exceptional \(m=10\) first fan has only 39 red-link incidence profiles

## Result type

**Exact symbolic lemma, structural-family exclusion, and complete finite
projection.** Consider the exceptional equality state from the
incidence-budget first-fan normalization theorem. Up to exchanging colors,
the unique singular vertex \(w\) has selected clause degrees

\[
(d_R^U(w),d_B^U(w))=(1,10),                                \tag{1}
\]

the selected color split is \((r,b)=(21,23)\), and every vertex other than
\(w\) has selected blue degree two.

Let

\[
\rho=d_R^G(w)                                               \tag{2}
\]

be the red degree of \(w\) in the underlying \((5,5,42)\)-Ramsey core.
Then

\[
\boxed{17\le \rho\le21}.                                   \tag{3}
\]

Thus the complete exceptional structural family with

\[
\rho\in\{22,23,24\}                                        \tag{4}
\]

is impossible. For each surviving \(\rho\), the selected blue clauses have
one of exactly 39 canonical red-link intersection profiles: 18, 11, 6, 3,
and 1 profiles for \(\rho=17,18,19,20,21\), respectively.

This is a complete classification of the intersection-number projection,
not a claim that all 39 profiles lift to actual red/blue \(K_4\) supports.

## Exact clause decomposition at the singular pivot

Write the unique selected red clause through \(w\) as

\[
R_0=\{w,a_1,a_2,a_3\}.                                    \tag{5}
\]

The ten selected blue side clauses through \(w\) have the form

\[
S_i=\{w\}\cup T_i,\qquad T_i\subseteq N_B^G(w),
\qquad 1\le i\le10.                                       \tag{6}
\]

Hence they contain no vertex of \(N_R^G(w)\). The remaining

\[
23-10=13                                                   \tag{7}
\]

selected blue clauses avoid \(w\).

The one-flip common-link theorem supplies three distinct selected blue
witnesses \(D_1,D_2,D_3\), also avoiding \(w\), such that

\[
D_j\cap N_R^G(w)=\{a_j\}.                                 \tag{8}
\]

Their distinctness is essential: one blue clause cannot witness two
vertices of the red triangle \(\{a_1,a_2,a_3\}\).

## The link-incidence cutoff

Every vertex of \(N_R^G(w)\) is different from \(w\), and the exceptional
degree profile gives it selected blue degree exactly two. Therefore the
total selected blue incidence into the red neighborhood is

\[
\sum_{B\in U_B}|B\cap N_R^G(w)|=2\rho.                     \tag{9}
\]

The ten clauses in (6) contribute zero. Thus all of (9) must be carried by
the thirteen clauses avoiding \(w\). The three witnesses in (8) contribute
exactly three incidences. Each of the remaining ten blue \(K_4\)'s
contributes at most four, so

\[
2\rho\le3+10\cdot4=43.                                    \tag{10}
\]

Since \(\rho\) is integral,

\[
\rho\le21.                                                  \tag{11}
\]

The previously proved Ramsey-link interval \(17\le\rho\le24\) now gives
(3). This argument is independent of the terminal formula \(F_p\) and of
all later singular-DP steps.

## Canonical residual deficit profiles

Remove one witness \(D_j\) for each \(a_j\). The choice is immaterial at
the profile level: every possible witness has red-neighborhood intersection
one. Let \(\mathcal C\) be the ten remaining blue clauses avoiding \(w\).
For \(C\in\mathcal C\), define its deficit

\[
\delta(C)=4-|C\cap N_R^G(w)|=|C\cap N_B^G(w)|\in\{0,1,2,3,4\}. \tag{12}
\]

Equations (8)--(9) give the exact identity

\[
\sum_{C\in\mathcal C}\delta(C)
=40-(2\rho-3)
=43-2\rho.                                                  \tag{13}
\]

Let

\[
x_j=|\{C\in\mathcal C:\delta(C)=j\}|,
\qquad 0\le j\le4.                                        \tag{14}
\]

Then every exceptional support system maps to a nonnegative integer solution
of

\[
\sum_{j=0}^4x_j=10,
\qquad
\sum_{j=0}^4j x_j=43-2\rho.                               \tag{15}
\]

Conversely, equations (14)--(15) completely classify the residual
intersection-number multiset: a solution vector uniquely decodes to ten
deficits, with \(x_j\) copies of \(j\). Therefore sorting by the vector
\((x_0,x_1,x_2,x_3,x_4)\) is a complete canonicalization at this projection
level.

Exact enumeration of (15) gives:

| \(\rho\) | Total deficit \(43-2\rho\) | Canonical profiles | Forced selected blue \(K_4\)'s inside \(N_R(w)\) |
|---:|---:|---:|---:|
| 17 | 9 | 18 | at least 1 |
| 18 | 7 | 11 | at least 3 |
| 19 | 5 | 6 | at least 5 |
| 20 | 3 | 3 | at least 7 |
| 21 | 1 | 1 | exactly 9 |

The last column follows because a positive-deficit clause consumes at least
one unit of the total deficit. Hence

\[
x_0\ge10-(43-2\rho)=2\rho-33.                             \tag{16}
\]

At the top stratum \(\rho=21\), (15) has the unique solution

\[
(x_0,x_1,x_2,x_3,x_4)=(9,1,0,0,0).                        \tag{17}
\]

Thus nine residual selected blue clauses lie wholly inside the red
neighborhood and the tenth has a \(3+1\) red/blue-neighborhood split.

## Consequence for the global symbolic encoding

The exceptional \(m=10\) branch no longer needs an unconstrained degree
stratum or a 13-clause off-pivot alphabet. A complete support-aware encoding
may:

1. restrict \(\rho\) to \(17,18,19,20,21\);
2. choose one of the 39 certified vectors in (15);
3. realize the corresponding red-link intersection sizes with actual blue
   \(K_4\) supports;
4. enforce the three distinguished one-flip witnesses; and
5. impose opposite-color intersection, \(K_5\)-freeness, and singular-DP
   ancestry only after this projection.

The unique \(\rho=21\) profile is the strongest next symbolic target. Its
nine internal blue \(K_4\)'s and exact degree-two coverage can be tested
against the finite family of \((4,5,21)\)-link graphs, preferably with a
proof-producing SAT encoding or a completeness-proved rewrite certificate.

## Exact certificate and checker

The JSON certificate contains all 39 canonical vectors. The standard-library
checker independently reconstructs equations (7), (10), and (13), enumerates
every nonnegative solution of (15), verifies the internal-\(K_4\) staircase
(16), and checks a canonical SHA-256 digest.

Run:

~~~bash
python3 ramsey_r55_symbolic_extension/verify_exceptional_m10_link_incidence.py \
  ramsey_r55_symbolic_extension/exceptional-m10-link-incidence-certificate.json
~~~

Expected summary:

~~~text
verified: exceptional m=10 forces 17<=rho<=21; canonical profile counts={17: 18, 18: 11, 19: 6, 20: 3, 21: 1}; total=39; sha256=61af373a215e67d106d050518d9630ca50864ba474275b620391ff4cae93dc62
~~~

## Novelty assessment

The committed graph was searched through height 1135 for “link-incidence,”
“rho<=21,” “exceptional first-fan,” and related normalization language. No
matching contribution was found beyond the imported \(m\le10\) normalization
and \(m\le26\) universal link bound. Targeted searches of the primary Ramsey
extension and singular-DP literature found no statement of (10), (13), or
the 39-profile projection.

The claimed new content is the synthesis of the exceptional signed-degree
profile with the one-flip witnesses and the actual red/blue neighborhood
partition. This is an apparent novelty claim relative to the searched graph
and sources, not a historical-priority claim.

## Scope and trust boundary

The proof imports the exceptional incidence profile, the one-flip
common-link witness theorem, and the prior \(17\le\rho\le24\) Ramsey-link
interval. The new cutoff and profile classification use only exact counting.
No SAT, SMT, floating-point computation, terminal \(F_p\), or objective-level
enumeration is used.

The 39 vectors are necessary intersection-number states. The certificate
does not assert that any vector is realizable by actual red and blue
\(K_4\)'s in one \(K_5\)-free core, nor that a profile lifts through the
remaining singular-DP ancestry. The checker audits the arithmetic and finite
canonicalization; the reduction from Ramsey supports to (9) and (12) remains
the proof text.

## Public source and provenance

The reader-facing source is
[exceptional-m10-link-incidence-frontier.md](https://github.com/njallskarp/math_source_code_open/blob/main/ramsey_r55_symbolic_extension/exceptional-m10-link-incidence-frontier.md).
Verified source commit: `9cace153cc88d44b3d1035bd0d76026650247b48`.

- Research note SHA-256:
  `81f988e68f4c6b458e3121314d38189e4a94bb42ac80cfe4b5e26df7fc6642b9`.
- Exact certificate SHA-256:
  `1b72bb55d5d113bfa7417965cd8c78b0b5d2a7b955fb500ab137a282ff53f63a`.
- Checker SHA-256:
  `0938bc18cad4b1c9d07b51c570800ff8a308b7b7a4c8989411ac89c795196e90`.

The Discovery Net receipt is added after committed inclusion.
