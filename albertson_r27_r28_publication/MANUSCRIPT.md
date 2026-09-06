# Albertson's conjecture for chromatic numbers 27 and 28

*Consolidated proof and publication audit, 6 September 2026.*

## Abstract

We give one account of the two previously reviewed proofs of
\[
\chi(G)\ge r\quad\Longrightarrow\quad
\operatorname{cr}(G)\ge\operatorname{cr}(K_r),
\qquad r\in\{27,28\}.
\]
A common order reduction leaves three critical-graph rows with connected
complements. Perfect matchings and a finite component classification force
two vertices to carry almost all degree excess. Gallai's theorem then
produces disjoint large clique blocks whose crossing numbers exceed the
target. The smallest terminal margin is six crossings. The new order
certificate uses refereed inputs and explicitly derives complement
connectivity; it avoids the recent Cranston and Sadhu frontier theorems.
The underlying terminal proofs have independent graph reviews. This
consolidation and its modified order bridge have not themselves received
independent review.

## 1. Statement, provenance, and conventions

All graphs are finite and simple. Crossing number is the ordinary
topological crossing number, with unrestricted curved edges, not rectilinear
crossing number. An \(r\)-critical graph has chromatic number \(r\) and all
proper subgraphs have chromatic number below \(r\). Write \(TK_r\) for a
subdivision of \(K_r\), and
\[
Z(r)=\frac14\left\lfloor\frac r2\right\rfloor
 \left\lfloor\frac{r-1}2\right\rfloor
 \left\lfloor\frac{r-2}2\right\rfloor
 \left\lfloor\frac{r-3}2\right\rfloor .
\]
Hill's drawing gives \(\operatorname{cr}(K_r)\le Z(r)\), with
\(Z(27)=6084\) and \(Z(28)=7098\). No equality with \(Z(r)\) is assumed.

**Theorem.** For each \(r\in\{27,28\}\), every graph \(G\) with
\(\chi(G)\ge r\) satisfies
\(\operatorname{cr}(G)\ge\operatorname{cr}(K_r)\).

The terminal arguments were contributed at Discovery Net heights 2659
and 2711, and independently reviewed at 2679 and 2725. The finite
\(r=28\) component interface has its own review at 2699. This note
consolidates those results, the simplifications at 2677/2683/2871/2903,
and the subsequent corrections to the matching and sampling interfaces.
The accompanying [publication audit](PUBLICATION_AUDIT.md) records exact
artifact references, contributor distinctions, and source pins. Neither
the \(r=27\) theorem nor an Albertson theorem for any smaller chromatic
number is a premise of the \(r=28\) proof.

It suffices to exclude an \(r\)-critical counterexample \(G\).
Indeed, a subgraph minimal with chromatic number at least \(r\) has
chromatic number exactly \(r\): after deleting any vertex it is
\((r-1)\)-colorable, and adding that vertex uses at most one extra color.
Such a counterexample has
\[
\operatorname{cr}(G)<\operatorname{cr}(K_r)\le Z(r)
\tag{1}
\]
and contains no \(TK_r\). Smoothing the subdivided paths shows
\(\operatorname{cr}(TK_r)=\operatorname{cr}(K_r)\); crossing number is
monotone under taking subgraphs. We do not need to minimize the order
among counterexamples.

## 2. Exact external inputs

Here are the imported statements, with the hypotheses used. Proofs of
these published theorems are outside the finite certificate.

**Critical graphs.** Barát--Tóth [BT], Corollaries 5, 7 and 11, give:

- An \(r\)-critical graph of order at most \(r+4\) contains \(TK_r\).
- For \(r\ge4\), an \(r\)-critical graph without \(TK_r\) has
  \(2m\ge(r-1)n+2r-6\).
- If also \(n=r+p\), \(2\le p\le r-1\), then
  \(2m\ge(r-1)n+p(r-p)-1\).

Their Lemma 3, with the hypothesis \(r\ge17\) used in its proof,
excludes counterexamples of order \(n\ge3.57r\). Both values of \(r\)
here satisfy that hypothesis. The critical-degree bound
\(\delta(G)\ge r-1\) follows directly by extending a coloring of \(G-v\).

