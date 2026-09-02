import CharneyDavis17

/-!
# The polar-size-three bottleneck at 17 vertices

This file packages a non-enumerative reduction for a hypothetical negative
Charney--Davis counterexample among 17-vertex flag generalized homology
5-spheres.

The topology from Labbé--Nevo is kept outside the kernel as explicitly named
hypotheses.  Lean checks the polynomial derivative identity and the finite
arithmetic consequence: a negative counterexample has polar size exactly
three, has `1 ≤ gammaTwo ≤ 5`, and has at least eight vertices with exactly
three antipodes.  If the Labbé--Nevo suspension alternative is supplied, all
of those minimum-antipode vertex links are nonsuspensions.
-/

namespace CharneyDavis17

open Polynomial

section VertexLinkDerivative

/-- The gamma-basis expansion of a degree-five vertex-link h-polynomial. -/
noncomputable def hFive (gammaZero gammaOne gammaTwo : ℤ) : Polynomial ℤ :=
  C gammaZero * (1 + X) ^ 5 +
    C gammaOne * X * (1 + X) ^ 3 +
    C gammaTwo * X ^ 2 * (1 + X)

/-- Differentiation at `t = -1` extracts the top link coefficient. -/
@[simp]
theorem eval_negOne_derivative_hFive
    (gammaZero gammaOne gammaTwo : ℤ) :
    eval (-1) (derivative (hFive gammaZero gammaOne gammaTwo)) = gammaTwo := by
  simp [hFive, derivative_pow]

/--
For a degree-six h-polynomial, differentiating the vertex-link identity and
evaluating at `t = -1` leaves `3 * gammaThree + 4 * gammaTwo`.
-/
@[simp]
theorem eval_negOne_derivative_vertexLinkRhs
    (gammaZero gammaOne gammaTwo gammaThree : ℤ) :
    eval (-1)
        (derivative
          (C 6 * hSix gammaZero gammaOne gammaTwo gammaThree +
            (1 - X) * derivative (hSix gammaZero gammaOne gammaTwo gammaThree))) =
      3 * gammaThree + 4 * gammaTwo := by
  simp [hSix, derivative_pow]
  ring

/--
The standard identity
`sum_v h_link(v) = 6 h_Delta + (1-t) h'_Delta` forces
`sum_v gammaTwo(link(v)) = 3 gammaThree(Delta) + 4 gammaTwo(Delta)`.
-/
theorem sum_vertexLink_gammaTwo_eq
    {V : Type*} [Fintype V]
    (deltaZero deltaOne deltaTwo deltaThree : ℤ)
    (linkZero linkOne linkTwo : V → ℤ)
    (vertexLinkIdentity :
      (∑ v, hFive (linkZero v) (linkOne v) (linkTwo v)) =
        C 6 * hSix deltaZero deltaOne deltaTwo deltaThree +
          (1 - X) * derivative (hSix deltaZero deltaOne deltaTwo deltaThree)) :
    ∑ v, linkTwo v = 3 * deltaThree + 4 * deltaTwo := by
  calc
    (∑ v, linkTwo v) =
        eval (-1) (derivative (∑ v, hFive (linkZero v) (linkOne v) (linkTwo v))) := by
          rw [derivative_sum, eval_finsetSum]
          simp
    _ = eval (-1)
        (derivative
          (C 6 * hSix deltaZero deltaOne deltaTwo deltaThree +
            (1 - X) * derivative (hSix deltaZero deltaOne deltaTwo deltaThree))) := by
          rw [vertexLinkIdentity]
    _ = 3 * deltaThree + 4 * deltaTwo :=
      eval_negOne_derivative_vertexLinkRhs _ _ _ _

end VertexLinkDerivative

section PolarArithmetic

/--
The exact polar-size case split for the 17-vertex boundary.  The hypotheses
name the four imported topological inputs: the general polar bounds, exclusion
of polar sizes one and two, exclusion of the octahedral endpoint six, and the
Labbé--Nevo vanishing theorem for polar size at least four.
-/
theorem negative_forces_polarSize_three
    (polarSize gammaThree : ℤ)
    (negative : gammaThree < 0)
    (polarLower : 1 ≤ polarSize)
    (polarUpper : polarSize ≤ 6)
    (notPolarOne : polarSize ≠ 1)
    (notPolarTwo : polarSize ≠ 2)
    (notPolarSix : polarSize ≠ 6)
    (largePolarVanishes : 4 ≤ polarSize → gammaThree = 0) :
    polarSize = 3 := by
  omega

