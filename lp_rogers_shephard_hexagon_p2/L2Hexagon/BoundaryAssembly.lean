import L2Hexagon.BoundaryParametrization

/-!
# Assembly of curved arcs and jump segments

The canonical support boundary point jumps when the one-sided support derivative
changes at a generator sign boundary.  Those jumps trace straight boundary
segments.  This file proves the exact determinant of all three upper-half
jumps and assembles them with the two curved oriented-density integrals.

The jump contributions are

* `1+b` at `pi/2`,
* `a+b` at `pi/2 + arctan (b/a)`,
* `1+a` at `pi`.

The Sector I boundary point is constant and has zero oriented arc density.  The
resulting arcs-plus-jumps total is exactly

`2(1+a+b) + (1+b)phi + (1+a)(pi/2-phi)`.

This is the complete scalar oriented-boundary precursor on a half-period.  The
remaining geometric theorem must still show that these arcs and segments trace
the boundary of the halfspace-defined Firey body and then identify the closed
line integral with planar Lebesgue area.
-/

open Real Set MeasureTheory
open scoped Interval

namespace L2Hexagon

/-- Determinant between two canonical support boundary points at one normal angle. -/
noncomputable def supportBoundaryTransitionDet
    (h₁ k₁ h₂ k₂ : ℝ → ℝ) (θ : ℝ) : ℝ :=
  supportBoundaryX h₁ k₁ θ * supportBoundaryY h₂ k₂ θ -
    supportBoundaryY h₁ k₁ θ * supportBoundaryX h₂ k₂ θ

