# A complete defect partition of the hard M=215 slice

All graphs are simple. Red edges form a graph G on 43 vertices, and blue
edges form its complement. Assume neither color contains K5. We import
R(4,5)=25 and the reviewed exact maxima

\[
(U(18),\ldots,U(24))=(85,92,100,107,114,122,132)
\]

for the number of edges in a (4,5) graph. For each vertex v, let d(v) be
its red degree, t_R(v) the red edges on its red neighborhood, and t_B(v)
the blue edges on its blue neighborhood. The **hard branch** means

\[
r(v)=U(d(v))-7-t_R(v)\geq0,\qquad
b(v)=U(42-d(v))-7-t_B(v)\geq0.
\]

These are integer excesses over deficiency seven; write s(v)=r(v)+b(v).
They are intrinsic vertex statistics, not freely imposed labels. Let
D be the vertices of type (d,r,b)=(21,0,0).

## Global coverage and the meaning of M

Every hypothetical Ramsey graph first has 18 <= d <= 24. Its 86 local
deficiencies are nonnegative. It falls into exactly one of the cases:
some local deficiency is at most six; or every local deficiency is at
least seven. The present result concerns the latter case only.

The reviewed triangle count gives

\[
2\Delta=1247-W,\quad
W=21(n_{18}+n_{24})+12(n_{19}+n_{23})+3(n_{20}+n_{22}).
\]

Hence W <= 43 in the hard branch. Handshaking makes the number of
even-degree vertices odd, so W is 3 modulo 6 and W <= 39. Orient colors
so red has fewer edges. Since W >= 3 sum_v |d(v)-21|, the red edge count
m lies in 445,...,451. Put M=m-231, giving all seven slices 214,...,220.

There are at most W/3 noncentral vertices and at most (43-W)/2 central
vertices with positive excess. Consequently

\[
|D|\geq43-W/3-(43-W)/2=(129+W)/6\geq22.
\]

At any u in D, its two neighborhoods have 21 vertices, 100 red edges
on its red side A, and 100 blue edges on its blue side B. There are 110
red edges inside B and 21 incident to u. Therefore the red A--B total
is m-231=M. Reanchoring at another element of D preserves M exactly.
In particular, no reanchoring maps the present slice into M=214.

## Three degree profiles, derived without a catalog of profiles

Now set M=215, so m=446 and sum_v(d(v)-21)=-11. Let P be the sum of
positive deviations, and let n_j count vertices of absolute deviation j.
The exact weight expression is

\[
W=33+6(P+n_2+2n_3)\leq39.
\]

Thus only the following profiles occur. E always denotes the degree-20
class and C the degree-21 class. A singleton of another degree is denoted z
or h. Profile names A,B,C below are names, not the anchor sides A,B above.

| Profile | Red degrees | W | Total excess | (sum r, sum b) |
|---|---|---:|---:|---|
| A | 20^11 21^32 | 33 | 5 | (2,3) or (5,0) |
| B | 19^1 20^9 21^33 | 39 | 2 | (1,1) |
| C | 20^12 21^30 22^1 | 39 | 2 | (2,0) |

The excess is Delta-86*7=(43-W)/2. The red and blue cap sums
(sum(U(d)-7), sum(U(42-d)-7)) are respectively
(4223,4377), (4222,4378), and (4223,4377). Subtracting each color's
excess must give three times an integer triangle count. This proves
the last column; it does not assume separate local sides are exact.

## Parity localizes the defects

Write a(v)=|N_R(v) intersect E|. Directly counting edges in the partition
{v}, N_R(v), N_B(v) gives, for every graph,

\[
t_R(v)+t_B(v)=\binom{42-d(v)}2-m+
\sum_{w\in N_R(v)}d(w).
\]

Substituting the caps gives the following exact identities. Let S_X be
the sum of s(v) over a class X.

**Profile A.** For every vertex s(v)=a(v)-5. Thus

\[
S_E=2e_R(E)-55\in\{1,3,5\},\qquad S_C=5-S_E\in\{4,2,0\}.
\]

In particular, not all excess can lie on central vertices. The internal
red edge totals of E are respectively 28,29,30.

**Profile B.** Let z have degree 19. Then

\[
s(z)=a(z)-6,\qquad
s(v)=a(v)+2\mathbf1_{vz\in R}-5\quad(v\ne z).
\]

Summing the latter over E gives

\[
S_E=2e_R(E)+2a(z)-45.
\]

This is odd, nonnegative and at most two, so S_E=1. Exactly one degree-20
vertex has excess one, and exactly one other vertex, in {z} union C,
has excess one. All remaining vertices have excess zero. Since the color
totals are (1,1), these are **different vertices with opposite excess
colors**. If the second vertex is z, a(z)=7 and e_R(E)=16. Otherwise
a(z)=6 and e_R(E)=17. This is four intrinsic cases: the second vertex
has degree 19 or 21, and the degree-20 defect is red or blue.

**Profile C.** Let h have degree 22. Then

\[
s(h)=a(h)-6,\qquad
s(v)=a(v)-\mathbf1_{vh\in R}-5\quad(v\ne h).
\]

Thus

\[
2e_R(E)=66+S_E+s(h),\qquad S_C\equiv0\pmod2.
\]

Both excess units are red. They lie either entirely in C or entirely in
E union {h}. The six cases are one excess-two vertex of degree 20,21,22,
or two excess-one vertices with degree pairs (20,20), (20,22), (21,21).
The E edge total is 33 when S_C=2 and 34 when S_C=0.

## Stronger exact-anchor bounds

The preceding localization gives the following lower bounds. Here
delta_R and delta_B are the minimum degrees in the two graphs induced on D.