/--
The missing-edge identity and the differentiated vertex-link identity force
`1 ≤ gammaTwo ≤ 5` in a negative counterexample once every antipode number is
at least three.
-/
theorem gammaTwo_bounds_of_negative
    (iota linkGammaTwo : Fin 17 → ℤ)
    (gammaTwo gammaThree : ℤ)
    (negative : gammaThree < 0)
    (iotaLower : ∀ v, 3 ≤ iota v)
    (missingEdgeIdentity : ∑ v, iota v = 62 - 2 * gammaTwo)
    (linkGammaTwoNonnegative : ∀ v, 0 ≤ linkGammaTwo v)
    (vertexLinkGammaIdentity :
      ∑ v, linkGammaTwo v = 3 * gammaThree + 4 * gammaTwo) :
    1 ≤ gammaTwo ∧ gammaTwo ≤ 5 := by
  have linkSumNonnegative : 0 ≤ ∑ v, linkGammaTwo v := by
    exact Finset.sum_nonneg fun v _ => linkGammaTwoNonnegative v
  have iotaSumLower : (51 : ℤ) ≤ ∑ v, iota v := by
    calc
      (51 : ℤ) = ∑ _v : Fin 17, (3 : ℤ) := by norm_num
      _ ≤ ∑ v, iota v := Finset.sum_le_sum fun v _ => iotaLower v
  constructor <;> omega

/-- The same identities bound the only still-open coefficient by `-6 ≤ gammaThree`. -/
theorem gammaThree_lower_bound_of_negative
    (linkGammaTwo : Fin 17 → ℤ) (gammaTwo gammaThree : ℤ)
    (linkGammaTwoNonnegative : ∀ v, 0 ≤ linkGammaTwo v)
    (vertexLinkGammaIdentity :
      ∑ v, linkGammaTwo v = 3 * gammaThree + 4 * gammaTwo)
    (gammaTwoUpper : gammaTwo ≤ 5) :
    -6 ≤ gammaThree := by
  have linkSumNonnegative : 0 ≤ ∑ v, linkGammaTwo v := by
    exact Finset.sum_nonneg fun v _ => linkGammaTwoNonnegative v
  omega

/--
At 17 vertices, the link formula `gammaOne(link(v)) = 6 - iota(v)`
turns the minimum-antipode reduction into the uniform ranges
`3 ≤ iota(v) ≤ 6` and `0 ≤ gammaOne(link(v)) ≤ 3`.
-/
theorem antipode_and_linkGammaOne_ranges
    (iota linkGammaOne : Fin 17 → ℤ)
    (iotaLower : ∀ v, 3 ≤ iota v)
    (linkGammaOneIdentity : ∀ v, linkGammaOne v = 6 - iota v)
    (linkGammaOneNonnegative : ∀ v, 0 ≤ linkGammaOne v) :
    ∀ v, (3 ≤ iota v ∧ iota v ≤ 6) ∧
      (0 ≤ linkGammaOne v ∧ linkGammaOne v ≤ 3) := by
  intro v
  have hiota := iotaLower v
  have hid := linkGammaOneIdentity v
  have hlink := linkGammaOneNonnegative v
  omega

/--
Gal's real-root inequality for a four-dimensional flag homology-sphere link
sharpens a minimum-antipode link to `gammaTwo(link(v)) ∈ {0,1,2}`.
-/
theorem minimumLink_gamma_profile
    (iota linkGammaOne linkGammaTwo : Fin 17 → ℤ)
    (linkGammaOneIdentity : ∀ v, linkGammaOne v = 6 - iota v)
    (linkGammaTwoNonnegative : ∀ v, 0 ≤ linkGammaTwo v)
    (linkRealRootBound : ∀ v, 4 * linkGammaTwo v ≤ (linkGammaOne v) ^ 2) :
    ∀ v, iota v = 3 →
      linkGammaOne v = 3 ∧
        (0 ≤ linkGammaTwo v ∧ linkGammaTwo v ≤ 2) := by
  intro v hiota
  have hone := linkGammaOneIdentity v
  have htwoLower := linkGammaTwoNonnegative v
  have htwoUpper := linkRealRootBound v
  have hlinkOne : linkGammaOne v = 3 := by omega
  rw [hlinkOne] at htwoUpper
  norm_num at htwoUpper
  exact ⟨hlinkOne, by omega⟩

