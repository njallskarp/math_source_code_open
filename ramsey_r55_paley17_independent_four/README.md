# Paley-17 forbids a disjoint independent four-set in a (4,5) graph

**Local theorem.** If \(J\) contains neither a red \(K_4\) nor a blue
\(K_5\), and \(J[A]\) is the Paley graph on 17 vertices, then
\(J[V(J)\setminus A]\) has no independent four-set.

**Global consequence.** In a graph with neither a red nor a blue \(K_5\),
let \(uv\) be a red edge and let
\(C=N_R(u)\cap N_R(v)\). If \(C\) contains a blue \(K_4\), then

\[
\max\{d_R(u),d_R(v)\}\leq |C|+17.
\]

The global consequence imports uniqueness of the order-17 \((4,4)\)
Ramsey graph. The local theorem is an exact, self-contained finite
computation with two independent implementations and no external catalogue.
The same global statement applies after interchanging colors.

**Consumption of the thirteen-interface classification.** In the complete
dense degree-five/five-separator family on 22 vertices, one of the thirteen
interfaces has \(K_{1,4}\) as its unique degree-five hub's neighborhood.
For that interface, the hub cannot have global red degree 23. It has global
degree at most 22. The other twelve interfaces retain the bound 23.
This excludes a complete intrinsic global subfamily, with all other
edges unrestricted. It does not exclude any entire 22-vertex interface,
any entire degree profile of a 43-vertex graph, or determine \(R(5,5)\).

## Complete local obstruction

Write \(P=P_{17}\), with vertices \(0,\ldots,16\) and red differences
\(\{1,2,4,8,9,13,15,16\}\) modulo 17. Suppose four independent vertices
\(b_1,\ldots,b_4\) lie outside this induced core, and put
\(X_i=N_R(b_i)\cap V(P)\).

Each \(X_i\) is triangle-free, since a red triangle in it would combine
with \(b_i\) to make a red \(K_4\). For every pair \(i\ne j\),

\[
P\bigl[V(P)\setminus(X_i\cup X_j)\bigr]
\quad\text{has no independent triple}.
\]

Otherwise that triple and the blue pair \(b_i b_j\) form a blue \(K_5\).
Only these necessary one-vertex and two-vertex attachment conditions are
needed; imposing the other possible blue five-sets would strengthen them.

For the purpose of this local nonexistence proof, enlarge each \(X_i\)
to an inclusion-maximal triangle-free subset \(Y_i\) of \(P\).
The pair conditions persist because their missed sets only shrink.
Equivalently, the induced graph on the core and four independent vertices
remains a \((4,5)\) graph after these additions: no red clique can use two
of the independent vertices, and adding red edges destroys blue cliques.

This is an existence implication within the necessary local subgraph.
It does not assert that the additions are valid in a 43-vertex extension,
or prescribe those additions to any surviving global case.

The exact computation enumerates all \(2^{17}\) core subsets and obtains
7,991 triangle-free subsets. Exactly 459 are inclusion-maximal: 408 have
size seven and 51 have size eight. Make a compatibility graph \(D\) on
these **labeled subsets**, with \(XY\) an edge when
\(P[V(P)\setminus(X\cup Y)]\) has no independent triple.

Every self-pair is incompatible, so repeated maximal columns cannot
satisfy the necessary pair conditions. The four \(Y_i\) would therefore
give a \(K_4\) in \(D\). But its exact clique counts are:

| Clique size | Count |
|---:|---:|
| 0 | 1 |
| 1 | 459 |
| 2 | 13,617 |
| 3 | 21,352 |
| 4 | **0** |

This proves the local theorem. There is no symmetry quotient, no implicit
restriction to maximum-cardinality columns, and no assumption that a
Paley automorphism extends to a larger graph. In particular the 408 maximal
seven-subsets are retained. The positive clique counts are compatibility
counts, not counts of complete Ramsey extensions.

## Transport to a whole global family

