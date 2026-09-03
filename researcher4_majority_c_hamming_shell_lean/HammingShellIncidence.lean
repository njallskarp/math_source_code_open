import MajorityShellBound

/-!
# Hamming first-shell/distance-two-shell incidence

This file formalizes the graph-theoretic double count consumed by
`MajorityCHamming.card_ge_of_shell_incidence`.  It uses Mathlib's literal
`hammingDist` on finite dependent function types.
-/

open Finset Function

namespace MajorityCHamming

universe u v

variable {ι : Type u} {β : ι → Type v}
variable [Fintype ι] [DecidableEq ι]
variable [∀ i, DecidableEq (β i)]

/-- The finite set of coordinates at which two Hamming words differ. -/
def changeSupport (x y : ∀ i, β i) : Finset ι :=
  Finset.univ.filter fun i => x i ≠ y i

omit [DecidableEq ι] in
@[simp]
theorem mem_changeSupport {x y : ∀ i, β i} {i : ι} :
    i ∈ changeSupport x y ↔ x i ≠ y i := by
  simp [changeSupport]

omit [DecidableEq ι] in
theorem card_changeSupport (x y : ∀ i, β i) :
    #(changeSupport x y) = hammingDist x y :=
  rfl

omit [DecidableEq ι] in
@[simp]
theorem changeSupport_self (x : ∀ i, β i) : changeSupport x x = ∅ := by
  ext i
  simp

/-- The selected words which differ from `v` in exactly direction `i`. -/
def directionShell (C : Finset (∀ i, β i)) (v : ∀ i, β i) (i : ι) :
    Finset (∀ i, β i) :=
  C.filter fun u => changeSupport v u = {i}

/-- The selected words at Hamming distance `d` from `v`. -/
def distanceShell (C : Finset (∀ i, β i)) (v : ∀ i, β i) (d : ℕ) :
    Finset (∀ i, β i) :=
  C.filter fun u => hammingDist v u = d

/-- The selected Hamming neighbors of `u`. -/
def internalNeighbors (C : Finset (∀ i, β i)) (u : ∀ i, β i) :
    Finset (∀ i, β i) :=
  C.filter fun w => hammingDist u w = 1

/-- The first shell with its unique differing coordinate retained. -/
def directedFirstShell (C : Finset (∀ i, β i)) (v : ∀ i, β i) :
    Finset (ι × (∀ i, β i)) :=
  (Finset.univ.product C).filter fun p => changeSupport v p.2 = {p.1}

omit [DecidableEq ι] in
theorem hammingDist_eq_one_of_changeSupport_eq_singleton
    {x y : ∀ i, β i} {i : ι} (h : changeSupport x y = {i}) :
    hammingDist x y = 1 := by
  rw [← card_changeSupport, h]
  simp

omit [DecidableEq ι] in
theorem changeSupport_eq_singleton_of_hammingDist_eq_one
    {x y : ∀ i, β i} (h : hammingDist x y = 1) :
    ∃ i, changeSupport x y = {i} := by
  rw [← card_changeSupport] at h
  exact Finset.card_eq_one.mp h

omit [DecidableEq ι] in
theorem eq_at_of_not_mem_changeSupport
    {x y : ∀ i, β i} {i : ι} (h : i ∉ changeSupport x y) : x i = y i := by
  simpa using h

/-- Two first-shell words adjacent to each other lie in the same coordinate
direction from their common center. -/
theorem changeSupport_eq_of_first_shell_adjacent
    {v₀ u w : ∀ i, β i} {i : ι}
    (hu : changeSupport v₀ u = {i})
    (hvw : hammingDist v₀ w = 1)
    (huw : hammingDist u w = 1) :
    changeSupport v₀ w = {i} := by
  obtain ⟨j, hw⟩ := changeSupport_eq_singleton_of_hammingDist_eq_one hvw
  suffices j = i by simp [hw, this]
  by_contra hji
  have hij : i ≠ j := Ne.symm hji
  have hi_u : v₀ i ≠ u i := by
    have : i ∈ changeSupport v₀ u := by simp [hu]
    simpa using this
  have hj_w : v₀ j ≠ w j := by
    have : j ∈ changeSupport v₀ w := by simp [hw]
    simpa using this
  have hw_i : w i = v₀ i := by
    have : i ∉ changeSupport v₀ w := by simp [hw, hij]
    exact (eq_at_of_not_mem_changeSupport this).symm
  have hu_j : u j = v₀ j := by
    have : j ∉ changeSupport v₀ u := by simp [hu, hji]
    exact (eq_at_of_not_mem_changeSupport this).symm
  have hi : i ∈ changeSupport u w := by
    simp [hw_i, hi_u.symm]
  have hj : j ∈ changeSupport u w := by
    simp [hu_j, hj_w]
  have hpairs : ({i, j} : Finset ι) ⊆ changeSupport u w := by
    simpa [Finset.insert_subset_iff] using And.intro hi hj
  have hcard := Finset.card_le_card hpairs
  rw [Finset.card_pair hij, card_changeSupport, huw] at hcard
  omega

