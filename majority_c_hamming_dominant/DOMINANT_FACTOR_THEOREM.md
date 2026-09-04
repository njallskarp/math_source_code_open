# Dominant-factor theorem

## Statement

For `d >= 2`, let

\[
G=K_{n_1}\mathbin\square K_{n_2}\mathbin\square\cdots
  \mathbin\square K_{n_d},
\qquad n_1\ge n_2\ge\cdots\ge n_d\ge2.
\]

Put \(N_i=n_i-1\), \(S=\sum_{i=2}^dN_i\),
\(D=N_1+S\), and \(h=\lceil D/2\rceil\).  Thus \(G\) is
\(D\)-regular, and a colour class is legal exactly when its induced subgraph
has minimum degree at least \(h\).

**Theorem.** If

\[
N_1\ge S+2,
\tag{1}
\]

then

\[
\overline\chi_{\ge}(G)=\prod_{i=2}^d n_i.
\tag{2}
\]

If additionally \(d\ge3\), every colouring attaining (2) has, up to colour
names, precisely the fibres

\[
[n_1]\times\{(x_2,\ldots,x_d)\}
\]

as its colour classes.

Condition (1) is equivalent to \(h<N_1\).  For three factors, it is therefore
exactly the strongly imbalanced range complementary to the near-triangle range
\(h\ge N_1\).

## A shell inequality

Let \(C\) be any colour class in a majority C-colouring and fix \(v\in C\).
For each coordinate
\(i\), let \(a_i\) count the vertices of \(C\) on the coordinate-\(i\) line
through \(v\), excluding \(v\).  The first shell contains
\(A=\sum_i a_i\ge h\) vertices of \(C\).

A first-shell vertex in direction \(i\) already sees \(v\) and the other
\(a_i-1\) vertices in that line.  It must consequently see at least
\(h-a_i\) vertices of \(C\) in the second Hamming shell about \(v\).  Every
second-shell vertex is adjacent to at most two first-shell vertices.  Double
counting these incidences gives

\[
 |C|\ge
 1+A+\frac12\sum_{i=1}^d a_i(h-a_i).
\tag{3}
\]

This is a purely local inequality; vertices in more distant shells can only
increase \(|C|\).

## Every class has at least \(n_1\) vertices

Write \(\ell=\lfloor D/2\rfloor=D-h\), set \(a=a_1\), and put
\(b=\sum_{i=2}^d a_i\).  If the dominant fibre through \(v\) is not contained
in \(C\), choose a vertex \(w\) of that fibre outside \(C\).  The vertex \(w\)
has at most \(D-h=\ell\) neighbours of other colours, while it sees all
\(a+1\) vertices of \(C\) in the fibre.  Hence

\[
a\le\ell-1.
\tag{4}
\]

Also \(b\le S\), and \(a+b\ge h\).  Define

\[
g(t)=t+\frac{t(h-t)}2.
\]

Merging the minor-coordinate terms in (3) loses only nonnegative cross terms:

\[
\sum_{i=2}^d a_i(h-a_i)
=b(h-b)+2\sum_{2\le i<j\le d}a_i a_j
\ge b(h-b).
\]

Therefore

\[
|C|\ge Q(a,b):=1+g(a)+g(b),
\tag{5}
\]

on the domain

\[
h-S\le a\le\ell-1,
\qquad h-a\le b\le S.
\tag{6}
\]

The function \(g\) is concave.  For fixed \(a\), the minimum in \(b\) is at
\(b=h-a\) or \(b=S\).  On either resulting boundary, the expression is again
concave in \(a\).  It is thus enough to check the three corners

\[
(h-S,S),\qquad (\ell-1,h-\ell+1),\qquad(\ell-1,S).
\tag{7}
\]

Here is the complete endpoint check.

### Even \(D=2h\)

Now \(\ell=h\), \(N_1=2h-S\), and (1) gives \(h\ge S+1\).  At the first two
corners in (7), respectively,

\[
Q=1+h+S(h-S),
\qquad Q=2h.
\]

Their differences from \(n_1=N_1+1=2h-S+1\) are

\[
(S-1)(h-S),
\qquad S-1.
\]

At the third corner,

\[
Q-2h=\frac{(S-1)(h-S+1)}2\ge0.
\]

Thus a non-full-fibre class has \(|C|\ge n_1\); if \(d\ge3\), then
\(S\ge2\), so in fact \(|C|\ge n_1+1\).

### Odd \(D=2h-1\)

Now \(\ell=h-1\), \(N_1=2h-1-S\), and the parity in (1) strengthens the
bound to \(h\ge S+2\).  The first two corner values are

\[
Q=1+h+S(h-S),
\qquad Q=3h-3.
\]

Their differences from \(n_1=2h-S\) are

\[
(S-1)(h-S)+1,
\qquad h+S-3.
\]

At the third corner,

\[
Q-(3h-3)=\frac{(S-2)(h-S)}2\ge0.
\]

For \(d\ge3\), all three differences from \(n_1\) are at least three.
(When \(d=2\) and the domain (6) is empty, there is simply no
non-full-fibre case.)

If the fibre through \(v\) is contained in \(C\), then trivially
\(|C|\ge n_1\).  Together with the preceding cases, every legal colour class
has at least \(n_1\) vertices.

## Counting classes and classifying equality

The graph has \(n_1\prod_{i=2}^d n_i\) vertices.  Since each colour class has
at least \(n_1\) vertices, every majority C-colouring uses at most
\(\prod_{i=2}^d n_i\) colours.

Conversely, colour each full dominant fibre separately.  Every vertex then has
exactly \(N_1\ge h+1\) same-coloured neighbours, so this is a legal colouring
with \(\prod_{i=2}^d n_i\) colours.  This proves (2).

If \(d\ge3\) and equality holds, every class has exactly \(n_1\) vertices.
The strict form of the shell estimate excludes the non-full-fibre case.  Each
class therefore contains a full dominant fibre and, by its size, equals that
fibre.  This proves the equality classification.

## Relation to the open problem

Proposition 15(i) of Bujtas--Dettlaff--Furmanczyk--Laskowska gives the fibre
construction, hence the lower bound in (2), when the dominant factor degree is
at least the sum of the others.  It does not give the upper bound above.  Their
Open Problem 2 asks for the three- and four-dimensional imbalanced Hamming
cases.  The theorem settles all dimensions in the strict dominant range and,
in dimension three, joins the independently obtained near-triangle formula to
cover the remaining side of its parameter split.
