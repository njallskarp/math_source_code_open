import Lean.Elab.Tactic.Omega
import Lean.Elab.Tactic.Grind

/-!
# Arithmetic core of the Collatz adjacent-swap cocycle

The theorems below isolate the exact algebra used when a parity subword `01`
is changed to `10`.  They do not assume the Collatz conjecture and introduce
no axioms.
-/

namespace CollatzSwapCocycle

/-- The affine numerator/residue expression scaled by the common denominator. -/
def scaledMargin (A B r c : Int) : Int := (A - B) * r - c

/-- For a valid affine endpoint equation, `scaledMargin` is the denominator
times the actual descent margin. -/
theorem scaledMargin_eq_mul_gap (A B r c z : Int)
    (hz : A * z = B * r + c) :
    scaledMargin A B r c = A * (r - z) := by
  grind [scaledMargin]

/-- An unwrapped residue displacement by `F*u`, paired with a numerator
decrease by `F*e`, changes the scaled margin by `F*(d*u+e)`. -/
theorem unwrappedScaledCocycle (A B r c F u e : Int) :
    scaledMargin A B (r + F * u) (c - F * e) =
      scaledMargin A B r c + F * ((A - B) * u + e) := by
  grind [scaledMargin]

/-- If the canonical residue wraps by subtracting `A`, the same local move
subtracts one full circumference `A*(A-B)` from the scaled change. -/
theorem wrappedScaledCocycle (A B r c F u e : Int) :
    scaledMargin A B (r + F * u - A) (c - F * e) =
      scaledMargin A B r c +
        F * ((A - B) * u + e) - A * (A - B) := by
  grind [scaledMargin]

/-- The two positive jump numerators are complementary: if `v=L-u`, their
sum is exactly `L*d`. -/
theorem complementaryJumpNumerators (d u v e L : Int)
    (hv : v = L - u) :
    (d * u + e) + (d * v - e) = L * d := by
  grind

/-- The congruence behind the wrapped jump.  Here `A=L*x`, `P*u=1+L*y`,
`d=A-P*e`, and `v=L-u`; then `d*v-e` is a multiple of `L`. -/
theorem wrappedJumpDivisible (A P e L u v d x y : Int)
    (hA : A = L * x) (hInv : P * u = 1 + L * y)
    (hd : d = A - P * e) (hv : v = L - u) :
    ∃ t : Int, d * v - e = L * t := by
  refine ⟨A - x * u - P * e + e * y, ?_⟩
  grind

/-- A multiple of positive `L` lying strictly above `-L` has a nonnegative
quotient.  This is the short-interval step used to prove wrapped jumps do not
have the wrong sign. -/
theorem shortMultiple_nonnegative (x L t : Int)
    (hL : 0 < L) (hlower : -L < x) (hx : x = L * t) :
    0 ≤ t := by
  have hcases : 0 ≤ t ∨ t ≤ -1 := by omega
  cases hcases with
  | inl ht => exact ht
  | inr ht =>
      have hL0 : 0 ≤ L := by omega
      have hprod : L * t ≤ L * (-1) :=
        Int.mul_le_mul_of_nonneg_left ht hL0
      have hle : L * t ≤ -L := by simpa using hprod
      rw [hx] at hlower
      omega

/-- If the short multiple is nonzero, its quotient is strictly positive. -/
theorem shortMultiple_positive (x L t : Int)
    (hL : 0 < L) (hlower : -L < x) (hx : x = L * t)
    (hne : x ≠ 0) :
    0 < t := by
  have ht := shortMultiple_nonnegative x L t hL hlower hx
  have htne : t ≠ 0 := by
    intro hzero
    apply hne
    rw [hx, hzero]
    simp
  omega

/-- In the normalized (unscaled) cocycle, an unwrapped move adds `J`. -/
theorem unwrappedGapChange (oldGap newGap J : Int)
    (hchange : newGap - oldGap = J) (hJ : 0 < J) :
    oldGap < newGap := by
  omega

/-- A wrapped move adds `J-d`; when `0<J<d`, it strictly decreases the
descent margin. -/
theorem wrappedGapChange (oldGap newGap J d : Int)
    (hchange : newGap - oldGap = J - d)
    (hJ : J < d) :
    newGap < oldGap := by
  omega

#print axioms scaledMargin_eq_mul_gap
#print axioms unwrappedScaledCocycle
#print axioms wrappedScaledCocycle
#print axioms complementaryJumpNumerators
#print axioms wrappedJumpDivisible
#print axioms shortMultiple_nonnegative
#print axioms shortMultiple_positive
#print axioms unwrappedGapChange
#print axioms wrappedGapChange

end CollatzSwapCocycle
