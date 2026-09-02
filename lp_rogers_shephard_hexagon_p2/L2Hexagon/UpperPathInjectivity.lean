import L2Hexagon.SimplePathOrientation

/-!
# Injectivity under path concatenation and endpoint coordinates

This file separates a reusable topological lemma from the convex-geometric
range-intersection problem.  Two injective paths whose ranges meet only at
their common endpoint have injective concatenation.  Exact Cartesian endpoint
gaps and strict monotonicity of the curved first coordinates then classify all
cross-piece intersections in the five-piece upper-normal chain.  Consequently
the complete upper boundary path is injective.

Injectivity modulo endpoints of the closed cyclic path remains a separate
theorem: it additionally requires controlling intersections between the upper
chain and its pointwise negative.
-/

open Real Set

namespace L2Hexagon

noncomputable section

/-! ## A reusable concatenation theorem -/

/-- If two injective paths meet only at their common endpoint, their standard
concatenation is injective. -/
theorem Path.injective_trans_of_range_inter_subset {X : Type*} [TopologicalSpace X]
    {x y z : X} (γ : Path x y) (δ : Path y z)
    (hγ : Function.Injective γ) (hδ : Function.Injective δ)
    (hinter : Set.range γ ∩ Set.range δ ⊆ {y}) :
    Function.Injective (γ.trans δ) := by
  intro s t hst
  rw [Path.trans_apply, Path.trans_apply] at hst
  split_ifs at hst with hs ht
  · have hp := hγ hst
    apply Subtype.ext
    have hp' := congrArg Subtype.val hp
    dsimp only at hp'
    linarith
  · let ps : unitInterval :=
      ⟨2 * (s : ℝ), by constructor <;> linarith [s.2.1, s.2.2]⟩
    let qt : unitInterval :=
      ⟨2 * (t : ℝ) - 1, by
        constructor <;> linarith [t.2.1, t.2.2, not_le.1 ht]⟩
    have hmeet : γ ps ∈ Set.range γ ∩ Set.range δ := by
      refine ⟨Set.mem_range_self ps, ?_⟩
      exact ⟨qt, by simpa only [ps, qt] using hst.symm⟩
    have hy : γ ps = y := by
      simpa only [Set.mem_singleton_iff] using hinter hmeet
    have hps : ps = (1 : unitInterval) := by
      apply hγ
      simpa using hy
    have hqt : qt = (0 : unitInterval) := by
      apply hδ
      have : δ qt = y := by
        have hqp : δ qt = γ ps := by
          simpa only [ps, qt] using hst.symm
        exact hqp.trans hy
      simpa using this
    have hps' := congrArg Subtype.val hps
    have hqt' := congrArg Subtype.val hqt
    apply Subtype.ext
    change 2 * (s : ℝ) = 1 at hps'
    change 2 * (t : ℝ) - 1 = 0 at hqt'
    linarith
  · let pt : unitInterval :=
      ⟨2 * (t : ℝ), by constructor <;> linarith [t.2.1, t.2.2]⟩
    let qs : unitInterval :=
      ⟨2 * (s : ℝ) - 1, by
        constructor <;> linarith [s.2.1, s.2.2, not_le.1 hs]⟩
    have hmeet : γ pt ∈ Set.range γ ∩ Set.range δ := by
      refine ⟨Set.mem_range_self pt, ?_⟩
      exact ⟨qs, by simpa only [pt, qs] using hst⟩
    have hy : γ pt = y := by
      simpa only [Set.mem_singleton_iff] using hinter hmeet
    have hpt : pt = (1 : unitInterval) := by
      apply hγ
      simpa using hy
    have hqs : qs = (0 : unitInterval) := by
      apply hδ
      have : δ qs = y := by
        have hqp : δ qs = γ pt := by
          simpa only [pt, qs] using hst
        exact hqp.trans hy
      simpa using this
    have hpt' := congrArg Subtype.val hpt
    have hqs' := congrArg Subtype.val hqs
    apply Subtype.ext
    change 2 * (t : ℝ) = 1 at hpt'
    change 2 * (s : ℝ) - 1 = 0 at hqs'
    linarith
  · have hp := hδ hst
    apply Subtype.ext
    have hp' := congrArg Subtype.val hp
    dsimp only at hp'
    linarith

/-! ## Exact endpoints of the curved pieces -/

/-- The Sector II curved arc begins at the right endpoint of the first jump. -/
theorem sectorTwoBoundaryPoint_pi_div_two' {a b : ℝ} (hb : 0 < b) :
    sectorTwoBoundaryPoint a b (π / 2) = planeVector a (1 + b) := by
  exact sectorTwoBoundaryPoint_pi_div_two hb

/-! ## Embedded jump pieces -/

