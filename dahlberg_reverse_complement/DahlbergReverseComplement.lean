import Mathlib.Data.Fin.Rev
import Mathlib.Data.Finset.Card
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic

/-!
# Reverse-complement transfer for Dahlberg's length-four pattern classes

This file isolates the structural, non-computational symmetry behind the
reverse-complement companion to the descent-set census for involutions avoiding
`1432` and `2134`.

A permutation of length `n + 1` is represented as `Equiv.Perm (Fin (n + 1))`.
Its descent positions therefore form a `Finset (Fin n)`.  Length-four pattern
containment is stated directly by inequalities, avoiding any external pattern
library or certificate.
-/

namespace DahlbergReverseComplement

open Equiv

/-- Reverse-complement (180-degree rotation of the permutation plot). -/
def reverseComplement {n : ℕ} (π : Equiv.Perm (Fin n)) : Equiv.Perm (Fin n) :=
  Fin.revPerm.trans (π.trans Fin.revPerm)

@[simp]
theorem reverseComplement_apply {n : ℕ} (π : Equiv.Perm (Fin n)) (i : Fin n) :
    reverseComplement π i = (π i.rev).rev := rfl

@[simp]
theorem reverseComplement_reverseComplement {n : ℕ} (π : Equiv.Perm (Fin n)) :
    reverseComplement (reverseComplement π) = π := by
  ext i
  simp [reverseComplement]

/-- Reverse-complement, as an involutive equivalence on permutations. -/
def reverseComplementEquiv (n : ℕ) :
    Equiv.Perm (Fin n) ≃ Equiv.Perm (Fin n) where
  toFun := reverseComplement
  invFun := reverseComplement
  left_inv := reverseComplement_reverseComplement
  right_inv := reverseComplement_reverseComplement

/-- Being an involution is invariant under reverse-complement. -/
theorem reverseComplement_involutive {n : ℕ} {π : Equiv.Perm (Fin n)}
    (hπ : Function.Involutive π) :
    Function.Involutive (reverseComplement π) := by
  intro i
  simp only [reverseComplement_apply, Fin.rev_rev]
  rw [hπ i.rev, Fin.rev_rev]

/-- A `1432` occurrence: values have relative order `1,4,3,2`. -/
def Contains1432 {n : ℕ} (π : Equiv.Perm (Fin n)) : Prop :=
  ∃ i j k l : Fin n,
    i < j ∧ j < k ∧ k < l ∧
    π i < π l ∧ π l < π k ∧ π k < π j

/-- A `3214` occurrence: values have relative order `3,2,1,4`. -/
def Contains3214 {n : ℕ} (π : Equiv.Perm (Fin n)) : Prop :=
  ∃ i j k l : Fin n,
    i < j ∧ j < k ∧ k < l ∧
    π k < π j ∧ π j < π i ∧ π i < π l

/-- A `2134` occurrence: values have relative order `2,1,3,4`. -/
def Contains2134 {n : ℕ} (π : Equiv.Perm (Fin n)) : Prop :=
  ∃ i j k l : Fin n,
    i < j ∧ j < k ∧ k < l ∧
    π j < π i ∧ π i < π k ∧ π k < π l

/-- A `1243` occurrence: values have relative order `1,2,4,3`. -/
def Contains1243 {n : ℕ} (π : Equiv.Perm (Fin n)) : Prop :=
  ∃ i j k l : Fin n,
    i < j ∧ j < k ∧ k < l ∧
    π i < π j ∧ π j < π l ∧ π l < π k

def Avoids1432 {n : ℕ} (π : Equiv.Perm (Fin n)) : Prop := ¬ Contains1432 π
def Avoids3214 {n : ℕ} (π : Equiv.Perm (Fin n)) : Prop := ¬ Contains3214 π
def Avoids2134 {n : ℕ} (π : Equiv.Perm (Fin n)) : Prop := ¬ Contains2134 π
def Avoids1243 {n : ℕ} (π : Equiv.Perm (Fin n)) : Prop := ¬ Contains1243 π

private theorem reversed_index_chain {n : ℕ} {i j k l : Fin n}
    (hij : i < j) (hjk : j < k) (hkl : k < l) :
    l.rev < k.rev ∧ k.rev < j.rev ∧ j.rev < i.rev := by
  exact ⟨Fin.rev_lt_rev.mpr hkl, Fin.rev_lt_rev.mpr hjk,
    Fin.rev_lt_rev.mpr hij⟩