/--
If 17 antipode numbers are at least three, their sum is
`62 - 2 * gammaTwo`, and `gammaTwo ≥ 1`, then at least eight vertices attain
the minimum value three.
-/
theorem atLeastEight_vertices_have_three_antipodes
    (iota : Fin 17 → ℤ) (gammaTwo : ℤ)
    (iotaLower : ∀ v, 3 ≤ iota v)
    (missingEdgeIdentity : ∑ v, iota v = 62 - 2 * gammaTwo)
    (gammaTwoLower : 1 ≤ gammaTwo) :
    8 ≤ (Finset.univ.filter fun v => iota v = 3).card := by
  let high : Finset (Fin 17) := Finset.univ.filter fun v => iota v ≠ 3
  have termwise : ∀ v : Fin 17,
      (3 : ℤ) + (if iota v = 3 then 0 else 1) ≤ iota v := by
    intro v
    split_ifs with h
    · omega
    · have := iotaLower v
      omega
  have summed :
      ∑ v : Fin 17, ((3 : ℤ) + (if iota v = 3 then 0 else 1)) ≤
        ∑ v, iota v :=
    Finset.sum_le_sum fun v _ => termwise v
  have highBound : (high.card : ℤ) ≤ 9 := by
    have indicator :
        (∑ v : Fin 17, (if iota v = 3 then 0 else 1 : ℤ)) = high.card := by
      calc
        (∑ v : Fin 17, (if iota v = 3 then 0 else 1 : ℤ)) =
            ∑ v : Fin 17, (if iota v ≠ 3 then 1 else 0 : ℤ) := by
              apply Finset.sum_congr rfl
              intro v _
              split_ifs <;> simp_all
        _ = high.card := by
          simpa only [high] using
            (Finset.natCast_card_filter (R := ℤ)
              (fun v : Fin 17 => iota v ≠ 3)
              (Finset.univ : Finset (Fin 17))).symm
    have normalized : (51 : ℤ) + high.card ≤ ∑ v, iota v := by
      simpa [Finset.sum_add_distrib, indicator] using summed
    omega
  have partition :=
    Finset.card_filter_add_card_filter_not
      (s := (Finset.univ : Finset (Fin 17))) (fun v => iota v = 3)
  have universeCard : (Finset.univ : Finset (Fin 17)).card = 17 := by simp
  change 8 ≤ (Finset.univ.filter fun v => iota v = 3).card
  dsimp [high] at highBound
  omega

/-- A minimum-antipode link cannot be a suspension in a negative example. -/
theorem negative_forces_minimumLink_nonsuspension
    (iota : Fin 17 → ℤ) (gammaThree : ℤ)
    (LinkIsSuspension : Fin 17 → Prop)
    (negative : gammaThree < 0)
    (suspensionStep :
      ∀ v, iota v = 3 → LinkIsSuspension v → 0 ≤ gammaThree) :
    ∀ v, iota v = 3 → ¬LinkIsSuspension v := by
  intro v hiota hsuspension
  exact (not_le_of_gt negative) (suspensionStep v hiota hsuspension)