For a red edge \(uv\), set

\[
T=N_R(v)\setminus\bigl(N_R(u)\cup\{u\}\bigr).
\]

A red four-clique in \(T\) combines with \(v\) to make a red five-clique;
a blue four-clique combines with \(u\) to make a blue five-clique.
Thus \(G[T]\) is a \((4,4)\) graph. If \(|T|\geq17\), choose seventeen
vertices from it. The classical uniqueness theorem makes their graph
Paley-17. The red neighborhood of \(v\) is a \((4,5)\) graph and contains
both this Paley core and the assumed independent four-set in \(C\),
contradicting the local theorem. Hence \(|T|\leq16\), giving
\(d_R(v)=1+|C|+|T|\leq|C|+17\). Interchanging \(u,v\) proves the other
endpoint bound. This argument works at every order, not just 43.

Now take the [reviewed thirteen dense degree-five interfaces](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification),
source commit `8bf27902fba404e35593c90cbc7d2991abeda510`, also covering
every [dense five-separator case](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_five_separator_classification).
The latter bridge has an [independent review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_five_separator_classification_independent_review).
Their completeness statements are imported, not rerun here.

Let \(H=N_R(r)\) be one such 22-vertex neighborhood of a hypothetical
43-vertex Ramsey graph, let \(z\) be its unique degree-five vertex, and
let \(S=N_H(z)\). Only \(H\) and the root star are initially fixed:
all \(22\cdot20+\binom{20}{2}=630\) other physical edges are free.

The 20 vertices outside \(H\cup\{r\}\) split into \(T\), red to \(z\),
and \(B\), blue to \(z\). Here \(d_R(z)=6+|T|\), and \(T\) is a
\((4,4)\) graph, so the classical \(R(4,4)=18\) bound gives
\(d_R(z)\leq23\). Degree 23 forces \(|T|=17\) and \(|B|=3\).
Its Paley core is forced by the intrinsic degree case, not selected as an
extra hypothesis. All its relative cross-attachments remain free.

The three possible induced graphs on \(S\) are:

| Type | Zero-based interface indices | Degree-23 local test |
|---|---|---|
| \(K_{1,4}\) | 5 | Impossible: four independent leaves outside Paley-17 |
| \(K_{2,3}\) minus an edge | 6, 7, 8 | Locally feasible; no global case excluded |
| \(K_{2,3}\) | 0, 1, 2, 3, 4, 9, 10, 11, 12 | Locally feasible; no global case excluded |

`inputs.json` pins all thirteen graph6 records and the upstream certificate
identity. Both implementations verify their Ramsey property, edge count,
unique hub and induced hub-neighborhood type. The excluded record is

