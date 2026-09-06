# The unique dense four-separator Ramsey neighborhood

## Result and scope

**Computer-assisted classification, awaiting independent mathematical review.**
Let \(H\) be a simple graph on \(22\) vertices with no \(K_4\), no independent
set of size five, and \(e(H)\ge108\). If a set \(S\) of four vertices disconnects
\(H\), then \(e(H)=108\), and the marked pair \((H,S)\) is isomorphic to the
explicit pair \((H_*,\{17,18,19,20\})\) below.

Consequently **every four-separator family at densities at least \(109\) is
excluded**, and the entire density-\(108\) four-separator family reduces to
one graph, not one arbitrarily selected literal core. This does not classify
graphs without a four-separator. In the degree-\(22\), deficiency-at-most-six
branch, where the imported local upper bound is \(114\), it classifies exactly
the four-separator subfamily.

The surviving graph is a genuine \(R(4,5;22)\) graph. Its red cone is a valid
local \(23\)-vertex \(R(5,5)\) graph. Neither object is a \(43\)-vertex Ramsey
graph, and no completion, whole degree branch, or Ramsey bound is settled.

The earlier [connectivity package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_low_deficiency_connectivity)
gave this graph as a sharpness witness at Discovery Net height 3210.
**That theorem is not a premise here:** the current proof explicitly assumes
a four-separator. No independent review of height 3210 was visible in the
committed graph through height 3226 when this pass selected its target.
The new content is the family-wide uniqueness reduction and its exact orbit
certificate, not another review of the old construction.

## Structural reduction

Write \(R(a,b;n)\) for the class with no clique of size \(a\) and no independent
set of size \(b\). Import the classical bounds
\(R(4,2)=4\), \(R(4,3)=9\), and \(R(4,4)=18\).
The independence numbers of the components of \(H-S\) add to at most four.
A component with independence number one, two, or three has order at most
\(3,8,17\), respectively. A component with independence number four is
impossible because there is another nonempty component.

There are \(18\) vertices outside \(S\). The only possible independence
partition is therefore \(1+3\): partitions \(2+2\), \(1+1+2\), and
\(1+1+1+1\) accommodate at most \(16,14,12\) vertices, and the smaller
budgets accommodate fewer. Thus there are precisely two components:
a clique \(B\) of size \(b\in\{1,2,3\}\), and a graph
\(A\in R(4,4;18-b)\).

Every vertex of \(S\) has at most eight neighbors in \(A\). Its neighbors
are triangle-free, since \(H\) is \(K_4\)-free, and have no independent
four-set, since they lie in \(A\). The bound \(R(3,4)=9\) applies.

