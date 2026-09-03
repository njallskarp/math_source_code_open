import HammingShellIncidence

/-!
# Three-dimensional Hamming color-class lower bound

This file specializes the generic Hamming-shell incidence theorem to
`Fin 3 → Fin n` and composes it with `card_ge_of_shell_incidence`.  The result
is the complete lower bound for one color class, expressed only through the
internal Hamming-degree hypothesis.
-/

open Finset Function

namespace MajorityCHamming

universe u v

variable {ι : Type u} {β : ι → Type v}
variable [Fintype ι] [DecidableEq ι]
variable [∀ i, DecidableEq (β i)]

/-- Evaluation at the changed coordinate is injective on one direction shell. -/
theorem eq_of_mem_directionShell_of_eq_at
    {C : Finset (∀ i, β i)} {v₀ u w : ∀ i, β i} {i : ι}
    (hu : u ∈ directionShell C v₀ i)
    (hw : w ∈ directionShell C v₀ i)
    (hi : u i = w i) :
    u = w := by
  have hu_support : changeSupport v₀ u = {i} := (Finset.mem_filter.mp hu).2
  have hw_support : changeSupport v₀ w = {i} := (Finset.mem_filter.mp hw).2
  funext j
  by_cases hji : j = i
  · subst j
    exact hi
  · have huj : v₀ j = u j := by
      apply eq_at_of_not_mem_changeSupport
      simp [hu_support, hji]
    have hwj : v₀ j = w j := by
      apply eq_at_of_not_mem_changeSupport
      simp [hw_support, hji]
    exact huj.symm.trans hwj

/-- A coordinate direction in a finite Hamming space contains at most all
coordinate values other than the center value. -/
theorem card_directionShell_le_card_sub_one
    [∀ i, Fintype (β i)]
    (C : Finset (∀ i, β i)) (v₀ : ∀ i, β i) (i : ι) :
    #(directionShell C v₀ i) ≤ Fintype.card (β i) - 1 := by
  classical
  let values := (directionShell C v₀ i).image fun u => u i
  have hinj : Set.InjOn (fun u : ∀ i, β i => u i)
      (directionShell C v₀ i : Set (∀ i, β i)) := by
    intro u hu w hw huw
    exact eq_of_mem_directionShell_of_eq_at hu hw huw
  have hcard : #values = #(directionShell C v₀ i) := by
    exact Finset.card_image_of_injOn hinj
  have hsubset : values ⊆ Finset.univ.erase (v₀ i) := by
    intro a ha
    obtain ⟨u, hu, rfl⟩ := Finset.mem_image.mp ha
    have hu_support : changeSupport v₀ u = {i} := (Finset.mem_filter.mp hu).2
    have hne : v₀ i ≠ u i := by
      have : i ∈ changeSupport v₀ u := by simp [hu_support]
      simpa using this
    exact Finset.mem_erase.mpr ⟨hne.symm, Finset.mem_univ _⟩
  calc
    #(directionShell C v₀ i) = #values := hcard.symm
    _ ≤ #(Finset.univ.erase (v₀ i)) := Finset.card_le_card hsubset
    _ = Fintype.card (β i) - 1 := by simp

