# Global minimum size and rigidity of a nonlinear Hamming class

The small-alphabet argument in `MULTIBOX_OBSTRUCTION.md` assumes that every
ambient factor has order at most the degree threshold.  Boundary-mixing
constructions do not satisfy that assumption: a colour class may enter a
stripped block and hence use a long coordinate line.  The following theorem
removes the ambient caps completely, provided the class is genuinely
nonlinear.

## Global theorem

Let

\[
H=K_{n_1}\mathbin\square\cdots\mathbin\square K_{n_d}
\]

be an arbitrary finite Hamming graph, let \(h\ge2\), and let
\(\varnothing\ne C\subseteq V(H)\).  Suppose \(H[C]\) has minimum degree at
least \(h\).  If \(C\) is not contained in one coordinate line, then

\[
\boxed{|C|\ge2h.}
\tag{1}
\]

Moreover, equality holds if and only if, after permuting coordinates and
symbols,

\[
C=X\times\{0,1\}\times\{0\}\times\cdots\times\{0\},
\qquad |X|=h.
\tag{2}
\]

Thus every equality set induces \(K_h\mathbin\square K_2\).  With
\(h=s-1\), every nonlinear legal part has at least \(2s-2\) vertices, and
the extremal part is uniquely of \(K_{s-1}\mathbin\square K_2\) type.

## Proof

Let \(M\) be the largest intersection of \(C\) with a coordinate line.

### Case 1: no line contains more than \(h\) selected vertices

Fix \(v\in C\).  For each coordinate \(i\), let \(a_i\) be the number of
selected neighbours of \(v\) in direction \(i\), and put
\(A=\sum_i a_i\).  Then

\[
0\le a_i\le h-1,
\qquad A\ge h.
\tag{3}
\]

A direction-\(i\) neighbour already sees \(v\) and the other \(a_i-1\)
selected vertices on that line.  It needs at least \(h-a_i\) selected
neighbours in the second Hamming shell around \(v\).  Every second-shell
vertex is adjacent to at most two first-shell vertices, so

\[
|C|\ge1+A+\frac12\sum_i a_i(h-a_i).
\tag{4}
\]

Under the caps in (3), cap-majorization minimizes the right side by filling
entries to \(h-1\).  At the first feasible total \(A=h\), the extremal
profile is \((h-1,1)\) and (4) equals \(2h\).  Replacing the partial entry
\(1\) by \(1+t\) adds \(t(h-t)/2\ge0\).  Once two caps are full, the bound is
at least \(1+3(h-1)\ge2h\), and subsequent cap intervals have their minimum
at an endpoint.  This proves (1) in the first case.

If equality holds, (3)--(4) force degree exactly \(h\), first-shell profile
\((h-1,1)\), and exactly \(h-1\) second-shell vertices.  The \(h-1\)
neighbours in the first direction, together with \(v\), form an \(h\)-set
on one line.  Each of them lacks one neighbour, while the lone neighbour in
the second direction lacks \(h-1\).  Equality in the double count forces
each second-shell vertex to be the unique rectangle completion joining that
lone neighbour to one point of the first line.  These are precisely the
vertices in (2).

### Case 2: some line contains at least \(h\) selected vertices

Choose a coordinate line \(L\) with \(|C\cap L|=M\ge h\), and put
\(O=C\setminus L\).  The set \(O\) is nonempty.  A vertex outside \(L\) is
adjacent to at most one vertex of \(L\).  If there is no edge from \(O\) to
\(L\), minimum degree gives \(|O|\ge h+1\), and hence
\(|C|\ge2h+1\).  Otherwise an endpoint in \(O\) has at least \(h-1\)
neighbours in \(O\), so \(|O|\ge h\) and

\[
|C|=M+|O|\ge2h.
\]

