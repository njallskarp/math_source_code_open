import L2Hexagon.CyclicBoundaryPath
import Mathlib.Analysis.Calculus.Deriv.MeanValue

/-!
# Embedded curved pieces and positive local orientation

For `a,b>0`, the canonical Sector II and Sector III boundary arcs have
strictly positive tangential speed `h+h''`.  Since their normal angles lie
strictly between `0` and `pi`, their first Cartesian coordinate has strictly
negative derivative.  Consequently both closed angular parametrizations, and
both bundled path parametrizations, are injective.

The same positive-speed calculation shows that the oriented determinant
density on each curved piece is strictly positive.  Together with the already
checked positive jump determinants, this supplies a local orientation and
per-piece embeddedness precursor for the eventual simple closed path theorem.

This file does not claim cross-piece disjointness or injectivity of the full
concatenated cyclic path.
-/

open Real Set

namespace L2Hexagon

noncomputable section

/-! ## Positive tangential speed -/

/-- The Sector II tangential speed `h+h''` is positive at every angle. -/
theorem sectorTwoBoundarySpeed_pos {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    0 < sectorTwoBoundarySpeed a b θ := by
  have hsq : 0 < sectorTwoSq a b θ := sectorTwoSq_pos hb θ
  have hsupp : 0 < sectorTwoSupport a b θ := by
    exact Real.sqrt_pos.2 hsq
  have hcurv : 0 < sectorTwoCurvature a b θ := by
    unfold sectorTwoCurvature
    exact div_pos (sq_pos_of_pos (by linarith)) hsq
  have hprod := sectorTwoSupport_mul_boundarySpeed_eq_curvature (a := a) hb θ
  nlinarith

/-- The Sector III tangential speed `h+h''` is positive at every angle. -/
theorem sectorThreeBoundarySpeed_pos {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    0 < sectorThreeBoundarySpeed a b θ := by
  have hsq : 0 < sectorThreeSq a b θ := sectorThreeSq_pos ha θ
  have hsupp : 0 < sectorThreeSupport a b θ := by
    exact Real.sqrt_pos.2 hsq
  have hcurv : 0 < sectorThreeCurvature a b θ := by
    unfold sectorThreeCurvature
    exact div_pos (sq_pos_of_pos (by linarith)) hsq
  have hprod := sectorThreeSupport_mul_boundarySpeed_eq_curvature (b := b) ha θ
  nlinarith

/-! ## Strict decrease of the first coordinate -/

/-- The Sector II boundary first coordinate strictly decreases throughout its
closed angular interval. -/
theorem strictAntiOn_sectorTwoBoundaryX {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    StrictAntiOn (sectorTwoBoundaryX a b)
      (Icc (π / 2) (π / 2 + arctan (b / a))) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  apply strictAntiOn_of_deriv_neg (convex_Icc (π / 2)
    (π / 2 + arctan (b / a)))
  · exact (continuous_iff_continuousAt.2 fun θ =>
      (hasDerivAt_sectorTwoBoundaryX hb θ).continuousAt).continuousOn
  · intro θ hθ
    have hθ' : θ ∈ Ioo (π / 2) (π / 2 + arctan (b / a)) := by
      simpa only [interior_Icc] using hθ
    have hθpos : 0 < θ := lt_trans (by positivity : 0 < π / 2) hθ'.1
    have hθpi : θ < π := by
      have hφlt : arctan (b / a) < π / 2 := by
        simpa [generatorAngle] using hφ.2
      nlinarith [hθ'.2, hφlt]
    rw [(hasDerivAt_sectorTwoBoundaryX hb θ).deriv]
    unfold sectorTwoBoundaryDX
    have hspeed := sectorTwoBoundarySpeed_pos (a := a) hb θ
    have hsin := Real.sin_pos_of_pos_of_lt_pi hθpos hθpi
    nlinarith [mul_pos hspeed hsin]

/-- The Sector III boundary first coordinate strictly decreases throughout its
closed angular interval. -/
theorem strictAntiOn_sectorThreeBoundaryX {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    StrictAntiOn (sectorThreeBoundaryX a b)
      (Icc (π / 2 + arctan (b / a)) π) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  apply strictAntiOn_of_deriv_neg (convex_Icc
    (π / 2 + arctan (b / a)) π)
  · exact (continuous_iff_continuousAt.2 fun θ =>
      (hasDerivAt_sectorThreeBoundaryX ha θ).continuousAt).continuousOn
  · intro θ hθ
    have hθ' : θ ∈ Ioo (π / 2 + arctan (b / a)) π := by
      simpa only [interior_Icc] using hθ
    have hφpos : 0 < arctan (b / a) := by
      simpa [generatorAngle] using hφ.1
    have hθpos : 0 < θ := by
      nlinarith [hθ'.1, hφpos, Real.pi_pos]
    rw [(hasDerivAt_sectorThreeBoundaryX ha θ).deriv]
    unfold sectorThreeBoundaryDX
    have hspeed := sectorThreeBoundarySpeed_pos (b := b) ha θ
    have hsin := Real.sin_pos_of_pos_of_lt_pi hθpos hθ'.2
    nlinarith [mul_pos hspeed hsin]

/-! ## Embedded curved pieces -/

/-- The actual Sector II boundary-point map is injective on its closed angular
interval. -/
theorem injOn_sectorTwoBoundaryPoint {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Set.InjOn (sectorTwoBoundaryPoint a b)
      (Icc (π / 2) (π / 2 + arctan (b / a))) := by
  intro θ hθ ψ hψ hEq
  apply (strictAntiOn_sectorTwoBoundaryX ha hb).injOn hθ hψ
  have := congrArg (fun x : Plane => x 0) hEq
  simpa [sectorTwoBoundaryPoint, planeVector] using this

/-- The actual Sector III boundary-point map is injective on its closed angular
interval. -/
theorem injOn_sectorThreeBoundaryPoint {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Set.InjOn (sectorThreeBoundaryPoint a b)
      (Icc (π / 2 + arctan (b / a)) π) := by
  intro θ hθ ψ hψ hEq
  apply (strictAntiOn_sectorThreeBoundaryX ha hb).injOn hθ hψ
  have := congrArg (fun x : Plane => x 0) hEq
  simpa [sectorThreeBoundaryPoint, planeVector] using this

/-- The bundled Sector II arc path has no self-intersections. -/
theorem injective_sectorTwoArcPath {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Function.Injective (sectorTwoArcPath a b hb) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφpos : 0 < arctan (b / a) := by
    simpa [generatorAngle] using hφ.1
  intro s t hst
  have hs : (Path.segment (π / 2) (π / 2 + arctan (b / a))) s ∈
      Icc (π / 2) (π / 2 + arctan (b / a)) := by
    have hs' : (Path.segment (π / 2) (π / 2 + arctan (b / a))) s ∈
        Set.range (Path.segment (π / 2) (π / 2 + arctan (b / a))) :=
      Set.mem_range_self s
    rw [Path.range_segment,
      segment_eq_Icc (by linarith : (π / 2 : ℝ) ≤ π / 2 + arctan (b / a))] at hs'
    exact hs'
  have ht : (Path.segment (π / 2) (π / 2 + arctan (b / a))) t ∈
      Icc (π / 2) (π / 2 + arctan (b / a)) := by
    have ht' : (Path.segment (π / 2) (π / 2 + arctan (b / a))) t ∈
        Set.range (Path.segment (π / 2) (π / 2 + arctan (b / a))) :=
      Set.mem_range_self t
    rw [Path.range_segment,
      segment_eq_Icc (by linarith : (π / 2 : ℝ) ≤ π / 2 + arctan (b / a))] at ht'
    exact ht'
  have hang : (Path.segment (π / 2) (π / 2 + arctan (b / a))) s =
      (Path.segment (π / 2) (π / 2 + arctan (b / a))) t := by
    apply injOn_sectorTwoBoundaryPoint ha hb hs ht
    simpa [sectorTwoArcPath, Path.map_coe] using hst
  exact Path.segment_injective_of_ne (by linarith :
    (π / 2 : ℝ) ≠ π / 2 + arctan (b / a)) hang

/-- The bundled Sector III arc path has no self-intersections. -/
theorem injective_sectorThreeArcPath {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Function.Injective (sectorThreeArcPath a b ha) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφlt : arctan (b / a) < π / 2 := by
    simpa [generatorAngle] using hφ.2
  intro s t hst
  have hs : (Path.segment (π / 2 + arctan (b / a)) π) s ∈
      Icc (π / 2 + arctan (b / a)) π := by
    have hs' : (Path.segment (π / 2 + arctan (b / a)) π) s ∈
        Set.range (Path.segment (π / 2 + arctan (b / a)) π) :=
      Set.mem_range_self s
    rw [Path.range_segment,
      segment_eq_Icc (by nlinarith [hφlt] :
        (π / 2 + arctan (b / a) : ℝ) ≤ π)] at hs'
    exact hs'
  have ht : (Path.segment (π / 2 + arctan (b / a)) π) t ∈
      Icc (π / 2 + arctan (b / a)) π := by
    have ht' : (Path.segment (π / 2 + arctan (b / a)) π) t ∈
        Set.range (Path.segment (π / 2 + arctan (b / a)) π) :=
      Set.mem_range_self t
    rw [Path.range_segment,
      segment_eq_Icc (by nlinarith [hφlt] :
        (π / 2 + arctan (b / a) : ℝ) ≤ π)] at ht'
    exact ht'
  have hang : (Path.segment (π / 2 + arctan (b / a)) π) s =
      (Path.segment (π / 2 + arctan (b / a)) π) t := by
    apply injOn_sectorThreeBoundaryPoint ha hb hs ht
    simpa [sectorThreeArcPath, Path.map_coe] using hst
  exact Path.segment_injective_of_ne (by linarith :
    (π / 2 + arctan (b / a) : ℝ) ≠ π) hang

/-! ## Positive local orientation -/

/-- The Sector II canonical arc has strictly positive oriented density. -/
theorem sectorTwoBoundaryOrientedDensity_pos {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    0 < sectorTwoBoundaryOrientedDensity a b θ := by
  rw [sectorTwoBoundaryOrientedDensity_eq_curvature hb]
  unfold sectorTwoCurvature
  exact div_pos (sq_pos_of_pos (by linarith)) (sectorTwoSq_pos hb θ)

/-- The Sector III canonical arc has strictly positive oriented density. -/
theorem sectorThreeBoundaryOrientedDensity_pos {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    0 < sectorThreeBoundaryOrientedDensity a b θ := by
  rw [sectorThreeBoundaryOrientedDensity_eq_curvature ha]
  unfold sectorThreeCurvature
  exact div_pos (sq_pos_of_pos (by linarith)) (sectorThreeSq_pos ha θ)

#print axioms sectorTwoBoundarySpeed_pos
#print axioms sectorThreeBoundarySpeed_pos
#print axioms strictAntiOn_sectorTwoBoundaryX
#print axioms strictAntiOn_sectorThreeBoundaryX
#print axioms injOn_sectorTwoBoundaryPoint
#print axioms injOn_sectorThreeBoundaryPoint
#print axioms injective_sectorTwoArcPath
#print axioms injective_sectorThreeArcPath
#print axioms sectorTwoBoundaryOrientedDensity_pos
#print axioms sectorThreeBoundaryOrientedDensity_pos

end

end L2Hexagon
