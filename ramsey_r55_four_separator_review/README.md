# Independent coverage review of the dense four-separator family

## Verdict and exact domain

**Accepted, with catalogue completeness explicitly imported.** This reviews
[the height-3236 classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_four_separator_classification),
source commit 4bf427dcb479b49978f772e12e55c3cea4711927, artifact
bafkreieuei63n3v6lbeepery6s4dhl4kcdyiexsywim4ypvedqrkaqu4da.

Let \(H\) be a simple 22-vertex graph with no red \(K_4\), no blue \(K_5\),
and at least 108 red edges. If a four-set \(S\) disconnects the red graph,
then \(H\) has exactly 108 red edges, and the marked pair \((H,S)\) is
isomorphic to the explicit pair \((H_*,\{17,18,19,20\})\) below.

The fixed neighborhood therefore covers a complete stated family; it is
not an arbitrary literal-core restriction. Graphs with no four-separator,
lower densities, and other neighborhood orders are not covered.
The 43-vertex completion of this family remains undecided.

## Structural audit with elementary density bounds

Independence numbers add across the components of \(H-S\), and their sum
is at most four. A component with independence number one, two, or three
has order at most \(3,8,17\), respectively. These follow from
\(R(4,2)\leq4\), \(R(4,3)\leq9\), and \(R(4,4)\leq18\).
The latter two upper bounds follow from the usual neighborhood recurrence,
using \(R(3,3)\leq6\) and the even/even handshaking refinement giving
\(R(3,4)\leq9\). Exact-value lower bounds are unnecessary here.

A component of independence number four is impossible because another
nonempty component exists. Among partitions with sum at most four,
only \(1+3\) can accommodate the 18 vertices outside \(S\):
\(2+2\), \(1+1+2\), and \(1+1+1+1\) have capacities \(16,14,12\).
Smaller independence budgets accommodate still fewer vertices.

Hence \(H-S\) has exactly two components: a clique \(B\) of order
\(b\in\{1,2,3\}\) and a graph \(A\in R(4,4;18-b)\).
Each vertex of \(S\) has at most eight neighbors in \(A\), since its
neighborhood there has no red triangle or blue four-clique.
Thus at most 32 edges join \(S\) to \(A\).