**Crossing inequalities.** Büngener--Kaufmann [BK], journal Theorem 4(b),
states, for simple graphs with \(n>2\),
\[
\operatorname{cr}(G)\ge5m-\frac{203}{9}(n-2).
\tag{2}
\]
There is no density condition. Theorem 6(b) is the numbering in the
arXiv version; the journal version was published on 5 August 2026 in an
issue labeled 2025. The weaker conference constant \(407/18\) is not
substituted for \(203/9\).

For the recursively rounded table we also use Euler's bound and the
Pach--Radoičić--Tardos--Tóth bounds, in the forms recorded as (1)--(3)
in [BT]:
\[
\operatorname{cr}(G)\ge
\max\left\{0,\ m-3(n-2),\
\frac73m-\frac{25}{3}(n-2),\
4m-\frac{103}{6}(n-2),\
5m-\frac{203}{9}(n-2)\right\}.
\tag{3}
\]
Only integer ceilings of these inequalities enter the code.

**Coloring and low vertices.** Gallai's connected-complement order
bound says that an \(r\)-critical graph with connected complement has
at least \(2r-1\) vertices; see [BT], Section 2. Stehlík [S] strengthens
this: for each vertex \(v\), an \(r\)-critical graph with connected
complement admits an \((r-1)\)-coloring of \(G-v\) whose color classes
all have size at least two. Gallai's low-vertex theorem says that the
subgraph induced by the vertices of degree \(r-1\) has only complete
graphs and odd cycles as blocks; a modern primary statement is [ST],
Theorem 4(a).

**Matching and small crossings.** We use Tutte's perfect-matching
criterion: a finite graph has a perfect matching exactly when
\(o(J-S)\le |S|\) for every vertex subset \(S\), where \(o\) counts
odd components [T]. The complete-graph seed values through order 12 are
\[
c(0),\ldots,c(12)=0,0,0,0,0,1,3,9,18,36,60,100,150.
\]
The last two are due to Pan--Richter [PR]; the earlier values are the
classical small complete-graph values recalled there. Kleitman's
formula [K] gives
\[
\operatorname{cr}(K_{6,t})
=6\left\lfloor\frac t2\right\rfloor
 \left\lfloor\frac{t-1}2\right\rfloor.
\tag{4}
\]
No claimed exact value for \(K_{13}\) or \(K_{14}\) is used.

These are ordinary imported mathematical theorems, not assumptions about
generated data. This audit verifies the statements and their application,
not new proofs of those external results. Access limitations for [S]
and [K] are explicit in the publication audit.

## 3. Sampling and complete finite order coverage

Fix a crossing-minimal good drawing, in which crossing edges have four
distinct endpoints. Each edge is present in \(\binom{n-2}{k-2}\)
induced \(k\)-vertex subdrawings and each crossing in
\(\binom{n-4}{k-4}\). Averaging (2), for \(4\le k\le n\), gives
\[
A(n,m,k)=
\frac{5m(n-2)(n-3)}{(k-2)(k-3)}
-\frac{203n(n-1)(n-2)(n-3)}{9k(k-1)(k-3)}
\le\operatorname{cr}(G).
\tag{5}
\]
This is the standard induced-sampling argument, also given in Sadhu
[Sa], Lemma 2.2.

Let \(L(n,m)\) start from the ceiling of (3). For increasing \(n\),
take the maximum with
\[
\left\lceil
\frac{(n)_4}{(k)_4}
\,\widehat L_k\left(\frac{m k(k-1)}{n(n-1)}\right)
\right\rceil,\qquad 4\le k<n,
\tag{6}
\]
where \((n)_4=n(n-1)(n-2)(n-3)\) and \(\widehat L_k\) is the
greatest convex minorant of the integer row \(L(k,\cdot)\).
Every update is a valid lower bound: apply the row bound to each induced
subgraph, minorize by \(\widehat L_k\), and use Jensen's inequality on
the exact average edge count. Induction on \(n\) proves validity of the
whole table. Repeated sweeps are harmless; a terminal unchanged sweep
checks implementation stability. All arithmetic is rational or integral.

We need only a lower bound. We do not assert that the Jensen value is
attained by an integer population of subgraphs, or by any actual graph.
That stronger assertion in height 2713 was refuted at height 3240;
the proof of (6) is unaffected.

