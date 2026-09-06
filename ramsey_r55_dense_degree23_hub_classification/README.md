# Sharp dense degree-five families over Paley-17

Let \(J\in\mathcal R(4,5;23)\), meaning that \(J\) has no red
\(K_4\) and no blue \(K_5\). Suppose \(h\) has red degree five,
and put \(S=N_R(h)\). This package proves the following complete
classification for two specified induced types of \(S\).

| Induced \(S\) | Sharp maximum \(e_R(J)\) | Isomorphism classes attaining it |
|---|---:|---:|
| \(K_{2,3}-e\), type 62 | **115** | **24** |
| \(K_{2,3}\), type 126 | **116** | **29** |

Every one of the 53 extremal graphs has a unique degree-five vertex and
trivial automorphism group. `certificate.json` gives every representative
by five literal attachment columns. These statements concern the two
displayed families, not all degree-five graphs of order 23.

**Joint-core exclusion.** All 144 complete ways to glue the 24 type-62
extremal neighborhoods to original interfaces 6, 7 and 8 are impossible.
Every case retains all 389 remaining physical edges. Independent formula
reconstruction and checked DRAT refutations therefore improve the global
degree-23 hub deficiency bound to **eight** for those three interfaces.

The nonneighbors \(T\) of \(h\) have order 17 and form a \((4,4)\)
graph. The general formulation therefore imports the classical uniqueness
of the order-17 \((4,4)\) graph, Paley-17. The computation on the
explicit Paley core itself imports no catalogue.

## Complete structural reduction

Use \(T=\mathbb Z_{17}\), red differences
\(\{1,2,4,8,9,13,15,16\}\), \(S=\{s_0,\ldots,s_4\}\), and
\(h\) red to all of \(S\) and blue to all of \(T\). The five
columns \(X_i=N_R(s_i)\cap T\) remain arbitrary actual columns.
**They are never replaced by saturated columns.**

The fixed red edges in \(S\) are

\[
02,03,04,12,13,
\]

with \(14\) additionally red in type 126. Both types are triangle-free,
have no independent four-set, and have just one independent triple,
\(\{s_2,s_3,s_4\}\). Consequently the complete forbidden-set conditions
are exactly:

1. Every \(X_i\) is triangle-free in \(T\).
2. For a red \(s_i s_j\), \(X_i\cap X_j\) is independent in \(T\).
3. For a blue \(s_i s_j\),
   \(T\setminus(X_i\cup X_j)\) has no independent triple.
4. \(T\setminus(X_2\cup X_3\cup X_4)\) is a red clique.

These conditions are sufficient as well as necessary. A red four-clique
meeting \(S\) uses one or two vertices of \(S\), since \(S\) is
triangle-free. A blue five-clique meeting \(S\) uses two or three,
since neither \(T\) nor \(S\) has an independent four-set. A forbidden
clique containing \(h\) is already prevented by the fixed core or the
triangle-free \(S\). This accounts for every physical forbidden set.

The core has 68 red edges, so

\[
e_R(J)=73+e_R(S)+\sum_{i=0}^4|X_i|.
\]

Complete subset enumeration gives maximum triangle-free column size
eight. To classify every tuple with column sum at least 37, each column
must therefore have size at least five. The complete domain contains
5,593 columns: 2,550 of size five, 2,176 of size six, 816 of size seven,
and 51 of size eight. All are used; repeated columns are permitted by
the search and rejected only if the actual compatibility conditions fail.

The two independent enumerations find:

| Type | All labeled valid tuples of sum at least 37 | Column sums found |
|---|---:|---|
| 62 | 6,528 | 37 only |
| 126 | 47,328 | 37 only |

Thus no tuple has sum at least 38. Both maxima are attained. The expanded
tuple sets agree entry by entry, not merely in their counts.

## Canonical classification and rigidity

The full automorphism group of the core consists of the 136 affine maps
\(v\mapsto av+b\), with \(a\) a nonzero quadratic residue modulo 17.
The audit proves completeness of this action directly. An automorphism
fixing zero restricts to an automorphism of its eight-vertex neighborhood.
All \(8!\) permutations of that neighborhood are checked: 16 preserve
its graph, and exactly eight lift to the whole core. The eight other
vertices have distinct adjacency signatures into the neighborhood, so
each lift is forced. Translations then give the full group of order 136.
No external automorphism-group catalogue is imported.

The automorphism groups of the two labeled \(S\) types have orders two
and twelve; all \(5!\) permutations are checked. Taking the least tuple
under the product action gives 24 and 29 classes. Every orbit has full
size, respectively \(136\cdot2=272\) and
\(136\cdot12=1632\). The representatives' unique degree-five hub is
checked physically, so every graph automorphism must preserve its
\(S,T\) partition. Full orbit size therefore proves rigidity of each
whole 23-vertex graph, not just rigidity under a selected subgroup.

The representative column-size profiles are \((6,7,8,8,8)\) and
\((7,7,7,8,8)\). Type 62 has twelve classes of each profile; type 126
has fourteen and fifteen. The compact certificate and its regenerated
full orbits give the classification independently of these summaries.