/-- The endpoints of the first upper jump are distinct. -/
theorem sectorOneVertex_ne_sectorTwoBoundaryPoint_pi_div_two {a b : ℝ}
    (hb : 0 < b) :
    sectorOneVertex a b ≠ sectorTwoBoundaryPoint a b (π / 2) := by
  rw [sectorTwoBoundaryPoint_pi_div_two' hb]
  intro h
  have h0 := congrArg (fun x : Plane => x 0) h
  simp [sectorOneVertex, planeVector] at h0

/-- The endpoints of the middle jump are distinct. -/
theorem middleSectorTwoEndpoint_ne_middleSectorThreeEndpoint {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    middleSectorTwoEndpoint a b ≠ middleSectorThreeEndpoint a b := by
  intro h
  have htangent := congrArg (fun x : Plane => inner ℝ x (middleTangent a b)) h
  rw [middleSectorTwoEndpoint_tangent_pairing ha,
    middleSectorThreeEndpoint_tangent_pairing ha hb] at htangent
  have hs := middleRadius_pos (b := b) ha
  nlinarith

/-- The middle jump travels strictly to the left in Cartesian coordinates. -/
theorem middleSectorThreeEndpoint_firstCoord_lt_two {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    (middleSectorThreeEndpoint a b) 0 < (middleSectorTwoEndpoint a b) 0 := by
  have hn2 := middleSectorTwoEndpoint_normal_pairing ha hb
  have hn3 := middleSectorThreeEndpoint_normal_pairing ha hb
  have ht2 := middleSectorTwoEndpoint_tangent_pairing (b := b) ha
  have ht3 := middleSectorThreeEndpoint_tangent_pairing ha hb
  rw [PiLp.inner_apply] at hn2 hn3 ht2 ht3
  rw [Fin.sum_univ_two] at hn2 hn3 ht2 ht3
  simp [middleNormal, middleTangent, planeVector] at hn2 hn3 ht2 ht3
  have hscaled :
      middleRadiusSq a b *
          ((middleSectorTwoEndpoint a b) 0 - (middleSectorThreeEndpoint a b) 0) =
        a * ((a + b) * middleRadius a b) := by
    unfold middleRadiusSq
    linear_combination a * (ht2 - ht3) - b * (hn2 - hn3)
  have hR := middleRadiusSq_pos (b := b) ha
  have hs := middleRadius_pos (b := b) ha
  have hab : 0 < a + b := add_pos ha hb
  nlinarith [mul_pos hab hs]

/-- The endpoints of the closing upper jump are distinct. -/
theorem sectorThreeBoundaryPoint_pi_ne_neg_sectorOneVertex {a b : ℝ}
    (ha : 0 < a) :
    sectorThreeBoundaryPoint a b π ≠ -sectorOneVertex a b := by
  unfold sectorThreeBoundaryPoint
  rw [sectorThreeBoundaryPoint_pi ha]
  intro h
  have h1 := congrArg (fun x : Plane => x 1) h
  simp [sectorOneVertex, planeVector] at h1

/-- The first straight jump path is injective. -/
theorem injective_sectorOneTwoJumpPath {a b : ℝ} (hb : 0 < b) :
    Function.Injective
      (Path.segment (sectorOneVertex a b)
        (sectorTwoBoundaryPoint a b (π / 2))) :=
  Path.segment_injective_of_ne
    (sectorOneVertex_ne_sectorTwoBoundaryPoint_pi_div_two hb)

/-- The middle straight jump path is injective. -/
theorem injective_sectorTwoThreeJumpPath {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Function.Injective
      (Path.segment
        (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
        (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a)))) := by
  apply Path.segment_injective_of_ne
  simpa [sectorTwoBoundaryPoint, sectorThreeBoundaryPoint,
    middleSectorTwoEndpoint, middleSectorThreeEndpoint] using
      middleSectorTwoEndpoint_ne_middleSectorThreeEndpoint ha hb

/-- The closing straight jump path is injective. -/
theorem injective_sectorThreeOneJumpPath {a b : ℝ} (ha : 0 < a) :
    Function.Injective
      (Path.segment (sectorThreeBoundaryPoint a b π) (-sectorOneVertex a b)) :=
  Path.segment_injective_of_ne
    (sectorThreeBoundaryPoint_pi_ne_neg_sectorOneVertex ha)

/-! ## The first exact cross-piece intersection -/

/-- The first jump and the Sector II curved arc meet only at their common
endpoint.  This is the first nontrivial cross-piece fact required by recursive
use of `Path.injective_trans_of_range_inter_subset`. -/
theorem range_sectorOneTwoJumpPath_inter_sectorTwoArcPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range
        (Path.segment (sectorOneVertex a b)
          (sectorTwoBoundaryPoint a b (π / 2))) ∩
      Set.range (sectorTwoArcPath a b hb) =
        {sectorTwoBoundaryPoint a b (π / 2)} := by
  ext x
  constructor
  · rintro ⟨hxJump, hxArc⟩
    rw [Path.range_segment] at hxJump
    rw [range_sectorTwoArcPath ha hb] at hxArc
    rcases hxArc with ⟨θ, hθ, rfl⟩
    rcases hxJump with ⟨c, d, hc, hd, hcd, hcombo⟩
    have hcoord := congrArg (fun p : Plane => p 0) hcombo
    rw [sectorTwoBoundaryPoint_pi_div_two' hb] at hcoord
    simp [sectorOneVertex, sectorTwoBoundaryPoint, planeVector] at hcoord
    have hge : a ≤ sectorTwoBoundaryX a b θ := by
      nlinarith
    have hθeq : θ = π / 2 := by
      apply le_antisymm
      · by_contra hnot
        have hltθ : π / 2 < θ := lt_of_not_ge hnot
        have hstrict := strictAntiOn_sectorTwoBoundaryX ha hb
          (show π / 2 ∈ Icc (π / 2) (π / 2 + arctan (b / a)) by
            constructor
            · exact le_rfl
            · have hφ := generatorAngle_mem_Ioo ha hb
              have : 0 < arctan (b / a) := by
                simpa [generatorAngle] using hφ.1
              linarith)
          hθ hltθ
        have hstart : sectorTwoBoundaryX a b (π / 2) = a := by
          have hp := sectorTwoBoundaryPoint_pi_div_two' (a := a) hb
          have hp0 := congrArg (fun p : Plane => p 0) hp
          simpa [sectorTwoBoundaryPoint, planeVector] using hp0
        rw [hstart] at hstrict
        linarith
      · exact hθ.1
    subst θ
    simp
  · intro hx
    rw [Set.mem_singleton_iff] at hx
    subst x
    constructor
    · rw [Path.range_segment]
      exact right_mem_segment ℝ _ _
    · rw [range_sectorTwoArcPath ha hb]
      exact ⟨π / 2, by
        constructor
        · exact le_rfl
        · have hφ := generatorAngle_mem_Ioo ha hb
          have : 0 < arctan (b / a) := by
            simpa [generatorAngle] using hφ.1
          linarith, rfl⟩

/-- The concatenation of the first jump and Sector II arc is injective. -/
theorem injective_sectorOneTwoJump_trans_sectorTwoArc {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Function.Injective
      ((Path.segment (sectorOneVertex a b)
        (sectorTwoBoundaryPoint a b (π / 2))).trans
          (sectorTwoArcPath a b hb)) := by
  apply Path.injective_trans_of_range_inter_subset
    _ _ (injective_sectorOneTwoJumpPath hb) (injective_sectorTwoArcPath ha hb)
  rw [range_sectorOneTwoJumpPath_inter_sectorTwoArcPath ha hb]

/-- The Sector II arc and the middle jump meet only at their common endpoint. -/
theorem range_sectorTwoArcPath_inter_sectorTwoThreeJumpPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range (sectorTwoArcPath a b hb) ∩
      Set.range
        (Path.segment
          (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
          (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a)))) =
      {sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a))} := by
  let θm := π / 2 + arctan (b / a)
  have hφ := generatorAngle_mem_Ioo ha hb
  have hθmMem : θm ∈ Icc (π / 2) θm := by
    constructor
    · have : 0 < arctan (b / a) := by
        simpa [generatorAngle] using hφ.1
      dsimp only [θm]
      linarith
    · exact le_rfl
  have hxOrder :
      sectorThreeBoundaryX a b θm < sectorTwoBoundaryX a b θm := by
    simpa [θm, middleSectorTwoEndpoint, middleSectorThreeEndpoint,
      planeVector] using middleSectorThreeEndpoint_firstCoord_lt_two ha hb
  dsimp only [θm] at hxOrder
  ext x
  constructor
  · rintro ⟨hxArc, hxJump⟩
    rw [range_sectorTwoArcPath ha hb] at hxArc
    rw [Path.range_segment] at hxJump
    rcases hxArc with ⟨θ, hθ, rfl⟩
    rcases hxJump with ⟨c, d, hc, hd, hcd, hcombo⟩
    have hcoord := congrArg (fun p : Plane => p 0) hcombo
    simp [sectorTwoBoundaryPoint, sectorThreeBoundaryPoint, planeVector] at hcoord
    have hle : sectorTwoBoundaryX a b θ ≤ sectorTwoBoundaryX a b θm := by
      dsimp only [θm]
      calc
        sectorTwoBoundaryX a b θ =
            c * sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) +
              d * sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) :=
          hcoord.symm
        _ ≤ c * sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) +
              d * sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) :=
          by
            have hdBound := mul_le_mul_of_nonneg_left hxOrder.le hd
            linarith only [hdBound]
        _ = sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) := by
          rw [← add_mul, hcd, one_mul]
    have hθeq : θ = θm := by
      apply le_antisymm
      · simpa only [θm] using hθ.2
      · by_contra hnot
        have hltθ : θ < θm := lt_of_not_ge hnot
        have hstrict := strictAntiOn_sectorTwoBoundaryX ha hb hθ
          (by simpa only [θm] using hθmMem) hltθ
        linarith
    subst θ
    simp [θm]
  · intro hx
    rw [Set.mem_singleton_iff] at hx
    subst x
    constructor
    · rw [range_sectorTwoArcPath ha hb]
      exact ⟨θm, by simpa only [θm] using hθmMem, by simp [θm]⟩
    · rw [Path.range_segment]
      exact left_mem_segment ℝ _ _

