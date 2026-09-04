import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Finset.Card
import Lean.Elab.Tactic.Omega

namespace RamseyLinkFan

/-- Ceiling division by four, in an `omega`-friendly normal form. -/
def ceilDivFour (n : Nat) : Nat := (n + 3) / 4

/-- A four-capacity cover of `n` objects needs at least `ceilDivFour n` sets. -/
theorem ceilDivFour_le_of_le_mul_four {n k : Nat} (h : n ≤ k * 4) :
    ceilDivFour n ≤ k := by
  unfold ceilDivFour
  omega

/-- In the relevant degree range, `ceil ((rho - 3) / 4) = rho / 4`. -/
theorem ceilDivFour_sub_three {rho : Nat} (h : 3 ≤ rho) :
    ceilDivFour (rho - 3) = rho / 4 := by
  unfold ceilDivFour
  omega

/-- The Ramsey-neighborhood interval once the two imported link bounds are supplied. -/
theorem ramsey_link_degree_interval
    {rho blueDegree : Nat}
    (hpartition : rho + blueDegree = 41)
    (hred : rho ≤ 24) (hblue : blueDegree ≤ 24) :
    17 ≤ rho ∧ rho ≤ 24 := by
  omega

/-- A generic capacity bound for a finite cover expressed as a `Finset.biUnion`. -/
theorem card_le_card_mul_of_biUnion_cover
    {V C : Type*} [DecidableEq V] [DecidableEq C]
    (target : Finset V) (clauses : Finset C) (piece : C → Finset V) (q : Nat)
    (cover : target ⊆ clauses.biUnion piece)
    (capacity : ∀ c ∈ clauses, (piece c).card ≤ q) :
    target.card ≤ clauses.card * q := by
  exact (Finset.card_le_card cover).trans
    (Finset.card_biUnion_le_card_mul clauses piece q capacity)

/-- Specialization of the generic cover bound to capacity four and ceiling form. -/
theorem covering_clauses_lower_bound
    {V C : Type*} [DecidableEq V] [DecidableEq C]
    (target : Finset V) (clauses : Finset C) (piece : C → Finset V)
    (cover : target ⊆ clauses.biUnion piece)
    (capacity : ∀ c ∈ clauses, (piece c).card ≤ 4) :
    ceilDivFour target.card ≤ clauses.card := by
  apply ceilDivFour_le_of_le_mul_four
  exact card_le_card_mul_of_biUnion_cover target clauses piece 4 cover capacity

/-- Four pairwise-disjoint finite categories inside `U` consume their summed budget. -/
theorem card_four_pairwise_disjoint_le
    {C : Type*} [DecidableEq C]
    (U R S W X : Finset C)
    (hRS : Disjoint R S) (hRW : Disjoint R W) (hRX : Disjoint R X)
    (hSW : Disjoint S W) (hSX : Disjoint S X) (hWX : Disjoint W X)
    (hsub : R ∪ S ∪ W ∪ X ⊆ U) :
    R.card + S.card + W.card + X.card ≤ U.card := by
  have hRSW : Disjoint (R ∪ S) W := Finset.disjoint_union_left.2 ⟨hRW, hSW⟩
  have hRSWX : Disjoint (R ∪ S ∪ W) X := by
    rw [Finset.disjoint_union_left]
    exact ⟨Finset.disjoint_union_left.2 ⟨hRX, hSX⟩, hWX⟩
  calc
    R.card + S.card + W.card + X.card = (R ∪ S ∪ W ∪ X).card := by
      rw [Finset.card_union_of_disjoint hRSWX,
        Finset.card_union_of_disjoint hRSW,
        Finset.card_union_of_disjoint hRS]
    _ ≤ U.card := Finset.card_le_card hsub

