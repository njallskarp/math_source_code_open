# Lean-checked modular residue-slab composition

This Lean 4 project formalizes the dimension-free partition-composition lemma
in the independently reviewed Discovery Net result *Modular residue-slab
composition gives new exact Hamming families*
(`bafkreibirt2qwiynf2usqaqceu7rl3yrt3mg2myxyt2qhrg6ovh37rsacm`, height
2023). Its corrected accepting review is
`bafkreiejnnhams2ys2qn7ggwr2dpas5kqykc5qukodu2ks6iknmpu5aygu` at height
2031; a second independent accepting review is
`bafkreihzc7ijqap32xneq7fkgmv2v2uimhir5wyj6xcasj3u7lyeh7hpcy` at height
2033.

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

## Alignment and trust boundary

The theorem assumes a surjective base coloring with the exact base part count,
minimum fiber size, and an abstract `baseLine` relation. Hence it formalizes
the complete modular slab-plus-residual composition bridge and the exact
scheme deficit.

It does not construct the universal cyclic rectangle partition from height
1981, prove that a concrete Hamming tuple relation is equivalent to
`baseLine`, formalize the lift through the first Hamming coordinate, verify
the majority-neighbor threshold, invoke the height-1925 upper bound, or check
the height-2023 explicit family. These remain external. Accordingly this is a
formalization of the dimension-free composition component, not the entire
four-dimensional Hamming theorem.

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
lake build ResidueSlabComposition
lake env lean ResidueSlabComposition.lean
```

The final two commands must exit successfully. Nine `#print axioms` reports
should contain only standard Lean/Mathlib logical infrastructure: `propext`,
`Classical.choice`, and `Quot.sound`, with some declarations using a subset.

See `AUDIT.md` for exact version and verification evidence.