Define the integer edge floor
\[
F_r(n)=\left\lceil\frac12
\max\{(r-1)n+2r-6,\ (r-1)n+(n-r)(2r-n)-1\}\right\rceil,
\tag{7}
\]
omitting the second entry unless \(r+2\le n\le2r-1\).

By [BT], a counterexample has \(r+5\le n<357r/100\).
The [order certificate](ORDER_CERTIFICATE.tsv) lists every integer in
those intervals: 65 orders for \(r=27\) and 67 for \(r=28\).
It evaluates (5) at \(m=F_r(n)\), keeping a maximizing integer \(k\).
Every row except \(52,53,54\) for \(r=27\), and \(54,55,56\) for \(r=28\),
has \(\lceil A\rceil\ge Z(r)\). Monotonicity in \(m\) excludes all
larger edge totals at those orders as well.

The recursive table then gives:

| \(r\) | \(n\) | Edge floor \(F_r(n)\) | Last \(m\) with \(L(n,m)<Z(r)\) | \(L\) at the next \(m\) |
| --- | --- | --- | --- | --- |
| 27 | 52 | 701 | 702 | 6095 |
| 27 | 53 | 713 | 713 | 6100 |
| 27 | 54 | 726 | 724 | 6106 |
| 28 | 54 | 755 | 757 | 7100 |
| 28 | 55 | 768 | 769 | 7123 |
| 28 | 56 | 781 | 780 | 7115 |

In particular, orders 54 and 56 respectively are impossible.
The table is checked across its complete integer edge domains, not
inferred from a few probes. No Cranston order band, Sadhu frontier
theorem, Kostochka--Yancey edge theorem, or earlier Albertson case is
a premise of this dispatch.

## 4. Connected complements: the marked join interface

If \(H=\overline G\) is disconnected, let \(V_i\) be its component
vertex sets and write \(n_i=|V_i|\), \(r_i=\chi(G[V_i])\).
Then \(G\) is the join of the critical graphs \(G[V_i]\) and
\(\sum r_i=r\). Criticality of each part follows by replacing it with
a proper subgraph in the join. Its complement is connected, so Gallai's
order bound gives \(n_i\ge2r_i-1\). A part is either
\((r_i,n_i)=(1,1)\), or \(r_i\ge3\); \(r_i=2\) would give \(K_2\),
whose complement is disconnected.

At least one part has no \(TK_{r_i}\). Otherwise choose subdivisions
inside every part and join their branch vertices with the actual
cross-part edges. The paths inside different parts have disjoint
internal vertices, and cross-part edges introduce none, giving \(TK_r\).
A marked part must have \(r_i\ge4\), since a 3-critical graph is an
odd cycle, hence a subdivision of \(K_3\).

Give every unmarked part only the elementary edge floor
\(\lceil(r_i-1)n_i/2\rceil\). Give one marked part the [BT]
Corollary 7 floor \(\lceil((r_i-1)n_i+2r_i-6)/2\rceil\).
Then
\[
2m\ge n^2+\sum_i(2 f_i-n_i^2).
\tag{8}
\]
Exactly one marked part suffices; assigning the stronger bound to every
part would be unjustified.

The finite dynamic program in reproduce.py minimizes (8) over all
allowed ordered part sequences with at least two parts. Its state
records the chromatic and order sums, whether a part is marked, and
the part count capped at two. Each transition appends one allowed
part. Since its chromatic number is positive, induction on the
chromatic sum proves completeness. Keeping only the cheapest state
is valid because all later costs depend only on the recorded sums
and mark. Allowing ordered sequences adds duplicates, not omissions.

| \(r,n\) | Sampling ceiling | Necessary edges if \(H\) disconnected | A minimizing relaxed partition |
| --- | --- | --- | --- |
| \(27,52\) | 702 | 712 | \((1,1)+(26,51)^*\) |
| \(27,53\) | 713 | 725 | \((1,1)+(26,52)^*\) |
| \(28,54\) | 757 | 766 | \((1,1)+(27,53)^*\) |
| \(28,55\) | 769 | 780 | \((1,1)+(27,54)^*\) |

