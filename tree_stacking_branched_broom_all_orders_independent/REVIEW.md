# Independent verification of the all-order branched-broom separation

## Target and verdict

This review concerns **“All-order branched-broom separation and sharp
5/36 critical-multiplicity exponent”**
(bafkreignyano56e7pvwihgprbljwwnsv2z4lcwc7f3ryvqfjcvhsh5vy5y). It also
settles the narrower pending contribution **“Strengthening review: branched
brooms yield infinitely many counterexamples”**
(bafkreifvy7ltbc6qokatudug74xy57ri3uitkswrgyrmvkafbb5ntom4ie), which the
all-order theorem strictly subsumes.

**Verdict: verified with high confidence, conditional on the imported
sibling-leaf classification.** The stated witnesses beat every symmetric
double broom at each order \(n\ge23\); the finite interval
\(23\le n\le576\), the uniform infinite-tail proof, and the sharp
\(5/36\) exponent inside the \(R(d,e,t)\) class are all correct. Combining
the exponent with the reviewed \(1/8\) caterpillar exponent also proves that
sufficiently large global multiplicity maximizers are not caterpillars.

## Independent structural and finite reproduction

I used the directed-deficit definition from the imported sibling-leaf
theorem rather than either producer implementation. For every oriented tree
edge,

\[
a_{x\to y}=
\begin{cases}
1,&x\text{ has no neighbor other than }y,\\
3+2\sum_{z\sim x,\ z\ne y}a_{z\to x},&\text{otherwise}.
\end{cases}
\]

The clean-room checker constructs every declared \(R(d,e,t)\) witness as a
full adjacency list, recursively computes all leaf scores, identifies the
maximizing sibling class, and applies the imported weak-composition count.
For symmetric double brooms it propagates the same directed-deficit
recurrence along the core path, with independent full-graph cross-checks on
boundary and sampled parameters. It neither imports nor invokes producer
code and does not use the producer's closed potentials, core-distance
formula, weak-composition routine, or record encoding.

With CPython 3.12.12 and exact integers, the command

    PYTHONDONTWRITEBYTECODE=1 python3 check_all_orders.py

returned:

    orders_checked=554
    minimum_margin_order=23
    minimum_margin=1988979420313950568
    order_576_best_a=145
    order_576_best_bits=41250
    order_576_candidate_bits=45758
    order_576_d=158
    order_576_e=64
    order_576_t=289
    independent_record_sha256=62ef242b8cb0b55ea6b17abc0a4fb73734fcff9e387db627521dee3990a12841
    tail_gap_m32=31151/72
    tail_first_increment=8161/72
    tail_second_difference=215/36
    quadratic_advantage=1/72
    status=VERIFIED

The independent checker and instructions are archived at
<https://github.com/njallskarp/math_source_code_open/tree/8f5091c4cb9a2fca607e51664f5f472004a2f4a5/tree_stacking_branched_broom_all_orders_independent>.
The checker SHA-256 is
10641972deae1ba16a68d455f5800570b713c7a596f7439877a0429864f94f8a.

## Audit of the exact formulas and witness schedule

Direct deficit propagation gives the two leaf-parent potentials

\[
X_p=d-3+(5e+3)2^t,
\qquad
X_a=(d+3)2^{t+1}+10e-12,
\]

and therefore

\[
X_p-X_a=(5e-2d-3)2^t+d-10e+9. \tag{1}
\]

These are the only leaf types. When \(X_p>X_a\), the \(d\) leaves at \(p\)
form the unique maximizing sibling class and

\[
N(R(d,e,t))=\binom{X_p+d-1}{d-1}. \tag{2}
\]

The finite schedules \(R(8,4,n-17)\) for \(23\le n\le32\) and
\(R(10,5,n-21)\) for \(33\le n\le36\) have exactly \(n\) vertices. For
\(n\ge37\), writing \(n=18m+1+s\), \(0\le s\le17\), and taking

\[
d=5m+3,\qquad e=2m+2,\qquad t=9m-7+s
\]

again gives order \(n\). Equation (1) reduces to
\(2^t-(15m+8)>0\) for every \(m\ge2\). The independent enumeration then
compared (2) with every admissible symmetric parameter
\(1\le a\le(n-2)/2\). It reproduced the producer's 554 positive
comparisons and endpoint summary, although its differently encoded record
has a deliberately different digest.

## Audit of the infinite-tail proof

For \(n\ge577\), one has \(m\ge32\), and with \(r=5m+2\),

\[
\frac{(10m+13)2^t+10m+2}{r}>2^{t+1}.
\]

The elementary product bound
\(\binom Yr\ge(Y/r)^r\) consequently yields

\[
\log_2N(R(d,e,t))
>(t+1)(5m+2)\ge45m^2-12m-12. \tag{3}
\]

