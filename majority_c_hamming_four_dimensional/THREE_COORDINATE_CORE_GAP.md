# A dimension gap for small Hamming cores

The global nonlinear-class theorem shows that a Hamming induced subgraph of
minimum degree at least \(h\) either lies on a coordinate line or has at least
\(2h\) vertices, with equality rigidly equal to
\(K_h\mathbin\square K_2\).  The next possible order still cannot use a
third coordinate.

## Theorem

Let

\[
H=K_{n_1}\mathbin\square\cdots\mathbin\square K_{n_d}
\]

be an arbitrary finite Hamming graph, let \(h\ge2\), and let
\(\varnothing\ne C\subseteq V(H)\) induce minimum degree at least \(h\).
If \(C\) is not contained in a coordinate two-flat—that is, if its vertices
vary in at least three ambient coordinates—then

\[
\boxed{|C|\ge2h+2.} \tag{1}
\]

Equivalently, every Hamming \(h\)-core on at most \(2h+1\) vertices is
contained in the Cartesian product of at most two coordinate lines.

The bound is attained for \(h=2\) by the induced six-cycle obtained from
the three-cube by deleting two opposite vertices, and for \(h=3\) by the
whole three-cube.

## Preliminaries

Every connected component of a graph of minimum degree at least \(h\) has
at least \(h+1\) vertices.  Thus an \(h\)-core with at most \(2h+1\)
vertices is connected.

At a vertex \(v\in C\), let \(a_i\) be the number of neighbours of \(v\)
in coordinate direction \(i\), omitting zero entries, and put
\(A=\sum_i a_i\).  If every coordinate line meets \(C\) in at most \(h\)
vertices, then

\[
1\le a_i\le h-1,\qquad A\ge h. \tag{2}
\]

A first-shell neighbour in direction \(i\) already has \(a_i\) neighbours
among \(v\) and the other vertices of that line.  It therefore needs at
least \(h-a_i\) neighbours in the second shell around \(v\).  A
second-shell vertex is adjacent to at most two first-shell vertices.  Hence

\[
|C|\ge 1+A+\frac12\sum_i a_i(h-a_i). \tag{3}
\]

For \(|C|=2h+1\), elementary capped majorization in (2)--(3) leaves only
the following positive direction profiles, up to order:

\[
\begin{array}{c|c}
h & (a_i)\\ \hline
2 &(1,1)\\
3 &(2,1),(2,2),(1,1,1)\\
4 &(3,1),(2,2)\\
h\ge5 &(h-1,1).
\end{array} \tag{4}
\]

For completeness, when \(h\ge4\), (3) first rules out \(A\ge h+1\) by
moving mass to entries of size \(h-1\).  At \(A=h\), three positive entries
have least penalty at \((h-2,1,1)\), which is possible only for \(h\le3\).
With two entries \(a+h-a=h\), inequality (3) becomes
\(a(h-a)\le h\), giving exactly the rows in (4).  Direct substitution gives
the two remaining small rows.

## Proof

Suppose for contradiction that \(|C|\le2h+1\) and \(C\) varies in at
least three coordinates.  The global nonlinear theorem already handles
smaller orders: a nonlinear set has at least \(2h\) vertices, and equality
is the two-dimensional prism \(K_h\mathbin\square K_2\).  It therefore
suffices to treat

\[
|C|=2h+1. \tag{5}
\]

Let \(M\) be the largest intersection of \(C\) with a coordinate line.

### A line containing at least \(h+1\) selected vertices

Take a maximizing line \(L\).  Because \(C\) is not itself a line,
\(O=C\setminus L\) is nonempty.  A vertex outside \(L\) has at most one
neighbour on \(L\).  If \(M\ge h+2\), then such a vertex has degree at most

\[
1+(|O|-1)=|C|-M\le h-1,
\]

a contradiction.  Hence \(M=h+1\) and \(|O|=h\).

