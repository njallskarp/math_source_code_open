import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Tactic

/-!
# The admissible-edge obstruction at the 17-vertex Charney--Davis boundary

This file checks two exact finite interfaces used by the proposed contraction
argument for a flag generalized homology 5-sphere on 17 vertices.

* The edge-subdivision identity for the h-polynomials of a 5-sphere, its
  contracted 5-sphere, and its edge link forces
  `gammaThree = contractedGammaThree + linkGammaTwo`.
* If every admissible edge would imply nonnegativity of `gammaThree`, then a
  negative counterexample has every edge in an induced four-cycle.

The topological statements that an admissible contraction preserves the flag
generalized-homology-sphere property, that the h-polynomial recurrence applies,
and that the two smaller gamma entries are nonnegative are deliberately passed
as hypotheses. No custom axioms are introduced.
-/

namespace CharneyDavis17

open Polynomial

section GammaPolynomial

/-- The gamma-basis expansion of a degree-six h-polynomial. -/
noncomputable def hSix (gammaZero gammaOne gammaTwo gammaThree : ℤ) : Polynomial ℤ :=
  C gammaZero * (1 + X) ^ 6 +
    C gammaOne * X * (1 + X) ^ 4 +
    C gammaTwo * X ^ 2 * (1 + X) ^ 2 +
    C gammaThree * X ^ 3

/-- The gamma-basis expansion of a degree-four h-polynomial. -/
noncomputable def hFour (gammaZero gammaOne gammaTwo : ℤ) : Polynomial ℤ :=
  C gammaZero * (1 + X) ^ 4 +
    C gammaOne * X * (1 + X) ^ 2 +
    C gammaTwo * X ^ 2

/-- At `t = -1`, a degree-six h-polynomial retains only `-gammaThree`. -/
@[simp]
theorem eval_negOne_hSix
    (gammaZero gammaOne gammaTwo gammaThree : ℤ) :
    eval (-1) (hSix gammaZero gammaOne gammaTwo gammaThree) = -gammaThree := by
  norm_num [hSix]

/-- At `t = -1`, a degree-four h-polynomial retains only `gammaTwo`. -/
@[simp]
theorem eval_negOne_hFour (gammaZero gammaOne gammaTwo : ℤ) :
    eval (-1) (hFour gammaZero gammaOne gammaTwo) = gammaTwo := by
  norm_num [hFour]

/--
The degree-six/degree-four h-polynomial recurrence forces the top gamma
coefficient recurrence. This is the exact algebraic bridge used for an edge
contraction of a 5-sphere.
-/
theorem gammaThree_eq_of_hPolynomial_recurrence
    (deltaZero deltaOne deltaTwo deltaThree : ℤ)
    (contractedZero contractedOne contractedTwo contractedThree : ℤ)
    (linkZero linkOne linkTwo : ℤ)
    (hRecurrence :
      hSix deltaZero deltaOne deltaTwo deltaThree =
        hSix contractedZero contractedOne contractedTwo contractedThree +
          X * hFour linkZero linkOne linkTwo) :
    deltaThree = contractedThree + linkTwo := by
  have evaluated := congrArg (eval (-1)) hRecurrence
  have h : -deltaThree = -contractedThree + -linkTwo := by
    simpa using evaluated
  omega

/--
The formal conditional Charney--Davis step: the h-polynomial recurrence and
nonnegativity of the contracted top gamma entry and link top gamma entry imply
nonnegativity of the original top gamma entry.
-/
theorem charneyDavis_of_admissibleEdge_data
    (deltaZero deltaOne deltaTwo deltaThree : ℤ)
    (contractedZero contractedOne contractedTwo contractedThree : ℤ)
    (linkZero linkOne linkTwo : ℤ)
    (hRecurrence :
      hSix deltaZero deltaOne deltaTwo deltaThree =
        hSix contractedZero contractedOne contractedTwo contractedThree +
          X * hFour linkZero linkOne linkTwo)
    (contractedNonnegative : 0 ≤ contractedThree)
    (linkNonnegative : 0 ≤ linkTwo) :
    0 ≤ deltaThree := by
  rw [gammaThree_eq_of_hPolynomial_recurrence _ _ _ _ _ _ _ _ _ _ _ hRecurrence]
  omega

end GammaPolynomial

section InducedFourCycle

variable {V : Type*}

/-- The six pairwise inequalities for four vertices in cyclic order. -/
def PairwiseDistinctFour (u v a b : V) : Prop :=
  u ≠ v ∧ u ≠ a ∧ u ≠ b ∧ v ≠ a ∧ v ≠ b ∧ a ≠ b

