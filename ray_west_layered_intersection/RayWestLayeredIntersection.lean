import Mathlib.Data.Fin.Rev
import Mathlib.Data.Fin.Tuple.Sort
import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Perm
import Lean.Elab.Tactic.Omega

/-!
# The layered/colayered intersection in the Ray--West minimizer theorem

This file formalizes the elementary structural hinge used to count the two
families of Ray--West codimension-two minimizers. Pattern containment is stated
directly by inequalities on a permutation of `Fin m`.
-/

namespace RayWestLayeredIntersection

/-- A `231` occurrence: values have relative order `2,3,1`. -/
def Contains231 {m : ℕ} (π : Equiv.Perm (Fin m)) : Prop :=
  ∃ i j k : Fin m, i < j ∧ j < k ∧ π k < π i ∧ π i < π j

/-- A `312` occurrence: values have relative order `3,1,2`. -/
def Contains312 {m : ℕ} (π : Equiv.Perm (Fin m)) : Prop :=
  ∃ i j k : Fin m, i < j ∧ j < k ∧ π j < π k ∧ π k < π i

/-- A `132` occurrence: values have relative order `1,3,2`. -/
def Contains132 {m : ℕ} (π : Equiv.Perm (Fin m)) : Prop :=
  ∃ i j k : Fin m, i < j ∧ j < k ∧ π i < π k ∧ π k < π j

/-- A `213` occurrence: values have relative order `2,1,3`. -/
def Contains213 {m : ℕ} (π : Equiv.Perm (Fin m)) : Prop :=
  ∃ i j k : Fin m, i < j ∧ j < k ∧ π j < π i ∧ π i < π k

def Avoids231 {m : ℕ} (π : Equiv.Perm (Fin m)) : Prop := ¬ Contains231 π
def Avoids312 {m : ℕ} (π : Equiv.Perm (Fin m)) : Prop := ¬ Contains312 π
def Avoids132 {m : ℕ} (π : Equiv.Perm (Fin m)) : Prop := ¬ Contains132 π
def Avoids213 {m : ℕ} (π : Equiv.Perm (Fin m)) : Prop := ¬ Contains213 π

/-- Membership in both classical pattern classes for layered and colayered
permutations. -/
def InLayeredColayeredIntersection {m : ℕ} (π : Equiv.Perm (Fin m)) : Prop :=
  Avoids231 π ∧ Avoids312 π ∧ Avoids132 π ∧ Avoids213 π

/-- Avoiding the four nonmonotone patterns prevents two successive comparisons
from changing orientation. -/
theorem adjacent_orientation_same {n : ℕ} (π : Equiv.Perm (Fin (n + 2)))
    (h : InLayeredColayeredIntersection π) (i : Fin n) :
    π i.castSucc.castSucc < π i.castSucc.succ ↔
      π i.succ.castSucc < π i.succ.succ := by
  let a : Fin (n + 2) := i.castSucc.castSucc
  let b : Fin (n + 2) := i.castSucc.succ
  let c : Fin (n + 2) := i.succ.succ
  have hab_index : a < b := by simp [a, b]
  have hbc_index : b < c := by simp [b, c]
  have hac_ne : π a ≠ π c := by
    intro heq
    have := π.injective heq
    exact (hab_index.trans hbc_index).ne this
  constructor
  · intro hab
    have hab' : π a < π b := by simpa [a, b] using hab
    by_contra hbc
    have hcb : π c < π b := by
      apply lt_of_le_of_ne (le_of_not_gt (by simpa [b, c] using hbc))
      intro heq
      have := π.injective heq
      exact hbc_index.ne this.symm
    rcases lt_trichotomy (π a) (π c) with hac | heq | hca
    · exact h.2.2.1 ⟨a, b, c, hab_index, hbc_index, hac, hcb⟩
    · exact hac_ne heq
    · exact h.1 ⟨a, b, c, hab_index, hbc_index, hca, hab'⟩
  · intro hbc
    have hbc' : π b < π c := by simpa [b, c] using hbc
    by_contra hab
    have hba : π b < π a := by
      apply lt_of_le_of_ne (le_of_not_gt (by simpa [a, b] using hab))
      intro heq
      have := π.injective heq
      exact hab_index.ne this.symm
    rcases lt_trichotomy (π a) (π c) with hac | heq | hca
    · exact h.2.2.2 ⟨a, b, c, hab_index, hbc_index, hba, hac⟩
    · exact hac_ne heq
    · exact h.2.1 ⟨a, b, c, hab_index, hbc_index, hbc', hca⟩

