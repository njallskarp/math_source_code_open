import Mathlib.Combinatorics.SimpleGraph.Clique

namespace MPLCOrder4

open SimpleGraph

set_option maxRecDepth 100000

/-- A layer-row-column-symbol entry of an order-four partial Latin cube. -/
abbrev Word4 := Fin 4 × Fin 4 × Fin 4 × Fin 4

/-- Hamming distance on the four coordinates of an order-four entry. -/
def hammingDist (x y : Word4) : Nat :=
  (if x.1 = y.1 then 0 else 1) +
  (if x.2.1 = y.2.1 then 0 else 1) +
  (if x.2.2.1 = y.2.2.1 then 0 else 1) +
  (if x.2.2.2 = y.2.2.2 then 0 else 1)

@[simp] theorem hammingDist_self (x : Word4) : hammingDist x x = 0 := by
  simp [hammingDist]

theorem hammingDist_comm (x y : Word4) : hammingDist x y = hammingDist y x := by
  simp only [hammingDist, eq_comm]

theorem hammingDist_eq_zero_iff (x y : Word4) : hammingDist x y = 0 ↔ x = y := by
  rcases x with ⟨a, b, c, d⟩
  rcases y with ⟨a', b', c', d'⟩
  simp [hammingDist, and_assoc]

theorem hammingDist_pos_of_ne {x y : Word4} (hxy : x ≠ y) :
    0 < hammingDist x y := by
  exact Nat.pos_of_ne_zero fun h => hxy ((hammingDist_eq_zero_iff x y).mp h)

/-- The Hamming graph `H(4,4)`: two words are adjacent exactly when they
differ in one coordinate. -/
def hammingGraph : SimpleGraph Word4 where
  Adj x y := hammingDist x y = 1
  symm.symm x y := by
    intro h
    simpa [hammingDist_comm] using h
  loopless.irrefl x := by
    intro h
    simp at h

instance : DecidableRel hammingGraph.Adj := by
  intro x y
  simp only [hammingGraph]
  infer_instance

/-- The coordinate form of a partial Latin cube: distinct chosen entries
agree in at most two coordinates. -/
def IsPartialLatinCube (C : Set Word4) : Prop :=
  ∀ ⦃x : Word4⦄, x ∈ C → ∀ ⦃y : Word4⦄, y ∈ C →
    x ≠ y → 2 ≤ hammingDist x y

/-- A partial Latin cube is maximal when every word is selected or is at
Hamming distance one from a selected word. -/
def IsMaximalPartialLatinCube (C : Set Word4) : Prop :=
  IsPartialLatinCube C ∧
    ∀ w, ∃ c ∈ C, hammingDist w c ≤ 1

/-- The order-four spectrum predicate corresponding to membership in
`ML(3,4)`: a duplicate-free list of `k` entries whose underlying set is a
maximal partial Latin cube. -/
def InOrderFourSpectrum (k : Nat) : Prop :=
  ∃ C : List Word4, C.Nodup ∧ C.length = k ∧
    IsMaximalPartialLatinCube {x | x ∈ C}

/-- Closed-neighborhood domination, stated for any simple graph. -/
def ClosedDominates {V : Type*} (G : SimpleGraph V) (C : Set V) : Prop :=
  ∀ w, w ∈ C ∨ ∃ c ∈ C, G.Adj w c

/-- The coordinate definition of a partial Latin cube is exactly independence
in the Hamming graph. -/
theorem isPartialLatinCube_iff_isIndepSet (C : Set Word4) :
    IsPartialLatinCube C ↔ hammingGraph.IsIndepSet C := by
  rw [SimpleGraph.isIndepSet_iff]
  constructor
  · intro h x hx y hy hxy hadj
    have hdist := h hx hy hxy
    change hammingDist x y = 1 at hadj
    omega
  · intro h x hx y hy hxy
    have hnot := h hx hy hxy
    change hammingDist x y ≠ 1 at hnot
    have hpos := hammingDist_pos_of_ne hxy
    omega

