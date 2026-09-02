import L2Hexagon.ClosingExposedFace
import Mathlib.Analysis.Calculus.LocalExtr.Basic

/-!
# Lower exposed faces and curved-point uniqueness

The exact halfspace body is centrally symmetric.  We first package this as a
transport theorem for an arbitrary exposed face and apply it to the three
already classified upper-half jump faces.

For a normal in the interior of a curved sector, the support function agrees
with a differentiable scalar support on a whole neighbourhood.  A body point
on the supporting line therefore makes the support gap locally minimal.  The
vanishing derivative of that gap fixes both its normal and tangent pairings,
and hence fixes the point itself.  The transition normals are deliberately
excluded because their exposed faces are nontrivial segments.
-/

open Real Set Filter

namespace L2Hexagon

/-! ## Exposed faces and central symmetry -/

/-- The literal exposed face of the exact normalized halfspace body. -/
noncomputable def normalizedExposedFace (a b : ℝ) (u : Plane) : Set Plane :=
  {x | x ∈ normalizedLpSumTwo a b ∧
    inner ℝ x u = normalizedFireySupportVec a b u}

/-- Negation transports the exposed face at `u` exactly to the face at `-u`. -/
theorem normalizedExposedFace_neg (a b : ℝ) (u : Plane) :
    normalizedExposedFace a b (-u) = -normalizedExposedFace a b u := by
  ext x
  rw [Set.mem_neg]
  constructor
  · rintro ⟨hx, hxu⟩
    refine ⟨(neg_mem_normalizedLpSumTwo_iff a b x).2 hx, ?_⟩
    rw [inner_neg_left, ← inner_neg_right, hxu,
      normalizedFireySupportVec_neg]
  · rintro ⟨hx, hxu⟩
    refine ⟨(neg_mem_normalizedLpSumTwo_iff a b x).1 hx, ?_⟩
    rw [inner_neg_right, ← inner_neg_left, hxu,
      normalizedFireySupportVec_neg]

