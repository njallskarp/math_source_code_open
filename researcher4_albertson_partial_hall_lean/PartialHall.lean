import Mathlib.Combinatorics.Hall.Finite
import Mathlib.Combinatorics.Enumerative.DoubleCounting
import Mathlib.Data.Finset.Sum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Choose

/-! Incidence capacity implies Hall with a deficit.
No graph classification, crossing estimate or source table is imported. -/

open Finset

namespace AlbertsonPartialHall

variable {I A : Type*} [Fintype I] [DecidableEq I] [DecidableEq A]

omit [DecidableEq I] in
theorem sum_rows_le_union_capacity (N : I → Finset A) (c : ℕ)
    (hcol : ∀ a, (univ.filter fun i => a ∈ N i).card ≤ c) (S : Finset I) :
    (∑ i ∈ S, (N i).card) ≤ c * (S.biUnion N).card := by
  classical
  have heq := sum_card_bipartiteAbove_eq_sum_card_bipartiteBelow
    (fun i a => a ∈ N i) (s := S) (t := S.biUnion N)
  have hleft : ∀ i ∈ S, (S.biUnion N).bipartiteAbove (fun i a => a ∈ N i) i = N i := by
    intro i hi
    ext a
    simp only [mem_bipartiteAbove]
    exact ⟨And.right, fun ha => ⟨mem_biUnion.mpr ⟨i, hi, ha⟩, ha⟩⟩
  have hsum : (∑ i ∈ S, (N i).card) =
      ∑ a ∈ S.biUnion N, (S.filter fun i => a ∈ N i).card := by
    simpa only [sum_congr rfl (fun i hi => congrArg card (hleft i hi)), bipartiteBelow]
      using heq
  rw [hsum]
  calc
    _ ≤ ∑ _a ∈ S.biUnion N, c := sum_le_sum fun a _ =>
      (card_le_card (filter_subset_filter _ (subset_univ S))).trans (hcol a)
    _ = _ := by simp [Nat.mul_comm]

/-- A strict incidence surplus rules out every Hall deficit larger than d. -/
theorem hall_defect_of_capacity (N : I → Finset A) (q c δ d : ℕ)
    (hcq : c ≤ q) (hsize : δ + d + 1 ≤ Fintype.card I)
    (hmin : ∀ i, δ ≤ (N i).card) (hmax : ∀ i, (N i).card ≤ q)
    (hcol : ∀ a, (univ.filter fun i => a ∈ N i).card ≤ c)
    (hmass : c * δ + q * (Fintype.card I - (δ + d + 1)) < ∑ i, (N i).card) :
    ∀ S : Finset I, S.card ≤ (S.biUnion N).card + d := by
  intro S
  by_contra hbad
  have hS : S.Nonempty := card_pos.mp (by omega)
  obtain ⟨i, hi⟩ := hS
  have hu : δ ≤ (S.biUnion N).card :=
    (hmin i).trans (card_le_card (subset_biUnion_of_mem N hi))
  have hs : δ + d + 1 ≤ S.card := by omega
  have hsn : S.card ≤ Fintype.card I := card_le_univ S
  have hsmall := sum_rows_le_union_capacity N c hcol S
  have hrest : (∑ i ∈ Sᶜ, (N i).card) ≤ q * (Fintype.card I - S.card) := by
    calc
      _ ≤ ∑ _i ∈ Sᶜ, q := sum_le_sum fun i _ => hmax i
      _ = _ := by simp [card_compl, Nat.mul_comm]
  have hsplit : (∑ i ∈ S, (N i).card) + (∑ i ∈ Sᶜ, (N i).card) =
      ∑ i, (N i).card := sum_add_sum_compl S _
  have hnsub : Fintype.card I - S.card + S.card = Fintype.card I := Nat.sub_add_cancel hsn
  have hbase : Fintype.card I - (δ + d + 1) + (δ + d + 1) = Fintype.card I :=
    Nat.sub_add_cancel hsize
  have hslack : (q - c) * (S.card - (δ + d + 1)) ≥ 0 := Nat.zero_le _
  have hqc : q - c + c = q := Nat.sub_add_cancel hcq
  have hsc : S.card - (δ + d + 1) + (δ + d + 1) = S.card := Nat.sub_add_cancel hs
  have hU : (S.biUnion N).card + d + 1 ≤ S.card := by omega
  have hm := Nat.mul_le_mul_left c hU
  nlinarith

