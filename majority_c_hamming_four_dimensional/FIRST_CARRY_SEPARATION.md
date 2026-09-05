# Exact first-carry separation in the thin Hamming range

This note combines the one-box residue construction with the sharp
thin-coordinate line bound.  It classifies exactly when the standard
whole-tail completion works in the first modular-carry range and shows that
every admissible residue pattern occurs in an infinite family of ordered
four-dimensional Hamming graphs.

## First-carry classification

Fix integers

\[
s\ge 3,\qquad m,n\ge s,\qquad 2\le p<s,
\]

and write

\[
m=sA+r,\qquad n=sB+u,\qquad 1\le r,u<s.
\]

Put \(R=rup\), and assume \(R<2s\).  Sequentially strip exact
coordinate-line \(s\)-cliques in the first two coordinates.  This leaves the
tail

\[
T=[r]\times[u]\times[p]
\]

and exactly

\[
Q_0=\frac{mnp-R}{s}
\tag{1}
\]

line parts.

**Theorem 1 (first-carry one-box classification).**  Adding the whole tail
\(T\) as one further part gives a partition into
\(\lfloor mnp/s\rfloor\) sets of induced minimum degree at least \(s-1\) if
and only if

\[
s\le R<2s
\qquad\text{and}\qquad
r+u+p\ge s+2.
\tag{2}
\]

Whenever (2) holds, the maximum number of coordinate-line parts of size at
least \(s\) is exactly

\[
L_s(m,n,p)
=p\left\lfloor\frac{mn}{s}\right\rfloor
=\left\lfloor\frac{mnp}{s}\right\rfloor-1.
\tag{3}
\]

Thus (2) is a sharp region where one nonlinear residue-box part repairs the
unique modular carry, while no coordinate-line partition can repair it.

### Proof

Every vertex of \(T\) has induced degree

\[
(r-1)+(u-1)+(p-1)=r+u+p-3.
\tag{4}
\]

Consequently the whole tail is a legal part exactly when
\(r+u+p\ge s+2\).  Formula (1) follows by expanding
\((sA+r)(sB+u)p\).  Because \(R<2s\), adding one tail part reaches the
volume quotient exactly when \(R\ge s\).  This proves the equivalence.

For the separation, \(p\ge2\) and \(rup<2s\) imply \(ru<s\).  Hence

\[
mn\bmod s=ru
\]

and (2) gives

\[
\left\lfloor\frac{p(mn\bmod s)}s\right\rfloor
=\left\lfloor\frac{rup}s\right\rfloor=1.
\]

The sharp thin-coordinate theorem gives the first equality in (3), and its
exact deficit identity gives the second.  The result is structural: no
enumeration is used in the proof.

The restriction \(p\ge2\) is essential for separation.  For example,
\((s,r,u,p)=(4,3,2,1)\) has a legal first-carry tail, but
\(mn\bmod4=2\), so line parts already attain the quotient.  The degree
condition is also essential: \((4,2,1,2)\) has \(R=s\), but its tail has
minimum degree \(2<s-1\).

## A near-triangle embedding

The classification transfers to majority C-colourings without any search.
Let \(m\ge n\ge p\ge2\), assume \(p<s\) and \(n+p\ge2s\), and define

\[
n_1=m+n+p-2s,
\qquad
G=K_{n_1}\mathbin\square K_m\mathbin\square K_n\mathbin\square K_p.
\tag{5}
\]

Then \(n_1\ge m\), so the factor orders in (5) are nonincreasing.  If
\(N_i=n_i-1\) and

\[
h=\left\lceil\frac{N_1+N_2+N_3+N_4}{2}\right\rceil,
\]

direct substitution gives

\[
h=m+n+p-s-2,
\qquad h-N_1+1=s,
\qquad h-N_1=s-1.
\tag{6}
\]

Moreover

\[
(N_1+N_2)-h=m-s\ge0.
\]

Thus this is exactly the near-triangle regime with minor threshold \(s\),
including both side conditions \(N_1\le h\le N_1+N_2\) of the shell bound.

**Theorem 2 (universal residue-pattern realization).**  Suppose the residues
\(r=m\bmod s\), \(u=n\bmod s\), and the thin order \(p\) satisfy (2).  Then

\[
\overline\chi_{\ge}(G)
=\left\lfloor\frac{mnp}{s}\right\rfloor,
\tag{7}
\]

whereas every colouring obtained by lifting a coordinate-line partition of
the minor box has at most the right side of (7) minus one colours.

Indeed, lift every part of the partition in Theorem 1 through the complete
first coordinate.  Equations (4) and (6) show that each lifted vertex has at
least

\[
N_1+(s-1)=h
\]

same-coloured neighbours.  The near-triangle shell bound supplies the
matching quotient upper bound, proving (7), while (3) proves the line-lift
ceiling.

Every admissible residue pattern has infinitely many such realizations.  Up
to interchanging \(r,u\), assume \(r\ge u\), and for every \(q\ge2\) put

\[
\begin{aligned}
n_2&=sq+r,\\
n_3&=sq+u,\\
n_4&=p,\\
n_1&=2sq+r+u+p-2s.
\end{aligned}
\tag{8}
\]

Here (5) holds, and the ordering follows explicitly from

\[
n_1-n_2=s(q-2)+u+p>0,
\quad n_2-n_3=r-u\ge0,
\quad n_3-p=sq+u-p>0.
\]

Therefore

\[
\boxed{
\overline\chi_{\ge}
\left(K_{n_1}\square K_{n_2}\square K_{n_3}\square K_p\right)
=spq^2+pq(r+u)+1,
}
\tag{9}
\]

while the exact line-lift ceiling is \(spq^2+pq(r+u)\).  The smallest
admissible residue pattern is \((s,r,u,p)=(3,2,1,2)\); (8) at \(q=2\)
gives

\[
\overline\chi_{\ge}(K_{11}\square K_8\square K_7\square K_2)=37,
\]

versus line-lift ceiling \(36\).

## Source, novelty, and trust boundary

The primary problem source is Bujtás, Dettlaff, Furmańczyk, and Laskowska,
*Majority C-coloring in Cartesian products* (2026),
<https://arxiv.org/abs/2608.27669>, whose Open Problem 2 asks for imbalanced
three- and four-dimensional Hamming graphs.  The paper does not state
Theorems 1--2 or the residue-pattern family (8)--(9).

The one-box construction is proved in `RESIDUE_BOX_EXTENSION.md`; the sharp
thin-coordinate maximum is proved in `BALANCED_STARS_THIN_OBSTRUCTION.md`;
and the majority-C upper bound is proved in
`NEAR_TRIANGLE_FOUR_DIMENSIONAL.md`.  The candidate-new content here is the
iff intersection of those mechanisms, its exact nonlinear-versus-line
separation, and the universal embedding of every admissible residue pattern.
Novelty is search-relative, not a priority claim.

The accompanying CPython checker uses only exact integer and set operations.
It exhausts the bounded residue domain, checks the algebra and embeddings,
constructs bounded partitions cell by cell, and rejects three sharp boundary
mutations.  These computations audit the definitions and implementation;
the universal claims rest on the displayed proofs and the cited prerequisite
theorems.