/-- A permutation of length at least two avoiding the four mixed patterns is
strictly increasing or strictly decreasing. -/
theorem strictMono_or_strictAnti_of_mem_intersection {n : ℕ}
    (π : Equiv.Perm (Fin (n + 2)))
    (h : InLayeredColayeredIntersection π) :
    StrictMono π ∨ StrictAnti π := by
  have hne : π (0 : Fin (n + 2)) ≠ π ((0 : Fin (n + 1)).succ) := by
    intro heq
    have := π.injective heq
    simp at this
  rcases lt_or_gt_of_ne hne with hbase | hbase
  · left
    rw [Fin.strictMono_iff_lt_succ]
    intro i
    induction i using Fin.induction with
    | zero => simpa using hbase
    | succ i ih => exact (adjacent_orientation_same π h i).mp ih
  · right
    rw [Fin.strictAnti_iff_succ_lt]
    intro i
    induction i using Fin.induction with
    | zero => simpa using hbase
    | succ i ih =>
        have hnot_previous :
            ¬π i.castSucc.castSucc < π i.castSucc.succ :=
          not_lt_of_ge ih.le
        have hnot_next : ¬π i.succ.castSucc < π i.succ.succ := fun hnext =>
          hnot_previous ((adjacent_orientation_same π h i).mpr hnext)
        have hnext_ne : π i.succ.castSucc ≠ π i.succ.succ := by
          intro heq
          have := π.injective heq
          have hidx : i.succ.castSucc < i.succ.succ := Fin.castSucc_lt_succ
          exact hidx.ne this
        exact (lt_or_gt_of_ne hnext_ne).resolve_left hnot_next

theorem strictMono_mem_intersection {m : ℕ} {π : Equiv.Perm (Fin m)}
    (hπ : StrictMono π) : InLayeredColayeredIntersection π := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rintro ⟨i, j, k, hij, hjk, hki, -⟩
    exact not_lt_of_ge (hπ (hij.trans hjk)).le hki
  · rintro ⟨i, j, k, hij, hjk, -, hki⟩
    exact not_lt_of_ge (hπ (hij.trans hjk)).le hki
  · rintro ⟨i, j, k, -, hjk, -, hkj⟩
    exact not_lt_of_ge (hπ hjk).le hkj
  · rintro ⟨i, j, k, hij, -, hji, -⟩
    exact not_lt_of_ge (hπ hij).le hji

theorem strictAnti_mem_intersection {m : ℕ} {π : Equiv.Perm (Fin m)}
    (hπ : StrictAnti π) : InLayeredColayeredIntersection π := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rintro ⟨i, j, k, hij, -, -, hijv⟩
    exact not_lt_of_ge (hπ hij).le hijv
  · rintro ⟨i, j, k, -, hjk, hjkv, -⟩
    exact not_lt_of_ge (hπ hjk).le hjkv
  · rintro ⟨i, j, k, hij, hjk, hik, -⟩
    exact not_lt_of_ge (hπ (hij.trans hjk)).le hik
  · rintro ⟨i, j, k, hij, hjk, -, hik⟩
    exact not_lt_of_ge (hπ (hij.trans hjk)).le hik

/-- An increasing permutation of `Fin m` is the identity, while a decreasing
one is the reversal. -/
theorem eq_one_or_revPerm_of_mem_intersection {n : ℕ}
    (π : Equiv.Perm (Fin (n + 2)))
    (h : InLayeredColayeredIntersection π) :
    π = 1 ∨ π = Fin.revPerm := by
  rcases strictMono_or_strictAnti_of_mem_intersection π h with hmono | hanti
  · exact Or.inl ((Equiv.Perm.monotone_iff π).mp hmono.monotone)
  · right
    have hπ : Antitone ((id : Fin (n + 2) → Fin (n + 2)) ∘ π) := by
      simpa using hanti.antitone
    have hrev : Antitone
        ((id : Fin (n + 2) → Fin (n + 2)) ∘
          (Fin.revPerm : Equiv.Perm (Fin (n + 2)))) := by
      intro i j hij
      change j.rev ≤ i.rev
      exact Fin.rev_le_rev.mpr hij
    have heq := Tuple.unique_antitone hπ hrev
    exact Equiv.ext fun i => congrFun heq i

