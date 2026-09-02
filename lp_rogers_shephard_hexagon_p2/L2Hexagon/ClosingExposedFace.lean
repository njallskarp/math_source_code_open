import L2Hexagon.MiddleExposedFace

/-!
# The closing exposed transition face

Let `S(x,y)=(y,x)`.  The normalized three-generator construction is equivariant
under simultaneously applying `S` and exchanging the parameters `a,b`.
Transporting the already classified vertical face for parameters `(b,a)` gives
the face at `e₁` for `(a,b)`; central symmetry then gives the closing face at
`-e₁`.

The exact theorem proved below is

`{x ∈ normalizedLpSumTwo a b |
    ⟨x,-e₁⟩ = normalizedFireySupportVec a b (-e₁)}
  = sectorThreeOneJump a b`.

All support and body equivariance statements are proved for arbitrary vector
directions before the exposed-face theorem is transported.
-/

open Real Set

namespace L2Hexagon

/-- Coordinate exchange in the chosen Euclidean-plane model. -/
noncomputable def coordinateSwap (x : Plane) : Plane := planeVector (x 1) (x 0)

@[simp] theorem coordinateSwap_apply_zero (x : Plane) : coordinateSwap x 0 = x 1 := by
  simp [coordinateSwap, planeVector]

@[simp] theorem coordinateSwap_apply_one (x : Plane) : coordinateSwap x 1 = x 0 := by
  simp [coordinateSwap, planeVector]

@[simp] theorem coordinateSwap_involutive (x : Plane) :
    coordinateSwap (coordinateSwap x) = x := by
  ext i
  fin_cases i <;> simp

@[simp] theorem coordinateSwap_neg (x : Plane) :
    coordinateSwap (-x) = -coordinateSwap x := by
  ext i
  fin_cases i <;> simp

@[simp] theorem coordinateSwap_add (x y : Plane) :
    coordinateSwap (x + y) = coordinateSwap x + coordinateSwap y := by
  ext i
  fin_cases i <;> simp

@[simp] theorem coordinateSwap_smul (r : ℝ) (x : Plane) :
    coordinateSwap (r • x) = r • coordinateSwap x := by
  ext i
  fin_cases i <;> simp

theorem inner_coordinateSwap_left (x y : Plane) :
    inner ℝ (coordinateSwap x) y = inner ℝ x (coordinateSwap y) := by
  rw [PiLp.inner_apply, PiLp.inner_apply, Fin.sum_univ_two, Fin.sum_univ_two]
  simp
  ring

theorem inner_coordinateSwap_both (x y : Plane) :
    inner ℝ (coordinateSwap x) (coordinateSwap y) = inner ℝ x y := by
  rw [inner_coordinateSwap_left, coordinateSwap_involutive]

@[simp] theorem coordinateSwap_planeE1 : coordinateSwap planeE1 = planeE2 := by
  ext i
  fin_cases i <;> simp [coordinateSwap, planeE1, planeE2, planeVector]

@[simp] theorem coordinateSwap_planeE2 : coordinateSwap planeE2 = planeE1 := by
  ext i
  fin_cases i <;> simp [coordinateSwap, planeE1, planeE2, planeVector]

/-- Swapping coordinates and parameters preserves the literal squared Firey
support in every vector direction. -/
theorem normalizedFireySupportVecSq_coordinateSwap (a b : ℝ) (xi : Plane) :
    normalizedFireySupportVecSq a b (coordinateSwap xi) =
      normalizedFireySupportVecSq b a xi := by
  rw [normalizedFireySupportVecSq_eq_positiveParts,
    normalizedFireySupportVecSq_eq_positiveParts]
  simp only [coordinateSwap, PiLp.inner_apply, Fin.sum_univ_two]
  simp [planeVector]
  have hmid : xi 1 * a + xi 0 * b = xi 0 * b + xi 1 * a := by ring
  have hmidNeg : -(xi 0 * b) + -(xi 1 * a) =
      -(xi 1 * a) + -(xi 0 * b) := by ring
  rw [hmid, hmidNeg]
  ring

/-- The nonnegative square-root support has the same equivariance. -/
theorem normalizedFireySupportVec_coordinateSwap (a b : ℝ) (xi : Plane) :
    normalizedFireySupportVec a b (coordinateSwap xi) =
      normalizedFireySupportVec b a xi := by
  unfold normalizedFireySupportVec
  rw [normalizedFireySupportVecSq_coordinateSwap]

