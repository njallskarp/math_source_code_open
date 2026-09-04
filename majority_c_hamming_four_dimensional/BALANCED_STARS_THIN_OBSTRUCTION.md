# Balanced varying-star rectangles and a sharp thin-coordinate obstruction

## A balanced optimal partition of every large rectangle

Fix integers \(s\ge2\) and \(m,n\ge s\), and put

\[
q=\left\lfloor\frac{mn}{s}\right\rfloor,
\qquad t=mn\bmod s.
\]

Then the Hamming rectangle \([m]\times[n]\) has a partition into exactly
\(q\) coordinate-line parts such that

\[
\boxed{
q-t\text{ parts have size }s,
\qquad t\text{ parts have size }s+1.
}
\tag{1}
\]

Thus the size discrepancy is at most one. Identifying the cells with the
edges of \(K_{m,n}\), (1) is an explicit decomposition into stars whose
orders are the two consecutive values \(s\) and \(s+1\).

### Balanced cyclic corner

It is enough to strengthen the corner construction. Let

\[
M=s+a,\qquad N=s+b,\qquad 1\le a,b<s,
\]

and write

\[
ab=sq_0+t,\qquad 0\le t<s,\qquad L=b+q_0.
\tag{2}
\]

Select \(L\) columns. As in the original cyclic construction,
\(q_0\le a-1\), so \(L<s+b=N\). Put

\[
\rho=\max(0,t-L),\qquad \delta=t-\rho=\min(t,L).
\tag{3}
\]

In exactly \(\rho\) rows mark \(b-1\) selected columns, and in each of the
other \(M-\rho\) rows mark \(b\) selected columns. Make the marks by taking
one globally consecutive sequence of residues modulo \(L\): maintain a
cursor, mark the next \(b-1\) or \(b\) residues in the current row, and then
advance the cursor by that row's mark count. Each row has distinct marks
because both possible counts are at most \(b\le L\).

The complement of the marks in a row is a row part. Hence exactly \(\rho\)
row parts have size \(s+1\), and all other row parts have size \(s\). The
total number of marks is

\[
Mb-\rho=(s+a)b-\rho=s(b+q_0)+t-\rho=sL+\delta.
\tag{4}
\]

Because the marks were consecutive modulo \(L\), each selected column
contains \(s\) or \(s+1\) marks, and exactly \(\delta\) selected columns
contain \(s+1\). These marked columns are the remaining parts. The corner
therefore has \(M+L=\lfloor MN/s\rfloor\) parts, and the number of size
\(s+1\) parts is

\[
\rho+\delta=t=MN\bmod s.
\]

For general \(m,n\), write \(m=su+a\), \(n=sv+b\). If either residue is
zero, use exact \(s\)-blocks along that coordinate. Otherwise strip the
first \((u-1)s\) rows into column \(s\)-sets and the first \((v-1)s\)
columns of the remaining rows into row \(s\)-sets. Apply the balanced
construction above to the remaining \((s+a)\)-by-\((s+b)\) corner. Every
stripped part has size \(s\), while the corner residue \(ab\bmod s\) equals
\(mn\bmod s\). This proves (1).

## Exact theorem for a thin third coordinate

Let \(m,n\ge s\ge2\) and \(1\le p<s\). Among all partitions of

\[
[m]\times[n]\times[p]
\]

into coordinate-line parts of size at least \(s\), the maximum number of
parts is exactly

\[
\boxed{
L_s(m,n,p)=p\left\lfloor\frac{mn}{s}\right\rfloor.
}
\tag{5}
\]

Indeed, a coordinate-3 line has only \(p<s\) cells and cannot contain a
legal part. Every legal line part is therefore contained in one fixed
coordinate-3 layer. The volume bound in each layer gives at most
\(\lfloor mn/s\rfloor\) parts, proving the upper bound in (5). Repeating
the balanced rectangle partition independently in all \(p\) layers attains
it.

If \(\tau=mn\bmod s\), comparison with the global volume quotient gives the
exact deficit

\[
\boxed{
\left\lfloor\frac{mnp}{s}\right\rfloor-L_s(m,n,p)
=\left\lfloor\frac{p\tau}{s}\right\rfloor.
}
\tag{6}
\]

In particular, an optimal quotient-sized line partition exists if and only
if \(p\tau<s\). This proves necessity, not merely sufficiency, for the
thin-coordinate range of the residue-slab condition.