/-- Forgetting the direction gives a bijection between the directed first
shell and the selected Hamming neighbors of the center. -/
theorem card_directedFirstShell_eq_internalNeighbors
    (C : Finset (∀ i, β i)) (v₀ : ∀ i, β i) :
    #(directedFirstShell C v₀) = #(internalNeighbors C v₀) := by
  classical
  apply Finset.card_bij (fun p _ => p.2)
  · intro p hp
    have hp' := Finset.mem_filter.mp hp
    exact Finset.mem_filter.mpr
      ⟨(Finset.mem_product.mp hp'.1).2,
        hammingDist_eq_one_of_changeSupport_eq_singleton hp'.2⟩
  · intro p hp q hq hpq
    have hp_support := (Finset.mem_filter.mp hp).2
    have hq_support := (Finset.mem_filter.mp hq).2
    apply Prod.ext
    · apply Finset.singleton_inj.mp
      calc
        {p.1} = changeSupport v₀ p.2 := hp_support.symm
        _ = changeSupport v₀ q.2 := congrArg (changeSupport v₀) hpq
        _ = {q.1} := hq_support
    · exact hpq
  · intro u hu
    have hu' := Finset.mem_filter.mp hu
    obtain ⟨i, hi⟩ :=
      changeSupport_eq_singleton_of_hammingDist_eq_one hu'.2
    refine ⟨(i, u), ?_, rfl⟩
    exact Finset.mem_filter.mpr
      ⟨Finset.mem_product.mpr ⟨Finset.mem_univ i, hu'.1⟩, hi⟩

/-- The internal degree of the center is the sum of its coordinate-direction
shell sizes. -/
theorem card_internalNeighbors_eq_sum_directionShell
    (C : Finset (∀ i, β i)) (v₀ : ∀ i, β i) :
    #(internalNeighbors C v₀) = ∑ i, #(directionShell C v₀ i) := by
  rw [← card_directedFirstShell_eq_internalNeighbors]
  simpa using sum_directedFirstShell C v₀ (fun _ => 1)

omit [DecidableEq ι] in
/-- The center, its selected first shell, and its selected distance-two shell
are disjoint selected subsets. -/
theorem one_add_card_internal_add_card_distanceShell_two_le
    (C : Finset (∀ i, β i)) (v₀ : ∀ i, β i) (hv : v₀ ∈ C) :
    1 + #(internalNeighbors C v₀) + #(distanceShell C v₀ 2) ≤ #C := by
  classical
  let L := internalNeighbors C v₀
  let B := distanceShell C v₀ 2
  have hLB : Disjoint L B := Finset.disjoint_left.mpr fun w hwL hwB => by
    have h1 : hammingDist v₀ w = 1 := (Finset.mem_filter.mp hwL).2
    have h2 : hammingDist v₀ w = 2 := (Finset.mem_filter.mp hwB).2
    omega
  have hvL : v₀ ∉ L := by
    simp [L, internalNeighbors]
  have hvB : v₀ ∉ B := by
    simp [B, distanceShell]
  have hvLB : v₀ ∉ L ∪ B := by simp [hvL, hvB]
  have hsubset : insert v₀ (L ∪ B) ⊆ C := by
    intro w hw
    rcases Finset.mem_insert.mp hw with rfl | hw
    · exact hv
    · rcases Finset.mem_union.mp hw with hwL | hwB
      · exact (Finset.mem_filter.mp hwL).1
      · exact (Finset.mem_filter.mp hwB).1
  have hcard := Finset.card_le_card hsubset
  rw [Finset.card_insert_of_notMem hvLB,
    Finset.card_union_of_disjoint hLB] at hcard
  simpa [L, B, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hcard

/-- Complete three-dimensional color-class lower bound.

For `n ≥ 2`, any selected set in `Fin 3 → Fin n` whose every selected word
has at least `(n-1) + floor(n/2)` selected Hamming neighbors has cardinality
at least `n * (floor(n/2)+1)`. -/
theorem fin3_card_ge_of_internal_degree
    {n : ℕ} (hn : 2 ≤ n)
    (C : Finset (Fin 3 → Fin n)) (v₀ : Fin 3 → Fin n) (hv : v₀ ∈ C)
    (hdegree : ∀ u ∈ C,
      n - 1 + n / 2 ≤ #(internalNeighbors C u)) :
    n * (n / 2 + 1) ≤ #C := by
  have hn1 : 1 ≤ n := by omega
  have hnorm : n - 1 + 1 = n := Nat.sub_add_cancel hn1
  have hsum : n - 1 + (n - 1 + 1) / 2 ≤
      #(directionShell C v₀ 0) + #(directionShell C v₀ 1) +
        #(directionShell C v₀ 2) := by
    have hvdegree := hdegree v₀ hv
    rw [card_internalNeighbors_eq_sum_directionShell,
      Fin.sum_univ_three] at hvdegree
    simpa only [hnorm] using hvdegree
  have hincidence :
      #(directionShell C v₀ 0) *
          (n - 1 + (n - 1 + 1) / 2 - #(directionShell C v₀ 0)) +
        #(directionShell C v₀ 1) *
          (n - 1 + (n - 1 + 1) / 2 - #(directionShell C v₀ 1)) +
        #(directionShell C v₀ 2) *
          (n - 1 + (n - 1 + 1) / 2 - #(directionShell C v₀ 2)) ≤
        2 * #(distanceShell C v₀ 2) := by
    have hi := hamming_shell_incidence C v₀ (n - 1 + n / 2) hdegree
    rw [Fin.sum_univ_three] at hi
    simpa only [hnorm] using hi
  have hsubsets :
      1 + (#(directionShell C v₀ 0) + #(directionShell C v₀ 1) +
        #(directionShell C v₀ 2)) + #(distanceShell C v₀ 2) ≤ #C := by
    have hs := one_add_card_internal_add_card_distanceShell_two_le C v₀ hv
    rw [card_internalNeighbors_eq_sum_directionShell,
      Fin.sum_univ_three] at hs
    exact hs
  have hbound := card_ge_of_shell_incidence
    (N := n - 1)
    (a := #(directionShell C v₀ 0))
    (b := #(directionShell C v₀ 1))
    (c := #(directionShell C v₀ 2))
    (B := #(distanceShell C v₀ 2))
    (C := #C)
    (by omega)
    (by simpa using card_directionShell_le_card_sub_one C v₀ (0 : Fin 3))
    (by simpa using card_directionShell_le_card_sub_one C v₀ (1 : Fin 3))
    (by simpa using card_directionShell_le_card_sub_one C v₀ (2 : Fin 3))
    hsum hincidence hsubsets
  simpa only [hnorm] using hbound

#print axioms card_directionShell_le_card_sub_one
#print axioms card_internalNeighbors_eq_sum_directionShell
#print axioms one_add_card_internal_add_card_distanceShell_two_le
#print axioms fin3_card_ge_of_internal_degree

end MajorityCHamming