## Consumption by the complete thirteen-interface family

Take the [reviewed dense degree-five classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification),
also covering the [dense five-separator family](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_five_separator_classification).
All thirteen interfaces \(H=N_R(r)\) have order 22, 109 edges, and a
unique local degree-five hub \(z\). Only \(H\) and the root star are
initially fixed; all 630 other physical edges are free.

The intrinsic case \(d_R(z)=23\) forces its seventeen red neighbors
outside \(H\cup\{r\}\) to induce Paley-17. Three other outside
vertices remain, denoted \(B\). This leaves 474 free physical edges.
The [independently accepted Paley obstruction](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_paley17_independent_four)
already excludes the star-type interface 5 in this degree case.

In each of the other twelve cases, \(J=G[N_R(z)]\) has order 23 and
contains \(r\) as its degree-five hub. Its hub neighborhood is the
same \(S=N_H(z)\). The new theorem therefore gives:

| Original interface indices | \(e_R(N_R(z))\) bound | Red deficiency \(122-e_R(N_R(z))\) |
|---|---:|---:|
| 6, 7, 8 | at most 115 | at least **7** |
| 0, 1, 2, 3, 4, 9, 10, 11, 12 | at most 116 | at least **6** |

This excludes the complete intrinsic degree-23 subfamilies with hub red
deficiency at most six in the first row and at most five in the second.
The density threshold is a stated intrinsic branch, not an assumed
outside quota. No entire remaining degree-23 interface is excluded.

At equality, every red neighborhood \(N_R(z)\) belongs to the
corresponding complete extremal classification. All relative \(S\)
markings are retained: two per type-62 representative and twelve per
type-126 representative. The resulting boundary cover has

\[
3\cdot24\cdot2=144,\qquad
9\cdot29\cdot12=3132,
\]

or **3,276 complete marked templates**. These are coverage keys, not
realizable global graph counts. The audit reconstructs every template;
none is selected by fixing a convenient local witness.

Each boundary template leaves **389 physical edges free**: 272 from the
original sixteen-vertex core to \(T\), 48 from that core to \(B\), 15
from \(S\) to \(B\), 51 between \(T\) and \(B\), and three within
\(B\). Only the now-classified 85 \(S\)-to-\(T\) edges were added
to the forced information. No automorphism of \(S\) or \(T\) is
assumed to extend to the original interface or a global graph. Instead,
every relative \(S\) marking is explicitly included and all remaining
attachments stay free. The original interface is not quotiented further.

The complete type-62 equality consumer is additionally decided below.
Its surviving degree-23 cases have density at most 114, hence deficiency
at least eight. The 3,132 type-126 equality templates remain open.
Below their respective boundaries, all twelve degree-23 families retain
all 474 physical edge variables subject to their intrinsic density bounds. Lower global
hub degrees, the frozen \(H_*\) route, all other structural families,
and the full order-43 question remain open.

## Complete joint-core decision at type-62 equality

For each of original interfaces 6, 7 and 8, take all 24 local extremal
representatives and both relative S markings. This is exactly 144 cases.
Each fixes the original 22-vertex neighborhood, both anchor stars, the
forced Paley-17 core, and the classified S-to-core edges. The other 389
edges are independent Boolean variables, with red represented by one.

For every physical five-set, impose the clause prohibiting all-red
edges and the clause prohibiting all-blue edges, substituting only the
fixed colors. A clause made true by a fixed opposite color disappears;
duplicate residual clauses are removed. The resulting formula is
equivalent to the complete remaining (5,5) extension problem for that
marked case. It adds no outside quota, degree profile, symmetry or
unforced fixed edge.

`glue.py` reconstructs each physical specification and generates these
clauses by compatible-clique recursion. A separate matrix construction
uses the independent graph6 decoder and direct physical assignments.
`audit_cnf.cpp` then enumerates all \(\binom{43}{5}=962598\) five-sets
literally from that independently reconstructed matrix. Every one of the
144 resulting CNFs agrees byte for byte with the producer. All formulas
have 389 physical variables and no auxiliary variables.

Kissat returned UNSAT on every formula. Every trace was independently
checked by `drat-trim` with verdict `s VERIFIED`. Therefore the entire
type-62 density-115 branch is empty, despite all 24 local neighborhoods
being valid Ramsey graphs. This consumes the classification using both
cores on the same physical graph. It leaves the lower-density type-62
cases and the type-126 boundary open.

`GLUING_MANIFEST.json` pins every key, variable count, clause count and
CNF hash. Manifest SHA-256:
`e5d7b3b63e4508537c65cedeec9ef38c1ba39ca6e636349eb4f78227d15c214a`.
`EXPECTED_GLUING.json` records the verified complete-family verdict.
The 16,851,125 bytes of observed proof traces are regenerated in scratch,
not published. Trace hashes can change across valid replays; exact
formula identities and successful checker verdicts are required.