theorem contains1432_reverseComplement_iff {n : ℕ} (π : Equiv.Perm (Fin n)) :
    Contains1432 (reverseComplement π) ↔ Contains3214 π := by
  constructor
  · rintro ⟨i, j, k, l, hij, hjk, hkl, hil, hlk, hkj⟩
    refine ⟨l.rev, k.rev, j.rev, i.rev, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact Fin.rev_lt_rev.mpr hkl
    · exact Fin.rev_lt_rev.mpr hjk
    · exact Fin.rev_lt_rev.mpr hij
    · simpa using Fin.rev_lt_rev.mp hkj
    · simpa using Fin.rev_lt_rev.mp hlk
    · simpa using Fin.rev_lt_rev.mp hil
  · intro h
    rcases h with ⟨i, j, k, l, hij, hjk, hkl, hkj, hji, hil⟩
    refine ⟨l.rev, k.rev, j.rev, i.rev, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact Fin.rev_lt_rev.mpr hkl
    · exact Fin.rev_lt_rev.mpr hjk
    · exact Fin.rev_lt_rev.mpr hij
    · simpa using Fin.rev_lt_rev.mpr hil
    · simpa using Fin.rev_lt_rev.mpr hji
    · simpa using Fin.rev_lt_rev.mpr hkj

theorem contains2134_reverseComplement_iff {n : ℕ} (π : Equiv.Perm (Fin n)) :
    Contains2134 (reverseComplement π) ↔ Contains1243 π := by
  constructor
  · rintro ⟨i, j, k, l, hij, hjk, hkl, hji, hik, hklv⟩
    refine ⟨l.rev, k.rev, j.rev, i.rev, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact Fin.rev_lt_rev.mpr hkl
    · exact Fin.rev_lt_rev.mpr hjk
    · exact Fin.rev_lt_rev.mpr hij
    · simpa using Fin.rev_lt_rev.mp hklv
    · simpa using Fin.rev_lt_rev.mp hik
    · simpa using Fin.rev_lt_rev.mp hji
  · intro h
    rcases h with ⟨i, j, k, l, hij, hjk, hkl, hijv, hjl, hlk⟩
    refine ⟨l.rev, k.rev, j.rev, i.rev, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact Fin.rev_lt_rev.mpr hkl
    · exact Fin.rev_lt_rev.mpr hjk
    · exact Fin.rev_lt_rev.mpr hij
    · simpa using Fin.rev_lt_rev.mpr hlk
    · simpa using Fin.rev_lt_rev.mpr hjl
    · simpa using Fin.rev_lt_rev.mpr hijv

theorem avoids1432_reverseComplement_iff {n : ℕ} (π : Equiv.Perm (Fin n)) :
    Avoids1432 (reverseComplement π) ↔ Avoids3214 π :=
  not_congr (contains1432_reverseComplement_iff π)

theorem avoids2134_reverseComplement_iff {n : ℕ} (π : Equiv.Perm (Fin n)) :
    Avoids2134 (reverseComplement π) ↔ Avoids1243 π :=
  not_congr (contains2134_reverseComplement_iff π)

/-- Descent positions of a permutation of length `n + 1`. -/
def descentSet {n : ℕ} (π : Equiv.Perm (Fin (n + 1))) : Finset (Fin n) :=
  Finset.univ.filter fun i => π i.castSucc > π i.succ

/-- Reverse-complement reflects descent positions across the middle gap. -/
theorem mem_descentSet_reverseComplement_iff {n : ℕ}
    (π : Equiv.Perm (Fin (n + 1))) (i : Fin n) :
    i ∈ descentSet (reverseComplement π) ↔ i.rev ∈ descentSet π := by
  simp only [descentSet, Finset.mem_filter, Finset.mem_univ, true_and,
    reverseComplement_apply, Fin.rev_castSucc, Fin.rev_succ]
  exact Fin.rev_lt_rev

/-- Set-level form of descent reflection. -/
theorem descentSet_reverseComplement {n : ℕ}
    (π : Equiv.Perm (Fin (n + 1))) :
    descentSet (reverseComplement π) = (descentSet π).image Fin.rev := by
  ext i
  rw [mem_descentSet_reverseComplement_iff]
  constructor
  · intro hi
    exact Finset.mem_image.mpr ⟨i.rev, hi, Fin.rev_rev i⟩
  · intro hi
    rcases Finset.mem_image.mp hi with ⟨a, ha, rfl⟩
    simpa using ha

/-- Reflection of a set of descent positions. -/
def reflectDescents {n : ℕ} (D : Finset (Fin n)) : Finset (Fin n) :=
  D.image Fin.rev

@[simp]
theorem mem_reflectDescents_iff {n : ℕ} {D : Finset (Fin n)} {i : Fin n} :
    i ∈ reflectDescents D ↔ i.rev ∈ D := by
  constructor
  · intro hi
    rcases Finset.mem_image.mp hi with ⟨a, ha, hrev⟩
    have haeq : a = i.rev := Fin.rev_eq_iff.mp hrev
    simpa [haeq] using ha
  · intro hi
    exact Finset.mem_image.mpr ⟨i.rev, hi, Fin.rev_rev i⟩

@[simp]
theorem reflectDescents_reflectDescents {n : ℕ} (D : Finset (Fin n)) :
    reflectDescents (reflectDescents D) = D := by
  ext i
  simp

theorem reflectDescents_compl {n : ℕ} (D : Finset (Fin n)) :
    reflectDescents Dᶜ = (reflectDescents D)ᶜ := by
  ext i
  simp