/-- Coordinate exchange maps the exact halfspace body with swapped parameters
onto the original exact halfspace body. -/
theorem coordinateSwap_mem_normalizedLpSumTwo_iff (a b : ℝ) (x : Plane) :
    coordinateSwap x ∈ normalizedLpSumTwo a b ↔ x ∈ normalizedLpSumTwo b a := by
  constructor
  · intro hx xi
    have h := hx (coordinateSwap xi)
    rw [inner_coordinateSwap_both,
      normalizedFireySupportVec_coordinateSwap] at h
    exact h
  · intro hx xi
    have h := hx (coordinateSwap xi)
    rw [← inner_coordinateSwap_left,
      normalizedFireySupportVec_coordinateSwap] at h
    exact h

/-- Membership in the centrally symmetric halfspace body is invariant under
negation, in both directions. -/
theorem neg_mem_normalizedLpSumTwo_iff (a b : ℝ) (x : Plane) :
    -x ∈ normalizedLpSumTwo a b ↔ x ∈ normalizedLpSumTwo a b := by
  constructor
  · intro hx
    have := neg_mem_normalizedLpSumTwo hx
    simpa using this
  · exact neg_mem_normalizedLpSumTwo

/-- The involution that transports the positive vertical face with exchanged
parameters to the closing negative horizontal face. -/
noncomputable def closingSymmetry (x : Plane) : Plane := -coordinateSwap x

@[simp] theorem closingSymmetry_involutive (x : Plane) :
    closingSymmetry (closingSymmetry x) = x := by
  simp [closingSymmetry]

@[simp] theorem closingSymmetry_add (x y : Plane) :
    closingSymmetry (x + y) = closingSymmetry x + closingSymmetry y := by
  ext i
  fin_cases i <;> simp [closingSymmetry, coordinateSwap, planeVector] <;> ring

@[simp] theorem closingSymmetry_smul (r : ℝ) (x : Plane) :
    closingSymmetry (r • x) = r • closingSymmetry x := by
  simp [closingSymmetry]

theorem closingSymmetry_mem_normalizedLpSumTwo_iff (a b : ℝ) (x : Plane) :
    closingSymmetry x ∈ normalizedLpSumTwo b a ↔
      x ∈ normalizedLpSumTwo a b := by
  rw [closingSymmetry, neg_mem_normalizedLpSumTwo_iff,
    coordinateSwap_mem_normalizedLpSumTwo_iff]

theorem inner_closingSymmetry_planeE2 (x : Plane) :
    inner ℝ (closingSymmetry x) planeE2 = inner ℝ x (-planeE1) := by
  rw [closingSymmetry, inner_neg_left, inner_coordinateSwap_left,
    coordinateSwap_planeE2, inner_neg_right]

theorem normalizedFireySupportVec_closingDirection (a b : ℝ) :
    normalizedFireySupportVec b a planeE2 =
      normalizedFireySupportVec a b (-planeE1) := by
  rw [normalizedFireySupportVec_neg]
  have h := normalizedFireySupportVec_coordinateSwap b a planeE1
  simpa using h

/-- The Sector III endpoint at `pi` has the expected Cartesian coordinates. -/
theorem sectorThreeBoundaryPoint_pi {a b : ℝ} (ha : 0 < a) :
    planeVector (sectorThreeBoundaryX a b π) (sectorThreeBoundaryY a b π) =
      planeVector (-(1 + a)) (-b) := by
  ext i
  fin_cases i
  · simp [sectorThreeBoundaryX, supportBoundaryX,
      sectorThreeSupport_pi ha, sectorThreeSupportDerivative_pi ha, planeVector]
  · simp [sectorThreeBoundaryY, supportBoundaryY,
      sectorThreeSupport_pi ha, sectorThreeSupportDerivative_pi ha, planeVector]

@[simp] theorem closingSymmetry_sectorOneVertex (a b : ℝ) :
    closingSymmetry (sectorOneVertex b a) = -sectorOneVertex a b := by
  ext i
  fin_cases i <;>
    simp [closingSymmetry, coordinateSwap, sectorOneVertex, planeVector]

@[simp] theorem closingSymmetry_verticalEndpoint (a b : ℝ) :
    closingSymmetry (planeVector b (1 + a)) = planeVector (-(1 + a)) (-b) := by
  ext i
  fin_cases i <;> simp [closingSymmetry, coordinateSwap, planeVector]

