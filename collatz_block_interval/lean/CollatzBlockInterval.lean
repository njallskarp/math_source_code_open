import Lean.Elab.Tactic.Omega

/-!
# Algebraic core for exact Collatz block composition

The theorems are division-free.  `affine_compose` proves the offset law for
two concatenated parity blocks.  `compatible_block_lift` proves that once a
base lift is compatible with an inner prefix of length `j`, every lift by a
multiple of `2^H` stays compatible and its endpoint changes by the predicted
integer coefficient.
-/

namespace CollatzBlockInterval

/-- Exact affine-offset law for concatenating two realized blocks. -/
theorem affine_compose (n y z k h q p Cu Cv : Nat)
    (left : 2 ^ k * y = 3 ^ q * n + Cu)
    (right : 2 ^ h * z = 3 ^ p * y + Cv) :
    2 ^ (k + h) * z =
      3 ^ (q + p) * n + (3 ^ p * Cu + 2 ^ k * Cv) := by
  calc
    2 ^ (k + h) * z = 2 ^ k * (2 ^ h * z) := by
      simp [Nat.pow_add, Nat.mul_comm, Nat.mul_left_comm]
    _ = 2 ^ k * (3 ^ p * y + Cv) := by rw [right]
    _ = 3 ^ p * (2 ^ k * y) + 2 ^ k * Cv := by
      simp [Nat.mul_add, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
    _ = 3 ^ p * (3 ^ q * n + Cu) + 2 ^ k * Cv := by rw [left]
    _ = 3 ^ (q + p) * n + (3 ^ p * Cu + 2 ^ k * Cv) := by
      rw [Nat.pow_add]
      simp only [Nat.mul_add]
      ac_rfl

/-- Algebraic transport of a compatible lift through an internal block prefix. -/
theorem compatible_block_lift (s B a C z p j H u : Nat)
    (hjH : j ≤ H)
    (base : 2 ^ j * z = 3 ^ p * (s + B * a) + C) :
    2 ^ j * (z + 3 ^ p * B * 2 ^ (H - j) * u) =
      3 ^ p * (s + B * (a + 2 ^ H * u)) + C := by
  have hpow : 2 ^ H = 2 ^ j * 2 ^ (H - j) := by
    rw [← Nat.pow_add]
    congr
    omega
  calc
    2 ^ j * (z + 3 ^ p * B * 2 ^ (H - j) * u) =
        2 ^ j * z + 3 ^ p * B * (2 ^ j * 2 ^ (H - j)) * u := by
      simp [Nat.mul_add, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
    _ = (3 ^ p * (s + B * a) + C) + 3 ^ p * B * 2 ^ H * u := by
      rw [base, hpow]
    _ = 3 ^ p * (s + B * (a + 2 ^ H * u)) + C := by
      simp only [Nat.mul_add]
      ac_rfl

#print axioms affine_compose
#print axioms compatible_block_lift

end CollatzBlockInterval