The [primary complete catalogues](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
give maximum edge counts \(55,60,68\) at orders \(15,16,17\), and the
order-17 catalogue is one graph, isomorphic to \(P_{17}\). The checker
reads all \(640,2,1\) records, respectively, verifies both forbidden
four-set conditions, counts every edge, and checks a proposed
catalogue-to-Paley permutation on every pair.
These operations do not prove catalogue completeness.

This review does not need the target's stronger Turán bound in the
middle row. The following elementary estimates suffice:

| \(b\) | Bound on \(e(H[B\cup S])\) | Bound on \(e(H)\) |
| --- | --- | --- |
| 1 | 8 | \(68+32+8=108\) |
| 2 | \(1+8+5=14\) | \(60+32+14=106\) |
| 3 | \(3+8+5=16\) | \(55+32+16=103\) |

For the first row, a five-vertex graph with nine edges contains a
four-clique. For the second, count the edge of \(B\), all eight possible
cross edges, and at most five edges on \(S\). For the third, each vertex
of \(S\) has at most two neighbors in the three-clique \(B\), and again
\(e(H[S])\leq5\). Thus only \(b=1\) can reach 108.

Write \(B=\{z\}\). If \(zs\) were blue for some \(s\in S\), the
18-vertex \(K_4\)-free graph on \(A\cup\{s\}\) would contain a blue
four-clique. Adding \(z\), which is blue to all of \(A\cup\{s\}\),
would give a blue \(K_5\). Therefore \(N_H(z)=S\), and \(H[S]\) is
triangle-free.

Density equality forces \(A=P_{17}\), all four \(S\)-to-\(A\) degrees
equal to eight, and \(H[S]\) to have four edges. A triangle-free
four-vertex graph with four edges is \(C_4\). This derives the complete
fixed-core interface before any column or orbit computation.
Height 3210's connectivity theorem and the local bound \(U(22)=114\)
are not premises of this review.

## Physical forbidden-set identity

Fix \(P_{17}\) on residues modulo 17, adjacent when their difference is
a nonzero square. Fix a red cycle on \(17,18,19,20\), a hub \(21\)
red to exactly that cycle, and all hub-to-Paley pairs blue.
Let \(x_{i,a}\) indicate a red edge from cycle vertex \(17+i\) to
Paley vertex \(a\). There are 68 free Boolean variables.

The independent checker substitutes these fixed colors in every one of
the 7,315 physical four-sets and 26,334 physical five-sets. After
discarding satisfied clauses, the residual clause multiset is exactly:

- 272 negative three-literal clauses: one cycle vertex and a Paley
  red triangle.
- 272 negative four-literal clauses: adjacent cycle vertices and a
  Paley red edge.
- 136 positive six-literal clauses: opposite cycle vertices and a
  Paley independent triple.

Every residual appears once; there is no empty residual. Their signed
physical indices agree entrywise, not just in total count, with the
three published attachment conditions:

1. Each column \(X_i\) is triangle-free in \(P_{17}\).
2. \(X_i\cap X_{i+1}\) is independent.
3. The complement of \(X_i\cup X_{i+2}\) has no independent triple.

This Boolean identity holds for every assignment of the 68 incidences,
even before imposing the four column sizes. It is not a solver verdict
or a sample of completed graphs. The exhaustiveness also has a short
vertex-type proof: a forbidden set without the hub uses at most two
cycle vertices; hub-containing cases reduce to a triangle in \(C_4\)
or an independent four-set in \(P_{17}\).

## A different finite coverage decomposition

The checker imports neither target program. Instead of enumerating
the complete four-column family directly, it first partitions all
eligible eight-subsets into orbits of the 136 affine maps
\(a\mapsto qa+t\), where \(q\) is a nonzero square modulo 17.
Each map is checked on every Paley edge. All eligible columns are
covered by exactly two disjoint orbits:

| First-column representative | Orbit size | Complete ordered remaining-column choices |
| --- | --- | --- |
| \(0,1,3,4,6,10,11,15\) | 17 | 16 |
| \(0,1,3,6,7,10,12,13\) | 34 | 24 |

For each representative, all \(51^3\) ordered triples of remaining
columns are tested, including repeated columns. Thus these are
complete fibers, not selected profiles.

The seed has columns

| Cycle vertex | Paley neighbors |
| --- | --- |
| 17 | \(0,1,3,4,6,10,11,15\) |
| 18 | \(0,2,3,6,7,9,12,14\) |
| 19 | \(1,2,5,7,8,12,13,15\) |
| 20 | \(2,4,5,8,9,11,14,16\) |

For each first-column representative, its complete fiber equals
entrywise the corresponding fiber of the seed's affine-dihedral orbit.
Every arbitrary first column can be moved to one representative.
Transporting its remaining columns preserves all three physical
conditions. It follows that every admissible quadruple is in the
seed orbit. The checker also lifts the fibers back and compares the
entire resulting set with that orbit.

There are \(17\cdot16+34\cdot24=1088\) ordered quadruples, all in one
orbit. No completeness assertion about the full automorphism group
is used. The group action is on labeled constraint systems, not an
assumed automorphism of a hypothetical 43-vertex graph.

The seed is separately checked for every forbidden four- and five-set,
has 108 edges and degree multiplicities \(4^1,9^3,10^{13},11^5\).
Checking all 9,109 subsets of size at most four finds just the cut
\(\{17,18,19,20\}\). These are degrees and cuts inside the neighborhood,
not degrees or cuts of a future global completion.

## Exact graph-to-fixed-neighborhood handoff

Suppose a 43-vertex Ramsey coloring has a vertex \(v\) whose red
neighborhood \(H\) has order 22, at least 108 red edges, and a
four-vertex separator. Apply the reviewed isomorphism to \(H\), label
\(v\) by 22, and label its remaining 20 vertices arbitrarily by
\(23,\ldots,42\). The graph is now a completion of:

- The entire fixed \(H_*\) on \(0,\ldots,21\).
- Red edges from 22 to all of \(H_*\).
- Blue edges from 22 to \(23,\ldots,42\).

Conversely, any full Ramsey completion of this literal interface has
a neighborhood in the stated separator family. Every one of the
remaining \(22\cdot20+\binom{20}{2}=630\) graph edges is free at this
coverage step. No opposite neighborhood, outside profile, degree
sequence, profile quota, symmetry of the completed graph, or preferred
outside labeling has been imposed.

This equivalence is existential up to relabeling. It is the precise
permission for a different lane to search one fixed neighborhood as
a complete separator branch. It does not say that every degree-22
neighborhood has a separator, or that a hypothetical global graph
must enter this branch. Color exchange gives the corresponding
blue-neighborhood statement.

## Reproduction and evidence

With CPython 3.12.12 and its standard library, from the repository root:

~~~bash
python3 -B ramsey_r55_four_separator_review/check.py
python3 -O -B ramsey_r55_four_separator_review/check.py
~~~

Each command reads the three small pinned original catalogues over
HTTPS into memory. An offline directory containing those original
files can be supplied with the optional flag:

~~~bash
python3 -B ramsey_r55_four_separator_review/check.py --catalog-dir /path/to/catalogues
cd ramsey_r55_four_separator_review
shasum -a 256 -c SHA256SUMS
~~~

Both outputs must equal [EXPECTED.json](EXPECTED.json) byte for byte.
Its SHA-256 is
8bbdfc8d45b161f1119c7eeb3cc471c310d55751d19263da8f160e734bb511c5.

The tuple SHA-256 is
74662241469b6584cf8199574d914b2c21441929f0272c4cf38a48c219097e5a;
the seed-edge SHA-256 is
7ad8fce8852efd386b3ec188841e114930c9ab8856d80c5e8339b8c73805032a.
They agree with the independently computed target identities.
The residual-clause SHA-256 is
3f6192f0f98133cade36acb681ddffd694497897fb44f9eb6fc3491bbb73b039.
These hashes use compact JSON followed by one newline.

Seventeen component-level negative controls reject malformed graph6,
wrong or nonbijective catalogue maps, malformed columns, repeated-column
Ramsey violations, and missing, duplicated, sign-corrupted, or
index-corrupted residual clauses. Positive small graph6 controls pass.
Normal and optimized runs agree; observed times including primary
downloads were 5.25 and 6.65 seconds, not performance guarantees.
No large certificate, catalogue, formula, or solver state is published.

## Trust, independence, and remaining work

The full-family theorem imports primary catalogue completeness and
classical small Ramsey bounds. Record validity, edge counts, the
catalogue-to-Paley witness, the physical Boolean identity, orbit
fibers, seed properties, and finite coverage are checked here.
The computation cannot prove that the supplied catalogues omit no
graphs; their completeness is the external mathematical premise.

The seed and catalogue permutation are public input data from the
target, validated here rather than trusted. No target executable or
research module is imported. The new finite decomposition and physical
clause audit provide external implementation independence, not
proof-assistant formalization. Trust also remains in the displayed
unformalized proof, exact Python, hardware, decoding, and file identities.

The target author receives credit for the classification. This review
claims no novel Ramsey or group-action method. The primary catalogue
page and the target's complete public proof were inspected; a limited
literature search is not a priority determination.

This does not duplicate slot 1's direct search, slot 2's conditional
family enlargement, slot 5's composition work, or Helgi's Core194 and
overlapping-neighborhood searches. The planned Core194 normalization
audit was not pursued because height 3224 had already independently
accepted that exact cover.

The global range remains \(43\leq R(5,5)\leq46\), using the
[Angeltveit–McKay upper bound](https://arxiv.org/abs/2409.15709).
There is no global row elimination or 43-vertex witness here.
The next consumer test is a full checked completion or refutation
of the literal interface with all 630 remaining graph edges retained.
This coverage seat should next inspect a new restriction of that
interface, not repeat the same attachment enumeration.
