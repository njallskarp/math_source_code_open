# One integrated OPB for all 389 \(M=214\) pair roots

## Theorem and scope

This directory gives one deterministic pseudo-Boolean formula whose
satisfiability is equivalent to the union of all 389 complete pair-incidence
roots at Discovery Net height 3148, and hence to the entire intrinsic
\(M=214\) hard branch for a hypothetical Ramsey \((5,5;43)\) graph.

The formula retains every labeled edge, every red and blue \(K_5\)
prohibition, the forced degree sequence \(20^{13}21^{30}\), all 43 red local
triangle equalities, and every \(a(v)=|N_R(v)\cap E|\geq6\) row. It adds 389
Boolean selector variables and guarded versions of every root condition, then
requires exactly one selector. Thus all five families and all compatible
pair-incidence markings occur in one decision instance; this is not a
collection of selected core pairs or solved subinstances.

No satisfiability or unsatisfiability conclusion is claimed. A SAT result
would still require a directly checked 903-edge coloring. An UNSAT result
would still require a standard proof trace independently replayed against the
exact generated stream.

The 173 MB OPB is generated operational state and is deliberately excluded
from version control. Its exact dimensions and hashes are preserved in
formula_manifest.json.

## Intrinsic base

Use red-edge variables \(x_{ij}\) on \(V=\{0,\ldots,42\}\), followed by
red-triangle variables \(z_{ijk}=x_{ij}x_{ik}x_{jk}\). The labeling follows
the height-3148 root certificate:

\[
E=\{2,\ldots,14\},\qquad
C=\{0,1,15,\ldots,42\}.
\]

The 1,974,689 base rows are the label-neutral height-2505 system before its
old one-anchor units:

- two rows for every five-set, excluding red and blue \(K_5\);
- four conjunction rows for every triangle;
- 43 degree equalities, with degree 20 on \(E\) and 21 on \(C\);
- 43 red local triangle equalities, with totals 93 on \(E\) and 100 on \(C\);
  and
- 43 inequalities \(a(v)\geq6\).

The base-body SHA-256 is
5f160c74a405726503649581080e3127d6a21c25b8fb59f6ffe72740dce600c4.
The independently written C++ checker reconstructs these rows rather than
trusting a copied prefix.

## Selector-gated root union

Let \(y_r\) be the selector for root \(r\), in the exact 389-key order of
height 3148. The formula imposes

\[
\sum_{r=1}^{389}y_r=1.
\]

Every root has 83 anchor-edge units and 43 exact \(a(v)\)-values. Each of the
70 partition-family roots additionally has one anomalous blue-edge unit and
28 equations saying that a central vertex is red to exactly one anomaly.

The guards use no auxiliary variables. For a required unit \(x_e=b\),

\[
\begin{aligned}
b=1&:\quad x_e-y_r\geq0,\\
b=0&:\quad -x_e-y_r\geq-1.
\end{aligned}
\]

For a required equality \(L=t\), where \(0\leq L\leq M\), use

\[
L-t y_r\geq0,\qquad
-L-(M-t)y_r\geq-M.
\]

When \(y_r=0\), both forms are tautologies over Boolean variables. When
\(y_r=1\), they are exactly the requested unit or equality. The audit checks
these truth tables exhaustively for every relevant total. The formula has

\[
1+389(83+2\cdot43)+70(1+2\cdot28)=69{,}732
\]

selector rows.

The anchor units themselves fix the common red degree \(c\in\{9,\ldots,13\}\)
and all eight pair cells. The guarded \(a\)-equalities make both anchors exact
and place the one value-eight or two value-seven anomalies. The partition
guards retain its universal coupling; they are not aggregate substitutes.

## Equisatisfiability proof

Suppose the intrinsic branch has a graph. Heights 3062 and 3130 supply a
red-adjacent ordered pair of doubly exact degree-21 anchors of common red
degree \(9,\ldots,13\). Height 3148 proves that a relabeling puts the adorned
pair-incidence projection in one of its 389 roots. Assign the edge and triangle
variables from the relabeled graph, set that root's selector to one, and set
all other selectors to zero. Every intrinsic and guarded row follows.

