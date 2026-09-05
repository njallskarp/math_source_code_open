# Proof of the reanchoring cover and exact-partner bounds

## 1. Mapping the hard branch to intrinsic hypotheses

This section pins the inherited input; the subsequent cover needs only the
intrinsic hypotheses stated in the README.

In the hard-deficiency branch every red and blue color-neighborhood has
deficiency at least seven relative to its exact extremal value \(U(d)\).
The inherited values on orders \(18,\ldots,24\) are

\[
(U(18),\ldots,U(24))=(85,92,100,107,114,122,132).
\]

The reviewed degree/deficiency identity gives the weight function
\(w(18)=w(24)=21\), \(w(19)=w(23)=12\),
\(w(20)=w(22)=3\), \(w(21)=0\), with total weight \(W\leq39\).
All degrees lie in \(18,\ldots,24\). For a doubly exact anchor and
\(M=214\), the two side-deviation sums are \(-6,-7\).
Consequently

\[
39\geq W\geq3\sum_v|d(v)-21|
\geq3\left|\sum_v(d(v)-21)\right|=39.
\]

Equality forces all nonzero deviations negative, and the pointwise weight
inequality is strict at deviations of magnitude at least two. Hence there
are exactly 13 degree-20 vertices and 30 degree-21 vertices; the anchor's
red and blue sides contain respectively six and seven of the former.
This derivation uses no degree-profile enumeration.

The same deficiency identity gives total deficiency
\((1247-39)/2=604\), only two above the baseline \(86\cdot7=602\).
The red local-edge baseline is

\[
13(100-7)+30(107-7)=4209.
\]

The red excess is between zero and two. Subtracting it from 4209 gives
three times the number of red triangles, so the excess is divisible by
three and is zero. Thus all red deficiencies are exactly seven.

For any vertex of any red graph, count edges on the blue neighborhood,
using the sum of degrees over the red neighborhood, to obtain

\[
t_R(v)+t_B(v)=
\binom{42-d(v)}2-m+\sum_{w\in N_R(v)}d(w).
\]

Here \(m=445\) and the neighbor-degree sum is \(21d(v)-a(v)\).
For both possible degrees the right side is \(206-a(v)\). Therefore

\[
t_B(v)=
\begin{cases}
113-a(v)&v\in E,\\
106-a(v)&v\in C.
\end{cases}
\]

The blue hard-deficiency inequalities are exactly \(a(v)\geq6\).
In \(C\), equality is exactly the doubly exact condition. This establishes
the claimed branch identification using only the displayed inherited inputs.

Conversely, any Ramsey graph satisfying the intrinsic hypotheses has at
least 28 exact central anchors by the next section. At any such anchor,
the two 21-vertex neighborhoods contain respectively 100 red and 100 blue
edges. The blue side therefore contains 110 red edges, and the red cross
total is \(445-21-100-110=214\).

## 2. Intrinsic excess classification

Double-count incidences with \(E\):

\[
\sum_{v\in V}a(v)=\sum_{z\in E}d(z)=260=43\cdot6+2.
\]

Also \(\sum_{z\in E}a(z)=2e_R(E)\). Thus the excess in \(E\) is an even
integer between zero and two. Both excess units lie in the same intrinsic
class. They are either concentrated at one vertex (value eight) or split
between two (values seven). This gives precisely E8, E77, C8, C77.
It also shows that every other central vertex is doubly exact.

## 3. Reanchoring all four intrinsic types

In E8 the exceptional vertex has \(20-8=12\) red neighbors in \(C\);
choose any of them as anchor. All central vertices are exact.

In E77 each exceptional vertex has \(20-7=13\) red neighbors in \(C\).
Their union has size at most 26, leaving at least four central vertices
blue to both. Choose any of these exact anchors.

In C8 the exceptional vertex has \(21-8=13\) red neighbors among the
other 29 central vertices. The remaining 16 are exact and blue to it.

For C77 write \(T=\{p,q\}\) and \(X=C\setminus T\), so \(|X|=28\).
Let \(\epsilon\) indicate the red edge \(pq\), and put

\[
A=N_R(p)\cap X,\qquad B=N_R(q)\cap X,\qquad j=|A\cap B|.
\]

Both \(A,B\) have size \(14-\epsilon\). Thus

\[
|X\setminus(A\cup B)|=28-2(14-\epsilon)+j=2\epsilon+j.
\]

If this number is positive, choose an exact anchor blue to both.
If it is zero, nonnegativity forces \(\epsilon=j=0\).
The edge \(pq\) is blue and \(A,B\) are disjoint 14-sets partitioning
\(X\). Every exact central vertex is then red to exactly one of \(p,q\)
and blue to the other. Any of the 28 can be the anchor.

The first three types and these two alternatives are mutually exclusive
intrinsic conditions. Relabeling the chosen anchor and its red/blue cells,
then sorting within each cell by the equivariant key, yields exactly the
five rows in the README. No other vertex edges are fixed by this argument.

## 4. Incidence certificate completeness

For two ordered subsets of an \(L\)-vertex set with equal size \(w\), their
four incidence-bin sizes are

\[
(n_{00},n_{01},n_{10},n_{11})=(L-2w+j,w-j,w-j,j).
\]

Every allowable nonnegative tuple is realized by a partition into four
sets of those sizes. Two pairs have the same tuple if and only if a
permutation of the universe carries one to the other: choose a bijection
separately in each bin. The labeled multiplicity is

\[
\frac{L!}{n_{00}!n_{01}!n_{10}!n_{11}!},
\]

and the multiplicities sum to \(\binom Lw^2\).

Apply this with \((L,w)=(30,13)\) for E77, and \((28,14-\epsilon)\)
for C77. This gives 14, 15, 14 orbits respectively, exactly those in the
certificate. The generator and checker reach the same full table through
different enumerations. This checks the incidence projection completely;
it does not require any projection to lift to a Ramsey graph.

## 5. Finding a second doubly exact anchor

For a red edge \(uv\), its common red neighborhood contains no red triangle
(else with \(u,v\) it gives a red \(K_5\)) and no blue \(K_5\).
The classical \(R(3,5)=14\) therefore gives

\[
c(u,v)=|N_R(u)\cap N_R(v)|\leq13.
\]

For an exact central anchor \(u\), double-count the red edges in its
neighborhood to obtain

\[
\sum_{v\in N_R(u)}c(u,v)=2t_R(u)=200.
\]

There are six exceptional and 15 central red neighbors.
In the first four covering families, all 15 central red neighbors are
exact, by the anchor choices above. Their codegree sum is at least
\(200-6\cdot13=122\); one has codegree at least
\(\lceil122/15\rceil=9\).

In the partition family, exactly one central red neighbor is nonexact.
The remaining 14 exact ones have sum at least
\(200-7\cdot13=109\); one has codegree at least
\(\lceil109/14\rceil=8\).
If none of these 14 has codegree at least nine, then the anomalous central
red neighbor has codegree at least \(200-6\cdot13-14\cdot8=10\).
This last alternative is only a necessary condition, not an exclusion.

Thus every graph in the branch has a red-adjacent doubly exact pair of
codegree at least eight, and every nonpartition case admits one of
codegree at least nine with the stated first-anchor normalization.
