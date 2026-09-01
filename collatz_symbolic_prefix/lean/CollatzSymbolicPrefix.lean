import Lean.Elab.Tactic.Omega

/-!
# Symbolic affine-prefix obstruction for Collatz trajectories

This file formalizes two reusable facts for the shortcut Collatz map.  The map
itself is kept abstract in the minimal-counterexample theorem; a finite parity
word is connected to its endpoints by the `Realizes` relation.

For a realized word `steps` from `n` to `z`, `affine_identity` proves

`2^steps.length * z = 3^oddCount(steps) * n + offset(steps)`.

If the word is a prefix of a trajectory which never drops below `n`, and its
linear multiplier is contracting, `fallingPrefixQuotientBound` proves the exact
integer bound

`n ≤ offset(steps) / (2^steps.length - 3^oddCount(steps))`.

Finally, `leastBadFallingPrefixBound` obtains the no-descent premise from the
minimality of a hypothetical counterexample to reaching `1`.
-/

namespace CollatzSymbolicPrefix

/-- `iter T k n` applies `T` exactly `k` times to `n`. -/
def iter (T : Nat → Nat) : Nat → Nat → Nat
  | 0, n => n
  | k + 1, n => T (iter T k n)

theorem iter_add (T : Nat → Nat) (a b n : Nat) :
    iter T (a + b) n = iter T b (iter T a n) := by
  induction b with
  | zero => simp [iter]
  | succ b ih =>
      rw [Nat.add_succ]
      simp only [iter]
      rw [ih]

/-- A starting value reaches `1` after finitely many applications of `T`. -/
def ReachesOne (T : Nat → Nat) (n : Nat) : Prop :=
  ∃ k, iter T k n = 1

/-- A least counterexample cannot have a later iterate below its start. -/
theorem leastBadNeverDescends (T : Nat → Nat) (n : Nat)
    (hbad : ¬ ReachesOne T n)
    (hminimal : ∀ m < n, ReachesOne T m) :
    ∀ k, n ≤ iter T k n := by
  intro k
  by_cases hge : n ≤ iter T k n
  · exact hge
  · have hlt : iter T k n < n := Nat.lt_of_not_ge hge
    obtain ⟨l, hl⟩ := hminimal (iter T k n) hlt
    exact False.elim (hbad ⟨k + l, by rw [iter_add, hl]⟩)

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

/-- Integer offset in the cleared-denominator affine iterate formula. -/
def offset : List Step → Nat
  | [] => 0
  | Step.even :: steps => 2 * offset steps
  | Step.odd :: steps => 3 ^ oddCount steps + 2 * offset steps

/--
`Realizes steps n z` says that `steps` is a valid shortcut-Collatz parity word
from `n` to `z`.  Even steps satisfy `n = 2*m`; odd steps satisfy
`3*n + 1 = 2*m`.
-/
inductive Realizes : List Step → Nat → Nat → Prop
  | nil (n : Nat) : Realizes [] n n
  | even {steps : List Step} {n m z : Nat}
      (head : n = 2 * m) (tail : Realizes steps m z) :
      Realizes (Step.even :: steps) n z
  | odd {steps : List Step} {n m z : Nat}
      (head : 3 * n + 1 = 2 * m) (tail : Realizes steps m z) :
      Realizes (Step.odd :: steps) n z

/-- The exact affine iterate identity for every realized finite parity word. -/
theorem affine_identity {steps : List Step} {n z : Nat}
    (h : Realizes steps n z) :
    2 ^ steps.length * z = 3 ^ oddCount steps * n + offset steps := by
  induction h with
  | nil n => simp [oddCount, offset]
  | @even steps n m z head tail ih =>
      simp only [List.length_cons, oddCount, offset, Nat.pow_succ]
      calc
        2 ^ steps.length * 2 * z = 2 * (2 ^ steps.length * z) := by
          simp [Nat.mul_comm, Nat.mul_left_comm]
        _ = 2 * (3 ^ oddCount steps * m + offset steps) := by rw [ih]
        _ = 3 ^ oddCount steps * n + 2 * offset steps := by
          rw [head]
          simp [Nat.mul_add, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
  | @odd steps n m z head tail ih =>
      simp only [List.length_cons, oddCount, offset, Nat.pow_succ]
      calc
        2 ^ steps.length * 2 * z = 2 * (2 ^ steps.length * z) := by
          simp [Nat.mul_comm, Nat.mul_left_comm]
        _ = 2 * (3 ^ oddCount steps * m + offset steps) := by rw [ih]
        _ = 3 ^ oddCount steps * (3 * n + 1) + 2 * offset steps := by
          rw [head]
          simp [Nat.mul_add, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
        _ = 3 ^ oddCount steps * 3 * n +
              (3 ^ oddCount steps + 2 * offset steps) := by
          simp [Nat.mul_add, Nat.add_assoc, Nat.mul_assoc]

/--
A contracting realized prefix of a trajectory that never drops below its start
has positive denominator and obeys the exact cross-multiplied affine bound.
-/
theorem fallingPrefixBound {steps : List Step} {n z : Nat}
    (hreal : Realizes steps n z)
    (hnever : n ≤ z)
    (hfall : 3 ^ oddCount steps < 2 ^ steps.length) :
    0 < 2 ^ steps.length - 3 ^ oddCount steps ∧
      (2 ^ steps.length - 3 ^ oddCount steps) * n ≤ offset steps := by
  have hscaled :
      2 ^ steps.length * n ≤
        3 ^ oddCount steps * n + offset steps := by
    calc
      2 ^ steps.length * n ≤ 2 ^ steps.length * z :=
        Nat.mul_le_mul_left (2 ^ steps.length) hnever
      _ = 3 ^ oddCount steps * n + offset steps := affine_identity hreal
  constructor
  · exact Nat.sub_pos_of_lt hfall
  · rw [Nat.sub_mul, Nat.sub_le_iff_le_add']
    exact hscaled

/-- Quotient form of `fallingPrefixBound`, using exact natural-number division. -/
theorem fallingPrefixQuotientBound {steps : List Step} {n z : Nat}
    (hreal : Realizes steps n z)
    (hnever : n ≤ z)
    (hfall : 3 ^ oddCount steps < 2 ^ steps.length) :
    n ≤ offset steps /
      (2 ^ steps.length - 3 ^ oddCount steps) := by
  obtain ⟨hpos, hbound⟩ := fallingPrefixBound hreal hnever hfall
  apply (Nat.le_div_iff_mul_le hpos).2
  simpa [Nat.mul_comm] using hbound

/--
For a least counterexample, every contracting realized orbit prefix supplies the
cross-multiplied affine bound.  `horbit` links the abstract orbit to the endpoint
used by `Realizes`.
-/
theorem leastBadFallingPrefixBound (T : Nat → Nat)
    {steps : List Step} {k n z : Nat}
    (hbad : ¬ ReachesOne T n)
    (hminimal : ∀ m < n, ReachesOne T m)
    (horbit : iter T k n = z)
    (hreal : Realizes steps n z)
    (hfall : 3 ^ oddCount steps < 2 ^ steps.length) :
    0 < 2 ^ steps.length - 3 ^ oddCount steps ∧
      (2 ^ steps.length - 3 ^ oddCount steps) * n ≤ offset steps := by
  apply fallingPrefixBound hreal
  · rw [← horbit]
    exact leastBadNeverDescends T n hbad hminimal k
  · exact hfall

#print axioms leastBadNeverDescends
#print axioms affine_identity
#print axioms fallingPrefixBound
#print axioms fallingPrefixQuotientBound
#print axioms leastBadFallingPrefixBound

end CollatzSymbolicPrefix
