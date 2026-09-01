import Mathlib.Analysis.SpecialFunctions.Trigonometric.Arctan
import Mathlib.Tactic

/-!
# Strictness of the normalized hexagon deficit

For the normalized three-generator zonotope

`[0,e₁] + [0,(a,b)] + [0,e₂]`, with `a,b > 0`, put
`φ = arctan (b/a)`.  The paper calculation gives the exact area deficit

`a * φ + b * (π/2 - φ)`.

This file machine-checks that this expression is strictly positive and that
the exact candidate area formula is therefore strictly below the planar
Rogers--Shephard constant.  The geometric derivation of the area formula is
kept separate in `PAPER_PROOF.md`; this module does not claim to formalize
Lebesgue area or the Firey sum itself.
-/

open Real

namespace L2Hexagon

/-- The angle of the middle generator after normalizing the two extreme generators. -/
noncomputable def generatorAngle (a b : ℝ) : ℝ := arctan (b / a)

/-- The exact normalized deficit obtained by the support-sector calculation. -/
noncomputable def normalizedDeficit (a b : ℝ) : ℝ :=
  a * generatorAngle a b + b * (π / 2 - generatorAngle a b)

/-- A genuine middle generator has angle strictly between the two extreme generators. -/
theorem generatorAngle_mem_Ioo {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    generatorAngle a b ∈ Set.Ioo 0 (π / 2) := by
  constructor
  · exact Real.arctan_pos.mpr (div_pos hb ha)
  · exact Real.arctan_lt_pi_div_two (b / a)

/-- The normalized deficit is strictly positive for every genuine hexagon. -/
theorem normalizedDeficit_pos {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    0 < normalizedDeficit a b := by
  have hφ := generatorAngle_mem_Ioo ha hb
  exact add_pos (mul_pos ha hφ.1) (mul_pos hb (sub_pos.mpr hφ.2))

/--
Algebraic assembly of the support-sector formula: subtracting the candidate
area from `(π/2+2)` times the normalized hexagon area gives exactly the
positive deficit.
-/
theorem normalized_bound_sub_area_formula (a b : ℝ) :
    (π / 2 + 2) * (1 + a + b)
        - (2 * (1 + a + b) + (1 + b) * generatorAngle a b
          + (1 + a) * (π / 2 - generatorAngle a b)) =
      normalizedDeficit a b := by
  rw [normalizedDeficit]
  ring

/-- The exact normalized candidate area is strictly below the sharp bound. -/
theorem normalized_area_formula_lt_bound {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    2 * (1 + a + b) + (1 + b) * generatorAngle a b
        + (1 + a) * (π / 2 - generatorAngle a b) <
      (π / 2 + 2) * (1 + a + b) := by
  rw [← sub_pos]
  rw [normalized_bound_sub_area_formula]
  exact normalizedDeficit_pos ha hb

#print axioms generatorAngle_mem_Ioo
#print axioms normalizedDeficit_pos
#print axioms normalized_bound_sub_area_formula
#print axioms normalized_area_formula_lt_bound

end L2Hexagon
