import AbsorptionColoring

open Finset

namespace AlbertsonPartialHall

/-- Canonical adjacency rows in a labeled finite region. -/
def neighborsIn {V T : Type*} [Fintype T] (H : SimpleGraph V)
    [DecidableRel H.Adj] (v : V) (f : T → V) : Finset T :=
  univ.filter fun t => H.Adj v (f t)

theorem card_filter_sum_regions {A B : Type*} [Fintype A] [Fintype B]
    (p : A ⊕ B → Prop) [DecidablePred p] :
    (univ.filter p).card = (univ.filter fun a => p (Sum.inl a)).card +
      (univ.filter fun b => p (Sum.inr b)).card := by
  classical
  have h : univ.filter p = (univ.filter fun a => p (Sum.inl a)).disjSum
      (univ.filter fun b => p (Sum.inr b)) := by
    ext x
    cases x <;> simp
  rw [h, card_disjSum]

/-- Count the same graph incidences from either labeled region. No
injectivity is needed: repeated labels are counted on both sides. -/
theorem sum_neighborsIn_comm {V A B : Type*} [Fintype A] [Fintype B]
    (H : SimpleGraph V) [DecidableRel H.Adj] (f : A → V) (g : B → V) :
    (∑ a, (neighborsIn H (f a) g).card) =
      ∑ b, (neighborsIn H (g b) f).card := by
  classical
  simpa [neighborsIn, bipartiteAbove, bipartiteBelow, H.adj_comm] using
    sum_card_bipartiteAbove_eq_sum_card_bipartiteBelow
      (fun a b => H.Adj (f a) (g b)) (s := univ) (t := univ)

section FourRegions

variable {I A B W : Type*} [Fintype I] [Fintype A] [Fintype B] [Fintype W]

abbrev indexVertex (i : I) : (I ⊕ A ⊕ B) ⊕ W := Sum.inl (Sum.inl i)
abbrev firstVertex (a : A) : (I ⊕ A ⊕ B) ⊕ W := Sum.inl (Sum.inr (Sum.inl a))
abbrev secondVertex (b : B) : (I ⊕ A ⊕ B) ⊕ W := Sum.inl (Sum.inr (Sum.inr b))
abbrev extraVertex (w : W) : (I ⊕ A ⊕ B) ⊕ W := Sum.inr w

variable (H : SimpleGraph ((I ⊕ A ⊕ B) ⊕ W)) [DecidableRel H.Adj]

/-- Native degree decomposes over the four disjoint sum regions. -/
theorem degree_four_regions (v : (I ⊕ A ⊕ B) ⊕ W) :
    H.degree v = (neighborsIn H v indexVertex).card +
      (neighborsIn H v firstVertex).card + (neighborsIn H v secondVertex).card +
      (neighborsIn H v extraVertex).card := by
  simp only [SimpleGraph.degree, SimpleGraph.neighborFinset_eq_filter,
    card_filter_sum_regions, neighborsIn, indexVertex, firstVertex, secondVertex, extraVertex]
  omega

