# Near-triangle upper bound in four-dimensional Hamming graphs

## Theorem

Let

\[
G=K_{n_1}\square K_{n_2}\square K_{n_3}\square K_{n_4},
\qquad n_1\ge n_2\ge n_3\ge n_4\ge2.
\]

Write \(N_i=n_i-1\),

\[
D=N_1+N_2+N_3+N_4,
\qquad h=\left\lceil\frac D2\right\rceil,
\]

and assume \(h\ge N_1\).  Put

\[
r=h-N_1,
\qquad s=r+1.
\]

Then every majority C-colouring of \(G\) satisfies

\[
\boxed{
\overline\chi_{\ge}(G)
\le
\left\lfloor\frac{n_2n_3n_4}{s}\right\rfloor .
}
\tag{1}
\]

If \(s\mid n_j\) for at least one \(j\in\{2,3,4\}\), then equality holds:

\[
\boxed{
\overline\chi_{\ge}(G)=\frac{n_2n_3n_4}{s}.
}
\tag{2}
\]

The same proof gives the following dimension-free formulation.  If
\(n_1\ge\cdots\ge n_d\ge2\), \(h=\lceil\sum_i(n_i-1)/2\rceil\), and

\[
N_1\le h\le N_1+N_2,
\]

then every colour class has at least

\[
n_1(h-N_1+1)
\]

vertices.  Consequently

\[
\overline\chi_{\ge}
\left(K_{n_1}\square\cdots\square K_{n_d}\right)
\le
\left\lfloor
\frac{\prod_{i=2}^d n_i}{h-N_1+1}
\right\rfloor,
\tag{3}
\]

with equality whenever \(h-N_1+1\) divides some minor order \(n_j\).
For four factors, the upper inequality \(h\le N_1+N_2\) is automatic.

## First/second-shell inequality

Let \(C\) be a colour class and fix \(v\in C\).  In direction \(i\), let
\(a_i\) count the same-coloured neighbours of \(v\).  Thus

\[
0\le a_i\le N_i,
\qquad A:=\sum_i a_i\ge h.
\]

A selected neighbour in direction \(i\) sees \(v\) and the other
\(a_i-1\) selected vertices on that coordinate line.  It therefore needs at
least \(h-a_i\) selected neighbours in the second Hamming shell around
\(v\).  Every second-shell vertex is adjacent to at most two first-shell
vertices.  Double counting gives

\[
|C|\ge
1+A+\frac12\sum_{i=1}^d a_i(h-a_i).
\tag{4}
\]

No assumption about farther shells is made; they only increase \(|C|\).

## Optimizing the shell bound

Set

\[
g(x)=x+\frac{x(h-x)}2.
\]

For fixed \(A\), the right side of (4) is

\[
1+\frac{A(h+2)}2-\frac12\sum_i a_i^2.
\]

It is minimized by maximizing \(\sum_i a_i^2\) subject to the ordered caps
\(a_i\le N_i\).  The greedy vector

\[
(N_1,N_2,\ldots,N_k,t,0,\ldots,0)
\]

does this: it majorizes every feasible capped vector, and the sum of squares
is Schur-convex.  Equivalently, repeated transfers from a later nonzero
coordinate into an earlier unfilled cap cannot decrease the sum of squares.

Write \(h=N_1+r\), where \(0\le r\le N_2\).  At \(A=h\), the greedy vector
is \((N_1,r,0,\ldots,0)\), and (4) becomes

\[
1+h+\frac12\{N_1r+rN_1\}
=(N_1+1)(r+1)=n_1s.
\tag{5}
\]

For \(A=N_1+t\) with \(r\le t\le N_2\), the excess over (5) is exactly

\[
(t-r)\left(1+\frac{N_1-t}{2}\right)\ge0.
\tag{6}
\]

After the second cap fills, adding \(t\) vertices in any later coordinate
changes the greedy lower bound by

\[
g(t)=t+\frac{t(h-t)}2\ge0,
\tag{7}
\]

because \(t\le N_i\le N_1\le h\).  Equations (5)--(7) cover every
\(A\ge h\), so every colour class has size at least \(n_1s\).  Counting all
vertices proves (1) and (3).

For four factors, it remains to justify \(r\le N_2\).  We have

\[
D=N_1+N_2+N_3+N_4\le2(N_1+N_2).
\]

If equality holds, \(D\) is even; otherwise taking a ceiling still gives
\(h\le N_1+N_2\).  Hence \(0\le r\le N_2\), as required.

## Construction in the divisibility regime

Suppose \(s\mid n_j\) for a minor coordinate \(j\ge2\).  Partition
\([n_j]\) into blocks of size \(s\).  For every block \(B\) and every fixed
choice of the remaining minor coordinates, make

\[
[n_1]\times B
\]

(with all other coordinates fixed) one colour class.  Each vertex has

\[
N_1+(s-1)=N_1+r=h
\]

same-coloured neighbours.  The construction partitions the graph into
\(\prod_{i=2}^d n_i/s\) legal classes, proving (2) and the equality assertion
after (3).

## Parameter map

For three factors, the domains of the two committed claims are complementary:

\[
h<N_1\iff N_1\ge N_2+N_3+2,
\]

while

\[
h\ge N_1\iff N_1\le N_2+N_3+1.
\]

There is therefore no uncovered integer triple between heights 1907 and 1485.
In four dimensions, height 1907 covers the first inequality with
\(N_2+N_3+N_4\) in place of \(N_2+N_3\).  The theorem above supplies a
universal upper bound throughout the complementary near-triangle region and
settles its divisibility subfamilies.  The residual exact-value problem is

\[
h\ge N_1,
\qquad
s=h-N_1+1,
\qquad
s\nmid n_j\quad\text{for every }j=2,3,4.
\]

## Literature and trust boundary

Bujtas, Dettlaff, Furmanczyk, and Laskowska, *Majority C-coloring in
Cartesian products* (2026), explicitly ask for the imbalanced three- and
four-dimensional Hamming cases in Open Problem 2.  Their Proposition 15 gives
coordinate-fibre lower bounds, not (1)--(3):
<https://arxiv.org/abs/2608.27669>.

The universal result rests on the elementary shell count and capped-concavity
optimization above.  The accompanying exact checker audits finite parameter
and graph instances only; it is not the proof.
