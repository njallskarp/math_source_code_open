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

/-- Writing a canonical full residue as `rho + F*t`, adding the swap
displacement `F*u` wraps modulo `F*L` exactly when the local lift coordinate
`t+u` wraps modulo `L`. -/
theorem fullWrap_iff_liftWrap (rho F t u L : Int)
    (hF : 0 < F) (hrho0 : 0 ≤ rho) (hrhoF : rho < F) :
    F * L ≤ rho + F * t + F * u ↔ L ≤ t + u := by
  constructor
  · intro hfull
    have hcases : L ≤ t + u ∨ t + u ≤ L - 1 := by omega
    cases hcases with
    | inl hlocal => exact hlocal
    | inr htu =>
        have hmul : F * (t + u) ≤ F * (L - 1) :=
          Int.mul_le_mul_of_nonneg_left htu (by omega)
        have hsmall : rho + F * (t + u) < F * L := by grind
        have heq : rho + F * t + F * u = rho + F * (t + u) := by
          grind
        rw [heq] at hfull
        omega
  · intro hlocal
    have hmul : F * L ≤ F * (t + u) :=
      Int.mul_le_mul_of_nonneg_left hlocal (by omega)
    have hsum : F * L ≤ rho + F * (t + u) := by omega
    grind

/-- The cumulative full-wrap count minus the coefficient-gap winding number
is the change in canonical-window index.  This is the path-independent
wrap-defect identity. -/
theorem wrapDefectIdentity
    (M0 M1 μ0 μ1 d S fullWraps circleWindings κ0 κ1 : Int)
    (hmargin : M1 = M0 + S - d * fullWraps)
    (hcircle : μ1 = μ0 + S - d * circleWindings)
    (hwindow0 : μ0 - M0 = d * κ0)
    (hwindow1 : μ1 - M1 = d * κ1)
    (hd : d ≠ 0) :
    κ1 - κ0 = fullWraps - circleWindings := by
  have hproduct :
      d * (κ1 - κ0) = d * (fullWraps - circleWindings) := by
    grind
  exact Int.eq_of_mul_eq_mul_left hd hproduct