/-- The Sector II middle endpoint lies strictly left of its vertical endpoint. -/
theorem sectorTwoBoundaryX_middle_lt_a {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) < a := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφpos : 0 < arctan (b / a) := by
    simpa [generatorAngle] using hφ.1
  have hstrict := strictAntiOn_sectorTwoBoundaryX ha hb
    (show π / 2 ∈ Icc (π / 2) (π / 2 + arctan (b / a)) by
      constructor <;> linarith)
    (show π / 2 + arctan (b / a) ∈
        Icc (π / 2) (π / 2 + arctan (b / a)) by
      constructor <;> linarith)
    (by linarith)
  have hstart : sectorTwoBoundaryX a b (π / 2) = a := by
    have hp := sectorTwoBoundaryPoint_pi_div_two' (a := a) hb
    have hp0 := congrArg (fun p : Plane => p 0) hp
    simpa [sectorTwoBoundaryPoint, planeVector] using hp0
  rwa [hstart] at hstrict

/-- The first and middle jump paths have disjoint ranges. -/
theorem range_sectorOneTwoJumpPath_inter_sectorTwoThreeJumpPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range
        (Path.segment (sectorOneVertex a b)
          (sectorTwoBoundaryPoint a b (π / 2))) ∩
      Set.range
        (Path.segment
          (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
          (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a)))) =
      ∅ := by
  have hxOrder :
      sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) <
        sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) := by
    simpa [middleSectorTwoEndpoint, middleSectorThreeEndpoint, planeVector] using
      middleSectorThreeEndpoint_firstCoord_lt_two ha hb
  ext x
  constructor
  · rintro ⟨hxFirst, hxMiddle⟩
    rw [Path.range_segment] at hxFirst hxMiddle
    rcases hxFirst with ⟨c, d, hc, hd, hcd, hFirst⟩
    rcases hxMiddle with ⟨r, s, hr, hs, hrs, hMiddle⟩
    have hFirstCoord := congrArg (fun p : Plane => p 0) hFirst
    rw [sectorTwoBoundaryPoint_pi_div_two' hb] at hFirstCoord
    simp [sectorOneVertex, planeVector] at hFirstCoord
    have hLower : a ≤ x 0 := by nlinarith
    have hMiddleCoord := congrArg (fun p : Plane => p 0) hMiddle
    simp [sectorTwoBoundaryPoint, sectorThreeBoundaryPoint, planeVector] at hMiddleCoord
    have hsBound := mul_le_mul_of_nonneg_left hxOrder.le hs
    have hUpper : x 0 ≤
        sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) := by
      calc
        x 0 = r * sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) +
            s * sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) :=
          hMiddleCoord.symm
        _ ≤ r * sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) +
            s * sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) := by
          linarith only [hsBound]
        _ = sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) := by
          rw [← add_mul, hrs, one_mul]
    have hMiddleLt := sectorTwoBoundaryX_middle_lt_a ha hb
    simp only [Set.mem_empty_iff_false]
    linarith
  · simp