/-- Exact graph-to-summary bridge for an induced complete bipartite low
region. The row and column bounds and total incidence balance are derived
from native degrees, not supplied as independent data. -/
theorem incidence_summary_of_degrees (dA dB : ℕ)
    (hAA : ∀ a a', ¬ H.Adj (firstVertex a) (firstVertex a'))
    (hBB : ∀ b b', ¬ H.Adj (secondVertex b) (secondVertex b'))
    (hcross : ∀ a b, H.Adj (firstVertex a) (secondVertex b))
    (hdegA : ∀ a, H.degree (firstVertex a) = dA)
    (hdegB : ∀ b, H.degree (secondVertex b) = dB) :
    (∀ a, (neighborsIn H (firstVertex a) indexVertex).card ≤ dA - Fintype.card B) ∧
    (∀ b, (neighborsIn H (secondVertex b) indexVertex).card ≤ dB - Fintype.card A) ∧
    (∀ i, (neighborsIn H (indexVertex i) firstVertex).card +
      (neighborsIn H (indexVertex i) secondVertex).card ≤ H.degree (indexVertex i)) ∧
    (∑ i, ((neighborsIn H (indexVertex i) firstVertex).card +
      (neighborsIn H (indexVertex i) secondVertex).card)) +
      (∑ w, ((neighborsIn H (extraVertex w) firstVertex).card +
        (neighborsIn H (extraVertex w) secondVertex).card)) +
      2 * Fintype.card A * Fintype.card B = Fintype.card A * dA + Fintype.card B * dB := by
  have hA (a : A) : (neighborsIn H (firstVertex a) indexVertex).card +
      (neighborsIn H (firstVertex a) extraVertex).card + Fintype.card B = dA := by
    have h := degree_four_regions H (firstVertex a)
    simp only [hdegA, neighborsIn, hAA, hcross, filter_false, card_empty,
      filter_true, card_univ] at h
    simp only [neighborsIn]
    omega
  have hB (b : B) : (neighborsIn H (secondVertex b) indexVertex).card +
      (neighborsIn H (secondVertex b) extraVertex).card + Fintype.card A = dB := by
    have h := degree_four_regions H (secondVertex b)
    have hcross' : ∀ a, H.Adj (secondVertex b) (firstVertex a) :=
      fun a => H.adj_symm (hcross a b)
    simp only [hdegB, neighborsIn, hBB, hcross', filter_false, card_empty,
      filter_true, card_univ] at h
    simp only [neighborsIn]
    omega
  refine ⟨fun a => by have := hA a; omega, fun b => by have := hB b; omega, ?_, ?_⟩
  · intro i
    have := degree_four_regions H (indexVertex i)
    omega
  · have hsA := sum_congr rfl (fun a (_ : a ∈ (univ : Finset A)) => hA a)
    have hsB := sum_congr rfl (fun b (_ : b ∈ (univ : Finset B)) => hB b)
    simp only [sum_add_distrib, sum_const, card_univ, smul_eq_mul] at hsA hsB
    rw [sum_neighborsIn_comm H firstVertex indexVertex,
      sum_neighborsIn_comm H firstVertex extraVertex] at hsA
    rw [sum_neighborsIn_comm H secondVertex indexVertex,
      sum_neighborsIn_comm H secondVertex extraVertex] at hsB
    rw [sum_add_distrib, sum_add_distrib]
    nlinarith

end FourRegions

/-- Structural graph consumer: no arbitrary row families or externally
computed incidence mass remain. The extra-to-low budget is an explicit
graph quantity; its derivation from a Tutte barrier remains external. -/
theorem colorable_28_of_degree_partition
    (H : SimpleGraph ((Fin 7 ⊕ Fin 24 ⊕ Fin 24) ⊕ Fin 2)) [DecidableRel H.Adj]
    (hAA : ∀ a a', ¬ H.Adj (firstVertex a) (firstVertex a'))
    (hBB : ∀ b b', ¬ H.Adj (secondVertex b) (secondVertex b'))
    (hcross : ∀ a b, H.Adj (firstVertex a) (secondVertex b))
    (hdegA : ∀ a, H.degree (firstVertex a) = 28)
    (hdegB : ∀ b, H.degree (secondVertex b) = 28)
    (hdegI : ∀ i, H.degree (indexVertex i) ≤ 27)
    (hbudget : (∑ w, ((neighborsIn H (extraVertex w) firstVertex).card +
      (neighborsIn H (extraVertex w) secondVertex).card)) ≤ 4) :
    Hᶜ.Colorable 28 := by
  obtain ⟨hA, hB, hI, hmass⟩ :=
    incidence_summary_of_degrees H 28 28 hAA hBB hcross hdegA hdegB
  simp only [Fintype.card_fin] at hA hB hmass
  apply colorable_28_of_joint_capacity H
    (fun i => neighborsIn H (indexVertex i) firstVertex)
    (fun i => neighborsIn H (indexVertex i) secondVertex)
  · intro i a ha
    exact (mem_filter.mp ha).2
  · intro i b hb
    exact (mem_filter.mp hb).2
  · exact hcross
  · intro a
    simpa [neighborsIn, H.adj_comm] using hA a
  · intro b
    simpa [neighborsIn, H.adj_comm] using hB b
  · intro i
    exact (hI i).trans (hdegI i)
  · omega

end AlbertsonPartialHall
