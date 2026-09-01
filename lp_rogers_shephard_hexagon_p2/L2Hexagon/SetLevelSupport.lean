import L2Hexagon.SupportIdentity
import Mathlib.Analysis.Convex.Segment
import Mathlib.Order.ConditionallyCompleteLattice.Indexed
import Mathlib.Tactic

/-!
# Set-level support of a three-segment zonotope

This file closes the first bridge between the scalar support expression used
in `SupportIdentity.lean` and an actual subset of an inner-product space.

For a set `K`, `setSupportFunction K ξ` is literally the supremum of
`inner x ξ` over `x ∈ K`, using the same subtype-indexed supremum convention
as the source Formal Conjectures statement.  The main theorem proves that
the support of

`[0,u] + [0,v] + [0,w]`

is exactly the sum of the positive parts of the three generator pairings.
-/

open Real Set
open scoped Convex Pointwise

namespace L2Hexagon

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The support function of a set, as a subtype-indexed supremum. -/
noncomputable def setSupportFunction (K : Set E) (ξ : E) : ℝ :=
  ⨆ x : K, inner ℝ (x : E) ξ

/-- The actual Minkowski sum of three closed segments from the origin. -/
def threeSegmentZonotope (u v w : E) : Set E :=
  [0 -[ℝ] u] + [0 -[ℝ] v] + [0 -[ℝ] w]

/-- Every point of `[0,u]` has support value at most the positive part at `u`. -/
theorem inner_le_positivePart_of_mem_segment {u ξ x : E} (hx : x ∈ [0 -[ℝ] u]) :
    inner ℝ x ξ ≤ positivePart (inner ℝ u ξ) := by
  rcases hx with ⟨a, b, ha, hb, hab, rfl⟩
  have hb_one : b ≤ 1 := by linarith
  simp only [smul_zero, zero_add, inner_smul_left]
  rcases le_total 0 (inner ℝ u ξ) with hinner | hinner
  · rw [positivePart, max_eq_left hinner]
    exact mul_le_of_le_one_left hinner hb_one
  · rw [positivePart, max_eq_right hinner]
    exact mul_nonpos_of_nonneg_of_nonpos hb hinner

/-- The positive-part support bound of a segment is attained at one endpoint. -/
theorem exists_mem_segment_inner_eq_positivePart (u ξ : E) :
    ∃ x ∈ [0 -[ℝ] u], inner ℝ x ξ = positivePart (inner ℝ u ξ) := by
  rcases le_total 0 (inner ℝ u ξ) with hinner | hinner
  · refine ⟨u, right_mem_segment ℝ 0 u, ?_⟩
    rw [positivePart, max_eq_left hinner]
  · refine ⟨0, left_mem_segment ℝ 0 u, ?_⟩
    rw [inner_zero_left, positivePart, max_eq_right hinner]

/-- Every point of the three-segment zonotope obeys the predicted support bound. -/
theorem inner_le_threeSegmentSupport_of_mem {u v w ξ x : E}
    (hx : x ∈ threeSegmentZonotope u v w) :
    inner ℝ x ξ ≤ threeSegmentSupport u v w ξ := by
  rcases Set.mem_add.mp hx with ⟨xy, hxy, xw, hxw, rfl⟩
  rcases Set.mem_add.mp hxy with ⟨xu, hxu, xv, hxv, rfl⟩
  simp only [inner_add_left, threeSegmentSupport]
  linarith [inner_le_positivePart_of_mem_segment (ξ := ξ) hxu,
    inner_le_positivePart_of_mem_segment (ξ := ξ) hxv,
    inner_le_positivePart_of_mem_segment (ξ := ξ) hxw]

/-- The predicted support value of the three-segment zonotope is attained. -/
theorem exists_mem_threeSegmentZonotope_inner_eq_support (u v w ξ : E) :
    ∃ x ∈ threeSegmentZonotope u v w,
      inner ℝ x ξ = threeSegmentSupport u v w ξ := by
  obtain ⟨xu, hxu, hu⟩ := exists_mem_segment_inner_eq_positivePart u ξ
  obtain ⟨xv, hxv, hv⟩ := exists_mem_segment_inner_eq_positivePart v ξ
  obtain ⟨xw, hxw, hw⟩ := exists_mem_segment_inner_eq_positivePart w ξ
  refine ⟨xu + xv + xw, Set.add_mem_add (Set.add_mem_add hxu hxv) hxw, ?_⟩
  simp only [inner_add_left, threeSegmentSupport, hu, hv, hw]

/--
The subtype-supremum support of `[0,u]+[0,v]+[0,w]` is the sum of the
positive generator pairings.
-/
theorem setSupportFunction_threeSegmentZonotope (u v w ξ : E) :
    setSupportFunction (threeSegmentZonotope u v w) ξ = threeSegmentSupport u v w ξ := by
  obtain ⟨x, hx, hvalue⟩ := exists_mem_threeSegmentZonotope_inner_eq_support u v w ξ
  have hnonempty : (threeSegmentZonotope u v w).Nonempty := ⟨x, hx⟩
  have hgreatest :
      IsGreatest ((fun y : E ↦ inner ℝ y ξ) '' threeSegmentZonotope u v w)
        (threeSegmentSupport u v w ξ) := by
    constructor
    · exact ⟨x, hx, hvalue⟩
    · rintro _ ⟨y, hy, rfl⟩
      exact inner_le_threeSegmentSupport_of_mem hy
  exact hgreatest.isLUB.ciSup_set_eq hnonempty

#print axioms inner_le_positivePart_of_mem_segment
#print axioms exists_mem_segment_inner_eq_positivePart
#print axioms inner_le_threeSegmentSupport_of_mem
#print axioms exists_mem_threeSegmentZonotope_inner_eq_support
#print axioms setSupportFunction_threeSegmentZonotope

end L2Hexagon
