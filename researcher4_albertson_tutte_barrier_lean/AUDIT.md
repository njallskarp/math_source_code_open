# Theorem alignment and trust audit — 2026-09-05

## Frozen selection

The human requested a reusable Albertson graph-to-summary bridge, not another
row-specific scalar instantiation. The selected implication is Tutte witness
extraction from an actual factor-critical graph after a nonconformal triple
deletion. Mathlib already has matchings, induced graphs, connected components,
odd-component parity, and Tutte's theorem. Gallai-block soundness would first
require a graph/block-decomposition API; the broader one-triple Kempe route
would introduce new coloring structure. Neither is developed here.

Graph dependencies inspected before coding (references, not Lean axioms):

* Height 2539, matching-barrier dichotomy:
  `bafkreigq45vyowvg6vn62apr6xv5orshf3k4jybmft3ypqfjah6tntc4eq`.
  The tight-witness equality is the precise fragment formalized.
* Height 2569, separator certificate and prose withdrawal of equality:
  `bafkreidvo7xirljsxtmz6udphiluggng3zfvz5gvduw4pqxmhycd4le7pu`.
  The withdrawal is corrected, not the certificate's permissive enumeration.
* Height 2699, independently accepted r=28 separator classification:
  `bafkreid4n5smkci3gi722sjgaaiy7jz5stkcxkb7v3krhn6xff3rweelne`.
  This review uses only the weaker lower bound and is not repeated here.
* Height 2599, this researcher's prior conformal-separator formalization:
  `bafkreif53fm4al62vqssmpbx6d3ojc3itv2iqjo42waracwjlne2ujscam`.
  The matching-subgraph definitions agree after unfolding. That file and its
  singleton-separator theorem are not imported or republished.

Duplicate/status refresh at indexed height 2808 found no existing formalization
of this extraction. This contribution is an authoring/formalization result,
not an independent review of an artifact signed by this researcher.

## Exact Lean interface

All declarations below are in namespace `AlbertsonTutteBarrier`.

| Declaration | Formal meaning |
| --- | --- |
| `HasMatchingOff G S` | A native matching subgraph has vertex set exactly `Sᶜ`. |
| `FactorCritical G` | `∀ a, HasMatchingOff G {a}`. Vacuous on an empty type; the main theorem's triple guarantees nonemptiness. |
| `oddCount G S` | `ncard` of Mathlib's odd connected components of `G.induce Sᶜ`. Not an unconstrained summary variable. |
| `hasMatchingOff_iff` | Equivalence with a native perfect matching on the induced complement. |
| `tutte_iff` | Mathlib Tutte transported to the induced-complement interface. |
| `oddCount_delete` | Deleting `R`, then a subtype set `S`, equals deleting `R ∪ Subtype.val '' S` for odd-component counts. |
| `ncard_union_image_remaining` | The union has cardinality `R.ncard + S.ncard`. |
| `exists_oddCount_gap_two` | No perfect matching in an even-order graph yields `S.ncard + 2 ≤ oddCount G S`. |
| `FactorCritical.oddCount_add_one_le` | For every nonempty `B`, `oddCount G B + 1 ≤ B.ncard`. |
| `FactorCritical.odd_card` | A nonempty finite factor-critical graph has odd order. |
| `exists_deletion_witness` | For arbitrary `T` with even complement and no matching off `T`, some `B ⊇ T` has `B.ncard + 2 ≤ oddCount G B + T.ncard`. |
| `exists_tight_witness_of_three_deleted` | Under finite factor-criticality, `T.ncard = 3`, and no matching off `T`, some `B ⊇ T` satisfies `oddCount G B + 1 = B.ncard`. |

The graph isomorphisms and component/cardinal equalities are proved, not assumed.
No independent summary-to-graph realization assumption is hidden in the result.
The extraction is classical existential, not an executable barrier-finding
algorithm or an enumeration of all component-size multisets.

## Axioms and reproducibility

`lake build` succeeds without warnings. `lake env lean Audit.lean` audits the ten
original interface/main theorems plus the eight extension declarations listed
below; their axiom union is exactly:

```text
propext, Classical.choice, Quot.sound
```

`hasMatchingOff_iff` uses only `propext` and `Quot.sound`. No theorem uses
`sorryAx`, `Lean.ofReduceBool`, a user-declared axiom, `sorry`, `admit`,
`native_decide`, or an unsafe shortcut. No external data file is consumed.
Trust comprises Lean's kernel, the stated standard axioms, the pinned Mathlib
dependencies, and the ordinary toolchain. All mathematical matching and Tutte
bridges used here are proved in these sources/dependencies.

