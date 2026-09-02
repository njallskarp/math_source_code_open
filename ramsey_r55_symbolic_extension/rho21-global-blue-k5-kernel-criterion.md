# Exact global-kernel criterion for forced blue \(K_5\)'s at \(\rho=21\)

## Result type

**Symbolic obstruction theorem with a finite local-pattern certificate.**  In
the exceptional \(m=10,\rho=21\) branch, let \(U_B\) be the 23 selected blue
\(K_4\)-clauses.  There is a marked loopless multigraph \(D\) on these 23
clause nodes and a distinguished ten-node set \(S\) such that the selected
blue supports force a blue \(K_5\) if and only if at least one of the
following holds:

1. some triangle of \(D\) has total edge multiplicity at least five;
2. some triangle containing at least two nodes of \(S\) has total edge
   multiplicity at least four; or
3. some node outside \(S\) sends four edges, counted with multiplicity, into
   \(S\).

Equivalently, the selected blue support union is \(K_5\)-free exactly when

\[
\begin{aligned}
\mu_D(a,b)+\mu_D(b,c)+\mu_D(c,a)&\le4
    &&\text{for all }\{a,b,c\}\subseteq V(D),\\
\mu_D(a,b)+\mu_D(b,c)+\mu_D(c,a)&\le3
    &&\text{if }|\{a,b,c\}\cap S|\ge2,\\
d_D(v,S)&\le3
    &&\text{for every }v\notin S.
\end{aligned}                                                   \tag{1}
\]

This is an exact colored-support obstruction on the joint \(X/Y\) kernel,
not merely a degree profile.  Both abstract two-link degree families have
explicit members satisfying (1), so selected-blue \(K_5\)-freeness alone
does not exclude \(\rho=21\).

## The global clause kernel

Every vertex \(x\ne w\) belongs to exactly two selected blue clauses, while
\(w\) belongs to the ten side clauses.  Construct \(D\) as follows:

- its 23 nodes are the clauses in \(U_B\);
- every \(x\ne w\) becomes an edge \(e_x\) joining its two clause nodes;
- \(S\subseteq V(D)\) is the set of ten side-clause nodes containing \(w\).

Supports are sets, so the two clauses containing \(x\) are distinct and
\(D\) is loopless.  Distinct blue \(K_4\)-clauses cannot share four vertices,
so

\[
\mu_D(u,v)\le3.                                               \tag{2}
\]

There is a sharper marked constraint inside the side set.  Two side clauses
already share \(w\), so three shared ordinary vertices would make their full
\(K_4\)-supports identical.  Therefore

\[
\mu_D(s,t)\le2\qquad(s,t\in S).                              \tag{2a}
\]

There are 41 ordinary edge-vertices.  A side clause uses one place for
\(w\), whereas every other clause contains four ordinary vertices.  Hence

\[
|E(D)|=41,\qquad
d_D(s)=3\ (s\in S),\qquad d_D(v)=4\ (v\notin S).            \tag{3}
\]

The original vertex \(w\) is represented by the ten-element incidence set
\(S\).  Every other original vertex is represented by the two-element
incidence set \(e_x\).  Two original vertices are forced blue by the selected
clauses exactly when their incidence sets intersect.  Thus the selected-blue
support graph is the intersection graph of

\[
\{e_x:x\ne w\}\cup\{S\}.                                    \tag{4}
\]

The two-link gluing theorem constructs the same \(D\) concretely: start with
the ten-node \(J_X\) and thirteen-node \(J_Y\), turn the three \(X\)
half-edges into edges to the three witness nodes, turn the \(Y\) half-edge
into an edge to the mixed \(Q\)-node, and mark the ten side nodes as \(S\).

## Pairwise-intersecting edge lemma

### Lemma

Let \(\mathcal E\) be a multiset of at least four distinct edge occurrences
of a loopless multigraph.  If every two occurrences intersect, then either

- all occurrences share a common endpoint, or
- all their endpoints lie in one triangle.

### Proof

Choose an occurrence \(ab\).  Every other edge meets \(a\) or \(b\).  If all
meet the same one, the family is a star.  Otherwise there are edges \(ac\)
and \(bd\), with \(c\ne b\) and \(d\ne a\).  They must intersect, so
\(c=d\).  Any further edge must meet each of \(ab,ac,bc\); looplessness then
forces it to be one of these three edge types.  Hence the family is supported
on the triangle \(abc\).  Parallel occurrences cause no exception. \(\square\)

This elementary line-graph fact is the complete local classification needed
below; no global kernel enumeration enters the proof.

## Blue \(K_5\)'s avoiding \(w\)

A forced blue \(K_5\) avoiding \(w\) is exactly a family of five pairwise
intersecting edges of \(D\).  The star alternative in the lemma is impossible
by (3), since \(\Delta(D)=4\).  Therefore all five occurrences lie on a
triangle of \(D\), and its total multiplicity is at least five.  Conversely,
any five edge occurrences on the three sides of a triangle are pairwise
intersecting and yield a blue \(K_5\).  This proves condition 1.

## Blue \(K_5\)'s containing \(w\)

Such a clique consists of \(w\) and four ordinary edge-vertices.  The four
edges must be pairwise intersecting, and every one must meet \(S\), because
intersection with \(S\) is exactly adjacency to \(w\) in (4).