A star denotes the single marked part; a relaxed partition is not
claimed realizable. Orders \(2r-2\) have disconnected complement by
Gallai and are excluded. At order \(2r-1\) the same calculation
**forces connected complement**, including the \(r=28,n=55\) case.
This establishes the exact common frontier
\[
(r,n,m)=(27,53,713),\quad(28,55,768),\quad(28,55,769),
\qquad H\text{ connected}.
\tag{9}
\]

## 5. The matching and component interface

Put \(n=2r-1\), \(\Delta(H)\le r-1\), and
\[
x_v=d_G(v)-(r-1)=r-1-d_H(v)\ge0,\qquad
X=\sum_vx_v=2m-n(r-1).
\tag{10}
\]
At the three rows, \(X=48,51,53\), respectively.

Stehlík's deletion coloring has exactly \(2r-2\) vertices and \(r-1\)
classes, each of size at least two. Each class therefore has size two
and is an edge of \(H\). Thus \(H-v\) has a perfect matching for every
\(v\): \(H\) is factor-critical. A triangle \(T\) of \(H\) cannot have
a perfect matching outside it, since the triangle and the
\((n-3)/2\) matching edges would color \(G\) with \(r-1\) colors.

If \(H\) is triangle-free, choose a vertex of maximum degree.
Because \(X<n\), some \(x_v=0\), so that degree is \(r-1\).
Its \(H\)-neighborhood is a clique of order \(r-1\) in \(G\).
Put \(q=r-1\). Its independence in \(H\) means that its incident
\(H\)-edges number at least \(q(r-1)-X\). Hence the residual
\(n-q\) vertices induce at least
\(\binom{n-q}{2}-[e(H)-q(r-1)+X]\) edges in \(G\).
Adding crossing lower bounds on the two disjoint induced subgraphs gives 7088,
8268 and 8238 at the respective rows, all above \(Z(r)\).
The code records the residual edge counts and reproduces this
reviewed calculation.

Otherwise take a triangle \(T\). Tutte's theorem applied to the
even-order graph \(H-T\), which has no perfect matching, produces
\(B\supseteq T\) with \(o(H-B)\ge |B|-1\). Indeed its strict
Tutte violation has even positive gap, hence at least two.
Writing \(b=|B|\) and the component orders as \(c_1,\ldots,c_t\), we have
\[
3\le b\le r,\quad
\sum_i c_i=n-b,\quad
\#\{i:c_i\text{ odd}\}\ge b-1,\quad
\sum_i c_i\max(0,r-b-c_i)\le X.
\tag{11}
\]
The last inequality is degree deficiency: a vertex in a component of
order \(c\) has at most \(c-1+b\) neighbors in \(H\).

In fact equality \(o(H-B)=b-1\) follows: choose \(a\in B\) and
apply the necessary part of Tutte to the perfect matching of \(H-a\),
deleting the other \(b-1\) vertices of \(B\). The earlier withdrawal
of this equality at height 2569 was itself corrected at 2815.
We keep the weaker condition (11), as the reviewed enumeration did;
it is a safe superset.

The complete component certificate has 34 candidate multisets for
the first row, and 37 at each of the other rows, after (11).
Every candidate and its numerical filter values appear in
[COMPONENT_CERTIFICATE.tsv](COMPONENT_CERTIFICATE.tsv).
The common surviving list is
\[
\begin{array}{c|c}
 b&\text{component orders}\\ \hline
3&(2r-5,1),\ (2r-6,1,1)\\
4&(2r-7,1,1).
\end{array}
\tag{12}
\]
Section 8 specifies all further filters and their soundness.
The \(r=28\) table matches the independent review entry by entry;
the \(r=27\) table is also regenerated by the same checker with its
parameters changed, using only the weaker single-level sampling
bound. This latter replay agrees with the separate \(r=27\) review.

## 6. Two singletons force small high-vertex sets

For any vertex \(w\) of a factor-critical graph without conformal
triangles, no vertex \(a\in N_H(w)\) can dominate the rest of that
neighborhood. A perfect matching of \(H-a\) matches \(w\) to some
neighbor \(u\ne a\). If \(au\) were an edge, deleting the matching
edge \(wu\) would exhibit a conformal triangle \(awu\).

