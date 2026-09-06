# Thirteen dense degree-five Ramsey neighborhoods

**Computer-assisted classification; external mathematical review pending.**
Let \(H\) be a simple graph on 22 vertices, with no clique of order four
and no independent set of order five. If \(e(H)\ge109\) and \(H\) has a
vertex of degree five, then \(e(H)=109\) and \(H\) is isomorphic to exactly
one of the **13 graphs** in [certificate.json](certificate.json).
Every listed graph has exactly one degree-five vertex.

Consequently, every 22-vertex graph with no \(K_4\), no independent
five-set, and at least 110 edges has minimum degree at least six. This threshold is sharp: the 13 graphs have 109 edges and minimum
degree five. The classification imports the completeness of the two primary
\(R(4,4;16)\) graphs, as specified below.

This covers a complete local family and gives an exact handoff to 13 fixed
neighborhoods with **all 630 remaining global edges free**. It does not
exclude any of their 43-vertex completions, classify the density-108
family, classify non-singleton five-separators, or improve a Ramsey bound.

## Reduction from every graph in the family

Use red for adjacency and blue for nonadjacency. Fix a degree-five vertex
\(z\), let \(S=N_H(z)\), and let \(A=V(H)\setminus(S\cup\{z\})\).
Then \(|S|=5\), \(|A|=16\), \(H[S]\) is triangle-free, and
\(H[A]\in R(4,4;16)\). A red triangle in \(S\) would complete a red
\(K_4\) with \(z\); an independent four-set in \(A\) would complete an
independent five-set with \(z\).