The project was built with Lean 4.33.1 and Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`. Development reused dependency caches
inside this researcher's workspace; this is a build convenience, not a source
dependency. Public source excludes `.lake` and all binaries/caches.

## External Albertson interfaces not closed

Applying the result to a complement `H` of a critical graph still requires:

1. The theorem (e.g. the campaign's use of Stehlík) giving factor-criticality of
   the relevant complement. It is a hypothesis here, not imported as an axiom.
2. A three-vertex clique and the chromatic-number/order hypotheses. The extension
   below now derives the absence of a complementary perfect matching from these
   native graph properties; no separate nonconformality assumption is needed.
3. Conversion of actual components into the downstream enumerator's complete
   size/degree/edge summary, including every filter's soundness and exhaustion.
4. All drawing/topology, crossing-number estimates, critical-graph reductions,
   and numerical contradictions.

Thus this closes one load-bearing finite graph implication, not the Albertson
conjecture or a complete r=29 row. It does not count toward a successful r=29
numerical feasibility gate.

## Next falsifiable handoff

Researcher 3/principal can replace the permissive witness hypothesis by the
proved equality when auditing the existing route. Continue only if a specific
downstream argument needs that strength; otherwise this interface is complete.
No new profile enumeration or coloring/topology library is warranted merely to
extend this pass. An independent alignment review should check the scoped
correction against the exact assumptions at heights 2539 and 2569.

## Follow-up: clique plus matching to a native coloring

The next status pass (indexed height 2822) found no incoming review of height
2815 (`bafkreiara6fa3x2lzk2tl5whq3laozphrrqbbbzxfrhn5pzhzz5mf4avv4`). It did not
re-review that author-signed result. Instead, it closed the separate elementary
clique-cover implication explicitly used in branch 2 of height 2539, thereby
removing one external application premise of the previous interface.

The r=29 numerical gate remained paused. Researcher 3's height-2805
conformal-diamond/Hall-capacity theorem
(`bafkreih4hp5a22mphxzsxf7vkh5fgtmb64iiuw4ktwhzashv7yjictrchy`) was inspected;
its cross-diamond capacity condition remains a separate open input and is not
encoded or reviewed here. The present construction has no Kempe path or
subdivision representation and no numerical application to a surviving row.

The frozen informal target was a clique `T` plus a matching on its complement
giving `1+(|V|-|T|)/2` colors to the complementary graph. The first milestone
was an actual `SimpleGraph.Coloring`, not a scalar color count. The pivot
condition was substantial new matching/partition representation work. Mathlib's
existing `IsMatching.toEdge`, two-vertex fibers, and `Coloring.mk` made that
unnecessary. The prototype and composed theorem compile.

New declarations in `AlbertsonCliqueMatching.lean`:

| Declaration | Exact role |
| --- | --- |
| `matching_toEdge_ne_of_compl_adj` | Complement-adjacent vertices receive distinct matching-edge colors. |
| `cliqueMatchingColoring` | A proper coloring with palette `Option M.edgeSet`: `none` for `T`, `some e` for edge `e`. |
| `matching_edge_fiber_ncard` | Each assignment fiber is the actual pair of edge endpoints; size two, even for an infinite ambient type. |
| `matching_verts_ncard` | For finite ambient type, `M.verts.ncard = 2*M.edgeSet.ncard`, proved by finite fiber counting. |
| `colorable_compl_of_clique_matching` | For arbitrary clique `T` and matching off `T`, `Hᶜ.Colorable (1+(Nat.card V-T.ncard)/2)`. |
| `no_matchingOff_triangle_of_not_colorable` | At order `2*k+1`, `¬ Hᶜ.Colorable k` rules out a complementary matching for every three-clique. |
| `exists_tight_witness_of_triangle` | Factor-criticality plus the preceding coloring obstruction gives the actual tight set `B`. |
| `exists_tight_witness_of_chromaticNumber` | The same conclusion with `(k : ℕ∞) < Hᶜ.chromaticNumber`. |

The matching cardinality and division are proved from the graph, not imported
from a count table. The sole custom predicates (`FactorCritical`,
`HasMatchingOff`, `oddCount`) retain their already audited native-graph meaning.
All eight new audits, including the coloring construction itself, use only
`propext`, `Classical.choice`, and `Quot.sound`. No extra data or trust mechanism
is introduced. Both source modules are built by the default Lake target.

For Albertson order `2*r-1`, substitute `k=r-1` with the relevant natural-number
side conditions. The theorem still does not derive factor-criticality from
criticality, enumerate component summaries, or prove a crossing-number bound.
The strongest current endpoint is the exact finite triangle-to-Tutte-summary
implication. Its next useful test is external alignment review, not another
arithmetic instantiation or a reopening of the r=29 feasibility gate.
