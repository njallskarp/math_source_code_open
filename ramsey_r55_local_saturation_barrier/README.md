# A minimal outside-triangle obstruction to local Ramsey saturation

## Result and scope

There is a graph \(H\in R(4,5;22)\) with \(108\) edges, vertex
connectivity \(7\), and diameter \(3\). Exactly one pair, \(\{4,5\}\),
is at distance three. Adding edge \(45\) gives another \(R(4,5;22)\)
graph, now with \(109\) edges and diameter two.

Nevertheless, a fully checked \(26\)-vertex Ramsey \((5,5)\) graph
\(G\) contains \(H\) as the red neighborhood of vertex \(22\), and
adding that same edge creates exactly one red \(K_5\):

\[
\{4,5,23,24,25\}.
\]

Thus even seven-connectivity and local deficiency six do not force
diameter two. Moreover, a locally safe saturation step need not preserve
an already valid partial Ramsey extension. The general obstruction below
identifies the exact missing outside interface, and this witness achieves
the least possible number of outside vertices for that obstruction.

This is **not** a Ramsey graph on \(43\) vertices, an exclusion of its
low-deficiency branch, or an assertion that \(G\) extends to order \(43\).
It does not show that every possible sequence of locally safe additions
fails. It refutes the unconditional single-edge transfer and the
diameter-two inference from the stated local hypotheses. No previously
published theorem is alleged to make either false inference.

## An exact, outside-size-independent obstruction lemma

Let \(G\) be any red/blue complete graph without a monochromatic
\(K_5\). Let a root \(r\) be red to every vertex of \(H\) and blue to
every vertex in \(O=V(G)\setminus(V(H)\cup\{r\})\). Suppose
\(a,b\in H\) are blue-adjacent and have no common red neighbor in \(H\).
Write

\[
T=N_R(a)\cap N_R(b)\cap O.
\]

Recolor \(ab\) red, leaving all other edges unchanged. This operation is
locally safe in \(H\), since a newly created red \(K_4\) would require
two common red neighbors there, while adding red cannot create an
independent five-set. Globally, it preserves the Ramsey \((5,5)\)
property **if and only if** \(G[T]\) has no red triangle.

Indeed, every new red \(K_5\) must use \(ab\), and its other three
vertices must be a red triangle in their common red neighborhood. That
common neighborhood is exactly \(\{r\}\cup T\). The root is blue to
all of \(T\), so it lies in no such triangle. Hence the new red
\(K_5\)'s correspond bijectively to red triangles of \(G[T]\). No new
blue clique can be created by recoloring a blue edge red.

This proof applies to every outside size. In particular, at most two
outside vertices can never obstruct this operation. Our witness uses
exactly three, proving sharpness of that boundary. With a \(22\)-vertex
core and its root, \(26\) is therefore the least extension order for
this specified kind of obstruction; no broader minimal-order claim is made.

## Explicit dense core and extension

The parent is record 65, numbered from zero, in the primary
\(R(4,5;22,e=114)\) edge-extremal file. Its graph6 record is:

```text
ULYUULtmfAYOBAB@Fwx}UrLrKz?dyhB|UajiSTtW
```

Delete exactly these six red edges:

\[
4\!:\!12,\quad5\!:\!13,\quad5\!:\!14,\quad
4\!:\!15,\quad4\!:\!16,\quad5\!:\!17.
\]

The resulting graph has degree multiset \(7^2\,9^2\,10^{14}\,11^4\).
Its vertices \(4,5\) have disjoint red neighborhoods, and
\(4,6,7,5\) is a red path of length three. Their pair is the only one
at distance greater than two. Removing

\[
N_H(4)=\{1,2,6,9,13,14,17\}
\]

isolates vertex \(4\). The connectivity lower bound is verified both
by all cuts of size at most six and by seven explicit internally
vertex-disjoint paths between every nonadjacent pair, as described below.

Add root \(22\), red to all \(22\) core vertices. Add a red triangle
on \(23,24,25\), blue to the root. Their red neighborhoods inside \(H\)
are exactly:

\[
\begin{aligned}
N_R(23)\cap H&=\{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,17\},\\
N_R(24)\cap H&=\{0,1,4,5,8,9,10,11,12,14,15,16,19,20,21\},\\
N_R(25)\cap H&=\{2,3,4,5,6,7,10,11,13,15,16,18,20,21\}.
\end{aligned}
\]

All unlisted pairs are blue. This specifies every pair of the
\(26\)-vertex graph, which has \(178\) red edges. Both \(4\) and
\(5\) are red to the outside triangle, producing the claimed obstruction.
[WITNESS.json](WITNESS.json) includes the parent/deletions and an independently
readable final-core adjacency list, not just a graph hash.

## Exact deletion mechanism

The witness was not obtained by changing the frozen four-separator core.
For a blue pair \(a,b\) in a parent \(R(4,5)\) graph, let \(C\) be
its common red neighborhood. For each \(x\in C\), delete exactly one
of \(ax,bx\). This destroys every common red neighbor, without creating
a red clique. Assign a bit \(y_x=1\) when \(ax\) is retained and
\(y_x=0\) when \(bx\) is retained.