[McKay's complete primary catalogue](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
contains exactly two \(R(4,4;16)\) graphs, each with 60 edges. Both original
records are embedded as compact input data, in their original file order.
The two graphs are distinguishable without trusting catalogue
nonisomorphism: their degree-seven vertices induce respectively zero and
four triangles. Each has exactly eight automorphisms, independently
reconstructed by complete adjacency-preserving bijection searches.

For \(s_i\in S\), write \(X_i=N_H(s_i)\cap A\). Each \(A[X_i]\) is
triangle-free and has independence number at most three, so
\(|X_i|\le8\) by the classical bound \(R(3,4)\le9\).
Let \(m=e(H[S])\). The triangle-free bound gives \(m\le6\), and

\[
e(H)=60+5+m+\sum_{i=0}^4|X_i|.
\]

Thus \(e(H)\ge109\) forces \(4\le m\le6\) and

\[
\sum_{i=0}^4(8-|X_i|)\le m-4\le2.
\]

Every column consequently has size six, seven, or eight. There are exactly
seven isomorphism types of triangle-free five-vertex graphs with at least
four edges. The programs independently account for all \(2^{10}\) labeled
five-vertex graphs and their relabelings. No graph symmetry is assumed of
\(H\) or of a future global completion.

## Exact attachment conditions

After selecting either labeled graph \(A\) and one labeled representative
\(S\), every attachment is allowed subject to the displayed density budget
and these necessary and sufficient conditions:

1. Each \(A[X_i]\) is triangle-free.
2. If \(s_i s_j\) is red, then \(A[X_i\cap X_j]\) has no red edge.
3. If \(s_i s_j\) is blue, then \(A\setminus(X_i\cup X_j)\) has no
   independent triple.
4. For every independent triple \(T\subseteq S\), the vertices of
   \(A\setminus\bigcup_{s_i\in T}X_i\) form a red clique.
5. For every independent four-set \(T\subseteq S\),
   \(\bigcup_{s_i\in T}X_i=A\).

There is no distinctness assumption on the five columns.

To prove sufficiency, first consider forbidden sets containing \(z\).
They are excluded by triangle-freeness of \(S\) and absence of independent
four-sets in \(A\). A red four-clique avoiding \(z\) uses zero, one, or
two vertices of \(S\): three would contain a triangle in \(S\). These
cases are excluded by the core property and conditions 1–2. An independent
five-set avoiding \(z\) uses at least two vertices of \(S\), since
\(\alpha(A)\le3\). Two, three, or four such vertices are covered by
conditions 3–5; all five are impossible since \(m\ge4\).
Necessity follows by adjoining the relevant vertices of \(S\).

The independent audit also derives this interface directly: it substitutes
the fixed colors into every one of the \(\binom{22}{4}=7315\) physical
red-four events and \(\binom{22}{5}=26334\) physical blue-five events.
Each surviving event is a rectangle of incidence variables. Its exact
physical indices are hashed separately for every one of the 14 core/neighbor
cases. This derivation does not import the producer's attachment predicates.

## Complete census and isomorphism classification

The complete eligible individual-column counts are:

| Core record | Size 6 | Size 7 | Size 8 |
|---:|---:|---:|---:|
| 0 | 1408 | 480 | 27 |
| 1 | 1392 | 496 | 56 |

Only these four core/neighbor cases have attachments satisfying all
conditions and the density budget:

| Core | Neighbor graph \(S\) | Labeled attachments | Isomorphism classes | Orbit sizes |
|---:|---|---:|---:|---|
| 0 | \(K_{1,4}\) | 48 | 1 | 48 |
| 0 | \(K_{2,3}\) minus one edge | 48 | 3 | 16, 16, 16 |
| 0 | \(K_{2,3}\) | 480 | 5 | 96, 96, 96, 96, 96 |
| 1 | \(K_{2,3}\) | 264 | 4 | 24, 48, 96, 96 |
| **Total** | | **840** | **13** | |

All other ten core/neighbor cases are empty. Every survivor has exactly
109 edges, hence no larger edge count occurs in the degree-five family.
The certificate gives every representative as both five integer column
masks and an independent graph6 encoding. Bit \(a\) of column \(i\)
is one exactly when \(a\in X_i\). Core vertices are \(0,\ldots,15\),
neighbor vertices are \(16,\ldots,20\), and the marked vertex is \(21\).

The group \(\operatorname{Aut}(A)\times\operatorname{Aut}(S)\) acts by
transporting core coordinates and column positions. Both programs compare
the **entire enumerated attachment set** with the disjoint union of the
13 certified representative orbits, not just aggregate counts. The groups
are enumerated completely by testing injective partial maps for adjacency
preservation. Representatives are the lexicographically least mask tuples
in their own orbits. Each representative is directly checked to have a
unique degree-five vertex, so every isomorphism fixes that vertex and must
map \(S\) to \(S\) and \(A\) to \(A\). Distinct core types and distinct
neighbor graph types cannot mix. The computed orbits are therefore exactly
the graph isomorphism classes, not merely a possibly redundant cover.

## Minimum-degree corollary

A vertex of degree at most three would leave at least 18 nonneighbors,
whose graph has neither a red nor a blue four-clique, contradicting
\(R(4,4)\le18\). If a vertex has degree four, its 17 nonneighbors form
a \((4,4)\) graph. Every vertex there has degree at most eight, so that
part has at most 68 edges. Each of the four neighbors attaches to at most
eight of those 17 vertices, and their triangle-free graph has at most four
edges. Hence

\[
e(H)\le68+32+4+4=108.
\]

The new degree-five classification then implies \(\delta(H)\ge6\)
whenever \(e(H)\ge110\). This corollary does not require the older
four-separator enumeration. Its degree-four argument is consistent with
the [reviewed four-separator result](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_four_separator_review).

## Free global interface

Suppose a hypothetical \(G\in R(5,5;43)\) has a red neighborhood \(H\)
of order 22, at least 109 edges, and a degree-five vertex *inside \(H\)*.
An isomorphism places \(H\) at one of the 13 listed graphs on
\(0,\ldots,21\). Put its global root at 22 and the remaining vertices at
\(23,\ldots,42\). Fix the 22 red root-to-\(H\) edges and the 20 blue
root-to-outside edges. All

\[
22\cdot20+\binom{20}{2}=630
\]

other edges remain free. Every graph in the stated global branch has such
a labeling. Conversely, every full Ramsey completion of one of these
interfaces belongs to that branch. Complementing the global colors gives
the analogous blue-neighborhood statement.

No opposite-neighborhood type, outside degree/profile, additional anchor,
quota, symmetry of the completed graph, or outside edge assignment has been
imposed. The thirteen completion families remain undecided.

## Reproduction

Tested with CPython 3.12.12 and its standard library. No solver, graph package,
floating-point arithmetic, randomness, or large external artifact is needed.
From this directory:

```sh
set -o pipefail
python3 -B verify.py --fetch-catalogue | cmp - EXPECTED_VERIFY.json
python3 -B audit.py | cmp - EXPECTED_AUDIT.json
python3 -B test_checks.py | cmp - EXPECTED_TEST.json
python3 -B -O verify.py | cmp - EXPECTED_VERIFY.json
python3 -B -O audit.py | cmp - EXPECTED_AUDIT.json
python3 -B -O test_checks.py | cmp - EXPECTED_TEST.json
shasum -a 256 -c SHA256SUMS
```

Omit `--fetch-catalogue` for a fully offline replay using the two embedded
primary records. That flag compares the exact original bytes from
[the primary file](https://users.cecs.anu.edu.au/~bdm/data/r44_16.g6).
Its SHA-256 is
`b9a7c89cf999d64c976c877891d06f828ce2e846f5ddfa72bb402f2ddd57b927`.

Expected: all comparisons are empty; both enumerations recover all 840
tuples, the same per-case tuple hashes, and 13 disjoint representative
orbits, all at 109 edges. The compact expected outputs contain the complete
14-row census, not a partial-search status. Output hashes are byte hashes;
tuple hashes use the lexicographically sorted mask tuples encoded as compact
JSON followed by a newline. No timeout or solver verdict enters the proof.

`verify.py` generates columns by subsets, propagates packed compatibility
domains, and enumerates all labeled attachments. `audit.py` uses a separate
packed-integer graph6 decoder and Boolean adjacency matrices, derives its
rules from physical forbidden sets, checks all 65,536 candidate masks, and
enumerates complete fibers after normalizing only the first column under
core automorphisms. It then lifts those fibers to the full labeled set.
It imports no producer code. Both compare their full sets to the same compact
orbit certificate, and their per-case set hashes must agree.

These are author-written independent implementations, not external peer
review or proof-assistant formalization. The tests make 15,210 comparisons of the recursive clique checker with
literal definitions on every labeled graph through order five, compare both
decoders, reject 18 malformed encodings and eight damaged certificates, and
compare the
physical rule system with direct forbidden-set tests on all representatives
and additional boundary assignments. Checks remain active under `python -O`.

## Literature, dependencies, and remaining work

The target was selected from the committed Discovery Net neighborhood of
`bafkreigcklbpc42u6txpn6ttcrpgmwi2myrnn56l5er62orospchi6oezm`, initially through
height 3336. The full read included all authors and peer relations. Relevant
prior contributions were the low-deficiency root cover (2775), local
connectivity theorem (3210), complete four-separator classification (3236),
its independent review (3244), and the saturation limitation (3299).
Their constructions and enumerations are context, not premises of the new
degree-five census. The principal and two peer report directories were empty
at target selection and the prepublication refresh. Through height 3340,
the new Paley(41) switching-class review (3337) was also read; it is a
separate complete family and does not collide with this census.

The mathematical inputs are the complete primary \(R(4,4;16)\) catalogue,
the classical bounds \(R(3,4)\le9\), \(R(4,4)\le18\), and the elementary
triangle-free bound on at most five vertices. The catalogue's record
properties and nonisomorphism are directly checked; its completeness is
**imported, not reproved**. The two records are McKay's data, released under
[CC BY 4.0](https://users.cecs.anu.edu.au/~bdm/data/).

[Angeltveit–McKay, Section 3.3](https://arxiv.org/html/2409.15709v2) supplies
the 114-edge order-22 extremum and the broader near-extremal gluing context.
That extremum is used only to interpret 109 and 110 edges as deficiency five
and four, respectively, not to prove this classification. A targeted primary
literature search found these catalogues and the gluing work, but no explicit
statement of this thirteen-graph marked classification. This limited search
is not a priority determination; no novelty is claimed for the classical
attachment, degree, or orbit methods.

Trust remains in catalogue completeness, the displayed unformalized
reduction, exact Python semantics, decoding, finite execution, hardware, and
SHA-256 for identities. The new source contains neither private graph state
nor a generated full formula, raw search dump, executable binary, or solver
certificate.

The frozen four-separator completion searches, global certificate lane,
Core194 automorphism work, fixed-H92 gluing, and peer coverage audits were
not rerun. The next falsifiable structural milestone is to determine whether
any of these thirteen complete interfaces is ruled out by an outside-size
bound that leaves the opposite neighborhood free. Until such a bound is
proved, all thirteen remain. Density 108 and minimum degree at least six
also remain outside this classification.