/--
The reusable arithmetic and local-link core of the 17-vertex reduction.
All topology appears only through `suspensionStep` and the already reduced
fact that every antipode number is at least three.
-/
theorem negative_counterexample_has_eight_nonsuspension_minimumLinks
    (iota linkGammaTwo : Fin 17 → ℤ)
    (gammaTwo gammaThree : ℤ)
    (LinkIsSuspension : Fin 17 → Prop)
    (negative : gammaThree < 0)
    (iotaLower : ∀ v, 3 ≤ iota v)
    (missingEdgeIdentity : ∑ v, iota v = 62 - 2 * gammaTwo)
    (linkGammaTwoNonnegative : ∀ v, 0 ≤ linkGammaTwo v)
    (vertexLinkGammaIdentity :
      ∑ v, linkGammaTwo v = 3 * gammaThree + 4 * gammaTwo)
    (suspensionStep :
      ∀ v, iota v = 3 → LinkIsSuspension v → 0 ≤ gammaThree) :
    (1 ≤ gammaTwo ∧ gammaTwo ≤ 5) ∧
      -6 ≤ gammaThree ∧
      8 ≤ (Finset.univ.filter fun v => iota v = 3).card ∧
      ∀ v, iota v = 3 → ¬LinkIsSuspension v := by
  have gammaBounds := gammaTwo_bounds_of_negative iota linkGammaTwo gammaTwo
    gammaThree negative iotaLower missingEdgeIdentity linkGammaTwoNonnegative
    vertexLinkGammaIdentity
  exact ⟨gammaBounds,
    gammaThree_lower_bound_of_negative linkGammaTwo gammaTwo gammaThree
      linkGammaTwoNonnegative vertexLinkGammaIdentity gammaBounds.2,
    atLeastEight_vertices_have_three_antipodes iota gammaTwo iotaLower
      missingEdgeIdentity gammaBounds.1,
    negative_forces_minimumLink_nonsuspension iota gammaThree LinkIsSuspension
      negative suspensionStep⟩

/--
The complement-graph face-count identity makes the polar-size-three reduction
rigid.  Here `iota v` is the degree of `v` in the complement of the
one-skeleton and `triangleCount` is the number of complement triangles.  The
identity

`2 * gammaThree = 348 + sum_v iota(v) * (iota(v) - 10) - 2 * triangleCount`

