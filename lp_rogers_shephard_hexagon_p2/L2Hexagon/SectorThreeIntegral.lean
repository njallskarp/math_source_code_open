import L2Hexagon.SectorTwoIntegral

/-!
# Sector III from the Sector II symmetry

For the third upper-half-circle support sector of the normalized hexagon, put

`W(θ) = (1+a) cos θ + b sin θ`

and `F₃(θ) = sin² θ + W(θ)²`.  Its support-area density is written
directly from `F₃` and `F₃'/2` below.  Under the reflection

`η = 3π/2 - θ`,

these literal Sector III expressions become the Sector II expressions with
the parameters interchanged.  The identity

`arctan (a/b) = π/2 - arctan (b/a)`

then identifies the reflected endpoints.  This module transports the already
proved Sector II integral and obtains the complete Sector III contribution

`(1+a)(π/2-arctan(b/a)) - ab`.

No planar support-area theorem or set-level sector restriction is asserted
here.
-/

open Real Set MeasureTheory
open scoped Interval

namespace L2Hexagon

/-- The nontrivial moving coordinate in the Sector III support square. -/
noncomputable def sectorThreeW (a b θ : ℝ) : ℝ :=
  (1 + a) * cos θ + b * sin θ

/-- The derivative of `sectorThreeW`. -/
noncomputable def sectorThreeZ (a b θ : ℝ) : ℝ :=
  -(1 + a) * sin θ + b * cos θ

/-- The literal squared support on Sector III. -/
noncomputable def sectorThreeSq (a b θ : ℝ) : ℝ :=
  sin θ ^ 2 + sectorThreeW a b θ ^ 2

/-- The quantity `h h' = F₃'/2` on Sector III. -/
noncomputable def sectorThreeBoundary (a b θ : ℝ) : ℝ :=
  sin θ * cos θ + sectorThreeW a b θ * sectorThreeZ a b θ

/-- The support-area density written directly from the Sector III square. -/
noncomputable def sectorThreeDensity (a b θ : ℝ) : ℝ :=
  sectorThreeSq a b θ - sectorThreeBoundary a b θ ^ 2 / sectorThreeSq a b θ

/-- Cosine under the orientation-reversing Sector II/III reflection. -/
theorem cos_three_pi_div_two_sub (θ : ℝ) :
    cos (3 * π / 2 - θ) = -sin θ := by
  rw [show 3 * π / 2 - θ = (π - θ) + π / 2 by ring,
    Real.cos_add_pi_div_two, Real.sin_pi_sub]

/-- Sine under the orientation-reversing Sector II/III reflection. -/
theorem sin_three_pi_div_two_sub (θ : ℝ) :
    sin (3 * π / 2 - θ) = -cos θ := by
  rw [show 3 * π / 2 - θ = (π - θ) + π / 2 by ring,
    Real.sin_add_pi_div_two, Real.cos_pi_sub]

/-- The Sector III support square is reflected Sector II with swapped parameters. -/
theorem sectorThreeSq_reflect (a b θ : ℝ) :
    sectorThreeSq a b θ = sectorTwoSq b a (3 * π / 2 - θ) := by
  rw [sectorThreeSq, sectorThreeW, sectorTwoSq, sectorTwoU,
    cos_three_pi_div_two_sub, sin_three_pi_div_two_sub]
  ring

/-- The endpoint quantity changes sign under the reflection. -/
theorem sectorThreeBoundary_reflect (a b θ : ℝ) :
    sectorThreeBoundary a b θ =
      -sectorTwoBoundary b a (3 * π / 2 - θ) := by
  rw [sectorThreeBoundary, sectorThreeW, sectorThreeZ, sectorTwoBoundary,
    sectorTwoU, sectorTwoV, cos_three_pi_div_two_sub, sin_three_pi_div_two_sub]
  ring

/-- The support-area density is invariant under the reflection and parameter swap. -/
theorem sectorThreeDensity_reflect (a b θ : ℝ) :
    sectorThreeDensity a b θ = sectorTwoDensity b a (3 * π / 2 - θ) := by
  unfold sectorThreeDensity sectorTwoDensity
  rw [sectorThreeSq_reflect, sectorThreeBoundary_reflect]
  ring

/-- Positive reciprocal slopes give complementary generator angles. -/
theorem arctan_div_swap {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    arctan (a / b) = π / 2 - arctan (b / a) := by
  have hratio : a / b = (b / a)⁻¹ := by
    field_simp [ha.ne', hb.ne']
  rw [hratio, Real.arctan_inv_of_pos (div_pos hb ha)]

/--
The exact Sector III integral follows from Sector II by the reflection
`η=3π/2-θ`, including the orientation and both transformed endpoints.
-/
theorem integral_sectorThreeDensity {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    (∫ θ in π / 2 + arctan (b / a)..π, sectorThreeDensity a b θ) =
      (1 + a) * (π / 2 - arctan (b / a)) - a * b := by
  have hangle := arctan_div_swap ha hb
  calc
    (∫ θ in π / 2 + arctan (b / a)..π, sectorThreeDensity a b θ) =
        ∫ θ in π / 2 + arctan (b / a)..π,
          sectorTwoDensity b a (3 * π / 2 - θ) := by
            apply intervalIntegral.integral_congr
            intro θ _
            exact sectorThreeDensity_reflect a b θ
    _ = ∫ η in 3 * π / 2 - π..
          3 * π / 2 - (π / 2 + arctan (b / a)), sectorTwoDensity b a η := by
            rw [intervalIntegral.integral_comp_sub_left]
    _ = ∫ η in π / 2..π / 2 + arctan (a / b), sectorTwoDensity b a η := by
            congr 1
            · ring
            · rw [hangle]
              ring
    _ = (1 + a) * arctan (a / b) - b * a := integral_sectorTwoDensity hb ha
    _ = (1 + a) * (π / 2 - arctan (b / a)) - a * b := by
          rw [hangle]
          ring

#print axioms cos_three_pi_div_two_sub
#print axioms sin_three_pi_div_two_sub
#print axioms sectorThreeSq_reflect
#print axioms sectorThreeBoundary_reflect
#print axioms sectorThreeDensity_reflect
#print axioms arctan_div_swap
#print axioms integral_sectorThreeDensity

end L2Hexagon
