# The multi-box barrier and its unique two-box exception

## A sharp small-alphabet class-size lemma

Let

\[
H=K_{r_1}\mathbin\square\cdots\mathbin\square K_{r_d},
\qquad 1\le r_i\le s-1,
\]

where \(s\ge3\).  If a nonempty vertex set \(C\subseteq V(H)\) induces
minimum degree at least \(s-1\), then

\[
\boxed{|C|\ge 2s-2.}
\tag{1}
\]

The bound is sharp: a copy of
\(K_{s-1}\mathbin\square K_2\), with all other coordinates fixed, has
\(2s-2\) vertices and induced degree \(s-1\).

### Proof

Put \(h=s-1\), fix \(v\in C\), and let \(a_i\) be the number of neighbours
of \(v\) in \(C\) along coordinate \(i\).  Then

\[
0\le a_i\le r_i-1\le h-1,
\qquad A:=\sum_i a_i\ge h.
\tag{2}
\]

Each selected neighbour in direction \(i\) already sees \(v\) and the other
\(a_i-1\) selected vertices on its coordinate line.  It therefore needs at
least \(h-a_i\) selected neighbours in the second Hamming shell around
\(v\).  A second-shell vertex is adjacent to at most two first-shell
vertices.  Double counting gives

\[
|C|\ge
1+A+\frac12\sum_i a_i(h-a_i).
\tag{3}
\]

For a fixed value of \(A\), the right side is minimized by maximizing
\(\sum_i a_i^2\).  Under the relaxed common cap \(a_i\le h-1\), a greedy
vector with as many entries \(h-1\) as possible and at most one partial
entry does this by majorization.  Write

\[
g(x)=x+\frac{x(h-x)}2.
\]

At the first feasible total \(A=h\), the greedy vector is
\((h-1,1,0,\ldots)\), and

\[
1+g(h-1)+g(1)=2h.
\tag{4}
\]

Until the second cap fills, write the partial entry as \(1+t\), where
\(0\le t\le h-2\).  Its change from (4) is

\[
g(1+t)-g(1)=\frac{t(h-t)}2\ge0.
\tag{5}
\]

At two full caps the bound is \(1+3(h-1)\), exceeding \(2h\) by
\(h-2\).  On every later cap interval the greedy bound is concave in its
single partial entry, so its minimum occurs at an endpoint; every endpoint
has at least two full caps and hence is no smaller.  Thus (3) is at least
\(2h=2s-2\), proving (1).

For \(s=2\), every \(r_i\le1\), so the residue graph is edgeless and no
nonempty set can have minimum degree at least one.  This vacuous case will
also cause no exception below.

## Classification of pure residual-box completion in four factors

Let

\[
B_r=[r_2]\times[r_3]\times[r_4],
\qquad 0\le r_j<s,
\qquad R=r_2r_3r_4,
\]

and put \(q=\lfloor R/s\rfloor\).  Suppose \(q\ge2\).  Consider the
natural *pure residual-box completion* of the mixed-radix construction: after
all exact axis-parallel \(s\)-cliques have been stripped, partition \(B_r\)
into exactly \(q\) sets, each inducing minimum degree at least \(s-1\) in
the residual Hamming graph.

Such a completion exists if and only if

\[
\boxed{s=3\quad\text{and}\quad(r_2,r_3,r_4)=(2,2,2),}
\tag{6}
\]

up to permuting the three minor coordinates.

Indeed, (1) would force

\[
R\ge q(2s-2).
\tag{7}
\]

On the other hand, the definition of \(q\) gives \(R<(q+1)s\).  For
\(s\ge4\) and \(q\ge2\),

\[
q(2s-2)-(q+1)s=(q-1)s-2q\ge0,
\]