/-- Under the closing involution, the first jump for swapped parameters is
exactly the closing jump for the original parameters. -/
theorem closingSymmetry_mem_sectorOneTwoJump_iff {a b : ℝ} (ha : 0 < a)
    (x : Plane) :
    closingSymmetry x ∈ sectorOneTwoJump b a ↔ x ∈ sectorThreeOneJump a b := by
  unfold sectorOneTwoJump sectorThreeOneJump
  rw [sectorTwoBoundaryPoint_pi_div_two ha, sectorThreeBoundaryPoint_pi ha]
  constructor
  · rintro ⟨r, q, hr, hq, hrq, heq⟩
    refine ⟨q, r, hq, hr, by linarith, ?_⟩
    have heq' := congrArg closingSymmetry heq
    simp only [closingSymmetry_add, closingSymmetry_smul,
      closingSymmetry_sectorOneVertex, closingSymmetry_verticalEndpoint,
      closingSymmetry_involutive] at heq'
    calc
      q • planeVector (-(1 + a)) (-b) + r • -sectorOneVertex a b =
          r • -sectorOneVertex a b + q • planeVector (-(1 + a)) (-b) := by
            rw [add_comm]
      _ = x := heq'
  · rintro ⟨r, q, hr, hq, hrq, heq⟩
    refine ⟨q, r, hq, hr, by linarith, ?_⟩
    have heq' := congrArg closingSymmetry heq
    simp only [closingSymmetry_add, closingSymmetry_smul] at heq'
    have hfirst : closingSymmetry (-sectorOneVertex a b) = sectorOneVertex b a := by
      ext i
      fin_cases i <;>
        simp [closingSymmetry, coordinateSwap, sectorOneVertex, planeVector]
    have hsecond : closingSymmetry (planeVector (-(1 + a)) (-b)) =
        planeVector b (1 + a) := by
      ext i
      fin_cases i <;> simp [closingSymmetry, coordinateSwap, planeVector]
    rw [hsecond, hfirst] at heq'
    calc
      q • sectorOneVertex b a + r • planeVector b (1 + a) =
          r • planeVector b (1 + a) + q • sectorOneVertex b a := by
            rw [add_comm]
      _ = closingSymmetry x := heq'

/-! ## Exact closing exposed face -/

/-- The closing upper-half derivative jump is the complete exposed face at
the negative first-coordinate normal. -/
theorem exposedFace_neg_planeE1_eq_sectorThreeOneJump {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    {x | x ∈ normalizedLpSumTwo a b ∧
        inner ℝ x (-planeE1) = normalizedFireySupportVec a b (-planeE1)} =
      sectorThreeOneJump a b := by
  ext x
  constructor
  · rintro ⟨hxbody, hsupport⟩
    have hybody : closingSymmetry x ∈ normalizedLpSumTwo b a :=
      (closingSymmetry_mem_normalizedLpSumTwo_iff a b x).2 hxbody
    have hysupport : inner ℝ (closingSymmetry x) planeE2 =
        normalizedFireySupportVec b a planeE2 := by
      rw [inner_closingSymmetry_planeE2,
        normalizedFireySupportVec_closingDirection]
      exact hsupport
    have hyface : closingSymmetry x ∈ sectorOneTwoJump b a := by
      have : closingSymmetry x ∈
          {y | y ∈ normalizedLpSumTwo b a ∧
            inner ℝ y planeE2 = normalizedFireySupportVec b a planeE2} :=
        ⟨hybody, hysupport⟩
      rwa [exposedFace_planeE2_eq_sectorOneTwoJump hb ha] at this
    exact (closingSymmetry_mem_sectorOneTwoJump_iff ha x).mp hyface
  · intro hxjump
    have hyjump : closingSymmetry x ∈ sectorOneTwoJump b a :=
      (closingSymmetry_mem_sectorOneTwoJump_iff ha x).mpr hxjump
    have hyface : closingSymmetry x ∈
        {y | y ∈ normalizedLpSumTwo b a ∧
          inner ℝ y planeE2 = normalizedFireySupportVec b a planeE2} := by
      rwa [exposedFace_planeE2_eq_sectorOneTwoJump hb ha]
    refine ⟨(closingSymmetry_mem_normalizedLpSumTwo_iff a b x).mp hyface.1, ?_⟩
    rw [← inner_closingSymmetry_planeE2,
      ← normalizedFireySupportVec_closingDirection]
    exact hyface.2

#print axioms normalizedFireySupportVecSq_coordinateSwap
#print axioms coordinateSwap_mem_normalizedLpSumTwo_iff
#print axioms closingSymmetry_mem_sectorOneTwoJump_iff
#print axioms exposedFace_neg_planeE1_eq_sectorThreeOneJump

end L2Hexagon
