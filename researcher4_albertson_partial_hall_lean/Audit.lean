import AbsorptionColoring

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
#print axioms exists_equiv_extending_representatives
#print axioms colorable_compl_of_common_representatives
#print axioms colorable_compl_with_extra_region
#print axioms colorable_28_of_joint_capacity

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

-- Empty regions and empty representative sets require no positive-size guard.
example (H : SimpleGraph (Fin 0 ⊕ Fin 0 ⊕ Fin 0)) : Hᶜ.Colorable 0 := by
  simpa using colorable_compl_of_common_representatives H rfl ∅
    (fun i => Fin.elim0 i.val) (fun i => Fin.elim0 i.val)
    (fun i => Fin.elim0 i.val) (fun i => Fin.elim0 i.val)
    (fun i => Fin.elim0 i.val) (fun i => Fin.elim0 i.val)
    (fun a => Fin.elim0 a)

-- Full-domain identity extension.
example : ∃ e : Fin 3 ≃ Fin 3, ∀ i : Fin 3, e i = i :=
  exists_equiv_extending_representatives rfl id id
    Function.injective_id Function.injective_id

-- Four genuine triangles and complete cross-region adjacency do not suffice
-- for 28 colors. This fixture is NOT claimed to satisfy the joint mass 188.
def fourTriangleGraph : SimpleGraph (Fin 9 ⊕ Fin 24 ⊕ Fin 24) :=
  SimpleGraph.fromRel fun v w => match v, w with
    | Sum.inl i, Sum.inr (Sum.inl a) => i.val < 4 ∧ i.val = a.val
    | Sum.inl i, Sum.inr (Sum.inr b) => i.val < 4 ∧ i.val = b.val
    | Sum.inr (Sum.inl _), Sum.inr (Sum.inr _) => True
    | _, _ => False

example : ∀ a b : Fin 24,
    fourTriangleGraph.Adj (Sum.inr (Sum.inl a)) (Sum.inr (Sum.inr b)) := by
  intro a b
  simp [fourTriangleGraph, SimpleGraph.fromRel_adj]

example : ∀ i : Fin 4, fourTriangleGraph.IsNClique 3
    (triangle (i.castLE (by decide) : Fin 9)
      (i.castLE (by decide) : Fin 24) (i.castLE (by decide) : Fin 24)) := by
  intro i
  apply SimpleGraph.is3Clique_triple_iff.mpr
  simp [fourTriangleGraph, SimpleGraph.fromRel_adj, i.isLt]

example : ∀ i j : Fin 4, i ≠ j → Disjoint
    (triangle (i.castLE (by decide) : Fin 9)
      (i.castLE (by decide) : Fin 24) (i.castLE (by decide) : Fin 24))
    (triangle (j.castLE (by decide) : Fin 9)
      (j.castLE (by decide) : Fin 24) (j.castLE (by decide) : Fin 24)) := by decide

example : ¬ fourTriangleGraphᶜ.Colorable 28 := by
  let k : Fin 24 ⊕ Fin 5 → Fin 9 ⊕ Fin 24 ⊕ Fin 24 :=
    Sum.elim (fun a => Sum.inr (Sum.inl a))
      (fun i => Sum.inl ⟨i.val + 4, by omega⟩)
  have hk : Pairwise fun i j => fourTriangleGraphᶜ.Adj (k i) (k j) := by
    rintro (a | i) (b | j) h
    · simp_all [k, fourTriangleGraph, SimpleGraph.fromRel_adj]
    · simp [k, fourTriangleGraph, SimpleGraph.fromRel_adj]
    · simp [k, fourTriangleGraph, SimpleGraph.fromRel_adj]
    · simp_all [k, fourTriangleGraph, SimpleGraph.fromRel_adj, Fin.val_inj]
  intro hc
  have h := hc.card_le_of_pairwise_adj k hk
  norm_num at h

-- End-to-end native graph with exactly the tested incidences, complete low
-- cross edges and no edge incident to either extra vertex.
def capacityGraph : SimpleGraph ((Fin 7 ⊕ Fin 24 ⊕ Fin 24) ⊕ Fin 2) :=
  SimpleGraph.fromRel fun v w => match v, w with
    | Sum.inl (Sum.inl i), Sum.inl (Sum.inr (Sum.inl a)) => a ∈ firstRows i
    | Sum.inl (Sum.inl i), Sum.inl (Sum.inr (Sum.inr b)) => b ∈ balancedRows i
    | Sum.inl (Sum.inr (Sum.inl _)), Sum.inl (Sum.inr (Sum.inr _)) => True
    | _, _ => False

example : capacityGraphᶜ.Colorable 28 :=
  colorable_28_of_joint_capacity capacityGraph firstRows balancedRows
    (by intros; simp_all [capacityGraph, SimpleGraph.fromRel_adj])
    (by intros; simp_all [capacityGraph, SimpleGraph.fromRel_adj])
    (by intros; simp [capacityGraph, SimpleGraph.fromRel_adj])
    (by decide) (by decide) (by decide) (by decide)

example : ∀ w : Fin 2, ∀ v, ¬ capacityGraph.Adj (Sum.inr w) v := by
  rintro w ((i | a | b) | w') <;> simp [capacityGraph, SimpleGraph.fromRel_adj]
