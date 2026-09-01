import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Tactic

/-!
# Squared Firey support identity for three segments

For a segment `[0, u]`, the support value in direction `xi` is the positive
part of `inner u xi`.  The support of the sum of three such segments is the
sum of the three positive parts.  This file proves the exact algebraic
identity obtained after adding the square of that support to the square of
the reflected support.

The result is the local support-function reduction used for the normalized
centrally symmetric hexagon in the accompanying paper proof.  It is stated
for an arbitrary real inner-product space.
-/

open Real

namespace L2Hexagon

/-- The positive part of a real number. -/
def positivePart (x : ℝ) : ℝ := max x 0

/-- Positive part expressed through the absolute value. -/
theorem positivePart_eq_half_add_abs (x : ℝ) :
    positivePart x = (x + |x|) / 2 := by
  rcases le_total 0 x with hx | hx
  · rw [positivePart, max_eq_left hx, abs_of_nonneg hx]
    ring
  · rw [positivePart, max_eq_right hx, abs_of_nonpos hx]
    ring

/--
The scalar three-generator identity.  The two terms on the left are the
squared supports of a three-segment zonotope and of its reflection.  On the
right, the absolute-value sum is twice the support of the centered zonotope,
and the signed sum is twice the support of its center.
-/
theorem three_positive_parts_sq_identity (x y z : ℝ) :
    (positivePart x + positivePart y + positivePart z) ^ 2
        + (positivePart (-x) + positivePart (-y) + positivePart (-z)) ^ 2 =
      2 * (((|x| + |y| + |z|) / 2) ^ 2 + ((x + y + z) / 2) ^ 2) := by
  simp only [positivePart_eq_half_add_abs, abs_neg]
  ring

section InnerProduct

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The support expression for the Minkowski sum `[0,u] + [0,v] + [0,w]`. -/
noncomputable def threeSegmentSupport (u v w ξ : E) : ℝ :=
  positivePart (inner ℝ u ξ) + positivePart (inner ℝ v ξ)
    + positivePart (inner ℝ w ξ)

/--
The squared `p = 2` support expression for a three-generator zonotope and
its reflection, decomposed into its centered support and translation parts.
-/
theorem threeSegmentSupport_sq_add_reflection_sq (u v w ξ : E) :
    threeSegmentSupport u v w ξ ^ 2 + threeSegmentSupport (-u) (-v) (-w) ξ ^ 2 =
      2 *
        (((|inner ℝ u ξ| + |inner ℝ v ξ| + |inner ℝ w ξ|) / 2) ^ 2
          + ((inner ℝ u ξ + inner ℝ v ξ + inner ℝ w ξ) / 2) ^ 2) := by
  simpa only [threeSegmentSupport, inner_neg_left] using
    three_positive_parts_sq_identity (inner ℝ u ξ) (inner ℝ v ξ) (inner ℝ w ξ)

end InnerProduct

#print axioms positivePart_eq_half_add_abs
#print axioms three_positive_parts_sq_identity
#print axioms threeSegmentSupport_sq_add_reflection_sq

end L2Hexagon
