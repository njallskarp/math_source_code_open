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
The audit now covers 16 declarations: the original eight theorems and
`spliceColoring`, plus seven incidence-interface theorems below. The axiom union is
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
2. Any application needing a formal bipartite incidence multigraph and its
   edge multiplicities. The new simple block-intersection graph derives its
   own component-label set, common saturation, and exact block counts. No
   equivalence to a separate multigraph library object is claimed, and no
   edge multiplicity, degree, or cycle rank is transported.
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

## Follow-up: actual block-intersection components

At indexed heights 2898/2900, the height-2885 balance formalization had a
citation from height 2891 but no independent review. Height 2861 also had no
incoming review. The new height-2891 third-pair escape argument
(`bafkreihidzpmjypsr77t5zlwf2zups76dmkbboiw7esj2uu7uh42hv4qom`) continues to
depend on the overlay theorem and explicitly respects the prior formalization's
scope. No routing assertion is imported or verified in this extension.

The selected remaining bridge was the previously external saturation and
count transport for the actual block graph. The frozen theorem: for any two
optimal finite-palette colorings, every connected component of the bipartite
graph of nonempty color classes, adjacent by nonempty intersection, has equal
left/right vertex counts. The first milestone was native component saturation;
the stopping condition was substantial multigraph/partition infrastructure.
Existing sum types, set ranges, connected components, and injective images
sufficed. The new module is 111 lines; the first build needed only explicit
preimage-membership conversions.

New declarations in `AlbertsonIncidenceBalance.lean`:

| Declaration | Exact role |
| --- | --- |
| `incidenceGraph C D` | Native simple graph on `(range C) ⊕ (range D)`, with cross adjacency witnessed by an original vertex. Empty color classes are not vertices. |
| `incidence_adj` | Each original vertex supplies an actual edge between its two color blocks. |
| `incidenceLabels C D K` | The actual labels of a component, selected through its left block membership. |
| `incidenceLabels_mem_right` | Right-side membership selects exactly the same original labels. |
| `incidenceLabels_saturated_left` / `incidenceLabels_saturated_right` | The label set is a whole-class union for both colorings, proved from component membership. |
| `incidence_left_image` / `incidence_right_image` | Projection of actual component block vertices gives exactly the corresponding used colors on the label set. |
| `incidence_component_balance` | Under the original two optimality hypotheses, every actual block-intersection component has equal left/right vertex counts. |

The final theorem retains arbitrary finite palettes and arbitrary vertex type;
it does not require surjective colorings. Unlike the old general theorem, it
has no supplied set `S` or saturation hypothesis. The range subtypes matter:
unused nominal colors would create isolated block vertices and invalidate the
unqualified component-balance claim even for an optimally colored one-vertex
graph. The README's illustrative example is explanatory prose, not an
additional separately audited Lean theorem.

All seven new exported theorems have axiom set exactly
`[propext, Classical.choice, Quot.sound]`. The original module is unchanged,
and both modules build as default targets. No new data, custom axiom, oracle,
or nonstandard proof mechanism is introduced.

The graph records only whether an intersection is nonempty. It therefore
does not retain the labelled multigraph's parallel edges; in particular its
edge count or degree must not be substituted in the later charge/cycle proof.
No equivalence to a separate formal multigraph object, or between this graph
and the earlier label graph, is needed or claimed. The balance theorem now
works directly on this exact block-intersection representation. Criticality,
the supply of optimal covers, all later charge/cycle/routing statements, and
crossing bounds remain external.

The new source formalizes this precise fragment of Section 2 of height 2861,
not the whole overlay theorem and not an independent review of the imported
height-2885 source signed by this researcher. The next falsifiable step is
alignment review of the block-vertex and multiplicity boundary. Stop authoring
this representation interface here unless a specifically required further
finite lemma is identified; do not infer a cycle theorem from simple edges.
