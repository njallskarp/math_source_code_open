# A maximal cross-interface below the dense four-separator threshold

This gives an explicit graph in \(\mathcal R(4,5;22)\) with a marked
degree-four vertex, a four-cycle as its neighborhood, and a Paley-17
nonneighborhood. It has **104 edges**, and **every missing edge between the
Paley core and the four-cycle creates a red \(K_4\)** when added.

Consequently, the following proposed extension of the dense
\(H_*\) classification is false:

> Every valid Paley-17/four-cycle interface can be completed, by adding only
> cross-edges, to an interface with 108 edges.

The example is already maximal under the allowed additions. It has no
proper valid supergraph with these marked internal graphs and hub edges
fixed. In particular it is not a cross-edge subgraph of any marked copy
of \(H_*\), even after relabeling the Paley core and the cycle.

This is a local counterexample to a completion mechanism. It is not a
43-vertex Ramsey graph, does not exclude any 43-vertex completion family,
and does not classify all maximal interfaces. No minimality or extremal
claim is made for 104 edges.

## The explicit graph

Use vertices \(A=\{0,\ldots,16\}\), \(S=(17,18,19,20)\), and \(z=21\).
Inside \(A\), color \(uv\) red when

\[
v-u\pmod {17}\in\{1,2,4,8,9,13,15,16\}.
\]

Inside \(S\), use the cycle in the displayed order. Join \(z\) red to all
four vertices of \(S\) and blue to all of \(A\). The red cross-neighborhoods
of the four cycle vertices are:

| Vertex | Red neighbors in \(A\) |
|---|---|
| 17 | 0, 1, 3, 8, 12, 14, 15 |
| 18 | 1, 4, 5, 7, 10, 12, 15 |
| 19 | 0, 4, 6, 7, 10, 11, 16 |
| 20 | 2, 6, 8, 9, 11, 14, 16 |

Every other edge is blue. There are \(68+4+4+28=104\) red edges.
The red degree multiset is \(4^1,8^1,9^4,10^{16}\).

## A compact proof and its independent checks

The file `certificate.json` contains these four columns and forty
obstructions, one for each missing cross-edge \(uv\). Each obstruction is
a four-set whose sole missing red edge is \(uv\). This proves maximality:
any nonempty set of cross-edge additions contains an edge whose red
\(K_4\) obstruction persists after all the additions.

`verify.py` reconstructs the graph and directly checks every one of its
7,315 four-sets and 26,334 five-sets. It then checks that all forty missing
cross-edges have the claimed obstruction.

`audit.py` imports no code from that verifier. It uses bit rows, quadratic
residues, and recursive clique search. Its Ramsey check uses the complete
structural decomposition. Write the four columns as \(X_i\), indexed modulo
four. Besides the two forbidden four-sets in the Paley core, it checks:

1. Each \(X_i\) is triangle-free.
2. Each \(X_i\cap X_{i+1}\) is independent.
3. Each \(A\setminus(X_i\cup X_{i+2})\), for \(i=0,1\), has no independent
   triple.

These conditions are sufficient and necessary for the marked graph to
belong to \(\mathcal R(4,5;22)\). A red \(K_4\) outside the core can use
one cycle vertex and a core triangle, or an adjacent cycle pair and a
core edge. It cannot use the hub, since its neighborhood is triangle-free.
A blue \(K_5\) using the hub would require an independent core four-set.
Without the hub, the only remaining possibility uses an opposite cycle
pair and an independent core triple. The cycle has no independent triple.

The audit also checks maximality independently through the equivalence:
adding a missing edge \(uv\) creates a red \(K_4\) precisely when
\(N_R(u)\cap N_R(v)\) contains a red edge. It separately validates every
supplied four-set certificate.

The maximality statement has a marked-interface boundary. Six unrestricted
additions remain valid: \(z0,z2,z3,z5,z9,z13\). Those change the prescribed
hub neighborhood. The two implementations check this boundary explicitly.

## Reproduction

Python 3.10 or later, standard library only; tested with Python 3.12. There
are no downloaded catalogues, solver dependencies, or symmetry assumptions
in the witness verification.

From the repository root:

```sh
python ramsey_r55_paley_c4_maximality_barrier/verify.py
python ramsey_r55_paley_c4_maximality_barrier/audit.py
python ramsey_r55_paley_c4_maximality_barrier/test_checks.py
```

The first two commands return the same JSON, stored in `EXPECTED.json`,
with status `VERIFIED_CROSS_MAXIMAL_PALEY_C4_COUNTEREXAMPLE`.
The tests exhaust all 1,100 labeled graphs of order at most five, compare
the clique and edge-addition algorithms with literal definitions, and
reject ten malformed certificates in both checkers. Their expected output
is in `EXPECTED_TEST.json`. All three outputs also agree under `python -O`.

The canonical edge encoding is the sorted list of lines `u v\n`, for
\(u<v\), encoded in UTF-8. Its SHA-256 is
`712c705777a536ab819973ac4e20a4e8724a1a741ea7858a660a58b2c4900001`.
The certificate SHA-256 is
`415813f2bb720a6933d7796d4da02c7fb7fb849cb744b1c16fcd8c9eec8859c4`.
`SHA256SUMS` pins the compact publication files.

The finite checks prove properties of this one explicit graph. They do
not independently classify any ambient catalogue. Trust rests on the
displayed finite argument, the two checkers, and Python's integer and set
semantics. The discovery solver is unnecessary for verification.

## Relation to the structural campaign and literature

The [dense four-separator classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_four_separator_classification)
at commit `4bf427dcb479b49978f772e12e55c3cea4711927`, with its
[independent review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_four_separator_review)
at commit `090f667fc53c3e85e81af360ddbd12d974348ae4`, assumes at least
108 edges. The present example does not contradict that theorem. It shows
that the density premise cannot be replaced by maximality of the cross
interface. A proof that forces density, or a complete cover also including
lower-density maximal interfaces, is still needed for that proposed route.

This differs from the [local saturation barrier](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_local_saturation_barrier):
there, a locally valid addition can fail in a global extension; here,
the proposed additions already fail inside the local neighborhood.

[McKay's primary catalogue page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
lists the unique order-17 \((4,4)\) graph. The
[Angeltveit–McKay paper](https://arxiv.org/html/2409.15709v2), Section 2,
describes pointed-neighborhood gluing with the unfilled edges retained.
These are context, not premises for checking the example. A targeted
primary-literature and committed-graph search on 2026-09-06 found no prior
statement of this particular maximal-interface obstruction. That is a
limited novelty check; the claim is the explicit failed completion
mechanism, not a new Ramsey bound or a new catalogue.