/-- The complete lower face opposite the first upper jump. -/
theorem exposedFace_neg_planeE2_eq_neg_sectorOneTwoJump {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedExposedFace a b (-planeE2) = -sectorOneTwoJump a b := by
  rw [normalizedExposedFace_neg]
  change -{x | x ∈ normalizedLpSumTwo a b ∧
      inner ℝ x planeE2 = normalizedFireySupportVec a b planeE2} = _
  rw [exposedFace_planeE2_eq_sectorOneTwoJump ha hb]

/-- The complete lower face opposite the middle upper jump. -/
theorem exposedFace_neg_middleNormal_eq_neg_sectorTwoThreeJump {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedExposedFace a b (-middleNormal a b) = -sectorTwoThreeJump a b := by
  rw [normalizedExposedFace_neg]
  change -{x | x ∈ normalizedLpSumTwo a b ∧
      inner ℝ x (middleNormal a b) =
        normalizedFireySupportVec a b (middleNormal a b)} = _
  rw [exposedFace_middleNormal_eq_sectorTwoThreeJump ha hb]

/-- The complete lower face opposite the closing upper jump. -/
theorem exposedFace_planeE1_eq_neg_sectorThreeOneJump {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedExposedFace a b planeE1 = -sectorThreeOneJump a b := by
  have h := normalizedExposedFace_neg a b (-planeE1)
  simp only [neg_neg] at h
  rw [h]
  change -{x | x ∈ normalizedLpSumTwo a b ∧
      inner ℝ x (-planeE1) = normalizedFireySupportVec a b (-planeE1)} = _
  rw [exposedFace_neg_planeE1_eq_sectorThreeOneJump ha hb]

/-! ## The differentiable support-gap mechanism -/

/-- Coordinate formula for pairing an arbitrary point with the angular unit
normal. -/
theorem inner_planeDirection_apply (x : Plane) (θ : ℝ) :
    inner ℝ x (planeDirection θ) = x 0 * cos θ + x 1 * sin θ := by
  rw [PiLp.inner_apply, Fin.sum_univ_two]
  simp [planeDirection, planeVector]
  ring

/-- Pairing a fixed plane point with the angular unit normal differentiates
to its pairing with the angular unit tangent. -/
theorem hasDerivAt_inner_planeDirection (x : Plane) (θ : ℝ) :
    HasDerivAt (fun t ↦ inner ℝ x (planeDirection t))
      (-x 0 * sin θ + x 1 * cos θ) θ := by
  rw [show (fun t ↦ inner ℝ x (planeDirection t)) =
      fun t ↦ x 0 * cos t + x 1 * sin t by
        funext t
        exact inner_planeDirection_apply x t]
  exact (((Real.hasDerivAt_cos θ).const_mul (x 0)).add
    ((Real.hasDerivAt_sin θ).const_mul (x 1))).congr_deriv (by ring)

/-- Normal and tangent pairings at one angle determine a plane point. -/
theorem eq_of_normal_tangent_pairings {x y : Plane} {θ : ℝ}
    (hn : inner ℝ x (planeDirection θ) = inner ℝ y (planeDirection θ))
    (ht : -x 0 * sin θ + x 1 * cos θ =
      -y 0 * sin θ + y 1 * cos θ) : x = y := by
  rw [inner_planeDirection_apply, inner_planeDirection_apply] at hn
  ext i
  fin_cases i
  · change x 0 = y 0
    have hcoord : (x 0 - y 0) * (cos θ ^ 2 + sin θ ^ 2) = 0 := by
      linear_combination cos θ * hn - sin θ * ht
    rw [add_comm, Real.sin_sq_add_cos_sq, mul_one] at hcoord
    linarith
  · change x 1 = y 1
    have hcoord : (x 1 - y 1) * (sin θ ^ 2 + cos θ ^ 2) = 0 := by
      linear_combination sin θ * hn + cos θ * ht
    rw [Real.sin_sq_add_cos_sq, mul_one] at hcoord
    linarith

/-! ## Sector II singleton faces -/

/-- On the closed second sector, the exact vector support is the displayed
square-root support, not only its square. -/
theorem normalizedFireySupportVec_eq_sectorTwoSupport {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2) (π / 2 + arctan (b / a))) :
    normalizedFireySupportVec a b (planeDirection θ) =
      sectorTwoSupport a b θ := by
  rw [normalizedFireySupportVec, normalizedFireySupportVecSq_planeDirection,
    normalizedFireySupportSq_eq_sectorTwoSq_on_sector ha hb hθ]
  rfl

/-- A supporting body point in the open second sector makes the difference
between the differentiable sector support and its own normal pairing locally
minimal. -/
theorem sectorTwo_supportGap_isLocalMin {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Ioo (π / 2) (π / 2 + arctan (b / a)))
    {x : Plane} (hx : x ∈ normalizedLpSumTwo a b)
    (hsupport : inner ℝ x (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ)) :
    IsLocalMin
      (fun t ↦ sectorTwoSupport a b t - inner ℝ x (planeDirection t)) θ := by
  have hθsupport : inner ℝ x (planeDirection θ) = sectorTwoSupport a b θ := by
    rw [hsupport, normalizedFireySupportVec_eq_sectorTwoSupport ha hb
      ⟨hθ.1.le, hθ.2.le⟩]
  filter_upwards [Ioo_mem_nhds hθ.1 hθ.2] with t ht
  have hbound := hx (planeDirection t)
  rw [normalizedFireySupportVec_eq_sectorTwoSupport ha hb
    ⟨ht.1.le, ht.2.le⟩] at hbound
  linarith

/-- Any supporting body point at an open Sector II normal has the canonical
tangent pairing. -/
theorem sectorTwo_tangent_pairing_of_support {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Ioo (π / 2) (π / 2 + arctan (b / a)))
    {x : Plane} (hx : x ∈ normalizedLpSumTwo a b)
    (hsupport : inner ℝ x (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ)) :
    -x 0 * sin θ + x 1 * cos θ = sectorTwoSupportDerivative a b θ := by
  have hmin := sectorTwo_supportGap_isLocalMin ha hb hθ hx hsupport
  have hderiv : HasDerivAt
      (fun t ↦ sectorTwoSupport a b t - inner ℝ x (planeDirection t))
      (sectorTwoSupportDerivative a b θ -
        (-x 0 * sin θ + x 1 * cos θ)) θ :=
    (hasDerivAt_sectorTwoSupport (a := a) hb θ).sub
      (hasDerivAt_inner_planeDirection x θ)
  have hzero := hmin.hasDerivAt_eq_zero hderiv
  linarith

/-- Every open Sector II support face is the singleton canonical curved point. -/
theorem exposedFace_sectorTwo_eq_singleton {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Ioo (π / 2) (π / 2 + arctan (b / a))) :
    normalizedExposedFace a b (planeDirection θ) =
      {planeVector (sectorTwoBoundaryX a b θ) (sectorTwoBoundaryY a b θ)} := by
  ext x
  simp only [normalizedExposedFace, Set.mem_ofPred_eq, Set.mem_singleton_iff]
  constructor
  · rintro ⟨hx, hsupport⟩
    have hySupport := sectorTwoBoundaryPoint_supporting ha hb
      ⟨hθ.1.le, hθ.2.le⟩
    apply eq_of_normal_tangent_pairings (hsupport.trans hySupport.symm)
    have htangent := sectorTwo_tangent_pairing_of_support ha hb hθ hx hsupport
    have hyTangent :
        -sectorTwoBoundaryX a b θ * sin θ +
            sectorTwoBoundaryY a b θ * cos θ =
          sectorTwoSupportDerivative a b θ := by
      simpa [sectorTwoBoundaryX, sectorTwoBoundaryY] using
        supportBoundary_tangent_pairing (sectorTwoSupport a b)
          (sectorTwoSupportDerivative a b) θ
    exact htangent.trans hyTangent.symm
  · rintro rfl
    exact ⟨sectorTwoBoundaryPoint_mem_normalizedLpSumTwo hb,
      sectorTwoBoundaryPoint_supporting ha hb ⟨hθ.1.le, hθ.2.le⟩⟩

/-! ## Sector III singleton faces -/

/-- On the closed third sector, the exact vector support is the displayed
square-root support. -/
theorem normalizedFireySupportVec_eq_sectorThreeSupport {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2 + arctan (b / a)) π) :
    normalizedFireySupportVec a b (planeDirection θ) =
      sectorThreeSupport a b θ := by
  rw [normalizedFireySupportVec, normalizedFireySupportVecSq_planeDirection,
    normalizedFireySupportSq_eq_sectorThreeSq_on_sector ha hb hθ]
  rfl

/-- A supporting body point in the open third sector makes its differentiable
support gap locally minimal. -/
theorem sectorThree_supportGap_isLocalMin {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Ioo (π / 2 + arctan (b / a)) π)
    {x : Plane} (hx : x ∈ normalizedLpSumTwo a b)
    (hsupport : inner ℝ x (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ)) :
    IsLocalMin
      (fun t ↦ sectorThreeSupport a b t - inner ℝ x (planeDirection t)) θ := by
  have hθsupport : inner ℝ x (planeDirection θ) = sectorThreeSupport a b θ := by
    rw [hsupport, normalizedFireySupportVec_eq_sectorThreeSupport ha hb
      ⟨hθ.1.le, hθ.2.le⟩]
  filter_upwards [Ioo_mem_nhds hθ.1 hθ.2] with t ht
  have hbound := hx (planeDirection t)
  rw [normalizedFireySupportVec_eq_sectorThreeSupport ha hb
    ⟨ht.1.le, ht.2.le⟩] at hbound
  linarith

/-- Any supporting body point at an open Sector III normal has the canonical
tangent pairing. -/
theorem sectorThree_tangent_pairing_of_support {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Ioo (π / 2 + arctan (b / a)) π)
    {x : Plane} (hx : x ∈ normalizedLpSumTwo a b)
    (hsupport : inner ℝ x (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ)) :
    -x 0 * sin θ + x 1 * cos θ = sectorThreeSupportDerivative a b θ := by
  have hmin := sectorThree_supportGap_isLocalMin ha hb hθ hx hsupport
  have hderiv : HasDerivAt
      (fun t ↦ sectorThreeSupport a b t - inner ℝ x (planeDirection t))
      (sectorThreeSupportDerivative a b θ -
        (-x 0 * sin θ + x 1 * cos θ)) θ :=
    (hasDerivAt_sectorThreeSupport (b := b) ha θ).sub
      (hasDerivAt_inner_planeDirection x θ)
  have hzero := hmin.hasDerivAt_eq_zero hderiv
  linarith

/-- Every open Sector III support face is the singleton canonical curved point. -/
theorem exposedFace_sectorThree_eq_singleton {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Ioo (π / 2 + arctan (b / a)) π) :
    normalizedExposedFace a b (planeDirection θ) =
      {planeVector (sectorThreeBoundaryX a b θ) (sectorThreeBoundaryY a b θ)} := by
  ext x
  simp only [normalizedExposedFace, Set.mem_ofPred_eq, Set.mem_singleton_iff]
  constructor
  · rintro ⟨hx, hsupport⟩
    have hySupport := sectorThreeBoundaryPoint_supporting ha hb
      ⟨hθ.1.le, hθ.2.le⟩
    apply eq_of_normal_tangent_pairings (hsupport.trans hySupport.symm)
    have htangent := sectorThree_tangent_pairing_of_support ha hb hθ hx hsupport
    have hyTangent :
        -sectorThreeBoundaryX a b θ * sin θ +
            sectorThreeBoundaryY a b θ * cos θ =
          sectorThreeSupportDerivative a b θ := by
      simpa [sectorThreeBoundaryX, sectorThreeBoundaryY] using
        supportBoundary_tangent_pairing (sectorThreeSupport a b)
          (sectorThreeSupportDerivative a b) θ
    exact htangent.trans hyTangent.symm
  · rintro rfl
    exact ⟨sectorThreeBoundaryPoint_mem_normalizedLpSumTwo ha,
      sectorThreeBoundaryPoint_supporting ha hb ⟨hθ.1.le, hθ.2.le⟩⟩

#print axioms normalizedExposedFace_neg
#print axioms exposedFace_neg_planeE2_eq_neg_sectorOneTwoJump
#print axioms exposedFace_neg_middleNormal_eq_neg_sectorTwoThreeJump
#print axioms exposedFace_planeE1_eq_neg_sectorThreeOneJump
#print axioms hasDerivAt_inner_planeDirection
#print axioms eq_of_normal_tangent_pairings
#print axioms sectorTwo_supportGap_isLocalMin
#print axioms exposedFace_sectorTwo_eq_singleton
#print axioms sectorThree_supportGap_isLocalMin
#print axioms exposedFace_sectorThree_eq_singleton

end L2Hexagon
