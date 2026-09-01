import Lean.Elab.Tactic.Omega

/-!
# Exact cylinder transport for finite Collatz parity words

A realized parity word of length `k` from `n` to `z` represents the entire
2-adic cylinder

`n + 2^k t  ↦  z + 3^q t`,

where `q` is its number of odd steps and `t` is any natural number.  For a
contracting word, the lifted endpoint remains at least the lifted start exactly
while

`(2^k - 3^q) t ≤ z - n`.

This compresses infinitely many starts sharing one parity prefix to a single
base endpoint, a lift parameter, and one linear inequality.
-/

namespace CollatzCylinderTransport

/-- One step of the shortcut Collatz map. -/
inductive Step where
  | even
  | odd
  deriving DecidableEq

/-- Number of odd steps in a finite parity word. -/
def oddCount : List Step → Nat
  | [] => 0
  | Step.even :: steps => oddCount steps
  | Step.odd :: steps => oddCount steps + 1

/--
`Realizes steps n z` states that the shortcut Collatz rules carry `n` to `z`
with the specified parity word.
-/
inductive Realizes : List Step → Nat → Nat → Prop
  | nil (n : Nat) : Realizes [] n n
  | even {steps : List Step} {n m z : Nat}
      (head : n = 2 * m) (tail : Realizes steps m z) :
      Realizes (Step.even :: steps) n z
  | odd {steps : List Step} {n m z : Nat}
      (head : 3 * n + 1 = 2 * m) (tail : Realizes steps m z) :
      Realizes (Step.odd :: steps) n z

/--
Every natural lift by `2^k t` realizes the same length-`k` word, and its
endpoint is lifted by `3^q t`.
-/
theorem realizes_lift {steps : List Step} {n z : Nat}
    (h : Realizes steps n z) (t : Nat) :
    Realizes steps
      (n + 2 ^ steps.length * t)
      (z + 3 ^ oddCount steps * t) := by
  induction h generalizing t with
  | nil n =>
      simpa [oddCount] using Realizes.nil (n + t)
  | @even steps n m z head tail ih =>
      apply Realizes.even (m := m + 2 ^ steps.length * t)
      · simp only [List.length_cons, Nat.pow_succ]
        rw [head]
        simp [Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm]
      · exact ih t
  | @odd steps n m z head tail ih =>
      apply Realizes.odd (m := m + 2 ^ steps.length * (3 * t))
      · simp only [List.length_cons, Nat.pow_succ]
        calc
          3 * (n + 2 ^ steps.length * 2 * t) + 1 =
              (3 * n + 1) + 3 * (2 ^ steps.length * 2 * t) := by omega
          _ = 2 * m + 3 * (2 ^ steps.length * 2 * t) := by rw [head]
          _ = 2 * (m + 2 ^ steps.length * (3 * t)) := by
            simp [Nat.mul_add, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
      · simpa [oddCount, Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm,
          Nat.mul_left_comm] using ih (3 * t)

/-- Algebraic core of the contracting-cylinder endpoint criterion. -/
theorem linearContractingLiftIff (n z A B t : Nat)
    (hcontract : B < A) (hbase : n ≤ z) :
    n + A * t ≤ z + B * t ↔ (A - B) * t ≤ z - n := by
  have hAB : B ≤ A := Nat.le_of_lt hcontract
  have hsplit : A * t = (A - B) * t + B * t := by
    calc
      A * t = ((A - B) + B) * t := by rw [Nat.sub_add_cancel hAB]
      _ = (A - B) * t + B * t := by rw [Nat.add_mul]
  have hzsplit : z = n + (z - n) := by omega
  constructor <;> intro h <;> omega

/--
For a contracting parity word and a non-descending base representative, a lift
is non-descending exactly when its lift parameter obeys one linear inequality.
-/
theorem contractingLiftIff {steps : List Step} {n z t : Nat}
    (hcontract : 3 ^ oddCount steps < 2 ^ steps.length)
    (hbase : n ≤ z) :
    n + 2 ^ steps.length * t ≤ z + 3 ^ oddCount steps * t ↔
      (2 ^ steps.length - 3 ^ oddCount steps) * t ≤ z - n := by
  exact linearContractingLiftIff n z
    (2 ^ steps.length) (3 ^ oddCount steps) t hcontract hbase

/-- Exact quotient bound on every non-descending lift parameter. -/
theorem contractingLiftParameterBound {steps : List Step} {n z t : Nat}
    (hcontract : 3 ^ oddCount steps < 2 ^ steps.length)
    (hbase : n ≤ z)
    (hlift : n + 2 ^ steps.length * t ≤
      z + 3 ^ oddCount steps * t) :
    t ≤ (z - n) / (2 ^ steps.length - 3 ^ oddCount steps) := by
  have hpos : 0 < 2 ^ steps.length - 3 ^ oddCount steps :=
    Nat.sub_pos_of_lt hcontract
  apply (Nat.le_div_iff_mul_le hpos).2
  have hbound := (contractingLiftIff hcontract hbase).1 hlift
  simpa [Nat.mul_comm] using hbound

/--
Packaged cylinder theorem: the lifted endpoints realize the same word, and
their no-descent condition is exactly the contracting lift inequality.
-/
theorem realizedContractingCylinder {steps : List Step} {n z t : Nat}
    (hreal : Realizes steps n z)
    (hcontract : 3 ^ oddCount steps < 2 ^ steps.length)
    (hbase : n ≤ z) :
    Realizes steps
        (n + 2 ^ steps.length * t)
        (z + 3 ^ oddCount steps * t) ∧
      (n + 2 ^ steps.length * t ≤ z + 3 ^ oddCount steps * t ↔
        (2 ^ steps.length - 3 ^ oddCount steps) * t ≤ z - n) := by
  exact ⟨realizes_lift hreal t, contractingLiftIff hcontract hbase⟩

#print axioms realizes_lift
#print axioms linearContractingLiftIff
#print axioms contractingLiftIff
#print axioms contractingLiftParameterBound
#print axioms realizedContractingCylinder

end CollatzCylinderTransport
