import Mathlib.Data.List.Sort

/-!
# Insertion-sort shifts equal inversions

This file formalizes the deterministic algorithmic bridge behind the
categorical insertion-sort expectation formulas.  Equal keys are never
shifted: Mathlib's stable `List.insertionSort (· ≤ ·)` stops before them.
-/

namespace InsertionSortInversion

/-- Number of later entries strictly below each entry of a word. -/
def inversionCount {α : Type*} [LinearOrder α] : List α → ℕ
  | [] => 0
  | a :: l => l.countP (fun b => decide (b < a)) + inversionCount l

/-- A weakly increasing word has no inversions, including when keys repeat. -/
theorem inversionCount_eq_zero_of_pairwise {α : Type*} [LinearOrder α]
    {l : List α} (hl : l.Pairwise (· ≤ ·)) : inversionCount l = 0 := by
  induction l with
  | nil => rfl
  | cons a l ih =>
      rw [List.pairwise_cons] at hl
      rcases hl with ⟨hal, hl⟩
      have hz : l.countP (fun b => decide (b < a)) = 0 :=
        List.countP_eq_zero.mpr (by
          intro b hb
          simp only [decide_eq_true_eq, not_lt]
          exact hal b hb)
      simp [inversionCount, hz, ih hl]

/-- Swapping one strictly inverted adjacent pair removes exactly one inversion,
independently of the surrounding prefix and suffix. -/
theorem inversionCount_adjacent_swap {α : Type*} [LinearOrder α]
    (u v : List α) {a b : α} (hba : b < a) :
    inversionCount (u ++ a :: b :: v) =
      inversionCount (u ++ b :: a :: v) + 1 := by
  induction u with
  | nil =>
      simp [inversionCount, hba, not_lt_of_ge hba.le, Nat.add_assoc,
        Nat.add_left_comm, Nat.add_comm]
  | cons x u ih =>
      simp only [List.cons_append, inversionCount]
      simp only [List.countP_append, List.countP_cons]
      rw [ih]
      omega

/-- Adjacent shifts made while inserting `a` into an already sorted list. -/
def insertShiftCost {α : Type*} [LinearOrder α] (a : α) : List α → ℕ
  | [] => 0
  | b :: l => if a ≤ b then 0 else 1 + insertShiftCost a l

/-- The cost is the length of the prefix that Mathlib's `orderedInsert`
moves past `a`; see `List.orderedInsert_eq_take_drop`. -/
theorem insertShiftCost_eq_shiftedPrefix_length {α : Type*} [LinearOrder α]
    (a : α) (l : List α) :
    insertShiftCost a l =
      (l.takeWhile fun b => decide (¬ a ≤ b)).length := by
  induction l with
  | nil => rfl
  | cons b l ih =>
      by_cases hab : a ≤ b
      · simp [insertShiftCost, hab]
      · have hba : b < a := lt_of_not_ge hab
        simp [insertShiftCost, hab, hba, ih, Nat.add_comm]

/-- Total adjacent shifts in Mathlib's fold-right insertion sort. -/
def insertionSortCost {α : Type*} [LinearOrder α] : List α → ℕ
  | [] => 0
  | a :: l =>
      insertionSortCost l + insertShiftCost a (l.insertionSort (· ≤ ·))

theorem insertShiftCost_eq_countP {α : Type*} [LinearOrder α]
    (a : α) {l : List α} (hl : l.Pairwise (· ≤ ·)) :
    insertShiftCost a l = l.countP (fun b => decide (b < a)) := by
  induction l with
  | nil => simp [insertShiftCost]
  | cons b l ih =>
      rw [List.pairwise_cons] at hl
      rcases hl with ⟨hbl, hl⟩
      by_cases hab : a ≤ b
      · have hnone : ∀ c ∈ l, ¬ c < a := by
          intro c hc hca
          exact (not_lt_of_ge (hab.trans (hbl c hc))) hca
        have hz : l.countP (fun c => decide (c < a)) = 0 :=
          List.countP_eq_zero.mpr (by simpa using hnone)
        simp [insertShiftCost, hab, not_lt_of_ge hab, hz]
      · have hba : b < a := lt_of_not_ge hab
        simp [insertShiftCost, hab, hba, ih hl, Nat.add_comm]

theorem insertShiftCost_insertionSort {α : Type*} [LinearOrder α]
    (a : α) (l : List α) :
    insertShiftCost a (l.insertionSort (· ≤ ·)) =
      l.countP (fun b => decide (b < a)) := by
  rw [insertShiftCost_eq_countP a (List.pairwise_insertionSort (· ≤ ·) l)]
  exact (List.perm_insertionSort (· ≤ ·) l).countP_eq _

/-- The adjacent-shift count of stable insertion sort is exactly the inversion
count, for every list over every linear order (duplicates included). -/
theorem insertionSortCost_eq_inversionCount {α : Type*} [LinearOrder α]
    (l : List α) : insertionSortCost l = inversionCount l := by
  induction l with
  | nil => rfl
  | cons a l ih =>
      simp [insertionSortCost, inversionCount, insertShiftCost_insertionSort, ih,
        Nat.add_comm]

/-- Mathlib's stable insertion-sort output has inversion count zero. -/
theorem inversionCount_insertionSort_eq_zero {α : Type*} [LinearOrder α]
    (l : List α) : inversionCount (l.insertionSort (· ≤ ·)) = 0 :=
  inversionCount_eq_zero_of_pairwise (List.pairwise_insertionSort (· ≤ ·) l)

example : insertionSortCost [3, 1, 2, 1] = 4 := by decide

#print axioms insertShiftCost_eq_countP
#print axioms insertShiftCost_eq_shiftedPrefix_length
#print axioms insertShiftCost_insertionSort
#print axioms insertionSortCost_eq_inversionCount
#print axioms inversionCount_eq_zero_of_pairwise
#print axioms inversionCount_adjacent_swap
#print axioms inversionCount_insertionSort_eq_zero

end InsertionSortInversion