/-- Rotating `(h,k)` to Cartesian coordinates preserves its determinant. -/
theorem supportBoundaryTransitionDet_eq
    (h₁ k₁ h₂ k₂ : ℝ → ℝ) (θ : ℝ) :
    supportBoundaryTransitionDet h₁ k₁ h₂ k₂ θ =
      h₁ θ * k₂ θ - k₁ θ * h₂ θ := by
  unfold supportBoundaryTransitionDet supportBoundaryX supportBoundaryY
  calc
    (h₁ θ * cos θ - k₁ θ * sin θ) *
          (h₂ θ * sin θ + k₂ θ * cos θ) -
        (h₁ θ * sin θ + k₁ θ * cos θ) *
          (h₂ θ * cos θ - k₂ θ * sin θ) =
      (h₁ θ * k₂ θ - k₁ θ * h₂ θ) *
        (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = h₁ θ * k₂ θ - k₁ θ * h₂ θ := by
      rw [Real.sin_sq_add_cos_sq]
      ring

/-- Sector I has second derivative `-h`, hence zero boundary speed. -/
theorem hasDerivAt_sectorOneDerivative (a b θ : ℝ) :
    HasDerivAt (sectorOneDerivative a b) (-sectorOneSupport a b θ) θ := by
  unfold sectorOneDerivative sectorOneSupport
  exact (((Real.hasDerivAt_sin θ).const_mul (-(1 + a))).add
    ((Real.hasDerivAt_cos θ).const_mul (1 + b))).congr_deriv (by ring)

/-- First coordinate of the Sector I canonical boundary point. -/
noncomputable def sectorOneBoundaryX (a b θ : ℝ) : ℝ :=
  supportBoundaryX (sectorOneSupport a b) (sectorOneDerivative a b) θ

/-- Second coordinate of the Sector I canonical boundary point. -/
noncomputable def sectorOneBoundaryY (a b θ : ℝ) : ℝ :=
  supportBoundaryY (sectorOneSupport a b) (sectorOneDerivative a b) θ

/-- The Sector I boundary point is the fixed vertex `(1+a,1+b)`. -/
theorem sectorOneBoundaryX_eq (a b θ : ℝ) : sectorOneBoundaryX a b θ = 1 + a := by
  unfold sectorOneBoundaryX supportBoundaryX sectorOneSupport sectorOneDerivative
  calc
    ((1 + a) * cos θ + (1 + b) * sin θ) * cos θ -
        (-(1 + a) * sin θ + (1 + b) * cos θ) * sin θ =
      (1 + a) * (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = 1 + a := by rw [Real.sin_sq_add_cos_sq]; ring

/-- The Sector I boundary point is the fixed vertex `(1+a,1+b)`. -/
theorem sectorOneBoundaryY_eq (a b θ : ℝ) : sectorOneBoundaryY a b θ = 1 + b := by
  unfold sectorOneBoundaryY supportBoundaryY sectorOneSupport sectorOneDerivative
  calc
    ((1 + a) * cos θ + (1 + b) * sin θ) * sin θ +
        (-(1 + a) * sin θ + (1 + b) * cos θ) * cos θ =
      (1 + b) * (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = 1 + b := by rw [Real.sin_sq_add_cos_sq]; ring

/-- Sector I's canonical boundary path has zero oriented density. -/
noncomputable def sectorOneBoundaryOrientedDensity (a b θ : ℝ) : ℝ :=
  supportBoundaryX (sectorOneSupport a b) (sectorOneDerivative a b) θ *
      supportBoundaryDY (sectorOneSupport a b) (fun t => -sectorOneSupport a b t) θ -
    supportBoundaryY (sectorOneSupport a b) (sectorOneDerivative a b) θ *
      supportBoundaryDX (sectorOneSupport a b) (fun t => -sectorOneSupport a b t) θ

theorem sectorOneBoundaryOrientedDensity_eq_zero (a b θ : ℝ) :
    sectorOneBoundaryOrientedDensity a b θ = 0 := by
  unfold sectorOneBoundaryOrientedDensity
  simpa using supportBoundary_orientedDensity (sectorOneSupport a b)
    (sectorOneDerivative a b) (fun t => -sectorOneSupport a b t) θ

theorem integral_sectorOneBoundaryOrientedDensity (a b : ℝ) :
    (∫ θ in (0 : ℝ)..π / 2, sectorOneBoundaryOrientedDensity a b θ) = 0 := by
  simp [sectorOneBoundaryOrientedDensity_eq_zero]

theorem sectorOneSupport_pi_div_two (a b : ℝ) :
    sectorOneSupport a b (π / 2) = 1 + b := by simp [sectorOneSupport]

theorem sectorOneDerivative_pi_div_two (a b : ℝ) :
    sectorOneDerivative a b (π / 2) = -(1 + a) := by simp [sectorOneDerivative]

theorem sectorTwoSupport_pi_div_two {a b : ℝ} (hb : 0 < b) :
    sectorTwoSupport a b (π / 2) = 1 + b := by
  have hs : sectorTwoSq a b (π / 2) = (1 + b) ^ 2 := by
    simp [sectorTwoSq, sectorTwoU]
  rw [sectorTwoSupport, hs, Real.sqrt_sq_eq_abs, abs_of_pos (by linarith)]

theorem sectorTwoSupportDerivative_pi_div_two {a b : ℝ} (hb : 0 < b) :
    sectorTwoSupportDerivative a b (π / 2) = -a := by
  change sectorTwoBoundary a b (π / 2) / sectorTwoSupport a b (π / 2) = -a
  rw [sectorTwoBoundary_pi_div_two, sectorTwoSupport_pi_div_two hb]
  field_simp [ne_of_gt (by linarith : 0 < 1 + b)]

/-- The first jump segment contributes exactly `1+b`. -/
theorem sectorOneTwo_transitionDet {a b : ℝ} (hb : 0 < b) :
    supportBoundaryTransitionDet
      (sectorOneSupport a b) (sectorOneDerivative a b)
      (sectorTwoSupport a b) (sectorTwoSupportDerivative a b) (π / 2) =
        1 + b := by
  rw [supportBoundaryTransitionDet_eq, sectorOneSupport_pi_div_two,
    sectorOneDerivative_pi_div_two, sectorTwoSupport_pi_div_two hb,
    sectorTwoSupportDerivative_pi_div_two hb]
  ring

/-- Sector II support square is one at the middle generator sign boundary. -/
theorem sectorTwoSq_generator_boundary {a b : ℝ} (ha : 0 < a) :
    sectorTwoSq a b (π / 2 + arctan (b / a)) = 1 := by
  let φ := arctan (b / a)
  have hrel : a * sin φ = b * cos φ := by
    simpa [φ] using generatorAngle_sin_relation (b := b) ha
  have hU : a * -sin φ + (1 + b) * cos φ = cos φ := by linarith
  rw [show arctan (b / a) = φ by rfl, show π / 2 + φ = φ + π / 2 by ring]
  simp only [sectorTwoSq, sectorTwoU, Real.cos_add_pi_div_two,
    Real.sin_add_pi_div_two]
  rw [hU]
  nlinarith [Real.sin_sq_add_cos_sq φ]

theorem sectorTwoSupport_generator_boundary {a b : ℝ} (ha : 0 < a) :
    sectorTwoSupport a b (π / 2 + arctan (b / a)) = 1 := by
  rw [sectorTwoSupport, sectorTwoSq_generator_boundary ha, Real.sqrt_one]

theorem sectorTwoSupportDerivative_generator_boundary {a b : ℝ} (ha : 0 < a) :
    sectorTwoSupportDerivative a b (π / 2 + arctan (b / a)) = -a := by
  change sectorTwoBoundary a b (π / 2 + arctan (b / a)) /
      sectorTwoSupport a b (π / 2 + arctan (b / a)) = -a
  rw [sectorTwoBoundary_pi_div_two_add (generatorAngle_sin_relation ha),
    sectorTwoSupport_generator_boundary ha]
  ring

theorem sectorThreeSupport_generator_boundary {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    sectorThreeSupport a b (π / 2 + arctan (b / a)) = 1 := by
  unfold sectorThreeSupport
  rw [← sectorTwoSq_eq_sectorThreeSq_boundary ha hb,
    sectorTwoSq_generator_boundary ha, Real.sqrt_one]

/-- Sector III has endpoint quantity `b` at the middle generator sign boundary. -/
theorem sectorThreeBoundary_generator_boundary {a b : ℝ} (ha : 0 < a) :
    sectorThreeBoundary a b (π / 2 + arctan (b / a)) = b := by
  let φ := arctan (b / a)
  have hrel : a * sin φ = b * cos φ := by
    simpa [φ] using generatorAngle_sin_relation (b := b) ha
  have hW : (1 + a) * -sin φ + b * cos φ = -sin φ := by linarith
  have hrelc := congrArg (fun z : ℝ => z * cos φ) hrel
  rw [show arctan (b / a) = φ by rfl, show π / 2 + φ = φ + π / 2 by ring]
  simp only [sectorThreeBoundary, sectorThreeW, sectorThreeZ,
    Real.cos_add_pi_div_two, Real.sin_add_pi_div_two]
  rw [hW]
  calc
    cos φ * -sin φ + -sin φ * (-(1 + a) * cos φ + b * -sin φ) =
        a * sin φ * cos φ + b * sin φ ^ 2 := by ring
    _ = b * (cos φ ^ 2 + sin φ ^ 2) := by rw [hrelc]; ring
    _ = b := by rw [add_comm, Real.sin_sq_add_cos_sq]; ring

theorem sectorThreeSupportDerivative_generator_boundary {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    sectorThreeSupportDerivative a b (π / 2 + arctan (b / a)) = b := by
  change sectorThreeBoundary a b (π / 2 + arctan (b / a)) /
      sectorThreeSupport a b (π / 2 + arctan (b / a)) = b
  rw [sectorThreeBoundary_generator_boundary ha,
    sectorThreeSupport_generator_boundary ha hb]
  ring

/-- The middle jump segment contributes exactly `a+b`. -/
theorem sectorTwoThree_transitionDet {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    supportBoundaryTransitionDet
      (sectorTwoSupport a b) (sectorTwoSupportDerivative a b)
      (sectorThreeSupport a b) (sectorThreeSupportDerivative a b)
      (π / 2 + arctan (b / a)) = a + b := by
  rw [supportBoundaryTransitionDet_eq, sectorTwoSupport_generator_boundary ha,
    sectorTwoSupportDerivative_generator_boundary ha,
    sectorThreeSupport_generator_boundary ha hb,
    sectorThreeSupportDerivative_generator_boundary ha hb]
  ring

/-- Sector III support at `pi`. -/
theorem sectorThreeSupport_pi {a b : ℝ} (ha : 0 < a) :
    sectorThreeSupport a b π = 1 + a := by
  have hs : sectorThreeSq a b π = (1 + a) ^ 2 := by
    simp [sectorThreeSq, sectorThreeW]
    ring
  rw [sectorThreeSupport, hs, Real.sqrt_sq_eq_abs, abs_of_pos (by linarith)]

theorem sectorThreeBoundary_pi (a b : ℝ) :
    sectorThreeBoundary a b π = (1 + a) * b := by
  simp [sectorThreeBoundary, sectorThreeW, sectorThreeZ]
  ring

theorem sectorThreeSupportDerivative_pi {a b : ℝ} (ha : 0 < a) :
    sectorThreeSupportDerivative a b π = b := by
  change sectorThreeBoundary a b π / sectorThreeSupport a b π = b
  rw [sectorThreeBoundary_pi, sectorThreeSupport_pi ha]
  field_simp [ne_of_gt (by linarith : 0 < 1 + a)]

/-- Sector I support shifted to the next half-period. -/
noncomputable def sectorOneSupportShiftPi (a b θ : ℝ) : ℝ :=
  sectorOneSupport a b (θ - π)

/-- Derivative of the shifted Sector I support. -/
noncomputable def sectorOneDerivativeShiftPi (a b θ : ℝ) : ℝ :=
  sectorOneDerivative a b (θ - π)

theorem sectorOneSupportShiftPi_pi (a b : ℝ) :
    sectorOneSupportShiftPi a b π = 1 + a := by simp [sectorOneSupportShiftPi, sectorOneSupport]

theorem sectorOneDerivativeShiftPi_pi (a b : ℝ) :
    sectorOneDerivativeShiftPi a b π = 1 + b := by
  simp [sectorOneDerivativeShiftPi, sectorOneDerivative]

/-- The closing upper-half jump contributes exactly `1+a`. -/
theorem sectorThreeOne_transitionDet {a b : ℝ} (ha : 0 < a) :
    supportBoundaryTransitionDet
      (sectorThreeSupport a b) (sectorThreeSupportDerivative a b)
      (sectorOneSupportShiftPi a b) (sectorOneDerivativeShiftPi a b) π =
        1 + a := by
  rw [supportBoundaryTransitionDet_eq, sectorThreeSupport_pi ha,
    sectorThreeSupportDerivative_pi ha, sectorOneSupportShiftPi_pi,
    sectorOneDerivativeShiftPi_pi]
  ring

/-- Arcs plus jump segments for the complete upper-half boundary traversal. -/
noncomputable def normalizedUpperBoundaryOrientedTotal (a b : ℝ) : ℝ :=
  (∫ θ in (0 : ℝ)..π / 2, sectorOneBoundaryOrientedDensity a b θ) +
    supportBoundaryTransitionDet
      (sectorOneSupport a b) (sectorOneDerivative a b)
      (sectorTwoSupport a b) (sectorTwoSupportDerivative a b) (π / 2) +
    (∫ θ in π / 2..π / 2 + arctan (b / a),
      sectorTwoBoundaryOrientedDensity a b θ) +
    supportBoundaryTransitionDet
      (sectorTwoSupport a b) (sectorTwoSupportDerivative a b)
      (sectorThreeSupport a b) (sectorThreeSupportDerivative a b)
      (π / 2 + arctan (b / a)) +
    (∫ θ in π / 2 + arctan (b / a)..π,
      sectorThreeBoundaryOrientedDensity a b θ) +
    supportBoundaryTransitionDet
      (sectorThreeSupport a b) (sectorThreeSupportDerivative a b)
      (sectorOneSupportShiftPi a b) (sectorOneDerivativeShiftPi a b) π

/-- Exact oriented boundary total over one half-period, including all jumps. -/
theorem normalizedUpperBoundaryOrientedTotal_eq {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedUpperBoundaryOrientedTotal a b =
      2 * (1 + a + b) + (1 + b) * arctan (b / a) +
        (1 + a) * (π / 2 - arctan (b / a)) := by
  rw [normalizedUpperBoundaryOrientedTotal,
    integral_sectorOneBoundaryOrientedDensity,
    sectorOneTwo_transitionDet hb,
    integral_sectorTwoBoundaryOrientedDensity ha hb,
    sectorTwoThree_transitionDet ha hb,
    integral_sectorThreeBoundaryOrientedDensity ha hb,
    sectorThreeOne_transitionDet ha]
  ring

/-- The assembled support-density integral equals the arcs-plus-jumps boundary total. -/
theorem integral_normalizedUpperDensity_eq_boundaryOrientedTotal {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    (∫ θ in (0 : ℝ)..π, normalizedUpperDensity a b θ) =
      normalizedUpperBoundaryOrientedTotal a b := by
  rw [integral_normalizedUpperDensity ha hb,
    normalizedUpperBoundaryOrientedTotal_eq ha hb]

#print axioms supportBoundaryTransitionDet_eq
#print axioms sectorOneBoundaryX_eq
#print axioms sectorOneBoundaryY_eq
#print axioms integral_sectorOneBoundaryOrientedDensity
#print axioms sectorOneTwo_transitionDet
#print axioms sectorTwoThree_transitionDet
#print axioms sectorThreeOne_transitionDet
#print axioms normalizedUpperBoundaryOrientedTotal_eq
#print axioms integral_normalizedUpperDensity_eq_boundaryOrientedTotal

end L2Hexagon