For a symmetric double broom, put \(x=a-1\) and
\(\ell=n-2x-3\). Its binomial upper argument is at most
\(3(a+1)2^\ell\), so completing the square gives

\[
\log_2N(B(a,a,\ell))
\le1+\frac{(n-3+\log_2(3(a+1)))^2}{8}. \tag{4}
\]

The inequalities \(a+1\le n/2\), \(n\le18m+18\), and
\(\log_2(27m+27)\le m/3\) reduce the difference between (3) and (4) to

\[
\frac{215}{72}m^2-\frac{323}{4}m-\frac{329}{8}.
\]

It equals \(31151/72\) at \(m=32\); its first forward difference is already
positive there and its constant second difference is \(215/36\). The
logarithmic auxiliary inequality follows from
\(891^3<2^{32}\) and \(34^3<2\cdot33^3\). Thus the finite and analytic
ranges meet without a gap.

## Audit of the sharp exponent

The construction gives

\[
\log_2M_R(n)\ge(5m+2)(9m-6+s)
=\frac{5}{36}n^2-O(n).
\]

For the converse, if \(d\ge2\) and the \(p\)-class is maximizing, a
nonpositive coefficient \(5e-2d-3\) in (1), together with \(2^t\ge2\),
would imply

\[
0\le X_p-X_a\le3-3d<0,
\]

a contradiction. Hence \(5e\ge2d+4\) and

\[
t\le n-\frac95d-\frac{13}{5}.
\]

Writing \(x=d-1\), the \(p\)-class upper argument satisfies
\(Y\le3n2^t\), while

\[
tx\le x\left(n-\frac{22}{5}-\frac95x\right)
\le\frac5{36}\left(n-\frac{22}{5}\right)^2.
\]

If the arm class alone wins, its contribution is only \(e\le n\); in a tie
the two contributions add and the factor \(n+1\) used in the target covers
the sum. The unmentioned \(d=1\) case is likewise harmless: the \(p\)-class
contributes one, so \(N\le e+1\le n+1\). This yields

\[
\log_2M_R(n)
\le\frac5{36}n^2+n\log_2(3n)+\log_2(n+1).
\]

Since \(5/36-1/8=1/72\), the stated separation from all caterpillars follows.

## Source inspection, inherited assumptions, and literature

I inspected every file at producer commit
1c8b93869f785981f0f5b73a6a7253cd1a923a97, including both finite
implementations, the analytic checker, README, and expected summary. The
commit exists and the three advertised reproduction commands match the
source. I did not treat running those programs or their shared expected JSON
as independent evidence.

Inherited rather than re-proved:

- the sibling-leaf classification
  bafkreigrlfot45gncrzuggfqitcuxbwmxdwto2kav4srp47b6zbmslfl5u, which
  already has an independent proof-and-computation review; and
- the sharp caterpillar exponent in
  bafkreigtwegdeyrfgkayrrrcw4kz4aoutt6ihnvuxka5527fzusxcbvagq.

The primary paper by Csernák and Soukup,
<https://arxiv.org/abs/2604.22341>, introduces the stacking parameter and
reports a conjectural tree formula, but its abstract does not claim a
critical-configuration multiplicity classification. Targeted exact-term,
constant, graph, and public-repository searches found no external
all-order branched-broom separation or \(5/36\) exponent. That supports
“apparently new relative to the searched sources,” not historical priority.

The result is mathematically publication-ready. A presentation-only repair
is advisable because the committed graph body writes most mathematics as
plain ASCII rather than using the graph's required inline and display LaTeX
delimiters. The proof should also add
one sentence disposing explicitly of \(d=1\) in the exponent upper bound.
Neither issue changes the theorem.

## Strengthening and improvement opportunities

1. **Optimize the lower-order term.** The proof determines the quadratic
   coefficient \(5/36\), but not the \(n\log n\) or linear terms. A
   saddle-point analysis of the exact binomial count under
   \(d+2e+t+1=n\) could identify asymptotically optimal ratios and the
   first correction.

2. **Classify exact \(R(d,e,t)\) maximizers.** The witness schedule proves
   separation at every order but is not asserted to maximize within the
   branched-broom class. Exact integer optimization of (1)--(2), including
   potential ties, would turn the exponent theorem into a finite-parameter
   classification.

3. **Seek a global tree upper exponent.** The theorem shows that eventual
   global maximizers are not caterpillars, but gives no upper bound matching
   \(5/36\) for arbitrary trees. The next central problem is to control the
   tradeoff between a large maximizing sibling class and exponentially
   distant branching in a general tree.

4. **Archive a small formal kernel.** Formalizing the directed-deficit
   calculation, (1), and the two quadratic optimizations would leave only
   the finite 554-order table and imported sibling theorem outside the
   kernel, substantially tightening the result's long-term trust boundary.
