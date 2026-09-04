# Three-coordinate residue-slab composition

## A dimension-free modular composition lemma

Fix \(s\ge2\). Let

\[
B=[m_1]\times\cdots\times[m_d],
\qquad M=\prod_{i=1}^d m_i,
\]

and suppose \(B\) already has a partition into
\(\lfloor M/s\rfloor\) coordinate-line sets of size at least \(s\). Let
\(p\ge1\), and put

\[
\tau=M\bmod s,
\qquad c=p\bmod s.
\]

If \(c\tau<s\), then \(B\times[p]\) has an optimal coordinate-line
partition into \(\lfloor Mp/s\rfloor\) parts of size at least \(s\).

Indeed, write \(p=sv+c\) and \(M=sQ+\tau\). On every new-coordinate
line, partition the first \(sv\) cells into \(v\) exact \(s\)-sets. In each
of the last \(c\) layers use a copy of the given \(Q\)-part partition of
\(B\). The resulting number of parts is \(vM+cQ\), while

\[
Mp=s(vM+cQ)+c\tau.
\]

The hypothesis makes this count \(\lfloor Mp/s\rfloor\), and the size bound
makes it optimal.

This lemma can be iterated. Starting with any optimal line-partitioned box,
one may append coordinates successively whenever the new side residue times
the current volume residue is less than \(s\). The criterion and construction
are invariant under adding multiples of \(s\) to the newly appended side.

## Optimal line partitions from an iterated modular remainder

Let \(s\ge 2\), let \(m,n\ge s\), and let \(p\ge1\). Put

\[
\tau=(mn)\bmod s,
\qquad
c=p\bmod s.
\tag{1}
\]

If

\[
\boxed{c\tau<s,}
\tag{2}
\]

then the three-dimensional Hamming box

\[
[m]\times[n]\times[p]
\]

has a partition into exactly

\[
\boxed{\left\lfloor\frac{mnp}{s}\right\rfloor}
\tag{3}
\]

sets, each contained in one coordinate line and having at least \(s\)
vertices.

### Direct construction

Write

\[
p=sv+c,
\qquad
mn=sQ+\tau,
\qquad 0\le c,\tau<s.
\tag{4}
\]

For every fixed pair in \([m]\times[n]\), partition the first \(sv\)
points of its coordinate-3 line into \(v\) consecutive \(s\)-sets. This
gives \(vmn\) line parts and leaves precisely the last \(c\) coordinate-3
layers.

In each remaining layer apply the cyclic rectangle theorem from
`CROSS_BOUNDARY_EXCHANGE.md`: since \(m,n\ge s\), the layer partitions into
\(Q=\lfloor mn/s\rfloor\) coordinate-line sets of size at least \(s\).
This gives another \(cQ\) parts. They are disjoint from the coordinate-3
parts and together cover the entire box. Finally,

\[
\begin{aligned}
mnp
  &=(sQ+\tau)(sv+c)\\
  &=s\bigl(vmn+cQ\bigr)+c\tau.
\end{aligned}
\tag{5}
\]

Condition (2) therefore gives

\[
vmn+cQ=\left\lfloor\frac{mnp}{s}\right\rfloor.
\]

The quotient is also an upper bound on the number of parts because every
part has at least \(s\) vertices, proving optimality. Equivalently, this is
the modular composition lemma applied to the cyclic optimal partition of
\([m]\times[n]\).

The point of (2) is that the third side itself has disappeared: only its
residue \(c\) interacts with the pair remainder \(\tau\). Thus complete
\(s\)-slabs are handled exactly before the cyclic two-coordinate exchange is
used. In particular, this strictly weakens the preceding layerwise condition
\(p\tau<s\).

## Four-dimensional Hamming consequence

Let

\[
G=K_{n_1}\mathbin\square K_{n_2}\mathbin\square
K_{n_3}\mathbin\square K_{n_4},
\qquad n_1\ge n_2\ge n_3\ge n_4\ge2,
\]

write \(N_i=n_i-1\), and put

\[
h=\left\lceil\frac{N_1+N_2+N_3+N_4}{2}\right\rceil,
\qquad
s=h-N_1+1.
\tag{6}
\]

Assume \(h\ge N_1\) and \(s\ge2\). Choose distinct
\(j,k,\ell\in\{2,3,4\}\), assume \(n_j,n_k\ge s\), and set