/-- If `w` is at distance two from `v₀`, a first-shell word adjacent to `w`
must use one of the two changed coordinates of `w`. -/
theorem direction_mem_changeSupport_of_adjacent_secondShell
    {v₀ u w : ∀ i, β i} {i : ι}
    (hu : changeSupport v₀ u = {i})
    (hw : hammingDist v₀ w = 2)
    (huw : hammingDist u w = 1) :
    i ∈ changeSupport v₀ w := by
  by_contra hi
  have hsubset : changeSupport v₀ w ⊆ changeSupport u w := by
    intro j hj
    have hji : j ≠ i := by
      intro h
      subst j
      exact hi hj
    have huj : u j = v₀ j := by
      have : j ∉ changeSupport v₀ u := by simp [hu, hji]
      exact (eq_at_of_not_mem_changeSupport this).symm
    have hvwj : v₀ j ≠ w j := by simpa using hj
    simp [huj, hvwj]
  have hcard := Finset.card_le_card hsubset
  rw [card_changeSupport, hw, card_changeSupport, huw] at hcard
  omega

/-- For a fixed center, direction, and distance-two endpoint there is at most
one first-shell word in that direction adjacent to the endpoint. -/
theorem eq_of_same_direction_adjacent_secondShell
    {v₀ u u' w : ∀ i, β i} {i : ι}
    (hu : changeSupport v₀ u = {i})
    (hu' : changeSupport v₀ u' = {i})
    (hw : hammingDist v₀ w = 2)
    (huw : hammingDist u w = 1)
    (hu'w : hammingDist u' w = 1) :
    u = u' := by
  have hiw := direction_mem_changeSupport_of_adjacent_secondShell hu hw huw
  have hcard_vw : #(changeSupport v₀ w) = 2 := by
    rw [card_changeSupport, hw]
  have ui_eq_wi : u i = w i := by
    by_contra hui
    have hi_uw : i ∈ changeSupport u w := by simpa using hui
    have hsubset : changeSupport v₀ w ⊆ changeSupport u w := by
      intro j hj
      by_cases hji : j = i
      · simpa [hji] using hi_uw
      · have huj : u j = v₀ j := by
          have : j ∉ changeSupport v₀ u := by simp [hu, hji]
          exact (eq_at_of_not_mem_changeSupport this).symm
        have hvwj : v₀ j ≠ w j := by simpa using hj
        simp [huj, hvwj]
    have hcard := Finset.card_le_card hsubset
    rw [hcard_vw, card_changeSupport, huw] at hcard
    omega
  have u'i_eq_wi : u' i = w i := by
    by_contra hu'i
    have hi_u'w : i ∈ changeSupport u' w := by simpa using hu'i
    have hsubset : changeSupport v₀ w ⊆ changeSupport u' w := by
      intro j hj
      by_cases hji : j = i
      · simpa [hji] using hi_u'w
      · have hu'j : u' j = v₀ j := by
          have : j ∉ changeSupport v₀ u' := by simp [hu', hji]
          exact (eq_at_of_not_mem_changeSupport this).symm
        have hvwj : v₀ j ≠ w j := by simpa using hj
        simp [hu'j, hvwj]
    have hcard := Finset.card_le_card hsubset
    rw [hcard_vw, card_changeSupport, hu'w] at hcard
    omega
  funext j
  by_cases hji : j = i
  · subst j
    exact ui_eq_wi.trans u'i_eq_wi.symm
  · have huj : u j = v₀ j := by
      have : j ∉ changeSupport v₀ u := by simp [hu, hji]
      exact (eq_at_of_not_mem_changeSupport this).symm
    have hu'j : u' j = v₀ j := by
      have : j ∉ changeSupport v₀ u' := by simp [hu', hji]
      exact (eq_at_of_not_mem_changeSupport this).symm
    exact huj.trans hu'j.symm

/-- A selected distance-two word has at most two adjacent directed
first-shell words. -/
theorem card_directedFirstShell_neighbors_le_two
    (C : Finset (∀ i, β i)) (v₀ w : ∀ i, β i)
    (hw : w ∈ distanceShell C v₀ 2) :
    #((directedFirstShell C v₀).bipartiteBelow
      (fun p w => hammingDist p.2 w = 1) w) ≤ 2 := by
  classical
  let S := (directedFirstShell C v₀).bipartiteBelow
    (fun p w => hammingDist p.2 w = 1) w
  have hwC : hammingDist v₀ w = 2 := (Finset.mem_filter.mp hw).2
  calc
    #S ≤ #(changeSupport v₀ w) := by
      refine Finset.card_le_card_of_injOn Prod.fst ?_ ?_
      · intro p hp
        have hp' : p ∈ directedFirstShell C v₀ ∧ hammingDist p.2 w = 1 := by
          simpa [S, Finset.bipartiteBelow] using hp
        have hpL := Finset.mem_filter.mp hp'.1
        exact direction_mem_changeSupport_of_adjacent_secondShell hpL.2 hwC hp'.2
      · intro p hp q hq hpq
        have hp' : p ∈ directedFirstShell C v₀ ∧ hammingDist p.2 w = 1 := by
          simpa [S, Finset.bipartiteBelow] using hp
        have hq' : q ∈ directedFirstShell C v₀ ∧ hammingDist q.2 w = 1 := by
          simpa [S, Finset.bipartiteBelow] using hq
        have hpL := Finset.mem_filter.mp hp'.1
        have hqL := Finset.mem_filter.mp hq'.1
        apply Prod.ext hpq
        have hqdir : changeSupport v₀ q.2 = {p.1} :=
          hqL.2.trans (congrArg ({·} : ι → Finset ι) hpq).symm
        exact eq_of_same_direction_adjacent_secondShell
          hpL.2 hqdir hwC hp'.2 hq'.2
    _ = 2 := by rw [card_changeSupport, hwC]

