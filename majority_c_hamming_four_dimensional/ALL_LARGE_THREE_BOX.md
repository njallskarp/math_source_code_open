# Transversal star alignment eliminates every carry in large three-boxes

## Anchored balanced rectangles

Fix integers \(s\ge2\) and \(m,n\ge s\), and put

\[
Q=\left\lfloor\frac{mn}{s}\right\rfloor,
\qquad \tau=mn\bmod s.
\]

The balanced rectangle theorem can be strengthened as follows.

**Anchored rectangle lemma.** The rectangle \([m]\times[n]\) has a
partition into \(Q\) coordinate-line parts, all of size \(s\) or \(s+1\),
such that:

1. exactly \(\tau\) parts have size \(s+1\);
2. all \(\tau\) larger parts are parallel column parts; and
3. one row meets every larger part, in \(\tau\) distinct cells.

When \(\tau>0\), the set of columns occupied by the larger parts may be
cyclically shifted within a common block of at least \(s\) columns.

### Construction in the final corner

Exact \(s\)-strips reduce the problem to a corner

\[
M=s+a,\qquad N=s+b,\qquad 1\le a,b<s.
\]

Write

\[
ab=sq+\tau,qquad 0\le\tau<s.
\tag{1}
\]

Since \(ab<as\), we have \(q\le a-1\). Divide the \(M\) rows into

\[
x=a+q\quad\hbox{sparse rows},
\qquad f=s-q\quad\hbox{full rows}.
\tag{2}
\]

In each full row, mark all \(N\) cells. Across the sparse rows, mark \(b\)
cells per row, taking one globally consecutive cyclic sequence modulo
\(N\). The complement of the marks in each sparse row is a row part of size
\(N-b=s\); full rows leave no row part.

The number of sparse-row marks is

\[
xb=(a+q)b=ab+qb=q(s+b)+\tau=qN+\tau.
\tag{3}
\]

Thus exactly \(\tau\) columns receive \(q+1\) sparse marks, and every other
column receives \(q\). After the \(f=s-q\) full-row marks are included, the
column parts have size \(s+1\) in exactly \(\tau\) columns and size \(s\) in
all other columns. Every column part contains every full row, so any one of
those rows is a common transversal. There is at least one such row because
\(q\le a-1<s\).

The total number of parts is

\[
x+N=a+q+s+b
=\left\lfloor\frac{(s+a)(s+b)}s\right\rfloor.
\]

Relabeling the \(N\) corner columns cyclically moves the \(\tau\) larger
column parts to any desired cyclic interval. Reattaching the exact strips
proves the lemma.

## Optimal balanced line partitions of every large three-box

**Theorem.** For all integers

\[
m,n,p\ge s\ge2,
\]

the Hamming box \([m]\times[n]\times[p]\) partitions into exactly

\[
\boxed{\left\lfloor\frac{mnp}{s}\right\rfloor}
\tag{4}
\]

coordinate-line parts of size at least \(s\). More precisely, every part
has size \(s\) or \(s+1\), and exactly \(mnp\bmod s\) parts have size
\(s+1\).

### Cross-slab carry exchange

Write

\[
p=sv+c,\qquad mn=sQ+\tau,
\qquad 0\le c,\tau<s.
\tag{5}
\]

First partition the initial \(sv\) points on every coordinate-3 line into
\(v\) exact \(s\)-sets. In each of the final \(c\) layers, use an anchored
balanced rectangle partition. Use the same transversal row in all layers,
and cyclically shift the larger-column interval: enumerate the
\(c\tau\) larger residual parts by

\[
h=\ell\tau+r,qquad
0\le\ell<c,\quad0\le r<\tau,
\]

and put the part indexed by \(h\) in corner column \(h\bmod N\), where the
common corner width satisfies \(N\ge s\).

Set

\[
k=\left\lfloor\frac{c\tau}{s}\right\rfloor,
\qquad r_0=c\tau-ks.
\tag{6}
\]

For each \(g=0,\ldots,k-1\), use the \(s\) residual parts indexed by
\(h=gs,\ldots,(g+1)s-1\). Their columns are distinct, because they are
\(s\) consecutive residues modulo \(N\ge s\). From each of these size
\(s+1\) parts, remove its cell on the common transversal row and donate that
cell to the initial coordinate-3 \(s\)-part at the same base position. From
each receiving coordinate-3 part, remove instead its cell in layer \(g\).
The receiving part loses and gains equally many cells and remains a
coordinate-3 part of size \(s\). The \(s\) displaced cells lie in one row
in layer \(g\), in distinct columns, and form one new size-\(s\) part.

These exchanges are compatible even when a base column recurs in different
groups: group \(g\) uses a different initial layer, and

\[
k\le\left\lfloor\frac{(s-1)^2}{s}\right\rfloor=s-2<s.
\]

Each exchange creates one part and consumes exactly \(s\) of the original
size-\(s+1\) residual parts. The final number of parts is

\[
vmn+cQ+k
=\left\lfloor\frac{mnp}{s}\right\rfloor,
\]

