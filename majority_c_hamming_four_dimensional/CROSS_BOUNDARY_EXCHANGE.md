# Cyclic cross-boundary exchange in two minor coordinates

## Optimal line partition of every large rectangle

Let \(s\ge2\) and \(m,n\ge s\).  The Hamming rectangle

\[
[m]\times[n]=V(K_m\mathbin\square K_n)
\]

can be partitioned into

\[
\boxed{\left\lfloor\frac{mn}{s}\right\rfloor}
\tag{1}
\]

sets, each contained in one coordinate line and having at least \(s\)
vertices.  Since every such set has size at least \(s\), the number in (1)
is optimal among partitions with that property.

### The cross-boundary corner switch

First consider a corner of size

\[
M\times N=(s+a)\times(s+b),
\qquad 1\le a,b<s.
\]

Write

\[
ab=sq+t,\qquad 0\le t<s,
\qquad L=b+q.
\tag{2}
\]

Select \(L\) of the \(N\) columns.  This is possible: \(b<s\) gives
\(q=\lfloor ab/s\rfloor\le a-1\le s-2\), hence
\(L=b+q<s+b=N\).  Index the \(M\) rows by
\(i=0,\ldots,M-1\) and the selected columns by
\(0,\ldots,L-1\).  In row \(i\), mark the \(b\) cells in columns

\[
ib,ib+1,\ldots,ib+b-1\pmod L.
\tag{3}
\]

They are distinct because \(b\le L\).  Make the unmarked cells of each row
one part.  Each row part has

\[
N-b=s
\]

vertices.

Now make the marked cells in each selected column one further part.  As \(i\)
and the offset in (3) vary, the marked cells correspond consecutively to

\[
0,1,\ldots,Mb-1
\]

reduced modulo \(L\).  Thus their column sizes differ by at most one.  From
(2),

\[
Mb=(s+a)b=sb+ab=s(b+q)+t=sL+t,
\]

so every marked column has at least \(\lfloor Mb/L\rfloor\ge s\) cells.
The corner is therefore partitioned into

\[
M+L=s+a+b+\left\lfloor\frac{ab}{s}\right\rfloor
=\left\lfloor\frac{(s+a)(s+b)}s\right\rfloor
\tag{4}
\]

legal line sets.  This is the promised cross-boundary exchange: every row
gives \(b\) boundary cells to a cyclic family of column parts, while retaining
exactly \(s\) cells.

### Reduction of a general rectangle to the corner

Write

\[
m=su+a,\qquad n=sv+b,
\qquad u,v\ge1,\quad 0\le a,b<s.
\]

If \(a=0\) or \(b=0\), partition along the corresponding divisible
coordinate.  Otherwise:

1. In the first \((u-1)s\) rows, take \(u-1\) vertical \(s\)-sets in every
   column.
2. In the remaining \(s+a\) rows and first \((v-1)s\) columns, take
   \(v-1\) horizontal \(s\)-sets in every row.
3. Apply (2)--(4) to the remaining \((s+a)\times(s+b)\) corner.

The parts are disjoint and cover the rectangle.  Their number is

\[
(u-1)n+(s+a)(v-1)
+s+a+b+\left\lfloor\frac{ab}{s}\right\rfloor
=suv+ub+av+\left\lfloor\frac{ab}{s}\right\rfloor,
\]

which is exactly \(\lfloor mn/s\rfloor\).  This proves (1).

## Pair-remainder exactness for four-dimensional Hamming graphs

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
\]

Assume \(h\ge N_1\) and \(s\ge2\).  Choose distinct
\(j,k,\ell\in\{2,3,4\}\) and assume

\[
n_j\ge s,\qquad n_k\ge s.
\tag{5}
\]

Let

\[
\tau=(n_jn_k)\bmod s.
\]

If

\[
\boxed{n_\ell\tau<s,}
\tag{6}

then

\[
\boxed{
\overline\chi_{\ge}(G)
=\left\lfloor\frac{n_2n_3n_4}{s}\right\rfloor .
}
\tag{7}

Indeed, write \(n_jn_k=sQ+\tau\).  In every fixed coordinate-\(\ell\)
layer, apply the rectangle theorem to obtain \(Q\) minor line parts of size
at least \(s\).  Across all \(n_\ell\) layers this gives \(n_\ell Q\) parts,
and (6) says

\[
n_\ell Q
=\left\lfloor\frac{n_\ell(sQ+\tau)}s\right\rfloor.
\]

Lift every minor line part through the whole first coordinate.  A lifted
vertex has at least

\[
N_1+(s-1)=h

\]

same-coloured neighbours.  The construction therefore attains the right side
of (7).  The reverse inequality is the first/second-shell class-size bound
from `NEAR_TRIANGLE_FOUR_DIMENSIONAL.md`.

In particular, (7) holds whenever

\[
s\mid n_jn_k
\tag{8}

\]

and (5) holds.  Condition (8) can hold although \(s\) divides neither factor;
this is a genuinely pairwise divisibility phenomenon not covered by the
earlier single-coordinate divisibility theorem.

## An infinite family beyond the multi-box barrier

For every integer \(k\ge2\), put \(s=k^2\) and define

\[
G_k=
K_{k^2+2k+3}\mathbin\square
K_{k^2+k}\mathbin\square
K_{k^2+k}\mathbin\square
K_{k^2+2}.
\tag{9}

The orders are nonincreasing.  Their deficits sum to

\[
4k^2+4k+1,
\]

so

\[
h=2k^2+2k+1,
\qquad h-(n_1-1)+1=k^2=s.
\]

The second and third factor orders are both at least \(s\), neither is
divisible by \(s\), but

\[
(k^2+k)^2=k^2(k+1)^2

\]

is divisible by \(s\).  Thus (7) gives

\[
\boxed{
\overline\chi_{\ge}(G_k)=(k+1)^2(k^2+2).
}
\tag{10}

All three minor residues modulo \(s\) are \((k,k,2)\), whose product is

\[
2k^2=2s.
\]

Hence this family lies exactly in the first \(s\ge4\) multi-box range.  The
height-1965 obstruction proves that the isolated residue box cannot be split
into its two quotient parts; the cyclic row--column switch succeeds because
it exchanges cells across the stripped-block boundary.  For \(k=2\), (9)
is \(K_{11}\square K_6\square K_6\square K_6\) and (10) equals \(54\).

## Trust and literature boundary

The theorem is the explicit cyclic construction (3), the exact count (4),
and the layer/lift calculation.  No finite search establishes any universal
claim.

The accompanying standard-library Python checker constructs every bounded
partition cell by cell, verifies disjointness, coverage, line containment,
minimum sizes, the exact quotient, the four-dimensional criterion, lifted
majority degree, and a long initial range of (9)--(10).  It uses exact integer
arithmetic only; these checks corroborate the proof and conventions rather
than replace them.

The primary literature boundary remains Bujtas, Dettlaff, Furmanczyk, and
Laskowska, *Majority C-coloring in Cartesian products* (2026),
<https://arxiv.org/abs/2608.27669>.  Its author source was inspected directly
on 2026-09-04.  Proposition 15 gives coordinate-projection lower bounds and
Open Problem 2 asks for imbalanced three- and four-dimensional Hamming graphs;
it does not state the cyclic rectangle partition, pair-remainder criterion
(6), or family (9)--(10).  Targeted primary-source searches found no matching
statement.  Novelty is search-relative, not a historical-priority claim.
