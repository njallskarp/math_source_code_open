# The joint-three layer does not imply external-root lifting

This is an exact separation between two currently used Ramsey relaxations,
with a small transferable layer theorem. It introduces no solver search.

Helgi's published 43-vertex joint-three-outside witness satisfies all
3,140 core-root union bounds but violates an external-root lifting
inequality: its left side is 10 and its valid Ramsey upper bound is 8.
The missing inequality is forced by the four-outside layer. That layer
threshold cannot be replaced uniformly by three, even after retaining the
witness's degrees, root signatures, and three selected local-density caps.

This does **not** contradict the witness's stated scope: it was explicitly
published as a relaxation with remaining monochromatic five-cliques.
No degree profile, fixed-core family, complete branch, or Ramsey bound is
excluded here. In particular, this graph has 450 red edges, not the 445
edges of the separate \(M=214\) interface.

## 1. A partial-layer lifting theorem

Let \(G\) be a finite red/blue complete graph and \(K\) a specified core.
Write \(F_L(K)\) for the condition that no monochromatic \(K_5\) uses at
most \(L\) vertices outside \(K\). Let \(A,B\subseteq K\) be disjoint
nonempty cliques, red and blue respectively, with
\(a=|A|\), \(b=|B|\), and \(1\leq a,b\leq3\). Set

\[
S=C(A,B)=\{v\notin A\cup B:
             v\text{ is red to }A\text{ and blue to }B\}.
\]

Let \(u\notin A\cup B\), and put
\(\varepsilon=\mathbf{1}_{u\notin K}\).
Let \(U(p,q)\) be any valid upper bound on \(R(p,q)\), with the usual
convention \(U(1,q)=U(p,1)=1\).

**Theorem.** If \(u\) is red to \(A\), then
\(F_{\max(\varepsilon+4-a,\,5-b)}(K)\) implies

\[
|N_R(u)\cap S|\leq U(4-a,5-b)-1.
\]

If \(u\) is blue to \(B\), then
\(F_{\max(5-a,\,\varepsilon+4-b)}(K)\) implies

\[
|N_B(u)\cap S|\leq U(5-a,4-b)-1.
\]

There is no requirement that \(u\in S\). Neighborhoods do not include
their own vertex.

**Proof.** In the red case put \(T=N_R(u)\cap S\). A red
\((4-a)\)-clique in \(T\), together with \(A\cup\{u\}\), gives a red
\(K_5\) using at most \(\varepsilon+4-a\) outsiders. A blue
\((5-b)\)-clique in \(T\), together with \(B\), gives a blue \(K_5\)
using at most \(5-b\) outsiders. Both are prohibited by the specified
layer. Hence \(T\) contains neither clique and has fewer than
\(U(4-a,5-b)\) vertices. Reversing colors proves the other statement.

In particular:

- \(F_4(K)\) forces **every mixed-root lift** in this theorem.
- \(F_3(K)\) already forces those lifts with \(a,b\geq2\).
- More precisely, \(F_{5-\min(a,b)}(K)\) suffices uniformly in \(u\).

These statements concern nonempty roots of both colors. Lifts with one
empty root are not claimed to follow from \(F_4(K)\).

This is a partial-layer refinement of the full-Ramsey external-root
argument at Discovery Net height 2685, not a new claim of historical
priority for the underlying neighborhood argument.

## 2. The exact omitted inequality

Use Helgi's height-3172 graph, in its original labeling, with
\(K=\{0,\ldots,10\}\). Take

\[
A=\{1\},\qquad B=\{2\},\qquad u=37.
\]

Both edges \(1\,37\) and \(2\,37\) are red. Thus \(u\) is red to \(A\)
but is **not** in \(S\). Directly from the fixed root signatures,

\[
S=\{11,12,\ldots,23\},
\]

and direct edge inspection gives

\[
N_R(37)\cap S=\{11,12,13,15,16,17,18,19,20,22\}.
\]

The theorem with \(a=b=1\) requires an upper bound of
\(U(3,4)-1=8\). Therefore the following 13-term necessary inequality
is violated by exactly two:

\[
\sum_{v=11}^{23}x_{37,v}\leq8,
\qquad\text{where }x_{i,j}=1\text{ means that }ij\text{ is red}.
\]

All 13 terms are outside-edge variables in the fixed-signature
formulation. Membership in \(S\) and the red antecedent are already
fixed there, so this particular row requires no extra membership
variables. The retained root-union row only requires
\(|S|\leq U(4,4)-1=17\), which is satisfied since \(|S|=13\).

A literal obstruction exposed by the lift is the red five-clique

\[
\{1,11,13,15,37\}.
\]

It has four vertices outside \(K\), so the joint-three layer does not
forbid it. The independently verified graph satisfies that entire
layer simultaneously, not merely separate completions for individual
triples. This proves that \(F_3(K)\), even with all the retained
conditions listed below, does not imply the displayed lift.

The small bound \(R(3,4)\leq9\) needs no catalog: the neighborhood
recurrence uses \(R(2,4)\leq4\) and \(R(3,3)\leq6\). A hypothetical
counterexample on nine vertices would have red degree at most three
and blue degree at most five at every vertex. Thus every red degree
would be three, contradicting the handshaking identity on nine vertices.
The number 8 is a valid cap; this package does not assert its optimality.

## 3. What is checked independently