by (5)--(6). Exactly \(r_0=mnp\bmod s\) unconsumed larger parts remain.
This proves (4) and the balanced size profile.

The theorem complements the sharp thin-coordinate obstruction: if two
sides are at least \(s\) but the third is smaller than \(s\), the exact line
optimum can be below the volume quotient. The presence of just one complete
\(s\)-slab in the third direction is sufficient to absorb every modular
carry.

## Four-dimensional majority C-colouring consequence

Let

\[
G=K_{n_1}\mathbin\square K_{n_2}\mathbin\square
K_{n_3}\mathbin\square K_{n_4},
\qquad n_1\ge n_2\ge n_3\ge n_4\ge2,
\]

write \(N_i=n_i-1\), and put

\[
h=\left\lceil\frac{N_1+N_2+N_3+N_4}{2}\right\rceil,
\qquad s=h-N_1+1.
\tag{7}
\]

Assume \(h\ge N_1\), \(s\ge2\), and

\[
\boxed{n_4\ge s.}
\tag{8}
\]

Then all three minor sides are at least \(s\), so (4) partitions the minor
box into \(\lfloor n_2n_3n_4/s\rfloor\) line parts. Lift every part through
the full first coordinate. Each lifted vertex has at least

\[
N_1+(s-1)=h
\]

same-coloured neighbours. Together with the first/second-shell upper bound,
this proves

\[
\boxed{
\overline\chi_{\ge}(G)
=\left\lfloor\frac{n_2n_3n_4}{s}\right\rfloor.
}
\tag{9}

Thus the unresolved line-partition region is confined sharply to the case
where at least one minor side is thinner than the class threshold.

## An infinite first-carry family beyond all earlier residue criteria

For every integer \(k\ge3\), put

\[
s=k^2-k
\]

and define

\[
G_k=K_{k^2+2k}\mathbin\square
K_{k^2}\mathbin\square K_{k^2}\mathbin\square K_{k^2}.
\tag{10}

The deficit sum is \(4k^2+2k-4\), so

\[
h=2k^2+k-2,
\qquad h-(k^2+2k-1)+1=k^2-k=s.
\]

Every minor order is \(k^2=s+k\), hence is at least \(s\), with residue
\(k\). For every choice of a base pair,

\[
(k^2\cdot k^2)\bmod s=k,
\qquad k\cdot k=k^2,
\qquad s\le k^2<2s.
\]

So this is uniformly in the first carry range: the height-2023 slab
condition fails in every coordinate order by exactly one carry. The residue
product \(k^3\ge2s\), so the mixed-radix and one-box criteria also fail, and
there is no divisible minor side or pair. Theorem (9) nevertheless gives

\[
\boxed{
\overline\chi_{\ge}(G_k)
=\left\lfloor\frac{k^6}{k^2-k}\right\rfloor
=k^4+k^3+k^2+k+1.
}
\tag{11}

At \(k=3\), this says

\[
\overline\chi_{\ge}(K_{15}\square K_9\square K_9\square K_9)=121.
\]

## Trust and literature boundary

The proof is the explicit anchored rectangle construction, the exact carry
identity (6), and the local three-line exchange. No finite search establishes
the universal result.

The accompanying standard-library Python checker reconstructs bounded
anchored rectangles and three-box partitions cell by cell; checks line
containment, disjointness, coverage, sizes, anchors, every exchange, quotient
counts, and the balanced profile; maps the new Hamming parameter region
against every preceding criterion in this suite; and verifies (10)--(11) on
a long exact range. Exact integers, tuples, lists, and sets are used. The
computation corroborates the construction and conventions rather than
replacing the proof.

Under the identification of a three-box with the hyperedges of the complete
three-partite three-uniform hypergraph, a coordinate-line part fixes two
vertices and varies the third. The rectangle ingredient is a graph
star-decomposition. Its divisible uniform-size special case is classical:
Yamamoto et al., *On claw-decomposition of complete graphs and complete
bigraphs* (1975), <https://doi.org/10.32917/hmj/1206136782>. Cameron and
Horsley, *Decompositions of complete multigraphs into stars of varying
sizes*, <https://arxiv.org/abs/1807.10738>, give general graph
varying-star criteria; Hajebi and Javadi,
*Parameterized Complexity of the Star Decomposition Problem*,
<https://arxiv.org/abs/2411.13348>, treat the broader algorithmic problem.

The graph-theoretic target is Open Problem 2 of Bujtás, Dettlaff,
Furmańczyk, and Laskowska, *Majority C-coloring in Cartesian products*,
<https://arxiv.org/abs/2608.27669>, which asks for the three- and
four-dimensional imbalanced Hamming cases. Their stated results and bounds do
not include the all-large-minor quotient formula (9).

Targeted searches for decompositions of complete multipartite uniform
hypergraphs, multidimensional arrays, and Cartesian boxes into variable
coordinate lines found no matching anchored carry-exchange theorem. The
candidate-new claim is the explicit three-dimensional construction and its
Hamming consequence; novelty remains search-relative, not a historical
priority claim.
