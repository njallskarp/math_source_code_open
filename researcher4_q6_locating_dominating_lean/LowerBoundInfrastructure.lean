import Mathlib
import LocatingDominating

/-!
# Family infrastructure for locating-dominating lower bounds

This file isolates the reusable part of the Honkala--Laihonen--Ranto
family/excess argument.  A father is a vertex with signature size at least
three; its sons are the vertices whose two-element signatures are contained
in the father's signature.

The main theorem proves that, when distinct closed neighborhoods intersect in
at most two vertices, the signature map injects the sons into the two-subsets
of the father's signature.  Thus an `i`-covered father has at most
`Nat.choose i 2` sons.  The proof is structural: locating domination resolves
collisions between two non-codewords, while the closed-neighborhood
intersection hypothesis resolves every collision involving a codeword.
-/

open Finset

namespace SimpleGraph

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

/-- Every pair of distinct vertices has at most two common closed neighbors. -/
def ClosedNeighborhoodIntersectionsAtMostTwo : Prop :=
  ∀ ⦃u v : V⦄, u ≠ v →
    (G.closedNeighborFinset u ∩ G.closedNeighborFinset v).card ≤ 2

/-- A father is a vertex covered by at least three codewords. -/
def IsFather (C : Finset V) (x : V) : Prop :=
  3 ≤ (G.locatingSignature C x).card

/-- The sons of `x` are precisely the vertices with a two-element signature
contained in the signature of `x`.  This includes codeword sons. -/
def sons (C : Finset V) (x : V) : Finset V :=
  univ.filter fun y ↦
    (G.locatingSignature C y).card = 2 ∧
      G.locatingSignature C y ⊆ G.locatingSignature C x

@[simp] theorem mem_closedNeighborFinset_iff {u v : V} :
    u ∈ G.closedNeighborFinset v ↔ u = v ∨ G.Adj v u := by
  simp [closedNeighborFinset]

theorem mem_closedNeighborFinset_comm {u v : V} :
    u ∈ G.closedNeighborFinset v ↔ v ∈ G.closedNeighborFinset u := by
  simp only [mem_closedNeighborFinset_iff]
  constructor
  · rintro (rfl | huv)
    · exact Or.inl rfl
    · exact Or.inr huv.symm
  · rintro (rfl | hvu)
    · exact Or.inl rfl
    · exact Or.inr hvu.symm

/-- If two distinct vertices are closed neighbors and their closed
neighborhoods have intersection size at most two, they are the only common
closed neighbors. -/
theorem common_closedNeighbor_eq_endpoint
    (hsmall : G.ClosedNeighborhoodIntersectionsAtMostTwo)
    {u v w : V} (huv : u ≠ v)
    (hv_close_u : v ∈ G.closedNeighborFinset u)
    (hw_close_u : w ∈ G.closedNeighborFinset u)
    (hw_close_v : w ∈ G.closedNeighborFinset v) :
    w = u ∨ w = v := by
  let common := G.closedNeighborFinset u ∩ G.closedNeighborFinset v
  have huv_subset : {u, v} ⊆ common := by
    intro z hz
    simp only [mem_insert, mem_singleton] at hz
    rcases hz with rfl | rfl
    · exact mem_inter.mpr ⟨by simp, (G.mem_closedNeighborFinset_comm).mp hv_close_u⟩
    · exact mem_inter.mpr ⟨hv_close_u, by simp⟩
  have hcommon : common = {u, v} := by
    symm
    apply eq_of_subset_of_card_le huv_subset
    have hc := hsmall huv
    simpa [common, huv] using hc
  have hw : w ∈ common := mem_inter.mpr ⟨hw_close_u, hw_close_v⟩
  rw [hcommon] at hw
  simpa using hw

/-- Once two distinct common closed neighbors are known, the intersection
bound forces every further common closed neighbor to be one of them. -/
theorem common_closedNeighbor_eq_of_two
    (hsmall : G.ClosedNeighborhoodIntersectionsAtMostTwo)
    {a b p q r : V} (hab : a ≠ b)
    (hp_a : p ∈ G.closedNeighborFinset a)
    (hp_b : p ∈ G.closedNeighborFinset b)
    (hq_a : q ∈ G.closedNeighborFinset a)
    (hq_b : q ∈ G.closedNeighborFinset b)
    (hpq : p ≠ q)
    (hr_a : r ∈ G.closedNeighborFinset a)
    (hr_b : r ∈ G.closedNeighborFinset b) :
    r = p ∨ r = q := by
  let common := G.closedNeighborFinset a ∩ G.closedNeighborFinset b
  have hpq_subset : {p, q} ⊆ common := by
    intro z hz
    simp only [mem_insert, mem_singleton] at hz
    rcases hz with rfl | rfl
    · exact mem_inter.mpr ⟨hp_a, hp_b⟩
    · exact mem_inter.mpr ⟨hq_a, hq_b⟩
  have hcommon : common = {p, q} := by
    symm
    apply eq_of_subset_of_card_le hpq_subset
    have hc := hsmall hab
    simpa [common, hpq] using hc
  have hr : r ∈ common := mem_inter.mpr ⟨hr_a, hr_b⟩
  rw [hcommon] at hr
  simpa using hr

