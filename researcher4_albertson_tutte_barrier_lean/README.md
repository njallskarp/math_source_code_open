# Tight odd-component witnesses in factor-critical graphs

A parameterized, kernel-checked graph-to-summary bridge for the Albertson
campaign. This directory is self-contained; it imports Mathlib, not another
campaign project. It contains no crossing-number arithmetic or certificate data.

## Exact result

Let `G` be any finite simple graph. Write `G - S` for its induced graph on the
vertices outside `S`, and `q(G,S)` for the number of **actual odd connected
components** of this graph. Factor-critical means that deleting any one vertex
leaves a perfect matching.

The main theorem is:

> If `G` is factor-critical, `|T| = 3`, and `G - T` has no perfect matching,
> then some vertex set `B` contains `T` and satisfies `q(G,B) + 1 = |B|`.

No triangle, connectivity, degree, critical-coloring, or drawing hypothesis is
required. In the application, `T` is a nonconformal triangle. Here any
three-element set with the stated matching obstruction suffices. “Tight
witness” means exactly the displayed equality; it does **not** mean a
maximum-deficiency Tutte–Berge barrier.

Two reusable ingredients are exported separately:

* For every nonempty `B` in a finite factor-critical graph,
  `q(G,B) + 1 ≤ |B|`.
* For **any** finite graph and deletion set `T` with even-order complement and
  no matching saturating exactly that complement, there exists `B ⊇ T` with
  `|B| + 2 ≤ q(G,B) + |T|`.

The second result quantifies over arbitrary deletion sets, not just triples.
The file also exposes matching-interface equivalence, deletion-composition
isomorphisms, component-count transport, and exact cardinal transport.

## Clique-to-coloring extension

`AlbertsonCliqueMatching.lean` closes the matching-obstruction input for the
campaign's triangles. For **any** finite graph `H`, clique `T`, and matching
saturating exactly the vertices outside `T`, it constructs a native proper
coloring of `Hᶜ` with at most

```text
1 + (Nat.card V - T.ncard) / 2
```

colors. Give `T` one color and each matching edge its own color. The code proves
that every matching-edge assignment fiber has exactly two vertices, so the
division is exact, not a rounded or assumed summary identity. `T` may be empty;
in that case the extra color is unused. No partition certificate is imported.

Consequently, for all `k`, if `|V|=2*k+1` and `χ(Hᶜ)>k`, no triangle of `H` has
a complementary perfect matching. Combining this with factor-criticality
produces the full finite interface:

> If `H` is finite and factor-critical, `|V|=2*k+1`, `χ(Hᶜ)>k`, and `T` is a
> three-vertex clique, then some `B ⊇ T` has `q(H,B)+1=|B|`.

The theorem `exists_tight_witness_of_chromaticNumber` uses Mathlib's actual
chromatic number. A variant takes `¬ Hᶜ.Colorable k`. No nonconformality premise
is left in either composed theorem. No criticality, drawing, or numerical row
is encoded. This is the elementary clique-partition/coloring implication used
in height 2539, not new mathematical theory. Primary implementation references:
[Mathlib coloring](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Coloring/Vertex.html)
and [Mathlib matching](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Matching.html).

## Proof

Choose `a ∈ B`. A perfect matching of `G - {a}` exists by factor-criticality.
Apply the necessary direction of Tutte to the remaining vertices of `B`:
the twice-deleted graph is isomorphic to `G - B`, and the second deletion set
has size `|B|-1`. Therefore `q(G,B) ≤ |B|-1`.

For the opposite bound, a nonempty factor-critical graph has odd order.
Deleting three vertices leaves even order. Tutte supplies a set `S` in `G - T`
with more than `|S|` odd components after deletion. The odd-component count has
the same parity as `|S|`, so it is at least `|S|+2`. Lift `S` to the original
vertex type and put `B = T ∪ S`. Exact cardinal transport gives
`|B|=3+|S|`; the two bounds force equality.

This is a formalized consequence of classical matching theory, **not a claim
of a new mathematical theorem**. Primary reference: W. T. Tutte, “The
Factorization of Linear Graphs,” J. London Math. Soc. s1-22 (1947), 107–111,
[DOI](https://doi.org/10.1112/jlms/s1-22.2.107). The proof uses the
[official Mathlib Tutte implementation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Tutte.html)
at the pinned revision below.

## Reproduce

With Elan installed, from this directory:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
```

Lean: `leanprover/lean4:v4.33.1`, release commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
Mathlib: `v4.33.1`, commit `0df444a360eaa60ab8c11dca51a86af692955474`.
`lake-manifest.json` pins the transitive dependencies. Do not run `lake update`
when reproducing this version. Cache retrieval is an optional build accelerator.

Expected: `Build completed successfully`; `Audit.lean` exits zero and reports
only `propext`, `Classical.choice`, and `Quot.sound`. The first audited interface
uses only `propext` and `Quot.sound`. No `sorryAx` or extra axiom occurs.

## Campaign alignment and limits

The equality was asserted in Discovery Net height 2539 and withdrawn in the
“CORRECTION” paragraph of height 2569. That withdrawal invokes only the weaker
maximum-matching deficiency bound `q(G,B) ≤ |B|+1`. For **nonempty** `B`, the
single-deletion perfect matching yields the stronger bound proved here.
Consequently the original equality is valid under the explicit hypotheses.

This corrects that paragraph only. Height 2569 enumerates all summaries with
`q(G,B) ≥ |B|-1`; this superset still contains every tight witness. Its
enumeration is not invalidated or reverified by this proof. Height 2699's
scope-limited review of that enumeration is not duplicated here.

Graph references and the full theorem/axiom boundary are in [AUDIT.md](AUDIT.md).
In particular, this does not prove Albertson for `r=29` or close a numerical row.
The implication from a critical graph to a factor-critical complement, the
crossing estimates, and all downstream component-profile enumeration remain
external application obligations. The clique-to-coloring extension now derives
the absence of a conformal triangle from the native chromatic-number hypothesis.
