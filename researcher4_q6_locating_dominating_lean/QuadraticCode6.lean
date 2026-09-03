import Mathlib
import LocatingDominating
import LowerBoundInfrastructure

/-!
# The quadratic 16-word locating-dominating code in the binary 6-cube

This file kernel-checks the finite construction in the reviewed Discovery Net
finding. The published general lower bound remains an explicit hypothesis of
the optimality theorem.
-/

open Finset

namespace Q6LocatingDominating

/-- The binary Hamming cube on a finite coordinate type. -/
def hammingCube (I : Type*) [Fintype I] [DecidableEq I] :
    SimpleGraph (I → Bool) :=
  SimpleGraph.fromRel fun x y ↦
    ((univ.filter fun i ↦ x i ≠ y i).card = 1)

/-- Adjacency in a finite Hamming cube is decidable definitionally. -/
instance hammingCubeDecidableAdj (I : Type*) [Fintype I] [DecidableEq I] :
    DecidableRel (hammingCube I).Adj :=
  fun x y ↦ inferInstanceAs <|
    Decidable (x ≠ y ∧
      (((univ.filter fun i ↦ x i ≠ y i).card = 1) ∨
        ((univ.filter fun i ↦ y i ≠ x i).card = 1)))

/-- Addition in the two-element field, presented on Booleans. -/
def add2 (a b : Bool) : Bool := a.xor b

/-- The reviewed quadratic code, using zero-based coordinates. -/
def quadraticCode6 : Finset (Fin 6 → Bool) :=
  univ.filter fun x ↦
    x 1 = add2 (add2 (add2 (add2 (x 0) (x 3)) (x 4)) (x 5)) false ∧
    x 2 = add2 (add2 (add2 (add2 (x 0) (x 3)) (x 5)) ((x 0) && (x 4)))
      ((x 0) && (x 5))

theorem quadraticCode6_card : quadraticCode6.card = 16 := by
  decide

set_option maxRecDepth 500000
set_option maxHeartbeats 0

/-- The generic son bound specialized to `Q₆`, with the elementary cube
closed-neighborhood intersection property left explicit.  A direct `decide`
proof of that property through the current nested `Finset` representation is
not a small checker; a coordinate-level Hamming-distance proof is preferable. -/
theorem q6_card_sons_le_choose
    (D : Finset (Fin 6 → Bool))
    (hD : (hammingCube (Fin 6)).IsLocatingDominating D)
    (hsmall :
      (hammingCube (Fin 6)).ClosedNeighborhoodIntersectionsAtMostTwo)
    (x : Fin 6 → Bool) (hx : (hammingCube (Fin 6)).IsFather D x) :
    ((hammingCube (Fin 6)).sons D x).card ≤
      Nat.choose ((hammingCube (Fin 6)).locatingSignature D x).card 2 :=
  SimpleGraph.IsLocatingDominating.card_sons_le_choose
    (hammingCube (Fin 6)) hD hsmall hx

/-- The 16-word quadratic code is locating-dominating in `Q₆`. This is a
kernel evaluation of all 64 vertices and all pairs of non-codewords. -/
theorem quadraticCode6_isLocatingDominating :
    (hammingCube (Fin 6)).IsLocatingDominating quadraticCode6 := by
  unfold SimpleGraph.IsLocatingDominating
  decide

/-- The three signature sizes occur equally often among the 48 non-codewords. -/
theorem quadraticCode6_signature_distribution :
    (univ.filter fun v : Fin 6 → Bool ↦
      v ∉ quadraticCode6 ∧
        ((hammingCube (Fin 6)).locatingSignature quadraticCode6 v).card = 1).card = 16 ∧
    (univ.filter fun v : Fin 6 → Bool ↦
      v ∉ quadraticCode6 ∧
        ((hammingCube (Fin 6)).locatingSignature quadraticCode6 v).card = 2).card = 16 ∧
    (univ.filter fun v : Fin 6 → Bool ↦
      v ∉ quadraticCode6 ∧
        ((hammingCube (Fin 6)).locatingSignature quadraticCode6 v).card = 3).card = 16 := by
  decide

/-- The code contains no adjacent pair, matching the review's independent
incidence check. -/
theorem quadraticCode6_independent :
    ∀ ⦃u v⦄, u ∈ quadraticCode6 → v ∈ quadraticCode6 →
      ¬ (hammingCube (Fin 6)).Adj u v := by
  decide

/-- Every product lift of the quadratic code is locating-dominating. -/
theorem quadraticCode6_product_lift (m : ℕ) :
    ((hammingCube (Fin 6)) □ (hammingCube (Fin m))).IsLocatingDominating
      (quadraticCode6 ×ˢ (univ : Finset (Fin m → Bool))) :=
  SimpleGraph.IsLocatingDominating.boxProd_univ _ _
    quadraticCode6_isLocatingDominating

/-- The product lift has the claimed size `16 · 2^m`. -/
theorem quadraticCode6_product_lift_card (m : ℕ) :
    (quadraticCode6 ×ˢ (univ : Finset (Fin m → Bool))).card = 16 * 2 ^ m := by
  simp [quadraticCode6_card]

/-- The numerical specialization of the Honkala--Laihonen--Ranto lower bound:
its rational inequality forces every locating-dominating code in `Q₆` to
have at least 16 words. -/
theorem card_ge_sixteen_of_HLR_bound
    (D : Finset (Fin 6 → Bool))
    (h : (288 : ℚ) / 19 ≤ D.card) :
    16 ≤ D.card := by
  have hq : (15 : ℚ) < D.card := lt_of_lt_of_le (by norm_num) h
  have hn : 15 < D.card := by exact_mod_cast hq
  omega

/-- Conditional exact theorem alignment. The finite upper bound is fully
checked above; the only hypothesis is the published general lower bound,
specialized to `Q₆`. -/
theorem quadraticCode6_isMinimum_of_HLR_bound
    (HLR : ∀ D : Finset (Fin 6 → Bool),
      (hammingCube (Fin 6)).IsLocatingDominating D →
        (288 : ℚ) / 19 ≤ D.card) :
    (hammingCube (Fin 6)).IsMinimumLocatingDominating quadraticCode6 := by
  refine ⟨quadraticCode6_isLocatingDominating, ?_⟩
  intro D hD
  rw [quadraticCode6_card]
  exact card_ge_sixteen_of_HLR_bound D (HLR D hD)

end Q6LocatingDominating

#print axioms Q6LocatingDominating.quadraticCode6_isLocatingDominating
#print axioms Q6LocatingDominating.q6_card_sons_le_choose
#print axioms Q6LocatingDominating.quadraticCode6_product_lift
#print axioms Q6LocatingDominating.quadraticCode6_isMinimum_of_HLR_bound
