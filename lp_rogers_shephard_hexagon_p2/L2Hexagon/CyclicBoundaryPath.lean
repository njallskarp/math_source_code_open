import L2Hexagon.FrontierAtlas
import Mathlib.Analysis.Convex.PathConnected

/-!
# A genuine cyclic path for the normalized halfspace body

Let `C(a,b)` be the exact halfspace-defined normalized `p=2` body.  Informally,
for `a,b>0` the five consecutive upper-normal pieces

1. the first jump segment,
2. the Sector II canonical arc,
3. the middle jump segment,
4. the Sector III canonical arc, and
5. the closing jump segment

form a continuous path from the fixed Sector I vertex to its negative.  Its
pointwise negative is a return path, so their concatenation is a closed path.
The main theorem below proves that the range of this literal bundled
`Path` is exactly `frontier C(a,b)`.

This is a topological boundary object, not an area definition.  Injectivity
modulo the common endpoint, positive orientation, the Green/Jordan bridge,
and the affine normal form remain separate downstream obligations.
-/

open Real Set

namespace L2Hexagon

noncomputable section

/-! ## Continuous canonical curved pieces -/

/-- The actual Cartesian point on the Sector II canonical support arc. -/
def sectorTwoBoundaryPoint (a b θ : ℝ) : Plane :=
  planeVector (sectorTwoBoundaryX a b θ) (sectorTwoBoundaryY a b θ)

/-- The actual Cartesian point on the Sector III canonical support arc. -/
def sectorThreeBoundaryPoint (a b θ : ℝ) : Plane :=
  planeVector (sectorThreeBoundaryX a b θ) (sectorThreeBoundaryY a b θ)

/-- The Sector II canonical point depends continuously on its normal angle. -/
theorem continuous_sectorTwoBoundaryPoint {a b : ℝ} (hb : 0 < b) :
    Continuous (sectorTwoBoundaryPoint a b) := by
  change Continuous (fun θ =>
    planeVector (sectorTwoBoundaryX a b θ) (sectorTwoBoundaryY a b θ))
  unfold planeVector
  apply (PiLp.continuous_toLp 2 (fun _ : Fin 2 => ℝ)).comp
  apply continuous_pi
  intro i
  fin_cases i
  · exact continuous_iff_continuousAt.2 fun θ =>
      (hasDerivAt_sectorTwoBoundaryX hb θ).continuousAt
  · exact continuous_iff_continuousAt.2 fun θ =>
      (hasDerivAt_sectorTwoBoundaryY hb θ).continuousAt

/-- The Sector III canonical point depends continuously on its normal angle. -/
theorem continuous_sectorThreeBoundaryPoint {a b : ℝ} (ha : 0 < a) :
    Continuous (sectorThreeBoundaryPoint a b) := by
  change Continuous (fun θ =>
    planeVector (sectorThreeBoundaryX a b θ) (sectorThreeBoundaryY a b θ))
  unfold planeVector
  apply (PiLp.continuous_toLp 2 (fun _ : Fin 2 => ℝ)).comp
  apply continuous_pi
  intro i
  fin_cases i
  · exact continuous_iff_continuousAt.2 fun θ =>
      (hasDerivAt_sectorThreeBoundaryX ha θ).continuousAt
  · exact continuous_iff_continuousAt.2 fun θ =>
      (hasDerivAt_sectorThreeBoundaryY ha θ).continuousAt

/-- Sector II, parametrized continuously from its vertical endpoint to its
middle-transition endpoint. -/
def sectorTwoArcPath (a b : ℝ) (hb : 0 < b) :
    Path (sectorTwoBoundaryPoint a b (π / 2))
      (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a))) :=
  (Path.segment (π / 2) (π / 2 + arctan (b / a))).map
    (continuous_sectorTwoBoundaryPoint hb)

/-- Sector III, parametrized continuously from its middle-transition endpoint
to its endpoint at angle `π`. -/
def sectorThreeArcPath (a b : ℝ) (ha : 0 < a) :
    Path (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a)))
      (sectorThreeBoundaryPoint a b π) :=
  (Path.segment (π / 2 + arctan (b / a)) π).map
    (continuous_sectorThreeBoundaryPoint ha)

