# Edge-deletion absorption in the two-leaf diamond footprint

This note identifies exactly where proper-subgraph criticality can add new
information to the two-leaf obstruction.  Eleven of the local graph edges
are already chromatic-critical for elementary reasons: after deleting any
one of them, the fixed eight-vertex complement footprint can be covered by
three cliques.  The only potentially informative edges are the missing
incidences between the unavailable endpoint and the two obstructing pairs.
Deleting one of those edges forces every colouring witness to alter a third
pair class outside the footprint.

The result is a local structural reduction.  It does not eliminate any of
the order-58 frontier rows.

## 1. Exact footprint

Let \(H=\overline G\).  Use the two-leaf notation

\[
X=\{v,w,p,q,a_i,b_i,a_j,b_j\},
\qquad M_i=\{a_i,b_i\},\quad M_j=\{a_j,b_j\}.
\]

The induced graph \(H[X]\) has the following fixed edges:

\[
vp,vq,pq,wp,wq,
\]

\[
va_i,va_j,wb_i,wb_j,
\]

and all four edges between \(\{a_i,a_j\}\) and
\(\{b_i,b_j\}\).  Its only remaining variable edges are the incidences
from \(q\) to the two pair classes.  Put

\[
Q_i=N_H(q)\cap M_i,
\qquad Q_j=N_H(q)\cap M_j.
\]

The blocker conclusion of the two-leaf theorem says that \(Q_i,Q_j\) are
nonempty and that either

\[
|Q_i|+|Q_j|\geq 3,
\]

or the two singleton blockers have the same orientation:

\[
(Q_i,Q_j)=(\{a_i\},\{a_j\})
\quad\text{or}\quad
(Q_i,Q_j)=(\{b_i\},\{b_j\}).
\]

These are exactly seven labelled blocker states.

Define the eleven forced nonedges of \(H[X]\)

\[
\begin{aligned}
E_0=\{&vw,,vb_i,,vb_j,,wa_i,,wa_j,\\
      &pa_i,,pb_i,,pa_j,,pb_j,,a_i a_j,,b_i b_j\}.
\end{aligned}
\]

Thus every member of \(E_0\) is an edge of \(G[X]\).  The only other
possible edges of \(G[X]\) are the **blocker gaps**

\[
D=\{qx:x\in M_i\cup M_j\text{ and }qx\notin E(H)\}.
\]

The blocker alternatives imply \(0\leq |D|\leq 2\).

## 2. Local absorption dichotomy

### Theorem

For the footprint above, the following statements hold.

1. For every \(e\in E_0\), the graph \(H[X]+e\) has a partition into
   three cliques.
2. For every \(e\in D\),

   \[
   \theta(H[X]+e)=4.
   \]

Consequently, suppose the fixed minimum clique partition of \(H\) is

\[
\mathcal P_v=\{\{v\},\{w,p,q\},M_i,M_j\}
  \cup\{M_\ell:\ell\notin\{i,j\}\},
\]

where there are \(k-4\) outside pair blocks.  If \(\chi(G)=k\), then every
edge in \(E_0\) is already chromatic-critical:

\[
\chi(G-e)=k-1\qquad(e\in E_0).
\]

This conclusion uses no edge-criticality hypothesis.  If instead
\(e\in D\) and proper-subgraph criticality supplies a \((k-1)\)-colouring
of \(G-e\), then the corresponding \((k-1)\)-clique cover of \(H+e\)
must alter at least one outside pair \(M_\ell\).  It cannot be supported on
the eight-vertex footprint alone.

### Proof of absorption

It is enough to give four representative three-clique covers; swapping
\(i,j\), and simultaneously applying

\[
v\leftrightarrow w,
\qquad a_i\leftrightarrow b_i,
\qquad a_j\leftrightarrow b_j,
\]

gives all eleven cases.  Slashes separate clique blocks.

| Added edge | Three-clique cover of \(X\) |
|---|---|
| \(vw\) | \(\{v,w,p,q\}/M_i/M_j\) |
| \(vb_i\) | \(\{v,a_i,b_i\}/\{w,p,q\}/M_j\) |
| \(a_i a_j\) | \(\{v,p,q\}/\{w,b_i\}/\{a_i,a_j,b_j\}\) |
| \(pa_i\), if \(qa_i\in E(H)\) | \(\{v,p,q,a_i\}/\{w,b_i\}/M_j\) |
| \(pa_i\), if \(qa_i\notin E(H)\) | \(\{v,p,a_i\}/\{w,q,b_i\}/M_j\) |

In the final row, nonemptiness of \(Q_i\) gives \(qb_i\in E(H)\).
Every displayed block is therefore a clique after the indicated single edge
is added.  The symmetry gives the covers for \(wa_i\), the four edges from
\(p\) to the pair vertices, and the second diagonal \(b_i b_j\).

