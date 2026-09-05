import Mathlib.Combinatorics.Hall.Basic

/-!
# Uniform finite neighborhoods from a matching obstruction

This file isolates the finite-family lemma behind the common-support branch of
the reviewed Albertson two-clique reduction.  Its statement does not mention
drawings, crossing numbers, colorings, subdivisions, or graph topology.

For a family `N : ι → Finset α`, a transversal on `S` chooses one member of
each `N i`, with all choices distinct.  If every row indexed by a finite set
`L` has cardinality `d`, `L` has at least `d + 1` indices, and no `d + 1`
indices admit a transversal, then all rows on `L` are equal.

The proof is a direct application of Mathlib's finite-set form of Hall's
marriage theorem.  Two unequal `d`-element rows in a set of `d + 1` rows make
Hall's inequalities hold: a subfamily of at most `d` rows contains one whole
`d`-element row, while the full subfamily contains the union of two distinct
`d`-element rows and hence at least `d + 1` elements.
-/

namespace AlbertsonUniformRows

/-- A system of distinct representatives for the rows indexed by `S`. -/
def HasTransversalOn {I A : Type*} [DecidableEq I]
    (N : I → Finset A) (S : Finset I) : Prop :=
  ∃ f : {i // i ∈ S} → A, Function.Injective f ∧ ∀ i, f i ∈ N i.1

/-- If a family of `d + 1` many `d`-element rows contains two unequal rows,
then it has a transversal.  This is the local Hall-theoretic kernel. -/
theorem hasTransversalOn_of_card_eq_succ_of_ne
    {I A : Type*} [DecidableEq I] [DecidableEq A]
    (N : I → Finset A) (d : ℕ) (S : Finset I)
    (hS : S.card = d + 1)
    (hcard : ∀ i ∈ S, (N i).card = d)
    {i j : I} (hi : i ∈ S) (hj : j ∈ S) (hij : N i ≠ N j) :
    HasTransversalOn N S := by
  classical
  rw [HasTransversalOn]
  apply (Finset.all_card_le_biUnion_card_iff_exists_injective
    (fun x : {i // i ∈ S} ↦ N x.1)).mp
  intro U
  by_cases hU : U = ∅
  · simp [hU]
  by_cases hUd : U.card ≤ d
  · obtain ⟨x, hx⟩ := U.nonempty_iff_ne_empty.mpr hU
    calc
      U.card ≤ d := hUd
      _ = (N x.1).card := (hcard x.1 x.2).symm
      _ ≤ (U.biUnion (fun y : {i // i ∈ S} ↦ N y.1)).card :=
        Finset.card_le_card (Finset.subset_biUnion_of_mem
          (fun y : {i // i ∈ S} ↦ N y.1) hx)
  · have hUcard : U.card = d + 1 := by
      have hle : U.card ≤ d + 1 := by
        calc
          U.card ≤ Fintype.card {i // i ∈ S} := Finset.card_le_univ U
          _ = S.card := Fintype.card_coe S
          _ = d + 1 := hS
      omega
    have hUuniv : U = Finset.univ := by
      apply Finset.eq_univ_of_card
      rw [hUcard, Fintype.card_coe, hS]
    let ii : {x // x ∈ S} := ⟨i, hi⟩
    let jj : {x // x ∈ S} := ⟨j, hj⟩
    have hNi : N i ⊆ U.biUnion (fun x : {i // i ∈ S} ↦ N x.1) := by
      exact Finset.subset_biUnion_of_mem (fun x : {i // i ∈ S} ↦ N x.1)
        (x := ii) (by rw [hUuniv]; exact Finset.mem_univ ii)
    have hNj : N j ⊆ U.biUnion (fun x : {i // i ∈ S} ↦ N x.1) := by
      exact Finset.subset_biUnion_of_mem (fun x : {i // i ∈ S} ↦ N x.1)
        (x := jj) (by rw [hUuniv]; exact Finset.mem_univ jj)
    have hproper : N i ⊂ N i ∪ N j := by
      refine Finset.ssubset_iff_subset_ne.mpr ⟨Finset.subset_union_left, ?_⟩
      intro heq
      apply hij
      have hsub : N j ⊆ N i := by
        intro x hx
        have hx' : x ∈ N i ∪ N j := Finset.mem_union_right _ hx
        rw [← heq] at hx'
        exact hx'
      exact (Finset.eq_of_subset_of_card_le hsub (by
        rw [hcard i hi, hcard j hj])).symm
    calc
      U.card = d + 1 := hUcard
      _ ≤ (N i ∪ N j).card := by
        have hlt := Finset.card_lt_card hproper
        have hiCard := hcard i hi
        omega
      _ ≤ (U.biUnion (fun x : {i // i ∈ S} ↦ N x.1)).card :=
        Finset.card_le_card (Finset.union_subset hNi hNj)

/-- Uniform-row consequence of a matching-number obstruction.

The hypothesis `hno` says that no `d + 1` rows inside `L` have a system of
distinct representatives.  Equivalently, the associated bipartite incidence
graph has no matching of cardinality `d + 1` with left endpoints in `L`.
-/
theorem all_rows_eq_of_uniform_card_of_no_succ_transversal
    {I A : Type*} [DecidableEq I] [DecidableEq A]
    (N : I → Finset A) (d : ℕ) (L : Finset I)
    (hL : d + 1 ≤ L.card)
    (hcard : ∀ i ∈ L, (N i).card = d)
    (hno : ∀ S : Finset I, S ⊆ L → S.card = d + 1 →
      ¬ HasTransversalOn N S) :
    ∀ i ∈ L, ∀ j ∈ L, N i = N j := by
  classical
  intro i hi j hj
  by_contra hij
  have hd : 0 < d := by
    by_contra hd0
    have hd0' : d = 0 := Nat.eq_zero_of_not_pos hd0
    have hNi : N i = ∅ := Finset.card_eq_zero.mp (by simpa [hd0'] using hcard i hi)
    have hNj : N j = ∅ := Finset.card_eq_zero.mp (by simpa [hd0'] using hcard j hj)
    exact hij (hNi.trans hNj.symm)
  obtain ⟨S, hpS, hSL, hScard⟩ := Finset.exists_subsuperset_card_eq
    (s := ({i, j} : Finset I)) (t := L) (n := d + 1)
    (by
      intro x hx
      simp only [Finset.mem_insert, Finset.mem_singleton] at hx
      rcases hx with rfl | rfl
      · exact hi
      · exact hj)
    (by
      have hij' : i ≠ j := fun h ↦ hij (congrArg N h)
      simp [hij']
      omega)
    hL
  apply hno S hSL hScard
  apply hasTransversalOn_of_card_eq_succ_of_ne N d S hScard
  · intro x hx
    exact hcard x (hSL hx)
  · exact hpS (Finset.mem_insert_self i {j})
  · exact hpS (Finset.mem_insert.mpr (Or.inr (Finset.mem_singleton_self j)))
  · exact hij

end AlbertsonUniformRows

#print axioms AlbertsonUniformRows.hasTransversalOn_of_card_eq_succ_of_ne
#print axioms AlbertsonUniformRows.all_rows_eq_of_uniform_card_of_no_succ_transversal
