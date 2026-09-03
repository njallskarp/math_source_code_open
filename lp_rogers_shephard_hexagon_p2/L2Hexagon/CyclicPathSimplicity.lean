import L2Hexagon.UpperPathInjectivity
import Mathlib.Analysis.Convex.Topology

/-!
# Cyclic simplicity of the normalized Firey boundary path

Let `v=(1+a,1+b)` and let `U` be the range of the checked five-piece
upper-normal boundary path.  The geometric separation statement proved here
is

`U ∩ (-U) = {v,-v}`.

The proof is not diagrammatic.  The determinant with the diameter `[-v,v]`
can vanish at a frontier point only at the two endpoints: every other point
of that diameter lies in the interior because the body is convex and contains
the origin in its interior.  Continuity and one explicit point of the first
jump then give a strict determinant sign on the open upper path.

Combining the exact range intersection with injectivity of each half gives a
closed path that is injective on `[0,1)`; on the full unit interval its only
nontrivial repetition is the common initial/final endpoint.  This remains a
topological statement.  Positive global orientation and the Green/Jordan area
bridge are separate downstream obligations.
-/

open Real Set

namespace L2Hexagon

noncomputable section

/-! ## The separating diameter determinant -/

/-- Oriented determinant with the endpoint diameter vector
`v=(1+a,1+b)`. -/
def upperDiameterDet (a b : ℝ) (x : Plane) : ℝ :=
  (1 + a) * x 1 - (1 + b) * x 0

@[simp] theorem upperDiameterDet_sectorOneVertex (a b : ℝ) :
    upperDiameterDet a b (sectorOneVertex a b) = 0 := by
  simp [upperDiameterDet, sectorOneVertex, planeVector]
  ring

@[simp] theorem upperDiameterDet_neg (a b : ℝ) (x : Plane) :
    upperDiameterDet a b (-x) = -upperDiameterDet a b x := by
  simp [upperDiameterDet]
  ring

