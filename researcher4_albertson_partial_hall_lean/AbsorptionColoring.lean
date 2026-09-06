import TriangleExtraction
import Mathlib.Combinatorics.SimpleGraph.Coloring.Vertex
import Mathlib.Logic.Equiv.Fintype

open Finset

namespace AlbertsonPartialHall

/-- A partial pairing of equally large finite regions extends to a full pairing.
The paired vertices are actual injective maps, not matching ranks. -/
theorem exists_equiv_extending_representatives
    {J A B : Type*} [Finite J] [Fintype A] [Fintype B]
    (hcard : Fintype.card A = Fintype.card B)
    (f : J → A) (g : J → B)
    (hf : Function.Injective f) (hg : Function.Injective g) :
    ∃ e : A ≃ B, ∀ i, e (f i) = g i := by
  let e₀ : A ≃ B := Fintype.equivOfCardEq hcard
  obtain ⟨σ, hσ⟩ := Equiv.Perm.exists_extending_pair
    (fun i => e₀ (f i)) g (e₀.injective.comp hf) hg
  exact ⟨e₀.trans σ, hσ⟩

variable {I A B : Type*} [Fintype I] [Fintype A] [Fintype B]
  [DecidableEq I]

/-- Absorb a common transversal into the paired low regions. All unmatched
indices have fresh colors. No adjacency among the index vertices is assumed. -/
theorem colorable_compl_of_common_representatives
    (H : SimpleGraph (I ⊕ A ⊕ B))
    (hcard : Fintype.card A = Fintype.card B)
    (U : Finset I) (f : U → A) (g : U → B)
    (hf : Function.Injective f) (hg : Function.Injective g)
    (hN : ∀ i : U, H.Adj (Sum.inl (i : I)) (Sum.inr (Sum.inl (f i))))
    (hM : ∀ i : U, H.Adj (Sum.inl (i : I)) (Sum.inr (Sum.inr (g i))))
    (hcross : ∀ a b, H.Adj (Sum.inr (Sum.inl a)) (Sum.inr (Sum.inr b))) :
    Hᶜ.Colorable (Fintype.card A + (Fintype.card I - U.card)) := by
  classical
  obtain ⟨e, he⟩ := exists_equiv_extending_representatives hcard f g hf hg
  let cI : I → A ⊕ {i : I // i ∉ U} := fun i =>
    if hi : i ∈ U then Sum.inl (f ⟨i, hi⟩) else Sum.inr ⟨i, hi⟩
  have hIinj : Function.Injective cI := by
    intro i j hij
    by_cases hi : i ∈ U <;> by_cases hj : j ∈ U
    · have hfg : f ⟨i, hi⟩ = f ⟨j, hj⟩ := by simpa [cI, hi, hj] using hij
      exact congrArg (fun x : U => (x : I)) (hf hfg)
    · simp [cI, hi, hj] at hij
    · simp [cI, hi, hj] at hij
    · simpa [cI, hi, hj] using hij
  have hIa (i : I) (a : A) (h : cI i = Sum.inl a) :
      H.Adj (Sum.inl i) (Sum.inr (Sum.inl a)) := by
    by_cases hi : i ∈ U
    · have ha : f ⟨i, hi⟩ = a := by simpa [cI, hi] using h
      exact ha ▸ hN ⟨i, hi⟩
    · simp [cI, hi] at h
  have hIb (i : I) (b : B) (h : cI i = Sum.inl (e.symm b)) :
      H.Adj (Sum.inl i) (Sum.inr (Sum.inr b)) := by
    by_cases hi : i ∈ U
    · have ha : f ⟨i, hi⟩ = e.symm b := by simpa [cI, hi] using h
      have hb : g ⟨i, hi⟩ = b := by rw [← he, ha, e.apply_symm_apply]
      exact hb ▸ hM ⟨i, hi⟩
    · simp [cI, hi] at h
  let c : I ⊕ A ⊕ B → A ⊕ {i : I // i ∉ U} :=
    Sum.elim cI (Sum.elim Sum.inl (fun b => Sum.inl (e.symm b)))
  have hc : ∀ v w, c v = c w → v = w ∨ H.Adj v w := by
    rintro (i | a | b) (j | a' | b') h
    · exact Or.inl (congrArg Sum.inl (hIinj h))
    · exact Or.inr (hIa i a' h)
    · exact Or.inr (hIb i b' h)
    · exact Or.inr (H.adj_symm (hIa j a h.symm))
    · exact Or.inl (by simpa [c] using h)
    · exact Or.inr (hcross a b')
    · exact Or.inr (H.adj_symm (hIb j b h.symm))
    · exact Or.inr (H.adj_symm (hcross a' b))
    · have hb : e.symm b = e.symm b' := by simpa [c] using h
      exact Or.inl (by rw [e.symm.injective hb])
  let C : Hᶜ.Coloring (A ⊕ {i : I // i ∉ U}) :=
    SimpleGraph.Coloring.mk c (by
      intro v w hvw heq
      rcases hc v w heq with h | h
      · exact hvw.1 h
      · exact hvw.2 h)
  have hleft : Fintype.card {i : I // i ∉ U} = Fintype.card I - U.card := by
    simp [Fintype.card_subtype_compl]
  simpa only [Fintype.card_sum, hleft] using C.colorable

/-- Add an arbitrary finite vertex region with its own palette. No edge
conditions involving this extra region are required. -/
theorem colorable_compl_with_extra_region {V W : Type*} [Fintype W]
    (H : SimpleGraph (V ⊕ W)) {n : ℕ}
    (hc : (H.comap Sum.inl)ᶜ.Colorable n) :
    Hᶜ.Colorable (n + Fintype.card W) := by
  obtain ⟨C⟩ := hc
  let D : Hᶜ.Coloring (Fin n ⊕ W) := SimpleGraph.Coloring.mk
    (Sum.elim (fun v => Sum.inl (C v)) Sum.inr) (by
      rintro (v | w) (v' | w') h heq
      · apply C.valid ⟨fun hv => h.1 (congrArg Sum.inl hv), h.2⟩
        exact Sum.inl.inj heq
      · simp at heq
      · simp at heq
      · exact h.1 (congrArg Sum.inr (Sum.inr.inj heq)))
  simpa only [Fintype.card_sum, Fintype.card_fin] using D.colorable

/-- The complete finite 57-vertex consumer. This proves a genuine complement
coloring, not merely a triangle count. The two extra vertices are unrestricted. -/
theorem colorable_28_of_joint_capacity
    (H : SimpleGraph ((Fin 7 ⊕ Fin 24 ⊕ Fin 24) ⊕ Fin 2))
    (N M : Fin 7 → Finset (Fin 24))
    (hN : ∀ i a, a ∈ N i →
      H.Adj (Sum.inl (Sum.inl i)) (Sum.inl (Sum.inr (Sum.inl a))))
    (hM : ∀ i b, b ∈ M i →
      H.Adj (Sum.inl (Sum.inl i)) (Sum.inl (Sum.inr (Sum.inr b))))
    (hcross : ∀ a b, H.Adj (Sum.inl (Sum.inr (Sum.inl a)))
      (Sum.inl (Sum.inr (Sum.inr b))))
    (hNcol : ∀ a, (univ.filter fun i => a ∈ N i).card ≤ 4)
    (hMcol : ∀ a, (univ.filter fun i => a ∈ M i).card ≤ 4)
    (hrow : ∀ i, (N i).card + (M i).card ≤ 27)
    (hmass : 188 ≤ ∑ i, ((N i).card + (M i).card)) :
    Hᶜ.Colorable 28 := by
  obtain ⟨U, hU, f, g, hf, hg, hmem⟩ :=
    five_representatives_of_joint_capacity N M hNcol hMcol hrow hmass
  have hc := colorable_compl_of_common_representatives (H.comap Sum.inl)
    rfl U f g hf hg (fun i => hN i (f i) (hmem i).1)
    (fun i => hM i (g i) (hmem i).2) hcross
  apply (colorable_compl_with_extra_region H hc).mono
  simp only [Fintype.card_fin]
  omega

end AlbertsonPartialHall
