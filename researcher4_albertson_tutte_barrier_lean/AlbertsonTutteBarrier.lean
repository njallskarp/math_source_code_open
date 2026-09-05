import Mathlib.Combinatorics.SimpleGraph.Tutte
import Mathlib.Tactic.NormNum

/-!
# Factor-critical graphs and tight witnesses after deleting three vertices

For any finite factor-critical graph `G`, if deleting a three-element set `T`
leaves no perfect matching, there is a set `B` containing `T` such that the
number of odd components of `G - B` is exactly `|B| - 1`.

The proof uses actual induced graphs and Mathlib's matching, component, and
Tutte APIs. Critical coloring, complements, and drawing topology are external.
-/

open Set SimpleGraph

namespace AlbertsonTutteBarrier

variable {V W : Type*}

/-- Vertex deletion as a graph on the remaining subtype. -/
abbrev deleteGraph (G : SimpleGraph V) (S : Set V) := G.induce Sᶜ

/-- A matching in the original graph saturating exactly the complement of `S`. -/
def HasMatchingOff (G : SimpleGraph V) (S : Set V) : Prop :=
  ∃ M : G.Subgraph, M.verts = Sᶜ ∧ M.IsMatching

/-- Factor-criticality in the campaign's original matching-subgraph interface. -/
def FactorCritical (G : SimpleGraph V) : Prop :=
  ∀ a, HasMatchingOff G {a}

/-- The count uses Mathlib's actual odd connected components. -/
noncomputable def oddCount (G : SimpleGraph V) (S : Set V) : ℕ :=
  (deleteGraph G S).oddComponents.ncard

theorem hasMatchingOff_iff (G : SimpleGraph V) (S : Set V) :
    HasMatchingOff G S ↔ ∃ M : (deleteGraph G S).Subgraph, M.IsPerfectMatching := by
  constructor
  · rintro ⟨M, hverts, hM⟩
    let N : (deleteGraph G S).Subgraph :=
      { verts := Set.univ
        Adj := fun v w => M.Adj v.val w.val
        adj_sub := fun h => h.adj_sub
        edge_vert := fun _ => Set.mem_univ _
        symm := ⟨fun _ _ h => h.symm⟩ }
    refine ⟨N, ?_, fun _ => Set.mem_univ _⟩
    intro v _
    have hvM : v.val ∈ M.verts := by rw [hverts]; exact v.property
    obtain ⟨w, hvw, huniq⟩ := hM hvM
    have hwS : w ∈ Sᶜ := by rw [← hverts]; exact hvw.snd_mem
    refine ⟨⟨w, hwS⟩, hvw, ?_⟩
    intro z hz
    exact Subtype.ext (huniq z.val hz)
  · rintro ⟨M, hM⟩
    let f : deleteGraph G S →g G := ⟨Subtype.val, fun h => h⟩
    refine ⟨M.map f, ?_, hM.1.map f Subtype.val_injective⟩
    rw [SimpleGraph.Subgraph.map_verts, hM.2.verts_eq_univ]
    ext v
    change (∃ x : (Sᶜ : Set V), x ∈ Set.univ ∧ x.val = v) ↔ v ∈ Sᶜ
    constructor
    · rintro ⟨x, _, rfl⟩
      exact x.property
    · intro hv
      exact ⟨⟨v, hv⟩, Set.mem_univ _, rfl⟩

