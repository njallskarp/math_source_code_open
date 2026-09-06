# Sharp blue-pair footprint compression

## Universal union theorem

Let \(G\) be a red/blue coloring of a complete graph with no monochromatic
\(K_5\). Let \(uv\) be red and put

\[
H=N_R(u)\cap N_R(v),\qquad |H|=c.
\]

For exterior vertices \(z,z'\notin H\cup\{u,v\}\), define

\[
S_z=N_R(z)\cap H,\qquad S_{z'}=N_R(z')\cap H.
\]

If \(zz'\) is blue, then

\[
|S_z\cup S_{z'}|\geq c-5.
\]

Indeed, the red graph on \(H\) is triangle-free. If a red-independent triple
\(Q\subseteq H\) missed \(S_z\cup S_{z'}\), then the three edges in \(Q\),
all six contacts from \(Q\) to \(z,z'\), and \(zz'\) would be blue. This is a
blue \(K_5\). Hence the triangle-free graph on
\(H\setminus(S_z\cup S_{z'})\) has no independent triple. The elementary
equality \(R(3,3)=6\) bounds its order by five.

For completeness, the upper bound \(R(3,3)\leq6\) follows by choosing any
vertex of a two-colored \(K_6\), taking three same-colored incident edges,
and inspecting the triangle on their other endpoints. A red five-cycle with
blue complement proves the lower bound.

## Sharpness for every codegree

Use the cyclic red graph on \(\mathbb Z/13\mathbb Z\) whose edge differences
are \(\{1,5,8,12\}\). It is triangle-free and has independence number four.
Let

\[
T=\{0,1,2,3,4,5,8,9\},\qquad
(e_1,\ldots,e_5)=(6,7,10,11,12),
\]

and set \(H_c=T\cup\{e_1,\ldots,e_{c-8}\}\) for
\(c=9,\ldots,13\). The set

\[
C=\{0,1,2,3,8\}
\]

has independence number two. Thus \(U_c=H_c\setminus C\) has size \(c-5\),
meets every independent four-set, and meets every independent triple. Give
two new vertices the same footprint \(U_c\) and color their mutual edge blue.
The resulting \(H_c\)-plus-two-vertices coloring has no monochromatic
\(K_5\), so the union bound is sharp from the local conditions for all five
codegrees. This does not assert extension to order 43.

## Sharp auxiliary-free projection

Because \(|S_z\cup S_{z'}|\leq |S_z|+|S_{z'}|\), a blue exterior edge also
forces

\[
|S_z|+|S_{z'}|\geq c-5.
\]

The prior individual bound gives \(|S_z|+|S_{z'}|\geq2(c-8)\). Therefore the
new sum inequality is strictly stronger precisely for \(c=9,10\), equal at
\(c=11\), and weaker at \(c=12,13\).

The right-hand side is sharp in the two strict cases. For the nested cores
above, disjoint valid footprints are

```text
c=9:  {0,4} and {5,6}
c=10: {0,4,5} and {2,3}
```

Their unions meet every independent triple and their sizes sum to \(c-5\).
The individual rows do not imply the pair row: assigning both exterior
vertices footprint \(\{6\}\) at \(c=9\), or \(\{6,7\}\) at \(c=10\),
satisfies both individual transversal bounds but misses an independent triple.

## Selector-guarded formula

For a selected height-3148 root \(r\), let \(H_r\) have codegree
\(c_r\in\{9,10\}\), and let \(y_r\) be its selector. For every unordered pair
\(z,z'\) outside \(H_r\cup\{u,v\}\), append

\[
\sum_{h\in H_r}(x_{zh}+x_{z'h})
+(c_r-5)x_{zz'}-(c_r-5)y_r\geq0.
\]

When \(y_r=0\), the row is tautological. When \(y_r=1\) and \(zz'\) is red,
the edge term makes it tautological. When the root is active and \(zz'\) is
blue, it is exactly the proved sum bound.

There are 78 roots at each of \(c=9,10\). Their exterior sets have sizes 32
and 31, so the nonredundant suffix has

\[
78\binom{32}{2}+78\binom{31}{2}=74{,}958
\]

rows. Every model of the prior complete formula satisfies the suffix, while
every strengthened model is plainly a prior model. The two formulas are
therefore equisatisfiable.