For equality, \(M=|O|=h\).  Every vertex of \(O\) has at most one neighbour
in \(L\), so it must be adjacent to all other \(h-1\) vertices of \(O\).
Thus \(O\) is an \(h\)-clique and lies on a coordinate line.  The same
degree count forces exactly one cross-edge at every vertex of both lines.
Two disjoint coordinate-line subsets of size at least two can have such a
perfect matching only when the lines are parallel, their fixed coordinates
differ in exactly one position, and they use the same \(h\) symbols in the
varying coordinate.  This is again (2), completing the proof.

Conversely, the set in (2) has \(2h\) vertices and induced degree
\((h-1)+1=h\), so every stated equality configuration really is extremal.

## First-carry obstruction and rigidity

Let \(s\ge3\), \(m,n\ge s\), and \(2\le p<s\).  Write

\[
m\equiv r\pmod s,
\qquad n\equiv u\pmod s,
\qquad 1\le r,u<s,
\]

and assume

\[
ru<s,
\qquad s\le R:=rup<2s.
\tag{5}
\]

The sharp thin-coordinate theorem gives

\[
Q=p\left\lfloor\frac{mn}{s}\right\rfloor
\]

as the maximum number of coordinate-line parts of minimum degree at least
\(s-1\).  Since \(mn\bmod s=ru\), condition (5) gives

\[
mnp=sQ+R,
\qquad
\left\lfloor\frac{mnp}{s}\right\rfloor=Q+1.
\tag{6}
\]

Suppose the minor box nevertheless partitions into the quotient-optimal
\(Q+1\) legal parts.  At least one part is nonlinear.  Every legal part has
at least \(s\) vertices, while (1) makes that nonlinear part have at least
\(2s-2\).  Comparing with (6) yields

\[
R\ge2s-2.
\tag{7}
\]

If equality holds in (7), a second nonlinear part would contribute at least
\(2s-2>s\) vertices and make the volume inequality strict.  Hence the
nonlinear part is unique and is extremal in (1).  Every remaining part has
exactly \(s\) vertices and minimum degree \(s-1\), so it is a clique; every
clique of a Hamming graph is contained in one coordinate line.

Consequently:

1. If \(s\le R\le2s-3\), no boundary-mixing partition can repair the line
   deficit.
2. If \(R=2s-2\) and an optimal partition exists, it contains exactly one
   nonlinear part; that part is a \(K_{s-1}\square K_2\), and every other
   part is a coordinate-line \(K_s\).

In particular, the \(K_4\square K_2\) used by the `(2,2,2)` construction at
\(s=5\) is not merely sufficient: its order and isomorphism type are forced
in every quotient-optimal repair.

This corollary concerns optimal partitions of the minor Hamming box and the
major-coordinate lifts obtained from them.  It does not assert that every
majority colouring of the full four-dimensional graph is such a lift.

## Literature and trust boundary

The originating majority-colouring problem is Open Problem 2 of Bujtás,
Dettlaff, Furmańczyk, and Laskowska, *Majority C-coloring in Cartesian
products* (2026), <https://arxiv.org/abs/2608.27669>.  The small-alphabet
version of (1) and its equality classification are already recorded in the
committed graph at heights 1965 and 1977.  The new content here is the removal
of every ambient alphabet cap for nonlinear classes and the resulting global
first-carry obstruction and rigidity.  Targeted searches through 2026-09-05
found work on large induced Hamming subgraphs with bounded maximum degree and
on induced-subgraph recognition, but no matching minimum-order/minimum-degree
theorem or (7).  Novelty is search-relative, not a priority claim.

The accompanying standard-library CPython checker exhausts every subset of
small products, evaluates every applicable degree threshold, recognizes the
equality geometry directly from coordinates, and audits the first-carry
arithmetic on a large finite parameter range.  These computations corroborate
the definitions, equality cases, and algebra.  Universal validity rests on
the displayed shell, maximal-line, and volume arguments plus the cited sharp
thin-coordinate theorem.
