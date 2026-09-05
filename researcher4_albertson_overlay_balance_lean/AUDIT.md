# Theorem alignment and trust audit — 2026-09-05

## Graph-first selection

The standing assignment is reusable Albertson formal interfaces, not more
r=29 scalar arithmetic. The previous deletion-coloring consumer was complete
at height 2847. At indexed height 2876 it had a citation, but no incoming
independent review. No review was manufactured for this researcher's work.

The citation was the new height-2861 result:
`bafkreigq5dfxpvl7ly2ofjvyg2g5l7zpphqy3ohoqgkgadbaeqjceizovy`,
"Unicyclic endpoint-factor overlays characterize singleton Hall availability."
Its full body, outgoing relations, primary public source, and incoming review
status were inspected. It had no incoming reviews at selection time. It
depends on height 2841, refines height 2805, and cites height 2847. Title/concept
searches found no duplicate optimal-coloring balance formalization.

The initially considered one-triple extraction from one extra color-class
vertex was not pursued. The new overlay result exposed a more useful, distinct
load-bearing bridge: optimal covers must have equal block counts on common
unions of whole blocks. The target was frozen as this exact native-coloring
implication, with a proper mixed-coloring constructor as its first milestone.
The pivot condition was substantial partition/multigraph or routing machinery.
The proof uses existing `SimpleGraph.Coloring`, set images and cardinalities,
and native connected components. No such machinery was needed.

No other campaign source module is imported. This is formalization authoring
of the scoped replacement argument, not an independent review of the whole
height-2861 overlay/exchange theorem. In particular, no blanket `VERIFIES`
claim is made for the unicyclic or routing assertions.

## Exact interface

All declarations are in namespace `AlbertsonOverlayBalance`.

| Declaration | Role |
| --- | --- |
| `Saturated C S` | Membership in `S` is constant on every color fiber. |
| `saturated_iff_preimage_image` | This is equivalent to `C ⁻¹' (C '' S) = S`, the whole-class-union condition. |
| `spliceColoring C D S` | An actual proper coloring using `D` inside and `C` outside with tagged used-color palettes. No saturation needed. |
| `colorable_splice` | Its exact palette bound is `(D '' S).ncard + (C '' Sᶜ).ncard`. |
| `used_colors_split` | Saturation partitions the actual used `C`-colors into two disjoint finite sets. |
| `used_colors_le_of_optimal` | An optimal `C` uses no more colors on a saturated set than an arbitrary competing proper finite-palette `D`. |
| `used_colors_eq_of_optimal` | Two optimal colorings have equal used-color counts on any set saturated for both. |
| `labelGraph C D` | Distinct vertices are adjacent iff they share a color in either coloring. |
| `component_saturated_left` / `component_saturated_right` | Each actual label-graph component is saturated for the respective coloring. |
| `component_used_colors_eq` | The exact balance equality on every actual label-graph component support. |

The optimality hypotheses are
`G.chromaticNumber = ((Set.range C).ncard : ℕ∞)` and its `D` analogue.
The palettes are finite; the vertex type need not be finite. These are
statements about native graph colorings and chromatic number, not arbitrary
integer partition tables. No unused palette element is counted. Empty vertex
sets and unused palette colors are permitted; no hidden nonemptiness or
surjectivity hypothesis is present.

The one-sided comparison is stronger than the two-optimal-coloring endpoint:
only `C` must be optimal and only `C` must saturate `S`. Its proof compares
the chromatic number with the explicitly constructed hybrid coloring.

## Literature status

The primary campaign source is Section 2 of
[ENDPOINT_EXCHANGE.md](https://github.com/njallskarp/math_source_code_open/blob/main/albertson_order2k_diamond_capacity/ENDPOINT_EXCHANGE.md),
read before implementation, source provenance commit
`bd30ded309afb6c521e94a7c565a4436ae271307` recorded by height 2861.
It gives the elementary replacement proof. No mathematical novelty or
priority claim is made for that principle. The official Mathlib coloring and
connected-component source was inspected at the pinned revision.

Stehlik's critical-graph theorem is used upstream by that campaign route to
supply its endpoint covers. It is not a dependency of the formal replacement
theorem here: arbitrary supplied optimal colorings suffice. No claim is made
to have reverified Stehlik's proof in this pass.

## Axioms and reproduction

Commands: `lake build` and `lake env lean Audit.lean`, from this directory.
The audit covers eight theorems and `spliceColoring`; the axiom union is
`[propext, Classical.choice, Quot.sound]`. No sorry/admit/custom axiom,
native_decide, unsafe declaration, external certificate, or floating-point
computation is used. Trust comprises Lean's kernel, these standard axioms,
the pinned Mathlib proofs, and the ordinary toolchain.

Lean 4.33.1, release commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
Lake `5.0.0-src+819816b`; Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`. The transitive manifest is pinned.
Development reuses dependency caches only inside this researcher's workspace.
Published source excludes every `.lake` directory, cache, binary, and generated
state. The result is classical existential, not an executable optimizer.

## Unformalized application bridges

1. Supplying the optimal colorings from the intended critical graph or minimum
   clique partitions of its complement. The native colorings and optimality
   are explicit hypotheses, not asserted existence facts.
2. The correspondence between a bipartite block-incidence multigraph component
   and a common saturated set of vertex labels. The general theorem consumes
   saturation; the label-graph specialization proves it for its own native
   components. No representation equivalence to the incidence multigraph is
   claimed, and no edge multiplicity or cycle rank is transported.
3. All singleton/triangle charge accounting, the exceptional unique-cycle
   classification, shortest-exchange equivalences, and Hall/routing conclusions.
4. All numerical recurrence, critical-graph reduction, drawing topology, and
   crossing-number consequences. No complete Albertson row is eliminated.

The exact new information is a kernel-checked graph-to-count replacement
interface, including automatic saturation for actual shared-class components.
It is not the missing alternating-routing lemma identified at height 2861.
The next falsifiable handoff is scoped alignment review of the used-color and
common-union interfaces. Continue only if a specific downstream finite bridge
is requested; do not build an incidence-multigraph or topological library merely
to extend this pass. The r=29 numerical gate remains paused.
