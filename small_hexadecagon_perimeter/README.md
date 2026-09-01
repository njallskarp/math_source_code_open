# Certified local maximum for the small-hexadecagon fixed code

This directory independently reconstructs and locally certifies the `n=16`
candidate reported by Bernd Mulansky and Andreas Potschka for their fixed-code
zonogon nonlinear program.  The first-quarter code is `+--+-++-`.  Axial
symmetry gives the first-half code

```text
+--+-++-+--+-++-
```

and antipodality gives the full cyclic code

```text
+--+-++-+--+-++--++-+--+-++-+--+
```

whose negative-run composition is
`(2,1,1,2,1,2,1,2,1,1,2)`.

## Certified statement

Fix `phi_1=0`, `phi_17=pi`, and the first-half code above.  Put

```text
P(phi) = sum_{j=1}^{16} 2 sin((phi_{j+1}-phi_j)/2),
g1(phi) = sum_{j=2}^{16} (c_{j-1}-c_j) cos(phi_j) - (c_1+c_16),
g2(phi) = sum_{j=2}^{16} (c_{j-1}-c_j) sin(phi_j).
```

Let `F` be the 17-dimensional KKT system for `f=-P/2` subject to
`g1=g2=0`; scaling the objective by `1/2` does not change its maximizing
angles.  At 512-bit Arb precision, `verify_local_certificate.py` proves:

1. The Krawczyk image is strictly contained in the coordinatewise
   radius-`1e-110` box around the dyadic centers derived from
   `candidate.json`.  Therefore `F` has exactly one zero in that box.
2. Every angle gap is strictly positive throughout the box, so none of the
   ordering inequalities is active.
3. Interval `LDL^T` elimination of the KKT Jacobian has pivot signs
   `+++++++++++++++--` throughout the box.  In particular, the 15-by-15
   Lagrangian Hessian is positive definite and the constraint Jacobian has
   full row rank at the enclosed zero.

The enclosed zero is consequently a strict local maximizer of `P` on the
fixed-code equality manifold.  Arb encloses its perimeter by

```text
[3.136547716486607386085967031941228227298136765809232692789218203577745755473817628905857362542821159391634981 +/- 6.62e-109]
```

This is a local theorem.  It does **not** prove that the point is the unique
stationary point over the whole ordered-angle domain, the global maximizer
for this code, the best code, or the unrestricted longest small
hexadecagon.

## Reproduction

Python 3.12 was used for the recorded run.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python reconstruct_candidate.py
.venv/bin/python verify_local_certificate.py
.venv/bin/python -m unittest -v test_local_certificate.py
shasum -a 256 -c SHA256SUMS
```

`reconstruct_candidate.py` is a non-rigorous, 160-decimal-digit mpmath
Newton reconstruction starting at regular angles.  It independently matches
the published perimeter.  `verify_local_certificate.py` reimplements the
system with Arb balls, uses a fixed exact-dyadic approximate inverse in the
Krawczyk operator, and performs the interval inertia check.  The verifier
does not import the reconstruction formulas.

## Formula audit

The paper defines `P=-f` but its displayed first derivative is the derivative
of `f=-P/2`.  Its displayed off-diagonal Hessian sine argument, and the sign
of the `y2` term on the Hessian diagonal, also differ from direct
differentiation of that displayed first derivative.  These are harmless for
the reported stationary angles but matter for a proof checker.  Both programs
here derive the Jacobian directly from the explicitly stated KKT residual;
the two implementations use different arithmetic libraries.

## Primary source

- Bernd Mulansky and Andreas Potschka, *A zonogon approach for computing
  small polygons of maximum perimeter*, Mathematical Programming (2025),
  [journal article](https://doi.org/10.1007/s10107-025-02244-x),
  [author preprint and source](https://arxiv.org/abs/2404.01841).

The quarter code is Table 4 of the paper; the fixed-code NLP and the authors'
statement that uniqueness was not proved appear in Sections 4--5.
