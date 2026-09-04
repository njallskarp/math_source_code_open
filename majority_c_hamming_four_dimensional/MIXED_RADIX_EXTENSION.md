# Mixed-radix line partitions and new exact Hamming families

## Box partition lemma

Let

\[
B=[m_1]\times\cdots\times[m_k]
\]

and let \(s\ge1\).  Suppose at least one \(m_i\) is at least \(s\), and put

\[
r_i=m_i\bmod s,\qquad R=\prod_{i=1}^k r_i.
\]

If \(R<s\), then \(B\) can be partitioned into

\[
\left\lfloor\frac{\prod_i m_i}{s}\right\rfloor
\]

sets, each of size at least \(s\) and contained in an axis-parallel line.

### Proof

Reorder the coordinates so that \(m_k\ge s\), and write

\[
m_i=sq_i+r_i,qquad 0\le r_i<s.
\]

Starting with coordinate 1, split its first \(sq_1\) levels into consecutive
blocks of \(s\) on every coordinate-1 line.  The cells not yet used form a
box whose first side has length \(r_1\).  In that residual box, do the same in
coordinate 2.  Continue through coordinate \(k-1\).

The remaining cells are disjoint coordinate-\(k\) lines of length \(m_k\).
Because \(q_k\ge1\), partition each such line into \(q_k\) sets: use
\(q_k-1\) sets of size \(s\), and one set of size \(s+r_k\).  (When
\(r_k=0\), all \(q_k\) sets have size \(s\).)

The number of sets constructed is

\[
Q=\sum_{j=1}^k
\left(\prod_{i<j}r_i\right)q_j
\left(\prod_{i>j}m_i\right).
\tag{1}
\]

Repeatedly expanding \(m_i=sq_i+r_i\) gives the exact telescoping identity

\[
\prod_{i=1}^k m_i=sQ+\prod_{i=1}^k r_i=sQ+R.
\tag{2}
\]

Since \(0\le R<s\), equation (2) says
\(Q=\lfloor\prod_i m_i/s\rfloor\).  Every constructed set is contained in
one coordinate line and has at least \(s\) elements, proving the lemma.

## Majority C-colouring corollary

Let

\[
G=K_{n_1}\square\cdots\square K_{n_d},
\qquad n_1\ge\cdots\ge n_d\ge2,
\]

write \(N_i=n_i-1\), and set

\[
h=\left\lceil\frac{\sum_iN_i}{2}\right\rceil,
\qquad s=h-N_1+1.
\]

Assume

\[
N_1\le h\le N_1+N_2
\tag{3}
\]

and

\[
\prod_{i=2}^d(n_i\bmod s)<s.
\tag{4}
\]

Then

\[
\boxed{
\overline\chi_{\ge}(G)
=
\left\lfloor
\frac{\prod_{i=2}^d n_i}{s}
\right\rfloor .
}
\tag{5}
\]

Indeed, (3) implies \(s\le n_2\), so the box lemma applies to the minor box
\(B=\prod_{i=2}^d[n_i]\).  For each line set \(L\) in its partition, use

\[
[n_1]\times L
\]

as one colour class.  Every vertex in that class has at least

\[
N_1+(|L|-1)\ge N_1+s-1=h
\]

same-coloured neighbours.  The construction therefore gives the lower bound
in (5).  The reverse bound follows from the first/second-shell inequality:
under (3), every majority-C colour class has at least \(n_1s\) vertices.  For
completeness, if \(a_i\) counts the same-coloured neighbours of a fixed class
vertex in direction \(i\), then

\[
|C|\ge1+\sum_i a_i+\frac12\sum_i a_i(h-a_i).
\]

At fixed \(\sum_i a_i\), capped majorization fills the ordered caps \(N_i\)
greedily.  Writing \(h=N_1+r\), its value at the first feasible profile
\((N_1,r,0,\ldots)\) is \((N_1+1)(r+1)=n_1s\); filling the rest of the second
cap changes this by

\[
(t-r)\left(1+\frac{N_1-t}{2}\right)\ge0,
\]

and every later filled coordinate contributes
\(t+t(h-t)/2\ge0\).  Thus \(|C|\ge n_1s\), giving the upper bound in (5).

For four factors, (3)'s upper inequality is automatic because

\[
N_1+N_2+N_3+N_4\le2(N_1+N_2).
\]

Hence (5) holds throughout the four-dimensional near-triangle region
\(h\ge N_1\) whenever

\[
(n_2\bmod s)(n_3\bmod s)(n_4\bmod s)<s.
\tag{6}
\]

Condition (6) strictly extends the previously recorded divisibility regime.
For example, every nondivisible instance with \(s=2\) has three odd minor
orders, so the residue product is \(1<2\) and (5) is exact.
In particular,

\[
\overline\chi_{\ge}
(K_5\square K_3\square K_3\square K_3)=13:
\]

here \(h=5\), \(s=2\), none of the three minor orders is divisible by
\(s\), and the construction partitions the \(27\)-point minor box into
thirteen line sets.

## Scope and trust boundary

The box lemma is dimension-free and uses only the exact mixed-radix identity
(2).  The Hamming corollary combines it with the displayed shell argument;
no finite computation enters the proof.

The accompanying standard-library Python checker reconstructs the partitions
cell by cell for bounded instances, checks disjointness, coverage, line
structure, class sizes, the exact count, and the lifted internal-degree
condition.  It also checks (2) on a larger parameter range.  These checks
audit the implementation and boundary cases; they do not prove the theorem.

The primary literature boundary remains Open Problem 2 of Bujtas, Dettlaff,
Furmanczyk, and Laskowska, *Majority C-coloring in Cartesian products* (2026),
<https://arxiv.org/abs/2608.27669>.  That source asks for imbalanced three- and
four-dimensional Hamming graphs but does not state the mixed-radix partition
lemma or condition (6).  Novelty is search-relative, not a priority claim.
