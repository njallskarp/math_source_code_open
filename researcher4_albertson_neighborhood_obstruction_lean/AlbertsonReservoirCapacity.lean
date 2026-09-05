import Mathlib.Combinatorics.SimpleGraph.Coloring.Vertex
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic.SplitIfs

/-!
# Deletion-coloring reservoir capacity

An explicit coloring extension proves that every color sees the deleted vertex.
Common complement neighbors confined to a clique plus a reservoir then inject
into that reservoir. The singleton case closes the two-singleton interface.
-/

open Set SimpleGraph

namespace AlbertsonNeighborhoodObstruction

variable {V A : Type*} {G : SimpleGraph V} {a : V}

/-- Extend a deletion coloring with a color absent from the deleted vertex's neighbors. -/
noncomputable def extendDeletionColoring
    (C : (G.induce {x | x ≠ a}).Coloring A) (c : A)
    (hmiss : ∀ u : {x | x ≠ a}, G.Adj a u → C u ≠ c) : G.Coloring A := by
  classical
  refine Coloring.mk (fun x => if h : x = a then c else C ⟨x, h⟩) ?_
  intro x y hxy
  by_cases hx : x = a
  · subst x
    have hy : y ≠ a := hxy.ne.symm
    simpa [hy] using (hmiss ⟨y, hy⟩ hxy).symm
  · by_cases hy : y = a
    · subst y
      simpa [hx] using hmiss ⟨x, hx⟩ hxy.symm
    · simpa [hx, hy] using C.valid (show
        (G.induce {x | x ≠ a}).Adj ⟨x, hx⟩ ⟨y, hy⟩ from hxy)

/-- Every color of an insufficient deletion palette occurs on a neighbor of a. -/
theorem exists_neighbor_of_color [Fintype A]
    (C : (G.induce {x | x ≠ a}).Coloring A)
    (hchi : (Fintype.card A : ℕ∞) < G.chromaticNumber) (c : A) :
    ∃ u : {x | x ≠ a}, G.Adj a u ∧ C u = c := by
  classical
  by_contra hn
  push Not at hn
  exact (not_le_of_gt hchi) (extendDeletionColoring C c hn).colorable.chromaticNumber_le

/-- A class containing a common complement neighbor must meet the reservoir. -/
theorem exists_reservoir_same_color [Fintype A]
    (C : (G.induce {x | x ≠ a}).Coloring A)
    (hchi : (Fintype.card A : ℕ∞) < G.chromaticNumber)
    {Q R : Set V} (hQ : Gᶜ.IsClique Q) (ha : a ∈ Q)
    {w : V} (haw : Gᶜ.Adj a w) (hN : Gᶜ.neighborSet w ⊆ Q ∪ R) :
    ∃ u : {x | x ≠ a}, u.val ∈ R ∧ C u = C ⟨w, haw.ne.symm⟩ := by
  obtain ⟨u, hau, hcolor⟩ := exists_neighbor_of_color C hchi (C ⟨w, haw.ne.symm⟩)
  have hwu : w ≠ u.val := by
    intro heq
    exact haw.2 (heq.symm ▸ hau)
  have hcomp : Gᶜ.Adj w u.val := by
    refine ⟨hwu, ?_⟩
    intro hgu
    exact C.valid (show (G.induce {x | x ≠ a}).Adj
      ⟨w, haw.ne.symm⟩ u from hgu) hcolor.symm
  rcases hN hcomp with huQ | huR
  · exact ((hQ ha huQ hau.ne).2 hau).elim
  · exact ⟨u, huR, hcolor⟩

/-- Independent complement vertices sharing a clique vertex have distinct
reservoir representatives. All independence, boundary, and color facts are native. -/
theorem exists_reservoir_injection [Fintype A]
    (C : (G.induce {x | x ≠ a}).Coloring A)
    (hchi : (Fintype.card A : ℕ∞) < G.chromaticNumber)
    {Q W R : Set V} (hQ : Gᶜ.IsClique Q) (ha : a ∈ Q)
    (hW : Gᶜ.IsIndepSet W) (hadj : ∀ w ∈ W, Gᶜ.Adj a w)
    (hN : ∀ w ∈ W, Gᶜ.neighborSet w ⊆ Q ∪ R) :
    Nonempty (W ↪ R) := by
  classical
  have hex (w : W) := exists_reservoir_same_color C hchi hQ ha
    (hadj w w.property) (hN w w.property)
  choose f hf hcolor using hex
  let F : W → R := fun w => ⟨(f w).val, hf w⟩
  refine ⟨⟨F, ?_⟩⟩
  intro w z heq
  by_contra hwz
  have hne : w.val ≠ z.val := fun h => hwz (Subtype.ext h)
  have hclique : G.IsClique W := (G.isIndepSet_compl).mp hW
  have hcol := C.valid (show (G.induce {x | x ≠ a}).Adj
    ⟨w.val, (hadj w w.property).ne.symm⟩
    ⟨z.val, (hadj z z.property).ne.symm⟩ from hclique w.property z.property hne)
  have hval : (f w).val = (f z).val := congrArg (fun r : R => (r : V)) heq
  have hfz : f w = f z := Subtype.ext hval
  exact hcol ((hcolor w).symm.trans (hfz ▸ hcolor z))

