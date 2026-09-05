import AlbertsonReservoirCapacity
import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected

/-!
# Singleton deletion components and the complement-degree bound

The component hypotheses are native Mathlib support equalities. Their
neighborhood containment feeds the reservoir theorem and then actual degrees.
-/

open Set SimpleGraph

namespace AlbertsonNeighborhoodObstruction

variable {V : Type*} {H G : SimpleGraph V}

/-- A singleton component after deleting a set has no neighbors outside that set. -/
theorem neighborSet_subset_of_singleton_component {B : Set V} (w : ↑(Bᶜ))
    (hw : ((H.induce Bᶜ).connectedComponentMk w).supp = {w}) :
    H.neighborSet w.val ⊆ B := by
  intro u hwu
  by_contra hu
  let u' : ↑(Bᶜ) := ⟨u, hu⟩
  have hmem : u' ∈ ((H.induce Bᶜ).connectedComponentMk w).supp :=
    ConnectedComponent.mem_supp_of_adj_mem_supp _ rfl
      (show (H.induce Bᶜ).Adj w u' from hwu)
  rw [hw] at hmem
  have heq : u = w.val := congrArg Subtype.val (Set.mem_singleton_iff.mp hmem)
  exact hwu.ne heq.symm

/-- Two neighborhood sets confined to a set plus one vertex have combined
size at most two more than that set when their intersections with it are disjoint. -/
theorem card_add_card_le_of_singleton_overlap [DecidableEq V]
    (Q N₁ N₂ : Finset V) (s : V)
    (h₁ : N₁ ⊆ insert s Q) (h₂ : N₂ ⊆ insert s Q)
    (hd : Disjoint (Q ∩ N₁) (Q ∩ N₂)) :
    N₁.card + N₂.card ≤ Q.card + 2 := by
  have hu : N₁ ∪ N₂ ⊆ insert s Q := Finset.union_subset h₁ h₂
  have hi : N₁ ∩ N₂ ⊆ {s} := by
    intro x hx
    rcases Finset.mem_inter.mp hx with ⟨hx₁, hx₂⟩
    by_cases hxs : x = s
    · simpa using hxs
    · have hxQ := (Finset.mem_insert.mp (h₁ hx₁)).resolve_left hxs
      exact (Finset.disjoint_left.mp hd
        (Finset.mem_inter.mpr ⟨hxQ, hx₁⟩) (Finset.mem_inter.mpr ⟨hxQ, hx₂⟩)).elim
  have huc := (Finset.card_le_card hu).trans (Finset.card_insert_le s Q)
  have hic := Finset.card_le_card hi
  have hid := Finset.card_union_add_card_inter N₁ N₂
  simp only [Finset.card_singleton] at hic
  omega

/-- Actual singleton deletion components supply all neighborhood and nonedge
premises of the critical-coloring two-singleton theorem. -/
theorem disjoint_clique_neighbors_of_singleton_components
    {k : ℕ} (hchi : G.chromaticNumber = (k : ℕ∞) + 1)
    {Q : Set V} {s : V} (hQ : Gᶜ.IsClique Q)
    (hdrop : ∀ a ∈ Q, (G.induce {x | x ≠ a}).chromaticNumber < G.chromaticNumber)
    (w z : ↑((Q ∪ {s})ᶜ)) (hwz : w ≠ z)
    (hw : ((Gᶜ.induce (Q ∪ {s})ᶜ).connectedComponentMk w).supp = {w})
    (hz : ((Gᶜ.induce (Q ∪ {s})ᶜ).connectedComponentMk z).supp = {z}) :
    Disjoint (Q ∩ Gᶜ.neighborSet w.val) (Q ∩ Gᶜ.neighborSet z.val) := by
  have hNw := neighborSet_subset_of_singleton_component w hw
  have hNz := neighborSet_subset_of_singleton_component z hz
  exact disjoint_clique_neighbors_of_chromatic_drop hchi hQ hdrop
    (fun heq => hwz (Subtype.ext heq)) (fun hadj => z.property (hNw hadj)) hNw hNz

/-- Two singleton components outside a complement clique plus one vertex have
combined complement degree at most the clique size plus two. -/
theorem degree_add_degree_le_of_singleton_components
    [Fintype V] [DecidableEq V] [DecidableRel G.Adj]
    {k : ℕ} (hchi : G.chromaticNumber = (k : ℕ∞) + 1)
    (Q : Finset V) (s : V) (hQ : Gᶜ.IsClique (Q : Set V))
    (hdrop : ∀ a ∈ Q, (G.induce {x | x ≠ a}).chromaticNumber < G.chromaticNumber)
    (w z : ↑(((Q : Set V) ∪ {s})ᶜ)) (hwz : w ≠ z)
    (hw : ((Gᶜ.induce ((Q : Set V) ∪ {s})ᶜ).connectedComponentMk w).supp = {w})
    (hz : ((Gᶜ.induce ((Q : Set V) ∪ {s})ᶜ).connectedComponentMk z).supp = {z}) :
    Gᶜ.degree w.val + Gᶜ.degree z.val ≤ Q.card + 2 := by
  have hNw := neighborSet_subset_of_singleton_component w hw
  have hNz := neighborSet_subset_of_singleton_component z hz
  have hd := disjoint_clique_neighbors_of_singleton_components hchi hQ hdrop w z hwz hw hz
  have h₁ : Gᶜ.neighborFinset w.val ⊆ insert s Q := by
    intro x hx
    rcases hNw ((Gᶜ.mem_neighborFinset w.val x).mp hx) with hxQ | hxs
    · exact Finset.mem_insert_of_mem hxQ
    · exact Finset.mem_insert.mpr (Or.inl (Set.mem_singleton_iff.mp hxs))
  have h₂ : Gᶜ.neighborFinset z.val ⊆ insert s Q := by
    intro x hx
    rcases hNz ((Gᶜ.mem_neighborFinset z.val x).mp hx) with hxQ | hxs
    · exact Finset.mem_insert_of_mem hxQ
    · exact Finset.mem_insert.mpr (Or.inl (Set.mem_singleton_iff.mp hxs))
  have hdis : Disjoint (Q ∩ Gᶜ.neighborFinset w.val) (Q ∩ Gᶜ.neighborFinset z.val) := by
    rw [Finset.disjoint_left]
    intro x hx hy
    exact Set.disjoint_left.mp hd
      ⟨(Finset.mem_inter.mp hx).1, (Gᶜ.mem_neighborFinset w.val x).mp (Finset.mem_inter.mp hx).2⟩
      ⟨(Finset.mem_inter.mp hy).1, (Gᶜ.mem_neighborFinset z.val x).mp (Finset.mem_inter.mp hy).2⟩
  exact card_add_card_le_of_singleton_overlap Q _ _ s h₁ h₂ hdis

end AlbertsonNeighborhoodObstruction