/-- A frontier point on the line through the two path endpoints is one of
those endpoints.  The open part of the diameter lies in the interior of the
convex body because `0` is an interior point. -/
theorem eq_sectorOneVertex_or_eq_neg_of_mem_frontier_of_upperDiameterDet_eq_zero
    {a b : ℝ} (ha : 0 < a) (_hb : 0 < b) {x : Plane}
    (hxfrontier : x ∈ frontier (normalizedLpSumTwo a b))
    (hdet : upperDiameterDet a b x = 0) :
    x = sectorOneVertex a b ∨ x = -sectorOneVertex a b := by
  have hxfrontier' := hxfrontier
  rw [(isClosed_normalizedLpSumTwo a b).frontier_eq] at hxfrontier'
  have hxbody : x ∈ normalizedLpSumTwo a b := hxfrontier'.1
  have hA : 0 < 1 + a := by linarith
  let t : ℝ := x 0 / (1 + a)
  have hxline : x = t • sectorOneVertex a b := by
    ext i
    fin_cases i
    · change x 0 = t * (1 + a)
      simp only [t]
      field_simp
    · change x 1 = t * (1 + b)
      simp only [t, upperDiameterDet] at hdet ⊢
      field_simp [hA.ne'] at hdet ⊢
      nlinarith
  have hx0hi : x 0 ≤ 1 + a :=
    firstCoord_le_of_mem_normalizedLpSumTwo ha hxbody
  have hx0lo : -(1 + a) ≤ x 0 := by
    have hneg := firstCoord_le_of_mem_normalizedLpSumTwo ha
      (neg_mem_normalizedLpSumTwo hxbody)
    change -(x 0) ≤ 1 + a at hneg
    linarith
  have htlo : -1 ≤ t := by
    dsimp only [t]
    apply (le_div_iff₀ hA).2
    linarith
  have hthi : t ≤ 1 := by
    dsimp only [t]
    exact (div_le_one hA).2 hx0hi
  by_cases htneg : t = -1
  · right
    rw [hxline, htneg]
    simp
  by_cases htpos : t = 1
  · left
    rw [hxline, htpos]
    simp
  have htIoo : t ∈ Ioo (-1 : ℝ) 1 :=
    ⟨lt_of_le_of_ne htlo (Ne.symm htneg), lt_of_le_of_ne hthi htpos⟩
  have hxint : x ∈ interior (normalizedLpSumTwo a b) := by
    rw [hxline]
    rcases lt_trichotomy t 0 with ht | ht | ht
    · have hopen : t • sectorOneVertex a b ∈
          openSegment ℝ (0 : Plane) (-sectorOneVertex a b) := by
        refine ⟨1 + t, -t, by linarith [htIoo.1], by linarith, by ring, ?_⟩
        simp
      exact (convex_normalizedLpSumTwo a b).openSegment_interior_self_subset_interior
        (zero_mem_interior_normalizedLpSumTwo a b)
        (neg_sectorOneVertex_mem_normalizedLpSumTwo a b) hopen
    · rw [ht, zero_smul]
      exact zero_mem_interior_normalizedLpSumTwo a b
    · have hopen : t • sectorOneVertex a b ∈
          openSegment ℝ (0 : Plane) (sectorOneVertex a b) := by
        refine ⟨1 - t, t, by linarith [htIoo.2], ht, by ring, ?_⟩
        simp
      exact (convex_normalizedLpSumTwo a b).openSegment_interior_self_subset_interior
        (zero_mem_interior_normalizedLpSumTwo a b)
        (sectorOneVertex_mem_normalizedLpSumTwo a b) hopen
  exact (hxfrontier'.2 hxint).elim

/-- Every point of the five-piece upper path lies on the actual frontier. -/
theorem normalizedUpperBoundaryPath_mem_frontier {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) (t : unitInterval) :
    normalizedUpperBoundaryPath a b ha hb t ∈
      frontier (normalizedLpSumTwo a b) := by
  apply normalizedUpperNormalBoundary_subset_frontier ha hb
  apply normalizedClosedUpperBoundary_subset_upperNormalBoundary ha hb
  rw [← range_normalizedUpperBoundaryPath ha hb]
  exact ⟨t, rfl⟩

/-- The diameter determinant cannot vanish at an interior parameter of the
injective upper path. -/
theorem upperDiameterDet_ne_zero_on_open_upperPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) {t : unitInterval}
    (ht : (t : ℝ) ∈ Ioo 0 1) :
    upperDiameterDet a b (normalizedUpperBoundaryPath a b ha hb t) ≠ 0 := by
  intro hzero
  rcases
      eq_sectorOneVertex_or_eq_neg_of_mem_frontier_of_upperDiameterDet_eq_zero
        ha hb (normalizedUpperBoundaryPath_mem_frontier ha hb t) hzero with h | h
  · have ht0 : t = (0 : unitInterval) :=
      (injective_normalizedUpperBoundaryPath ha hb)
        (h.trans (normalizedUpperBoundaryPath a b ha hb).source.symm)
    have := congrArg Subtype.val ht0
    exact (ne_of_gt ht.1) this
  · have ht1 : t = (1 : unitInterval) :=
      (injective_normalizedUpperBoundaryPath ha hb)
        (h.trans (normalizedUpperBoundaryPath a b ha hb).target.symm)
    have := congrArg Subtype.val ht1
    exact (ne_of_lt ht.2) this

/-- The diameter determinant is strictly positive at every interior parameter
of the upper path.  Continuity prevents its sign from changing because the
previous theorem excludes an interior zero. -/
theorem upperDiameterDet_pos_on_open_upperPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) {t : unitInterval}
    (ht : (t : ℝ) ∈ Ioo 0 1) :
    0 < upperDiameterDet a b (normalizedUpperBoundaryPath a b ha hb t) := by
  let upper := normalizedUpperBoundaryPath a b ha hb
  let p := sectorTwoBoundaryPoint a b (π / 2)
  have hpU : p ∈ normalizedClosedUpperBoundary a b := by
    apply Or.inl
    apply Or.inl
    apply Or.inl
    apply Or.inl
    unfold sectorOneTwoJump
    exact right_mem_segment ℝ _ _
  have hpRange : p ∈ Set.range upper := by
    rw [range_normalizedUpperBoundaryPath ha hb]
    exact hpU
  obtain ⟨s, hs⟩ := hpRange
  have hpneStart : p ≠ sectorOneVertex a b := by
    exact (sectorOneVertex_ne_sectorTwoBoundaryPoint_pi_div_two hb).symm
  have hpneEnd : p ≠ -sectorOneVertex a b := by
    intro h
    have h0 := congrArg (fun z : Plane => z 0) h
    change sectorTwoBoundaryPoint a b (π / 2) 0 =
      (-sectorOneVertex a b) 0 at h0
    rw [sectorTwoBoundaryPoint_pi_div_two' hb] at h0
    simp [sectorOneVertex, planeVector] at h0
    linarith
  have hs0 : (s : ℝ) ≠ 0 := by
    intro hs0
    have hs0' : s = (0 : unitInterval) := Subtype.ext hs0
    subst s
    exact hpneStart (hs.symm.trans upper.source)
  have hs1 : (s : ℝ) ≠ 1 := by
    intro hs1
    have hs1' : s = (1 : unitInterval) := Subtype.ext hs1
    subst s
    exact hpneEnd (hs.symm.trans upper.target)
  have hsIoo : (s : ℝ) ∈ Ioo 0 1 :=
    ⟨lt_of_le_of_ne s.2.1 (Ne.symm hs0), lt_of_le_of_ne s.2.2 hs1⟩
  have hsp : 0 < upperDiameterDet a b (upper s) := by
    rw [hs]
    change 0 < upperDiameterDet a b (sectorTwoBoundaryPoint a b (π / 2))
    rw [sectorTwoBoundaryPoint_pi_div_two' hb]
    simp [upperDiameterDet, planeVector]
    linarith
  have hcont : Continuous (fun r : unitInterval => upperDiameterDet a b (upper r)) := by
    unfold upperDiameterDet
    fun_prop
  by_contra hnot
  have htne := upperDiameterDet_ne_zero_on_open_upperPath ha hb ht
  have htneg : upperDiameterDet a b (upper t) < 0 :=
    lt_of_le_of_ne (le_of_not_gt hnot) htne
  rcases le_total s t with hst | hts
  · obtain ⟨r, hr, hzero⟩ :=
      (intermediate_value_Icc' hst hcont.continuousOn)
        (show 0 ∈ Icc (upperDiameterDet a b (upper t))
            (upperDiameterDet a b (upper s)) from ⟨htneg.le, hsp.le⟩)
    have hrIoo : (r : ℝ) ∈ Ioo 0 1 := by
      have hsr : (s : ℝ) ≤ (r : ℝ) := hr.1
      have hrt : (r : ℝ) ≤ (t : ℝ) := hr.2
      exact ⟨lt_of_lt_of_le hsIoo.1 hsr, lt_of_le_of_lt hrt ht.2⟩
    exact (upperDiameterDet_ne_zero_on_open_upperPath ha hb hrIoo) hzero
  · obtain ⟨r, hr, hzero⟩ :=
      (intermediate_value_Icc hts hcont.continuousOn)
        (show 0 ∈ Icc (upperDiameterDet a b (upper t))
            (upperDiameterDet a b (upper s)) from ⟨htneg.le, hsp.le⟩)
    have hrIoo : (r : ℝ) ∈ Ioo 0 1 := by
      have htr : (t : ℝ) ≤ (r : ℝ) := hr.1
      have hrs : (r : ℝ) ≤ (s : ℝ) := hr.2
      exact ⟨lt_of_lt_of_le ht.1 htr, lt_of_le_of_lt hrs hsIoo.2⟩
    exact (upperDiameterDet_ne_zero_on_open_upperPath ha hb hrIoo) hzero

/-- The determinant is nonnegative on the closed upper path, with zeros only
at the two endpoints. -/
theorem upperDiameterDet_nonneg_on_upperPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) (t : unitInterval) :
    0 ≤ upperDiameterDet a b (normalizedUpperBoundaryPath a b ha hb t) := by
  by_cases ht0 : (t : ℝ) = 0
  · have ht0' : t = (0 : unitInterval) := Subtype.ext ht0
    subst t
    simp
  by_cases ht1 : (t : ℝ) = 1
  · have ht1' : t = (1 : unitInterval) := Subtype.ext ht1
    subst t
    simp
  exact (upperDiameterDet_pos_on_open_upperPath ha hb
    ⟨lt_of_le_of_ne t.2.1 (Ne.symm ht0), lt_of_le_of_ne t.2.2 ht1⟩).le

/-! ## Exact intersection of the two half-boundaries -/

/-- The closed upper boundary and its pointwise negative meet exactly at the
two endpoints of the diameter. -/
theorem normalizedClosedUpperBoundary_inter_neg {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedClosedUpperBoundary a b ∩ -normalizedClosedUpperBoundary a b =
      {sectorOneVertex a b, -sectorOneVertex a b} := by
  let upper := normalizedUpperBoundaryPath a b ha hb
  have hvU : sectorOneVertex a b ∈ normalizedClosedUpperBoundary a b := by
    rw [← range_normalizedUpperBoundaryPath ha hb]
    exact upper.source_mem_range
  have hnvU : -sectorOneVertex a b ∈ normalizedClosedUpperBoundary a b := by
    rw [← range_normalizedUpperBoundaryPath ha hb]
    exact upper.target_mem_range
  ext x
  constructor
  · rintro ⟨hxU, hxnegU⟩
    rw [Set.mem_neg] at hxnegU
    have hxRange : x ∈ Set.range upper := by
      rw [range_normalizedUpperBoundaryPath ha hb]
      exact hxU
    have hnegxRange : -x ∈ Set.range upper := by
      rw [range_normalizedUpperBoundaryPath ha hb]
      exact hxnegU
    obtain ⟨t, ht⟩ := hxRange
    obtain ⟨s, hs⟩ := hnegxRange
    have htNonneg := upperDiameterDet_nonneg_on_upperPath ha hb t
    have hsNonneg := upperDiameterDet_nonneg_on_upperPath ha hb s
    have hxdet : upperDiameterDet a b x = 0 := by
      rw [hs] at hsNonneg
      rw [upperDiameterDet_neg] at hsNonneg
      rw [ht] at htNonneg
      linarith
    have hxfrontier : x ∈ frontier (normalizedLpSumTwo a b) := by
      rw [← ht]
      exact normalizedUpperBoundaryPath_mem_frontier ha hb t
    rcases
        eq_sectorOneVertex_or_eq_neg_of_mem_frontier_of_upperDiameterDet_eq_zero
          ha hb hxfrontier hxdet with rfl | rfl
    · simp
    · simp
  · intro hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl
    · exact ⟨hvU, by rw [Set.mem_neg]; simpa using hnvU⟩
    · exact ⟨hnvU, by rw [Set.mem_neg]; simpa using hvU⟩

/-! ## A reusable closed-concatenation lemma -/

/-- If two injective paths run from `x` to `y` and back and their ranges meet
only at `x,y`, their concatenation is injective on the half-open unit
interval. -/
theorem Path.injOn_trans_Ico_of_range_inter_subset {X : Type*}
    [TopologicalSpace X] {x y : X} (p : Path x y) (q : Path y x)
    (hp : Function.Injective p) (hq : Function.Injective q)
    (hinter : Set.range p ∩ Set.range q ⊆ {x, y}) :
    Set.InjOn (p.trans q) (Ico (0 : unitInterval) 1) := by
  intro s hs t ht heq
  rw [Path.trans_apply, Path.trans_apply] at heq
  split_ifs at heq with hshalf hthalf
  · have harg := hp heq
    exact Subtype.ext (by
      have := congrArg Subtype.val harg
      norm_num at this ⊢
      linarith)
  · let ps : unitInterval :=
      ⟨2 * (s : ℝ), by constructor <;> linarith [s.2.1, s.2.2]⟩
    let qt : unitInterval :=
      ⟨2 * (t : ℝ) - 1, by
        constructor <;> linarith [t.2.1, t.2.2, not_le.1 hthalf]⟩
    have hmeet : p ps ∈ Set.range p ∩ Set.range q := by
      refine ⟨Set.mem_range_self ps, ?_⟩
      exact ⟨qt, by simpa only [ps, qt] using heq.symm⟩
    have hxy : p ps ∈ ({x, y} : Set X) := hinter hmeet
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hxy
    rcases hxy with hxval | hyval
    · have hsarg : ps = (0 : unitInterval) := by
        apply hp
        simpa using hxval
      have htarg : qt = (1 : unitInterval) := by
        apply hq
        have : q qt = x := by
          have hqp : q qt = p ps := by
            simpa only [ps, qt] using heq.symm
          exact hqp.trans hxval
        simpa using this
      have hsarg' := congrArg Subtype.val hsarg
      have htarg' := congrArg Subtype.val htarg
      change 2 * (s : ℝ) = 0 at hsarg'
      change 2 * (t : ℝ) - 1 = 1 at htarg'
      have htlt : (t : ℝ) < 1 := ht.2
      linarith
    · have hsarg : ps = (1 : unitInterval) := by
        apply hp
        simpa using hyval
      have htarg : qt = (0 : unitInterval) := by
        apply hq
        have : q qt = y := by
          have hqp : q qt = p ps := by
            simpa only [ps, qt] using heq.symm
          exact hqp.trans hyval
        simpa using this
      have hsarg' := congrArg Subtype.val hsarg
      have htarg' := congrArg Subtype.val htarg
      change 2 * (s : ℝ) = 1 at hsarg'
      change 2 * (t : ℝ) - 1 = 0 at htarg'
      linarith [not_le.1 hthalf]
  · let pt : unitInterval :=
      ⟨2 * (t : ℝ), by constructor <;> linarith [t.2.1, t.2.2]⟩
    let qs : unitInterval :=
      ⟨2 * (s : ℝ) - 1, by
        constructor <;> linarith [s.2.1, s.2.2, not_le.1 hshalf]⟩
    have hmeet : p pt ∈ Set.range p ∩ Set.range q := by
      refine ⟨Set.mem_range_self pt, ?_⟩
      exact ⟨qs, by simpa only [pt, qs] using heq⟩
    have hxy : p pt ∈ ({x, y} : Set X) := hinter hmeet
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hxy
    rcases hxy with hxval | hyval
    · have htarg : pt = (0 : unitInterval) := by
        apply hp
        simpa using hxval
      have hsarg : qs = (1 : unitInterval) := by
        apply hq
        have : q qs = x := by
          have hqp : q qs = p pt := by
            simpa only [pt, qs] using heq
          exact hqp.trans hxval
        simpa using this
      have hsarg' := congrArg Subtype.val hsarg
      have htarg' := congrArg Subtype.val htarg
      change 2 * (s : ℝ) - 1 = 1 at hsarg'
      change 2 * (t : ℝ) = 0 at htarg'
      have hslt : (s : ℝ) < 1 := hs.2
      linarith
    · have htarg : pt = (1 : unitInterval) := by
        apply hp
        simpa using hyval
      have hsarg : qs = (0 : unitInterval) := by
        apply hq
        have : q qs = y := by
          have hqp : q qs = p pt := by
            simpa only [pt, qs] using heq
          exact hqp.trans hyval
        simpa using this
      have hsarg' := congrArg Subtype.val hsarg
      have htarg' := congrArg Subtype.val htarg
      change 2 * (s : ℝ) - 1 = 0 at hsarg'
      change 2 * (t : ℝ) = 1 at htarg'
      linarith [not_le.1 hshalf]
  · have harg := hq heq
    exact Subtype.ext (by
      have := congrArg Subtype.val harg
      norm_num at this ⊢
      linarith)

/-- Exact range of the pointwise-negative return half. -/
theorem range_neg_normalizedUpperBoundaryPath {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.range
        (((normalizedUpperBoundaryPath a b ha hb).map
          (f := fun x : Plane => -x) continuous_neg).cast
            (x' := -sectorOneVertex a b) (y' := sectorOneVertex a b)
            rfl (by simp)) =
      -normalizedClosedUpperBoundary a b := by
  rw [Path.cast_coe, Path.map_coe, Set.range_comp,
    range_normalizedUpperBoundaryPath ha hb]
  ext x
  simp [Set.mem_neg]

/-- The actual normalized cyclic boundary path is injective on `[0,1)`. -/
theorem injOn_normalizedCyclicBoundaryPath_Ico {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    Set.InjOn (normalizedCyclicBoundaryPath a b ha hb)
      (Ico (0 : unitInterval) 1) := by
  let upper := normalizedUpperBoundaryPath a b ha hb
  let lower : Path (-sectorOneVertex a b) (sectorOneVertex a b) :=
    (upper.map (f := fun x : Plane => -x) continuous_neg).cast rfl (by simp)
  have hlower : Function.Injective lower := by
    intro s t hst
    apply injective_normalizedUpperBoundaryPath ha hb
    have hneg := congrArg (fun x : Plane => -x) hst
    simpa [lower, upper, Path.cast_coe, Path.map_coe] using hneg
  have hinter : Set.range upper ∩ Set.range lower ⊆
      {sectorOneVertex a b, -sectorOneVertex a b} := by
    rw [range_normalizedUpperBoundaryPath ha hb,
      range_neg_normalizedUpperBoundaryPath ha hb,
      normalizedClosedUpperBoundary_inter_neg ha hb]
  have h := Path.injOn_trans_Ico_of_range_inter_subset upper lower
    (injective_normalizedUpperBoundaryPath ha hb) hlower hinter
  simpa [normalizedCyclicBoundaryPath, upper, lower] using h

/-- On the full unit interval the only possible nontrivial repetition of the
cyclic path is the identified initial/final endpoint pair. -/
theorem eq_or_endpoints_of_normalizedCyclicBoundaryPath_eq {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) {s t : unitInterval}
    (hst : normalizedCyclicBoundaryPath a b ha hb s =
      normalizedCyclicBoundaryPath a b ha hb t) :
    s = t ∨ (s = 0 ∧ t = 1) ∨ (s = 1 ∧ t = 0) := by
  let γ := normalizedCyclicBoundaryPath a b ha hb
  have hinj := injOn_normalizedCyclicBoundaryPath_Ico ha hb
  by_cases hs1 : s = 1
  · by_cases ht1 : t = 1
    · exact Or.inl (hs1.trans ht1.symm)
    · have htlt : t < 1 := lt_of_le_of_ne t.2.2 ht1
      have ht0 : t = 0 := hinj ⟨t.2.1, htlt⟩
        ⟨le_rfl, zero_lt_one⟩ (by
          subst s
          simpa [γ] using hst.symm)
      exact Or.inr (Or.inr ⟨hs1, ht0⟩)
  · have hslt : s < 1 := lt_of_le_of_ne s.2.2 hs1
    by_cases ht1 : t = 1
    · have hs0 : s = 0 := hinj ⟨s.2.1, hslt⟩
          ⟨le_rfl, zero_lt_one⟩ (by
            subst t
            simpa [γ] using hst)
      exact Or.inr (Or.inl ⟨hs0, ht1⟩)
    · have htlt : t < 1 := lt_of_le_of_ne t.2.2 ht1
      exact Or.inl (hinj ⟨s.2.1, hslt⟩ ⟨t.2.1, htlt⟩ hst)

#print axioms
  eq_sectorOneVertex_or_eq_neg_of_mem_frontier_of_upperDiameterDet_eq_zero
#print axioms upperDiameterDet_pos_on_open_upperPath
#print axioms normalizedClosedUpperBoundary_inter_neg
#print axioms Path.injOn_trans_Ico_of_range_inter_subset
#print axioms injOn_normalizedCyclicBoundaryPath_Ico
#print axioms eq_or_endpoints_of_normalizedCyclicBoundaryPath_eq

end

end L2Hexagon