We import completeness of [McKay's primary Ramsey catalogues](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Exact inspection gives the following maxima, with the complete input file
identities in `EXPECTED.json`:

| \(b\) | \(\lvert A\rvert\) | Catalogue records | Maximum \(e(A)\) | Upper bound on \(e(H)\) |
| --- | --- | --- | --- | --- |
| 1 | 17 | 1 | 68 | 108 |
| 2 | 16 | 2 | 60 | 104 |
| 3 | 15 | 640 | 55 | 103 |

The last column is

\[
e(H)\le e(A)+32+\left\lfloor\frac{(b+4)^2}{3}\right\rfloor,
\]

using Turán's bound on the \(K_4\)-free graph induced by \(B\cup S\).
All catalogue entries are checked literally for both forbidden four-sets;
the sole order-\(17\) entry is identified with the Paley graph by an explicit
permutation. These checks do **not** independently prove that the catalogues
are complete.

Only \(b=1\) survives. Write \(B=\{z\}\). If \(z\) were nonadjacent to
some \(s\in S\), then the \(K_4\)-free graph \(A\cup\{s\}\), of order
\(18\), would contain an independent four-set. All of it is nonadjacent to
\(z\), producing an independent five-set in \(H\). Therefore \(z\) is
adjacent to every vertex of \(S\). In particular, \(H[S]\) is triangle-free.

Equality in the density bound forces all of the following:

- \(A=P_{17}\), the unique catalogue graph, with \(68\) edges.
- Each vertex of \(S\) has exactly eight neighbors in \(A\).
- \(H[S]=C_4\), with four edges.
- \(z\) has precisely the four neighbors in \(S\).

This is a proof for every qualifying graph, not an assumption about a
preselected neighborhood.

## Exact attachment criterion

Label \(P_{17}\) by \(\mathbb F_{17}\), with an edge when the nonzero
difference is a square. Label the cycle vertices in order by \(17,18,19,20\).
Let \(X_0,X_1,X_2,X_3\subseteq\mathbb F_{17}\) be their eight-element
red-neighbor sets. The constructed graph has the required Ramsey property
if and only if:

1. Each \(P_{17}[X_i]\) is triangle-free.
2. For consecutive indices modulo four, \(X_i\cap X_{i+1}\) is independent
   in \(P_{17}\).
3. For opposite indices, \(P_{17}[\mathbb F_{17}\setminus(X_i\cup X_{i+2})]\)
   has no independent triple.

Necessity follows respectively from a red \(K_4\) using one cycle vertex,
a red \(K_4\) using two consecutive cycle vertices, and an independent
five-set using two opposite cycle vertices. For sufficiency, any red
\(K_4\) avoiding \(z\) uses at most two cycle vertices and is covered by
these cases or the Ramsey property of \(P_{17}\). Any independent five-set
avoiding \(z\) uses at most two cycle vertices; zero or one would require an
independent four-set in \(P_{17}\), and two are covered by condition 3.
A red \(K_4\) containing \(z\) would require a triangle in \(C_4\).
An independent five-set containing \(z\) would require an independent
four-set in \(P_{17}\). Thus all cases are accounted for.

The exact computation finds \(51\) permitted individual signatures and
\(1088\) ordered quadruples satisfying these three conditions. No
distinctness assumption is imposed on the four signatures.

## One orbit, hence one graph

Take the seed columns in `certificate.json`:

| Cycle vertex | Neighbors in \(P_{17}\) |
| --- | --- |
| 17 | 0, 1, 3, 4, 6, 10, 11, 15 |
| 18 | 0, 2, 3, 6, 7, 9, 12, 14 |
| 19 | 1, 2, 5, 7, 8, 12, 13, 15 |
| 20 | 2, 4, 5, 8, 9, 11, 14, 16 |

Let \(x\mapsto ax+b\) act on \(P_{17}\), where \(a\) is one of the eight
nonzero squares and \(b\in\mathbb F_{17}\). Every such map preserves edges
because it multiplies each nonzero difference by a square. Independently
apply a rotation or reflection of \(C_4\), fixing \(z\). These are
\(136\cdot8=1088\) legitimate relabelings of the constructed graph.
We do not assume that they constitute its full automorphism group.

The checker proves **set equality**, not merely equality of counts, between
all admissible ordered quadruples and the orbit of this seed. That orbit
contains \(1088\) distinct quadruples. Every marked pair \((H,S)\) in the
theorem is therefore isomorphic to the seed pair, proving the classification.

The seed has degree multiplicities \(4^1,9^3,10^{13},11^5\). Its unique
degree-four vertex is \(z=21\). Any four-separator in this graph must isolate
a degree-four vertex by the proved classification, so its four-separator
is also unique. This last conclusion uses the degree list, not a new census
of vertex cuts.

## Reproduce

Validated with CPython 3.12.12 and its standard library. No solver, graph
library, floating-point calculation, randomized search, or background job
is involved. From the repository root:

```sh
python3 -B ramsey_r55_four_separator_classification/verify.py
python3 -B ramsey_r55_four_separator_classification/audit.py
python3 -B ramsey_r55_four_separator_classification/test_verify.py
python3 -B -O ramsey_r55_four_separator_classification/verify.py
python3 -B -O ramsey_r55_four_separator_classification/audit.py
python3 -B -O ramsey_r55_four_separator_classification/test_verify.py
```

The first two commands read the three original primary files directly over
HTTPS, verify their SHA-256 identities, and keep them only in memory:
[order 15](https://users.cecs.anu.edu.au/~bdm/data/r44_15.g6),
[order 16](https://users.cecs.anu.edu.au/~bdm/data/r44_16.g6), and
[order 17](https://users.cecs.anu.edu.au/~bdm/data/r44_17.g6).
For offline reproduction, place those exact original files in an external
directory and pass `--catalog-dir /absolute/path/to/catalogues` to either
command. No raw catalogue is included in this contribution.

Compare parsed JSON output with `EXPECTED.json`, `EXPECTED_AUDIT.json`, and
`EXPECTED_TEST.json`, respectively. Compact expected results:

```text
signatures = 51
compatible ordered quadruples = affine-dihedral orbit size = 1088
tuple SHA-256 = 74662241469b6584cf8199574d914b2c21441929f0272c4cf38a48c219097e5a
seed edge SHA-256 = 7ad8fce8852efd386b3ec188841e114930c9ab8856d80c5e8339b8c73805032a
controls: 1100 small graphs, 15210 clique comparisons, 18 rejected inputs
```

Hashes use compact JSON with a final newline. Tuple identity hashes the
lexicographically sorted list of admissible ordered quadruples, with each
column sorted. Edge identity hashes sorted unordered red pairs.

## Validation and trust boundary

`verify.py` uses subset lists, literal clique tests, opposite-pair joins,
and direct column relabelings. `audit.py` imports no producer: it uses a
different packed graph6 decoder, recursive bitset clique detection, all
\(2^{17}\) masks, cyclic backtracking, and physical \(22\)-vertex
permutations. Both reconstruct the complete set and obtain the same hash.
The audit reads `EXPECTED.json` for input identities and a proposed Paley
permutation; it checks the permutation on every pair rather than trusting
its interpretation. Its enumerated set must equal its own physically
generated orbit, independently of the expected count or hash.

The test suite covers all labeled graphs of orders zero through five,
both colors, clique sizes through one above the order, graph6 round trips,
twelve malformed graph6 decoder calls, and six malformed seed certificates.
Checks remain active under optimized Python. This is an author cross-check
with different implementations, **not independent peer review or a formal
proof**.

Trust remains in the displayed unformalized structural argument, the
classical small Ramsey bounds and Turán theorem, primary catalogue
completeness, graph interpretation, complete finite execution, exact Python,
hardware, and file identities. The direct seed check does not depend on
catalogue completeness; the whole-family classification does.

No novelty claim is made for these classical methods. A targeted primary
literature check found the catalogue and general Ramsey-connectivity work,
not a source explicitly asserting this precise marked density-\(108\)
classification; this limited search does not establish priority. The
campaign's remaining task is global completion, not another fixed-width
attachment census. A useful next falsifiable step is a checked full
completion or refutation for **all** completions of this now-complete
four-separator family, with the opposite neighborhood left free. The
previously frozen literal-core-pair searches are not reopened by this result.
