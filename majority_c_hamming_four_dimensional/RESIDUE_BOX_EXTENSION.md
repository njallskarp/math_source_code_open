# One-box residue absorption beyond the mixed-radix range

## Residue-box partition theorem

Let

\[
B=[m_1]\times\cdots\times[m_k],
\qquad m_i=sq_i+r_i,\qquad 0\le r_i<s,
\]

where \(s\ge1\).  Put

\[
R=\prod_{i=1}^k r_i.
\]

Assume

\[
s\le R<2s
\tag{1}
\]

and

\[
\sum_{i=1}^k r_i\ge s+k-1.
\tag{2}
\]

Then \(B\), viewed as the vertex set of the Hamming graph
\(K_{m_1}\square\cdots\square K_{m_k}\), can be partitioned into

\[
\left\lfloor\frac{\prod_i m_i}{s}\right\rfloor
\]

sets, each inducing minimum degree at least \(s-1\).

### Proof

Process the coordinates in any order.  In coordinate 1, take consecutive
\(s\)-sets from the first \(sq_1\) levels on every coordinate-1 line.  The
unused cells form a box with first side \(r_1\).  Repeat in this residual box
through coordinate \(k\).  Every set removed in this way is an
axis-parallel \(s\)-clique.

The final unused set is the residue box

\[
B_r=[r_1]\times\cdots\times[r_k].
\]

Condition (1) implies every \(r_i\) is positive.  Each vertex of \(B_r\) has
induced degree

\[
\sum_{i=1}^k(r_i-1)=\sum_{i=1}^k r_i-k\ge s-1
\]

by (2), so the whole residue box is one further legal set.

If \(Q_0\) is the number of removed \(s\)-cliques, the same mixed-radix
expansion as in the preceding result gives

\[
\prod_i m_i=sQ_0+R.
\]

By (1),

\[
Q_0+1=\left\lfloor\frac{\prod_i m_i}{s}\right\rfloor.
\]

Thus the line cliques together with \(B_r\) give the required partition.

## Four-dimensional Hamming corollary

Let

\[
G=K_{n_1}\square K_{n_2}\square K_{n_3}\square K_{n_4},
\qquad n_1\ge n_2\ge n_3\ge n_4\ge2,
\]

put \(N_i=n_i-1\),

\[
h=\left\lceil\frac{N_1+N_2+N_3+N_4}{2}\right\rceil,
\qquad s=h-N_1+1,
\]

and assume \(h\ge N_1\).  Write

\[
r_j=n_j\bmod s\quad(j=2,3,4),
\qquad R=r_2r_3r_4.
\]

If

\[
s\le R<2s
\qquad\text{and}\qquad
r_2+r_3+r_4\ge s+2,
\tag{3}
\]

then

\[
\boxed{
\overline\chi_{\ge}(G)
=
\left\lfloor\frac{n_2n_3n_4}{s}\right\rfloor .
}
\tag{4}
\]

Apply the residue-box theorem to the minor box.  Lift each of its parts
\(D\) to \([n_1]\times D\).  Since every vertex of \(D\) has at least
\(s-1\) neighbours inside \(D\), every lifted vertex has at least
\(N_1+s-1=h\) same-coloured neighbours.

The resulting number of colours is the right side of (4).  The reverse
inequality follows from the first/second-shell theorem proved in
NEAR_TRIANGLE_FOUR_DIMENSIONAL.md: every majority-C colour class has at least
\(n_1s\) vertices.  Its condition \(h\le N_1+N_2\) is automatic in four
dimensions because

\[
N_1+N_2+N_3+N_4\le2(N_1+N_2).
\]

This proves (4).  Conditions (3) are disjoint from the earlier
residue-product condition \(R<s\), so this is a genuine complementary
extension.

## Explicit infinite nondivisible family

For every integer \(s\ge3\), define

\[
G_s=
K_{2s+2}\square
K_{2s-1}\square
K_{s+2}\square
K_{s+1}.
\]

The factor orders are nonincreasing.  Their deficits sum to \(6s\), so

\[
h=3s,\qquad N_1=2s+1,\qquad h-N_1+1=s.
\]

The three minor residues modulo \(s\) are

\[
(s-1,2,1).
\]

Therefore

\[
R=2s-2,\qquad
s\le R<2s,\qquad
(s-1)+2+1=s+2.
\]

No minor order is divisible by \(s\), while (3) holds with equality in its
degree condition.  Consequently

\[
\boxed{
\overline\chi_{\ge}(G_s)=2s^2+5s
\qquad(s\ge3).
}
\tag{5}
\]

Indeed,

\[
\left\lfloor
\frac{(2s-1)(s+2)(s+1)}s
\right\rfloor
=2s^2+5s.
\]

The residue class is the two-coordinate rectangle
\([s-1]\times[2]\times[1]\), whose induced minimum degree is exactly
\((s-2)+1=s-1\).  This is the promised uniform two-coordinate rounding
mechanism.

## Trust and literature boundary

The proof uses exact Euclidean division, the displayed mixed-radix count, and
the regular degree of a Cartesian product of complete graphs.  No finite
search is used to establish the result.

The accompanying standard-library Python checker reconstructs bounded
partitions cell by cell, verifies the direct Hamming adjacency degrees, audits
the four-dimensional parameter conditions, and checks the displayed infinite
family symbolically for a long initial range.  Those checks corroborate the
construction and conventions but are not the proof.

The primary literature boundary remains Open Problem 2 of Bujtas, Dettlaff,
Furmanczyk, and Laskowska, *Majority C-coloring in Cartesian products* (2026),
<https://arxiv.org/abs/2608.27669>.  The authors ask for imbalanced
four-dimensional Hamming graphs but do not state the residue-box theorem,
condition (3), or family (5).  Novelty is search-relative.