```text
UsHHirKdlp[IFVI|KpqfRW}at`msFRwgqNKW??Bw
```

For this record the new global bound is \(18\leq d_R(z)\leq22\).
The other twelve retain \(18\leq d_R(z)\leq23\). The lower bound imports
the classical \(R(4,5)=25\) degree window. No outside degree profile,
edge quota, global symmetry, or local maximum-density condition is added.

For completeness of the three-type **local feasibility distinction**,
`inputs.json` also supplies full five-column witnesses for the other two
types, having 112 and 106 edges respectively on 23 vertices. Both are
checked directly as \((4,5)\) graphs. Their fixture labeling is a fresh
local labeling: core 0..16, five neighbors 17..21, hub 22. These examples
do not assign edges in the twelve remaining global interfaces and do
not assert any global feasibility.

## Independent computation and reproduction

`derive.py` enumerates every core mask, tests all red-triangle masks,
finds maximal columns by one-vertex extensions, and obtains compatibility
by a separate blue-triangle-free mask table. It counts four-cliques by
forward bitset intersections over every compatibility triangle.

`audit.py` imports no producer code. It recursively grows triangle-free
subsets using a Boolean matrix and tests maximality by red edges in each
possible added vertex's selected neighborhood. It constructs each pair
by literally inspecting triples in the two omitted sets' intersection.
For each compatibility edge it checks its common neighborhood: each
four-clique would be counted six times as an edge in such a neighborhood.
It reconstructs every certificate column exactly.

The consumer checks also differ: one uses a streaming-bit graph6 decoder,
literal forbidden-set tests and the induced degree signature of \(S\);
the other uses a packed-integer decoder, recursive clique checks and all
five-vertex permutations to identify \(S\). They verify the primary
order-17 record's displayed isomorphism to the fixed Paley labeling.

`test_checks.py` compares the complete column and pair sets entry by entry.
It also checks the domain and clique algorithms against literal definitions
on every labeled graph of order at most five. Its full physical attachment
controls cover every cross-assignment for core orders 0..3 and independent
outside sets of orders 0..4, including repeated columns where appropriate.
For every valid example, independently saturating the columns preserves
the Ramsey property. Damaged certificates, malformed encodings and missing
consumer cases are rejected. Exact counts are in `EXPECTED_TEST.json`.

From the repository root, with Python 3.10 or later and its standard library:

```sh
python ramsey_r55_paley17_independent_four/derive.py
python ramsey_r55_paley17_independent_four/audit.py
python ramsey_r55_paley17_independent_four/test_checks.py
```

The first two commands give identical `EXPECTED.json`, with status
`VERIFIED_PALEY17_INDEPENDENT_FOUR_OBSTRUCTION`. All commands were also
checked with `python -O`. The complete main enumeration takes under one
second per implementation on the production machine; no timeout is part
of the proof. No solver, network download or omitted large artifact is
required for reproduction.

Certificate SHA-256:
`d2b07c6dcb31cc2ff3f4c72ac676109adc46f390e9a3423727c498fd913dcfbe`.
The compatibility edge encoding consists of sorted UTF-8 lines `i j\n`,
where indices refer to increasing column masks in the certificate. Its
SHA-256 is
`409374628370bd3827317d5c59aff81650643965e529606fa2b622dcae1827b1`.
The expanded edge list is regenerated, not stored. `SHA256SUMS` pins the
compact publication files.

## Imported facts, literature and remaining cases

For the local theorem, every finite domain is enumerated here; no catalogue
completeness is assumed. The general endpoint cap imports uniqueness of
the order-17 \((4,4)\) graph. The thirteen-interface application also
imports the reviewed dense degree-five classification, its five-separator
bridge, and classical small Ramsey bounds. The [primary McKay page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
lists the complete order-17 catalogue. The literal record and its source
hash are included as compact input; checking the record does not prove
catalogue completeness.

After graph-first selection, targeted primary-literature inspection
included [Angeltveit–McKay](https://arxiv.org/html/2409.15709v2), especially
Sections 2 and 5–7 on complete pointed gluing. No matching exact
Paley/independent-four obstruction or endpoint-cap statement was found
in that limited search. No historical-priority or general-method novelty
claim is made. The new content is the explicit finite obstruction and
its complete structural consumer, not a new Ramsey-number bound.

The proof uses saturation only to enlarge a necessary local graph with
an independent outside set. This does not contradict the existing
[local-to-global saturation barrier](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_local_saturation_barrier)
or [Paley/C4 maximality barrier](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_paley_c4_maximality_barrier).
No saturated interface is substituted for a surviving global graph.

Trust remains in the displayed finite argument, two exact implementations,
the explicitly imported classification facts, Python semantics and
ordinary hardware. These are independently implemented author checks,
not an external peer review or a proof-assistant formalization.

Remaining: the star interface with hub degrees 18..22, the other twelve
interfaces with hub degrees 18..23, the frozen \(H_*\) route, all other
structural families and the whole order-43 problem. A next structural
milestone must exclude another complete intrinsic branch or explain a
compatibility obstruction with the original 16-vertex core; the two local
survivors alone cannot justify discarding their global families.