/-- The first three consecutive upper pieces form an injective path. -/
theorem injective_firstThreeUpperPieces {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Function.Injective
      (((Path.segment (sectorOneVertex a b)
        (sectorTwoBoundaryPoint a b (π / 2))).trans
          (sectorTwoArcPath a b hb)).trans
        (Path.segment
          (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
          (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a))))) := by
  apply Path.injective_trans_of_range_inter_subset _ _
    (injective_sectorOneTwoJump_trans_sectorTwoArc ha hb)
    (injective_sectorTwoThreeJumpPath ha hb)
  rw [Path.trans_range]
  intro x hx
  rcases hx with ⟨hxFirst | hxArc, hxMiddle⟩
  · have hEmpty : x ∈ (∅ : Set Plane) := by
      rw [← range_sectorOneTwoJumpPath_inter_sectorTwoThreeJumpPath ha hb]
      exact ⟨hxFirst, hxMiddle⟩
    exact hEmpty.elim
  · have hCommon : x ∈
        ({sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a))} : Set Plane) := by
      rw [← range_sectorTwoArcPath_inter_sectorTwoThreeJumpPath ha hb]
      exact ⟨hxArc, hxMiddle⟩
    exact hCommon

/-! ## Completing the upper five-piece path -/

/-- Every point of the Sector II arc lies weakly to the right of its middle
endpoint. -/
theorem sectorTwoBoundaryX_middle_le_of_mem_arc {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2) (π / 2 + arctan (b / a))) :
    sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) ≤
      sectorTwoBoundaryX a b θ := by
  exact (strictAntiOn_sectorTwoBoundaryX ha hb).antitoneOn hθ
    ⟨by
      have hφ := generatorAngle_mem_Ioo ha hb
      have : 0 < arctan (b / a) := by
        simpa [generatorAngle] using hφ.1
      linarith, le_rfl⟩ hθ.2

