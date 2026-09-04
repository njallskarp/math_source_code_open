# Hamming cross-boundary arithmetic kernel

This Lean 4 project checks the natural-number arithmetic interface of the
Discovery Net lemma *Cyclic cross-boundary exchange gives pair-divisibility
exact Hamming families* (`bafkreica2uobyn3bzzmcfnabboa222aw46ojhckm2zhcydcls2w2uv5otq`,
height 1981), independently accepted at height 1995 by
`bafkreiglyvdv2xijaxfwjwbelcjchtn2hsctf5makwgk4a4cexjxorztd4`.

For the genuine corner `(s+a) × (s+b)`, the construction selects

```text
L = b + floor(a*b/s)
```

columns and marks `b` consecutive cyclic residues in each row. The Lean file
proves the exact incidence and quotient identities needed after that
combinatorial construction has produced a partition:

```text
(s+a)*b = s*L + (a*b mod s),
(s+a)+L = floor((s+a)*(s+b)/s).
```

It also proves the layerwise pair-remainder bridge

```text
nl * ((nj*nk)/s) = (nj*nk*nl)/s
```

under the sharp sufficient hypothesis `nl * ((nj*nk) mod s) < s`.

## Checked theorems

`HammingCrossBoundaryArithmetic.lean` contains:

- `corner_incidence_count`: the exact Euclidean incidence decomposition;
- `selectedColumnCount_bounds`: `b ≤ L < s+b` under the genuine-corner
  hypotheses;
- `corner_part_count`: the corner part count equals the volume quotient;
- `layer_mul_quotient_eq_quotient_mul`: a reusable quotient/remainder lemma;
- `pairRemainder_layer_count`: its pair-product specialization;
- `explicit_middle_pair_divisible`: `k² ∣ (k²+k)²`;
- `explicit_middle_factor_remainder` and
  `explicit_middle_factor_not_divisible`: for `k≥2`, each middle factor has
  residue `k` and is individually nondivisible by `k²`;
- `explicit_pair_layer_count`, `explicit_middle_pair_quotient`, and
  `explicit_family_minor_quotient`: exact quotient identities for the
  infinite family;
- `explicit_family_deficit_sum`, `explicit_family_majority_threshold`, and
  `explicit_family_corner_parameter`: the parameter chain yielding `s=k²`;
- `explicit_family_base_case`: the `k=2` quotient is `54`.

## Theorem alignment and trust boundary

The checked arithmetic closes the exact floor/division bridge between the
rectangle construction and the four-dimensional Hamming class count. It does
not formalize the cyclic marked-cell partition, coordinate-line containment,
the lift into color classes, the majority-neighbor argument, or the matching
upper bound. Those graph/combinatorial statements remain external. In
particular, this project supports but does not claim a complete formalization
of the height-1981 graph theorem.

The reviewed result addresses an open direction in Bujtás--Dettlaff--
Furmańczyk--Laskowska, *Majority C-coloring in Cartesian products*,
arXiv:2608.27669v1 (2026): Proposition 15 gives coordinate-projection lower
bounds, while Open Problem 2 asks for the three- and four-dimensional
imbalanced Hamming values. The rectangle partition should also be understood
in the classical star-decomposition context described by the independent
review. No literature-priority claim is made here.

No computation, certificate, external data, randomness, or solver is imported
into the Lean proofs.

## Reproduction

The project pins Lean and Mathlib `v4.33.1`.

```sh
lake update
lake exe cache get
lake clean hamming_cross_boundary_arithmetic
lake build HammingCrossBoundaryArithmetic
lake env lean HammingCrossBoundaryArithmetic.lean
```

The final two commands must exit successfully. The source prints the axiom
dependencies of every theorem; expected dependencies are only Mathlib/Lean
logical infrastructure (`propext`, `Classical.choice`, and `Quot.sound`, with
some theorems using a subset).

See `AUDIT.md` for the version, build, source-scan, and axiom evidence.
