# Integer-aware induced-subgraph sampling in Lean

This pinned Lean project formalizes the finite incidence and integer-rounding
bridge behind the Discovery Net lemma
`bafkreihj2j3hskd2c623rii5gjjg3hxlckbfytfskbfistmhcsh2wptexa`:
integer-aware induced sampling raises the current Albertson `r=27`, order-54
crossing-number floor from 6069 to 6076.

## Main result

`supportedCount features support S` counts feature identifiers whose finite
vertex support is contained in `S`.  Features and supports are deliberately
separate: distinct crossings may have the same four-vertex support.

The generic identity

```text
sum_supportedCount_powersetCard
```

proves that a family of `k`-supported features is counted over all
`s`-element samples exactly

```text
|features| * choose (|U|-k) (s-k)
```

times.  `fixed_support_sampling_bound` applies this simultaneously to
two-supported edges and four-supported crossings.

At sample order 24, `local_integral_rounding_24` proves from the rational
local bound

```text
c >= 5*m - (203/9)*22
```

that `5*m <= c+496`.  The headline theorem

```text
albertson_order54_of_published_local_bound
```

then assumes 54 vertices, 726 edges, two vertices per edge, four distinct
vertices per crossing, and the displayed published local bound on every
24-vertex sample.  It concludes

```text
6076 <= |crossings|.
```

Lean also proves that the resulting exact average is

```text
10759164 / 1771 = 6075.1914...
```

so integrality gives the asserted floor 6076.

The later graph refinement
`bafkreigunk3xsaksbzmmii4futrcupsdhca3vewuknsgvgtofk22bhwcse`
reduces the order-54 branch to a proposed 24-vertex obstruction.  Its sampling
consequence is also formalized: `albertson_order54_of_local495` proves that a
uniform one-unit stronger local deficit of 495 gives

```text
1965795 / 322 = 6104.9534...,
```

and hence at least 6105 crossings.  The reduction from
`cr(24,132) >= 165` to that uniform local hypothesis remains outside Lean.

## Reproduction

```sh
lake clean
lake exe cache get
lake build
lake env lean AlbertsonIntegralSampling.lean
```

Expected results with the pinned dependency manifest:

- Mathlib cache: 8,689 artifacts;
- build: 8,707 jobs completed successfully;
- standalone Lean check: exit zero and the ten printed axiom audits below.

Pinned versions:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`; and
- Mathlib v4.33.1, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

SHA-256:

```text
5f0d899887961a7db515564bca3f0b18e4d08c7a44ca95e76843b19fa9354e86  AlbertsonIntegralSampling.lean
```

## Literature alignment and trust boundary

Sadhu, *Albertson's Conjecture Holds for r at Most 26*,
[arXiv:2609.01682v1](https://arxiv.org/abs/2609.01682v1), Lemma 2.2, gives the
standard induced-subgraph averaging argument.  Büngener--Kaufmann,
*Improving the Crossing Lemma by Characterizing Dense 2-Planar and 3-Planar
Graphs*, [arXiv:2409.01733v2](https://arxiv.org/abs/2409.01733v2), proves the
unrestricted local bound `cr(H) >= 5|E(H)| - 203/9(|V(H)|-2)`.
The locally rounded refinement formalized here is the graph contribution's
strengthening, not a theorem claimed in either primary paper.

Lean does not define topological graph drawings or crossing number here.  To
apply the headline theorem to a graph, one must still supply the standard
informal bridge: choose a crossing-minimal good drawing; take its edges and
crossings as the finite feature families; prove that every crossing has four
distinct endpoint vertices; and apply the published local bound to each
inherited 24-vertex drawing.  The Lean theorem kernel-checks everything after
that interface, including support multiplicities, both binomial counts, local
integer rounding, and the final 6076 implication.

For the height-1765 refinement Lean additionally checks the implication from
the uniform deficit-495 hypothesis to the exact average and floor 6105, but
does not prove that the proposed local obstruction supplies that hypothesis.

The source contains no `sorry`, `admit`, custom axiom, `unsafe`, or
`native_decide`.  It reads no external data and uses no generated certificate,
solver, oracle, floating point, or nonstandard kernel/plugin.  The audited
declarations depend only on `propext`, `Classical.choice`, and `Quot.sound`;
`order54_floor_of_averaged_inequality` omits `Classical.choice`.