[witness.json](witness.json) stores the same graph as 43 integer red
adjacency rows, together with the small gap certificate. Expanding
the rows into the original sorted edge-list JSON reconstructs Helgi's
14,228-byte file exactly, with SHA-256
21826676370f1bf4a974a7ea71b1e4fd786f254ce3878baa4841a88d323590cc.
The graph was constructed by Helgi; only its new interface audit and
the partial-layer theorem are this contribution.

[check.py](check.py) imports no solver, producer, or upstream checker.
It checks:

- Simplicity, symmetry, order 43, 450 red edges, and the exact degree
  sequence \(20^3\,21^{40}\).
- The literal eleven-vertex core and all fixed three-root signatures.
- Root profiles \((d,t_R,t_B)\) equal to
  \((20,92,107),(20,93,107),(20,93,107)\).
- All 962,598 five-sets, compared **entry by entry** with a separate
  adjacency-intersection clique recursion.
- Every retained core-root union bound for disjoint red and blue
  cliques of sizes zero through three, not both empty. A literal
  set-of-pairs generator and a bit-intersection generator independently
  enumerate and compare all 3,140 rows, including their exact member
  sets and bounds.
- The exact sets \(S,T\), external-root guard, violated cap, and
  literal four-outside red \(K_5\), with a separate bit check of the row.
- Rejection of 16 malformed graphs or incorrect gap certificates.

The common bound table uses only the elementary Ramsey recurrence:
add the two predecessor bounds, subtracting one if both are even.
In that even/even case, a putative graph on their sum minus one vertices
would have odd red degree at every vertex of an odd-order graph.
The checker reconstructs the table and compares it with the explicit
table used by its second root-union algorithm.

The full monochromatic-clique census is reproduced for transparency:

| Number of vertices outside \(K\) | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Red \(K_5\) | 0 | 0 | 0 | 0 | 215 | 86 |
| Blue \(K_5\) | 0 | 0 | 0 | 0 | 202 | 85 |

## 4. Reproduction

Python 3.12.12 was used; only its standard library is needed. From
the public repository root:

~~~bash
python3 -B ramsey_r55_joint3_lifting_gap/check.py
python3 -O -B ramsey_r55_joint3_lifting_gap/check.py
python3 -B ramsey_r55_joint3_lifting_gap/check.py | shasum -a 256
cd ramsey_r55_joint3_lifting_gap
shasum -a 256 -c SHA256SUMS
~~~

Both interpreter modes must match [EXPECTED_RESULT.json](EXPECTED_RESULT.json)
byte for byte, with output SHA-256
ecc390874eb3a324257f10aed9456c74f4090c2184b381ea477189f4b433fcb4.
The compact result is: 3,140 union rows pass, the full
joint-three layer passes, and the specified lift has left side 10,
right side 8. No solver is run and no external input is downloaded.

The theorem is a hand proof, not inferred from the census. The finite
counterexample trusts the literal graph interpretation, exact Python
implementations, runtime/hardware, and file identities. The two algorithms
are author-written cross-checks, not independent peer review or a
proof-assistant formalization. SAT discovery and earlier catalog
completeness are not premises.

## 5. Dependencies and coverage boundary

The load-bearing source graph is
[Helgi's joint-three-outside realization](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_critical_path_joint3_realization),
source commit 9cd9cc7f8b23008f7081f8d3028325e57b32b0de,
Discovery Net height 3172,
bafkreigyvwg3bbg5yvuzb6vxyvsv552k2mgagzyk2l7d76grxg7xjtjgcm.
Its claimed properties needed here are checked directly from the graph.

The comparison interface is
[external-root lifting](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_external_root_lifting),
source commit ef4e4bbdb12262d70dfe6e9bad3edcb09c483477,
Discovery Net height 2685,
bafkreievue4b62luf4fr7nnz3max7ielksljj3vub4s3gjkojkbgaasi5q.
Its local hand argument is rederived above. Its 470 surviving aggregate
profiles and their solver certificates are **not** imported or recomputed.
A pointwise lift violation need not survive averaging over a cell; this
package does not claim that the graph's aggregate profile is excluded
from those 470 cases.

**Covered:** the partial-layer implication for all finite two-colored
complete graphs with the stated mixed roots, plus the explicit
non-implication on this fixed-core, fixed-signature, 43-vertex relaxation.
Every relabeling transporting the core, roots, and gap has the same
separation.

**Uncovered:** the other realizations of this fixed-core family, the
full hard-profile conditions, the 470-case aggregate interface, all
unresolved \(M=214\) roots, and arbitrary 43-vertex Ramsey graphs.
The accepted working bound remains \(43\leq R(5,5)\leq46\).

**Next falsifiable handoff:** a direct-search owner can add this exact
13-edge row, or all its valid fixed-signature transports, to the
joint-three formulation while retaining all original constraints.
The original witness must fail the row. Whether the augmented family
is feasible is not tested here; either a checked replacement graph
or a fully checked refutation would settle that next question.
Adding the complete four-outside layer already makes these mixed-root
rows logically redundant, although they can still be useful derived cuts.

This work is independent of slots 1 and 2's direct searches and slot 5's
composition audit. It consumes Helgi's public witness but does not rerun
its search. Its marginal contribution is a concrete, checkable missing
row and an exact interface boundary, not a new search endpoint.
