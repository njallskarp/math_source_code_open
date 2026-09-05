import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Finset.Sum
import Mathlib.Data.Finset.Interval
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

/-!
# Proof-carrying capacity bounds for Gallai block spectra

This file isolates the finite packing bridge used after Gallai's low-vertex
theorem.  A clique block with increment `u = |Q| - 1` contributes
`u * (u + 1) / 2` edges.  An odd cycle with even increment `u >= 4`
compresses exactly to one increment-2 atom and `u - 2` increment-1 atoms:
the units and edge contribution are both preserved.  Consequently all block
spectra can be audited as finite multisets of positive clique atoms.

The central theorem accepts a small Bellman supersolution as a certificate and
proves an upper bound for every finite packing.  The numerical corollaries are
the two exact gaps needed downstream of the accepted Albertson separator
profiles.  Gallai's theorem and the graph-to-block decomposition remain
explicit external interfaces.
-/

open scoped BigOperators

namespace AlbertsonGallaiBlockSpectrum

/-- Edge contribution of a clique block whose order-minus-one is `u`. -/
def cliqueEdges (u : ℕ) : ℕ := u * (u + 1) / 2

theorem cliqueEdges_mono : Monotone cliqueEdges := by
  intro a b hab
  exact Nat.div_le_div_right (Nat.mul_le_mul hab (Nat.add_le_add_right hab 1))

/-- An odd cycle of order `u+1` has the same units and edge contribution as
one clique atom of increment two and `u-2` atoms of increment one. -/
theorem oddCycle_compression (u : ℕ) (hu : 2 ≤ u) :
    u = 2 + (u - 2) ∧
      u + 1 = cliqueEdges 2 + (u - 2) * cliqueEdges 1 := by
  constructor
  · omega
  · norm_num [cliqueEdges]
    omega

/-- A compact proof-carrying upper-bound table. -/
structure CapacityCertificate where
  values : List ℕ
  deriving DecidableEq, Repr

namespace CapacityCertificate

def value (cert : CapacityCertificate) (budget : ℕ) : ℕ :=
  cert.values.getD budget 0