/-- The parameterized finite capacity bound, with no graph-order assumption. -/
theorem reservoir_card_bound [Fintype A]
    (C : (G.induce {x | x ≠ a}).Coloring A)
    (hchi : (Fintype.card A : ℕ∞) < G.chromaticNumber)
    {Q : Set V} (W R : Finset V) (hQ : Gᶜ.IsClique Q) (ha : a ∈ Q)
    (hW : Gᶜ.IsIndepSet W) (hadj : ∀ w ∈ W, Gᶜ.Adj a w)
    (hN : ∀ w ∈ W, Gᶜ.neighborSet w ⊆ Q ∪ (R : Set V)) :
    W.card ≤ R.card := by
  obtain ⟨f⟩ := exists_reservoir_injection C hchi hQ ha hW hadj hN
  simpa using Fintype.card_le_of_injective f f.injective

/-- Two independent complement vertices cannot share a clique neighbor when
their only possible reservoir is one vertex. -/
theorem not_common_neighbor_of_singleton_reservoir [Fintype A]
    (C : (G.induce {x | x ≠ a}).Coloring A)
    (hchi : (Fintype.card A : ℕ∞) < G.chromaticNumber)
    {Q : Set V} {w z s : V} (hQ : Gᶜ.IsClique Q) (ha : a ∈ Q)
    (hwz : w ≠ z) (hnot : ¬Gᶜ.Adj w z)
    (hNw : Gᶜ.neighborSet w ⊆ Q ∪ {s})
    (hNz : Gᶜ.neighborSet z ⊆ Q ∪ {s}) :
    ¬(Gᶜ.Adj a w ∧ Gᶜ.Adj a z) := by
  classical
  rintro ⟨haw, haz⟩
  have hgz : G.Adj w z := by
    by_contra hn
    exact hnot ⟨hwz, hn⟩
  have hW : Gᶜ.IsIndepSet (↑({w, z} : Finset V) : Set V) := by
    simpa only [Finset.coe_pair, G.isIndepSet_compl, isClique_pair] using
      (fun (_ : w ≠ z) => hgz)
  have hbound := reservoir_card_bound C hchi ({w, z} : Finset V) {s} hQ ha hW
    (by simpa using And.intro haw haz)
    (by simpa using And.intro hNw hNz)
  simp [hwz] at hbound

/-- The two singleton components have disjoint neighbor sets inside the clique.
Deletion colorings are required only for vertices of that clique. -/
theorem disjoint_clique_neighbors_of_singleton_reservoir [Fintype A]
    {Q : Set V} {w z s : V} (hQ : Gᶜ.IsClique Q)
    (hdelete : ∀ a ∈ Q, Nonempty ((G.induce {x | x ≠ a}).Coloring A))
    (hchi : (Fintype.card A : ℕ∞) < G.chromaticNumber)
    (hwz : w ≠ z) (hnot : ¬Gᶜ.Adj w z)
    (hNw : Gᶜ.neighborSet w ⊆ Q ∪ {s})
    (hNz : Gᶜ.neighborSet z ⊆ Q ∪ {s}) :
    Disjoint (Q ∩ Gᶜ.neighborSet w) (Q ∩ Gᶜ.neighborSet z) := by
  rw [Set.disjoint_left]
  intro a hwa hza
  obtain ⟨C⟩ := hdelete a hwa.1
  exact not_common_neighbor_of_singleton_reservoir C hchi hQ hwa.1 hwz hnot
    hNw hNz ⟨hwa.2.symm, hza.2.symm⟩

/-- Finite chromatic number and strict drops supply the deletion colorings
through Mathlib, without any large-class or special deletion-cover hypothesis. -/
theorem disjoint_clique_neighbors_of_chromatic_drop
    {k : ℕ} (hchi : G.chromaticNumber = (k : ℕ∞) + 1)
    {Q : Set V} {w z s : V} (hQ : Gᶜ.IsClique Q)
    (hdrop : ∀ a ∈ Q, (G.induce {x | x ≠ a}).chromaticNumber < G.chromaticNumber)
    (hwz : w ≠ z) (hnot : ¬Gᶜ.Adj w z)
    (hNw : Gᶜ.neighborSet w ⊆ Q ∪ {s})
    (hNz : Gᶜ.neighborSet z ⊆ Q ∪ {s}) :
    Disjoint (Q ∩ Gᶜ.neighborSet w) (Q ∩ Gᶜ.neighborSet z) := by
  apply disjoint_clique_neighbors_of_singleton_reservoir (A := Fin k) hQ
    (fun a ha => chromaticNumber_le_iff_colorable.mp
      (Order.le_of_lt_add_one (hchi ▸ hdrop a ha)))
    (by rw [Fintype.card_fin, hchi]; exact_mod_cast Nat.lt_succ_self k)
    hwz hnot hNw hNz

end AlbertsonNeighborhoodObstruction
