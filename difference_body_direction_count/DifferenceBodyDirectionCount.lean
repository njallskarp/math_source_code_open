import Mathlib.Data.Finset.Card
import Lean.Elab.Tactic.Omega

/-!
# Antipodal direction counts for polygon difference bodies

This file isolates the finite-set bridge in the strict-edge reduction for
small polygons.  If `D` is the set of genuine oriented edge directions and
`opp` sends a direction to its antipode, the direction set of the formal
difference body is `D ∪ D.image opp`.

The geometric assertion that this finite union is exactly the genuine-edge
set of the Minkowski difference body is intentionally not formalized here.
-/

namespace DifferenceBodyDirectionCount

/-- Inclusion-exclusion for a finite set and its image under an involution. -/
theorem card_union_image_add_card_inter_image {α : Type*} [DecidableEq α]
    (D : Finset α) (opp : α → α) (hopp : Function.Involutive opp) :
    (D ∪ D.image opp).card + (D ∩ D.image opp).card = 2 * D.card := by
  rw [Finset.card_union_add_card_inter]
  rw [Finset.card_image_of_injective D hopp.injective]
  omega

/-- A disjoint choice of one representative from each two-element antipodal
orbit has twice as many elements after adjoining all antipodes. -/
theorem card_representatives_union_image {α : Type*} [DecidableEq α]
    (R : Finset α) (opp : α → α) (hopp : Function.Involutive opp)
    (hdisjoint : Disjoint R (R.image opp)) :
    (R ∪ R.image opp).card = 2 * R.card := by
  rw [Finset.card_union_of_disjoint hdisjoint]
  rw [Finset.card_image_of_injective R hopp.injective]
  omega

/-- If `R` contains one side of every antipodal pair lying in `D`, then the
merged direction count plus twice the number of pairs is twice `D.card`.

The equality hypothesis is the exact finite interface for saying that `R`
enumerates the antipodal pairs in `D`. -/
theorem merged_card_add_twice_pair_count {α : Type*} [DecidableEq α]
    (D R : Finset α) (opp : α → α) (hopp : Function.Involutive opp)
    (hdisjoint : Disjoint R (R.image opp))
    (hoverlap : D ∩ D.image opp = R ∪ R.image opp) :
    (D ∪ D.image opp).card + 2 * R.card = 2 * D.card := by
  have hmerge := card_union_image_add_card_inter_image D opp hopp
  have hpairs := card_representatives_union_image R opp hopp hdisjoint
  rw [hoverlap, hpairs] at hmerge
  exact hmerge

/-- The exact `m = 2k - 2r` form of the merged-direction count. -/
theorem merged_card_eq_two_mul_sub {α : Type*} [DecidableEq α]
    (D R : Finset α) (opp : α → α) (hopp : Function.Involutive opp)
    (hdisjoint : Disjoint R (R.image opp))
    (hoverlap : D ∩ D.image opp = R ∪ R.image opp) :
    (D ∪ D.image opp).card = 2 * D.card - 2 * R.card := by
  have hcount := merged_card_add_twice_pair_count
    D R opp hopp hdisjoint hoverlap
  omega

/-- Under the ambient bound `D.card ≤ n`, the merged set has the full `2n`
directions exactly when `D` has size `n` and contains no antipodal pair. -/
theorem full_merged_card_iff {α : Type*} [DecidableEq α]
    (n : ℕ) (D R : Finset α) (opp : α → α)
    (hopp : Function.Involutive opp) (hD : D.card ≤ n)
    (hdisjoint : Disjoint R (R.image opp))
    (hoverlap : D ∩ D.image opp = R ∪ R.image opp) :
    (D ∪ D.image opp).card = 2 * n ↔ D.card = n ∧ R.card = 0 := by
  have hcount := merged_card_add_twice_pair_count
    D R opp hopp hdisjoint hoverlap
  constructor <;> omega

/-- Unless the original direction set is full and antipode-free, the merged
count drops by at least two. -/
theorem merged_card_le_two_mul_sub_two {α : Type*} [DecidableEq α]
    (n : ℕ) (D R : Finset α) (opp : α → α)
    (hopp : Function.Involutive opp) (hn : 1 ≤ n) (hD : D.card ≤ n)
    (hdisjoint : Disjoint R (R.image opp))
    (hoverlap : D ∩ D.image opp = R ∪ R.image opp)
    (hnotfull : ¬(D.card = n ∧ R.card = 0)) :
    (D ∪ D.image opp).card ≤ 2 * n - 2 := by
  have hcount := merged_card_add_twice_pair_count
    D R opp hopp hdisjoint hoverlap
  omega

/-- Parametric full-or-drop-two dichotomy used by the strict-edge criterion. -/
theorem full_or_drop_two {α : Type*} [DecidableEq α]
    (n : ℕ) (D R : Finset α) (opp : α → α)
    (hopp : Function.Involutive opp) (hn : 1 ≤ n) (hD : D.card ≤ n)
    (hdisjoint : Disjoint R (R.image opp))
    (hoverlap : D ∩ D.image opp = R ∪ R.image opp) :
    ((D ∪ D.image opp).card = 2 * n ∧ D.card = n ∧ R.card = 0) ∨
      (D ∪ D.image opp).card ≤ 2 * n - 2 := by
  by_cases hfull : D.card = n ∧ R.card = 0
  · left
    exact ⟨(full_merged_card_iff n D R opp hopp hD hdisjoint hoverlap).2 hfull,
      hfull⟩
  · right
    exact merged_card_le_two_mul_sub_two
      n D R opp hopp hn hD hdisjoint hoverlap hfull

/-- The concrete combinatorial endpoint for a polygon with at most sixteen
genuine edge directions: either the difference-direction set has exactly
thirty-two members with sixteen antipode-free original directions, or it has
at most thirty members. -/
theorem sixteen_direction_dichotomy {α : Type*} [DecidableEq α]
    (D R : Finset α) (opp : α → α) (hopp : Function.Involutive opp)
    (hD : D.card ≤ 16) (hdisjoint : Disjoint R (R.image opp))
    (hoverlap : D ∩ D.image opp = R ∪ R.image opp) :
    ((D ∪ D.image opp).card = 32 ∧ D.card = 16 ∧ R.card = 0) ∨
      (D ∪ D.image opp).card ≤ 30 := by
  simpa using full_or_drop_two 16 D R opp hopp (by omega) hD hdisjoint hoverlap

#print axioms card_union_image_add_card_inter_image
#print axioms card_representatives_union_image
#print axioms merged_card_add_twice_pair_count
#print axioms merged_card_eq_two_mul_sub
#print axioms full_merged_card_iff
#print axioms merged_card_le_two_mul_sub_two
#print axioms full_or_drop_two
#print axioms sixteen_direction_dichotomy

end DifferenceBodyDirectionCount
