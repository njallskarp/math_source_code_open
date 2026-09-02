import L2Hexagon.NormalizedSectorSupport
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

/-!
# The exact Sector I support-density integral

For `A=1+a` and `B=1+b`, the first upper-half-circle sector has support

`h(θ)=A cos θ+B sin θ`.

This file differentiates that literal expression and proves

`∫_[0,π/2] (h²-(h')²) = 2AB`.

The density is not constant.  The proof uses the exact primitive

`((A²-B²)/2) sin(2θ)-AB cos(2θ)`.

The planar support-area theorem remains outside the claim.
-/

open Real MeasureTheory
open scoped Interval

namespace L2Hexagon

/-- The scalar support-area density on Sector I. -/
noncomputable def sectorOneDensity (a b θ : ℝ) : ℝ :=
  sectorOneSupport a b θ ^ 2 - sectorOneDerivative a b θ ^ 2

/-- An elementary primitive of the nonconstant Sector I density. -/
noncomputable def sectorOnePrimitive (a b θ : ℝ) : ℝ :=
  sin (2 * θ) * (((1 + a) ^ 2 - (1 + b) ^ 2) / 2) -
    cos (2 * θ) * ((1 + a) * (1 + b))

/-- The displayed Sector I derivative is the actual derivative of its support expression. -/
theorem hasDerivAt_sectorOneSupport (a b θ : ℝ) :
    HasDerivAt (sectorOneSupport a b) (sectorOneDerivative a b θ) θ := by
  unfold sectorOneSupport sectorOneDerivative
  exact (((Real.hasDerivAt_cos θ).const_mul (1 + a)).add
    ((Real.hasDerivAt_sin θ).const_mul (1 + b))).congr_deriv (by ring)

/-- The primitive differentiates to the exact, nonconstant Sector I density. -/
theorem hasDerivAt_sectorOnePrimitive (a b θ : ℝ) :
    HasDerivAt (sectorOnePrimitive a b) (sectorOneDensity a b θ) θ := by
  unfold sectorOnePrimitive sectorOneDensity sectorOneSupport sectorOneDerivative
  have htwo : HasDerivAt (fun x : ℝ => 2 * x) 2 θ := by
    simpa using (hasDerivAt_id θ).const_mul 2
  have hsin : HasDerivAt (fun x : ℝ => sin (2 * x)) (2 * cos (2 * θ)) θ := by
    exact ((Real.hasDerivAt_sin (2 * θ)).comp θ htwo).congr_deriv (by ring)
  have hcos : HasDerivAt (fun x : ℝ => cos (2 * x)) (-2 * sin (2 * θ)) θ := by
    exact ((Real.hasDerivAt_cos (2 * θ)).comp θ htwo).congr_deriv (by ring)
  have hprim :=
    (hsin.mul_const (((1 + a) ^ 2 - (1 + b) ^ 2) / 2)).sub
      (hcos.mul_const ((1 + a) * (1 + b)))
  exact hprim.congr_deriv (by
    rw [Real.sin_two_mul, Real.cos_two_mul]
    nlinarith [Real.sin_sq_add_cos_sq θ])

/-- Endpoint evaluation of the Sector I primitive. -/
theorem sectorOnePrimitive_endpoints (a b : ℝ) :
    sectorOnePrimitive a b (π / 2) - sectorOnePrimitive a b 0 =
      2 * (1 + a) * (1 + b) := by
  have hzero : sectorOnePrimitive a b 0 = -(1 + a) * (1 + b) := by
    simp [sectorOnePrimitive]
    ring
  have hright : sectorOnePrimitive a b (π / 2) = (1 + a) * (1 + b) := by
    rw [sectorOnePrimitive, show 2 * (π / 2) = π by ring, Real.sin_pi, Real.cos_pi]
    ring
  rw [hright, hzero]
  ring

/-- The complete exact Sector I support-density contribution. -/
theorem integral_sectorOneDensity (a b : ℝ) :
    (∫ θ in (0 : ℝ)..π / 2, sectorOneDensity a b θ) =
      2 * (1 + a) * (1 + b) := by
  have hint : IntervalIntegrable (sectorOneDensity a b) volume 0 (π / 2) := by
    apply Continuous.intervalIntegrable
    unfold sectorOneDensity sectorOneSupport sectorOneDerivative
    fun_prop
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt
    (fun θ _ => hasDerivAt_sectorOnePrimitive a b θ) hint,
    sectorOnePrimitive_endpoints]

#print axioms hasDerivAt_sectorOneSupport
#print axioms hasDerivAt_sectorOnePrimitive
#print axioms sectorOnePrimitive_endpoints
#print axioms integral_sectorOneDensity

end L2Hexagon