| Profile | |D| at least | delta_R at least | delta_B at least |
|---|---:|---:|---:|
| A | 28 | 12 | 11 |
| B | 32 | 15 | 14 |
| C | 28 | 12 | 11 |

To see this directly, let q=|C\D|. In A, q <= S_C <= 4, and an exact
anchor has five red E neighbors. Among the other central vertices it has
16 red and 15 blue neighbors. Removing the q nonexact ones proves the row.

In B, q <= 1. If x indicates the red edge to z, an exact anchor has
5-2x red E neighbors, 16+x red C neighbors and 16-x blue C neighbors.
Subtract q to obtain the row.

In C, q <= 2. If x indicates the red edge to h, an exact anchor has
5+x red E neighbors, 16-2x red C neighbors and 13+2x blue C neighbors.
Again subtract q. These arguments apply to every element of D.

Therefore throughout the entire M=215 slice,

\[
28\leq |D|\leq33,\quad \delta_R\geq12,\quad\delta_B\geq11.
\]

For completeness, a (5,5) graph J with minimum degree at least nine is
connected. Otherwise, no component is complete, as a complete K5-free
component has maximum degree three. Each component therefore has an
independent pair. There can only be two components, and both must have
independence number two, since the component independence numbers sum to
at most four. But a vertex neighborhood in a K5-free, independence-two
component is a (4,3) graph, so R(4,3)=9 bounds its degree by eight,
a contradiction. Applying this after vertex deletions shows

\[
\kappa(G_R[D])\geq4,\qquad \kappa(G_B[D])\geq3.
\]

Both diameters are at most five: a geodesic of length six supplies three
pairwise disjoint closed neighborhoods, each of size at least 12, exceeding
|D| <= 33. These are guarantees, not sharpness assertions.

## The complete intrinsic partition and rooted refinement

A defect type is a triple (d,r,b) with r+b>0. An intrinsic key consists of
the profile name and the sorted multiset of its defect types. Nondefective
type counts are recovered from the degree profile.

In A, partition the total colored excess (2,3) or (5,0) into nonzero
integer pairs, assign each pair to degree class E or C, and require the
E total to be odd. This gives 54 and 18 keys, respectively. The previous
section gives four B keys and six C keys. Thus there are exactly
**82 keys**, split as 72,4,6. Every actual graph has a unique intrinsic
key, so these define disjoint classes covering the full slice. Some or
all of those classes may be empty; no realizability is asserted.

For any exact anchor u, the red-side degree capacities are:

| Profile | Singleton red indicator | Degree-19 count | Degree-20 count | Degree-21 count | Degree-22 count |
|---|---:|---:|---:|---:|---:|
| A | 0 | 0 | 5 | 16 | 0 |
| B | x in {0,1} | x | 5-2x | 16+x | 0 |
| C | x in {0,1} | 0 | 5+x | 16-2x | x |

The blue-side counts are the degree totals minus these counts and minus
the anchor. These are the five complete degree split types; neither
singleton edge color is assumed forced. Distribute the nonzero defect
types between the red and blue sides within these capacities. Identical
types are indistinguishable for this operation. The result is exactly
624 A keys, 24 B keys, and 26 C keys: **674 rooted keys**. All internal
side graphs and all unprescribed cross edges remain variable.

Here is an optional rule making the rooted cover a canonical partition
as well. For a fixed intrinsic key, list all its vertex types in increasing
lexicographic order. For each u in D, let k(u) be the vector of red-neighbor
counts by those types. Choose any u minimizing k(u) lexicographically.
This vector and the resulting rooted key are intrinsic under relabeling.
Tied vertices give the same key. Within each side, sort vertices by type;
put the chosen anchor at label 42, its red side at 0,...,20 and its blue
side at 21,...,41. Every graph admits this labeling. The 674 indices are
a superset of the potentially nonempty canonical cells; the count does
not certify 674 realizable minima.

## Exact composition with a finite formula

For each rooted key, impose the following finite Boolean constraints on
red-edge bits x_ij for all 903 unordered pairs. This is a mathematical
specification, not a generated or solver-tested backend.

1. For each five-set S, require 1 <= sum_{ij subset S} x_ij <= 9.
2. Assign vertex types by the labeling above. Require sum_j x_vj=d(v).
3. Define, for every triple T, R_T as the conjunction of its three edge
   bits and B_T as the conjunction of their three negations. Require
   sum_{T contains v} R_T=U(d(v))-7-r(v) and
   sum_{T contains v} B_T=U(42-d(v))-7-b(v).
4. Set all 42 anchor edges to the prescribed red and blue sides.
5. For the canonical version, impose k(42) <=_lex k(v) for every vertex
   whose fixed type is (21,0,0).

Conjunctions have their usual exact Boolean meaning; implications in
only one direction are insufficient. Clause 5 can be expressed without
a new symmetry assumption: if there are L types, encode k(v) by the
integer sum_{i=0}^{L-1} 44^(L-1-i) k(v)_i and compare these integers.
Every digit is at most 42, so this is exactly lexicographic order.

Any satisfying assignment, after forgetting auxiliary triple bits, is
a hard-branch Ramsey graph of degree sum 892 and hence M=215. Its true
local excesses are exactly its assigned types. Conversely, every graph
in this slice has a minimum-key exact anchor, a rooted key in the complete
list, and a labeling satisfying all five families. The triple bits are
uniquely determined by its edges. Therefore excluding all these complete
formulas would exclude the complete M=215 slice. A computation retaining
only fixed neighborhood graphs, selected common cores, or some mixed
clique clauses would require its own additional coverage proof.

This theorem supplies that precise composition interface. It supplies
no UNSAT certificates and closes no whole M slice.