/-- A neighbor of a first-shell word is either the center, in the same
first-shell direction, or in the distance-two shell. -/
theorem adjacent_firstShell_classification
    {v₀ u w : ∀ i, β i} {i : ι}
    (hu : changeSupport v₀ u = {i})
    (huw : hammingDist u w = 1) :
    w = v₀ ∨ changeSupport v₀ w = {i} ∨ hammingDist v₀ w = 2 := by
  have hvu : hammingDist v₀ u = 1 :=
    hammingDist_eq_one_of_changeSupport_eq_singleton hu
  have hle := hammingDist_triangle v₀ u w
  rw [hvu, huw] at hle
  by_cases hw0 : hammingDist v₀ w = 0
  · exact Or.inl (hammingDist_eq_zero.mp hw0).symm
  by_cases hw1 : hammingDist v₀ w = 1
  · exact Or.inr (Or.inl (changeSupport_eq_of_first_shell_adjacent hu hw1 huw))
  · exact Or.inr (Or.inr (by omega))

/-- All selected neighbors of a directed first-shell word are accounted for
by the center and its own direction, or by the selected distance-two shell. -/
theorem card_internalNeighbors_le_direction_add_second
    (C : Finset (∀ i, β i)) (v₀ u : ∀ i, β i) (i : ι)
    (hu : u ∈ directionShell C v₀ i) :
    #(internalNeighbors C u) ≤ #(directionShell C v₀ i) +
      #((distanceShell C v₀ 2).bipartiteAbove
        (fun u w => hammingDist u w = 1) u) := by
  classical
  let L := directionShell C v₀ i
  let Bn := (distanceShell C v₀ 2).bipartiteAbove
    (fun u w => hammingDist u w = 1) u
  let accounted := insert v₀ (L.erase u) ∪ Bn
  have hu_support : changeSupport v₀ u = {i} := (Finset.mem_filter.mp hu).2
  have hsubset : internalNeighbors C u ⊆ accounted := by
    intro w hw
    have hw' := Finset.mem_filter.mp hw
    rcases adjacent_firstShell_classification hu_support hw'.2 with hwv | hwL | hwB
    · subst w
      simp [accounted]
    · have hw_mem_L : w ∈ L := by
        exact Finset.mem_filter.mpr ⟨hw'.1, hwL⟩
      have hwu : w ≠ u := by
        intro h
        subst w
        simpa using hw'.2
      have hw_erase : w ∈ L.erase u := by simpa [hwu] using hw_mem_L
      exact Finset.mem_union_left _ (Finset.mem_insert_of_mem hw_erase)
    · have hw_mem_Bn : w ∈ Bn := by
        simp [Bn, Finset.bipartiteAbove, distanceShell, hw'.1, hwB, hw'.2]
      exact Finset.mem_union_right _ hw_mem_Bn
  have hv_not_L : v₀ ∉ L := by
    simp [L, directionShell]
  have huL : u ∈ L := by simpa [L] using hu
  have hLone : 1 ≤ #L := Finset.one_le_card.mpr ⟨u, huL⟩
  have hv_not_erase : v₀ ∉ L.erase u := by
    exact fun h => hv_not_L (Finset.mem_of_mem_erase h)
  have hcard_accounted : #(insert v₀ (L.erase u)) = #L := by
    rw [Finset.card_insert_of_notMem hv_not_erase, Finset.card_erase_of_mem huL]
    exact Nat.sub_add_cancel hLone
  calc
    #(internalNeighbors C u) ≤ #accounted := Finset.card_le_card hsubset
    _ ≤ #(insert v₀ (L.erase u)) + #Bn := by
      simpa [accounted] using Finset.card_union_le (insert v₀ (L.erase u)) Bn
    _ = #L + #Bn := by rw [hcard_accounted]

