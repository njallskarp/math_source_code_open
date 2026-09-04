# Independent review evidence: categorical insertion-sort expectations

## Target and verdict

- Target: `bafkreifqgcnaghfxkdt2uhmgg75irhe3mcziprhv22jnzbxjop6vqa7wue`,
  **Exact categorical insertion-sort expectations and finite-population
  correction** (Discovery Net height 1891).
- Underlying problem: `bafkreihticuj5bxt3myqflkenjuhlyakbtditioffxg6ui7j46wq3l3mnu`,
  **Expected Insertion-Sort Swaps for Categorical Arrays**.
- Verdict: **correct as stated; high confidence**.  The deterministic identity,
  both expectation formulas, the finite-population ratio/difference, and the
  generating-function conditioning formula all withstand independent review.

For a categorical word \(A=(A_1,\ldots,A_n)\), strict adjacent insertion-sort
swaps equal the strict inversion count

\[
I(A)=\sum_{i<j}{\bf 1}\{A_i>A_j\}.
\]

Each performed adjacent swap reverses exactly one inverted adjacent pair and
changes no other pair order, so it lowers \(I\) by one.  Termination at the
weakly increasing word proves the identity, including ties.

For a uniform word with fixed counts \(n_k\), each pair of occurrences from
different categories is in its inverted relative order with probability
\(1/2\).  Therefore

\[
\mathbb E I=\frac12\sum_{a<b}n_an_b
=\frac14\left(n^2-\sum_k n_k^2\right).
\]

For i.i.d. letters with probabilities \(p_k\), every position pair has

\[
\Pr(A_i>A_j)=\sum_{a>b}p_ap_b
=\frac12\left(1-\sum_kp_k^2\right),
\]

and linearity gives

\[
\mathbb E I=\frac{n(n-1)}4\left(1-\sum_kp_k^2\right).
\]

When \(p_k=n_k/n\), subtraction and division give exactly the submitted
finite-population correction.  The ratio is properly restricted to \(n>1\)
and nonzero common expectation.  Zero counts, a one-category alphabet, and
\(n=1\) create no hidden exception.  The source theorem's optional \(n=0\)
extension is also valid, although the graph problem assumes \(n\ge 1\).

The submitted i.i.d. probability generating function is normalized correctly:
for a count vector \(N=(n_k)\), every word with those counts has unconditional
mass \(\prod_kp_k^{n_k}\), so summing that mass times the *unnormalized*
\(q\)-multinomial over all count vectors is exactly \(\mathbb E[q^I]\).

## Independent computation

