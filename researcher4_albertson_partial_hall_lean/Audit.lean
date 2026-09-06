import TriangleExtraction

open Finset AlbertsonPartialHall

#print axioms sum_rows_le_union_capacity
#print axioms hall_defect_of_capacity
#print axioms partial_transversal_of_hall_defect
#print axioms common_transversal_of_hall_defects
#print axioms five_common_representatives
#print axioms five_representatives_of_joint_capacity
#print axioms triangle
#print axioms disjoint_triangles
#print axioms triangles_of_common_representatives
#print axioms five_native_triangles_of_joint_capacity

-- Concrete incidence families: every column belongs to four of seven rows.
def firstRows (i : Fin 7) : Finset (Fin 24) :=
  univ.filter fun a => (a.val + i.val) % 7 < 4

def secondRows (i : Fin 7) : Finset (Fin 24) :=
  univ.filter fun a => (a.val + 2 * i.val) % 7 < 4

example : (∑ i, (firstRows i).card) = 96 := by decide
example : (∑ i, (secondRows i).card) = 96 := by decide

example : ∃ U : Finset (Fin 7), 5 ≤ U.card ∧
    ∃ f : U → Fin 24, ∃ g : U → Fin 24,
      Function.Injective f ∧ Function.Injective g ∧
      ∀ i : U, f i ∈ firstRows (i : Fin 7) ∧ g i ∈ secondRows (i : Fin 7) :=
  five_common_representatives firstRows secondRows
    (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)

-- Equality in the mass threshold cannot replace the strict hypothesis.
example : (∑ _i : Fin 2, ({0} : Finset (Fin 2)).card) = 2 * 1 + 2 * (2 - (1 + 0 + 1)) := by decide
example : (∀ _i : Fin 2, 1 ≤ ({0} : Finset (Fin 2)).card ∧
    ({0} : Finset (Fin 2)).card ≤ 2) ∧
    (∀ a : Fin 2, (univ.filter fun _i : Fin 2 => a ∈ ({0} : Finset (Fin 2))).card ≤ 2) := by decide
example : ¬ (∀ S : Finset (Fin 2), S.card ≤ (S.biUnion fun _ => ({0} : Finset (Fin 2))).card) := by decide

-- Empty domains and arbitrary dummy budgets are included.
example : ∃ S : Finset (Fin 0), Fintype.card (Fin 0) ≤ S.card + 3 ∧
    ∃ f : S → Fin 0, Function.Injective f ∧ ∀ i : S, f i ∈ (∅ : Finset (Fin 0)) :=
  partial_transversal_of_hall_defect (fun _ : Fin 0 => (∅ : Finset (Fin 0))) 3 (by
    intro S
    have hc : S.card = 0 := Nat.eq_zero_of_le_zero (card_le_univ S)
    rw [hc]
    exact Nat.zero_le _)

def balancedRows (i : Fin 7) : Finset (Fin 24) :=
  univ.filter fun a => (a.val + i.val + 3) % 7 < 4 ∧
    ¬ (a.val = 0 ∧ (i.val = 0 ∨ i.val = 5 ∨ i.val = 6))

example : (∑ i, ((firstRows i).card + (balancedRows i).card)) = 189 := by decide

example : ∃ U : Finset (Fin 7), 5 ≤ U.card ∧
    ∃ f : U → Fin 24, ∃ g : U → Fin 24,
      Function.Injective f ∧ Function.Injective g ∧
      ∀ i : U, f i ∈ firstRows (i : Fin 7) ∧ g i ∈ balancedRows (i : Fin 7) :=
  five_representatives_of_joint_capacity firstRows balancedRows
    (by decide) (by decide) (by decide) (by decide)

example : (triangle (0 : Fin 2) (0 : Fin 2) (0 : Fin 2)).card = 3 := by decide

-- Reusing a right-side representative creates a genuine vertex collision.
example : ¬ Disjoint (triangle (0 : Fin 2) (0 : Fin 2) (0 : Fin 2))
    (triangle (1 : Fin 2) (0 : Fin 2) (1 : Fin 2)) := by decide

example : (⊤ : SimpleGraph (Fin 2 ⊕ Fin 2 ⊕ Fin 2)).IsNClique 3
    (triangle (0 : Fin 2) (0 : Fin 2) (0 : Fin 2)) := by
  apply SimpleGraph.is3Clique_triple_iff.mpr
  simp
