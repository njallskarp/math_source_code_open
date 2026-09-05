import Mathlib.Combinatorics.SimpleGraph.Coloring.Vertex
import Mathlib.Tactic.SplitIfs

/-!
# Critical-vertex neighborhood obstruction

Neighborhood folding preserves chromatic number. Its complement form proves
the non-domination and clique-barrier step of Discovery Net height 2933 without
an order assumption, Stehlik's theorem, a matching, or a crossing model.
-/

open Set SimpleGraph

namespace AlbertsonNeighborhoodObstruction

variable {V : Type*} {G : SimpleGraph V}

/-- Fold a vertex onto a different vertex with a containing open neighborhood. -/
noncomputable def foldHom {a w : V} (haw : a ≠ w)
    (hN : G.neighborSet a ⊆ G.neighborSet w) :
    G →g G.induce {x | x ≠ a} := by
  classical
  refine ⟨fun x => if h : x = a then ⟨w, haw.symm⟩ else ⟨x, h⟩, ?_⟩
  intro x y hxy
  change G.Adj _ _
  by_cases hx : x = a
  · subst x
    have hy : y ≠ a := hxy.ne.symm
    simpa [hy] using hN hxy
  · by_cases hy : y = a
    · subst y
      simpa [hx] using (hN hxy.symm).symm
    · simpa [hx, hy] using hxy

/-- No finiteness assumption is required: both inequalities come from actual
graph homomorphisms and use Mathlib's extended-natural chromatic number. -/
theorem chromaticNumber_delete_eq_of_neighborSet_subset {a w : V} (haw : a ≠ w)
    (hN : G.neighborSet a ⊆ G.neighborSet w) :
    (G.induce {x | x ≠ a}).chromaticNumber = G.chromaticNumber := by
  exact le_antisymm
    (chromaticNumber_mono_of_hom (Embedding.induce {x | x ≠ a}).toHom)
    (chromaticNumber_mono_of_hom (foldHom haw hN))

/-- Strict chromatic drop at just `a` already prohibits this neighborhood inclusion. -/
theorem not_neighborSet_subset_of_chromatic_drop {a w : V} (haw : a ≠ w)
    (hdrop : (G.induce {x | x ≠ a}).chromaticNumber < G.chromaticNumber) :
    ¬ G.neighborSet a ⊆ G.neighborSet w := by
  intro hN
  exact hdrop.ne (chromaticNumber_delete_eq_of_neighborSet_subset haw hN)

/-- Exact complement translation: local domination gives a fold in the original graph. -/
theorem neighborSet_subset_of_compl_domination {a w : V} (hwa : Gᶜ.Adj w a)
    (hdom : ∀ u, Gᶜ.Adj w u → u ≠ a → Gᶜ.Adj a u) :
    G.neighborSet a ⊆ G.neighborSet w := by
  intro u hau
  change G.Adj a u at hau
  change G.Adj w u
  by_contra hwu
  have hne : w ≠ u := by
    intro heq
    subst u
    exact hwa.2 hau.symm
  exact (hdom u ⟨hne, hwu⟩ hau.ne.symm).2 hau

/-- Every complement neighbor of a chromatically essential vertex's neighbor
has a witness preventing domination. No special deletion-cover shape is needed. -/
theorem exists_compl_neighbor_not_adjacent {a w : V} (hwa : Gᶜ.Adj w a)
    (hdrop : (G.induce {x | x ≠ a}).chromaticNumber < G.chromaticNumber) :
    ∃ u, Gᶜ.Adj w u ∧ u ≠ a ∧ ¬ Gᶜ.Adj a u := by
  classical
  by_contra hn
  push Not at hn
  exact not_neighborSet_subset_of_chromatic_drop hwa.ne.symm hdrop
    (neighborSet_subset_of_compl_domination hwa hn)

/-- If every vertex deletion lowers the chromatic number, a nonempty complement
neighborhood cannot be contained in a complement clique. This is the local
clique-barrier obstruction; the set `B` need not be a Tutte barrier. -/
theorem not_isClique_of_neighborSet_subset
    (hcritical : ∀ a, (G.induce {x | x ≠ a}).chromaticNumber < G.chromaticNumber)
    {w : V} {B : Set V} (hne : (Gᶜ.neighborSet w).Nonempty)
    (hNB : Gᶜ.neighborSet w ⊆ B) : ¬ Gᶜ.IsClique B := by
  intro hB
  obtain ⟨a, hwa⟩ := hne
  obtain ⟨u, hwu, hua, hnau⟩ := exists_compl_neighbor_not_adjacent hwa (hcritical a)
  exact hnau (hB (hNB hwa) (hNB hwu) hua.symm)

end AlbertsonNeighborhoodObstruction
