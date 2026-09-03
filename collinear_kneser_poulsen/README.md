# Collinear and near-collinear equal-ball unions

This directory contains four self-contained analytic notes around the
Kneser--Poulsen conjecture for congruent balls.

- `COLLINEAR_MST_THEOREM.md` proves an exact formula for the volume of a union
  of equal balls with collinear centers as a truncated radial minimum-spanning-
  tree functional.  It derives a two-sided contraction-deficit sandwich,
  linear overlap-regime stability, and an equality criterion.
- `NEAR_COLLINEAR_QUADRATIC_STABILITY.md` proves an explicit quadratic upper
  bound for the excess union volume above the collinear projection when axial
  coordinates are distinct.  It also shows the quadratic order and inverse-gap
  degeneration are sharp and records the linear collision obstruction.
- `ADJACENT_PATH_TRANSVERSE_STABILITY.md` strengthens that bound from all
  overlapping pairs to only consecutive axial labels, incorporates the sharp
  near-tangency cutoff, reduces the uniform dependence from `binom(N,2)` to
  `N-1`, and proves the best uniform planar multiplier.
- `PLANAR_SECOND_VARIATION.md` computes the exact local transverse Hessian of
  planar union area at every fixed distinct collinear configuration.  It is
  twice a weighted path Laplacian on the strict-overlap blocks and its kernel
  consists exactly of componentwise translations.

The arguments are symbolic, based on perpendicular cross-sections, Fubini's
theorem, elementary MST exchange, a set-chain lemma, and a shell estimate.  No
numerical or computer-assisted claim is used.

## Reproduction and trust boundary

There is no executable proof checker.  A reader can authenticate the exact
published texts from the repository root with:

```text
cd collinear_kneser_poulsen
shasum -a 256 -c SHA256SUMS
```

Success prints `OK` for the four proof notes and this README.  The manifest
checks source integrity only; the theorems require human verification of the
displayed arguments and of the prior results cited in each literature section.
No generated output, external dataset, private state, or large certificate is
required.

## Discovery Net provenance

The notes support these committed contributions:

- height 1595,
  `bafkreidb5lbef3prijivxa6jonupdszbwet2tboatmdz7lq2juiagbq6si`;
- height 1611,
  `bafkreiglzathchjxfnmlpodmynyske7wea4nskt7nr5xi456wad7d2lcte`.
