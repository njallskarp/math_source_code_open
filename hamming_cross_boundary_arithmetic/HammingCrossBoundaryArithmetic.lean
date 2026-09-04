import Mathlib.Tactic

/-!
# Arithmetic kernel of the cyclic Hamming cross-boundary construction

The graph-theoretic construction partitions an `(s+a) × (s+b)` corner by
marking `b` consecutive residues in each row and using
`L = b + (a*b)/s` selected columns.  This file formalizes the exact natural-
number identities used after that combinatorial construction has supplied the
parts.  It deliberately does not claim that the cyclic marked sets form a
partition; that finite-incidence bridge remains external.
-/

namespace HammingCrossBoundary

/-- Euclidean division gives the incidence count used by the cyclic corner:
`(s+a)b = sL+t`, for `L=b+⌊ab/s⌋` and `t=ab mod s`. -/
theorem corner_incidence_count (s a b : ℕ) :
    (s + a) * b = s * (b + a * b / s) + a * b % s := by
  conv_lhs => rw [Nat.add_mul]
  conv_lhs => rhs; rw [← Nat.mod_add_div (a * b) s]
  ring

/-- Under the genuine-corner hypotheses, the selected-column count lies
between `b` and `s+b`; in particular the selected columns exist. -/
theorem selectedColumnCount_bounds
    {s a b : ℕ} (hs : 0 < s) (ha : 0 < a) (has : a < s) (hbs : b < s) :
    b ≤ b + a * b / s ∧ b + a * b / s < s + b := by
  constructor
  · exact Nat.le_add_right b _
  · have hab : a * b < a * s := (Nat.mul_lt_mul_left ha).2 hbs
    have hq : a * b / s < a := (Nat.div_lt_iff_lt_mul hs).2 hab
    omega

/-- The corner construction has exactly the quotient number of parts.  The
combinatorial input is only that the construction produces `(s+a)+L` parts;
this theorem checks that this is `⌊(s+a)(s+b)/s⌋`. -/
theorem corner_part_count
    {s a b : ℕ} (hs : 0 < s) :
    (s + a) + (b + a * b / s) = (s + a) * (s + b) / s := by
  have hfactor :
      (s + a) * (s + b) = s * (s + a + b) + a * b := by ring
  rw [hfactor, Nat.mul_add_div hs]
  omega

/-- Multiplying a quotient by a layer count commutes with division exactly
when the multiplied remainder stays below the divisor. -/
theorem layer_mul_quotient_eq_quotient_mul
    {s x layers : ℕ} (hs : 0 < s) (hremainder : layers * (x % s) < s) :
    layers * (x / s) = layers * x / s := by
  have hdecomp :
      layers * x = s * (layers * (x / s)) + layers * (x % s) := by
    conv_lhs => rhs; rw [← Nat.mod_add_div x s]
    ring
  rw [hdecomp, Nat.mul_add_div hs, Nat.div_eq_of_lt hremainder]
  omega

/-- The exact pair-remainder identity used in the four-dimensional Hamming
lift. -/
theorem pairRemainder_layer_count
    {s nj nk nl : ℕ} (hs : 0 < s)
    (hremainder : nl * ((nj * nk) % s) < s) :
    nl * (nj * nk / s) = nj * nk * nl / s := by
  rw [mul_comm (nj * nk) nl]
  exact layer_mul_quotient_eq_quotient_mul hs hremainder

/-- The middle pair in the explicit family is divisible by `s=k²`, even
though each individual factor `k²+k` is not divisible by `k²` for `k≥2`. -/
theorem explicit_middle_pair_divisible (k : ℕ) :
    k ^ 2 ∣ (k ^ 2 + k) ^ 2 := by
  refine ⟨(k + 1) ^ 2, ?_⟩
  ring

/-- Each middle factor has residue exactly `k` modulo `k²` for `k≥2`. -/
theorem explicit_middle_factor_remainder
    {k : ℕ} (hk : 2 ≤ k) :
    (k ^ 2 + k) % k ^ 2 = k := by
  have hklt : k < k ^ 2 := by nlinarith
  calc
    (k ^ 2 + k) % k ^ 2 = (k + k ^ 2 * 1) % k ^ 2 := by
      congr 1
      ring
    _ = k % k ^ 2 := by rw [Nat.add_mul_mod_self_left]
    _ = k := Nat.mod_eq_of_lt hklt