There is also a useful boundary-crossing consequence. Write an arbitrary
third side as \(P=sv+c\), where \(0<c<s\). Split the box into its first
\(sv\) layers and last \(c\) layers. If a line partition has no part meeting
both regions, the volume bound on the first region and (5) on the second give
at most

\[
v mn+c\left\lfloor\frac{mn}{s}\right\rfloor
\tag{7}
\]

parts. When \(c\tau\ge s\), (7) is strictly smaller than
\(\lfloor mnP/s\rfloor\). Therefore every quotient-sized line partition in
that carry range must contain a coordinate-3 part crossing the chosen
complete-slab/residual-layer boundary. The missing carry cannot be repaired
inside the residual layers alone.

## A uniform Hamming obstruction beyond line lifting

For every \(s\ge3\), consider

\[
G_s=K_{s+2}\mathbin\square K_{s+2}\mathbin\square
K_{s+1}\mathbin\square K_{s-1}.
\tag{8}
\]

The four coordinate deficits are \((s+1,s+1,s,s-2)\), so their sum is
\(4s\), the majority threshold is \(h=2s\), and the minor class threshold
is

\[
h-(s+1)+1=s.
\]

The minor box has sides \((s+2,s+1,s-1)\). Apply (5) to its first two
coordinates. Since

\[
(s+2)(s+1)=s(s+3)+2,
\]

every partition of the minor box into coordinate-line parts of size at
least \(s\) has at most

\[
(s-1)(s+3)=s^2+2s-3
\tag{9}

parts. But the volume quotient is

\[
\left\lfloor\frac{(s+2)(s+1)(s-1)}s\right\rfloor
=s^2+2s-2.
\tag{10}

Thus line lifting is short by exactly one for every member of (8).

Nevertheless the one-box residue theorem gives an optimal majority
\(C\)-colouring with the value in (10). The minor residues are
\((2,1,s-1)\); their product is \(2s-2\), which lies in \([s,2s)\), and
their sum is \(s+2\). Hence, after exact line blocks are stripped, the whole
residue box is one legal non-line colour class. Consequently

\[
\boxed{
\overline\chi_{\ge}(G_s)=s^2+2s-2,
}
\tag{11}
\]

but no optimal colouring of this family can be obtained solely by lifting a
partition of the minor box into coordinate-line parts. At \(s=3\), the
first example is \(K_5\square K_5\square K_4\square K_2\): its exact value
is \(13\), while every line-lift construction has at most \(12\) colours.

This separates two mechanisms cleanly. Cross-boundary line exchange is
necessary to realize a modular carry within the line-partition framework;
non-line residue classes can sometimes realize the Hamming optimum even when
such a line partition is impossible.

## Literature and trust boundary

The divisible special case \(s\mid mn\), where every star has order exactly
\(s\), is classical: Yamamoto, Ikeda, Shige-eda, Ushio, and Hamada, *On
claw-decomposition of complete graphs and complete bigraphs*, Hiroshima
Math. J. 5 (1975), 33--42,
<https://doi.org/10.32917/hmj/1206136782>.

Cameron and Horsley, *Decompositions of edge-colored multigraphs*,
<https://arxiv.org/abs/1807.10738>, give a general necessary-and-sufficient
flow criterion for decomposing a multigraph into prescribed stars with
prescribed centers. That result can subsume particular two-size instances
once suitable center data are supplied, but it does not state the universal
balanced family (1) or this cyclic certificate.

Hajebi and Javadi, *On the parameterized complexity of star decomposition*,
<https://arxiv.org/abs/2411.13348>, show that general varying-size star
decomposition remains parameterized-hard even for complete bipartite graphs.
The contribution here is deliberately narrower: an explicit construction
for the consecutive multiset forced by Euclidean division, together with
the sharp thin-coordinate and Hamming consequences (5)--(11). Lonc's 1992
varying-star result concerns complete graphs rather than this stated
complete-bipartite family. Novelty is search-relative, not a claim of
historical priority.

The proof is elementary and universal. The accompanying standard-library
Python checker reconstructs bounded balanced partitions cell by cell,
checks the sharp thin-coordinate formulas, audits the boundary-crossing
deficit, and verifies the Hamming family both symbolically and by explicit
one-box partitions. It uses exact integers and sets only. Computation checks
the construction and conventions; it does not establish the universal
theorems.
