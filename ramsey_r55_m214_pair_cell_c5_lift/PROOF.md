# Exact missed-pair-cell lift and the \(C_5\) edge hull

## Setting

Color every edge of \(K_{43}\) red or blue, and write \(x_{ij}=1\) for a red
edge. Assume there is no monochromatic \(K_5\). Let \(uv\) be the red anchor
edge of one root in the complete height-3148 cover, and let

\[
H=N_R(u)\cap N_R(v),\qquad |H|=c\in\{9,10,11,12,13\}.
\]

For an unordered exterior pair \(P=\{z,z'\}\), define its missed core cell

\[
M_P=\{h\in H:x_{zh}=x_{z'h}=0\}.
\]

Put \(m=|M_P|\), and let \(e\) be the number of red edges induced by
\(M_P\).

## The missed-cell theorem

If \(zz'\) is blue, then

\[
m\leq5,\qquad e\geq m-2,\qquad e\geq3m-10.
\]

When \(m=5\), the missed cell induces a red \(C_5\).

To prove this, first observe that the red graph on \(H\) is triangle-free:
a red triangle in \(H\), together with the red edge \(uv\), would be a red
\(K_5\). The red graph induced by \(M_P\) has no independent triple either.
Indeed, three pairwise blue vertices in \(M_P\), together with the blue edge
\(zz'\), would be a blue \(K_5\). Thus both the red graph on \(M_P\) and its
complement are triangle-free.

The equality \(R(3,3)=6\) gives \(m\leq5\). For orders zero through five, the
minimum possible red-edge counts are

\[
0,0,0,1,2,5.
\]

The values through order four are immediate: three vertices require one red
edge, while four vertices require at least two, with a matching attaining two.
For order five, each vertex has red degree exactly two. Red degree at least
three would give a blue triangle among its red neighbors, while red degree at
most one would give a red triangle among its blue neighbors. Hence the graph
is 2-regular and triangle-free on five vertices, so it is \(C_5\) and has five
red edges.

The lower convex envelope of the six displayed values has precisely the two
nonzero facets

\[
e\geq m-2,qquad e\geq3m-10.
\]

Together with \(e\geq0\), these inequalities recover every displayed minimum.

## Exact auxiliary definitions

The lift shares auxiliary variables across all roots. For every physically
used triple \((P,h)\), define

\[
m_{P,h}=(1-x_{zh})(1-x_{z'h}).
\]

Three Boolean inequalities define this conjunction exactly. For every
physically used \((P,\{i,j\})\), define

\[
q_{P,ij}=m_{P,i}m_{P,j}x_{ij}.
\]

Four Boolean inequalities define this conjunction exactly. Consequently, for
an active root,

\[
\sum_{h\in H}m_{P,h}=m,qquad
\sum_{\{i,j\}\in\binom H2}q_{P,ij}=e.
\]

The union of supports over all 389 roots contains 10,612 \(m\)-variables and
74,513 \(q\)-variables. Variables are not duplicated when two roots use the
same physical pair-cell coordinate.

## Guarded rows

Let \(y_r\) select root \(r\), and let \(x_P=x_{zz'}\). For each of the
169,662 root/exterior-pair instances, append the following three rows:

\[
-m+(c-5)x_P-(c-5)y_r\geq-c,
\]

\[
e-m+(c-2)x_P-(c-2)y_r\geq-c,
\]

\[
e-3m+(3c-10)x_P-(3c-10)y_r\geq-3c.
\]

If \(y_r=1\) and \(x_P=0\), these are exactly \(m\leq5\), \(e\geq m-2\),
and \(e\geq3m-10\). If the root is inactive or the exterior pair is red, the
rows follow from \(0\leq m\leq c\) and \(e\geq0\), so they are tautological.

## Equisatisfiability

Every assignment satisfying the height-3254 formula has a unique extension to
the new auxiliary variables, obtained from their displayed Boolean products.
The missed-cell theorem proves all new guarded rows for that extension.
Conversely, deleting the new variables and rows from any satisfying lifted
assignment leaves every height-3254 constraint unchanged. The lifted formula
is therefore satisfiable exactly when the complete height-3254 formula is.

This is an exact formulation strengthening, not an exclusion of a root or a
solver verdict.

## Sharpness

Use the cyclic red graph on
\(\mathbb Z/13\mathbb Z\), where \(ij\) is red when
\(i-j\pmod {13}\in\{1,5,8,12\}\). Its nested cores in the order

\[
0,1,2,3,4,5,8,9,6,7,10,11,12
\]

are triangle-free with independence number four at every order from nine
through thirteen. The missed sets

\[
\{0,1,3\},\qquad \{0,1,3,4\},\qquad \{0,1,2,3,8\}
\]

have respectively \(m=3,4,5\), independence number two, and \(e=1,2,5\).
Giving both blue-adjacent exterior vertices footprint \(H\setminus M_P\)
therefore produces local no-monochromatic-\(K_5\) witnesses. These three
examples attain the first facet, both facets, and the second facet,
respectively. They prove that neither coefficient nor right-hand side can be
strengthened from the local missed-cell hypotheses.