/-- When an inverse modulo `L` lifts to `u' = u + ε*L` modulo `2L`, the
associated coefficient-gap jump obeys `2J' = J+dε`.  For `ε=0,1`, this is the
inverse-doubling recurrence `J/2` or `(J+d)/2`. -/
theorem liftedJumpHalving
    (d u u' e L J J' ε : Int)
    (hjump : L * J = d * u + e)
    (hjump' : (2 * L) * J' = d * u' + e)
    (hlift : u' = u + ε * L)
    (hL : L ≠ 0) :
    2 * J' = J + d * ε := by
  have hproduct : L * (2 * J') = L * (J + d * ε) := by
    grind
  exact Int.eq_of_mul_eq_mul_left hL hproduct

/-- The normalized full-residue displacement and coefficient-gap jump differ
only by the affine-numerator decrement.  This is the division-free path form:
`A*S = d*D + (B₀-B₁)` transports the starting phase equation to an endpoint
phase lag of exactly `B₁`. -/
theorem pathPhaseLag
    (A d r μ κ D S B₀ B₁ : Int)
    (hsource : d * r = A * (μ - d * κ) + B₀)
    (hincrements : A * S = d * D + (B₀ - B₁)) :
    d * (r + D) = A * (μ + S - d * κ) + B₁ := by
  grind

/-- From a zero-window-index source, the wrap-defect identity forces the
opposite weak inequality from the hoped-for dominance: full-residue wraps
cannot be fewer than coefficient-circle wraps.  Across one residue addition,
the target index is consequently either zero or one. -/
theorem zeroIndexSourceWrapAntidominance
    (fullWraps circleWraps κ₁ : Int)
    (hwindow : κ₁ = fullWraps - circleWraps)
    (hκ₁ : 0 ≤ κ₁) (hfull0 : 0 ≤ fullWraps) (hfull1 : fullWraps ≤ 1)
    (hcircle : 0 ≤ circleWraps) :
    circleWraps ≤ fullWraps ∧ κ₁ ≤ 1 := by
  omega

/-- Exact arithmetic certificate for the smallest unrestricted strict defect.
The chronological words are `01101 -> 10101`: their affine equations are
`32z=27r+46` and `32z'=27r'+37`; the full phase wraps (`22+11=33`)
while the gap-five phase does not (`2+2=4`). -/
theorem lengthFiveStrictDefectCertificate :
    32 * 20 = 27 * 22 + 46 ∧
    32 * 2 = 27 * 1 + 37 ∧
    32 * 2 = 5 * 11 + 9 ∧
    22 + 11 = 1 + 32 ∧
    4 = 2 + 2 ∧
    22 - 20 = 2 ∧
    1 - 2 = 4 - 5 := by
  omega

/-- Exact prefix/suffix reconstruction for the target `p10s` of a wrapped
adjacent swap.  Here `rho, eta` are the prefix cylinder, `x` is the target
lift, `H, e, Bs, rs, zs` are the suffix data, and `m` is the compatible lift
transported through the suffix.  The conclusion isolates the prefix surplus
`L*rho - e*(3*eta+1) - 4*Bs`. -/
theorem splitTargetMargin
    (L H F P₀ e rho eta x rs Bs zs m r z d A : Int)
    (hL : L = 4 * H)
    (hA : A = F * L)
    (hd : d = A - P₀ * e)
    (hr : r = rho + F * x)
    (hcompat : P₀ * x + 3 * eta + 1 = 4 * rs + L * m)
    (hsuffix : H * zs = e * rs + Bs)
    (hz : z = zs + e * m) :
    L * (r - z) = d * x + (L * rho - e * (3 * eta + 1) - 4 * Bs) := by
  grind

/-- A lower bound `chi <= x` on the target lift certifies positive margin as
soon as it clears the split barrier.  Taking `chi = x mod 2^m` gives the
finite low-bit certificate hierarchy used by the exact audit. -/
theorem splitBarrierCertificate
    (L d M x chi Q : Int)
    (hmargin : L * M = d * x + Q)
    (hL : 0 < L) (hd : 0 ≤ d) (hchi : chi ≤ x)
    (hcertificate : 0 < d * chi + Q) :
    0 < M := by
  have hdx : d * chi ≤ d * x :=
    Int.mul_le_mul_of_nonneg_left hchi hd
  have hscaled : 0 < L * M := by
    rw [hmargin]
    omega
  have hcases : 0 < M ∨ M ≤ 0 := by omega
  cases hcases with
  | inl hM => exact hM
  | inr hM =>
      have hL0 : 0 ≤ L := by omega
      have hnonpos : L * M ≤ 0 :=
        Int.mul_nonpos_of_nonneg_of_nonpos hL0 hM
      omega

/-- If the full lift equals a truncated candidate lift, the ordinary integer
reached after `p10` is a lift of the suffix cylinder.  An independently
verified earlier coefficient crossing for `y` therefore rules out `x = chi`.
This theorem certifies the algebraic transport used by that shadowing test. -/
theorem equalLift_shadowsSuffix
    (P₀ c x chi y rs H k : Int)
    (hcandidate : P₀ * chi + c = 4 * y)
    (hcompat : P₀ * x + c = 4 * rs + 4 * H * k)
    (hequal : x = chi) :
    y = rs + H * k := by
  grind

/-- Once a shadowing test rules out equality with the truncated lift `chi`,
the next full lift is at least `chi + R`.  If that forced lower bound clears
the split barrier, the target margin is positive. -/
theorem shadowForcedBarrierCertificate
    (L d M x chi R Q t : Int)
    (hmargin : L * M = d * x + Q)
    (hlift : x = chi + R * t)
    (hL : 0 < L) (hd : 0 ≤ d) (hR : 0 < R) (ht : 0 ≤ t)
    (hne : x ≠ chi)
    (hcertificate : 0 < d * (chi + R) + Q) :
  0 < M := by
  have htne : t ≠ 0 := by
    intro htzero
    apply hne
    rw [hlift, htzero]
    simp
  have htone : 1 ≤ t := by omega
  have hRnonneg : 0 ≤ R := by omega
  have hRt : R * 1 ≤ R * t :=
    Int.mul_le_mul_of_nonneg_left htone hRnonneg
  have hlower : chi + R ≤ x := by
    rw [hlift]
    simpa using Int.add_le_add_left hRt chi
  exact splitBarrierCertificate
    L d M x (chi + R) Q hmargin hL hd hlower hcertificate

/-- If an induced candidate endpoint lies outside every lift of the prescribed
suffix residue, the candidate cannot equal the true split lift.  A concrete
parity mismatch within the suffix is an executable certificate of the
hypothesis `∀ k, y ≠ rs + H*k`. -/
theorem candidateClassMismatch_excludesLift
    (P₀ c x candidate y rs H : Int)
    (hcandidate : P₀ * candidate + c = 4 * y)
    (hcompat : ∃ k : Int, P₀ * x + c = 4 * rs + 4 * H * k)
    (hmismatch : ∀ k : Int, y ≠ rs + H * k) :
    x ≠ candidate := by
  intro hequal
  obtain ⟨k, hk⟩ := hcompat
  exact hmismatch k
    (equalLift_shadowsSuffix P₀ c x candidate y rs H k
      hcandidate hk hequal)

/-- Excluding the first `N` nonnegative ranks in a congruence class forces
the true lift above the corresponding ranked-lift threshold. -/
theorem excludedLiftLadderLowerBound
    (x chi R t N : Int)
    (hlift : x = chi + R * t)
    (hR : 0 ≤ R) (ht : 0 ≤ t)
    (hexcluded : ∀ k : Int, 0 ≤ k → k < N → x ≠ chi + R * k) :
    chi + R * N ≤ x := by
  have htN : N ≤ t := by
    have hcases : N ≤ t ∨ t < N := by omega
    cases hcases with
    | inl hle => exact hle
    | inr hlt => exact False.elim ((hexcluded t ht hlt) hlift)
  have hmul : R * N ≤ R * t :=
    Int.mul_le_mul_of_nonneg_left htN hR
  rw [hlift]
  exact Int.add_le_add_left hmul chi

/-- The excluded-lift ladder certificate: parity mismatches (or any other
exact exclusions) for ranks `0,...,N-1` produce a lower bound that proves the
split margin positive once it clears the affine barrier. -/
theorem excludedLiftLadderBarrierCertificate
    (L d M x chi R Q t N : Int)
    (hmargin : L * M = d * x + Q)
    (hlift : x = chi + R * t)
    (hL : 0 < L) (hd : 0 ≤ d) (hR : 0 ≤ R)
    (ht : 0 ≤ t)
    (hexcluded : ∀ k : Int, 0 ≤ k → k < N → x ≠ chi + R * k)
    (hcertificate : 0 < d * (chi + R * N) + Q) :
    0 < M := by
  have hlower : chi + R * N ≤ x :=
    excludedLiftLadderLowerBound x chi R t N
      hlift hR ht hexcluded
  exact splitBarrierCertificate
    L d M x (chi + R * N) Q hmargin hL hd hlower hcertificate

/-- The full suffix compatibility equation has a rank normal form.  If
`x = chi+4*t` and `y₀` is the endpoint induced by the base lift `chi`, then
the true rank satisfies `y₀+P₀*t = rs+H*m`. -/
theorem suffixRankEquation
    (P₀ c chi t y₀ rs H m : Int)
    (hbase : P₀ * chi + c = 4 * y₀)
    (hcompat : P₀ * (chi + 4 * t) + c = 4 * rs + 4 * H * m) :
    y₀ + P₀ * t = rs + H * m := by
  grind

/-- Candidate shadows form an exact arithmetic progression.  This is the
algebraic source of the valuation law for their first parity mismatch. -/
theorem candidateShadowDifference
    (P₀ y₀ k t yk yt : Int)
    (hk : yk = y₀ + P₀ * k)
    (ht : yt = y₀ + P₀ * t) :
    yk - yt = P₀ * (k - t) := by
  grind

/-- If `N` is the first rank whose affine barrier is positive, positivity of
the split margin is equivalent to the exact rank inequality `N ≤ t`. -/
theorem rankedBarrier_iff
    (L d M chi R Q t N : Int)
    (hmargin : L * M = d * (chi + R * t) + Q)
    (hL : 0 < L) (hd : 0 ≤ d) (hR : 0 ≤ R)
    (hbelow : d * (chi + R * (N - 1)) + Q ≤ 0)
    (habove : 0 < d * (chi + R * N) + Q) :
    0 < M ↔ N ≤ t := by
  constructor
  · intro hM
    have hscaled : 0 < L * M := Int.mul_pos hL hM
    rw [hmargin] at hscaled
    have hcases : N ≤ t ∨ t < N := by omega
    cases hcases with
    | inl hNt => exact hNt
    | inr htN =>
        have htle : t ≤ N - 1 := by omega
        have hmulR : R * t ≤ R * (N - 1) :=
          Int.mul_le_mul_of_nonneg_left htle hR
        have harg : chi + R * t ≤ chi + R * (N - 1) :=
          Int.add_le_add_left hmulR chi
        have hmulD : d * (chi + R * t) ≤
            d * (chi + R * (N - 1)) :=
          Int.mul_le_mul_of_nonneg_left harg hd
        have hq : d * (chi + R * t) + Q ≤
            d * (chi + R * (N - 1)) + Q :=
          Int.add_le_add_right hmulD Q
        have hnonpos : d * (chi + R * t) + Q ≤ 0 :=
          calc
            d * (chi + R * t) + Q ≤
                d * (chi + R * (N - 1)) + Q := hq
            _ ≤ 0 := hbelow
        omega
  · intro hNt
    have hmulR : R * N ≤ R * t :=
      Int.mul_le_mul_of_nonneg_left hNt hR
    have harg : chi + R * N ≤ chi + R * t :=
      Int.add_le_add_left hmulR chi
    have hmulD : d * (chi + R * N) ≤ d * (chi + R * t) :=
      Int.mul_le_mul_of_nonneg_left harg hd
    have hq : d * (chi + R * N) + Q ≤
        d * (chi + R * t) + Q :=
      Int.add_le_add_right hmulD Q
    have hpositive : 0 < d * (chi + R * t) + Q :=
      calc
        0 < d * (chi + R * N) + Q := habove
        _ ≤ d * (chi + R * t) + Q := hq
    have hscaled : 0 < L * M := by
      rw [hmargin]
      exact hpositive
    have hcases : 0 < M ∨ M ≤ 0 := by omega
    cases hcases with
    | inl hM => exact hM
    | inr hM =>
        have hL0 : 0 ≤ L := by omega
        have hnonpos : L * M ≤ 0 :=
          Int.mul_nonpos_of_nonneg_of_nonpos hL0 hM
        omega

/-- Once the low-two-bit class `chi` is chosen, the post-`p10` endpoint is
an affine function of the nonnegative rank `t`.  This division-free identity
is the algebraic core of the prefix-rank trajectory generator. -/
theorem prefixRankEndpoint
    (P c chi t y₀ : Int)
    (hbase : P * chi + c = 4 * y₀) :
    P * (chi + 4 * t) + c = 4 * (y₀ + P * t) := by
  grind

/-- The canonical local lift box `0 <= x < 4H` is exactly the rank box
`0 <= t < H` when `x=chi+4t` and `chi` is canonical modulo four. -/
theorem canonicalLift_iff_rankBox
    (x chi t H : Int)
    (hx : x = chi + 4 * t)
    (hchi0 : 0 ≤ chi) (hchi4 : chi < 4) :
    (0 ≤ x ∧ x < 4 * H) ↔ (0 ≤ t ∧ t < H) := by
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
#print axioms fullWrap_iff_liftWrap
#print axioms wrapDefectIdentity
#print axioms liftedJumpHalving
#print axioms pathPhaseLag
#print axioms zeroIndexSourceWrapAntidominance
#print axioms lengthFiveStrictDefectCertificate
#print axioms splitTargetMargin
#print axioms splitBarrierCertificate
#print axioms equalLift_shadowsSuffix
#print axioms shadowForcedBarrierCertificate
#print axioms candidateClassMismatch_excludesLift
#print axioms excludedLiftLadderLowerBound
#print axioms excludedLiftLadderBarrierCertificate
#print axioms suffixRankEquation
#print axioms candidateShadowDifference
#print axioms rankedBarrier_iff
#print axioms prefixRankEndpoint
#print axioms canonicalLift_iff_rankBox

end CollatzSwapCocycle