\[
\tau=(n_jn_k)\bmod s,
\qquad
c=n_\ell\bmod s.
\tag{7}
\]

If \(c\tau<s\), then

\[
\boxed{
\overline\chi_{\ge}(G)
=\left\lfloor\frac{n_2n_3n_4}{s}\right\rfloor.
}
\tag{8}

Indeed, apply the theorem to the minor box and lift each of its line parts
through the complete first coordinate. Every vertex in a lifted part has at
least

\[
N_1+(s-1)=h
\]

same-coloured neighbours. This attains the quotient in (8). The matching
upper bound is the height-1925 first/second-shell class-size theorem, whose
second-shell condition is automatic for four ordered factors.

The earlier cyclic criterion was \(n_\ell\tau<s\). Since
\(c\le n_\ell\), it implies (7)--(8); the converse can fail whenever the
third minor order contains at least one complete \(s\)-slab.

## An infinite family in the genuinely three-residue range

For every integer \(k\ge2\), define

\[
G_k=
K_{3k+6}\mathbin\square K_{3k+2}\mathbin\square
K_{2k+3}\mathbin\square K_{2k+3}.
\tag{9}

The deficit sum is \(10k+10\), so

\[
h=5k+5,
\qquad
s=h-(3k+5)+1=2k+1.
\tag{10}

The minor residues modulo \(s\) are

\[
(k+1,2,2).
\]

For the pair \((n_2,n_3)\),

\[
\tau=2(k+1)\bmod(2k+1)=1,
\qquad
c=n_4\bmod s=2,
\]

and hence \(c\tau=2<s\). The theorem gives

\[
\boxed{
\overline\chi_{\ge}(G_k)=6k^2+19k+16.
}
\tag{11}

The exact division behind (11) is

\[
(3k+2)(2k+3)^2
=(2k+1)(6k^2+19k+16)+2.
\]

This family lies outside every preceding construction in this suite. Its
residue product is

\[
4(k+1)=2s+2,
\]

so it is outside the mixed-radix and one-box ranges and is not the cubic
\(s=3\) exception. No minor side or pair product is divisible by \(s\):
the pair residues are \(1,1,4\), all nonzero because \(s\ge5\). Since all
three minor orders are at least \(s\), every old layerwise product of a
positive pair remainder with the remaining order is at least \(s\). Thus
the prior cyclic criterion also fails in every coordinate order. At
\(k=2\), (9) gives

\[
\overline\chi_{\ge}
(K_{12}\square K_8\square K_7\square K_7)=78.
\]

## Trust and literature boundary

The universal statement rests on the explicit slab partition, the cyclic
rectangle theorem, and the exact identity (5). The accompanying checker
reconstructs bounded boxes cell by cell, verifies all parts and the exact
count, maps the new Hamming parameter region against every earlier criterion,
and checks (9)--(11) on a long exact range. It uses standard-library exact
integers, tuples, and sets only. The computation corroborates the proof; it
does not replace it.

There is a classical scope boundary for the underlying rectangle lemma.
Identifying \([m]\times[n]\) with the edges of \(K_{m,n}\), a line part is a
star. When \(s\mid mn\), the all-size-\(s\) case is the classical
complete-bipartite star-decomposition theorem of Yamamoto, Ikeda, Shige-eda,
Ushio, and Hamada, *On claw-decomposition of complete graphs and complete
bigraphs*, Hiroshima Math. J. 5 (1975), 33--42,
<https://doi.org/10.32917/hmj/1206136782>. Cameron and Horsley also record
this equivalence in their modern star-decomposition survey and extension,
<https://arxiv.org/abs/1807.10738>. The cyclic nondivisible rectangle
construction and the iterated residue condition (2) are the relevant new
candidate content here.

Bujtas, Dettlaff, Furmanczyk, and Laskowska, *Majority C-coloring in
Cartesian products* (2026), <https://arxiv.org/abs/2608.27669>, state the
coordinate-projection lower bounds used at height 1925 and ask for imbalanced
three- and four-dimensional Hamming values in Open Problem 2. Their source
does not state (2), (8), or the family (9)--(11). Targeted primary-source
searches found no matching statement. Novelty is search-relative, not a
historical-priority claim.