/-- Under the two-common-closed-neighbors hypothesis, signatures are
injective on the sons of a father. -/
theorem IsLocatingDominating.injOn_locatingSignature_sons
    {C : Finset V} (hC : G.IsLocatingDominating C)
    (hsmall : G.ClosedNeighborhoodIntersectionsAtMostTwo)
    {x : V} (hx : G.IsFather C x) :
    Set.InjOn (G.locatingSignature C) (G.sons C x) := by
  unfold IsFather at hx
  intro y hy z hz hyz
  have hy' := (mem_filter.mp hy).2
  have hz' := (mem_filter.mp hz).2
  have code_case : ∀ {p q : V}, p ∈ G.sons C x → q ∈ G.sons C x →
      G.locatingSignature C p = G.locatingSignature C q → p ∈ C → p = q := by
    intro p q hp hq hpq hpC
    have hp' := (mem_filter.mp hp).2
    have hq' := (mem_filter.mp hq).2
    have hpp : p ∈ G.locatingSignature C p := by
      simp [locatingSignature, closedNeighborFinset, hpC]
    obtain ⟨a, b, hab, hab_sig⟩ := card_eq_two.mp hp'.1
    have hpab : p = a ∨ p = b := by
      rw [hab_sig] at hpp
      simpa using hpp
    obtain ⟨t, hpt, hpt_sig⟩ :
        ∃ t : V, p ≠ t ∧ G.locatingSignature C p = {p, t} := by
      rcases hpab with hpa | hpb
      · refine ⟨b, ?_, ?_⟩
        · exact hpa.trans_ne hab
        · simpa [hpa] using hab_sig
      · refine ⟨a, ?_, ?_⟩
        · exact hpb.trans_ne hab.symm
        · simpa [hpb, pair_comm] using hab_sig
    have ht_sig_p : t ∈ G.locatingSignature C p := by rw [hpt_sig]; simp
    have hp_sig_x : p ∈ G.locatingSignature C x := hp'.2 (by rw [hpt_sig]; simp)
    have ht_sig_x : t ∈ G.locatingSignature C x := hp'.2 (by rw [hpt_sig]; simp)
    have ht_close_p : t ∈ G.closedNeighborFinset p := (mem_inter.mp ht_sig_p).1
    have hx_endpoint : x = p ∨ x = t :=
      G.common_closedNeighbor_eq_endpoint hsmall hpt ht_close_p
        ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp hp_sig_x).1)
        ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp ht_sig_x).1)
    have hx_ne_p : x ≠ p := by
      intro hxp
      subst x
      omega
    have hxt : x = t := hx_endpoint.resolve_left hx_ne_p
    have hp_sig_q : p ∈ G.locatingSignature C q := by
      rw [← hpq, hpt_sig]
      simp
    have ht_sig_q : t ∈ G.locatingSignature C q := by
      rw [← hpq, hpt_sig]
      simp
    have hq_endpoint : q = p ∨ q = t :=
      G.common_closedNeighbor_eq_endpoint hsmall hpt ht_close_p
        ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp hp_sig_q).1)
        ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp ht_sig_q).1)
    have hq_ne_t : q ≠ t := by
      intro hqt
      have hqx : q = x := hqt.trans hxt.symm
      rw [hqx] at hq'
      omega
    exact (hq_endpoint.resolve_right hq_ne_t).symm
  by_cases hyC : y ∈ C
  · exact code_case hy hz hyz hyC
  · by_cases hzC : z ∈ C
    · exact (code_case hz hy hyz.symm hzC).symm
    · exact hC.2 hyC hzC hyz