/-- Every point of the Sector III arc lies weakly to the left of its middle
endpoint. -/
theorem sectorThreeBoundaryX_le_middle_of_mem_arc {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2 + arctan (b / a)) π) :
    sectorThreeBoundaryX a b θ ≤
      sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) := by
  exact (strictAntiOn_sectorThreeBoundaryX ha hb).antitoneOn
    ⟨le_rfl, by
      have hφ := generatorAngle_mem_Ioo ha hb
      have : arctan (b / a) < π / 2 := by
        simpa [generatorAngle] using hφ.2
      linarith⟩ hθ hθ.1

/-- The Sector III middle endpoint lies strictly to the right of its endpoint
at angle `π`. -/
theorem sectorThreeBoundaryX_pi_lt_middle {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    sectorThreeBoundaryX a b π <
      sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  apply strictAntiOn_sectorThreeBoundaryX ha hb
  · exact ⟨le_rfl, by
      have : arctan (b / a) < π / 2 := by
        simpa [generatorAngle] using hφ.2
      linarith⟩
  · exact ⟨by
      have : arctan (b / a) < π / 2 := by
        simpa [generatorAngle] using hφ.2
      linarith, le_rfl⟩
  · have : arctan (b / a) < π / 2 := by
      simpa [generatorAngle] using hφ.2
    linarith

/-- The middle jump and Sector III arc meet only at the latter's initial
endpoint. -/
theorem range_sectorTwoThreeJumpPath_inter_sectorThreeArcPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range
        (Path.segment
          (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
          (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a)))) ∩
      Set.range (sectorThreeArcPath a b ha) =
      {sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a))} := by
  let θm := π / 2 + arctan (b / a)
  have hφ := generatorAngle_mem_Ioo ha hb
  have hθmMem : θm ∈ Icc θm π := by
    constructor
    · exact le_rfl
    · have : arctan (b / a) < π / 2 := by
        simpa [generatorAngle] using hφ.2
      dsimp only [θm]
      linarith
  have hxOrder :
      sectorThreeBoundaryX a b θm < sectorTwoBoundaryX a b θm := by
    simpa [θm, middleSectorTwoEndpoint, middleSectorThreeEndpoint,
      planeVector] using middleSectorThreeEndpoint_firstCoord_lt_two ha hb
  ext x
  constructor
  · rintro ⟨hxJump, hxArc⟩
    rw [Path.range_segment] at hxJump
    rw [range_sectorThreeArcPath ha hb] at hxArc
    rcases hxArc with ⟨θ, hθ, rfl⟩
    rcases hxJump with ⟨c, d, hc, hd, hcd, hcombo⟩
    have hcoord := congrArg (fun p : Plane => p 0) hcombo
    simp [sectorTwoBoundaryPoint, sectorThreeBoundaryPoint, planeVector] at hcoord
    have hcBound := mul_le_mul_of_nonneg_left hxOrder.le hc
    have hge : sectorThreeBoundaryX a b θm ≤
        sectorThreeBoundaryX a b θ := by
      calc
        sectorThreeBoundaryX a b θm =
            c * sectorThreeBoundaryX a b θm +
              d * sectorThreeBoundaryX a b θm := by
            rw [← add_mul, hcd, one_mul]
        _ ≤ c * sectorTwoBoundaryX a b θm +
              d * sectorThreeBoundaryX a b θm := by
            linarith only [hcBound]
        _ = sectorThreeBoundaryX a b θ := by
            simpa only [θm] using hcoord
    have hθeq : θ = θm := by
      apply le_antisymm
      · by_contra hnot
        have hlt : θm < θ := lt_of_not_ge hnot
        have hstrict := strictAntiOn_sectorThreeBoundaryX ha hb
          (by simpa only [θm] using hθmMem) hθ hlt
        linarith
      · simpa only [θm] using hθ.1
    subst θ
    simp [θm]
  · intro hx
    rw [Set.mem_singleton_iff] at hx
    subst x
    constructor
    · rw [Path.range_segment]
      exact right_mem_segment ℝ _ _
    · rw [range_sectorThreeArcPath ha hb]
      exact ⟨θm, by simpa only [θm] using hθmMem, by simp [θm]⟩

