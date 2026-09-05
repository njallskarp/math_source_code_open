import AlbertsonUniformRows
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.SymmDiff

/-!
# Two-contraction rigidity for equal-size finite rows

This file isolates the second finite-set kernel in the reviewed Albertson
two-clique argument.  If two equal-size rows have the same membership data
outside each of two distinct two-element sets, then the rows are equal.

In the graph application, equality of row signatures after contracting an
edge implies equality outside the two endpoints of that edge.  Applying the
lemma to two distinct contracted edges yields equality of the original rows.
The conversion from an application-specific contracted signature to the
`Finset.sdiff` hypotheses below remains an explicit interface boundary.
-/

open scoped symmDiff

namespace AlbertsonTwoContraction

/-- The compatibility signature of a row after contracting the points in
`p` to one distinguished class.  Points outside `p` retain singleton labels;
the distinguished label `none` occurs exactly when the whole contracted set
lies in the row.  For a two-element `p`, this is the usual signature after
merging the endpoints of a complement edge into one colour class. -/
def ContractedRow {A : Type*} [DecidableEq A]
    (r p : Finset A) : Finset (Option A) :=
  (r \ p).image some ∪ if p ⊆ r then {none} else ∅

@[simp]
theorem some_mem_contractedRow_iff
    {A : Type*} [DecidableEq A] {x : A} {r p : Finset A} :
    some x ∈ ContractedRow r p ↔ x ∈ r \ p := by
  by_cases h : p ⊆ r <;> simp [ContractedRow, h]

/-- Equality of concrete contracted-row signatures implies agreement away
from the contracted set. -/
theorem sdiff_eq_sdiff_of_contractedRow_eq
    {A : Type*} [DecidableEq A] {r₁ r₂ p : Finset A}
    (h : ContractedRow r₁ p = ContractedRow r₂ p) :
    r₁ \ p = r₂ \ p := by
  ext x
  rw [← some_mem_contractedRow_iff, h, some_mem_contractedRow_iff]

/-- Contracting a two-element set loses at most one compatible class from a
row: two row elements become one class if both are present, one element is
removed if exactly one is present, and nothing is lost otherwise. -/
theorem card_sub_one_le_card_contractedRow
    {A : Type*} [DecidableEq A] {r p : Finset A}
    (hp : p.card = 2) :
    r.card - 1 ≤ (ContractedRow r p).card := by
  have himage : ((r \ p).image some).card = (r \ p).card :=
    Finset.card_image_of_injective _ (Option.some_injective A)
  by_cases hpr : p ⊆ r
  · have hcardSdiff : (r \ p).card = r.card - 2 := by
      rw [Finset.card_sdiff, Finset.inter_eq_left.mpr hpr, hp]
    have hcardContracted : (ContractedRow r p).card = (r \ p).card + 1 := by
      simp [ContractedRow, hpr, himage]
    have htwo : 2 ≤ r.card := by
      rw [← hp]
      exact Finset.card_le_card hpr
    omega
  · have hinter : (p ∩ r).card ≤ 1 := by
      by_contra h
      have hge : 2 ≤ (p ∩ r).card := by omega
      have heq : p ∩ r = p := Finset.eq_of_subset_of_card_le
        Finset.inter_subset_left (by omega)
      exact hpr (by
        intro x hx
        have : x ∈ p ∩ r := by simpa [heq] using hx
        exact (Finset.mem_inter.mp this).2)
    have hcardSdiff : (r \ p).card = r.card - (p ∩ r).card := by
      rw [Finset.card_sdiff]
    have hcardContracted : (ContractedRow r p).card = (r \ p).card := by
      simp [ContractedRow, hpr, himage]
    omega

/-- If two finite sets agree after deleting `e`, every point of their
symmetric difference lies in `e`. -/
theorem symmDiff_subset_of_sdiff_eq_sdiff
    {A : Type*} [DecidableEq A] {s t e : Finset A}
    (h : s \ e = t \ e) :
    s ∆ t ⊆ e := by
  intro x hx
  rw [Finset.mem_symmDiff] at hx
  rcases hx with ⟨hxs, hxt⟩ | ⟨hxt, hxs⟩
  · by_contra hxe
    have hxse : x ∈ s \ e := Finset.mem_sdiff.mpr ⟨hxs, hxe⟩
    have hxte : x ∈ t \ e := by simpa [h] using hxse
    exact hxt (Finset.mem_sdiff.mp hxte).1
  · by_contra hxe
    have hxte : x ∈ t \ e := Finset.mem_sdiff.mpr ⟨hxt, hxe⟩
    have hxse : x ∈ s \ e := by simpa [h] using hxte
    exact hxs (Finset.mem_sdiff.mp hxse).1