contradicting (7).  There is no \(s=2\) multi-box range because \(R\le1\).
When \(s=3\), one has \(R\le8\).  Since every legal part has at least four
vertices, \(q\ge2\) forces \(R=8\), hence all three residues equal two.
Conversely, split the cube \([2]^3\) into its two faces perpendicular to any
coordinate.  Each face is \(K_2\mathbin\square K_2\), so it has four vertices
and induced degree two.

This is a barrier for the specified Euclidean strategy, not a nonexistence
theorem for arbitrary majority C-colourings: a different optimal colouring
could mix residue cells with cells assigned to the stripped line blocks.

## Four-dimensional Hamming consequence

Let

\[
G=K_{n_1}\mathbin\square K_{n_2}\mathbin\square
K_{n_3}\mathbin\square K_{n_4},
\qquad n_1\ge n_2\ge n_3\ge n_4\ge2,
\]

write \(N_i=n_i-1\), and set

\[
h=\left\lceil\frac{N_1+N_2+N_3+N_4}{2}\right\rceil,
\qquad s=h-N_1+1.
\]

Assume \(h\ge N_1\), \(s=3\), and

\[
n_2\equiv n_3\equiv n_4\equiv2\pmod3.
\tag{8}
\]

Strip the exact \(3\)-cliques from the minor box as in the mixed-radix
construction.  Its unused box is \([2]^3\), which the two-face partition
above splits into two legal parts.  Since the residue volume is
\(8=2\cdot3+2\), the total number of minor parts is exactly
\(\lfloor n_2n_3n_4/3\rfloor\).  Lifting every minor part through the whole
first coordinate gives same-colour degree

\[
N_1+(s-1)=N_1+2=h.
\]

The first/second-shell upper bound from
`NEAR_TRIANGLE_FOUR_DIMENSIONAL.md` gives the reverse inequality.  Therefore

\[
\boxed{
\overline\chi_{\ge}(G)
=
\left\lfloor\frac{n_2n_3n_4}{3}\right\rfloor .
}
\tag{9}

This is outside both preceding residue regimes: its residue product is eight,
so it is neither less than \(s=3\) nor less than \(2s=6\).

## Explicit infinite families

Choose integers

\[
q_2\ge q_3\ge q_4\ge0,
\qquad q_3+q_4\ge1,
\qquad \varepsilon\in\{0,1\},
\]

and put \(Q=q_2+q_3+q_4\).  Define

\[
(n_1,n_2,n_3,n_4)
=
(3Q+\varepsilon,\ 3q_2+2,\ 3q_3+2,\ 3q_4+2).
\tag{10}

The factors in (10) are nonincreasing.  A direct deficit calculation gives

\[
h=3Q+\varepsilon+1,
\qquad h-(n_1-1)+1=3,
\]

and the three minor residues are \((2,2,2)\).  Hence (9) yields

\[
\boxed{
\overline\chi_{\ge}(G)
=9q_2q_3q_4
+6(q_2q_3+q_2q_4+q_3q_4)
+4Q+2.
}
\tag{11}

For example,
\(K_7\mathbin\square K_5\mathbin\square K_5\mathbin\square K_2\)
has \(s=3\) and majority C-chromatic number \(16\).

## Trust and literature boundary

The class-size lemma, volume contradiction, exceptional face partition, and
lift are universal arguments.  The accompanying standard-library Python
checker audits exact shell profiles, exhaustively checks all subsets of small
residue boxes, reconstructs bounded exceptional partitions cell by cell, and
verifies a finite grid from (10).  It uses no floating point, randomness,
solver, or external data; its finite checks corroborate the proof rather than
replace it.

The primary literature boundary remains Open Problem 2 of Bujtas, Dettlaff,
Furmanczyk, and Laskowska, *Majority C-coloring in Cartesian products* (2026),
<https://arxiv.org/abs/2608.27669>.  The paper asks for imbalanced
four-dimensional Hamming graphs but does not state (1), the residual-box
classification (6), or the exact family (10)--(11).  Novelty is
search-relative.