is the inclusion--exclusion count of independent triples in that complement.
Once supplied, Lean checks that any negative example has
`(gammaTwo, gammaThree) = (5, -6)`, triangle-free complement, degree sequence
`3^16 4^1`, and total vertex-link `gammaTwo` equal to two.
-/
theorem negative_forces_rigid_complement_profile
    (iota linkGammaTwo : Fin 17 → ℤ)
    (gammaTwo gammaThree triangleCount : ℤ)
    (negative : gammaThree < 0)
    (iotaBounds : ∀ v, 3 ≤ iota v ∧ iota v ≤ 6)
    (missingEdgeIdentity : ∑ v, iota v = 62 - 2 * gammaTwo)
    (linkGammaTwoNonnegative : ∀ v, 0 ≤ linkGammaTwo v)
    (vertexLinkGammaIdentity :
      ∑ v, linkGammaTwo v = 3 * gammaThree + 4 * gammaTwo)
    (complementTriangleIdentity :
      2 * gammaThree =
        348 + ∑ v, iota v * (iota v - 10) - 2 * triangleCount)
    (triangleCountNonnegative : 0 ≤ triangleCount) :
    gammaTwo = 5 ∧ gammaThree = -6 ∧ triangleCount = 0 ∧
      (∑ v, linkGammaTwo v) = 2 ∧
      (∀ v, iota v = 3 ∨ iota v = 4) ∧
      (Finset.univ.filter fun v => iota v = 3).card = 16 := by
  have gammaBounds := gammaTwo_bounds_of_negative iota linkGammaTwo gammaTwo
    gammaThree negative (fun v => (iotaBounds v).1) missingEdgeIdentity
    linkGammaTwoNonnegative vertexLinkGammaIdentity
  have gammaThreeLower := gammaThree_lower_bound_of_negative linkGammaTwo
    gammaTwo gammaThree linkGammaTwoNonnegative vertexLinkGammaIdentity
    gammaBounds.2
  have existsHigh : ∃ w : Fin 17, iota w ≠ 3 := by
    by_contra h
    have hall : ∀ w : Fin 17, iota w = 3 := by
      intro w
      exact not_ne_iff.mp (not_exists.mp h w)
    have iotaSum : ∑ v, iota v = 51 := by simp [hall]
    omega
  obtain ⟨w, hw⟩ := existsHigh
  have termUpper : ∀ v : Fin 17, iota v * (iota v - 10) ≤ -21 := by
    intro v
    have hv := iotaBounds v
    have hprod : (iota v - 3) * (iota v - 7) ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos (by omega) (by omega)
    nlinarith
  have specialTermUpper : iota w * (iota w - 10) ≤ -24 := by
    have hwBounds := iotaBounds w
    have hprod : (iota w - 4) * (iota w - 6) ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos (by omega) (by omega)
    nlinarith
  have adjustedTermUpper : ∀ v : Fin 17,
      iota v * (iota v - 10) ≤ -21 - (if v = w then 3 else 0) := by
    intro v
    by_cases hv : v = w
    · subst v
      simpa using specialTermUpper
    · simp [hv, termUpper v]
  have termSumUpper : (∑ v, iota v * (iota v - 10)) ≤ -360 := by
    have hsum := Finset.sum_le_sum fun v (_ : v ∈ Finset.univ) =>
      adjustedTermUpper v
    simpa [Finset.sum_sub_distrib] using hsum
  have gammaThreeUpper : gammaThree ≤ -6 := by omega
  have gammaThreeExact : gammaThree = -6 := by omega
  have linkSumNonnegative : 0 ≤ ∑ v, linkGammaTwo v :=
    Finset.sum_nonneg fun v _ => linkGammaTwoNonnegative v
  have gammaTwoExact : gammaTwo = 5 := by omega
  have iotaSumExact : ∑ v, iota v = 52 := by omega
  have excessSum : (∑ v, (iota v - 3)) = 1 := by
    calc
      (∑ v, (iota v - 3)) = (∑ v, iota v) - ∑ _v : Fin 17, (3 : ℤ) := by
        rw [Finset.sum_sub_distrib]
      _ = (∑ v, iota v) - 51 := by norm_num
      _ = 1 := by omega
  have iotaUpperFour : ∀ v, iota v ≤ 4 := by
    intro v
    have singleBound : iota v - 3 ≤ ∑ u, (iota u - 3) :=
      Finset.single_le_sum (f := fun u : Fin 17 => iota u - 3)
        (fun u (_ : u ∈ Finset.univ) => by
          have hu := (iotaBounds u).1
          omega)
        (Finset.mem_univ v)
    omega
  have iotaThreeOrFour : ∀ v, iota v = 3 ∨ iota v = 4 := by
    intro v
    have := (iotaBounds v).1
    have := iotaUpperFour v
    omega
  have exactTerm : ∀ v : Fin 17,
      iota v * (iota v - 10) = -21 - 3 * (iota v - 3) := by
    intro v
    rcases iotaThreeOrFour v with hv | hv <;> simp [hv]
  have termSumExact : (∑ v, iota v * (iota v - 10)) = -360 := by
    calc
      (∑ v, iota v * (iota v - 10)) =
          ∑ v, (-21 - 3 * (iota v - 3)) := by
            apply Finset.sum_congr rfl
            intro v _
            exact exactTerm v
      _ = (∑ _v : Fin 17, (-21 : ℤ)) - 3 * ∑ v, (iota v - 3) := by
        rw [Finset.sum_sub_distrib, Finset.mul_sum]
      _ = -360 := by rw [excessSum]; norm_num
  have triangleCountExact : triangleCount = 0 := by omega
  have linkSumExact : (∑ v, linkGammaTwo v) = 2 := by omega
  let high : Finset (Fin 17) := Finset.univ.filter fun v => iota v ≠ 3
  have highIndicator :
      (∑ v : Fin 17, (if iota v = 3 then 0 else 1 : ℤ)) = high.card := by
    calc
      (∑ v : Fin 17, (if iota v = 3 then 0 else 1 : ℤ)) =
          ∑ v : Fin 17, (if iota v ≠ 3 then 1 else 0 : ℤ) := by
            apply Finset.sum_congr rfl
            intro v _
            split_ifs <;> simp_all
      _ = high.card := by
        simpa only [high] using
          (Finset.natCast_card_filter (R := ℤ)
            (fun v : Fin 17 => iota v ≠ 3)
            (Finset.univ : Finset (Fin 17))).symm
  have highCardUpper : high.card ≤ 1 := by
    have indicatorBound :
        (∑ v : Fin 17, (if iota v = 3 then 0 else 1 : ℤ)) ≤
          ∑ v, (iota v - 3) := by
      exact Finset.sum_le_sum fun v _ => by
        split_ifs with hv
        · omega
        · have := (iotaBounds v).1
          omega
    rw [highIndicator, excessSum] at indicatorBound
    exact_mod_cast indicatorBound
  have highCardPositive : 1 ≤ high.card := by
    apply Finset.one_le_card.mpr
    exact ⟨w, by simp [high, hw]⟩
  have highCardExact : high.card = 1 := by omega
  have partition :=
    Finset.card_filter_add_card_filter_not
      (s := (Finset.univ : Finset (Fin 17))) (fun v => iota v = 3)
  have minimumCard :
      (Finset.univ.filter fun v => iota v = 3).card = 16 := by
    dsimp [high] at highCardExact
    have universeCard : (Finset.univ : Finset (Fin 17)).card = 17 := by simp
    omega
  exact ⟨gammaTwoExact, gammaThreeExact, triangleCountExact, linkSumExact,
    iotaThreeOrFour, minimumCard⟩

