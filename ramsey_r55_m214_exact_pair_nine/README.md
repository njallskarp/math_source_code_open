# Codegree nine is forced throughout the \(M=214\) branch

## Coverage theorem

Every hypothetical Ramsey \((5,5;43)\) graph in the complete \(M=214\)
hard branch admits **red-adjacent doubly exact degree-21 anchors whose
common red neighborhood has between nine and thirteen vertices**.

This closes the codegree-eight *coverage exception* left by the
[five-family reanchoring theorem](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_reanchoring_cover),
source commit 11df9442ceb2f31de190dbc0e6fc840d33399e39,
Discovery Net height 3062,
bafkreihgosxypptt7tlcm32splqtkmsdjp5y3z3hl552qoslztvmodc4sy.
It does not exclude the partition family itself, or any full Ramsey branch.

The five-family cover remains valid, with all five partner ranges now
\(9..13\), provided the first anchor in the partition family is chosen
as an endpoint of the high-codegree edge proved below. We do **not**
prove that every preselected exact anchor has such a partner.
No ordering rows may be combined with an arbitrary partner-label pin
without the stabilizer argument already required in the earlier source.

## Intrinsic domain and the remaining family

The red graph \(G\) has no clique or independent set of size five.
Its degree classes \(E,C\) have sizes 13 and 30, with red degrees 20 and
21. Put \(a(v)=|N_R(v)\cap E|\). All \(a(v)\geq6\), and the red
neighborhood edge counts are 93 on \(E\), 100 on \(C\).
These are the full intrinsic hypotheses of the earlier \(M=214\)
formulation, not a selected core or profile.

Only the partition family needs a new argument. In that family
\(T=\{p,q\}\subset C\) are the two vertices with \(a=7\), all other
vertices have \(a=6\), the edge \(pq\) is blue, and

\[
X=C\setminus T=A\sqcup B,\qquad
A=N_R(p)\cap X,\quad B=N_R(q)\cap X,\qquad |A|=|B|=14.
\]

Every \(x\in X\) is doubly exact and red-adjacent to exactly one vertex
of \(T\). Thus \(G[E]\) is 6-regular on 13 vertices, and \(J=G[X]\)
is 14-regular on 28 vertices, with 196 edges.

## Lemma: ten triangles on the exceptional class

Any 6-regular graph \(F\) on 13 vertices with no independent five-set
has at least ten triangles.

For each vertex \(v\), its six neighbors induce at least two edges;
zero or one edge would leave an independent five-set. If the total number
of triangles were at most nine, some vertex would lie in exactly two.
Write \(P=N_F(v)\) and let \(Q\) be its six nonneighbors.
The two edges in \(P\) must be disjoint, since adjacent edges on six
vertices leave five independent vertices.

Regularity gives 26 edges between \(P,Q\), and exactly five edges in
\(Q\). Each endpoint of an edge in \(P\) has four neighbors in \(Q\).
Its two endpoints therefore have at least two common neighbors in \(Q\).
The two \(P\)-edges yield at least four triangles of type \(PPQ\).

The five-edge graph \(F[Q]\) cannot be a star, which would have an
independent five-set. Any five-edge simple graph that is not a star
has at least two unordered pairs of disjoint edges. Indeed, if all edges
pairwise meet, five of them must form a star. If there were exactly one
disjoint pair \(ab,cd\), the other three edges would each meet both and
therefore belong to \(\{ac,ad,bc,bd\}\); any three of these contain
another disjoint pair.

It follows that

\[
\sum_{z\in Q}d_Q(z)^2
=10+2\,\#\{\text{pairs of incident edges in }F[Q]\}\leq26.
\]

For an edge \(yz\) in \(Q\), the endpoints have respectively
\(6-d_Q(y)\), \(6-d_Q(z)\) neighbors in \(P\). The total number of
triangles of type \(PQQ\) is consequently at least

\[
\sum_{yz\in E(F[Q])}(6-d_Q(y)-d_Q(z))
=30-\sum_{z\in Q}d_Q(z)^2\geq4.
\]

Together with the two triangles containing \(v\), this gives at least
\(2+4+4=10\), a contradiction. Negative individual common-neighbor
lower bounds, if any, are still valid; only their sum is used.

## Signed triangle accounting on the partition family

Let the numbers of red triangles of types EEE, EEX, EXX, XXX, EET, EXT,
XXT be \(a,b,c,d,e,f,g\), respectively. No triangle has two vertices
of \(T\), since \(pq\) is blue. Summing local red triangle counts on
\(E\) and \(X\), and summing common red degree over edges of \(J\), gives

\[
S_E=3a+2b+c+2e+f=13\cdot93=1209,
\]

\[
S_X=b+2c+3d+f+2g=28\cdot100=2800,
\]

\[
D=\sum_{xy\in E(J)}|N_R(x)\cap N_R(y)|=c+3d+g.
\]

Eliminating terms yields the exact identity

\[
D=S_X-S_E+3a+b+2e-g=1591+3a+b+2e-g.
\]