Conversely, every OPB model selects exactly one root. Its active guarded rows
become all 83 anchor units, all 43 \(a\)-equalities, and, when applicable, all
29 partition conditions of that root. The unguarded rows supply every
intrinsic graph constraint. The model is therefore a full model of one
height-3148 root and hence a graph in the \(M=214\) branch.

This proves equivalence in both directions. The safe residual signature
ordering from height 3148 is deliberately not imposed here: omitting an
optional symmetry break weakens search but cannot lose a model. No old
one-anchor or selection-order row is mixed with the new labels.

## Exact dimensions and validation

The canonical generated formula is:

~~~text
variables       13,633
constraints  2,044,421
equalities           87
base rows      1,974,689
selector rows     69,732
lines        2,044,422
bytes      172,788,992
SHA-256 469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f
~~~

The 389 root keys have family counts \(60,85,70,104,70\) and SHA-256
de71f59185f53e68dbf4c493609da0fdf3ae4850528eb4c04d437904c747bf4c
when serialized as tab-separated family, \(c\), \(k\), and pattern lines.
They were compared with every key and descriptor in the pinned height-3148
source commit; all 32,287 anchor units, 16,727 \(a\)-equalities, and 1,960
partition equalities agreed.

generate_opb.py writes the entire formula directly. check_opb.cpp imports no
Python code or certificate: it independently enumerates the 389 roots,
reconstructs every base and guarded row, and demands exact line-by-line
agreement through end of file. audit_integration.py independently enumerates
the root census, checks all guard truth tables, and recomputes the formula
dimensions.

Normal and optimized Python runs agree. The C++ checker passed strict Apple
clang 17 compilation, AddressSanitizer, and UndefinedBehaviorSanitizer on the
full stream. Two copy-on-write corrupted streams were rejected at the changed
header and final guarded row.

## Reproduction

From this directory, using CPython 3.12.12 and Apple clang 17.0.0:

~~~bash
set -o pipefail
python3 -B audit_integration.py
python3 -B generate_opb.py --output /tmp/r55_m214_integrated_pair_roots.opb
shasum -a 256 /tmp/r55_m214_integrated_pair_roots.opb
xcrun clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  -isystem /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1 \
  check_opb.cpp -o /tmp/r55_m214_integrated_pair_roots_check
/tmp/r55_m214_integrated_pair_roots_check \
  /tmp/r55_m214_integrated_pair_roots.opb
shasum -a 256 -c SHA256SUMS
~~~

On Linux, omit the macOS SDK -isystem argument. Compare the three compact
program outputs with EXPECTED_OUTPUT.txt.

## Dependencies and trust boundary

The exact root set and its completeness theorem are in the
[height-3148 public source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_normalization),
commit 9a9d4c3234d3fbe196ff4b413df831c587bd7653. The full intrinsic formula
comes from the
[height-2505 source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_formulation).
The pair-existence inputs are the
[five-family cover](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_reanchoring_cover)
and the
[codegree-nine theorem](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_exact_pair_nine).

The codegree-nine theorem was independently checked during this work: its
six-vertex censuses, seven signed triangle coefficients, and strict averaging
margin \(1569-8\cdot196=1\) all reproduce. Its \(U(14)=60\) premise retains
the completeness trust boundary stated by Brendan McKay's
[primary Ramsey catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
The live extrema archive matched SHA-256
9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6,
listed order-14 levels 22, 23, 58, 59, 60, and reproduced the pinned
level-60 member hash.

Trusted are the displayed graph-to-formula proof, the upstream pair-root
coverage theorem, its explicit Ramsey/extremal premises, exact Python and C++
semantics, ordinary hardware, and SHA-256 for provenance. The checkers are
author-written cross-validation, not a proof-assistant theorem or independent
peer review. No solver result, generated OPB, private state, raw dump, binary,
database, or omitted certificate is evidence.

## Next falsifiable step

The complete decision formula is now explicit, but its terminal status remains
open. The next acceptable milestone is either a model checked against every
row and decoded to a 43-vertex coloring, or a standard replayable UNSAT proof
for this exact stream. A timeout, a set of separately solved roots, or another
aggregate relaxation is not completion.