Also \(\delta(H)\ge2\) at these orders. An isolated vertex obstructs
a perfect matching after another vertex is deleted. If \(w\) has
only neighbor \(a\), then \(H-a\) has an isolated vertex. Thus
singletons in (12) cannot have all their neighbors in the clique
\(B=T\); this eliminates both \(b=3\) forms.

For \(b=4\), write \(B=T\cup\{s\}\), and let the singleton
components be \(w_1,w_2\), with large component \(C\) of order \(2r-7\).
Their neighborhoods have the form
\[
N_H(w_i)=\{s\}\cup A_i,\qquad
\varnothing\ne A_i\subseteq T,\qquad
E_H(s,A_1\cup A_2)=\varnothing.
\tag{13}
\]
If \(\alpha\in A_1\cap A_2\), a perfect matching of \(H-\alpha\)
cannot match either \(w_i\) to a different vertex of \(A_i\):
that would create a conformal triangle. It would have to match
both singletons to \(s\), impossible. Hence \(A_1,A_2\) are disjoint
and
\[
d_H(w_1)+d_H(w_2)=2+|A_1|+|A_2|\le5,\qquad
x_{w_1}+x_{w_2}\ge2r-7.
\tag{14}
\]

Let \(R=\{v:x_v>0\}\), \(h=|R|\), and \(L=G[V(G)\setminus R]\).
The singletons belong to \(R\), and each other high vertex consumes
at least one excess unit. Therefore
\[
2\le h\le2+X-(2r-7),
\]
namely \(h\le3,4,6\) for the three rows.
The exact low-edge identity is
\[
e(L)=m-\sum_{v\in R}d_G(v)+e(G[R])
=n(r-1)-m-(r-1)h+e(G[R]).
\tag{15}
\]
The edge \(w_1w_2\) is present in \(G\), so \(e(G[R])\ge1\).

For the tight cases \((r,m,h)=(28,768,4),(28,769,6)\),
all available excess outside the singletons is used, making equality
hold in (14). Thus \(A_1,A_2\) partition \(T\).
Among the other \(h-2\) high vertices, let \(\sigma\in\{0,1\}\)
indicate whether \(s\) is high, let \(\tau\le3\) count high vertices
in \(T\), and put \(z=h-2-\sigma-\tau\ge0\).
Each high vertex in \(C\) gives two edges to the singletons; each
in \(T\) gives one; and \(s\) is \(G\)-adjacent to all of \(T\).
Counting these distinct edges gives
\[
e(G[R])\ge1+2z+\tau+\sigma\tau.
\tag{16}
\]
Minimizing this small expression gives 3 and 6 in the two tight cases.
All other rows below use only the weaker bound 1.

## 7. A common terminal Gallai contradiction

Gallai's theorem makes every block of \(L\) a clique or odd cycle.
For each block let \(u=|V(Q)|-1\).
If \(L\) has \(c\) components, including isolated vertices, then
\[
\sum_Q u=|V(L)|-c,\qquad e(L)=\sum_Qe(Q).
\tag{17}
\]
These follow by successively removing leaf blocks, which share one
cut vertex with the rest. Isolated components contribute no block.

Two clique blocks of order at least 15 cannot share a vertex:
that vertex would have at least \(14+14=28\) neighbors in \(L\),
more than its full degree \(r-1\le27\).
They are therefore vertex-disjoint. In any drawing, the crossings
internal to their induced subgraphs are distinct, and consequently
\[
\operatorname{cr}(G)\ge
\sum_{\substack{Q\text{ clique block}\\|Q|\ge15}}c(|Q|),
\qquad
c(q)=\left\lceil\frac{q\,c(q-1)}{q-4}\right\rceil\quad(q\ge13).
\tag{18}
\]
The complete-graph recurrence counts vertex-deleted subdrawings and
starts only with the exact values through \(K_{12}\).

A finite state calculation minimizes the right side over all block
multisets satisfying (17) and the edge floor from (15)--(16).
For every increment \(u\ge1\), a clique contributes
\((u,\binom{u+1}{2},c(u+1))\), with the last coordinate set to zero
when \(u+1<15\). For even \(u\ge4\), an odd cycle contributes
\((u,u+1,0)\). Include all totals \(\sum u<|V(L)|\), thus all
component counts. The dynamic program keeps, for each total increment
and edge sum, the smallest crossing cost. Positive increments give
an elementary induction proving that every finite multiset is represented.
There is no cap or uniqueness assumption on clique-block orders.