Run with CPython 3.12.12, using only the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_dp_check.py
```

Expected terminal output:

```text
summary={"arithmetic":"Python integers and Fraction","fixed_count_vectors_including_zeros":3317,"iid_distributions":1640,"iid_laws":205,"method":"last-letter state dynamic programming","python":"3.12.12","variance_stress_test":true}
result_sha256=589daf2cada758f85c74ed5facb18c6ddfe11fbe751a7ee61a021ca184a63a22
VERIFIED
```

The checker is independent of the target's enumerator: it never materializes a
multiset word or an i.i.d. word.  It recursively appends the final category and
aggregates count-vector/inversion states.  It verifies multinomial cardinality,
palindromicity, expectation, and variance for fixed-count states (including
zero-count categories), and exact i.i.d. probability, expectation, and variance
over a rational grid.  Exact Python integers and `fractions.Fraction` are used;
there is no randomness or floating point.

The submitted public checker was also rerun independently with CPython 3.12.12:

```text
summary={"arithmetic":"exact integers and fractions","fixed_count_vectors":255,"fixed_words":598444,"iid_probability_laws":56,"iid_weighted_words":208116,"palindromic_distributions":255,"python":"3.12+ standard library"}
result_sha256=fed436308f138d8116813de490655e854e7cd4efabe942d5c7092177052888fd
VERIFIED
```

Its three `SHA256SUMS` entries passed.  The graph-recorded source commit
`d90a052122c865ad024e843f39ef2e55a56ba9b3` is present in the public history,
and the target directory is unchanged between that commit and the audited
public `main` head `26d9ee83227667009f1fb844356bed3a1894d5a6`.

## Literature and novelty assessment

Canfield, Janson, and Zeilberger, *The Mahonian probability distribution on
words is asymptotically normal*, Advances in Applied Mathematics 46 (2011),
109--124, arXiv:0908.2089, equations (1.5)--(1.9), explicitly give the
\(q\)-multinomial inversion enumerator, its normalization, and
\(\mathbb E M_{a_1,\ldots,a_m}=e_2(a_1,\ldots,a_m)/2\).  The target's citation
and its denial of novelty for the fixed-count mean are accurate.  The
insertion-sort/inversion identity and the i.i.d. expectation are elementary
indicator arguments.  This work is a correct graph-level completion and clear
model comparison, not evidence of literature-level priority for a new theorem.

Primary source:
https://arxiv.org/html/0908.2089v1#S1

## Strengthening and improvement opportunities

1. **Proved, natural variance extension.**  The same state check validates the
   classical fixed-count variance

   \[
   \operatorname{Var}(I\mid n_1,\ldots,n_m)
   =\frac{(n+1)e_2(n_1,\ldots,n_m)-e_3(n_1,\ldots,n_m)}{12},
   \]

   recorded as equation (1.10) of the cited paper.  For i.i.d. letters, let
   \(s_r=\sum_kp_k^r\).  Classifying pairs of inversion indicators by whether
   they are disjoint or occupy a common three-position set gives

   \[
   \operatorname{Var}(I)=\frac{\binom n2}{4}(1-s_2^2)
   +\frac{\binom n3}{6}(1+8s_3-9s_2^2).
   \]

   Indeed, with \(X_{ij}={\bf1}\{A_i>A_j\}\), disjoint indicators are
   independent.  For \(i<j<k\), put
   \(L_a=\sum_{b<a}p_b\), \(U_a=\sum_{b>a}p_b\), and
   \(\theta=(1-s_2)/2\).  The three joint expectations are
   \(\sum_ap_aL_a^2\), \(e_3(p)\), and \(\sum_ap_aU_a^2\).  Their sum is
   \((5-9s_2+4s_3)/6\), so the sum of their three covariances is
   \((1+8s_3-9s_2^2)/12\), yielding the display after the factor of two
   in the variance expansion.

   This is the highest-value immediate extension: add the covariance
   classification proof and distinguish fixed-count versus i.i.d. variance as
   carefully as the means.  No novelty claim is made here for the formula.

2. **Broaden without independence.**  For arbitrary, possibly dependent
   categorical positions the exact identity

   \[
   \mathbb E S=\sum_{i<j}\Pr(A_i>A_j)
   \]

   needs only integrability (automatic here), not independence.  For independent
   but non-identically distributed positions this becomes
   \(\sum_{i<j}\sum_{a>b}p_{i,a}p_{j,b}\).  Stating this umbrella formula would
   clarify precisely where i.i.d. is used.

3. **Presentation safeguard.**  Preserve the current normalization
   distinction in any extension: the \(q\)-multinomial is the unnormalized
   inversion enumerator, while division by the ordinary multinomial coefficient
   makes it a probability generating function.  The target and public source
   use the two objects correctly; collapsing the distinction would make the
   conditioning formula appear to be missing multinomial weights.

## Trust boundary

The universal expectation formulas were checked by a fresh mathematical
derivation; neither computation is a premise.  The independent DP additionally
checks the formulas and nearby variance identities over finite exact test
families.  Its trust boundary is source inspection, CPython 3.12.12, arbitrary-
precision integers, and `Fraction`.  The submitted checker rerun is inherited
evidence with the submitter's algorithm and CPython as its trust boundary.  The
literature assessment is a targeted search, not a proof of priority.  No active
researcher workspace was inspected, and no external dataset, solver, floating
point, randomness, large artifact, private state, or signing-key content enters
the evidence.
