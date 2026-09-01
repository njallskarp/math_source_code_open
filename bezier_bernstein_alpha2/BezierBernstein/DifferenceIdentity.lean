import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# The finite difference reduction for a pairwise minimum

This file isolates the exact algebraic identity behind the probabilistic
reduction

`E[min(X,Y)] = E[X] - E[|X-Y|] / 2`

for two independent, identically distributed finite random variables.  No
limit theorem or measure-theoretic API is needed for this finite layer.
-/

open scoped BigOperators

namespace BezierBernstein

/-- Total mass of a real sequence restricted to `{0, ..., n}`. -/
def totalMass (n : ℕ) (p : ℕ → ℝ) : ℝ :=
  ∑ i ∈ Finset.range (n + 1), p i

/-- First moment of a real mass sequence restricted to `{0, ..., n}`. -/
def firstMoment (n : ℕ) (p : ℕ → ℝ) : ℝ :=
  ∑ i ∈ Finset.range (n + 1), (i : ℝ) * p i

/-- The unnormalized first moment of the minimum of an independent pair. -/
def pairMinMoment (n : ℕ) (p : ℕ → ℝ) : ℝ :=
  ∑ i ∈ Finset.range (n + 1),
    ∑ j ∈ Finset.range (n + 1), (min (i : ℝ) (j : ℝ)) * p i * p j

/-- The unnormalized absolute-difference moment of an independent pair. -/
def pairAbsDiffMoment (n : ℕ) (p : ℕ → ℝ) : ℝ :=
  ∑ i ∈ Finset.range (n + 1),
    ∑ j ∈ Finset.range (n + 1), |(i : ℝ) - (j : ℝ)| * p i * p j

/-- Pointwise real identity expressing a minimum through an absolute difference. -/
theorem min_eq_add_sub_abs_div_two (a b : ℝ) :
    min a b = (a + b - |a - b|) / 2 := by
  rcases le_total a b with hab | hba
  · rw [min_eq_left hab, abs_of_nonpos (sub_nonpos.mpr hab)]
    ring
  · rw [min_eq_right hba, abs_of_nonneg (sub_nonneg.mpr hba)]
    ring

/-- The left-coordinate moment of a product mass factors. -/
theorem pairLeftMoment_eq_first_mul_total (n : ℕ) (p : ℕ → ℝ) :
    (∑ i ∈ Finset.range (n + 1),
      ∑ j ∈ Finset.range (n + 1), (i : ℝ) * p i * p j) =
      firstMoment n p * totalMass n p := by
  simp only [firstMoment, totalMass]
  calc
    (∑ i ∈ Finset.range (n + 1),
      ∑ j ∈ Finset.range (n + 1), (i : ℝ) * p i * p j) =
        ∑ i ∈ Finset.range (n + 1),
          ((i : ℝ) * p i) * (∑ j ∈ Finset.range (n + 1), p j) := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [Finset.mul_sum]
    _ = (∑ i ∈ Finset.range (n + 1), (i : ℝ) * p i) *
        (∑ j ∈ Finset.range (n + 1), p j) := by
      rw [Finset.sum_mul]

/-- The right-coordinate moment of a product mass factors. -/
theorem pairRightMoment_eq_total_mul_first (n : ℕ) (p : ℕ → ℝ) :
    (∑ i ∈ Finset.range (n + 1),
      ∑ j ∈ Finset.range (n + 1), (j : ℝ) * p i * p j) =
      totalMass n p * firstMoment n p := by
  simp only [firstMoment, totalMass]
  calc
    (∑ i ∈ Finset.range (n + 1),
      ∑ j ∈ Finset.range (n + 1), (j : ℝ) * p i * p j) =
        ∑ i ∈ Finset.range (n + 1),
          p i * (∑ j ∈ Finset.range (n + 1), (j : ℝ) * p j) := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j hj
      ring
    _ = (∑ i ∈ Finset.range (n + 1), p i) *
        (∑ j ∈ Finset.range (n + 1), (j : ℝ) * p j) := by
      rw [Finset.sum_mul]

/--
Exact finite difference reduction.  If `p` is normalized, `totalMass n p = 1`,
the right side is the usual first moment minus half the independent-pair
absolute-difference moment.
-/
theorem pairMinMoment_eq_total_mul_first_sub_half_abs (n : ℕ) (p : ℕ → ℝ) :
    pairMinMoment n p =
      totalMass n p * firstMoment n p - pairAbsDiffMoment n p / 2 := by
  calc
    pairMinMoment n p =
        ∑ i ∈ Finset.range (n + 1),
          ∑ j ∈ Finset.range (n + 1),
            (((i : ℝ) * p i * p j + (j : ℝ) * p i * p j -
              |(i : ℝ) - (j : ℝ)| * p i * p j) / 2) := by
      simp only [pairMinMoment]
      apply Finset.sum_congr rfl
      intro i hi
      apply Finset.sum_congr rfl
      intro j hj
      rw [min_eq_add_sub_abs_div_two]
      ring
    _ =
        ((∑ i ∈ Finset.range (n + 1),
            ∑ j ∈ Finset.range (n + 1), (i : ℝ) * p i * p j) +
          (∑ i ∈ Finset.range (n + 1),
            ∑ j ∈ Finset.range (n + 1), (j : ℝ) * p i * p j) -
          pairAbsDiffMoment n p) / 2 := by
      simp only [pairAbsDiffMoment]
      simp_rw [div_eq_mul_inv, sub_mul, add_mul, Finset.sum_sub_distrib,
        Finset.sum_add_distrib, Finset.sum_mul]
    _ = totalMass n p * firstMoment n p - pairAbsDiffMoment n p / 2 := by
      rw [pairLeftMoment_eq_first_mul_total, pairRightMoment_eq_total_mul_first]
      ring

/-- Centered form used for a probability mass of mean `c`. -/
theorem pairMinMoment_sub_of_normalized (n : ℕ) (p : ℕ → ℝ) (c : ℝ)
    (hmass : totalMass n p = 1) (hmean : firstMoment n p = c) :
    pairMinMoment n p - c = -pairAbsDiffMoment n p / 2 := by
  rw [pairMinMoment_eq_total_mul_first_sub_half_abs, hmass, hmean]
  ring

#print axioms min_eq_add_sub_abs_div_two
#print axioms pairLeftMoment_eq_first_mul_total
#print axioms pairRightMoment_eq_total_mul_first
#print axioms pairMinMoment_eq_total_mul_first_sub_half_abs
#print axioms pairMinMoment_sub_of_normalized

end BezierBernstein