/-- The two curved upper arcs are disjoint. -/
theorem range_sectorTwoArcPath_inter_sectorThreeArcPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range (sectorTwoArcPath a b hb) ∩
      Set.range (sectorThreeArcPath a b ha) = ∅ := by
  ext x
  constructor
  · rintro ⟨hxTwo, hxThree⟩
    rw [range_sectorTwoArcPath ha hb] at hxTwo
    rw [range_sectorThreeArcPath ha hb] at hxThree
    rcases hxTwo with ⟨θ, hθ, hθx⟩
    rcases hxThree with ⟨ψ, hψ, hψx⟩
    have hxTwoBound := sectorTwoBoundaryX_middle_le_of_mem_arc ha hb hθ
    have hxThreeBound := sectorThreeBoundaryX_le_middle_of_mem_arc ha hb hψ
    have hcoord := congrArg (fun p : Plane => p 0) (hθx.trans hψx.symm)
    simp [sectorTwoBoundaryPoint, sectorThreeBoundaryPoint, planeVector] at hcoord
    have hgap := middleSectorThreeEndpoint_firstCoord_lt_two ha hb
    simp [middleSectorTwoEndpoint, middleSectorThreeEndpoint, planeVector] at hgap
    simp only [Set.mem_empty_iff_false]
    linarith
  · simp

/-- The first jump is disjoint from the Sector III curved arc. -/
theorem range_sectorOneTwoJumpPath_inter_sectorThreeArcPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range
        (Path.segment (sectorOneVertex a b)
          (sectorTwoBoundaryPoint a b (π / 2))) ∩
      Set.range (sectorThreeArcPath a b ha) = ∅ := by
  ext x
  constructor
  · rintro ⟨hxFirst, hxThree⟩
    rw [Path.range_segment] at hxFirst
    rw [range_sectorThreeArcPath ha hb] at hxThree
    rcases hxFirst with ⟨c, d, hc, hd, hcd, hFirst⟩
    rcases hxThree with ⟨θ, hθ, hThree⟩
    have hFirstCoord := congrArg (fun p : Plane => p 0) hFirst
    rw [sectorTwoBoundaryPoint_pi_div_two' hb] at hFirstCoord
    simp [sectorOneVertex, planeVector] at hFirstCoord
    have hLower : a ≤ x 0 := by nlinarith
    have hThreeBound := sectorThreeBoundaryX_le_middle_of_mem_arc ha hb hθ
    have hThreeCoord := congrArg (fun p : Plane => p 0) hThree
    simp [sectorThreeBoundaryPoint, planeVector] at hThreeCoord
    have hMiddleLt := sectorTwoBoundaryX_middle_lt_a ha hb
    have hgap := middleSectorThreeEndpoint_firstCoord_lt_two ha hb
    simp [middleSectorTwoEndpoint, middleSectorThreeEndpoint, planeVector] at hgap
    simp only [Set.mem_empty_iff_false]
    linarith
  · simp

/-- The first four consecutive upper pieces form an injective path. -/
theorem injective_firstFourUpperPieces {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Function.Injective
      (((((Path.segment (sectorOneVertex a b)
        (sectorTwoBoundaryPoint a b (π / 2))).trans
          (sectorTwoArcPath a b hb)).trans
        (Path.segment
          (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
          (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a))))).trans
        (sectorThreeArcPath a b ha))) := by
  apply Path.injective_trans_of_range_inter_subset _ _
    (injective_firstThreeUpperPieces ha hb)
    (injective_sectorThreeArcPath ha hb)
  rw [Path.trans_range, Path.trans_range]
  intro x hx
  rcases hx with ⟨(hxFirst | hxTwo) | hxMiddle, hxThree⟩
  · have hEmpty : x ∈ (∅ : Set Plane) := by
      rw [← range_sectorOneTwoJumpPath_inter_sectorThreeArcPath ha hb]
      exact ⟨hxFirst, hxThree⟩
    exact hEmpty.elim
  · have hEmpty : x ∈ (∅ : Set Plane) := by
      rw [← range_sectorTwoArcPath_inter_sectorThreeArcPath ha hb]
      exact ⟨hxTwo, hxThree⟩
    exact hEmpty.elim
  · have hCommon : x ∈
        ({sectorThreeBoundaryPoint a b
          (π / 2 + arctan (b / a))} : Set Plane) := by
      rw [← range_sectorTwoThreeJumpPath_inter_sectorThreeArcPath ha hb]
      exact ⟨hxMiddle, hxThree⟩
    exact hCommon

/-- The Sector III arc and closing jump meet only at their common endpoint. -/
theorem range_sectorThreeArcPath_inter_sectorThreeOneJumpPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range (sectorThreeArcPath a b ha) ∩
      Set.range
        (Path.segment (sectorThreeBoundaryPoint a b π)
          (-sectorOneVertex a b)) =
      {sectorThreeBoundaryPoint a b π} := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hπMem : π ∈ Icc (π / 2 + arctan (b / a)) π := by
    constructor
    · have : arctan (b / a) < π / 2 := by
        simpa [generatorAngle] using hφ.2
      linarith
    · exact le_rfl
  ext x
  constructor
  · rintro ⟨hxArc, hxJump⟩
    rw [range_sectorThreeArcPath ha hb] at hxArc
    rw [Path.range_segment] at hxJump
    rcases hxArc with ⟨θ, hθ, rfl⟩
    rcases hxJump with ⟨c, d, hc, hd, hcd, hcombo⟩
    have hcoord := congrArg (fun p : Plane => p 0) hcombo
    have hpiPoint := sectorThreeBoundaryPoint_pi (b := b) ha
    have hpiCoord := congrArg (fun p : Plane => p 0) hpiPoint
    simp [sectorThreeBoundaryPoint, sectorOneVertex, planeVector] at hcoord hpiCoord
    have hconst :
        sectorThreeBoundaryX a b θ = sectorThreeBoundaryX a b π := by
      rw [hpiCoord]
      nlinarith
    have hθeq : θ = π := by
      exact (strictAntiOn_sectorThreeBoundaryX ha hb).injOn hθ hπMem hconst
    subst θ
    simp
  · intro hx
    rw [Set.mem_singleton_iff] at hx
    subst x
    constructor
    · rw [range_sectorThreeArcPath ha hb]
      exact ⟨π, hπMem, rfl⟩
    · rw [Path.range_segment]
      exact left_mem_segment ℝ _ _

/-- The middle and closing jumps have disjoint ranges. -/
theorem range_sectorTwoThreeJumpPath_inter_sectorThreeOneJumpPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range
        (Path.segment
          (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
          (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a)))) ∩
      Set.range
        (Path.segment (sectorThreeBoundaryPoint a b π)
          (-sectorOneVertex a b)) = ∅ := by
  ext x
  constructor
  · rintro ⟨hxMiddle, hxClosing⟩
    rw [Path.range_segment] at hxMiddle hxClosing
    rcases hxMiddle with ⟨c, d, hc, hd, hcd, hMiddle⟩
    rcases hxClosing with ⟨r, s, hr, hs, hrs, hClosing⟩
    have hxOrder :
        sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) <
          sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) := by
      simpa [middleSectorTwoEndpoint, middleSectorThreeEndpoint, planeVector] using
        middleSectorThreeEndpoint_firstCoord_lt_two ha hb
    have hMiddleCoord := congrArg (fun p : Plane => p 0) hMiddle
    simp [sectorTwoBoundaryPoint, sectorThreeBoundaryPoint, planeVector] at hMiddleCoord
    have hcBound := mul_le_mul_of_nonneg_left hxOrder.le hc
    have hLower :
        sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) ≤ x 0 := by
      calc
        _ = c * sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) +
              d * sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) := by
            rw [← add_mul, hcd, one_mul]
        _ ≤ c * sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) +
              d * sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) := by
            linarith only [hcBound]
        _ = x 0 := hMiddleCoord
    have hClosingCoord := congrArg (fun p : Plane => p 0) hClosing
    have hpiPoint := sectorThreeBoundaryPoint_pi (b := b) ha
    have hpiCoord := congrArg (fun p : Plane => p 0) hpiPoint
    simp [sectorThreeBoundaryPoint, sectorOneVertex, planeVector] at hClosingCoord hpiCoord
    have hUpper : x 0 = sectorThreeBoundaryX a b π := by
      rw [hpiCoord]
      nlinarith
    have hgap := sectorThreeBoundaryX_pi_lt_middle ha hb
    simp only [Set.mem_empty_iff_false]
    linarith
  · simp