end PolarArithmetic

section ThirdAntipodeEscape

variable {V : Type*}

/-!
The Labbé--Nevo two-antipode separator argument has an exact failure mode at
polar size three.  If the antipodes contain a path `x-y-z`, the edge `x-y`
may remain contraction-obstructed only through a four-cycle which uses the
third antipode `z`.  The following theorem extracts the resulting witness in
the vertex link of `v`.  The hypothesis `everyCycleUsesThird` is the
Jordan--Alexander conclusion for cycles avoiding `z`; it is intentionally
kept as an imported topological premise.
-/

/--
The unique third-antipode escape for a path edge produces a link vertex
adjacent to both path endpoints and nonadjacent to the middle vertex.
-/
theorem pathAntipodes_force_link_escapeWitness
    (G : SimpleGraph V) (v x y z : V)
    (vNotAdjacentX : ¬G.Adj v x)
    (onlyThreeAntipodes :
      ∀ w, w ≠ v → w ≠ x → w ≠ y → w ≠ z → G.Adj v w)
    (yzEdge : G.Adj y z)
    (xyCycle : EdgeInInducedFourCycle G x y)
    (everyCycleUsesThird :
      ∀ a b, IsInducedFourCycle G x y a b → a = z ∨ b = z) :
    ∃ w, G.Adj v w ∧ G.Adj z w ∧ G.Adj w x ∧ ¬G.Adj y w := by
  obtain ⟨a, b, hdistinct, hxy, hya, hab, hbx, hxa, hyb⟩ := xyCycle
  rcases everyCycleUsesThird a b
      ⟨hdistinct, hxy, hya, hab, hbx, hxa, hyb⟩ with ha | hb
  · subst a
    have hbv : b ≠ v := by
      intro hbv
      subst b
      exact vNotAdjacentX hbx
    have hlink : G.Adj v b :=
      onlyThreeAntipodes b hbv hdistinct.2.2.1.symm
        hdistinct.2.2.2.2.1.symm hdistinct.2.2.2.2.2.symm
    exact ⟨b, hlink, hab, hbx, hyb⟩
  · subst b
    exact False.elim (hyb yzEdge)

end ThirdAntipodeEscape

#print axioms eval_negOne_derivative_hFive
#print axioms eval_negOne_derivative_vertexLinkRhs
#print axioms sum_vertexLink_gammaTwo_eq
#print axioms negative_forces_polarSize_three
#print axioms gammaTwo_bounds_of_negative
#print axioms gammaThree_lower_bound_of_negative
#print axioms antipode_and_linkGammaOne_ranges
#print axioms minimumLink_gamma_profile
#print axioms atLeastEight_vertices_have_three_antipodes
#print axioms negative_forces_minimumLink_nonsuspension
#print axioms negative_counterexample_has_eight_nonsuspension_minimumLinks
#print axioms negative_forces_rigid_complement_profile
#print axioms pathAntipodes_force_link_escapeWitness

end CharneyDavis17
