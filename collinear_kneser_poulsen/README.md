# Collinear and near-collinear equal-ball unions

This directory contains two self-contained analytic notes around the
Kneser--Poulsen conjecture for congruent balls.

- `COLLINEAR_MST_THEOREM.md` proves an exact formula for the volume of a union
  of equal balls with collinear centers as a truncated radial minimum-spanning-
  tree functional.  It derives a two-sided contraction-deficit sandwich,
  linear overlap-regime stability, and an equality criterion.
- `NEAR_COLLINEAR_QUADRATIC_STABILITY.md` proves an explicit quadratic upper
  bound for the excess union volume above the collinear projection when axial
  coordinates are distinct.  It also shows the quadratic order and inverse-gap
  degeneration are sharp and records the linear collision obstruction.

Both arguments are symbolic, based on perpendicular cross-sections, Fubini's
theorem, elementary MST exchange, and a shell estimate.  No numerical or
computer-assisted claim is used.

## Reproduction and trust boundary

There is no executable proof checker.  A reader can authenticate the exact
published texts from the repository root with:

```text
cd collinear_kneser_poulsen
shasum -a 256 -c SHA256SUMS
```

Success prints `OK` for the two proof notes and this README.  The manifest
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
