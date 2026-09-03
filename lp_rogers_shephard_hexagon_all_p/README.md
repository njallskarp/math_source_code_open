# Firey `L_p` Rogers--Shephard equality for symmetric polygons

This directory proves an exact formula for the sharp planar symmetric Firey
Rogers--Shephard deficit of every centrally symmetric hexagon having the
origin as a vertex, then uses it to classify equality for every centrally
symmetric polygon containing the origin.

For the complete range `1<p<infinity`, equality in Corollary 29 of
Fradelizi--Manui--Meyer--Ndiaye (arXiv:2607.03582) holds among polygons if and
only if the polygon is a parallelogram and the origin is one of its vertices.
The hexagon proof also gives a uniform two-sided normalized stability
criterion for `p>=2`.

## Contents

- `FIREY_HEXAGON_ALL_P.md`: self-contained normal form, exact two-arc/three-
  face boundary calculation, strictness argument, and stability estimate.
- `SYMMETRIC_POLYGON_EQUALITY.md`: explicit constant-area generator-deletion
  shadow, equality-propagation induction, and exact translated-parallelogram
  edge deficit.
- `SHA256SUMS`: compact integrity manifest.

## Reproduction

From this directory run:

```sh
shasum -a 256 -c SHA256SUMS
```

Expected output:

```text
FIREY_HEXAGON_ALL_P.md: OK
SYMMETRIC_POLYGON_EQUALITY.md: OK
README.md: OK
```

## Trust boundary

The theorem is a human-readable symbolic proof.  The reproduction command
checks exact source bytes only; it does not machine-check the convex-geometric
normal forms, support-function differentiation, Green integrals,
shadow-system closure, convexity theorem, or monotonicity arguments.  No
numerical experiment, external data set, solver, large certificate, or omitted
generated artifact is required for either result.

The novelty check is search-relative.  The source preprint proves the sharp
inequality but states its equality characterization as Conjecture 5.  This
directory proves that characterization for every finite-sided centrally
symmetric body; it does not supply the limiting nonpolygonal step.