/-- The exact degree-stratified clause-budget inequality. -/
theorem fan_arity_degree_stratified
    {V C : Type*} [DecidableEq V] [DecidableEq C]
    (selected red side witness extra : Finset C)
    (target : Finset V) (piece : C → Finset V)
    (rho m : Nat)
    (hselected : selected.card = 44)
    (hred : 11 ≤ red.card)
    (hside : side.card = m)
    (hwitness : witness.card = 3)
    (hRS : Disjoint red side)
    (hRW : Disjoint red witness)
    (hRX : Disjoint red extra)
    (hSW : Disjoint side witness)
    (hSX : Disjoint side extra)
    (hWX : Disjoint witness extra)
    (hsub : red ∪ side ∪ witness ∪ extra ⊆ selected)
    (htarget : target.card = rho - 3)
    (hcover : target ⊆ extra.biUnion piece)
    (hcapacity : ∀ c ∈ extra, (piece c).card ≤ 4) :
    m + ceilDivFour (rho - 3) ≤ 30 := by
  have hcoverCount : ceilDivFour target.card ≤ extra.card :=
    covering_clauses_lower_bound target extra piece hcover hcapacity
  rw [htarget] at hcoverCount
  have hbudget := card_four_pairwise_disjoint_le selected red side witness extra
    hRS hRW hRX hSW hSX hWX hsub
  omega

/-- The reviewed subtraction form of the degree-stratified fan bound. -/
theorem fan_arity_sub_bound
    {rho m : Nat}
    (hstratified : m + ceilDivFour (rho - 3) ≤ 30) :
    m ≤ 30 - ceilDivFour (rho - 3) := by
  omega

/-- Degree at least 17 turns the stratified bound into the global `m ≤ 26` bound. -/
theorem fan_arity_le_26
    {rho m : Nat}
    (hrho : 17 ≤ rho)
    (hstratified : m + ceilDivFour (rho - 3) ≤ 30) :
    m ≤ 26 := by
  have hceil : ceilDivFour (rho - 3) = rho / 4 :=
    ceilDivFour_sub_three (by omega)
  rw [hceil] at hstratified
  omega

/-- The three degree strata in the reviewed fan-bound table. -/
theorem fan_degree_table
    {rho m : Nat}
    (hrhoLower : 17 ≤ rho) (hrhoUpper : rho ≤ 24)
    (hstratified : m + ceilDivFour (rho - 3) ≤ 30) :
    (rho ≤ 19 → m ≤ 26) ∧
      (20 ≤ rho → rho ≤ 23 → m ≤ 25) ∧
      (rho = 24 → m ≤ 24) := by
  have hceil : ceilDivFour (rho - 3) = rho / 4 :=
    ceilDivFour_sub_three (by omega)
  rw [hceil] at hstratified
  omega

/-- The full abstract finite-clause bridge for the Ramsey-link fan argument. -/
theorem ramsey_link_fan_arity_le_26
    {V C : Type*} [DecidableEq V] [DecidableEq C]
    (selected red side witness extra : Finset C)
    (target : Finset V) (piece : C → Finset V)
    (rho blueDegree m : Nat)
    (hpartition : rho + blueDegree = 41)
    (hredDegree : rho ≤ 24) (hblueDegree : blueDegree ≤ 24)
    (hselected : selected.card = 44)
    (hred : 11 ≤ red.card)
    (hside : side.card = m)
    (hwitness : witness.card = 3)
    (hRS : Disjoint red side)
    (hRW : Disjoint red witness)
    (hRX : Disjoint red extra)
    (hSW : Disjoint side witness)
    (hSX : Disjoint side extra)
    (hWX : Disjoint witness extra)
    (hsub : red ∪ side ∪ witness ∪ extra ⊆ selected)
    (htarget : target.card = rho - 3)
    (hcover : target ⊆ extra.biUnion piece)
    (hcapacity : ∀ c ∈ extra, (piece c).card ≤ 4) :
    m ≤ 26 := by
  have hrho : 17 ≤ rho :=
    (ramsey_link_degree_interval hpartition hredDegree hblueDegree).1
  apply fan_arity_le_26 hrho
  exact fan_arity_degree_stratified selected red side witness extra target piece rho m
    hselected hred hside hwitness hRS hRW hRX hSW hSX hWX hsub htarget hcover hcapacity

#print axioms ceilDivFour_le_of_le_mul_four
#print axioms ceilDivFour_sub_three
#print axioms ramsey_link_degree_interval
#print axioms card_le_card_mul_of_biUnion_cover
#print axioms covering_clauses_lower_bound
#print axioms card_four_pairwise_disjoint_le
#print axioms fan_arity_degree_stratified
#print axioms fan_arity_sub_bound
#print axioms fan_arity_le_26
#print axioms fan_degree_table
#print axioms ramsey_link_fan_arity_le_26

end RamseyLinkFan