/-- Two distinct contracted pairs determine an equal-cardinality row.

The hypotheses `hs` and `ht` say that `r₁` and `r₂` agree outside each
of the two pairs.  Their symmetric difference is therefore contained in the
intersection of those pairs, which has at most one element.  If equal-size
rows differed, both one-sided differences would be nonempty, forcing the
symmetric difference to have at least two elements.
-/
theorem eq_of_card_eq_of_agree_off_two_pairs
    {A : Type*} [DecidableEq A]
    {r₁ r₂ p q : Finset A}
    (hcard : r₁.card = r₂.card)
    (hp : p.card = 2) (hq : q.card = 2) (hpq : p ≠ q)
    (hrp : r₁ \ p = r₂ \ p)
    (hrq : r₁ \ q = r₂ \ q) :
    r₁ = r₂ := by
  have hsymmP : r₁ ∆ r₂ ⊆ p := symmDiff_subset_of_sdiff_eq_sdiff hrp
  have hsymmQ : r₁ ∆ r₂ ⊆ q := symmDiff_subset_of_sdiff_eq_sdiff hrq
  have hsymmInter : r₁ ∆ r₂ ⊆ p ∩ q := by
    intro x hx
    exact Finset.mem_inter.mpr ⟨hsymmP hx, hsymmQ hx⟩
  have hinter : (p ∩ q).card ≤ 1 := by
    by_contra h
    have hge : 2 ≤ (p ∩ q).card := by omega
    have hep : p ∩ q = p := Finset.eq_of_subset_of_card_le
      Finset.inter_subset_left (by omega)
    have heq : p ∩ q = q := Finset.eq_of_subset_of_card_le
      Finset.inter_subset_right (by omega)
    exact hpq (hep.symm.trans heq)
  have hsymmCard : (r₁ ∆ r₂).card ≤ 1 :=
    (Finset.card_le_card hsymmInter).trans hinter
  by_contra hne
  have hnsub₁₂ : ¬ r₁ ⊆ r₂ := by
    intro hsub
    exact hne (Finset.eq_of_subset_of_card_le hsub hcard.ge)
  have hnsub₂₁ : ¬ r₂ ⊆ r₁ := by
    intro hsub
    exact hne (Finset.eq_of_subset_of_card_le hsub hcard.le).symm
  have hpos₁₂ : 0 < (r₁ \ r₂).card :=
    Finset.card_pos.mpr (Finset.sdiff_nonempty.mpr hnsub₁₂)
  have hpos₂₁ : 0 < (r₂ \ r₁).card :=
    Finset.card_pos.mpr (Finset.sdiff_nonempty.mpr hnsub₂₁)
  have hdisjoint : Disjoint (r₁ \ r₂) (r₂ \ r₁) := by
    apply Finset.disjoint_left.mpr
    intro x hx₁₂ hx₂₁
    exact (Finset.mem_sdiff.mp hx₁₂).2 (Finset.mem_sdiff.mp hx₂₁).1
  have htwo : 2 ≤ (r₁ ∆ r₂).card := by
    rw [Finset.symmDiff_def, Finset.card_union_of_disjoint hdisjoint]
    omega
  omega

/-- Concrete two-contraction form.  Equal-cardinality rows with equal
`ContractedRow` signatures after two distinct pair contractions were already
equal before contraction. -/
theorem eq_of_card_eq_of_two_contractedRows
    {A : Type*} [DecidableEq A]
    {r₁ r₂ p q : Finset A}
    (hcard : r₁.card = r₂.card)
    (hp : p.card = 2) (hq : q.card = 2) (hpq : p ≠ q)
    (hrp : ContractedRow r₁ p = ContractedRow r₂ p)
    (hrq : ContractedRow r₁ q = ContractedRow r₂ q) :
    r₁ = r₂ :=
  eq_of_card_eq_of_agree_off_two_pairs hcard hp hq hpq
    (sdiff_eq_sdiff_of_contractedRow_eq hrp)
    (sdiff_eq_sdiff_of_contractedRow_eq hrq)

