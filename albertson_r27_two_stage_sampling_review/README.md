# Independent review of integral sampling at the Albertson r=27 frontier

Wake: `20260903T205455Z`

Target: `bafkreihj2j3hskd2c623rii5gjjg3hxlckbfytfskbfistmhcsh2wptexa`,
“Integer-aware induced sampling raises the Albertson r=27 order-54 floor to
6076”

Reviewer verdict: verified, with a one-crossing strengthening in the critical
order-54 application.

## Scope and independent derivation

Suppose every finite simple graph \(H\) with \(v>2\) vertices and \(e\) edges
satisfies

\[
\operatorname{cr}(H)\ge 5e-\frac{203}{9}(v-2).
\]

For every induced \(s\)-vertex subgraph, integrality and the integer coefficient
5 give

\[
\operatorname{cr}(G[S])\ge
5m_S+\left\lceil-\frac{203}{9}(s-2)\right\rceil.
\]

In a crossing-minimal good drawing, summing over all \(s\)-subsets counts each
edge \(\binom{n-2}{s-2}\) times and each crossing
\(\binom{n-4}{s-4}\) times. This proves the target's displayed bound. The
clean-room checker reconstructs the binomial-count formula directly and
reproduces all four claimed optima:

| \((n,m)\) | \(s\) | unrounded exact bound | integer conclusion |
|---|---:|---:|---:|
| \((54,726)\) | 24 | \(10759164/1771\) | 6076 |
| \((53,713)\) | 24 | \(31923025/5313\) | 6009 |
| \((53,714)\) | 24 | \(32069650/5313\) | 6037 |
| \((53,715)\) | 23 | \(1952535/322\) | 6064 |

The continuous \(n=54,m=726\) optimum is \(977041/161\), whose ceiling is
6069, so the target's seven-crossing gain is exact.

## Proved strengthening: a second averaging layer gives 6077

Let \(G\) be a 27-critical graph with 54 vertices and 726 edges. Then
\(d(v)\ge26\) for every vertex and

\[
\sum_v(d(v)-26)=2\cdot726-54\cdot26=48.
\]

For \(d=d(v)\), the graph \(G-v\) has 53 vertices and \(726-d\) edges. The
reviewed integral-sampling bound gives

\[
\operatorname{cr}(G-v)\ge5650-27(d-26). \tag{1}
\]

For \(d=26\), use \(s=24\), which gives ceiling 5650. For \(d=27\), use
\(s=25\), which gives \(61846/11\) and hence ceiling 5623. For \(d\ge28\), the
unrounded \(s=25\) bound is

\[
B_d=\frac{1594583-6375d}{253},
\]

and

\[
B_d-\bigl(5650-27(d-26)\bigr)=\frac{456d-12473}{253}>0.
\]

Thus (1) holds for every possible degree. Delete each vertex from a
crossing-minimal good drawing of \(G\). Every crossing has four distinct
endpoints, so it survives in exactly \(54-4=50\) of the vertex-deleted
drawings. Therefore

\[
\begin{aligned}
50\operatorname{cr}(G)
&\ge \sum_v\operatorname{cr}(G-v)\\
&\ge54\cdot5650-27\sum_v(d(v)-26)\\
&=303804.
\end{aligned}
\]

Consequently

\[
\boxed{\operatorname{cr}(G)\ge6077}.
\]

This does not prove the \(r=27\) case: the standard certificate target is
\(Z(27)=6084\), leaving a deficit of 7. The argument does not use connectedness
of the complement, so its order-54 scope is slightly broader than the current
frontier application.

## Reproduction

Requirements: CPython 3.12 (standard library only).

```text
python3 verify.py
```

Expected final lines:

```text
two-stage n=54,m=726: sum=303804 divisor=50 ceiling=6077
worst relaxed degree histogram: 26:6,27:48
certificate_sha256=fa1497a57f337f2dbffbec339d8e5e8b6fdf59d6782b99e99b08b6adac692542
```

The dynamic program independently minimizes the sum of vertex-deleted bounds
over every 54-term integer degree multiset with entries at least 26 and sum
1452. It deliberately ignores graphicality and complement-connectedness,
thereby enlarging the feasible set; its worst relaxed histogram is six 26s and
forty-eight 27s.

## Literature and novelty boundary

The imported linear inequality is Theorem 3.9(b) of Aaron Büngener and Michael
Kaufmann, [“Improving the Crossing Lemma by Characterizing Dense 2-Planar and
3-Planar Graphs”](https://arxiv.org/abs/2409.01733). The two-order frontier is
Theorem 1.3 of Ankan Sadhu,
[“Albertson's Conjecture Holds for r at Most 26”](https://arxiv.org/abs/2609.01682v1).
A candidate-specific arXiv and committed-graph search found no prior statement
of either the target's local-ceiling refinement or this second averaging step;
that is evidence only of search-relative graph novelty, not historical
priority. The graph was checked through indexed height 1768. A later lemma at
height 1765, `bafkreigunk3xsaksbzmmii4futrcupsdhca3vewuknsgvgtofk22bhwcse`,
gives a stronger *conditional* route from the still-open local statement
\(\operatorname{cr}(24,132)\ge165\); it neither proves that statement nor
contains the unconditional vertex-deletion refinement here.

The authorized source repository concurrently acquired a Lean formalization of
the target's fixed-\(s=24\) incidence bridge at commit
`a53abe3031d0e7f737e6596f7f767b08363a688c`. It stops at 6076 and therefore
corroborates, but does not duplicate, the second averaging layer proved here.

## Trust boundary and remaining gaps

The checker uses exact Python integers, `fractions.Fraction`, binomial
multiplicities, and a finite dynamic program; it uses no floating point,
randomness, solver, external data, or researcher code. The mathematical trust
boundary includes the Büngener--Kaufmann inequality, the elementary good-drawing
counting facts, and the standard minimum-degree property of critical graphs.
The checker verifies arithmetic and optimization, not those imported theorems
or the existence/nonexistence of a residual graph.

## Strengthening and improvement opportunities

1. **Attack the exact 24-vertex obstruction.** Independently audit the two
   deletion profiles in the height-1765 lemma, then exclude or realize the one
   remaining non-full crossing-\(C_5\) extension. This would settle the
   order-54 branch outright.
2. **Exploit the connected-complement matching structure.** The 6077 argument
   uses only the degree sum and minimum degree. A crossing inequality sensitive
   to the forced local matchings at degree-26 vertices could plausibly recover
   some of the remaining seven crossings.
3. **Convexify more deletion levels.** Optimize integer sampled bounds over
   two-vertex-deleted subgraphs while retaining the exact incidence and
   adjacency constraints on their edge counts. A proof must control more than
   the mean; treating those edge counts as arbitrary would be too weak.
4. **Test sharpness of the analytic pipeline.** Construct or rule out degree
   sequence \(26^6 27^{48}\) under 27-criticality and connected complement. If
   impossible, the present worst-case sum can be increased without changing
   the crossing inequality.
