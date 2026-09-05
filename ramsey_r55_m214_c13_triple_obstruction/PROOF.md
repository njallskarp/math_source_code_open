# Triple incompatibility in the cyclic \(c=13\) core

## General lemma

Let \(H\) be the red graph induced by the common-red core of two red-adjacent
anchors, and let

\[
S_x=N_R(x)\cap V(H)
\]

be the red core footprint of an outside vertex \(x\). Suppose three outside
vertices \(x,y,z\) have the following properties.

1. For each pair \(p,q\in\{x,y,z\}\), the set
   \(V(H)\setminus(S_p\cup S_q)\) contains an independent triple of \(H\).
2. The common footprint \(S_x\cap S_y\cap S_z\) contains an edge of \(H\).

Then these three footprints cannot occur simultaneously in a red/blue
coloring with no monochromatic \(K_5\).

## Proof

Fix a pair \(p,q\in\{x,y,z\}\). If \(pq\) were blue, then \(p,q\) together
with the independent triple from condition 1 would form a blue \(K_5\): the
three core edges are blue, and all six edges from the core triple to \(p,q\)
are blue because the triple misses \(S_p\cup S_q\). Hence each of \(xy,xz,yz\)
must be red.

Let \(ab\) be the red core edge supplied by condition 2. Both \(a\) and \(b\)
belong to all three footprints, so all six edges from \(\{a,b\}\) to
\(\{x,y,z\}\) are red. The three outside edges and \(ab\) are red as well.
Thus \(\{a,b,x,y,z\}\) is a red \(K_5\), a contradiction. \(\square\)

## Explicit obstruction

In the cyclic core on \(\mathbb Z/13\mathbb Z\), let

\[
i\sim j \quad\Longleftrightarrow\quad
i-j\in\{1,5,8,12\}\pmod {13}.
\]

The height-2969 certificate contains the three footprints

\[
\begin{aligned}
S_0&=\texttt{1c48}=\{3,6,10,11,12\},\\
S_{10}&=\texttt{0e2c}=\{2,3,5,9,10,11\},\\
S_{18}&=\texttt{1f42}=\{1,6,8,9,10,11,12\}.
\end{aligned}
\]

The core triple \(\{0,4,7\}\) is independent and is disjoint from each of
\(S_0\cup S_{10}\), \(S_0\cup S_{18}\), and
\(S_{10}\cup S_{18}\). Consequently all three outside pairs are forced red.
Their common footprint is exactly \(\{10,11\}\), which is a red core edge.
The general lemma therefore excludes every outside-edge completion of these
three rows.

The 52 affine core automorphisms

\[
i\longmapsto ai+b,
\qquad a\in\{1,5,8,12\},\quad b\in\mathbb Z/13\mathbb Z,
\]

produce 52 distinct unordered forbidden triples of footprint types. The
certificate checker verifies every transformed witness directly.
