# Sharp all-codegree common-core footprint bound

## Statement

Let \(G\) be a red/blue coloring of \(K_{43}\) with no monochromatic
\(K_5\). Let \(uv\) be red, and put

\[
H=N_R(u)\cap N_R(v),\qquad |H|=c.
\]

For every \(z\notin H\cup\{u,v\}\), define its red footprint on the common
core by

\[
S_z=N_R(z)\cap H.
\]

Then \(S_z\) meets every red-independent four-set of \(H\). Consequently,
when \(9\leq c\leq13\),

\[
|S_z|\geq c-8.
\]

The bound is sharp for every \(c\in\{9,10,11,12,13\}\) under exactly the
local requirements that the red graph on \(H\) be triangle-free and have
independence number at most four.

## Proof of the universal bound

The red graph induced by \(H\) contains no red triangle, since such a
triangle together with \(u,v\) would form a red \(K_5\). It has no
red-independent five-set, since that would be a blue \(K_5\).

Suppose that a red-independent four-set \(Q\subseteq H\) misses \(S_z\).
All four edges from \(z\) to \(Q\) are then blue, while all six edges inside
\(Q\) are blue. Thus \(Q\cup\{z\}\) is a blue \(K_5\), a contradiction.
Therefore \(S_z\) meets every such \(Q\).

If \(|S_z|\leq c-9\), then \(H\setminus S_z\) has at least nine vertices and
its red graph remains triangle-free. The classical equality \(R(3,4)=9\)
forces a red-independent four-set in \(H\setminus S_z\), contradicting the
previous paragraph. Hence \(|S_z|\geq c-8\).

## One nested sharpness family

On \(\mathbb Z/13\mathbb Z\), color \(ij\) red exactly when

\[
i-j\in\{1,5,8,12\}\pmod {13}.
\]

This graph has no red triangle and independence number four. Let

\[
T=\{0,1,2,3,4,5,8,9\},
\]

which has independence number three, and order the remaining vertices as

\[
(6,7,10,11,12).
\]

For \(c=9,\ldots,13\), let \(S_c\) be the first \(c-8\) vertices of this
list and let \(H_c=T\cup S_c\). The induced graph on \(H_c\) is
triangle-free and has independence number four. Because
\(H_c\setminus S_c=T\) has independence number three, \(S_c\) meets every
independent four-set of \(H_c\). Thus \(|S_c|=c-8\), proving sharpness from
the local core conditions alone. This is not a claim that these marked cores
extend to a 43-vertex Ramsey coloring.

The Python and independent C++ implementations exhaust all subsets of the
thirteen-vertex graph. For \(c=9,\ldots,13\), the numbers of independent
four-sets in \(H_c\) are respectively \(4,7,15,27,39\). Deleting any one
vertex from \(S_c\) exposes a missed independent four-set.

## Selector-guarded formulation

In a height-3160 root \(r\), the labels of \(H_r\) and its size \(c_r\) are
fixed whenever selector \(y_r=1\). Therefore, for each of the
\(41-c_r\) exterior vertices \(z\), add

\[
\sum_{h\in H_r}x_{zh}-(c_r-8)y_r\geq0.
\]

When \(y_r=0\), the row is tautological over Boolean edge variables. When
\(y_r=1\), it is precisely the proved footprint bound. Hence all added rows
are logical consequences of the active root and the monochromatic-\(K_5\)
constraints. Every original model satisfies them, and every strengthened
model is plainly an original model; satisfiability is unchanged.

There are 78 roots at each of \(c=9,10,11,12\) and 77 roots at \(c=13\).
The exact row count is

\[
78(32+31+30+29)+77\cdot28=11{,}672.
\]

This gives an all-root cut family without choosing or enumerating any
particular common-core isomorphism type.