/-- The Sector II arc and closing jump have disjoint ranges. -/
theorem range_sectorTwoArcPath_inter_sectorThreeOneJumpPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range (sectorTwoArcPath a b hb) ∩
      Set.range
        (Path.segment (sectorThreeBoundaryPoint a b π)
          (-sectorOneVertex a b)) = ∅ := by
  ext x
  constructor
  · rintro ⟨hxTwo, hxClosing⟩
    rw [range_sectorTwoArcPath ha hb] at hxTwo
    rcases hxTwo with ⟨θ, hθ, hTwo⟩
    have hTwoBound := sectorTwoBoundaryX_middle_le_of_mem_arc ha hb hθ
    rw [Path.range_segment] at hxClosing
    rcases hxClosing with ⟨c, d, hc, hd, hcd, hClosing⟩
    have hClosingCoord := congrArg (fun p : Plane => p 0) hClosing
    have hpiPoint := sectorThreeBoundaryPoint_pi (b := b) ha
    have hpiCoord := congrArg (fun p : Plane => p 0) hpiPoint
    simp [sectorThreeBoundaryPoint, sectorOneVertex, planeVector] at hClosingCoord hpiCoord
    have hTwoCoord := congrArg (fun p : Plane => p 0) hTwo
    simp [sectorTwoBoundaryPoint, planeVector] at hTwoCoord
    have hgap23 := middleSectorThreeEndpoint_firstCoord_lt_two ha hb
    simp [middleSectorTwoEndpoint, middleSectorThreeEndpoint, planeVector] at hgap23
    have hgap3pi := sectorThreeBoundaryX_pi_lt_middle ha hb
    simp only [Set.mem_empty_iff_false]
    rw [hpiCoord] at hgap3pi
    nlinarith
  · simp