/-- Executable local Bellman conditions sufficient for the table to
upper-bound every packing with parts at most `cap` and total units at most
`maxBudget`. -/
def checkValid (cert : CapacityCertificate) (cap maxBudget : ℕ) : Bool :=
  (cert.values.length == maxBudget + 1) && (cert.value 0 == 0) &&
    (List.range' 1 maxBudget).all fun budget ↦
      (List.range' 1 (min cap budget)).all fun part ↦
        decide (cliqueEdges part + cert.value (budget - part) ≤ cert.value budget)

def IsValid (cert : CapacityCertificate) (cap maxBudget : ℕ) : Prop :=
  cert.checkValid cap maxBudget = true

theorem step_of_valid {cert : CapacityCertificate} {cap maxBudget budget part : ℕ}
    (hcert : cert.IsValid cap maxBudget)
    (hbudget : budget ∈ Finset.Icc 1 maxBudget)
    (hpart : part ∈ Finset.Icc 1 (min cap budget)) :
    cliqueEdges part + cert.value (budget - part) ≤ cert.value budget := by
  simp only [IsValid, checkValid, Bool.and_eq_true, beq_iff_eq,
    List.all_eq_true, decide_eq_true_eq] at hcert
  rcases Finset.mem_Icc.mp hbudget with ⟨hbudgetPos, hbudgetMax⟩
  rcases Finset.mem_Icc.mp hpart with ⟨hpartPos, hpartMax⟩
  have hbudgetMem : budget ∈ List.range' 1 maxBudget := by
    rw [List.mem_range']
    exact ⟨budget - 1, by omega, by omega⟩
  have hpartMem : part ∈ List.range' 1 (min cap budget) := by
    rw [List.mem_range']
    exact ⟨part - 1, by omega, by omega⟩
  exact hcert.2 budget hbudgetMem part hpartMem

end CapacityCertificate

/-- A valid Bellman certificate bounds every finite packing, independently of
how the packing was generated. -/
theorem sum_cliqueEdges_le_certificate
    {ι : Type*} [DecidableEq ι]
    (cert : CapacityCertificate) (cap maxBudget : ℕ)
    (hcert : cert.IsValid cap maxBudget)
    (S : Finset ι) (units : ι → ℕ) (budget : ℕ)
    (hbudget : budget ≤ maxBudget)
    (hpos : ∀ i ∈ S, 0 < units i)
    (hcap : ∀ i ∈ S, units i ≤ cap)
    (hsum : ∑ i ∈ S, units i ≤ budget) :
    ∑ i ∈ S, cliqueEdges (units i) ≤ cert.value budget := by
  induction S using Finset.induction_on generalizing budget with
  | empty => simp
  | @insert i S hi ih =>
      rw [Finset.sum_insert hi] at hsum ⊢
      have hui_pos : 0 < units i := hpos i (by simp)
      have hui_cap : units i ≤ cap := hcap i (by simp)
      have hui_budget : units i ≤ budget := by omega
      have hbudget_pos : 1 ≤ budget := by omega
      have htail : ∑ j ∈ S, units j ≤ budget - units i := by omega
      have htail_budget : budget - units i ≤ maxBudget := by omega
      have htail_pos : ∀ j ∈ S, 0 < units j := by
        intro j hj
        exact hpos j (by simp [hj])
      have htail_cap : ∀ j ∈ S, units j ≤ cap := by
        intro j hj
        exact hcap j (by simp [hj])
      have hih := ih (budget - units i)
        htail_budget htail_pos htail_cap htail
      have hstep := CapacityCertificate.step_of_valid hcert
        (Finset.mem_Icc.mpr ⟨hbudget_pos, hbudget⟩)
        (Finset.mem_Icc.mpr ⟨hui_pos, le_min hui_cap hui_budget⟩)
      exact (Nat.add_le_add_left hih _).trans hstep

/-- Closed-form table used only to manufacture short certificates.  Its
validity is checked from the Bellman conditions, not trusted as a theorem. -/
def greedyValue (cap budget : ℕ) : ℕ :=
  cliqueEdges cap * (budget / cap) + cliqueEdges (budget % cap)

def greedyCertificate (cap maxBudget : ℕ) : CapacityCertificate where
  values := (List.range (maxBudget + 1)).map (greedyValue cap)

def cap23 : CapacityCertificate := greedyCertificate 23 49
def cap22 : CapacityCertificate := greedyCertificate 22 24
def cap21 : CapacityCertificate := greedyCertificate 21 23

theorem cap23_valid : cap23.IsValid 23 49 := by
  change cap23.checkValid 23 49 = true
  decide
theorem cap22_valid : cap22.IsValid 22 24 := by
  change cap22.checkValid 22 24 = true
  decide
theorem cap21_valid : cap21.IsValid 21 23 := by
  change cap21.checkValid 21 23 = true
  decide

theorem cap23_value_25 : cap23.value 25 = 279 := by decide
theorem cap23_value_49 : cap23.value 49 = 558 := by decide
theorem cap23_value_48 : cap23.value 48 = 555 := by decide
theorem cap22_value_24 : cap22.value 24 = 256 := by decide
theorem cap21_value_23 : cap21.value 23 = 234 := by decide

/-- No two distinct atoms have increment `special`. -/
def AtMostOnePart {ι : Type*} (S : Finset ι) (units : ι → ℕ)
    (special : ℕ) : Prop :=
  ∀ i ∈ S, ∀ j ∈ S, units i = special → units j = special → i = j

private theorem term_le_sum_erase
    {ι : Type*} [DecidableEq ι] {S : Finset ι} {f : ι → ℕ}
    {i j : ι} (hj : j ∈ S) (hij : j ≠ i) :
    f j ≤ ∑ k ∈ S.erase i, f k := by
  exact Finset.single_le_sum (fun k hk ↦ Nat.zero_le (f k))
    (Finset.mem_erase.mpr ⟨hij, hj⟩)

private theorem two_terms_le_sum
    {ι : Type*} [DecidableEq ι] {S : Finset ι} {f : ι → ℕ}
    {i j : ι} (hi : i ∈ S) (hj : j ∈ S) (hij : j ≠ i) :
    f i + f j ≤ ∑ k ∈ S, f k := by
  have hjle := term_le_sum_erase (f := f) hj hij
  have hsplit := Finset.sum_erase_add (s := S) (f := f) hi
  omega

/-- The height-2637 packing kernel in parameterized finite-packing form:
with total increment at most 50, a unique increment-25 atom and no
increment-24 atom force capacity at most 604. -/
theorem capacity_of_unique_25_without_24
    {ι : Type*} [DecidableEq ι]
    (S : Finset ι) (units : ι → ℕ)
    (hpos : ∀ i ∈ S, 0 < units i)
    (hmax : ∀ i ∈ S, units i ≤ 25)
    (hsum : ∑ i ∈ S, units i ≤ 50)
    (hunique : AtMostOnePart S units 25)
    (h25 : ∃ i ∈ S, units i = 25)
    (hno24 : ∀ i ∈ S, units i ≠ 24) :
    ∑ i ∈ S, cliqueEdges (units i) ≤ 604 := by
  obtain ⟨i, hi, hui⟩ := h25
  let T := S.erase i
  have hTsum : ∑ j ∈ T, units j ≤ 25 := by
    have hsplit := Finset.sum_erase_add (s := S) (f := units) hi
    dsimp [T]
    omega
  have hTpos : ∀ j ∈ T, 0 < units j := by
    intro j hj
    exact hpos j (Finset.mem_of_mem_erase hj)
  have hTcap : ∀ j ∈ T, units j ≤ 23 := by
    intro j hj
    have hjS := Finset.mem_of_mem_erase hj
    have hji : j ≠ i := (Finset.mem_erase.mp hj).1
    have hne25 : units j ≠ 25 := by
      intro h25j
      exact hji (hunique j hjS i hi h25j hui)
    have := hmax j hjS
    have := hno24 j hjS
    omega
  have htail := sum_cliqueEdges_le_certificate cap23 23 49 cap23_valid
    T units 25 (by norm_num) hTpos hTcap hTsum
  rw [cap23_value_25] at htail
  dsimp [T] at htail
  have hsplit := Finset.sum_erase_add (s := S)
    (f := fun j ↦ cliqueEdges (units j)) hi
  have hiEdge : cliqueEdges (units i) = 325 := by
    norm_num [hui, cliqueEdges]
  omega

/-- Exact relaxed spectrum gap on 50 vertices: with total block increment at
most 49 and clique atoms at most 25, the edge sum is at most 581 or at least
600.  Notice that no uniqueness assumption on increment 25 is needed: a
second large atom already lands above the gap. -/
theorem spectrum_gap_budget49
    {ι : Type*} [DecidableEq ι]
    (S : Finset ι) (units : ι → ℕ)
    (hpos : ∀ i ∈ S, 0 < units i)
    (hmax : ∀ i ∈ S, units i ≤ 25)
    (hsum : ∑ i ∈ S, units i ≤ 49) :
    (∑ i ∈ S, cliqueEdges (units i) ≤ 581) ∨
      600 ≤ ∑ i ∈ S, cliqueEdges (units i) := by
  by_cases h25 : ∃ i ∈ S, units i = 25
  · obtain ⟨i, hi, hui⟩ := h25
    let T := S.erase i
    have hTsum : ∑ j ∈ T, units j ≤ 24 := by
      have hsplit := Finset.sum_erase_add (s := S) (f := units) hi
      dsimp [T]
      omega
    have hTpos : ∀ j ∈ T, 0 < units j := by
      intro j hj
      exact hpos j (Finset.mem_of_mem_erase hj)
    by_cases hlarge : ∃ j ∈ T, 23 ≤ units j
    · right
      obtain ⟨j, hj, hju⟩ := hlarge
      have hjS := Finset.mem_of_mem_erase hj
      have hji : j ≠ i := (Finset.mem_erase.mp hj).1
      have hjedge : 276 ≤ cliqueEdges (units j) :=
        cliqueEdges_mono hju
      have htwo := two_terms_le_sum
        (f := fun k ↦ cliqueEdges (units k)) hi hjS hji
      have hiEdge : cliqueEdges (units i) = 325 := by
        norm_num [hui, cliqueEdges]
      omega
    · left
      have hTcap : ∀ j ∈ T, units j ≤ 22 := by
        intro j hj
        by_contra hnot
        exact hlarge ⟨j, hj, by omega⟩
      have htail := sum_cliqueEdges_le_certificate cap22 22 24 cap22_valid
        T units 24 (by norm_num) hTpos hTcap hTsum
      rw [cap22_value_24] at htail
      dsimp [T] at htail
      have hsplit := Finset.sum_erase_add (s := S)
        (f := fun j ↦ cliqueEdges (units j)) hi
      have hiEdge : cliqueEdges (units i) = 325 := by
        norm_num [hui, cliqueEdges]
      omega
  · by_cases h24 : ∃ i ∈ S, units i = 24
    · obtain ⟨i, hi, hui⟩ := h24
      let T := S.erase i
      have hTsum : ∑ j ∈ T, units j ≤ 25 := by
        have hsplit := Finset.sum_erase_add (s := S) (f := units) hi
        dsimp [T]
        omega
      have hTpos : ∀ j ∈ T, 0 < units j := by
        intro j hj
        exact hpos j (Finset.mem_of_mem_erase hj)
      by_cases hsecond : ∃ j ∈ T, 24 ≤ units j
      · right
        obtain ⟨j, hj, hju⟩ := hsecond
        have hjS := Finset.mem_of_mem_erase hj
        have hji : j ≠ i := (Finset.mem_erase.mp hj).1
        have hjedge : 300 ≤ cliqueEdges (units j) :=
          cliqueEdges_mono hju
        have htwo := two_terms_le_sum
          (f := fun k ↦ cliqueEdges (units k)) hi hjS hji
        have hiEdge : cliqueEdges (units i) = 300 := by
          norm_num [hui, cliqueEdges]
        omega
      · left
        have hTcap : ∀ j ∈ T, units j ≤ 23 := by
          intro j hj
          by_contra hnot
          exact hsecond ⟨j, hj, by omega⟩
        have htail := sum_cliqueEdges_le_certificate cap23 23 49 cap23_valid
          T units 25 (by norm_num) hTpos hTcap hTsum
        rw [cap23_value_25] at htail
        dsimp [T] at htail
        have hsplit := Finset.sum_erase_add (s := S)
          (f := fun j ↦ cliqueEdges (units j)) hi
        have hiEdge : cliqueEdges (units i) = 300 := by
          norm_num [hui, cliqueEdges]
        omega
    · left
      have hcap : ∀ i ∈ S, units i ≤ 23 := by
        intro i hi
        have himax := hmax i hi
        have hne25 : units i ≠ 25 := by
          intro heq
          exact h25 ⟨i, hi, heq⟩
        have hne24 : units i ≠ 24 := by
          intro heq
          exact h24 ⟨i, hi, heq⟩
        omega
      have hall := sum_cliqueEdges_le_certificate cap23 23 49 cap23_valid
        S units 49 (by norm_num) hpos hcap hsum
      rw [cap23_value_49] at hall
      exact hall.trans (by norm_num)

/-- Exact relaxed spectrum gap on 49 vertices. -/
theorem spectrum_gap_budget48
    {ι : Type*} [DecidableEq ι]
    (S : Finset ι) (units : ι → ℕ)
    (hpos : ∀ i ∈ S, 0 < units i)
    (hmax : ∀ i ∈ S, units i ≤ 25)
    (hsum : ∑ i ∈ S, units i ≤ 48) :
    (∑ i ∈ S, cliqueEdges (units i) ≤ 559) ∨
      576 ≤ ∑ i ∈ S, cliqueEdges (units i) := by
  by_cases h25 : ∃ i ∈ S, units i = 25
  · obtain ⟨i, hi, hui⟩ := h25
    let T := S.erase i
    have hTsum : ∑ j ∈ T, units j ≤ 23 := by
      have hsplit := Finset.sum_erase_add (s := S) (f := units) hi
      dsimp [T]
      omega
    have hTpos : ∀ j ∈ T, 0 < units j := by
      intro j hj
      exact hpos j (Finset.mem_of_mem_erase hj)
    by_cases hlarge : ∃ j ∈ T, 22 ≤ units j
    · right
      obtain ⟨j, hj, hju⟩ := hlarge
      have hjS := Finset.mem_of_mem_erase hj
      have hji : j ≠ i := (Finset.mem_erase.mp hj).1
      have hjedge : 253 ≤ cliqueEdges (units j) :=
        cliqueEdges_mono hju
      have htwo := two_terms_le_sum
        (f := fun k ↦ cliqueEdges (units k)) hi hjS hji
      have hiEdge : cliqueEdges (units i) = 325 := by
        norm_num [hui, cliqueEdges]
      omega
    · left
      have hTcap : ∀ j ∈ T, units j ≤ 21 := by
        intro j hj
        by_contra hnot
        exact hlarge ⟨j, hj, by omega⟩
      have htail := sum_cliqueEdges_le_certificate cap21 21 23 cap21_valid
        T units 23 (by norm_num) hTpos hTcap hTsum
      rw [cap21_value_23] at htail
      dsimp [T] at htail
      have hsplit := Finset.sum_erase_add (s := S)
        (f := fun j ↦ cliqueEdges (units j)) hi
      have hiEdge : cliqueEdges (units i) = 325 := by
        norm_num [hui, cliqueEdges]
      omega
  · by_cases h24 : ∃ i ∈ S, units i = 24
    · obtain ⟨i, hi, hui⟩ := h24
      let T := S.erase i
      have hTsum : ∑ j ∈ T, units j ≤ 24 := by
        have hsplit := Finset.sum_erase_add (s := S) (f := units) hi
        dsimp [T]
        omega
      have hTpos : ∀ j ∈ T, 0 < units j := by
        intro j hj
        exact hpos j (Finset.mem_of_mem_erase hj)
      by_cases hlarge : ∃ j ∈ T, 23 ≤ units j
      · right
        obtain ⟨j, hj, hju⟩ := hlarge
        have hjS := Finset.mem_of_mem_erase hj
        have hji : j ≠ i := (Finset.mem_erase.mp hj).1
        have hjedge : 276 ≤ cliqueEdges (units j) :=
          cliqueEdges_mono hju
        have htwo := two_terms_le_sum
          (f := fun k ↦ cliqueEdges (units k)) hi hjS hji
        have hiEdge : cliqueEdges (units i) = 300 := by
          norm_num [hui, cliqueEdges]
        omega
      · left
        have hTcap : ∀ j ∈ T, units j ≤ 22 := by
          intro j hj
          by_contra hnot
          exact hlarge ⟨j, hj, by omega⟩
        have htail := sum_cliqueEdges_le_certificate cap22 22 24 cap22_valid
          T units 24 (by norm_num) hTpos hTcap hTsum
        rw [cap22_value_24] at htail
        dsimp [T] at htail
        have hsplit := Finset.sum_erase_add (s := S)
          (f := fun j ↦ cliqueEdges (units j)) hi
        have hiEdge : cliqueEdges (units i) = 300 := by
          norm_num [hui, cliqueEdges]
        omega
    · left
      have hcap : ∀ i ∈ S, units i ≤ 23 := by
        intro i hi
        have himax := hmax i hi
        have hne25 : units i ≠ 25 := by
          intro heq
          exact h25 ⟨i, hi, heq⟩
        have hne24 : units i ≠ 24 := by
          intro heq
          exact h24 ⟨i, hi, heq⟩
        omega
      have hall := sum_cliqueEdges_le_certificate cap23 23 49 cap23_valid
        S units 48 (by norm_num) hpos hcap hsum
      rw [cap23_value_48] at hall
      exact hall.trans (by norm_num)

/-- The exact height-2637 numerical bridge.  A packing with the unique
increment-25 atom forced upstream cannot have edge sum in the whole interval
`[609, 615]`: without an increment-24 atom the Bellman certificate gives 604,
while with one the two large atoms alone give 625. -/
theorem no_spectrum_budget50_between_609_615_with_unique25
    {ι : Type*} [DecidableEq ι]
    (S : Finset ι) (units : ι → ℕ)
    (hpos : ∀ i ∈ S, 0 < units i)
    (hmax : ∀ i ∈ S, units i ≤ 25)
    (hsum : ∑ i ∈ S, units i ≤ 50)
    (hunique : AtMostOnePart S units 25)
    (h25 : ∃ i ∈ S, units i = 25)
    (hedgeLow : 609 ≤ ∑ i ∈ S, cliqueEdges (units i))
    (hedgeHigh : ∑ i ∈ S, cliqueEdges (units i) ≤ 615) : False := by
  by_cases h24 : ∃ j ∈ S, units j = 24
  · obtain ⟨i, hi, hui⟩ := h25
    obtain ⟨j, hj, huj⟩ := h24
    have hji : j ≠ i := by
      intro hEq
      subst j
      omega
    have htwo := two_terms_le_sum
      (f := fun k ↦ cliqueEdges (units k)) hi hj hji
    have hiEdge : cliqueEdges (units i) = 325 := by
      norm_num [hui, cliqueEdges]
    have hjEdge : cliqueEdges (units j) = 300 := by
      norm_num [huj, cliqueEdges]
    omega
  · have hcap := capacity_of_unique_25_without_24
      S units hpos hmax hsum hunique h25 (by
        intro i hi hEq
        exact h24 ⟨i, hi, hEq⟩)
    omega

/-- The 50-low-vertex gap used at height 2671 excludes precisely the imported
edge interval `[582, 591]`. -/
theorem no_spectrum_budget49_between_582_591
    {ι : Type*} [DecidableEq ι]
    (S : Finset ι) (units : ι → ℕ)
    (hpos : ∀ i ∈ S, 0 < units i)
    (hmax : ∀ i ∈ S, units i ≤ 25)
    (hsum : ∑ i ∈ S, units i ≤ 49)
    (hedgeLow : 582 ≤ ∑ i ∈ S, cliqueEdges (units i))
    (hedgeHigh : ∑ i ∈ S, cliqueEdges (units i) ≤ 591) : False := by
  rcases spectrum_gap_budget49 S units hpos hmax hsum with hlow | hhigh
  · omega
  · omega

/-- The 49-low-vertex gap used at height 2671 excludes precisely the imported
edge interval `[560, 569]`. -/
theorem no_spectrum_budget48_between_560_569
    {ι : Type*} [DecidableEq ι]
    (S : Finset ι) (units : ι → ℕ)
    (hpos : ∀ i ∈ S, 0 < units i)
    (hmax : ∀ i ∈ S, units i ≤ 25)
    (hsum : ∑ i ∈ S, units i ≤ 48)
    (hedgeLow : 560 ≤ ∑ i ∈ S, cliqueEdges (units i))
    (hedgeHigh : ∑ i ∈ S, cliqueEdges (units i) ≤ 569) : False := by
  rcases spectrum_gap_budget48 S units hpos hmax hsum with hlow | hhigh
  · omega
  · omega

end AlbertsonGallaiBlockSpectrum

#print axioms AlbertsonGallaiBlockSpectrum.oddCycle_compression
#print axioms AlbertsonGallaiBlockSpectrum.sum_cliqueEdges_le_certificate
#print axioms AlbertsonGallaiBlockSpectrum.cap23_valid
#print axioms AlbertsonGallaiBlockSpectrum.capacity_of_unique_25_without_24
#print axioms AlbertsonGallaiBlockSpectrum.spectrum_gap_budget49
#print axioms AlbertsonGallaiBlockSpectrum.spectrum_gap_budget48
#print axioms AlbertsonGallaiBlockSpectrum.no_spectrum_budget50_between_609_615_with_unique25
#print axioms AlbertsonGallaiBlockSpectrum.no_spectrum_budget49_between_582_591
#print axioms AlbertsonGallaiBlockSpectrum.no_spectrum_budget48_between_560_569