/-- Maximal partial Latin cubes are precisely independent dominating sets in
the Hamming graph. -/
theorem isMaximalPartialLatinCube_iff_independentDominating (C : Set Word4) :
    IsMaximalPartialLatinCube C ↔
      hammingGraph.IsIndepSet C ∧ ClosedDominates hammingGraph C := by
  rw [IsMaximalPartialLatinCube, isPartialLatinCube_iff_isIndepSet]
  apply and_congr Iff.rfl
  constructor
  · intro h w
    obtain ⟨c, hc, hdist⟩ := h w
    by_cases hwc : w = c
    · exact Or.inl (hwc ▸ hc)
    · right
      refine ⟨c, hc, ?_⟩
      change hammingDist w c = 1
      have hpos := hammingDist_pos_of_ne hwc
      omega
  · intro h w
    rcases h w with hw | ⟨c, hc, hwc⟩
    · exact ⟨w, hw, by simp⟩
    · exact ⟨c, hc, by simpa [hammingGraph] using hwc.le⟩

/-- The closed-neighborhood formulation is equivalent to the literal
"no absent word can be added" maximality condition. -/
theorem isMaximalPartialLatinCube_iff_no_addable (C : Set Word4) :
    IsMaximalPartialLatinCube C ↔
      IsPartialLatinCube C ∧
        ∀ w, w ∉ C → ¬IsPartialLatinCube (insert w C) := by
  constructor
  · rintro ⟨hpartial, hcover⟩
    refine ⟨hpartial, ?_⟩
    intro w hw hinsert
    obtain ⟨c, hc, hdist⟩ := hcover w
    have hwc : w ≠ c := fun h => hw (h ▸ hc)
    have htwo := hinsert (Set.mem_insert w C) (Set.mem_insert_of_mem w hc) hwc
    omega
  · rintro ⟨hpartial, hnoadd⟩
    refine ⟨hpartial, ?_⟩
    intro w
    by_cases hw : w ∈ C
    · exact ⟨w, hw, by simp⟩
    · by_contra hnot
      push Not at hnot
      apply hnoadd w hw
      intro x hx y hy hxy
      rw [Set.mem_insert_iff] at hx hy
      rcases hx with rfl | hx
      · rcases hy with rfl | hy
        · exact False.elim (hxy rfl)
        · exact hnot y hy
      · rcases hy with rfl | hy
        · rw [hammingDist_comm]
          exact hnot x hx
        · exact hpartial hx hy hxy

/-- All order-four symbols, in their canonical finite order. -/
def alphabet4 : List (Fin 4) := List.ofFn id