| \(r\) | \(m\) | \(h\) | Forced \(e(L)\) | Minimum split bound | Margin above \(Z(r)\) |
| --- | --- | --- | --- | --- | --- |
| 27 | 713 | 2 | 614 | 8424 | 2340 |
| 27 | 713 | 3 | 588 | 7722 | 1638 |
| 28 | 768 | 2 | 664 | 9920 | 2822 |
| 28 | 768 | 3 | 637 | 9126 | 2028 |
| 28 | 768 | 4 | 612 | 8424 | 1326 |
| 28 | 769 | 2 | 663 | 9920 | 2822 |
| 28 | 769 | 3 | 636 | 9126 | 2028 |
| 28 | 769 | 4 | 609 | 8424 | 1326 |
| 28 | 769 | 5 | 582 | 7589 | 491 |
| 28 | 769 | 6 | 560 | 7104 | 6 |

Every case contradicts (1), proving the theorem.
The minimizers printed by the checker are witnesses for the numerical
relaxation; they need not be realizable low-vertex graphs.

## 8. Soundness of the component certificate

Here are the filters behind (12), so the finite table is not an opaque
classification assumption. Put \(D=V(H)\setminus B\), \(d=|D|\),
\(E_H=\binom n2-m\), and
\[
P_{\min}=\sum_i(c_i-1),\qquad
P_{\max}=\sum_i\binom{c_i}{2},\qquad
Y_{\min}=\sum_i c_i\max(0,r-b-c_i).
\]
Connectedness of each component gives \(P_{\min}\le e_H(D)\le P_{\max}\).

First, actual cross edges in \(G\) obey
\[
\max\{b\max(0,r-b),d\max(0,r-d)\}
\le e_G(B,D)
\le d(b-r+1)+X+2P_{\max}.
\tag{19}
\]
The lower bound counts required degree across the cut from each side.
For the upper bound sum \(d_H(v)=r-1-x_v\) over \(D\), and use
\(e_H(D)\le P_{\max}\) and \(\sum_{D}x_v\le X\).
Incompatible endpoints exclude a row.

Second, any grouping of whole components with total size \(a\) gives
a \(K_{a,d-a}\) subgraph of \(G\). Counting its six-vertex selections
and using (4) gives the conservative bound
\[
b_6(a,t)=
\left\lfloor\frac{a(a-1)}{30}
\,6\left\lfloor\frac t2\right\rfloor
 \left\lfloor\frac{t-1}2\right\rfloor\right\rfloor
\quad(a\ge6),
\tag{20}
\]
with both orientations allowed. The complete subset-sum set of the
component orders enumerates every grouping. Floors are conservative.

Third, \(t\ge r\) components give a \(K_r\) by taking one vertex per
component. In the special form \(t=r-1\) with component orders
\(2,1,\ldots,1\), the multipartite graph on \(D\) is \(K_r\) with one
possible missing edge. If the degree count forces
\[
e(G[B])\ge
\left\lceil\frac{b(r-1)-U}{2}\right\rceil
>\binom{b-1}{2},
\tag{21}
\]
where \(U\) is the cross-edge upper bound in (19), then \(G[B]\)
is connected. Each endpoint of the missing pair has a neighbor in
\(B\), since it has at most \(r-2\) neighbors in \(D\).
A path through \(B\) completes a \(TK_r\) with branch vertices \(D\).

Finally enumerate every integer
\[
Y_{\min}\le y\le X,\qquad 3\le q_B\le\binom b2,
\quad
p_D=d(r-1)-y-E_H+q_B\in[P_{\min},P_{\max}].
\tag{22}
\]
Here actual values are \(y=\sum_Dx_v\), \(q_B=e(H[B])\), and
\(p_D=e(H[D])\). The lower bound \(q_B\ge3\) retains the triangle.
Complement counting yields (22) exactly. The disjoint induced graphs
on \(B,D\) force the split bound
\[
\max\{c(t),\,A_*(d,\binom d2-p_D),\,\text{bound (20)}\}
+A_*(b,\binom b2-q_B),
\tag{23}
\]
where \(A_*(v,e)=\lfloor\max(0,\max_{4\le k\le v}A(v,e,k))\rfloor\)
and is zero for \(v<4\). An empty interval in (22), or a minimum
over it above \(Z(r)\), excludes that multiset. This deliberately
uses a weaker bound than the recursive table in Section 3.