/-- Thus the pair-divisibility is genuine: neither middle factor is itself
divisible by `k²`. -/
theorem explicit_middle_factor_not_divisible
    {k : ℕ} (hk : 2 ≤ k) :
    ¬k ^ 2 ∣ k ^ 2 + k := by
  intro hdvd
  have hzero := Nat.mod_eq_zero_of_dvd hdvd
  rw [explicit_middle_factor_remainder hk] at hzero
  omega

/-- The divisible pair makes the layer-remainder hypothesis automatic for
every number of layers. -/
theorem explicit_pair_layer_count
    {k layers : ℕ} (hk : 0 < k) :
    layers * ((k ^ 2 + k) ^ 2 / k ^ 2) =
      (k ^ 2 + k) ^ 2 * layers / k ^ 2 := by
  rw [mul_comm ((k ^ 2 + k) ^ 2) layers]
  apply layer_mul_quotient_eq_quotient_mul (pow_pos hk _)
  rw [Nat.mod_eq_zero_of_dvd (explicit_middle_pair_divisible k), mul_zero]
  exact pow_pos hk _

/-- Exact quotient supplied by the divisible middle pair of the explicit
family. -/
theorem explicit_middle_pair_quotient {k : ℕ} (hk : 0 < k) :
    (k ^ 2 + k) ^ 2 / k ^ 2 = (k + 1) ^ 2 := by
  have hk2 : 0 < k ^ 2 := pow_pos hk _
  apply (Nat.div_eq_iff_eq_mul_left hk2 (explicit_middle_pair_divisible k)).2
  ring

/-- The target family's claimed number of lifted classes is the exact minor-
volume quotient. -/
theorem explicit_family_minor_quotient {k : ℕ} (hk : 0 < k) :
    ((k ^ 2 + k) ^ 2 * (k ^ 2 + 2)) / k ^ 2 =
      (k + 1) ^ 2 * (k ^ 2 + 2) := by
  have hk2 : 0 < k ^ 2 := pow_pos hk _
  have hdvd : k ^ 2 ∣ (k ^ 2 + k) ^ 2 * (k ^ 2 + 2) := by
    refine ⟨(k + 1) ^ 2 * (k ^ 2 + 2), ?_⟩
    ring
  apply (Nat.div_eq_iff_eq_mul_left hk2 hdvd).2
  ring

/-- The deficit sum in the explicit four-dimensional family. -/
theorem explicit_family_deficit_sum {k : ℕ} (hk : 1 ≤ k) :
    (k ^ 2 + 2 * k + 2) + (k ^ 2 + k - 1) +
        (k ^ 2 + k - 1) + (k ^ 2 + 1) =
      4 * k ^ 2 + 4 * k + 1 := by
  have hterm : 1 ≤ k ^ 2 + k := by omega
  omega

/-- Natural-number ceiling of half the odd deficit sum. -/
theorem explicit_family_majority_threshold (k : ℕ) :
    (4 * k ^ 2 + 4 * k + 1 + 1) / 2 = 2 * k ^ 2 + 2 * k + 1 := by
  have hfactor :
      4 * k ^ 2 + 4 * k + 1 + 1 = 2 * (2 * k ^ 2 + 2 * k + 1) := by
    ring
  rw [hfactor]
  exact Nat.mul_div_cancel_left _ (by norm_num)

/-- Subtracting the first-coordinate deficit from the majority threshold
recovers the construction parameter `s=k²`. -/
theorem explicit_family_corner_parameter
    {k : ℕ} (hk : 1 ≤ k) :
    (2 * k ^ 2 + 2 * k + 1) - (k ^ 2 + 2 * k + 2) + 1 = k ^ 2 := by
  have hk2 : 1 ≤ k ^ 2 := by nlinarith
  omega

/-- The base parameter `k=2` gives 54 classes. -/
theorem explicit_family_base_case :
    ((2 ^ 2 + 2) ^ 2 * (2 ^ 2 + 2)) / 2 ^ 2 = 54 := by
  norm_num

#print axioms corner_incidence_count
#print axioms selectedColumnCount_bounds
#print axioms corner_part_count
#print axioms layer_mul_quotient_eq_quotient_mul
#print axioms pairRemainder_layer_count
#print axioms explicit_middle_pair_divisible
#print axioms explicit_middle_factor_remainder
#print axioms explicit_middle_factor_not_divisible
#print axioms explicit_pair_layer_count
#print axioms explicit_middle_pair_quotient
#print axioms explicit_family_minor_quotient
#print axioms explicit_family_deficit_sum
#print axioms explicit_family_majority_threshold
#print axioms explicit_family_corner_parameter
#print axioms explicit_family_base_case

end HammingCrossBoundary