theorem mem_alphabet4 (a : Fin 4) : a ∈ alphabet4 := by
  rw [alphabet4, List.mem_ofFn']
  exact ⟨a, rfl⟩

/-- The complete list of the `4^4 = 256` order-four words. -/
def universe4 : List Word4 :=
  alphabet4.flatMap fun a =>
    alphabet4.flatMap fun b =>
      alphabet4.flatMap fun c =>
        alphabet4.map fun d => (a, b, c, d)

theorem mem_universe4 (w : Word4) : w ∈ universe4 := by
  rcases w with ⟨a, b, c, d⟩
  simp only [universe4, List.mem_flatMap, List.mem_map]
  exact ⟨a, mem_alphabet4 a, b, mem_alphabet4 b, c, mem_alphabet4 c,
    d, mem_alphabet4 d, rfl⟩

/-- A computable independence check for a listed partial Latin cube. -/
def partialCheck (C : List Word4) : Bool :=
  C.all fun x => C.all fun y =>
    decide (x = y) || decide (2 ≤ hammingDist x y)

/-- A computable closed-radius-one covering check. -/
def coverCheck (C : List Word4) : Bool :=
  universe4.all fun w => C.any fun c => decide (hammingDist w c ≤ 1)

/-- The Boolean checker exactly reflects the mathematical partial-cube
condition. -/
theorem partialCheck_eq_true_iff (C : List Word4) :
    partialCheck C = true ↔ IsPartialLatinCube {x | x ∈ C} := by
  simp only [partialCheck, List.all_eq_true, Bool.or_eq_true,
    decide_eq_true_eq, IsPartialLatinCube, Set.mem_ofPred_eq]
  constructor
  · intro h x hx y hy hxy
    exact (h x hx y hy).resolve_left hxy
  · intro h x hx y hy
    by_cases hxy : x = y
    · exact Or.inl hxy
    · exact Or.inr (h hx hy hxy)

/-- The Boolean checker exactly reflects closed-radius-one domination. -/
theorem coverCheck_eq_true_iff (C : List Word4) :
    coverCheck C = true ↔
      ∀ w, ∃ c ∈ ({x | x ∈ C} : Set Word4), hammingDist w c ≤ 1 := by
  simp only [coverCheck, List.all_eq_true, List.any_eq_true,
    decide_eq_true_eq, Set.mem_ofPred_eq]
  constructor
  · intro h w
    exact h w (mem_universe4 w)
  · intro h w _
    exact h w

/-- The independently reviewed 30-entry witness. -/
def certificate30 : List Word4 := [
  (0, 0, 0, 0),
  (0, 1, 1, 2),
  (0, 1, 3, 0),
  (0, 2, 2, 1),
  (0, 3, 0, 3),
  (0, 3, 1, 0),
  (0, 3, 3, 2),
  (1, 0, 1, 3),
  (1, 0, 2, 2),
  (1, 1, 0, 1),
  (1, 1, 2, 3),
  (1, 2, 0, 2),
  (1, 2, 1, 1),
  (1, 3, 3, 0),
  (2, 0, 2, 3),
  (2, 0, 3, 1),
  (2, 1, 1, 0),
  (2, 1, 2, 2),
  (2, 2, 3, 3),
  (2, 3, 0, 0),
  (2, 3, 1, 2),
  (3, 0, 0, 2),
  (3, 0, 1, 1),
  (3, 0, 3, 3),
  (3, 1, 0, 3),
  (3, 1, 3, 2),
  (3, 2, 0, 1),
  (3, 2, 1, 3),
  (3, 2, 2, 0),
  (3, 3, 2, 1)
]

theorem certificate30_length : certificate30.length = 30 := by decide

theorem certificate30_nodup : certificate30.Nodup := by decide

theorem certificate30_checks :
    partialCheck certificate30 = true ∧ coverCheck certificate30 = true := by
  decide

theorem certificate30_isMaximal :
    IsMaximalPartialLatinCube {x | x ∈ certificate30} := by
  rw [IsMaximalPartialLatinCube, ← partialCheck_eq_true_iff,
    ← coverCheck_eq_true_iff]
  exact certificate30_checks

theorem certificate30_independentDominating :
    hammingGraph.IsIndepSet {x | x ∈ certificate30} ∧
      ClosedDominates hammingGraph {x | x ∈ certificate30} :=
  (isMaximalPartialLatinCube_iff_independentDominating _).mp
    certificate30_isMaximal

theorem certificate30_no_addable :
    ∀ w, w ∉ ({x | x ∈ certificate30} : Set Word4) →
      ¬IsPartialLatinCube (insert w {x | x ∈ certificate30}) :=
  ((isMaximalPartialLatinCube_iff_no_addable _).mp
    certificate30_isMaximal).2

/-- The formal endpoint: `30 ∈ ML(3,4)`. -/
theorem thirty_mem_orderFourSpectrum : InOrderFourSpectrum 30 :=
  ⟨certificate30, certificate30_nodup, certificate30_length,
    certificate30_isMaximal⟩

#print axioms certificate30_length
#print axioms certificate30_nodup
#print axioms hammingDist_eq_zero_iff
#print axioms isPartialLatinCube_iff_isIndepSet
#print axioms isMaximalPartialLatinCube_iff_independentDominating
#print axioms isMaximalPartialLatinCube_iff_no_addable
#print axioms partialCheck_eq_true_iff
#print axioms coverCheck_eq_true_iff
#print axioms certificate30_checks
#print axioms certificate30_isMaximal
#print axioms certificate30_independentDominating
#print axioms certificate30_no_addable
#print axioms thirty_mem_orderFourSpectrum

end MPLCOrder4
