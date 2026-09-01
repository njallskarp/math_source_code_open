import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Finset.Interval
import Mathlib.Tactic

/-!
# The finite order-statistic identity behind the alpha = 2 Bernstein-Bezier operator

Let `p k` be the mass at `k` and let `tailMass n p k` be the mass in the
integer interval `[k, n]`.  For two independent variables with this common
mass function, the event that their minimum is exactly `k` is the disjoint
union of

* both variables equal `k`;
* the first equals `k` and the second is greater than `k`;
* the second equals `k` and the first is greater than `k`.

`minPairMass` is the resulting algebraic mass.  The main theorem proves that
it is the difference of consecutive squared tails.  Specializing `p` to the
binomial mass gives exactly the weights of the alpha = 2 Bezier-Bernstein
operator.
-/

open scoped BigOperators

namespace BezierBernstein

variable {R : Type*} [CommRing R]

/-- The finite tail mass `sum_{j=k}^n p j`. -/
def tailMass (n : ℕ) (p : ℕ → R) (k : ℕ) : R :=
  ∑ j ∈ Finset.Icc k n, p j

/--
The mass of the three disjoint cases giving `min (X,Y) = k` for two
independent variables with common mass function `p` supported on `[0,n]`.
-/
def minPairMass (n : ℕ) (p : ℕ → R) (k : ℕ) : R :=
  p k * p k + p k * tailMass n p (k + 1) + tailMass n p (k + 1) * p k

/-- A finite tail splits into its first atom and the following tail. -/
theorem tailMass_eq_add_succ (n k : ℕ) (p : ℕ → R) (hk : k ≤ n) :
    tailMass n p k = p k + tailMass n p (k + 1) := by
  rw [tailMass, tailMass]
  have hinterval : Finset.Icc k n = insert k (Finset.Icc (k + 1) n) := by
    ext j
    simp only [Finset.mem_Icc, Finset.mem_insert]
    omega
  rw [hinterval, Finset.sum_insert]
  simp

/--
Exact finite order-statistic identity:

`mass(min(X,Y)=k) = P(X≥k)^2 - P(X≥k+1)^2`.

The statement is algebraic, so it applies to probability masses in `ℝ` and
also to exact rational or symbolic coefficient rings.
-/
theorem minPairMass_eq_tail_sq_sub (n k : ℕ) (p : ℕ → R) (hk : k ≤ n) :
    minPairMass n p k = tailMass n p k ^ 2 - tailMass n p (k + 1) ^ 2 := by
  rw [tailMass_eq_add_succ n k p hk]
  simp only [minPairMass]
  ring

/-- The tail above the support is zero. -/
@[simp]
theorem tailMass_succ_top (n : ℕ) (p : ℕ → R) :
    tailMass n p (n + 1) = 0 := by
  simp [tailMass]

/--
The minimum masses telescope to the square of the total input mass.  In
particular, if `p` is normalized, the squared-tail differences form a
normalized finite mass function.
-/
theorem sum_minPairMass_eq_tail_zero_sq (n : ℕ) (p : ℕ → R) :
    ∑ k ∈ Finset.range (n + 1), minPairMass n p k = tailMass n p 0 ^ 2 := by
  calc
    ∑ k ∈ Finset.range (n + 1), minPairMass n p k =
        ∑ k ∈ Finset.range (n + 1),
          (tailMass n p k ^ 2 - tailMass n p (k + 1) ^ 2) := by
      apply Finset.sum_congr rfl
      intro k hk
      have hklt : k < n + 1 := Finset.mem_range.mp hk
      exact minPairMass_eq_tail_sq_sub n k p (by omega)
    _ = tailMass n p 0 ^ 2 - tailMass n p (n + 1) ^ 2 := by
      exact Finset.sum_range_sub' (fun k ↦ tailMass n p k ^ 2) (n + 1)
    _ = tailMass n p 0 ^ 2 := by simp

#print axioms tailMass_eq_add_succ
#print axioms minPairMass_eq_tail_sq_sub
#print axioms tailMass_succ_top
#print axioms sum_minPairMass_eq_tail_zero_sq

end BezierBernstein
