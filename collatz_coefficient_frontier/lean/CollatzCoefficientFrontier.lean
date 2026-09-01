import Lean.Elab.Tactic.Omega

/-!
# Rational ballot certificates for noncontracting Collatz coefficients

If `2^N ≤ 3^p`, then every parity prefix satisfying the integer ballot
inequality `p i ≤ N q_i` also satisfies the Collatz coefficient inequality
`2^i ≤ 3^q_i`.  This is the theorem-level inclusion behind the exact symbolic
frontier counter and its cyclic-rotation lower bound.
-/

namespace CollatzCoefficientFrontier

inductive Bit where
  | even
  | odd
  deriving DecidableEq

def oddCount : List Bit → Nat
  | [] => 0
  | Bit.even :: bits => oddCount bits
  | Bit.odd :: bits => oddCount bits + 1

def WeightedSafe (N p : Nat) (bits : List Bit) : Prop :=
  ∀ i, i ≤ bits.length → p * i ≤ N * oddCount (bits.take i)

def CoefficientSafe (bits : List Bit) : Prop :=
  ∀ i, i ≤ bits.length → 2 ^ i ≤ 3 ^ oddCount (bits.take i)

/-- Raising a rational ballot inequality through an integer power comparison. -/
theorem weightedExponent_noncontracting (N p i q : Nat)
    (hN : N ≠ 0) (hbase : 2 ^ N ≤ 3 ^ p) (hweight : p * i ≤ N * q) :
    2 ^ i ≤ 3 ^ q := by
  have hbasePow : (2 ^ N) ^ i ≤ (3 ^ p) ^ i :=
    Nat.pow_le_pow_left hbase i
  have hbasePow' : 2 ^ (N * i) ≤ 3 ^ (p * i) := by
    simpa [Nat.pow_mul] using hbasePow
  have hexponent : 3 ^ (p * i) ≤ 3 ^ (N * q) :=
    Nat.pow_le_pow_right (by omega) hweight
  have hpowered : (2 ^ i) ^ N ≤ (3 ^ q) ^ N := by
    simpa only [Nat.pow_mul'] using Nat.le_trans hbasePow' hexponent
  exact (Nat.pow_le_pow_iff_left hN).mp hpowered

/-- Every weighted-ballot word lies inside the coefficient-safe frontier. -/
theorem weightedSafe_coefficientSafe {N p : Nat} {bits : List Bit}
    (hN : N ≠ 0) (hbase : 2 ^ N ≤ 3 ^ p)
    (hsafe : WeightedSafe N p bits) : CoefficientSafe bits := by
  intro i hi
  exact weightedExponent_noncontracting N p i (oddCount (bits.take i))
    hN hbase (hsafe i hi)

#print axioms weightedExponent_noncontracting
#print axioms weightedSafe_coefficientSafe

end CollatzCoefficientFrontier