/-- The majority-degree hypothesis leaves at least `h - |L_i|` neighbors of
each directed first-shell word in the selected distance-two shell. -/
theorem threshold_sub_direction_card_le_second_neighbors
    (C : Finset (∀ i, β i)) (v₀ u : ∀ i, β i) (i : ι) (h : ℕ)
    (hu : u ∈ directionShell C v₀ i)
    (hdegree : h ≤ #(internalNeighbors C u)) :
    h - #(directionShell C v₀ i) ≤
      #((distanceShell C v₀ 2).bipartiteAbove
        (fun u w => hammingDist u w = 1) u) := by
  have haccount := card_internalNeighbors_le_direction_add_second C v₀ u i hu
  omega

/-- Summing a direction-dependent constant over the directed first shell is
the same as multiplying each direction value by that direction's size. -/
theorem sum_directedFirstShell
    (C : Finset (∀ i, β i)) (v₀ : ∀ i, β i) (f : ι → ℕ) :
    (∑ p ∈ directedFirstShell C v₀, f p.1) =
      ∑ i, #(directionShell C v₀ i) * f i := by
  classical
  calc
    (∑ p ∈ directedFirstShell C v₀, f p.1) =
        ∑ i ∈ Finset.univ, ∑ u ∈ directionShell C v₀ i, f i := by
      have hfib : ∀ p : ι × (∀ i, β i),
          p ∈ directedFirstShell C v₀ ↔
            p.1 ∈ Finset.univ ∧ p.2 ∈ directionShell C v₀ p.1 := by
        intro p
        simp [directedFirstShell, directionShell]
      simpa using
        (Finset.sum_finset_product' (directedFirstShell C v₀) Finset.univ
          (directionShell C v₀) hfib (f := fun i _ => f i))
    _ = ∑ i, #(directionShell C v₀ i) * f i := by
      apply Finset.sum_congr rfl
      intro i hi
      exact Finset.sum_const_nat fun _ _ => rfl

/-- The exact Hamming-shell incidence inequality.

If every selected word has at least `h` selected Hamming neighbors, the
weighted first-shell demand is at most twice the selected distance-two shell.
This is the graph-theoretic premise consumed by
`card_ge_of_shell_incidence`. -/
theorem hamming_shell_incidence
    (C : Finset (∀ i, β i)) (v₀ : ∀ i, β i) (h : ℕ)
    (hdegree : ∀ u ∈ C, h ≤ #(internalNeighbors C u)) :
    (∑ i, #(directionShell C v₀ i) *
      (h - #(directionShell C v₀ i))) ≤
      2 * #(distanceShell C v₀ 2) := by
  classical
  let L := directedFirstShell C v₀
  let B := distanceShell C v₀ 2
  let R : (ι × (∀ i, β i)) → (∀ i, β i) → Prop :=
    fun p w => hammingDist p.2 w = 1
  calc
    (∑ i, #(directionShell C v₀ i) *
        (h - #(directionShell C v₀ i))) =
        ∑ p ∈ L, (h - #(directionShell C v₀ p.1)) := by
      symm
      simpa [L] using sum_directedFirstShell C v₀
        (fun i => h - #(directionShell C v₀ i))
    _ ≤ ∑ p ∈ L, #(B.bipartiteAbove R p) := by
      refine Finset.sum_le_sum fun p hp => ?_
      have hpL := Finset.mem_filter.mp hp
      have hpC : p.2 ∈ C := (Finset.mem_product.mp hpL.1).2
      simpa [B, R, Finset.bipartiteAbove] using
        threshold_sub_direction_card_le_second_neighbors
        C v₀ p.2 p.1 h (Finset.mem_filter.mpr ⟨hpC, hpL.2⟩)
        (hdegree p.2 hpC)
    _ = ∑ w ∈ B, #(L.bipartiteBelow R w) := by
      exact Finset.sum_card_bipartiteAbove_eq_sum_card_bipartiteBelow R
    _ ≤ ∑ w ∈ B, 2 := by
      refine Finset.sum_le_sum fun w hw => ?_
      simpa [L, B, R] using card_directedFirstShell_neighbors_le_two C v₀ w hw
    _ = 2 * #B := by simp [Nat.mul_comm]
    _ = 2 * #(distanceShell C v₀ 2) := by rfl

#print axioms card_directedFirstShell_neighbors_le_two
#print axioms card_internalNeighbors_le_direction_add_second
#print axioms hamming_shell_incidence

end MajorityCHamming