Every actual graph satisfies these filters. Conversely no realization
of a surviving multiset is claimed. Exhaustion follows by generating
each positive integer partition of \(n-b\) by ascending multiplicities,
retaining (11), and evaluating the displayed finite intervals.
The two small TSV certificates expose the entire output relevant to
the proof.

## 9. Reproduction and remaining trust

From the repository root:

~~~sh
cd albertson_r27_r28_publication
PYTHONDONTWRITEBYTECODE=1 python3 reproduce.py > actual.txt
diff -u EXPECTED_OUTPUT.txt actual.txt
shasum -a 256 -c SHA256SUMS
~~~

The program checks the hashes of three previously reviewed source
modules, reconstructs the recursive table, verifies both complete
certificates byte for byte, and reproduces the join and terminal tables.
CPython 3.12.12 and the standard library suffice. The output ends with
a deterministic result digest and VERIFIED. The temporary actual.txt
is not source and should not be committed.

This is reproducible composition using reviewed code, not a new
independent implementation of every enumeration. There is no solver,
floating-point decision, random sampling, homology computation, or
hidden download. Neither crossing-number topology nor the external
theorems are established by executing Python.

Related Lean projects formalize deletion-coloring-to-matching,
clique-matching coloring, and the tight Tutte witness, or alternative
Gallai block-spectrum consequences. They do not provide an end-to-end
formal proof of this manuscript. Their exact scope, replay status,
and the remaining human bridges are in the publication audit.

## References

[BT] J. Barát and G. Tóth, *Towards the Albertson conjecture*,
Electronic Journal of Combinatorics 17 (2010), R73.
[Journal PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v17i1r73/pdf).

[BK] A. Büngener and M. Kaufmann, *Improving the Crossing Lemma by
Characterizing Dense 2-Planar and 3-Planar Graphs*, JGAA 29(3),
143--174; journal publication 2026, issue labeled 2025.
[Journal article](https://jgaa.info/index.php/jgaa/article/view/3000),
[Theorem 4, journal PDF](https://jgaa.info/index.php/jgaa/article/download/3000/3042/3937).

[S] M. Stehlík, *Critical graphs with connected complements*,
Journal of Combinatorial Theory B 89 (2003), 189--194.
[Publisher statement](https://www.sciencedirect.com/science/article/pii/S0095895603000698).

[ST] M. Stiebitz and B. Toft,
*A Brooks type theorem for the maximum local edge connectivity*,
Electronic Journal of Combinatorics 25(1) (2018), P1.50.
[Theorem 4](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v25i1p50/pdf/).

[T] W. T. Tutte, *The factorization of linear graphs*,
Journal of the London Mathematical Society 22 (1947), 107--111.
[DOI](https://doi.org/10.1112/jlms/s1-22.2.107).

[PR] S. Pan and R. B. Richter, *The crossing number of \(K_{11}\) is 100*,
Journal of Graph Theory 56 (2007), 128--134.
[Publisher statement](https://doi.org/10.1002/jgt.20249).

[K] D. J. Kleitman, *The crossing number of \(K_{5,n}\)*,
Journal of Combinatorial Theory 9 (1970), 315--323.
[DOI](https://doi.org/10.1016/S0021-9800(70)80087-4).
The exact formula is also stated in N. H. Nahas, *On the crossing number
of \(K_{m,n}\)*, EJC 10 (2003), N8,
[Theorem 3](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v10i1n8/pdf).

[Sa] A. Sadhu, *Albertson's Conjecture Holds for \(r\) at Most 26*,
arXiv:2609.01682v1 (2026).
[Preprint](https://arxiv.org/html/2609.01682v1).
Cited for context and the antecedent sampling exposition, not as an
unproved premise of the order bridge above.