/-- The first and closing jumps have disjoint ranges. -/
theorem range_sectorOneTwoJumpPath_inter_sectorThreeOneJumpPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range
        (Path.segment (sectorOneVertex a b)
          (sectorTwoBoundaryPoint a b (π / 2))) ∩
      Set.range
        (Path.segment (sectorThreeBoundaryPoint a b π)
          (-sectorOneVertex a b)) = ∅ := by
  ext x
  constructor
  · rintro ⟨hxFirst, hxClosing⟩
    rw [Path.range_segment] at hxFirst hxClosing
    rcases hxFirst with ⟨c, d, hc, hd, hcd, hFirst⟩
    rcases hxClosing with ⟨r, s, hr, hs, hrs, hClosing⟩
    have hFirstCoord := congrArg (fun p : Plane => p 0) hFirst
    rw [sectorTwoBoundaryPoint_pi_div_two' hb] at hFirstCoord
    simp [sectorOneVertex, planeVector] at hFirstCoord
    have hLower : a ≤ x 0 := by nlinarith
    have hClosingCoord := congrArg (fun p : Plane => p 0) hClosing
    have hpiPoint := sectorThreeBoundaryPoint_pi (b := b) ha
    have hpiCoord := congrArg (fun p : Plane => p 0) hpiPoint
    simp [sectorThreeBoundaryPoint, sectorOneVertex, planeVector] at hClosingCoord
    simp [planeVector] at hpiCoord
    have hUpper : x 0 = -(1 + a) := by nlinarith
    simp only [Set.mem_empty_iff_false]
    linarith
  · simp

/-- All five consecutive upper-normal pieces form an injective path. -/
theorem injective_normalizedUpperBoundaryPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Function.Injective (normalizedUpperBoundaryPath a b ha hb) := by
  unfold normalizedUpperBoundaryPath
  apply Path.injective_trans_of_range_inter_subset _ _
    (injective_firstFourUpperPieces ha hb)
    (injective_sectorThreeOneJumpPath ha)
  rw [Path.trans_range, Path.trans_range, Path.trans_range]
  intro x hx
  rcases hx with ⟨((hxFirst | hxTwo) | hxMiddle) | hxThree, hxClosing⟩
  · have hEmpty : x ∈ (∅ : Set Plane) := by
      rw [← range_sectorOneTwoJumpPath_inter_sectorThreeOneJumpPath ha hb]
      exact ⟨hxFirst, hxClosing⟩
    exact hEmpty.elim
  · have hEmpty : x ∈ (∅ : Set Plane) := by
      rw [← range_sectorTwoArcPath_inter_sectorThreeOneJumpPath ha hb]
      exact ⟨hxTwo, hxClosing⟩
    exact hEmpty.elim
  · have hEmpty : x ∈ (∅ : Set Plane) := by
      rw [← range_sectorTwoThreeJumpPath_inter_sectorThreeOneJumpPath ha hb]
      exact ⟨hxMiddle, hxClosing⟩
    exact hEmpty.elim
  · have hCommon : x ∈ ({sectorThreeBoundaryPoint a b π} : Set Plane) := by
      rw [← range_sectorThreeArcPath_inter_sectorThreeOneJumpPath ha hb]
      exact ⟨hxThree, hxClosing⟩
    exact hCommon

#print axioms Path.injective_trans_of_range_inter_subset
#print axioms sectorTwoBoundaryPoint_pi_div_two'
#print axioms injective_sectorOneTwoJumpPath
#print axioms injective_sectorTwoThreeJumpPath
#print axioms injective_sectorThreeOneJumpPath
#print axioms range_sectorOneTwoJumpPath_inter_sectorTwoArcPath
#print axioms injective_sectorOneTwoJump_trans_sectorTwoArc
#print axioms range_sectorTwoArcPath_inter_sectorTwoThreeJumpPath
#print axioms range_sectorOneTwoJumpPath_inter_sectorTwoThreeJumpPath
#print axioms injective_firstThreeUpperPieces
#print axioms sectorThreeBoundaryX_pi_lt_middle
#print axioms range_sectorTwoThreeJumpPath_inter_sectorThreeArcPath
#print axioms range_sectorTwoArcPath_inter_sectorThreeArcPath
#print axioms range_sectorOneTwoJumpPath_inter_sectorThreeArcPath
#print axioms injective_firstFourUpperPieces
#print axioms range_sectorThreeArcPath_inter_sectorThreeOneJumpPath
#print axioms range_sectorTwoThreeJumpPath_inter_sectorThreeOneJumpPath
#print axioms range_sectorTwoArcPath_inter_sectorThreeOneJumpPath
#print axioms range_sectorOneTwoJumpPath_inter_sectorThreeOneJumpPath
#print axioms injective_normalizedUpperBoundaryPath

end

end L2Hexagon