/--
The ordered vertices `u,v,a,b` span an induced four-cycle with cyclic edges
`uv`, `va`, `ab`, `bu` and missing diagonals `ua`, `vb`.
-/
def IsInducedFourCycle (G : SimpleGraph V) (u v a b : V) : Prop :=
  PairwiseDistinctFour u v a b ∧
    G.Adj u v ∧ G.Adj v a ∧ G.Adj a b ∧ G.Adj b u ∧
      ¬G.Adj u a ∧ ¬G.Adj v b

/-- An edge is contained in an induced four-cycle. -/
def EdgeInInducedFourCycle (G : SimpleGraph V) (u v : V) : Prop :=
  ∃ a b, IsInducedFourCycle G u v a b

/--
A local cross-neighborhood witness: one endpoint has an exclusive neighbor
`a`, the other has an exclusive neighbor `b`, and `a,b` are adjacent.
-/
def CrossNeighborhoodWitness (G : SimpleGraph V) (u v a b : V) : Prop :=
  G.Adj v a ∧ ¬G.Adj u a ∧ a ≠ u ∧
    G.Adj u b ∧ ¬G.Adj v b ∧ b ≠ v ∧ G.Adj a b

/--
An edge lies in an induced four-cycle exactly when its two exclusive
neighborhoods contain adjacent vertices. This local form avoids enumerating
four-cycles.
-/
theorem edgeInInducedFourCycle_iff_crossNeighborhood
    (G : SimpleGraph V) (u v : V) :
    EdgeInInducedFourCycle G u v ↔
      G.Adj u v ∧ ∃ a b, CrossNeighborhoodWitness G u v a b := by
  constructor
  · rintro ⟨a, b, hdistinct, huv, hva, hab, hbu, hua, hvb⟩
    refine ⟨huv, a, b, hva, hua, hdistinct.2.1.symm, hbu.symm, hvb, ?_, hab⟩
    exact hdistinct.2.2.2.2.1.symm
  · rintro ⟨huv, a, b, hva, hua, hau, hub, hvb, hbv, hab⟩
    refine ⟨a, b, ?_, huv, hva, hab, hub.symm, hua, hvb⟩
    exact ⟨huv.ne, hau.symm, hub.ne, hva.ne, hbv.symm, hab.ne⟩

/-- The graph-theoretic admissibility condition for a flag edge contraction. -/
def AdmissibleEdge (G : SimpleGraph V) (u v : V) : Prop :=
  G.Adj u v ∧ ¬EdgeInInducedFourCycle G u v

/-- Every edge is obstructed by an induced four-cycle. -/
def ContractionIrreducible (G : SimpleGraph V) : Prop :=
  ∀ ⦃u v⦄, G.Adj u v → EdgeInInducedFourCycle G u v

/-- A graph has no admissible edge exactly when every edge has a four-cycle obstruction. -/
theorem not_exists_admissibleEdge_iff_contractionIrreducible (G : SimpleGraph V) :
    (¬∃ u v, AdmissibleEdge G u v) ↔ ContractionIrreducible G := by
  constructor
  · intro hnone u v huv
    by_contra hcycle
    exact hnone ⟨u, v, huv, hcycle⟩
  · intro hirr hexists
    obtain ⟨u, v, huv, hcycle⟩ := hexists
    exact hcycle (hirr huv)

/--
The exact minimal-counterexample obstruction. If every admissible edge would
prove nonnegativity, then a negative gamma-three counterexample is contraction
irreducible, hence every edge lies in an induced four-cycle.
-/
theorem negative_gammaThree_forces_contractionIrreducible
    (G : SimpleGraph V) (gammaThree : ℤ)
    (negative : gammaThree < 0)
    (admissibleEdgeStep :
      ∀ ⦃u v⦄, AdmissibleEdge G u v → 0 ≤ gammaThree) :
    ContractionIrreducible G := by
  intro u v huv
  by_contra hcycle
  have nonnegative := admissibleEdgeStep ⟨huv, hcycle⟩
  omega

end InducedFourCycle

#print axioms eval_negOne_hSix
#print axioms eval_negOne_hFour
#print axioms gammaThree_eq_of_hPolynomial_recurrence
#print axioms charneyDavis_of_admissibleEdge_data
#print axioms edgeInInducedFourCycle_iff_crossNeighborhood
#print axioms not_exists_admissibleEdge_iff_contractionIrreducible
#print axioms negative_gammaThree_forces_contractionIrreducible

end CharneyDavis17