Any newly independent five-set must contain \(a\) or \(b\). It cannot
contain both: every member of \(C\) still sees one endpoint red, so the
common blue neighborhood of the endpoints is unchanged. For every
independent four-set \(S\) avoiding both endpoints, inspect
\(N(a)\cap S\). If this nonempty set lies entirely in \(C\), impose
\(\bigvee_{x\in N(a)\cap S}y_x\). The analogous constraint for \(b\)
uses \(\neg y_x\). An untouched exclusive neighbor makes the condition
automatic. These clauses are necessary and sufficient for preserving
the absence of independent five-sets.

Here \(C=\{12,13,14,15,16,17\}\), and the exact kernel has six
variables and sixteen distinct clauses. All \(64\) assignments are
checked against literal five-set enumeration. Its only solutions are
\((0,1,1,0,0,1)\) and \((1,0,1,0,0,1)\); the first constructs \(H\).
No complete classification of other parent graphs or distant pairs is
claimed. The parent catalogue need not be complete for this construction.

## Reproduction and independent checks

Use CPython 3.12.12 and the standard library, from this directory:

```sh
set -o pipefail
python3 -B verify.py | cmp - EXPECTED_VERIFY.json
python3 -B audit.py | cmp - EXPECTED_AUDIT.json
python3 -B test_verify.py | cmp - EXPECTED_TEST.json
python3 -B -O verify.py | cmp - EXPECTED_VERIFY.json
python3 -B -O audit.py | cmp - EXPECTED_AUDIT.json
python3 -B -O test_verify.py | cmp - EXPECTED_TEST.json
shasum -a 256 -c SHA256SUMS
```

[verify.py](verify.py) reconstructs the graph6 parent and edge deletions,
checks literal core four- and five-sets, all \(110056\) cuts of size at
most six, the entire six-bit deletion kernel, and all \(65780\) five-sets
of \(G\) in each color. It also checks the safe core addition and exactly
one newly forbidden global five-set.

[audit.py](audit.py) imports no producer code. It begins from the separate
adjacency list, uses bitset clique recursion and Floyd–Warshall distances,
and supplies \(861\) checked paths: seven internally vertex-disjoint
paths for each of the \(123\) nonadjacent core pairs. Paths are obtained
by integral residual flow but then decoded and checked for physical edges,
simplicity, endpoints, and internal disjointness. Thus no solver or flow
verdict is trusted. Any cut of at most six vertices misses one path between
each surviving nonadjacent pair; adjacent surviving vertices remain joined.
The displayed seven-cut gives equality. Full edge hashes agree between
the two representations.

[test_verify.py](test_verify.py) compares both clique methods on all graphs
through order five, totaling \(6600\) literal comparisons; rejects seven
malformed certificate/graph6 controls; and distinguishes seven disjoint
paths from six. Both full methods also check that removing any one of the
three outside vertices removes the new red obstruction.

Canonical sorted red-edge lists use compact JSON followed by a newline:

```text
core SHA-256: 7a62bdb8bba5659e9382ae584a40660910b10f6d7780bc5cef9104fa56b113a9
extension SHA-256: 0f5c653842d3d14733cf96f4d530e7d0da6949fa264ce1501ceb19adb13910ef
```

## Literature, discovery provenance and trust boundary

[Angeltveit–McKay, Section 3.3](https://arxiv.org/html/2409.15709v2) gives
\(U(22)=114\) and the \(133\) edge-extremal parent graphs.
[McKay's primary data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
provides those graphs. The selected parent file SHA-256 is
`54dffec4ecab0f863b75620ccf8b228e5d6299c799e2d6b284fd51c51aa96ed7`.
The catalogue is discovery provenance only: all required properties of
the embedded parent and final graph are checked directly. The imported
extremum is needed only to call \(108\) edges deficiency six.

A bounded deletion search used NetworkX 3.6 to decode the parent. One
Kissat 4.0.4 call then found the three signatures, with \(60\) variables,
\(660\) clauses, seed zero, a \(30\)-second internal cap and
\(40\)-second outer cap. Its SAT assignment was decoded and directly
checked. Discovery CNF SHA-256:
`85642dd75429207eacdad1875c400dba4120924486f851cce0a4d2e4f87aad65`.
Kissat source: `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
binary SHA-256:
`f32a4752349ac9a75e8b0a9852f647a469c63030f912af9ffe759d101961ac4a`.
Neither NetworkX nor Kissat is required or trusted for reproduction.
No UNSAT or full \(43\)-vertex solve is claimed. Raw search files,
catalogues, binaries and logs are not included.

Graph-first comparison found prior exact-anchor diameter bounds at heights
2135, 2141, 2145 and 2153, and the different order-22 four-connectivity
construction at 3210. Those statements remain valid and are not premises.
The current M214, Core194 and fixed-H92 lanes are separate. The previously
frozen four-separator completion tests were not rerun.

No priority claim is made for the elementary triangle criterion, deletion
principle, or classical parent graph. The contribution is the exact dense,
seven-connected limitation witness, its minimal partial extension, and
the complete missing-interface criterion. Verification is author-written
cross-checking, not independent peer review or proof-assistant formalization.
The displayed proofs, CPython semantics, exact parsing, SHA-256 and ordinary
hardware remain explicit trusts. Hashes and publication are not proofs.

The unconditional diameter-two/single-edge-saturation route is closed by
the counterexample. Any proposed transfer must control the outside
common-neighbor triangles; more local connectivity cannot repair it.