/-- Matchings and odd-component counts are invariant under graph isomorphism. -/
theorem oddComponents_ncard_eq_of_iso {G : SimpleGraph V} {H : SimpleGraph W}
    (e : G ≃g H) : G.oddComponents.ncard = H.oddComponents.ncard := by
  apply Set.ncard_congr'
  apply e.connectedComponentEquiv.subtypeEquiv
  intro c
  change Odd c.supp.ncard ↔ Odd (e.connectedComponentEquiv c).supp.ncard
  rw [Set.ncard_congr' (c.isoEquivSupp e)]

/-- Relate induced-complement deletion to the subgraph deletion used by Tutte. -/
def tutteDeleteIso (G : SimpleGraph V) (S : Set V) :
    ((⊤ : G.Subgraph).deleteVerts S).coe ≃g deleteGraph G S where
  toFun v := ⟨v.val, v.property.2⟩
  invFun v := ⟨v.val, Set.mem_univ _, v.property⟩
  left_inv _ := rfl
  right_inv _ := rfl
  map_rel_iff' := by intro a b; simp [a.property.2, b.property.2]

theorem tutte_iff (G : SimpleGraph V) [Finite V] :
    (∃ M : G.Subgraph, M.IsPerfectMatching) ↔ ∀ S, oddCount G S ≤ S.ncard := by
  rw [SimpleGraph.tutte]
  apply forall_congr'
  intro S
  rw [SimpleGraph.IsTutteViolator, not_lt,
    oddComponents_ncard_eq_of_iso (tutteDeleteIso G S)]
  rfl

/-- A second deletion is the union of the two actual removed vertex sets. -/
def deleteDeleteIso (G : SimpleGraph V) (R : Set V) (S : Set (Rᶜ : Set V)) :
    deleteGraph (deleteGraph G R) S ≃g deleteGraph G (R ∪ Subtype.val '' S) where
  toFun v := ⟨v.val.val, by
    rintro (hR | ⟨w, hw, heq⟩)
    · exact v.val.property hR
    · exact v.property (Subtype.ext heq ▸ hw)⟩
  invFun v := ⟨⟨v.val, fun h => v.property (Or.inl h)⟩,
    fun h => v.property (Or.inr ⟨_, h, rfl⟩)⟩
  left_inv _ := rfl
  right_inv _ := rfl
  map_rel_iff' := Iff.rfl

theorem oddCount_delete (G : SimpleGraph V) (R : Set V) (S : Set (Rᶜ : Set V)) :
    oddCount (deleteGraph G R) S = oddCount G (R ∪ Subtype.val '' S) :=
  oddComponents_ncard_eq_of_iso (deleteDeleteIso G R S)

theorem disjoint_image_remaining (R : Set V) (S : Set (Rᶜ : Set V)) :
    Disjoint R (Subtype.val '' S) := by
  rw [Set.disjoint_left]
  rintro v hv ⟨w, _, rfl⟩
  exact w.property hv

theorem ncard_union_image_remaining [Finite V] (R : Set V) (S : Set (Rᶜ : Set V)) :
    (R ∪ Subtype.val '' S).ncard = R.ncard + S.ncard := by
  rw [Set.ncard_union_eq (disjoint_image_remaining R S),
    Set.ncard_image_of_injective S Subtype.val_injective]

/-- The strict Tutte violation has gap at least two when the graph has even order. -/
theorem exists_oddCount_gap_two (G : SimpleGraph V) [Finite V]
    (heven : Even (Nat.card V))
    (hno : ¬ ∃ M : G.Subgraph, M.IsPerfectMatching) :
    ∃ S, S.ncard + 2 ≤ oddCount G S := by
  rw [tutte_iff] at hno
  push Not at hno
  obtain ⟨S, hS⟩ := hno
  refine ⟨S, ?_⟩
  have hparity : Odd (oddCount G S) ↔ Odd S.ncard := by
    rw [oddCount, SimpleGraph.odd_ncard_oddComponents, Nat.card_coe_set_eq,
      Set.odd_ncard_compl_iff heven]
  rw [Nat.odd_iff, Nat.odd_iff] at hparity
  omega

/-- Every nonempty deletion set in a factor-critical graph has odd-component
deficiency at most minus one. This uses a perfect matching after deleting one
vertex of the set, not the weaker maximum-matching deficiency bound. -/
theorem FactorCritical.oddCount_add_one_le (G : SimpleGraph V) [Finite V]
    (hfc : FactorCritical G) {B : Set V} (hne : B.Nonempty) :
    oddCount G B + 1 ≤ B.ncard := by
  obtain ⟨a, ha⟩ := hne
  let R : Set V := {a}
  let S : Set (Rᶜ : Set V) := {v | v.val ∈ B}
  have hunion : R ∪ Subtype.val '' S = B := by
    ext v
    constructor
    · rintro (hv | ⟨w, hw, rfl⟩)
      · simpa only [R, Set.mem_singleton_iff.mp hv] using ha
      · exact hw
    · intro hv
      by_cases hva : v = a
      · exact Or.inl hva
      · exact Or.inr ⟨⟨v, hva⟩, hv, rfl⟩
  obtain ⟨M, hM⟩ := (hasMatchingOff_iff G R).mp (hfc a)
  have hbound := (tutte_iff (deleteGraph G R)).mp ⟨M, hM⟩ S
  rw [oddCount_delete, hunion] at hbound
  have hcard := ncard_union_image_remaining R S
  rw [hunion] at hcard
  have hR : R.ncard = 1 := Set.ncard_singleton a
  omega

/-- A nonempty factor-critical graph has odd order. -/
theorem FactorCritical.odd_card (G : SimpleGraph V) [Finite V] [Nonempty V]
    (hfc : FactorCritical G) : Odd (Nat.card V) := by
  classical
  let a : V := Classical.choice inferInstance
  obtain ⟨M, hM⟩ := (hasMatchingOff_iff G {a}).mp (hfc a)
  let := Fintype.ofFinite (({a} : Set V)ᶜ : Set V)
  have heven : Even (({a} : Set V)ᶜ.ncard) := by
    simpa only [← Nat.card_eq_fintype_card, Nat.card_coe_set_eq] using hM.even_card
  have hcard := Set.ncard_add_ncard_compl ({a} : Set V)
  rw [Set.ncard_singleton] at hcard
  rw [Nat.odd_iff]
  rw [Nat.even_iff] at heven
  omega

/-- Tutte extraction with exact cardinal transport, for any deletion set with
even-order complement. No factor-criticality is required for this lower bound. -/
theorem exists_deletion_witness (G : SimpleGraph V) [Finite V]
    (T : Set V) (heven : Even (Nat.card (Tᶜ : Set V)))
    (hno : ¬ HasMatchingOff G T) :
    ∃ B : Set V, T ⊆ B ∧ B.ncard + 2 ≤ oddCount G B + T.ncard := by
  have hno' := (hasMatchingOff_iff G T).not.mp hno
  obtain ⟨S, hS⟩ := exists_oddCount_gap_two (deleteGraph G T) heven hno'
  refine ⟨T ∪ Subtype.val '' S, Set.subset_union_left, ?_⟩
  rw [ncard_union_image_remaining]
  rw [oddCount_delete] at hS
  omega

/-- A nonconformal three-set in any finite factor-critical graph extends to a
tight odd-component deletion set. Triangle adjacency is unnecessary. -/
theorem exists_tight_witness_of_three_deleted (G : SimpleGraph V) [Finite V]
    (hfc : FactorCritical G) (T : Set V) (hT : T.ncard = 3)
    (hno : ¬ HasMatchingOff G T) :
    ∃ B : Set V, T ⊆ B ∧ oddCount G B + 1 = B.ncard := by
  have hne : T.Nonempty := (Set.ncard_pos (Set.toFinite T)).mp (by omega)
  let : Nonempty V := hne.to_subtype.map Subtype.val
  have hodd := hfc.odd_card G
  have hcardT := Set.ncard_add_ncard_compl T
  have heven : Even (Nat.card (Tᶜ : Set V)) := by
    rw [Nat.card_coe_set_eq, Nat.even_iff]
    rw [Nat.odd_iff] at hodd
    omega
  obtain ⟨B, hTB, hlower⟩ := exists_deletion_witness G T heven hno
  have hBne : B.Nonempty := hne.mono hTB
  have hupper := hfc.oddCount_add_one_le G hBne
  refine ⟨B, hTB, ?_⟩
  omega

end AlbertsonTutteBarrier