/-- Hall with d universal dummy representatives gives a genuine partial
transversal, omitting at most d original indices. -/
theorem partial_transversal_of_hall_defect (N : I → Finset A) (d : ℕ)
    (hHall : ∀ S : Finset I, S.card ≤ (S.biUnion N).card + d) :
    ∃ S : Finset I, Fintype.card I ≤ S.card + d ∧
      ∃ f : S → A, Function.Injective f ∧ ∀ i : S, f i ∈ N (i : I) := by
  classical
  let M : I → Finset (Fin d ⊕ A) := fun i => univ.disjSum (N i)
  have hM : ∀ S : Finset I, S.card ≤ (S.biUnion M).card := by
    intro S
    obtain rfl | hS := S.eq_empty_or_nonempty
    · simp
    have heq : S.biUnion M = (univ : Finset (Fin d)).disjSum (S.biUnion N) := by
      ext x
      cases x with
      | inl a => simpa [M, Finset.Nonempty] using hS
      | inr a => simp [M]
    rw [heq, card_disjSum, card_univ, Fintype.card_fin]
    simpa [Nat.add_comm] using hHall S
  obtain ⟨f, hf, hmem⟩ := (all_card_le_biUnion_card_iff_existsInjective' M).mp hM
  let S : Finset I := univ.filter fun i => ∃ a, f i = Sum.inr a
  have hbad : (Sᶜ).card ≤ d := by
    calc
      _ = ((Sᶜ).image f).card := (card_image_of_injective _ hf).symm
      _ ≤ ((univ : Finset (Fin d)).map Function.Embedding.inl).card := by
        apply card_le_card
        intro x hx
        obtain ⟨i, hi, rfl⟩ := mem_image.mp hx
        cases hfi : f i with
        | inl a => simp
        | inr a =>
          have hin : i ∈ S := mem_filter.mpr ⟨mem_univ _, ⟨a, hfi⟩⟩
          exact False.elim ((mem_compl.mp hi) hin)
      _ = d := by simp
  have hgood : ∀ i : S, ∃ a, f i = Sum.inr a := fun i => (mem_filter.mp i.2).2
  choose g hg using hgood
  refine ⟨S, ?_, g, ?_, ?_⟩
  · rw [card_compl] at hbad
    have := card_le_univ S
    omega
  · intro i j hij
    apply Subtype.ext
    apply hf
    rw [hg i, hg j, hij]
  · intro i
    have hm := hmem i
    rw [hg i] at hm
    simpa [M] using hm

/-- Independent partial transversals have a common domain losing at most
the sum of their deficits. The returned maps are actual injective choices. -/
theorem common_transversal_of_hall_defects {B : Type*} [DecidableEq B]
    (N : I → Finset A) (M : I → Finset B) (d e : ℕ)
    (hN : ∀ S : Finset I, S.card ≤ (S.biUnion N).card + d)
    (hM : ∀ S : Finset I, S.card ≤ (S.biUnion M).card + e) :
    ∃ U : Finset I, Fintype.card I ≤ U.card + d + e ∧
      ∃ f : U → A, ∃ g : U → B,
        Function.Injective f ∧ Function.Injective g ∧
        ∀ i : U, f i ∈ N (i : I) ∧ g i ∈ M (i : I) := by
  obtain ⟨S, hS, f, hf, hmemf⟩ := partial_transversal_of_hall_defect N d hN
  obtain ⟨T, hT, g, hg, hmemg⟩ := partial_transversal_of_hall_defect M e hM
  let U := S ∩ T
  let left : U → S := fun i => ⟨i, (mem_inter.mp i.2).1⟩
  let right : U → T := fun i => ⟨i, (mem_inter.mp i.2).2⟩
  refine ⟨U, ?_, f ∘ left, g ∘ right, ?_, ?_, ?_⟩
  · have hcard := card_union_add_card_inter S T
    have hle := card_le_univ (S ∪ T)
    dsimp [U]
    omega
  · apply hf.comp
    intro i j hij
    exact Subtype.ext (congrArg (fun x : S => (x : I)) hij)
  · apply hg.comp
    intro i j hij
    exact Subtype.ext (congrArg (fun x : T => (x : I)) hij)
  · intro i
    exact ⟨hmemf (left i), hmemg (right i)⟩

/-- The finite incidence interface needed by the newly pinned Albertson case.
Each side separately needs more than 80 incidences; the graph application
supplies at least 92. No graph-realization or coloring hypothesis is hidden. -/
theorem five_common_representatives (N M : Fin 7 → Finset (Fin 24))
    (hNmin : ∀ i, 2 ≤ (N i).card) (hMmin : ∀ i, 2 ≤ (M i).card)
    (hNcol : ∀ a, (univ.filter fun i => a ∈ N i).card ≤ 4)
    (hMcol : ∀ a, (univ.filter fun i => a ∈ M i).card ≤ 4)
    (hNmass : 80 < ∑ i, (N i).card) (hMmass : 80 < ∑ i, (M i).card) :
    ∃ U : Finset (Fin 7), 5 ≤ U.card ∧
      ∃ f : U → Fin 24, ∃ g : U → Fin 24,
        Function.Injective f ∧ Function.Injective g ∧
        ∀ i : U, f i ∈ N (i : Fin 7) ∧ g i ∈ M (i : Fin 7) := by
  have hN := hall_defect_of_capacity N 24 4 2 1 (by decide) (by decide) hNmin
    (fun i => card_le_univ (N i)) hNcol (by simpa using hNmass)
  have hM := hall_defect_of_capacity M 24 4 2 1 (by decide) (by decide) hMmin
    (fun i => card_le_univ (M i)) hMcol (by simpa using hMmass)
  obtain ⟨U, hU, f, g, hf, hg, hmem⟩ := common_transversal_of_hall_defects N M 1 1 hN hM
  refine ⟨U, ?_, f, g, hf, hg, hmem⟩
  simpa using hU

/-- Derive the local row minima and both side masses from joint incidence
data, rather than accepting separately manufactured matching ranks. -/
theorem five_representatives_of_joint_capacity (N M : Fin 7 → Finset (Fin 24))
    (hNcol : ∀ a, (univ.filter fun i => a ∈ N i).card ≤ 4)
    (hMcol : ∀ a, (univ.filter fun i => a ∈ M i).card ≤ 4)
    (hrow : ∀ i, (N i).card + (M i).card ≤ 27)
    (hmass : 188 ≤ ∑ i, ((N i).card + (M i).card)) :
    ∃ U : Finset (Fin 7), 5 ≤ U.card ∧
      ∃ f : U → Fin 24, ∃ g : U → Fin 24,
        Function.Injective f ∧ Function.Injective g ∧
        ∀ i : U, f i ∈ N (i : Fin 7) ∧ g i ∈ M (i : Fin 7) := by
  have hNmax (i) : (N i).card ≤ 24 := card_le_univ (N i)
  have hMmax (i) : (M i).card ≤ 24 := card_le_univ (M i)
  have hmin (i : Fin 7) : 26 ≤ (N i).card + (M i).card := by
    have hs : (∑ j ∈ univ.erase i, ((N j).card + (M j).card)) ≤ 162 := by
      calc
        _ ≤ ∑ _j ∈ univ.erase i, 27 := sum_le_sum fun j _ => hrow j
        _ = 162 := by simp
    have he := sum_erase_add (univ : Finset (Fin 7))
      (fun j => (N j).card + (M j).card) (mem_univ i)
    omega
  have hbound (F : Fin 7 → Finset (Fin 24))
      (hF : ∀ a, (univ.filter fun i => a ∈ F i).card ≤ 4) :
      (∑ i, (F i).card) ≤ 96 := by
    have h := sum_rows_le_union_capacity F 4 hF univ
    have hu : (univ.biUnion F).card ≤ 24 := card_le_univ _
    omega
  have hbN := hbound N hNcol
  have hbM := hbound M hMcol
  rw [sum_add_distrib] at hmass
  exact five_common_representatives N M
    (fun i => by have := hmin i; have := hMmax i; omega)
    (fun i => by have := hmin i; have := hNmax i; omega)
    hNcol hMcol (by omega) (by omega)

end AlbertsonPartialHall