## Independent computation and reproduction

`derive.py` enumerates all core masks using exact independent-set and
triangle-free recurrences. It constructs compatibility bitsets and
searches columns in order \(0,2,1,3,4\), pruning only by necessary
compatibility and the maximum remaining column sum. It normalizes the
first column under the explicit affine action, retaining every orbit,
and finally generates the complete graph-isomorphism classes.

`audit_dense.cpp` imports no producer code, generated domains, certificate
or symmetry representatives. It recursively grows triangle-free subsets
using literal core-edge tests. It constructs pair compatibility from
explicit forbidden edge and triple lists. It enumerates every ordered
blue pair \((X_0,X_1)\), then the red-compatible \(C_4\) pair
\((X_2,X_3)\), and finally \(X_4\). It does no affine orbit pruning.
The interchangeable labels 2 and 3 are searched once in increasing
column order and both ordered tuples are emitted. Repetition there is
impossible by the checked blue-pair condition. All output tuples are
sorted and checked for duplicates.

`audit.py` imports neither enumerator. It checks the full core and S
automorphism groups, every representative's forbidden sets and unique
hub, complete disjoint orbit expansions, and exact equality to the C++
tuple streams. It independently decodes all thirteen imported graph6
records. It constructs every one of the 3,276 complete boundary templates
and performs 2,958,228 physical edge transports on arbitrary assignments
of the retained bits. These synthetic assignments test coverage and
transport; they are not asserted to be Ramsey graphs.

With Python 3.10+ and a C++20 compiler, run from the repository root:

```sh
python3 -B ramsey_r55_dense_degree23_hub_classification/reproduce.py /tmp/fresh-dense-hub-check --cxx c++
```

The scratch directory must be new and outside the source directory.
The complete replay regenerates the classification, builds the independent
enumerator, compares both complete labeled families, audits the full
consumer and runs the definition-level controls. Expected final status:
`VERIFIED_COMPLETE_DENSE_HUB_CLASSIFICATION`.

Production used CPython 3.12 and GCC 16.2 (`--cxx g++-16`). The full C++
enumeration was also checked with Clang address/undefined-behavior
sanitizers. Normal and assertion-disabled Python reports agree. There
is no solver or network download in the classification-only replay.
Expanded tuple streams, binaries and logs belong in
scratch, not Git.

For the **full claim including the joint-core exclusion**, build
[Kissat](https://github.com/arminbiere/kissat), observed source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` (version 4.0.4), and
[drat-trim](https://github.com/marijnheule/drat-trim), observed source
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, outside the source
checkout. Then run:

```sh
python3 -B ramsey_r55_dense_degree23_hub_classification/reproduce.py /tmp/fresh-dense-hub-full --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Expected final status:
`VERIFIED_DENSE_HUB_CLASSIFICATION_AND_GLOBAL_EXCLUSION`.
This regenerates and independently checks every formula and every proof.
No timeout result counts as a proof. The wrapper requires UNSAT exit
status, exact formula comparison and a successful checker verdict for
all 144 cases. `NATIVE_REPLAY.json` records observed tool identities and
resource totals. The classification-only command does not verify this
additional native-proof claim.

The sorted tuple encoding is five decimal masks separated by single
spaces, followed by a newline. Its SHA-256 hashes are:

- Type 62: `b314d237f489f94600ccd90e0ef7c7ac3faaf98a9910ae09ce4adfc8e827651c`.
- Type 126: `6006ad0f7d35b0ffe64128a1702d06924e755e46b675b0eaca8e7798d65b69fa`.

`EXPECTED.json` records the full audit and boundary-template hash.
`EXPECTED_DERIVE.json` and `EXPECTED_TEST.json` pin the other reports;
`SHA256SUMS` pins the compact package.

## Imported facts and limits

The literal two-core local computation uses only the displayed Paley
graph. The general degree-five theorem imports uniqueness of
\(\mathcal R(4,4;17)\), documented by the
[primary McKay catalogue](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
The global consumer imports the independently reviewed thirteen-interface
classification and separator bridge, and \(U(23)=122\) to name the
deficiency values. The input records and upstream certificate identity
are pinned in `inputs.json`; rechecking individual records does not
reprove the upstream catalogues' completeness.

Primary literature was checked after graph-first selection, including
[Angeltveit–McKay's complete pointed-gluing work](https://arxiv.org/html/2409.15709v2).
The limited search did not locate this exact two-family extremal census.
No historical-priority claim or new general gluing method is made.

Trust lies in the displayed finite reduction, independently implemented
complete enumerations, exact physical and group checks, the explicitly
imported facts, language/compiler semantics and ordinary hardware. The
joint-core exclusion additionally trusts the DRAT checking kernel;
solver status alone is not an input to the theorem.
These are author checks, not a new external peer review or formalization.
The remaining 3,132 type-126 boundary templates require joint compatibility
with their original cores; existence of their local representatives does
not establish a global completion. No entire degree-23 interface or
whole order-43 family is excluded.