/-- A son belongs to at most one father.  This is the disjointness mechanism
behind the family partition, and it uses only the closed-neighborhood
intersection hypothesis. -/
theorem son_has_unique_father
    {C : Finset V} (hsmall : G.ClosedNeighborhoodIntersectionsAtMostTwo)
    {y x x' : V}
    (hyx : y ∈ G.sons C x) (hyx' : y ∈ G.sons C x')
    (hx : G.IsFather C x) (hx' : G.IsFather C x') :
    x = x' := by
  unfold IsFather at hx hx'
  have hy := (mem_filter.mp hyx).2
  have hy' := (mem_filter.mp hyx').2
  obtain ⟨a, b, hab, hab_sig⟩ := card_eq_two.mp hy.1
  have ha_sig_y : a ∈ G.locatingSignature C y := by rw [hab_sig]; simp
  have hb_sig_y : b ∈ G.locatingSignature C y := by rw [hab_sig]; simp
  have ha_sig_x : a ∈ G.locatingSignature C x := hy.2 (by rw [hab_sig]; simp)
  have hb_sig_x : b ∈ G.locatingSignature C x := hy.2 (by rw [hab_sig]; simp)
  have ha_sig_x' : a ∈ G.locatingSignature C x' := hy'.2 (by rw [hab_sig]; simp)
  have hb_sig_x' : b ∈ G.locatingSignature C x' := hy'.2 (by rw [hab_sig]; simp)
  have hx_ne_y : x ≠ y := by
    intro hxy
    subst x
    omega
  have hx'_ne_y : x' ≠ y := by
    intro hxy
    subst x'
    omega
  have hx'_eq : x' = y ∨ x' = x :=
    G.common_closedNeighbor_eq_of_two hsmall hab
      ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp ha_sig_y).1)
      ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp hb_sig_y).1)
      ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp ha_sig_x).1)
      ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp hb_sig_x).1)
      hx_ne_y.symm
      ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp ha_sig_x').1)
      ((G.mem_closedNeighborFinset_comm).mp (mem_inter.mp hb_sig_x').1)
  exact (hx'_eq.resolve_left hx'_ne_y).symm

/-- The son-to-two-subset injection: an `i`-covered father has at most
`choose i 2` sons. -/
theorem IsLocatingDominating.card_sons_le_choose
    {C : Finset V} (hC : G.IsLocatingDominating C)
    (hsmall : G.ClosedNeighborhoodIntersectionsAtMostTwo)
    {x : V} (hx : G.IsFather C x) :
    (G.sons C x).card ≤ Nat.choose (G.locatingSignature C x).card 2 := by
  let f := G.locatingSignature C
  have hinj : Set.InjOn f (G.sons C x) :=
    SimpleGraph.IsLocatingDominating.injOn_locatingSignature_sons G hC hsmall hx
  have himage : (G.sons C x).image f ⊆
      (G.locatingSignature C x).powersetCard 2 := by
    intro s hs
    obtain ⟨y, hy, rfl⟩ := mem_image.mp hs
    exact mem_powersetCard.mpr ⟨(mem_filter.mp hy).2.2, (mem_filter.mp hy).2.1⟩
  calc
    (G.sons C x).card = ((G.sons C x).image f).card :=
      (card_image_of_injOn hinj).symm
    _ ≤ ((G.locatingSignature C x).powersetCard 2).card := card_le_card himage
    _ = Nat.choose (G.locatingSignature C x).card 2 := card_powersetCard _ _

/-- For signature sizes `3` through `6`, the father's excess together with
at most `choose i 2` sons has average excess at least `5/4`. -/
theorem five_mul_family_size_le_four_mul_excess
    {i s : ℕ} (hi_lower : 3 ≤ i) (hi_upper : i ≤ 6)
    (hs : s ≤ Nat.choose i 2) :
    5 * (s + 1) ≤ 4 * ((i - 1) + s) := by
  interval_cases i <;> norm_num [Nat.choose] at hs ⊢ <;> omega

/-- The final integer arithmetic of the specialized `Q₆` lower bound.  Here
`K` is the code size, `E` the total excess, and `F` the number of vertices in
families. -/
theorem card_ge_sixteen_of_q6_family_accounting
    {K E F : ℕ}
    (hincidence : E + 64 = 7 * K)
    (hcoverage : 64 ≤ F + 2 * K)
    (hratio : 5 * F ≤ 4 * E) :
    16 ≤ K := by
  omega

end SimpleGraph

#print axioms SimpleGraph.IsLocatingDominating.card_sons_le_choose
#print axioms SimpleGraph.son_has_unique_father
#print axioms SimpleGraph.five_mul_family_size_le_four_mul_excess
#print axioms SimpleGraph.card_ge_sixteen_of_q6_family_accounting
