import AlbertsonCliqueMatching

/-!
# The finite consumer of large-class deletion colorings

At order `2*k+1`, proper deletion colorings with `k` colors and at least two
vertices in every color class produce near-perfect matchings in the complement.
The theorem supplying the deletion colorings (Stehlík) remains external.
-/

open Set SimpleGraph
open scoped BigOperators

namespace AlbertsonTutteBarrier

variable {V A : Type*} {G : SimpleGraph V}

/-- Finite fiber counting, with no graph or uniformity hypothesis. -/
theorem sum_fiber_ncard [Finite V] [Fintype A] (f : V → A) :
    ∑ a, (f ⁻¹' {a}).ncard = Nat.card V := by
  classical
  let := Fintype.ofFinite V
  have hfiber (a : A) :
      (Finset.univ.filter (fun v => f v = a)).card = (f ⁻¹' {a}).ncard := by
    have heq : (↑(Finset.univ.filter (fun v => f v = a)) : Set V) =
        f ⁻¹' {a} := by ext v; simp
    rw [← Set.ncard_coe_finset, heq]
  have h := Finset.card_eq_sum_card_fiberwise (f := f)
    (s := Finset.univ) (t := Finset.univ) (by intro v _; simp)
  simp_rw [hfiber] at h
  simpa [Nat.card_eq_fintype_card] using h.symm

/-- If every fiber has size at least `d` and the total size is exactly `d`
times the palette size, then every fiber has size exactly `d`. -/
theorem fiber_ncard_eq_of_lower [Finite V] [Fintype A] (f : V → A) {d : ℕ}
    (htotal : Nat.card V = d * Fintype.card A)
    (hlower : ∀ a, d ≤ (f ⁻¹' {a}).ncard) :
    ∀ a, (f ⁻¹' {a}).ncard = d := by
  have hsum : (∑ _a : A, d) = ∑ a, (f ⁻¹' {a}).ncard := by
    rw [sum_fiber_ncard, htotal]
    simp [Nat.mul_comm]
  have heq := (Finset.sum_eq_sum_iff_of_le (fun a _ => hlower a)).mp hsum
  intro a
  exact (heq a (Finset.mem_univ a)).symm

/-- Every vertex in a two-element fiber has exactly one different vertex in
the same fiber. This is a finite-set fact, not a matching assumption. -/
theorem existsUnique_other_of_fiber_two (f : V → A)
    (hpair : ∀ a, (f ⁻¹' {a}).ncard = 2) (v : V) :
    ∃! w, v ≠ w ∧ f v = f w := by
  obtain ⟨x, y, hxy, hset⟩ := Set.ncard_eq_two.mp (hpair (f v))
  have hv : v = x ∨ v = y := by
    have : v ∈ f ⁻¹' {f v} := rfl
    rw [hset] at this
    exact this
  have hx : f x = f v := by
    change x ∈ f ⁻¹' {f v}
    rw [hset]
    simp
  have hy : f y = f v := by
    change y ∈ f ⁻¹' {f v}
    rw [hset]
    simp
  rcases hv with rfl | rfl
  · refine ⟨y, ⟨hxy, hy.symm⟩, ?_⟩
    intro w hw
    have hmem : w ∈ f ⁻¹' {f v} := hw.2.symm
    rw [hset] at hmem
    rcases hmem with rfl | rfl
    · exact (hw.1 rfl).elim
    · rfl
  · refine ⟨x, ⟨hxy.symm, hx.symm⟩, ?_⟩
    intro w hw
    have hmem : w ∈ f ⁻¹' {f v} := hw.2.symm
    rw [hset] at hmem
    rcases hmem with rfl | rfl
    · rfl
    · exact (hw.1 rfl).elim

/-- Equal-colored distinct vertices form an actual perfect matching of the
complement when each color class has size two. -/
theorem perfectMatching_compl_of_pair_coloring (C : G.Coloring A)
    (hpair : ∀ a, (C.colorClass a).ncard = 2) :
    ∃ M : Gᶜ.Subgraph, M.IsPerfectMatching := by
  let M : Gᶜ.Subgraph :=
    { verts := Set.univ
      Adj := fun v w => v ≠ w ∧ C v = C w
      adj_sub := fun h => ⟨h.1, fun hvw => C.valid hvw h.2⟩
      edge_vert := fun _ => Set.mem_univ _
      symm := ⟨fun _ _ h => ⟨h.1.symm, h.2.symm⟩⟩ }
  refine ⟨M, ?_, fun _ => Set.mem_univ _⟩
  intro v _
  exact existsUnique_other_of_fiber_two C hpair v

/-- The parameterized finite consumer of the lower bound on color classes. -/
theorem perfectMatching_compl_of_large_classes [Finite V] [Fintype A]
    (C : G.Coloring A) (htotal : Nat.card V = 2 * Fintype.card A)
    (hlower : ∀ a, 2 ≤ (C.colorClass a).ncard) :
    ∃ M : Gᶜ.Subgraph, M.IsPerfectMatching := by
  exact perfectMatching_compl_of_pair_coloring C
    (fiber_ncard_eq_of_lower C htotal hlower)

/-- Lift a complementary matching on an induced subtype to the original vertex
type, with its saturated vertex set exactly the inducing set. -/
theorem matching_on_set_of_pair_coloring (S : Set V) (C : (G.induce S).Coloring A)
    (hpair : ∀ a, (C.colorClass a).ncard = 2) :
    ∃ M : Gᶜ.Subgraph, M.verts = S ∧ M.IsMatching := by
  obtain ⟨M, hM⟩ := perfectMatching_compl_of_pair_coloring C hpair
  let f : (G.induce S)ᶜ →g Gᶜ :=
    ⟨Subtype.val, fun h => ⟨fun heq => h.1 (Subtype.ext heq), h.2⟩⟩
  refine ⟨M.map f, ?_, hM.1.map f Subtype.val_injective⟩
  rw [SimpleGraph.Subgraph.map_verts, hM.2.verts_eq_univ]
  ext v
  change (∃ x : S, x ∈ Set.univ ∧ x.val = v) ↔ v ∈ S
  constructor
  · rintro ⟨x, _, rfl⟩
    exact x.property
  · intro hv
    exact ⟨⟨v, hv⟩, Set.mem_univ _, rfl⟩

/-- The supplied endpoint of Stehlík's theorem. Its existence from criticality
and connected complement is not assumed as a new Lean axiom or proved here. -/
def HasLargeDeletionColorings (G : SimpleGraph V) (k : ℕ) : Prop :=
  ∀ v, ∃ C : (deleteGraph G {v}).Coloring (Fin k),
    ∀ c, 2 ≤ (C.colorClass c).ncard

/-- At order `2*k+1`, the large-class deletion-coloring endpoint yields
factor-criticality of the complement. -/
theorem factorCritical_compl_of_deletion_colorings [Finite V] {k : ℕ}
    (horder : Nat.card V = 2 * k + 1) (hdel : HasLargeDeletionColorings G k) :
    FactorCritical Gᶜ := by
  intro v
  obtain ⟨C, hlower⟩ := hdel v
  have hsum := Set.ncard_add_ncard_compl ({v} : Set V)
  have htotal : Nat.card (({v} : Set V)ᶜ : Set V) = 2 * Fintype.card (Fin k) := by
    rw [Nat.card_coe_set_eq, Fintype.card_fin]
    simp only [Set.ncard_singleton] at hsum
    omega
  exact matching_on_set_of_pair_coloring _ C
    (fiber_ncard_eq_of_lower C htotal hlower)

/-- The full finite consumer: supplied deletion colorings, order, and chromatic
number yield a tight witness for every triangle of the complement. -/
theorem exists_tight_witness_of_deletion_colorings [Finite V] {k : ℕ}
    (horder : Nat.card V = 2 * k + 1) (hdel : HasLargeDeletionColorings G k)
    (hchrom : (k : ℕ∞) < G.chromaticNumber) (T : Set V)
    (hclique : Gᶜ.IsClique T) (hT : T.ncard = 3) :
    ∃ B : Set V, T ⊆ B ∧ oddCount Gᶜ B + 1 = B.ncard := by
  exact exists_tight_witness_of_chromaticNumber
    (factorCritical_compl_of_deletion_colorings horder hdel) horder
    (by simpa using hchrom) T hclique hT

end AlbertsonTutteBarrier