theorem range_sectorTwoArcPath {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Set.range (sectorTwoArcPath a b hb) =
      sectorTwoBoundaryPoint a b ''
        Icc (π / 2) (π / 2 + arctan (b / a)) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφpos : 0 < arctan (b / a) := by
    simpa [generatorAngle] using hφ.1
  unfold sectorTwoArcPath
  rw [Path.map_coe, Set.range_comp, Path.range_segment,
    segment_eq_Icc (by linarith [hφpos])]

theorem range_sectorThreeArcPath {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Set.range (sectorThreeArcPath a b ha) =
      sectorThreeBoundaryPoint a b ''
        Icc (π / 2 + arctan (b / a)) π := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφlt : arctan (b / a) < π / 2 := by
    simpa [generatorAngle] using hφ.2
  unfold sectorThreeArcPath
  rw [Path.map_coe, Set.range_comp, Path.range_segment,
    segment_eq_Icc (by linarith [hφlt])]

/-! ## Upper chain and closed cyclic path -/

/-- The five-piece upper-normal chain, from the fixed vertex to its negative. -/
def normalizedUpperBoundaryPath (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    Path (sectorOneVertex a b) (-sectorOneVertex a b) :=
  ((((Path.segment (sectorOneVertex a b)
          (sectorTwoBoundaryPoint a b (π / 2))).trans
        (sectorTwoArcPath a b hb)).trans
      (Path.segment
        (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
        (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a))))).trans
    (sectorThreeArcPath a b ha)).trans
  (Path.segment (sectorThreeBoundaryPoint a b π) (-sectorOneVertex a b))

/-- The closed boundary path: traverse the upper-normal chain and then its
pointwise negative. -/
def normalizedCyclicBoundaryPath (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    Path (sectorOneVertex a b) (sectorOneVertex a b) :=
  let upper := normalizedUpperBoundaryPath a b ha hb
  upper.trans ((upper.map (f := fun x : Plane => -x) continuous_neg).cast rfl
    (by simp only [neg_neg]))

/-- A closed-image version of the positive-normal half of the canonical
boundary.  Endpoints of curved pieces are deliberately retained. -/
def normalizedClosedUpperBoundary (a b : ℝ) : Set Plane :=
  sectorOneTwoJump a b ∪
    sectorTwoBoundaryPoint a b ''
      Icc (π / 2) (π / 2 + arctan (b / a)) ∪
    sectorTwoThreeJump a b ∪
    sectorThreeBoundaryPoint a b ''
      Icc (π / 2 + arctan (b / a)) π ∪
    sectorThreeOneJump a b

/-- The five bundled pieces have exactly the expected closed upper range. -/
theorem range_normalizedUpperBoundaryPath {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Set.range (normalizedUpperBoundaryPath a b ha hb) =
      normalizedClosedUpperBoundary a b := by
  rw [normalizedUpperBoundaryPath, Path.trans_range, Path.trans_range,
    Path.trans_range, Path.trans_range, Path.range_segment,
    range_sectorTwoArcPath ha hb, Path.range_segment,
    range_sectorThreeArcPath ha hb, Path.range_segment]
  rfl

/-! ## Comparison with the checked frontier atlas -/

theorem normalizedClosedUpperBoundary_subset_upperNormalBoundary {a b : ℝ}
    (_ha : 0 < a) (_hb : 0 < b) :
    normalizedClosedUpperBoundary a b ⊆ normalizedUpperNormalBoundary a b := by
  intro x hx
  simp only [normalizedClosedUpperBoundary, Set.mem_union] at hx
  rcases hx with (((hx12 | hx2) | hx23) | hx3) | hx31
  · exact Or.inl (Or.inl (Or.inl (Or.inl (Or.inr hx12))))
  · rcases hx2 with ⟨θ, hθ, rfl⟩
    rcases lt_trichotomy θ (π / 2) with hlt | heq | hgt
    · exact (not_lt_of_ge hθ.1 hlt).elim
    · subst θ
      apply Or.inl
      apply Or.inl
      apply Or.inl
      apply Or.inl
      apply Or.inr
      unfold sectorOneTwoJump sectorTwoBoundaryPoint
      exact right_mem_segment ℝ (sectorOneVertex a b)
        (planeVector (sectorTwoBoundaryX a b (π / 2))
          (sectorTwoBoundaryY a b (π / 2)))
    · rcases lt_trichotomy θ (π / 2 + arctan (b / a)) with hmid | heq | hgt'
      · exact Or.inl (Or.inl (Or.inl (Or.inr
          ⟨θ, ⟨hgt, hmid⟩, rfl⟩)))
      · subst θ
        apply Or.inl
        apply Or.inl
        apply Or.inr
        unfold sectorTwoThreeJump sectorTwoBoundaryPoint
        change planeVector
            (sectorTwoBoundaryX a b (π / 2 + arctan (b / a)))
            (sectorTwoBoundaryY a b (π / 2 + arctan (b / a))) ∈
          segment ℝ
            (planeVector
              (sectorTwoBoundaryX a b (π / 2 + arctan (b / a)))
              (sectorTwoBoundaryY a b (π / 2 + arctan (b / a))))
            (planeVector
              (sectorThreeBoundaryX a b (π / 2 + arctan (b / a)))
              (sectorThreeBoundaryY a b (π / 2 + arctan (b / a))))
        exact left_mem_segment ℝ _ _
      · exact (not_lt_of_ge hθ.2 hgt').elim
  · exact Or.inl (Or.inl (Or.inr hx23))
  · rcases hx3 with ⟨θ, hθ, rfl⟩
    rcases lt_trichotomy θ (π / 2 + arctan (b / a)) with hlt | heq | hgt
    · exact (not_lt_of_ge hθ.1 hlt).elim
    · subst θ
      apply Or.inl
      apply Or.inl
      apply Or.inr
      unfold sectorTwoThreeJump sectorThreeBoundaryPoint
      change planeVector
          (sectorThreeBoundaryX a b (π / 2 + arctan (b / a)))
          (sectorThreeBoundaryY a b (π / 2 + arctan (b / a))) ∈
        segment ℝ
          (planeVector
            (sectorTwoBoundaryX a b (π / 2 + arctan (b / a)))
            (sectorTwoBoundaryY a b (π / 2 + arctan (b / a))))
          (planeVector
            (sectorThreeBoundaryX a b (π / 2 + arctan (b / a)))
            (sectorThreeBoundaryY a b (π / 2 + arctan (b / a))))
      exact right_mem_segment ℝ _ _
    · rcases lt_trichotomy θ π with hmid | heq | hgt'
      · exact Or.inl (Or.inr ⟨θ, ⟨hgt, hmid⟩, rfl⟩)
      · subst θ
        apply Or.inr
        unfold sectorThreeOneJump sectorThreeBoundaryPoint
        exact left_mem_segment ℝ
          (planeVector (sectorThreeBoundaryX a b π) (sectorThreeBoundaryY a b π))
          (-sectorOneVertex a b)
      · exact (not_lt_of_ge hθ.2 hgt').elim
  · exact Or.inr hx31

theorem normalizedUpperNormalBoundary_subset_closed_union_neg {a b : ℝ}
    (_ha : 0 < a) (_hb : 0 < b) :
    normalizedUpperNormalBoundary a b ⊆
      normalizedClosedUpperBoundary a b ∪ -normalizedClosedUpperBoundary a b := by
  intro x hx
  simp only [normalizedUpperNormalBoundary, Set.mem_union] at hx
  rcases hx with ((((((hxneg31 | hxv) | hx12) | hx2) | hx23) | hx3) | hx31)
  · right
    rw [Set.mem_neg] at hxneg31 ⊢
    exact Or.inr hxneg31
  · left
    rw [Set.mem_singleton_iff] at hxv
    subst x
    apply Or.inl
    apply Or.inl
    apply Or.inl
    apply Or.inl
    unfold sectorOneTwoJump
    exact left_mem_segment ℝ (sectorOneVertex a b)
      (planeVector (sectorTwoBoundaryX a b (π / 2))
        (sectorTwoBoundaryY a b (π / 2)))
  · left
    exact Or.inl (Or.inl (Or.inl (Or.inl hx12)))
  · left
    rcases hx2 with ⟨θ, hθ, rfl⟩
    exact Or.inl (Or.inl (Or.inl (Or.inr
      ⟨θ, ⟨hθ.1.le, hθ.2.le⟩, rfl⟩)))
  · left
    exact Or.inl (Or.inl (Or.inr hx23))
  · left
    rcases hx3 with ⟨θ, hθ, rfl⟩
    exact Or.inl (Or.inr ⟨θ, ⟨hθ.1.le, hθ.2.le⟩, rfl⟩)
  · left
    exact Or.inr hx31

/-- The closed cyclic path has exactly the already classified topological
frontier as its range. -/
theorem range_normalizedCyclicBoundaryPath {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Set.range (normalizedCyclicBoundaryPath a b ha hb) =
      frontier (normalizedLpSumTwo a b) := by
  let upper := normalizedUpperBoundaryPath a b ha hb
  have hrangeUpper : Set.range upper = normalizedClosedUpperBoundary a b :=
    range_normalizedUpperBoundaryPath ha hb
  have hrangeNeg : Set.range ((upper.map (f := fun x : Plane => -x) continuous_neg).cast
      (x' := -sectorOneVertex a b) (y' := sectorOneVertex a b) rfl
      (by simp only [neg_neg])) =
      -normalizedClosedUpperBoundary a b := by
    rw [Path.cast_coe, Path.map_coe, Set.range_comp, hrangeUpper]
    ext x
    simp [Set.mem_neg]
  rw [normalizedCyclicBoundaryPath, Path.trans_range, hrangeUpper, hrangeNeg,
    frontier_normalizedLpSumTwo_eq_upperNormalBoundary_union_neg ha hb]
  apply Set.Subset.antisymm
  · intro x hx
    rcases hx with hx | hx
    · exact Or.inl (normalizedClosedUpperBoundary_subset_upperNormalBoundary ha hb hx)
    · right
      rw [Set.mem_neg] at hx ⊢
      exact normalizedClosedUpperBoundary_subset_upperNormalBoundary ha hb hx
  · intro x hx
    rcases hx with hx | hx
    · exact normalizedUpperNormalBoundary_subset_closed_union_neg ha hb hx
    · rw [Set.mem_neg] at hx
      have h := normalizedUpperNormalBoundary_subset_closed_union_neg ha hb hx
      rcases h with h | h
      · right
        rw [Set.mem_neg]
        exact h
      · left
        rw [Set.mem_neg] at h
        simpa using h

#print axioms continuous_sectorTwoBoundaryPoint
#print axioms continuous_sectorThreeBoundaryPoint
#print axioms range_normalizedUpperBoundaryPath
#print axioms range_normalizedCyclicBoundaryPath

end

end L2Hexagon
