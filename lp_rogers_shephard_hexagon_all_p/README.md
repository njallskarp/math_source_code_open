# Firey `L_p` Rogers--Shephard equality for symmetric hexagons

This directory proves an exact formula for the sharp planar symmetric Firey
Rogers--Shephard deficit of every centrally symmetric hexagon having the
origin as a vertex.

The main result is strictness for the complete range `1<p<infinity`: a
nondegenerate such hexagon never attains the sharp constant from Corollary 29
of Fradelizi--Manui--Meyer--Ndiaye (arXiv:2607.03582).  The proof also gives a
uniform two-sided normalized stability criterion for `p>=2`.

## Contents

- `FIREY_HEXAGON_ALL_P.md`: self-contained normal form, exact two-arc/three-
  face boundary calculation, strictness argument, and stability estimate.
- `SHA256SUMS`: compact integrity manifest.

## Reproduction

From this directory run:

```sh
shasum -a 256 -c SHA256SUMS
```

Expected output:

```text
FIREY_HEXAGON_ALL_P.md: OK
README.md: OK
```

## Trust boundary

The theorem is a human-readable symbolic proof.  The reproduction command
checks exact source bytes only; it does not machine-check the convex-geometric
normal form, support-function differentiation, Green integral, or monotonicity
argument.  No numerical experiment, external data set, solver, large
certificate, or omitted generated artifact is required for the result.

The novelty check is search-relative.  The source preprint proves the sharp
inequality but states its equality characterization as Conjecture 5; this
directory proves only its origin-vertex six-sided subcase, not the conjecture
for arbitrary centrally symmetric planar bodies.
