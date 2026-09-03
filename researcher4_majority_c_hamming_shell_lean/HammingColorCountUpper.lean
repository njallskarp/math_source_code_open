import HammingFin3LowerBound

/-!
# From Hamming color-class size to the global color-count bound

This file uses a coloring function and its finite image, avoiding any custom
partition representation.  A generic finite double count turns a uniform
lower bound on nonempty fibers into an upper bound on the number of used
colors.  The final theorem composes that wrapper with
`fin3_card_ge_of_internal_degree`.
-/

open Finset Function

namespace MajorityCHamming

universe u v

/-- The colors actually used by a coloring of a finite type. -/
def usedColors {α : Type u} {γ : Type v} [Fintype α] [DecidableEq γ]
    (color : α → γ) : Finset γ :=
  Finset.univ.image color

/-- The fiber of a color, represented as a finset. -/
def colorClass {α : Type u} {γ : Type v} [Fintype α] [DecidableEq γ]
    (color : α → γ) (c : γ) : Finset α :=
  Finset.univ.filter fun x => color x = c

@[simp]
theorem mem_colorClass {α : Type u} {γ : Type v} [Fintype α]
    [DecidableEq γ] {color : α → γ} {c : γ} {x : α} :
    x ∈ colorClass color c ↔ color x = c := by
  simp [colorClass]

@[simp]
theorem mem_usedColors {α : Type u} {γ : Type v} [Fintype α]
    [DecidableEq γ] {color : α → γ} {c : γ} :
    c ∈ usedColors color ↔ ∃ x, color x = c := by
  simp [usedColors]

/-- A uniform lower bound on all used fibers bounds the number of used
values.  This is the partition/division interface needed by coloring
arguments, stated for an arbitrary finite domain and arbitrary codomain with
decidable equality. -/
theorem card_usedColors_mul_le_card
    {α : Type u} {γ : Type v} [Fintype α] [DecidableEq γ]
    (color : α → γ) (m : ℕ)
    (hclass : ∀ c ∈ usedColors color, m ≤ #(colorClass color c)) :
    #(usedColors color) * m ≤ Fintype.card α := by
  classical
  have hdouble := Finset.card_mul_le_card_mul
    (s := usedColors color) (t := (Finset.univ : Finset α))
    (r := fun c x => color x = c) (m := m) (n := 1)
    (fun c hc => by
      simpa [Finset.bipartiteAbove, colorClass] using hclass c hc)
    (fun x hx => by
      apply Finset.card_le_one.mpr
      intro c hc d hd
      have hc' : color x = c := (Finset.mem_filter.mp hc).2
      have hd' : color x = d := (Finset.mem_filter.mp hd).2
      exact hc'.symm.trans hd')
  simpa using hdouble

/-- Before division, the number of used majority colors times the proved
minimum class size is at most the number `n^3` of Hamming words. -/
theorem fin3_usedColors_mul_classBound_le
    {n : ℕ} (hn : 2 ≤ n) {γ : Type v} [DecidableEq γ]
    (color : (Fin 3 → Fin n) → γ)
    (hmajority : ∀ u,
      n - 1 + n / 2 ≤
        #(internalNeighbors (colorClass color (color u)) u)) :
    #(usedColors color) * (n * (n / 2 + 1)) ≤ n ^ 3 := by
  have hclass : ∀ c ∈ usedColors color,
      n * (n / 2 + 1) ≤ #(colorClass color c) := by
    intro c hc
    obtain ⟨v₀, hvc⟩ := mem_usedColors.mp hc
    apply fin3_card_ge_of_internal_degree hn (colorClass color c) v₀
    · simp [hvc]
    · intro u hu
      have huc : color u = c := mem_colorClass.mp hu
      simpa [huc] using hmajority u
  have hcount := card_usedColors_mul_le_card color (n * (n / 2 + 1)) hclass
  simpa [Fintype.card_fun] using hcount

/-- The natural-number representative of `ceil ((n+1)/2)`. -/
theorem div_two_add_one_eq_add_two_div_two (n : ℕ) :
    n / 2 + 1 = (n + 2) / 2 := by
  omega

/-- Global upper bound on the number of colors actually used by a majority
coloring of the balanced three-dimensional Hamming graph.

The right side is exactly `floor (n^2 / ceil ((n+1)/2))`. -/
theorem fin3_card_usedColors_le_majority_bound
    {n : ℕ} (hn : 2 ≤ n) {γ : Type v} [DecidableEq γ]
    (color : (Fin 3 → Fin n) → γ)
    (hmajority : ∀ u,
      n - 1 + n / 2 ≤
        #(internalNeighbors (colorClass color (color u)) u)) :
    #(usedColors color) ≤ n * n / ((n + 2) / 2) := by
  rw [← div_two_add_one_eq_add_two_div_two]
  have hnpos : 0 < n := by omega
  have hqpos : 0 < n / 2 + 1 := by omega
  have hmul := fin3_usedColors_mul_classBound_le hn color hmajority
  apply (Nat.le_div_iff_mul_le hqpos).2
  have hcancel :
      n * (#(usedColors color) * (n / 2 + 1)) ≤ n * (n * n) := by
    calc
      n * (#(usedColors color) * (n / 2 + 1)) =
          #(usedColors color) * (n * (n / 2 + 1)) := by ac_rfl
      _ ≤ n ^ 3 := hmul
      _ = n * (n * n) := by ring
  exact (Nat.mul_le_mul_left_iff hnpos).mp hcancel

#print axioms card_usedColors_mul_le_card
#print axioms fin3_usedColors_mul_classBound_le
#print axioms div_two_add_one_eq_add_two_div_two
#print axioms fin3_card_usedColors_le_majority_bound

end MajorityCHamming