/-- Exact structural form of the classical intersection
`Av(231,312) ∩ Av(132,213)` in every length at least two. -/
theorem mem_intersection_iff_eq_one_or_revPerm {n : ℕ}
    (π : Equiv.Perm (Fin (n + 2))) :
    InLayeredColayeredIntersection π ↔ π = 1 ∨ π = Fin.revPerm := by
  constructor
  · exact eq_one_or_revPerm_of_mem_intersection π
  · rintro (rfl | rfl)
    · exact strictMono_mem_intersection strictMono_id
    · exact strictAnti_mem_intersection Fin.rev_strictAnti

theorem revPerm_ne_one (n : ℕ) :
    (Fin.revPerm : Equiv.Perm (Fin (n + 2))) ≠ 1 := by
  intro h
  have hzero := DFunLike.congr_fun h (0 : Fin (n + 2))
  have hlast : (Fin.last (n + 1) : Fin (n + 2)) = 0 := hzero
  have hval := congrArg Fin.val hlast
  simp at hval

/-- The concrete finite set representing the layered/colayered intersection. -/
noncomputable def intersectionClass (n : ℕ) :
    Finset (Equiv.Perm (Fin (n + 2))) := by
  classical
  exact Finset.univ.filter InLayeredColayeredIntersection

/-- The avoidance class `Av(231,312)`, classically the layered permutations. -/
noncomputable def layeredClass (n : ℕ) :
    Finset (Equiv.Perm (Fin (n + 2))) := by
  classical
  exact Finset.univ.filter fun π => Avoids231 π ∧ Avoids312 π

/-- The avoidance class `Av(132,213)`, classically the colayered permutations. -/
noncomputable def colayeredClass (n : ℕ) :
    Finset (Equiv.Perm (Fin (n + 2))) := by
  classical
  exact Finset.univ.filter fun π => Avoids132 π ∧ Avoids213 π

theorem layeredClass_inter_colayeredClass (n : ℕ) :
    layeredClass n ∩ colayeredClass n = intersectionClass n := by
  classical
  ext π
  simp only [layeredClass, colayeredClass, intersectionClass,
    Finset.mem_inter, Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · rintro ⟨⟨h231, h312⟩, h132, h213⟩
    exact ⟨h231, h312, h132, h213⟩
  · rintro ⟨h231, h312, h132, h213⟩
    exact ⟨⟨h231, h312⟩, h132, h213⟩

theorem intersectionClass_eq_pair (n : ℕ) :
    intersectionClass n = {1, Fin.revPerm} := by
  classical
  ext π
  simp [intersectionClass, mem_intersection_iff_eq_one_or_revPerm]

/-- The layered and colayered pattern classes have exactly two common
permutations in every length at least two. -/
theorem card_intersectionClass (n : ℕ) : (intersectionClass n).card = 2 := by
  classical
  rw [intersectionClass_eq_pair]
  exact Finset.card_pair (revPerm_ne_one n).symm

/-- Inclusion--exclusion endpoint for the Ray--West minimizer count.

The two classical individual avoidance-class counts are explicit hypotheses;
this file proves the non-disjointness correction and the final arithmetic.
-/
theorem card_layered_union_colayered_of_class_counts (n : ℕ)
    (hlayered : (layeredClass n).card = 2 ^ (n + 1))
    (hcolayered : (colayeredClass n).card = 2 ^ (n + 1)) :
    (layeredClass n ∪ colayeredClass n).card = 2 ^ (n + 2) - 2 := by
  have hcard := Finset.card_union_add_card_inter (layeredClass n) (colayeredClass n)
  rw [layeredClass_inter_colayeredClass, card_intersectionClass,
    hlayered, hcolayered] at hcard
  have hpow : 2 ^ (n + 2) = 2 ^ (n + 1) + 2 ^ (n + 1) := by
    rw [show n + 2 = (n + 1) + 1 by omega, pow_succ]
    omega
  omega

#print axioms adjacent_orientation_same
#print axioms strictMono_or_strictAnti_of_mem_intersection
#print axioms strictMono_mem_intersection
#print axioms strictAnti_mem_intersection
#print axioms eq_one_or_revPerm_of_mem_intersection
#print axioms mem_intersection_iff_eq_one_or_revPerm
#print axioms layeredClass_inter_colayeredClass
#print axioms intersectionClass_eq_pair
#print axioms card_intersectionClass
#print axioms card_layered_union_colayered_of_class_counts

end RayWestLayeredIntersection
