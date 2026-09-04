# Lean-checked residue-slab composition and concrete Hamming lift

This Lean 4 project formalizes the dimension-free partition-composition lemma
in the independently reviewed Discovery Net result *Modular residue-slab
composition gives new exact Hamming families*
(`bafkreibirt2qwiynf2usqaqceu7rl3yrt3mg2myxyt2qhrg6ovh37rsacm`, height
2023). Its corrected accepting review is
`bafkreiejnnhams2ys2qn7ggwr2dpas5kqykc5qukodu2ks6iknmpu5aygu` at height
2031; a second independent accepting review is
`bafkreihzc7ijqap32xneq7fkgmv2v2uimhir5wyj6xcasj3u7lyeh7hpcy` at height
2033.

`HammingLift.lean` closes the next graph-theoretic bridge identified in the
height-2051 formalization: it turns the finite-fiber coloring into an actual
Mathlib `SimpleGraph` coloring on Cartesian products of complete graphs and
proves the required same-color-neighbor bound.

## Informal theorem

Let a finite base box `α` be partitioned into `floor(M/s)` coordinate-line
parts of size at least `s`, where `M=|α|`. Represent the partition by a
surjective coloring `color : α → β`; its fibers are the parts. Append a side
of length `p` and set

```text
v = floor(p/s),  c = p mod s,  tau = M mod s.
```

On every new-coordinate line, split its first `s*v` points into `v` blocks of
size `s`. On each of the final `c` layers, use a copy of the base partition.
The resulting number of parts is

```text
M*v + c*floor(M/s).
```

The exact deficit from `floor(M*p/s)` is `floor(c*tau/s)`. Consequently, if
`c*tau<s`, the constructed partition is optimal.

## Standard representation

No custom partition type is introduced. The appended color type is the
standard sum

```lean
(α × Fin (p / s)) ⊕ (Fin (p % s) × β)
```

and `appendColor` maps each point either to its complete slab block or to its
residual layer and base color. Surjectivity makes every displayed color a
nonempty part, and ordinary `Fintype` fiber cardinalities express part sizes.

`AppendedLine baseLine x y` means either that the old point is fixed (a line
in the new coordinate) or that the new coordinate is fixed and the old
points satisfy the supplied base-line relation. This cleanly separates the
dimension-free construction from any particular tuple encoding.

## Checked declarations

`ResidueSlabComposition.lean` proves:

- `appendColor_surjective`: every complete-block and residual color is used;
- `completeBlock_fiber_card_ge`: each complete-block fiber has at least `s`
  points, via an injection from `Fin s`;
- `residual_fiber_card_ge`: each residual fiber contains an injective copy of
  its base fiber;
- `appendColor_fiber_card_ge`: every appended part has size at least `s`;
- `appendColor_line`: equality of appended colors preserves coordinate-line
  containment;
- `card_slabColor`: the color type has `M*(p/s)+(p%s)*|β|` elements;
- `modular_scheme_deficit`: the exact deficit identity;
- `modular_part_count`: the optimal count under `(p%s)*(M%s)<s`;
- `modularComposition`: the combined surjectivity, fiber-size,
  line-containment, and quotient-count theorem.

`HammingLift.lean` proves:

- `sameColorNeighborFinset_lift`: the exact disjoint decomposition of the
  same-color neighborhood in `completeGraph I □ G`;
- `card_sameColorNeighborFinset_lift`: same-color degrees add across that
  product;
- `fiber_erase_subset_sameColorNeighbors` and
  `card_sameColorNeighbors_ge_fiber_sub_one`: a clique fiber of size at least
  `s` contributes at least `s-1` minor-coordinate neighbors;
- `hammingLift_sameColorNeighbors_ge`: the generic lift bound
  `(|I|-1)+(s-1)`;
- `appendedLineGraph`: distinct points on an appended coordinate line form a
  simple graph;
- `appendedLineGraph_sameOrAdjacent_eq_boxProd`: this graph is exactly
  `G □ completeGraph (Fin p)` when the base line relation is equality or
  adjacency in `G`;
- `residueSlab_hammingLift_sameColorNeighbors_ge`: the direct bridge from
  `appendColor` and its fiber theorem to the lifted graph;
- `residueSlab_iteratedBoxProd_sameColorNeighbors_ge`: the graph-native final
  statement on `completeGraph I □ (G □ completeGraph (Fin p))`.

## Alignment and trust boundary

The theorem assumes a surjective base coloring with the exact base part count,
minimum fiber size, and an abstract `baseLine` relation. Hence it formalizes
the complete modular slab-plus-residual composition bridge and the exact
scheme deficit.

It now formalizes the first-coordinate Hamming lift and the exact
same-color-neighbor lower bound.  If `|I|=n1`, then the bound is
`(n1-1)+(s-1)=N1+s-1`, exactly the threshold used by the reviewed Hamming
construction.  It also identifies the minor line graph with Mathlib's
Cartesian product, so this is not merely an arithmetic or abstract-relation
kernel.

It does not construct the universal cyclic rectangle partition from height
1981, instantiate its base coloring, formalize the separate height-1925
upper bound, or check the height-2023 parameter family. These remain
external. Accordingly the project formalizes the composition and lower
Hamming-lift bridges, not the entire four-dimensional equality theorem.

The cyclic-rectangle audit found usable standard primitives (`Fin`,
`finProdFinEquiv`, `Nat.ModEq`, and finite fibers), but no existing lemma for
the required equitable modulo-fiber count. Completing that constructor would
still require a custom cyclic-block injection, modulo-fiber enumeration, and
concrete four-coordinate Hamming interface. The composition theorem selected
here avoids those representation layers.

The primary paper Bujtás--Dettlaff--Furmańczyk--Laskowska, *Majority
C-coloring in Cartesian products*, arXiv:2608.27669v1 (2026), gives
coordinate-projection lower bounds in Proposition 15 and asks for imbalanced
three- and four-dimensional values in Open Problem 2. It does not state this
residue-slab criterion. Classical star-decomposition literature covers
important divisible base rectangles, so no historical-priority claim is made.

No external computation, certificate, data, randomness, solver, or
nonstandard kernel/plugin is used.

## Reproduction

The project pins Lean and Mathlib `v4.33.1`.

```sh
lake update
lake exe cache get
lake clean hamming_residue_slab_composition
lake build ResidueSlabComposition HammingLift
lake env lean ResidueSlabComposition.lean
lake env lean HammingLift.lean
```

The final three commands must exit successfully. Eighteen `#print axioms` reports
should contain only standard Lean/Mathlib logical infrastructure: `propext`,
`Classical.choice`, and `Quot.sound`, with some declarations using a subset.

See `AUDIT.md` for exact version and verification evidence.
