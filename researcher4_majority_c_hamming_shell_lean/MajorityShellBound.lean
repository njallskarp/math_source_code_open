import Mathlib

/-!
# The capped-quadratic shell bound for majority C-colourings

This file formalizes the numerical optimization at the heart of the lower
bound on a colour-class size in the reviewed exact formula for majority
C-colourings of the balanced three-dimensional Hamming graph.

The two concentration lemmas are stated over the integers so that their
quadratic identities have no truncated subtraction.  The headline theorem
uses the two inequalities that characterize `r = ceil(N / 2)` and exactly
matches the doubled shell bound in the informal proof.
-/

namespace MajorityCHamming

/-- If three nonnegative quantities of cap `N` have total `N + t`, their sum
of squares is at most the value obtained by filling one cap. -/
lemma sum_sq_le_one_cap
    {N t a b c : ℤ}
    (hN : 0 ≤ N) (ht0 : 0 ≤ t)
    (ha0 : 0 ≤ a) (hb0 : 0 ≤ b) (hc0 : 0 ≤ c)
    (haN : a ≤ N) (hbN : b ≤ N) (hcN : c ≤ N)
    (hsum : a + b + c = N + t) :
    a ^ 2 + b ^ 2 + c ^ 2 ≤ N ^ 2 + t ^ 2 := by
  rcases le_total (a + b) N with hab | hab
  · have hab0 : 0 ≤ a + b := by linarith
    have hab_sq : a ^ 2 + b ^ 2 ≤ (a + b) ^ 2 := by
      nlinarith [mul_nonneg ha0 hb0]
    have hleft : 0 ≤ N - (a + b) := by linarith
    have hright : 0 ≤ N - c := by linarith
    have hconcentrated : (a + b) ^ 2 + c ^ 2 ≤ N ^ 2 + t ^ 2 := by
      nlinarith [mul_nonneg hleft hright]
    linarith
  · let u := a + b - N
    have hu0 : 0 ≤ u := by
      dsimp [u]
      linarith
    have huN : u ≤ N := by
      dsimp [u]
      linarith
    have huc : u + c = t := by
      dsimp [u]
      linarith
    have hleft : 0 ≤ N - a := by linarith
    have hright : 0 ≤ N - b := by linarith
    have hab_sq : a ^ 2 + b ^ 2 ≤ N ^ 2 + u ^ 2 := by
      dsimp [u]
      nlinarith [mul_nonneg hleft hright]
    have huc_sq : u ^ 2 + c ^ 2 ≤ t ^ 2 := by
      rw [← huc]
      nlinarith [mul_nonneg hu0 hc0]
    linarith

/-- If three nonnegative quantities of cap `N` have total `2N + t`, their
sum of squares is at most the value obtained by filling two caps. -/
lemma sum_sq_le_two_caps
    {N t a b c : ℤ}
    (hN : 0 ≤ N) (ht0 : 0 ≤ t)
    (ha0 : 0 ≤ a) (hb0 : 0 ≤ b) (hc0 : 0 ≤ c)
    (haN : a ≤ N) (hbN : b ≤ N) (hcN : c ≤ N)
    (hsum : a + b + c = 2 * N + t) :
    a ^ 2 + b ^ 2 + c ^ 2 ≤ 2 * N ^ 2 + t ^ 2 := by
  let u := a + b - N
  have hab : N ≤ a + b := by linarith
  have hu0 : 0 ≤ u := by
    dsimp [u]
    linarith
  have huN : u ≤ N := by
    dsimp [u]
    linarith
  have huc : u + c = N + t := by
    dsimp [u]
    linarith
  have hleft_ab : 0 ≤ N - a := by linarith
  have hright_ab : 0 ≤ N - b := by linarith
  have hab_sq : a ^ 2 + b ^ 2 ≤ N ^ 2 + u ^ 2 := by
    dsimp [u]
    nlinarith [mul_nonneg hleft_ab hright_ab]
  have hleft_uc : 0 ≤ N - u := by linarith
  have hright_uc : 0 ≤ N - c := by linarith
  have huc_sq : u ^ 2 + c ^ 2 ≤ N ^ 2 + t ^ 2 := by
    nlinarith [mul_nonneg hleft_uc hright_uc]
  linarith

/-- The exact doubled capped-quadratic inequality used in the lower bound for
a colour class of `K_(N+1) square K_(N+1) square K_(N+1)`.