The lemma gives \(a\geq10\). Every \(x\in X\) has six red neighbors
in \(E\), whose induced graph has at least two edges; hence \(b\geq56\).
Each vertex of \(T\) has seven red neighbors in \(E\), whose induced
graph has at least three edges; otherwise deleting an endpoint from
each of at most two edges leaves five independent vertices. Thus \(e\geq6\).

Finally \(g=e_R(A)+e_R(B)\). Each of \(G[A]\) and \(G[B]\) has no red
\(K_4\) (add its red-adjacent vertex in \(T\)) and no independent
five-set. The published extremal value \(U(14)=60\) gives \(g\leq120\).
Therefore

\[
D\geq1591+3\cdot10+56+2\cdot6-120
=1569>8\cdot196.
\]

At least one edge of \(J\) has common red degree at least nine. Both
endpoints are doubly exact. The upper bound 13 follows from
\(R(3,5)=14\), as in the earlier theorem.

This proves the claimed new coverage statement without enumerating
43-vertex profiles, choosing a common core, or solving a SAT instance.
The counting mechanisms are classical; no historical-priority claim is
made for the auxiliary inequalities. Independent review is pending.

## Primary catalog input and sensitivity

[McKay's primary Ramsey data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
states that the extrema archive provides complete sets at the smallest
and largest few edge counts for orders 4 through 23.
The order-14 members have levels 22, 23, 58, 59, 60, with the unique
level-60 graph recorded in certificate.json. Its graph6 string is checked
directly for order 14, 60 edges, no \(K_4\), and no independent five-set.

The upper bound 60 depends on the **published completeness assertion**,
not merely the existence of that graph. Reproducing the small witness or
checking an archive hash does not reprove the upstream classification.

The archive is
[r45extreme.tar.gz](https://users.cecs.anu.edu.au/~bdm/data/r45extreme.tar.gz),
SHA-256
9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6,
member r45extreme/r4514.60.g6.
The archive is not included in this package.
The downloaded maximal member had one 18-byte line, SHA-256
752aa8b1509075bc39cb1151936b250c681fbdf0a9fdda20d8d5bbb6e6356c62,
and was compared directly with the embedded graph6 witness.

Without accepting \(U(14)\leq60\), the hand argument still proves the
explicit sensitivity bound

\[
D\geq1689-2U(14).
\]

This particular argument would not force nine if the available upper
bound were only 61. No asymptotic triangle theorem is used at order 13:
the small regular-graph lemma is proved above.

## Verification and trust

Tested with CPython 3.12.12, standard library only. From this directory:

~~~sh
set -o pipefail
python3 -B verify.py | cmp - EXPECTED_OUTPUT.txt
python3 -B independent_check.py | cmp - EXPECTED_INDEPENDENT.txt
python3 -B test_rejections.py
python3 -B -O verify.py | cmp - EXPECTED_OUTPUT.txt
python3 -B -O independent_check.py | cmp - EXPECTED_INDEPENDENT.txt
python3 -B -O test_rejections.py
shasum -a 256 -c SHA256SUMS
~~~

Expected: 45 admissible two-edge and 2997 admissible five-edge
six-vertex graphs; maximum degree-square sum 26; seven checked triangle
types; \(D\geq1569>1568\); eight rejected damaged certificates.
Certificate SHA-256:
015e1cec9107cafc6239605284acdecb1d56a93d9d0e0e7849af5122dca18149.

The exact checker validates all 105 two-edge and 3003 five-edge graphs on
six vertices, the relevant independence and degree-square bounds, all
seven triangle-type coefficients, the catalog witness, and the final
integer arithmetic. The independent checker uses literal triangle graphs
for the accounting identity and disjoint edge pairs for the small-graph
bound. Both are author-written cross-validation, not independent peer review.

The mathematical result is a hand proof, not an UNSAT certificate or a
formal proof-assistant theorem. Trusted are the displayed graph-to-count
argument, the earlier full-branch cover, the published \(U(14)\) upper
bound and \(R(3,5)\), Python/hardware, and hashes for file identity.
No private state, large certificate, or solver verdict is a premise.

## Independence and remaining work

This addresses a formerly conditional *anchor-selection restriction* for
the whole stated branch. It does not duplicate the new
[all-marking \(c=13\) triangle-balance interface](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_c13_triangle_balance),
which concerns E_left_8 and an
already selected common core; here the new argument concerns C77 and
selects the pair before any core is fixed. Slots 2 and Helgi's fixed
H20/O22 or creation-sensitive computations are not repeated.

All five families still require complete elimination or construction.
The codegrees \(9,\ldots,13\), all compatible E-markings, core types,
footprints, and outside-edge completions remain. The theorem applies
only to \(M=214\), not every hypothetical 43-vertex coloring.
The maintained global bound remains \(43\leq R(5,5)\leq46\).

Next falsifiable step: peer-check the signed triangle identity and the
catalog input, then integrate the all-five-family codegree-nine selection
with a completeness-preserving pair-label normalization. Do not infer
that the existing E_left_8 sixty-root quotient covers the other four
families without their separate label/profile interfaces.
