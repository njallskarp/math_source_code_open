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

`lake build` succeeds without warnings. `lake env lean Audit.lean` audits ten
interface/main theorems; their axiom union is exactly:

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
2. A three-vertex set whose deletion has no perfect matching. A nonconformal
   triangle supplies it, but the critical-coloring argument that forbids a
   conformal triangle is not formalized here.
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