Every vertex of \(O\) must now be adjacent to all other \(h-1\) vertices
of \(O\) and to one vertex of \(L\).  Thus \(O\) is a clique and is
contained in a coordinate line \(L'\).  There are at least two cross-edges
between \(L\) and \(L'\).  An elementary coordinate check shows that two
coordinate lines with two cross-edges have their union in a coordinate
two-flat: if they vary in different coordinates, all fixed coordinates
outside those two must agree; if they are parallel, their fixed vectors
can differ in exactly one coordinate.  Consequently \(C=L\cup O\) varies
in at most two coordinates, again a contradiction.

### Every selected line has size at most \(h\)

Now (2)--(4) apply at every vertex.

For \(h\ge5\), every vertex has profile \((h-1,1)\).  Its \(h-1\)
neighbours lie with it on a unique selected coordinate line of size \(h\).
Every other vertex on that line has the same line as its unique
\((h-1)\)-direction.  These \(h\)-vertex lines therefore partition \(C\),
forcing \(h\mid |C|=2h+1\), which is impossible.

For \(h=4\), a vertex of profile \((2,2)\) makes (3) an equality.  The four
first-shell vertices need eight second-shell incidences, so all four
rectangle completions are present.  The nine vertices of \(C\) are exactly
a \(3\)-by-\(3\) coordinate grid, contained in a two-flat.  If no vertex
has profile \((2,2)\), all profiles are \((3,1)\); the preceding line
partition argument would force \(4\mid9\), impossible.

For \(h=3\), profile \((2,2)\) would force two second-shell rectangle
completions forming a matching between the two pairs of first-shell
vertices.  Each completion would then have degree only two.  Profile
\((1,1,1)\) similarly forces the three pairwise rectangle completions, each
again of degree only two.  Both contradict minimum degree three.  Hence
every vertex has profile \((2,1)\), and the line partition forces
\(3\mid7\), impossible.

Finally let \(h=2\).  Profile (4) makes every vertex have degree exactly
two.  Since \(C\) is connected and has five vertices, it is a five-cycle.
Label each cycle edge by its changed Hamming coordinate.  Every coordinate
used by a closed walk must be changed at least twice.  Five edges can
therefore use at most two coordinate labels, so this cycle also lies in a
coordinate two-flat.

All cases contradict three-coordinate variation, proving (1).

## Structural meaning

Together with the preceding rigidity theorem, the small-order hierarchy is

\[
\begin{array}{c|c}
|C|\le2h-1 & C\text{ lies on a coordinate line},\\
|C|=2h & C\text{ nonlinear implies }C\cong K_h\square K_2,\\
|C|=2h+1 & C\text{ lies in a coordinate two-flat},\\
C\text{ varies in at least three coordinates} & |C|\ge2h+2.
\end{array}
\]

This is the first stability step beyond equality.  In the first-carry
partition problem, it shows that a nonlinear class consuming either of the
two smallest possible excess budgets cannot mix three minor coordinates.
The remaining \(2s-1\) boundary question is consequently two-dimensional
rather than an unrestricted three-box problem.

## Reproducibility and trust boundary

`verify_three_coordinate_core_gap.py` exhausts all subsets of eight small
Hamming hosts in dimensions two through four.  It computes induced minimum
degree and essential-coordinate support directly, checks the strongest
instance \(|C|\ge2\delta(C)+2\) for every three-coordinate core, hashes all
equality witnesses, and independently enumerates the shell profiles in (4).
It also verifies the six-cycle, cube, and \(3\)-by-\(3\) grid boundary
examples from coordinates.

Run with CPython 3.12 or later, standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_three_coordinate_core_gap.py \
  | diff -u expected_three_coordinate_core_gap_stdout.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_three_coordinate_core_gap.py
shasum -a 256 -c SHA256SUMS
```

Universal validity rests on the written shell, line, and coordinate-label
arguments plus the preceding global nonlinear-class theorem.  Exhaustive
computation is finite corroboration, not a proof of the universal claim.  It
uses no solver, floating point, randomness, network input, external data, or
omitted certificate.

The originating majority-colouring problem is Open Problem 2 of Bujtás,
Dettlaff, Furmańczyk, and Laskowska, *Majority C-coloring in Cartesian
products* (2026), <https://arxiv.org/abs/2608.27669>.  Targeted searches found
work on maximum degree in large induced Hamming subgraphs and general
induced-subgraph recognition, but no matching minimum-order versus essential-
dimension theorem.  Novelty is search-relative, not a priority claim.
