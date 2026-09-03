# Firey `L_p` Rogers--Shephard equality for symmetric planar bodies

This directory proves an exact formula for the sharp planar symmetric Firey
Rogers--Shephard deficit of every centrally symmetric hexagon having the
origin as a vertex, uses it to classify equality for every centrally
symmetric polygon, and then closes the nonpolygonal limit by a direct
slope-measure quantization shadow.

For the complete range `1<p<infinity`, equality in Corollary 29 of
Fradelizi--Manui--Meyer--Ndiaye (arXiv:2607.03582) holds among all
full-dimensional centrally symmetric planar convex bodies containing the
origin if and only if the body is a parallelogram and the origin is one of its
vertices.  This proves their Conjecture 5.  The hexagon proof also gives a
uniform two-sided normalized stability criterion for `p>=2`.

## Contents

- `FIREY_HEXAGON_ALL_P.md`: self-contained normal form, exact two-arc/three-
  face boundary calculation, strictness argument, and stability estimate.
- `SYMMETRIC_POLYGON_EQUALITY.md`: explicit constant-area generator-deletion
  shadow, equality-propagation induction, and exact translated-parallelogram
  edge deficit.
- `ZONOID_QUANTIZATION_FULL_EQUALITY.md`: one-sided slope-measure normal form,
  exact Gini-area quantization, a two-sided continuum shadow, and reduction of
  every remaining equality case to a forbidden hexagon.
- `verify_zonoid_quantization.py`: deterministic exact-rational checks of the
  quantization and constant-area identities for both measure branches.
- `SHA256SUMS`: compact integrity manifest.

## Reproduction

From this directory run:

```sh
python3 verify_zonoid_quantization.py
shasum -a 256 -c SHA256SUMS
```

The checker ends with:

```text
result_sha256=e0a90164ffd457f60d55c805af0ca31d1a038310b1ffad96fae7f8ed6cfed398
VERIFIED
```

The manifest then reports:

```text
FIREY_HEXAGON_ALL_P.md: OK
SYMMETRIC_POLYGON_EQUALITY.md: OK
ZONOID_QUANTIZATION_FULL_EQUALITY.md: OK
verify_zonoid_quantization.py: OK
README.md: OK
```

## Trust boundary

The theorem is a human-readable symbolic proof.  The checker uses Python
`Fraction` arithmetic for two continuous uniform-measure models; it does not
prove the general measure lemma.  The manifest checks exact source bytes only.
Neither command machine-checks the convex-geometric normal forms,
support-function differentiation, Green integrals, shadow-system closure,
convexity theorem, or arbitrary-measure limiting argument.  No numerical
experiment, external data set, solver, large certificate, or omitted generated
artifact is required.

The novelty check is search-relative.  The source preprint proves the sharp
inequality but states its equality characterization as Conjecture 5.  The
proof here first settles finite-sided bodies, then bypasses the nonuniform
deletion-factor obstruction by a single macroscopic measure quantization.