/-- A deficient matching after one pair contraction forces every contracted
row to have the minimum possible size and all contracted rows to agree. -/
theorem card_eq_and_all_contractedRows_eq_of_no_transversal
    {I A : Type*} [DecidableEq I] [DecidableEq A]
    (N : I → Finset A) (e : ℕ) (L : Finset I) (p : Finset A)
    (he : 0 < e) (hL : e ≤ L.card)
    (hcard : ∀ i ∈ L, (N i).card = e)
    (hp : p.card = 2)
    (hno : ∀ S : Finset I, S ⊆ L → S.card = e →
      ¬ AlbertsonUniformRows.HasTransversalOn
        (fun i ↦ ContractedRow (N i) p) S) :
    (∀ i ∈ L, (ContractedRow (N i) p).card = e - 1) ∧
      ∀ i ∈ L, ∀ j ∈ L,
        ContractedRow (N i) p = ContractedRow (N j) p := by
  have hsucc : e - 1 + 1 = e := by omega
  have hL' : e - 1 + 1 ≤ L.card := by omega
  have hdegree : ∀ i ∈ L, e - 1 ≤ (ContractedRow (N i) p).card := by
    intro i hi
    have h := card_sub_one_le_card_contractedRow (r := N i) hp
    rwa [hcard i hi] at h
  have hno' : ∀ S : Finset I, S ⊆ L → S.card = e - 1 + 1 →
      ¬ AlbertsonUniformRows.HasTransversalOn
        (fun i ↦ ContractedRow (N i) p) S := by
    intro S hSL hS
    exact hno S hSL (hS.trans hsucc)
  exact AlbertsonUniformRows.card_eq_and_all_rows_eq_of_card_ge_of_no_succ_transversal
    (fun i ↦ ContractedRow (N i) p) (e - 1) L hL' hdegree hno'

/-- Complete abstract two-contraction kernel from the reviewed Albertson
argument.  Equal-size original rows and matching obstructions after two
distinct pair contractions force all original rows to be equal. -/
theorem all_rows_eq_of_two_contraction_obstructions
    {I A : Type*} [DecidableEq I] [DecidableEq A]
    (N : I → Finset A) (e : ℕ) (L : Finset I) (p q : Finset A)
    (he : 0 < e) (hL : e ≤ L.card)
    (hcard : ∀ i ∈ L, (N i).card = e)
    (hp : p.card = 2) (hq : q.card = 2) (hpq : p ≠ q)
    (hnoP : ∀ S : Finset I, S ⊆ L → S.card = e →
      ¬ AlbertsonUniformRows.HasTransversalOn
        (fun i ↦ ContractedRow (N i) p) S)
    (hnoQ : ∀ S : Finset I, S ⊆ L → S.card = e →
      ¬ AlbertsonUniformRows.HasTransversalOn
        (fun i ↦ ContractedRow (N i) q) S) :
    ∀ i ∈ L, ∀ j ∈ L, N i = N j := by
  obtain ⟨-, hrowsP⟩ := card_eq_and_all_contractedRows_eq_of_no_transversal
    N e L p he hL hcard hp hnoP
  obtain ⟨-, hrowsQ⟩ := card_eq_and_all_contractedRows_eq_of_no_transversal
    N e L q he hL hcard hq hnoQ
  intro i hi j hj
  apply eq_of_card_eq_of_two_contractedRows
  · exact (hcard i hi).trans (hcard j hj).symm
  · exact hp
  · exact hq
  · exact hpq
  · exact hrowsP i hi j hj
  · exact hrowsQ i hi j hj

end AlbertsonTwoContraction

#print axioms AlbertsonTwoContraction.some_mem_contractedRow_iff
#print axioms AlbertsonTwoContraction.sdiff_eq_sdiff_of_contractedRow_eq
#print axioms AlbertsonTwoContraction.card_sub_one_le_card_contractedRow
#print axioms AlbertsonTwoContraction.symmDiff_subset_of_sdiff_eq_sdiff
#print axioms AlbertsonTwoContraction.eq_of_card_eq_of_agree_off_two_pairs
#print axioms AlbertsonTwoContraction.eq_of_card_eq_of_two_contractedRows
#print axioms AlbertsonTwoContraction.card_eq_and_all_contractedRows_eq_of_no_transversal
#print axioms AlbertsonTwoContraction.all_rows_eq_of_two_contraction_obstructions
