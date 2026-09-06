# Global missed-pair column hulls

## Setting

Let \(uv\) be the red anchor of a selected height-3148 root, let

\[
H=N_R(u)\cap N_R(v),\qquad |H|=c\in\{9,10,11,12,13\},
\]

and let \(X=V\setminus(\{u,v\}\cup H)\), so \(n=|X|=41-c\). For \(h\in H\),
write

\[
a_h=|N_R(h)\cap H|,
\]

and let \(d_h\in\{20,21\}\) be its prescribed total red degree. For every
pair \(P=\{z,z'\}\in\binom X2\), the height-3274 lift defines

\[
m_{P,h}=(1-x_{zh})(1-x_{z'h}).
\]

Put \(M_h=\sum_{P\in\binom X2}m_{P,h}\).

## The core-degree interval

The red graph on \(H\) is triangle-free, while its independence number is at
most four. The red neighbors of \(h\) inside \(H\) are independent, so

\[
a_h\leq4.
\]

The \(c-1-a_h\) blue neighbors of \(h\) inside \(H\) contain neither a red
triangle nor a blue \(K_4\): the latter together with \(h\) would be a blue
\(K_5\). The equality \(R(3,4)=9\) therefore gives

\[
c-1-a_h\leq8,
\]

and hence

\[
c-9\leq a_h\leq4. \tag{1}
\]

Because \(h\) is red to both anchors, its number \(b_h\) of blue neighbors in
\(X\) is fixed by its core degree:

\[
b_h=n-(d_h-2-a_h)=n-d_h+2+a_h. \tag{2}
\]

Thus \((1)\) and \((2)\) give

\[
\begin{array}{c|c}
d_h&\text{possible }b_h\\ \hline
20&14,15,\ldots,27-c\\
21&13,14,\ldots,26-c.
\end{array} \tag{3}
\]

## Exact column projection

Double counting unordered pairs of blue exterior neighbors gives the exact
Boolean identity

\[
M_h=\binom{b_h}{2}. \tag{4}
\]

Let \(L\leq b\leq U\) be either interval in \((3)\), and set
\(F=\binom b2\). The convex hull of the integer points

\[
\{(b,F):b=L,L+1,\ldots,U\}
\]

has lower facets

\[
F\geq tb-\binom{t+1}{2},\qquad t=L,L+1,\ldots,U-1, \tag{5}
\]

and upper facet

\[
2F\leq(L+U-1)b-LU. \tag{6}
\]

Indeed, \((5)\) is the line through the consecutive points at \(t,t+1\), and
the right side of \((6)\) is the line through the endpoint points. Convexity of
\(b\mapsto\binom b2\) proves validity, and these lines are exactly the two
boundaries of the polygon. When \(L=U\), one lower supporting line and \((6)\)
reduce to equality at the single point.

Substituting \((2)\) into \((5)\)--\((6)\) gives a complete two-dimensional hull in the
variables \(a_h,M_h\). This is the global column mechanism: every row couples
all \(\binom n2\) missed-pair variables for one core vertex.

## Guarded OPB rows

Write \(s=n-d_h+2\), so \(b_h=s+a_h\), and let \(y_r\) select the root.
For each lower slope \(t\), put

\[
B_t=ts-\binom{t+1}{2},\qquad G_t=B_t+t(c-1).
\]

The emitted guarded row is

\[
M_h-ta_h-G_ty_r\geq-t(c-1). \tag{7}
\]

For the upper chord, put

\[
q=L+U-1,\qquad B=LU-qs,
\]

and \(T=\binom n2\). The emitted row is

\[
-2M_h+qa_h-(B+2T)y_r\geq-2T. \tag{8}
\]

When \(y_r=1\), \((7)\)--\((8)\) are exactly \((5)\)--\((6)\). When \(y_r=0\), \((7)\) follows
from \(M_h\geq0\) and \(a_h\leq c-1\), while \((8)\) follows from
\(M_h\leq T\) and \(a_h\geq0\). Thus the guards are valid even over the
continuous box relaxation.

Across all 389 roots, the construction adds 13,078 rows and no variables.
The numbers of rows attached to a root of core order \(9,10,11,12,13\) are,
respectively,

\[
45,40,33,24,26.
\]

Every Boolean model of the height-3274 formulation satisfies \((4)\) and hence
all new rows. Deleting the rows recovers the prior formula unchanged, so the
strengthening is equisatisfiable with the complete \(M=214\) formulation.

## Strict full-LP separation certificate

The certificate selects root 48, with key

\[
(\mathtt{E8},13,0,\mathtt A).
\]

Its 13-vertex core is the cyclic red graph on \(\mathbb Z/13\mathbb Z\) with
differences \(\{1,5,8,12\}\). Each core vertex is central and has
\(a_h=4\). Every core-to-exceptional-exterior edge has value \(6/13\), and
every core-to-central-exterior edge has value \(3/5\). The remaining
exterior edges are the 20 rational orbit parameters in
`edge_parameters.tsv`.

The 171 rows of `triangle_orbits.tsv` assign one red-triangle value to each
class determined by the three vertex types and the sorted multiset of its
three edge values. Direct exact verification establishes:

- all 903 edge variables lie in \([0,1]\);
- all 962,598 five-set sums lie in \([1,9]\), with both endpoints attained;
- all 12,341 triangle variables satisfy their four conjunction rows;
- all 43 degree, red local-triangle, and exceptional-incidence equations hold;
- all 69,732 selector rows, 11,672 unary footprint rows, 74,958 projected
  pair rows, and 508,986 height-3274 local pair-cell rows hold.

Define every lifted missed variable at its McCormick lower bound,

\[
m_{P,h}=\max(0,1-x_{zh}-x_{z'h}),
\]

and every lifted red-inside variable by

\[
q_{P,ij}=\max(0,m_{P,i}+m_{P,j}+x_{ij}-2).
\]

These choices satisfy every defining row. In the active root, \(m_{P,h}\)
is \(1/13\) when both members of \(P\) are exceptional and is zero otherwise.
Consequently

\[
M_h=\binom{13}{2}\frac1{13}=6
\]

for each of the 13 core columns. The lower hull row of slope 13 instead
requires

\[
M_h\geq13\cdot13-\binom{14}{2}=78.
\]

Thus exactly 13 new rows are violated, each by 72. This proves that the
column hull strictly strengthens the LP relaxation of the entire height-3274
formula, rather than only a selected local subsystem.

The rational point is not a colored graph and gives no SAT/UNSAT conclusion.
Its role is solely to certify strict relaxation separation.