Appending the \(k-4\) unchanged outside pairs gives a
\((k-1)\)-clique cover of \(H+e\).  Hence \(\chi(G-e)\leq k-1\).  Since
adding one edge can raise chromatic number by at most one and
\(\chi(G)=k\), equality follows.

There is also a useful general explanation for the four incident edges.
In any \((k-1)\)-colouring of \(G-v\), a vertex \(v\) of degree \(k-1\)
has exactly one neighbour in each colour class.  After deleting an incident
edge \(vx\), assign \(v\) the colour of \(x\).  Thus every edge incident to
a low vertex has a canonical deletion colouring inherited from the
vertex-deletion colouring; its criticality contains no cross-factor data.

### Proof that blocker gaps do not absorb locally

The base partition

\[
\{v\}/\{w,p,q\}/M_i/M_j
\]

shows \(\theta(H[X]+e)\leq4\) for every blocker gap \(e\).  By the two
symmetries above, it remains to take \(e=qa_i\).

Here \(qa_i\notin E(H)\) before the edge is added.  Hence
\(Q_i=\{b_i\}\).  Blocker coherence then forces

\[
qb_i,qb_j\in E(H).
\]

The graph \(H[X]+qa_i\) has no clique of order four.  A partition of its
eight vertices into three cliques would therefore have block sizes
\(3,3,2\).

The vertex \(p\) is adjacent inside the footprint only to \(v,w,q\).  If
its block is a triangle, that block is \(\{p,v,q\}\) or
\(\{p,w,q\}\).  After deleting either triangle, the five remaining
vertices induce a complete bipartite graph \(K_{3,2}\), which has no
triangle and hence cannot be covered by a triangle and a pair.

If the block containing \(p\) is a pair, it is one of

\[
\{p,v\},\quad\{p,w\},\quad\{p,q\}.
\]

After deleting \(\{p,v\}\) or \(\{p,w\}\), every triangle of the
six-vertex remainder contains \(q\), so two disjoint triangles are
impossible.  After deleting \(\{p,q\}\), the remainder is bipartite and
has no triangle.  These cases exhaust the required \((3,3,2)\) partition.
Thus no three-clique cover exists, proving
\(\theta(H[X]+qa_i)=4\).

### Proof of the external escape

Suppose a \((k-1)\)-clique cover of \(H+e\), for \(e\in D\), left every
outside pair \(M_\ell\) as an unchanged block and used no outside vertex in
a block meeting \(X\).  Removing the \(k-4\) outside blocks would leave a
three-clique cover of \(H[X]+e\), contradicting the equality just proved.
Therefore at least one outside pair class must be altered or mixed into the
exceptional part of the cover.

For \(k=4\), there is no outside pair.  Proper-subgraph criticality then
forces \(D=\varnothing\).  For \(k=29\), every informative edge-deletion
witness at this two-leaf footprint must cross the boundary to at least one
of the other 25 pair classes.

## 3. Interpretation for the order-58 frontier

This theorem closes the most immediate attempt suggested by the
order-\(2k\) equality-scope audit.  Proper-subgraph criticality does not create an
independent factor at any edge incident to \(v\), at either rectangle
diagonal, or along any of the eight fixed routing incidences in \(E_0\).
All those witnesses are already encoded by the base diamond and rectangle.

Only blocker-gap edges at \(q\) can carry new local information.  When such
an edge exists, its deletion colouring must make a third-pair exchange.  If
all four blocker incidences are present in \(H\), then \(D=\varnothing\)
and every graph edge in the eight-vertex footprint is locally absorbed.

No edge row is eliminated: the theorem supplies an exact interface, not an
edge count.  A viable continuation must now couple a blocker-gap deletion
cover to the endpoint-deletion escape, or use the absence of blocker gaps as
a quantitative degree/excess condition.  Applying edge-criticality to an
arbitrary edge of the footprint without this dichotomy cannot add a new
constraint.

## 4. Reproduction and trust boundary

The standard-library checker enumerates the seven blocker states and all
set partitions of the labelled eight-vertex footprint.  It verifies all 77
forced-edge absorptions, checks each displayed constructive witness, and
confirms that all eight labelled blocker-gap instances have exact clique-
cover number four.

```sh
cd albertson_order2k_diamond_capacity
PYTHONDONTWRITEBYTECODE=1 python3 verify_edge_deletion_absorption.py
```

Expected output:

```text
blocker_states=7
forced_G_edges=11
forced_absorptions=77 all_three_clique=yes
blocker_gap_instances=8 theta_all=4 external_escape=yes
certificate_sha256=2823d26a79c80fd10da44afa67ef8335ced96a8c0f451a9e5063f458221ade72
```

The computation is exhaustive exact finite-set arithmetic.  It verifies the
local classification only; the uniform theorem and global escape consequence
are the prose proof above.  There is no solver, floating point, randomness,
crossing-number input, topology classification, or private data.