The hypotheses `N ≤ 2*r ≤ N+1` characterize `r = ceil(N/2)` for integral
`N` and `r`.  If `a`, `b`, and `c` are the three first-shell counts, the
right side is twice the shell-count lower bound
`1 + A + (1/2) * sum_i a_i * (N+r-a_i)`. -/
theorem balanced_shell_lower_bound_int
    {N r a b c : ℤ}
    (hN : 1 ≤ N)
    (hr_lower : N ≤ 2 * r) (hr_upper : 2 * r ≤ N + 1)
    (ha0 : 0 ≤ a) (hb0 : 0 ≤ b) (hc0 : 0 ≤ c)
    (haN : a ≤ N) (hbN : b ≤ N) (hcN : c ≤ N)
    (hsum : N + r ≤ a + b + c) :
    2 * ((N + 1) * (r + 1)) ≤
      2 * (1 + (a + b + c)) +
        a * (N + r - a) + b * (N + r - b) + c * (N + r - c) := by
  let A := a + b + c
  have hN0 : 0 ≤ N := by linarith
  have hr0 : 0 ≤ r := by linarith
  have hrN : r ≤ N := by linarith
  have hA_upper : A ≤ 3 * N := by
    dsimp [A]
    linarith
  rcases le_total A (2 * N) with hA_two | htwo_A
  · let t := A - N
    have ht0 : 0 ≤ t := by
      dsimp [t, A]
      linarith
    have htr : r ≤ t := by
      dsimp [t, A]
      linarith
    have htN : t ≤ N := by
      dsimp [t]
      linarith
    have hA_eq : a + b + c = N + t := by
      dsimp [t, A]
      linarith
    have hsq := sum_sq_le_one_cap hN0 ht0
      ha0 hb0 hc0 haN hbN hcN hA_eq
    have hfactor : 0 ≤ (t - r) * (N + 2 - t) := by
      exact mul_nonneg (by linarith) (by linarith)
    dsimp [A, t] at hsq hfactor ⊢
    nlinarith
  · let t := A - 2 * N
    have ht0 : 0 ≤ t := by
      dsimp [t]
      linarith
    have htN : t ≤ N := by
      dsimp [t]
      linarith
    have hA_eq : a + b + c = 2 * N + t := by
      dsimp [t, A]
      linarith
    have hsq := sum_sq_le_two_caps hN0 ht0
      ha0 hb0 hc0 haN hbN hcN hA_eq
    have hfactor : 0 ≤ t * (N + r + 2 - t) := by
      exact mul_nonneg ht0 (by linarith)
    dsimp [A, t] at hsq hfactor ⊢
    nlinarith

/-- Natural-number form of `balanced_shell_lower_bound_int`, with
`r = ceil(N/2) = (N+1)/2` substituted.  This is the form used for finite
cardinalities in the Hamming-graph shell argument. -/
theorem balanced_shell_lower_bound_nat
    {N a b c : ℕ}
    (hN : 1 ≤ N)
    (haN : a ≤ N) (hbN : b ≤ N) (hcN : c ≤ N)
    (hsum : N + (N + 1) / 2 ≤ a + b + c) :
    2 * ((N + 1) * ((N + 1) / 2 + 1)) ≤
      2 * (1 + (a + b + c)) +
        a * (N + (N + 1) / 2 - a) +
        b * (N + (N + 1) / 2 - b) +
        c * (N + (N + 1) / 2 - c) := by
  let r := (N + 1) / 2
  have hr_lower : N ≤ 2 * r := by
    dsimp [r]
    omega
  have hr_upper : 2 * r ≤ N + 1 := by
    dsimp [r]
    omega
  have ha_threshold : a ≤ N + r := by omega
  have hb_threshold : b ≤ N + r := by omega
  have hc_threshold : c ≤ N + r := by omega
  have hbound := balanced_shell_lower_bound_int
    (N := (N : ℤ)) (r := (r : ℤ))
    (a := (a : ℤ)) (b := (b : ℤ)) (c := (c : ℤ))
    (by exact_mod_cast hN)
    (by exact_mod_cast hr_lower) (by exact_mod_cast hr_upper)
    (by positivity) (by positivity) (by positivity)
    (by exact_mod_cast haN) (by exact_mod_cast hbN) (by exact_mod_cast hcN)
    (by exact_mod_cast hsum)
  exact_mod_cast hbound

/-- A direct cardinality interface for the Hamming-shell argument.

Here `B` is the size of the selected distance-two shell and `C` is the size
of the whole colour class.  The first extra hypothesis is exactly the
first-shell/distance-two-shell incidence bound; the second only says that the
origin, first shell, and distance-two shell are disjoint subsets of the class.
The conclusion is the required class-size lower bound. -/
theorem card_ge_of_shell_incidence
    {N a b c B C : ℕ}
    (hN : 1 ≤ N)
    (haN : a ≤ N) (hbN : b ≤ N) (hcN : c ≤ N)
    (hsum : N + (N + 1) / 2 ≤ a + b + c)
    (hincidence :
      a * (N + (N + 1) / 2 - a) +
        b * (N + (N + 1) / 2 - b) +
        c * (N + (N + 1) / 2 - c) ≤ 2 * B)
    (hsubsets : 1 + (a + b + c) + B ≤ C) :
    (N + 1) * ((N + 1) / 2 + 1) ≤ C := by
  have hshell := balanced_shell_lower_bound_nat hN haN hbN hcN hsum
  omega

#print axioms sum_sq_le_one_cap
#print axioms sum_sq_le_two_caps
#print axioms balanced_shell_lower_bound_int
#print axioms balanced_shell_lower_bound_nat
#print axioms card_ge_of_shell_incidence

end MajorityCHamming
