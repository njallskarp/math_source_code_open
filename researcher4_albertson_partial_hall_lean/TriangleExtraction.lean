import PartialHall
import Mathlib.Combinatorics.SimpleGraph.Clique

open Finset

namespace AlbertsonPartialHall

variable {I A B : Type*} [DecidableEq I] [DecidableEq A] [DecidableEq B]

/-- Three disjoint vertex regions, using the standard sum type. -/
def triangle (i : I) (a : A) (b : B) : Finset (I ⊕ A ⊕ B) :=
  {Sum.inl i, Sum.inr (Sum.inl a), Sum.inr (Sum.inr b)}

theorem disjoint_triangles (U : Finset I) (f : U → A) (g : U → B)
    (hf : Function.Injective f) (hg : Function.Injective g)
    (i j : U) (hij : i ≠ j) :
    Disjoint (triangle (i : I) (f i) (g i)) (triangle (j : I) (f j) (g j)) := by
  have ha : f i ≠ f j := fun h => hij (hf h)
  have hb : g i ≠ g j := fun h => hij (hg h)
  simp [triangle, Ne.symm hij, Ne.symm ha, Ne.symm hb]

/-- Actual native-graph triangles, not only arithmetic matching ranks.
The caller states every incidence and the complete cross-region adjacency. -/
theorem triangles_of_common_representatives
    (H : SimpleGraph (I ⊕ A ⊕ B)) (N : I → Finset A) (M : I → Finset B)
    (hN : ∀ i a, a ∈ N i → H.Adj (Sum.inl i) (Sum.inr (Sum.inl a)))
    (hM : ∀ i b, b ∈ M i → H.Adj (Sum.inl i) (Sum.inr (Sum.inr b)))
    (hcross : ∀ a b, H.Adj (Sum.inr (Sum.inl a)) (Sum.inr (Sum.inr b)))
    (U : Finset I) (f : U → A) (g : U → B)
    (hf : Function.Injective f) (hg : Function.Injective g)
    (hmem : ∀ i : U, f i ∈ N (i : I) ∧ g i ∈ M (i : I)) :
    (∀ i : U, H.IsNClique 3 (triangle (i : I) (f i) (g i))) ∧
    ∀ i j : U, i ≠ j →
      Disjoint (triangle (i : I) (f i) (g i)) (triangle (j : I) (f j) (g j)) := by
  refine ⟨?_, disjoint_triangles U f g hf hg⟩
  intro i
  apply SimpleGraph.is3Clique_triple_iff.mpr
  exact ⟨hN i (f i) (hmem i).1, hM i (g i) (hmem i).2, hcross (f i) (g i)⟩

/-- Complete finite incidence-to-native-triangle consumer. -/
theorem five_native_triangles_of_joint_capacity
    (H : SimpleGraph (Fin 7 ⊕ Fin 24 ⊕ Fin 24))
    (N M : Fin 7 → Finset (Fin 24))
    (hN : ∀ i a, a ∈ N i → H.Adj (Sum.inl i) (Sum.inr (Sum.inl a)))
    (hM : ∀ i b, b ∈ M i → H.Adj (Sum.inl i) (Sum.inr (Sum.inr b)))
    (hcross : ∀ a b, H.Adj (Sum.inr (Sum.inl a)) (Sum.inr (Sum.inr b)))
    (hNcol : ∀ a, (univ.filter fun i => a ∈ N i).card ≤ 4)
    (hMcol : ∀ a, (univ.filter fun i => a ∈ M i).card ≤ 4)
    (hrow : ∀ i, (N i).card + (M i).card ≤ 27)
    (hmass : 188 ≤ ∑ i, ((N i).card + (M i).card)) :
    ∃ U : Finset (Fin 7), 5 ≤ U.card ∧
      ∃ T : U → Finset (Fin 7 ⊕ Fin 24 ⊕ Fin 24),
        (∀ i, H.IsNClique 3 (T i) ∧ Sum.inl (i : Fin 7) ∈ T i) ∧
        ∀ i j, i ≠ j → Disjoint (T i) (T j) := by
  obtain ⟨U, hU, f, g, hf, hg, hmem⟩ :=
    five_representatives_of_joint_capacity N M hNcol hMcol hrow hmass
  obtain ⟨htri, hdis⟩ := triangles_of_common_representatives H N M hN hM hcross U f g hf hg hmem
  refine ⟨U, hU, fun i => triangle (i : Fin 7) (f i) (g i), ?_, hdis⟩
  intro i
  exact ⟨htri i, by simp [triangle]⟩

end AlbertsonPartialHall