If the four edges form a star centered at \(v\), then \(v\notin S\): a side
node has ordinary degree three by (3).  Each edge's other endpoint must lie
in \(S\).  Thus the star exists exactly when

\[
d_D(v,S)=4                                                   \tag{5}
\]

for some \(v\notin S\), which is condition 3.

Otherwise the edge lemma puts all four occurrences on a triangle.  At least
two triangle nodes must lie in \(S\).  With no side node, no edge meets
\(S\); with exactly one side node, all four eligible edges would be incident
to that node, contradicting its degree three.  Conversely, if at least two
triangle nodes lie in \(S\), every triangle side meets \(S\), so any four
edge occurrences on that triangle join \(w\) to form a blue \(K_5\).  This
is exactly condition 2 and completes the proof of (1).

## Exact audit and nonemptiness

The checker exhausts every multiset of four and five edge types on six
canonical labels.  Six labels are complete: five pairwise-intersecting edges
use at most a five-leaf star's six vertices, while four use at most five.  It
verifies the star/triangle dichotomy under (2)--(3), including every side-set
marking for the four-edge case and the sharper side-side bound (2a).

The compact certificate also glues the previously published simple
representatives into two explicit 23-node kernels, one for each value of

\[
q=|Q\cap A|\in\{0,1\}.                                      \tag{6}
\]

For each, a definition-level checker reconstructs the 42-vertex intersection
graph (4), inspects every five-vertex subset, and agrees with (1): neither
representative forces a blue \(K_5\).  These are abstract support witnesses,
not full Ramsey colorings.

Run:

~~~bash
python3 ramsey_r55_symbolic_extension/verify_rho21_global_blue_k5_kernel.py \
  ramsey_r55_symbolic_extension/rho21-global-blue-k5-kernel-certificate.json
~~~

The verifier uses only Python's standard library and exact integer
combinatorics.

## Consequence for the support-realizability program

Condition (1) is a completeness-preserving rewrite rule for every future
kernel enumerator or SAT projection.  Candidate generation can reject a
partial kernel immediately when a weighted triangle or side-star becomes
forbidden; no 21- or 20-vertex graph needs to be materialized for this test.

The explicit survivors also identify the limitation precisely.  The next
obstruction must use information absent from the selected-blue intersection
graph alone: red \(K_4\)-freeness in \(X\), completion of unspecified edges,
the selected red supports and their cross-color intersection bounds, or
singular-DP ancestry.

## Novelty assessment and literature position

Discovery Net was searched through indexed height 1165 for “line graph,”
“pairwise intersecting edges,” “kernel triangle,” and “forced blue
\(K_5\).” No matching contribution was found.  The star-or-triangle lemma is
elementary line-graph structure and is not claimed as new.  The apparently
new content is its exact application to the exceptional Ramsey support
kernel, especially the two additional \(S\)-marked conditions for cliques
containing \(w\).

The link graphs at \(\rho=21\) belong to the classical \((4,5)\)-Ramsey
setting.  McKay and Radziszowski proved \(R(4,5)=25\), and McKay's
[authoritative Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
document the relevant finite graph classes.  This result does not enumerate
or assume completeness of an order-21 dataset.

## Scope and trust boundary

The theorem imports the exceptional \(m=10,\rho=21\) profile and the exact
two-link gluing normal form.  The forward criterion and converse are a
symbolic proof about the selected blue clauses.  The checker audits the
finite local edge-family classification and the two supplied representatives;
it is not the universal proof.

An independent prepublication derivation accepted the theorem with high
confidence, checked the two glued representatives without reusing the
producer checker, and supplied the strengthening (2a).

Passing (1) says only that the **selected** blue clauses do not already force
a blue \(K_5\).  It does not produce a coloring of every unspecified edge,
exclude a red \(K_4\) in \(X\), realize the selected red clauses, or certify a
singular-DP lift.  No solver, floating point, or unbounded enumeration is
used.

## Public source and provenance

The reader-facing source is
[rho21-global-blue-k5-kernel-criterion.md](https://github.com/njallskarp/math_source_code_open/blob/main/ramsey_r55_symbolic_extension/rho21-global-blue-k5-kernel-criterion.md).
Immutable source commit:
`9a1cfb6f6cc535cd5a83f291c226cc5d8711e62f`.

- Initial research-note SHA-256:
  `5d2f5b99d8305e7f12a14c5a96a82cd2cdb91734923b8d359416c79cb9ed9acc`.
- Initial exact-certificate SHA-256:
  `deabd25217ad4432904a6ac9b32d8ed9f6bc6cd1f08c2e32cf87cdac483dce75`.
- Initial checker SHA-256:
  `982a6689454df162475d01524b899620023f0d3301b5ce6bc77fa1bc2cf9d691`.

The independently reviewed strengthening (2a), markup repair, and updated
checker are immutable at corrected source commit
`2b155af463e9bb8a9eadae7b734bd49de7256456`:

- corrected research-note SHA-256:
  `ca37ff1bace25a1fdc0d94e365db0d9dd062a844cfc043137a5888fc26166ff7`;
- corrected exact-certificate SHA-256:
  `6f30cd3cc288f6e58feeb57adc8b8f4122740b300c92795930639fbafc8fef87`;
- corrected checker SHA-256:
  `018263f92fa0f923facceec29fff149d647969e73e44021592608ee003a063db`.