/-- Involutions with pattern predicate `P` and exactly the descent set `D`. -/
def InvolutionPatternClass {n : ℕ}
    (P : Equiv.Perm (Fin (n + 1)) → Prop) (D : Finset (Fin n)) :=
  {π : Equiv.Perm (Fin (n + 1)) //
    Function.Involutive π ∧ P π ∧ descentSet π = D}

/-- Reverse-complement equivalence between two descent-refined pattern classes.

The hypothesis is exactly the pointwise pattern-transport fact. No enumerated
permutations or external census data enter this construction.
-/
def patternClassReverseComplementEquiv {n : ℕ}
    {P Q : Equiv.Perm (Fin (n + 1)) → Prop}
    (hPQ : ∀ π, P (reverseComplement π) ↔ Q π)
    (D : Finset (Fin n)) :
    InvolutionPatternClass Q D ≃
      InvolutionPatternClass P (reflectDescents D) where
  toFun x := ⟨reverseComplement x.1,
    reverseComplement_involutive x.2.1,
    (hPQ x.1).mpr x.2.2.1,
    by rw [descentSet_reverseComplement, x.2.2.2]; rfl⟩
  invFun x := ⟨reverseComplement x.1,
    reverseComplement_involutive x.2.1,
    (hPQ (reverseComplement x.1)).mp (by simpa using x.2.2.1),
    by
      rw [descentSet_reverseComplement, x.2.2.2]
      simpa [reflectDescents] using reflectDescents_reflectDescents D⟩
  left_inv x := Subtype.ext (reverseComplement_reverseComplement x.1)
  right_inv x := Subtype.ext (reverseComplement_reverseComplement x.1)

/-- Cardinality of a descent-refined involution class. -/
noncomputable def patternClassCount {n : ℕ}
    (P : Equiv.Perm (Fin (n + 1)) → Prop) (D : Finset (Fin n)) : ℕ :=
  Nat.card (InvolutionPatternClass P D)

theorem patternClassCount_reverseComplement {n : ℕ}
    {P Q : Equiv.Perm (Fin (n + 1)) → Prop}
    (hPQ : ∀ π, P (reverseComplement π) ↔ Q π)
    (D : Finset (Fin n)) :
    patternClassCount Q D = patternClassCount P (reflectDescents D) :=
  Nat.card_congr (patternClassReverseComplementEquiv hPQ D)

noncomputable abbrev count1432 {n : ℕ} (D : Finset (Fin n)) : ℕ :=
  patternClassCount Avoids1432 D

noncomputable abbrev count3214 {n : ℕ} (D : Finset (Fin n)) : ℕ :=
  patternClassCount Avoids3214 D

noncomputable abbrev count2134 {n : ℕ} (D : Finset (Fin n)) : ℕ :=
  patternClassCount Avoids2134 D

noncomputable abbrev count1243 {n : ℕ} (D : Finset (Fin n)) : ℕ :=
  patternClassCount Avoids1243 D

theorem count3214_eq_count1432_reflect {n : ℕ} (D : Finset (Fin n)) :
    count3214 D = count1432 (reflectDescents D) :=
  patternClassCount_reverseComplement avoids1432_reverseComplement_iff D

theorem count1243_eq_count2134_reflect {n : ℕ} (D : Finset (Fin n)) :
    count1243 D = count2134 (reflectDescents D) :=
  patternClassCount_reverseComplement avoids2134_reverseComplement_iff D

/-- The reviewed `1432/2134` descent-set identity implies its
`3214/1243` companion by reverse-complement.

This theorem does not assert or trust the finite census itself: the census
identity is the explicit hypothesis `h`.
-/
theorem companion_identity_of_original {n : ℕ}
    (h : ∀ D : Finset (Fin n), count1432 D = count2134 Dᶜ)
    (D : Finset (Fin n)) :
    count3214 D = count1243 Dᶜ := by
  calc
    count3214 D = count1432 (reflectDescents D) :=
      count3214_eq_count1432_reflect D
    _ = count2134 (reflectDescents D)ᶜ := h (reflectDescents D)
    _ = count2134 (reflectDescents Dᶜ) := by
      rw [reflectDescents_compl]
    _ = count1243 Dᶜ := (count1243_eq_count2134_reflect Dᶜ).symm

#print axioms reverseComplement_reverseComplement
#print axioms reverseComplement_involutive
#print axioms contains1432_reverseComplement_iff
#print axioms contains2134_reverseComplement_iff
#print axioms avoids1432_reverseComplement_iff
#print axioms avoids2134_reverseComplement_iff
#print axioms mem_descentSet_reverseComplement_iff
#print axioms descentSet_reverseComplement
#print axioms reflectDescents_reflectDescents
#print axioms reflectDescents_compl
#print axioms patternClassCount_reverseComplement
#print axioms count3214_eq_count1432_reflect
#print axioms count1243_eq_count2134_reflect
#print axioms companion_identity_of_original

end DahlbergReverseComplement
