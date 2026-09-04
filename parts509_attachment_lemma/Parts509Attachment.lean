import Mathlib.Combinatorics.SimpleGraph.Connectivity.Subgraph
import Mathlib.Combinatorics.SimpleGraph.Finite

/-!
# Connectivity after adjoining low-degree independent vertices

This file formalizes the vertex-deletion half of the attachment lemma isolated
in the independent review of the strict Parts-509 graph.  The finite Parts graph
and its path certificate remain external: the theorems below begin from the
certificate's abstract conclusion that the induced core stays connected after
small vertex deletions.
-/

namespace Parts509Attachment

open Set

set_option linter.unusedSectionVars false

universe u

variable {V : Type u} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

/-- The graph left after deleting a finite set of vertices, expressed using
Mathlib's induced-subgraph connectivity predicate. -/
def DeleteConnected (S : Finset V) : Prop :=
  (G.induce {v | v ∉ S}).Connected

/-- The surviving core after deleting the attached set `D` and the fault set
`S`. -/
def CoreDeleteConnected (D S : Finset V) : Prop :=
  (G.induce {v | v ∉ D ∧ v ∉ S}).Connected

/-- If the surviving core is connected and every surviving attached vertex has
a surviving neighbour, then the entire surviving graph is connected.  The
`h_toCore` hypothesis says that all neighbours of an attached vertex lie in the
core; in particular, the attached set is independent. -/
theorem deleteConnected_of_core_and_attachments
    {D S : Finset V}
    (hcore : CoreDeleteConnected G D S)
    (h_toCore : ∀ ⦃x⦄, x ∈ D → ∀ ⦃y⦄, G.Adj x y → y ∉ D)
    (hsurvives : ∀ x ∈ D, x ∉ S → ∃ y, y ∉ S ∧ G.Adj x y) :
    DeleteConnected G S := by
  change (G.induce {v | v ∉ D ∧ v ∉ S}).Connected at hcore
  rw [DeleteConnected, SimpleGraph.connected_iff_exists_forall_reachable]
  obtain ⟨u, huD, huS⟩ := hcore.nonempty
  refine ⟨⟨u, huS⟩, ?_⟩
  rintro ⟨v, hvS⟩
  by_cases hvD : v ∈ D
  · obtain ⟨y, hyS, hxy⟩ := hsurvives v hvD hvS
    have hyD : y ∉ D := h_toCore hvD hxy
    have huy := hcore ⟨u, huD, huS⟩ ⟨y, hyD, hyS⟩
    have huy' : (G.induce {z | z ∉ S}).Reachable ⟨u, huS⟩ ⟨y, hyS⟩ :=
      huy.map (SimpleGraph.induceHomOfLE G fun _ hz => hz.2).toHom
    have hyv : (G.induce {z | z ∉ S}).Adj ⟨y, hyS⟩ ⟨v, hvS⟩ := by
      simpa using hxy.symm
    exact huy'.trans hyv.reachable
  · exact (hcore ⟨u, huD, huS⟩ ⟨v, hvD, hvS⟩).map
      (SimpleGraph.induceHomOfLE G fun _ hz => hz.2).toHom

/-- A surviving attached vertex whose whole neighbourhood is deleted makes the
surviving graph disconnected.  Connectedness of the surviving core supplies a
second vertex, so this statement also handles Mathlib's nonempty convention for
connected graphs explicitly. -/
theorem not_deleteConnected_of_neighborFinset_subset
    {D S : Finset V}
    (hcore : CoreDeleteConnected G D S)
    {x : V} (hxD : x ∈ D) (hxS : x ∉ S)
    (hsub : G.neighborFinset x ⊆ S) :
    ¬ DeleteConnected G S := by
  change (G.induce {v | v ∉ D ∧ v ∉ S}).Connected at hcore
  intro hconn
  change (G.induce {v | v ∉ S}).Connected at hconn
  obtain ⟨u, huD, huS⟩ := hcore.nonempty
  have hxu : x ≠ u := fun h => huD (h ▸ hxD)
  let x' : {v : V // v ∉ S} := ⟨x, hxS⟩
  let u' : {v : V // v ∉ S} := ⟨u, huS⟩
  have hxu' : x' ≠ u' := fun h => hxu (congrArg Subtype.val h)
  have hxiso : (G.induce {v | v ∉ S}).IsIsolated x' := by
    intro w hxw
    have hxwG : G.Adj x w := by simpa [x'] using hxw
    have hwmem : (w : V) ∈ G.neighborFinset x :=
      G.mem_neighborFinset x w |>.2 hxwG
    exact w.property (hsub hwmem)
  have hxnotiso : ¬(G.induce {v | v ∉ S}).IsIsolated x' :=
    (G.induce {v | v ∉ S}).mem_support_iff_not_isIsolated.mp <|
      SimpleGraph.mem_support_of_reachable hxu' (hconn x' u')
  exact hxnotiso hxiso

/-- For a fixed fault set of size at most the attachment degree, disconnectedness
is equivalent to deleting the complete neighbourhood of a surviving attached
vertex. -/
theorem deleteConnected_iff_no_deleted_neighborhood
    {D S : Finset V}
    (hcore : CoreDeleteConnected G D S)
    (h_toCore : ∀ ⦃x⦄, x ∈ D → ∀ ⦃y⦄, G.Adj x y → y ∉ D) :
    DeleteConnected G S ↔
      ∀ x ∈ D, x ∉ S → ¬G.neighborFinset x ⊆ S := by
  constructor
  · intro hconn x hxD hxS hsub
    exact not_deleteConnected_of_neighborFinset_subset G hcore hxD hxS hsub hconn
  · intro h
    apply deleteConnected_of_core_and_attachments G hcore h_toCore
    intro x hxD hxS
    have hnsub := h x hxD hxS
    rw [Finset.not_subset] at hnsub
    obtain ⟨y, hyN, hyS⟩ := hnsub
    exact ⟨y, hyS, G.mem_neighborFinset x y |>.1 hyN⟩

/-- Generic minimum-vertex-cut classification for an attached independent set.
If the core survives every deletion of at most `d` vertices and every attached
vertex has degree `d`, then every disconnecting set of size at most `d` is
exactly the neighbourhood of a surviving attached vertex. -/
theorem small_vertex_cut_iff_eq_neighborFinset
    {D S : Finset V} {d : ℕ}
    (hcore : ∀ T : Finset V, T.card ≤ d → CoreDeleteConnected G D T)
    (h_toCore : ∀ ⦃x⦄, x ∈ D → ∀ ⦃y⦄, G.Adj x y → y ∉ D)
    (hdegree : ∀ x ∈ D, (G.neighborFinset x).card = d)
    (hS : S.card ≤ d) :
    ¬DeleteConnected G S ↔
      ∃ x ∈ D, x ∉ S ∧ S = G.neighborFinset x := by
  rw [deleteConnected_iff_no_deleted_neighborhood G (hcore S hS) h_toCore]
  push Not
  constructor
  · rintro ⟨x, hxD, hxS, hxsub⟩
    refine ⟨x, hxD, hxS, ?_⟩
    exact (Finset.eq_of_subset_of_card_le hxsub <| by
      simpa [hdegree x hxD] using hS).symm
  · rintro ⟨x, hxD, hxS, rfl⟩
    exact ⟨x, hxD, hxS, Finset.Subset.rfl⟩

/-- Every attached vertex supplies a disconnecting set of exactly its degree. -/
theorem attached_neighborhood_disconnects
    {D : Finset V} {d : ℕ}
    (hcore : ∀ T : Finset V, T.card ≤ d → CoreDeleteConnected G D T)
    (h_toCore : ∀ ⦃x⦄, x ∈ D → ∀ ⦃y⦄, G.Adj x y → y ∉ D)
    (hdegree : ∀ x ∈ D, (G.neighborFinset x).card = d)
    {x : V} (hxD : x ∈ D) :
    ¬DeleteConnected G (G.neighborFinset x) := by
  apply (small_vertex_cut_iff_eq_neighborFinset G hcore h_toCore hdegree
    (hdegree x hxD).le).2
  exact ⟨x, hxD, G.notMem_neighborFinset_self x, rfl⟩

/-- Consequently, every disconnecting set no larger than the attachment degree
has cardinality exactly that degree. -/
theorem small_vertex_cut_card_eq
    {D S : Finset V} {d : ℕ}
    (hcore : ∀ T : Finset V, T.card ≤ d → CoreDeleteConnected G D T)
    (h_toCore : ∀ ⦃x⦄, x ∈ D → ∀ ⦃y⦄, G.Adj x y → y ∉ D)
    (hdegree : ∀ x ∈ D, (G.neighborFinset x).card = d)
    (hS : S.card ≤ d) (hcut : ¬DeleteConnected G S) :
    S.card = d := by
  obtain ⟨x, hxD, -, rfl⟩ :=
    (small_vertex_cut_iff_eq_neighborFinset G hcore h_toCore hdegree hS).1 hcut
  exact hdegree x hxD

/-- If the attached set is nonempty, the deletion-connectivity threshold is
exactly `d`: fewer than `d` deleted vertices never disconnect, while one
neighbourhood of size `d` does. -/
theorem attachment_vertex_connectivity_threshold
    {D : Finset V} {d : ℕ}
    (hcore : ∀ T : Finset V, T.card ≤ d → CoreDeleteConnected G D T)
    (h_toCore : ∀ ⦃x⦄, x ∈ D → ∀ ⦃y⦄, G.Adj x y → y ∉ D)
    (hdegree : ∀ x ∈ D, (G.neighborFinset x).card = d)
    (hD : D.Nonempty) :
    (∀ S : Finset V, S.card < d → DeleteConnected G S) ∧
      ∃ S : Finset V, S.card = d ∧ ¬DeleteConnected G S := by
  constructor
  · intro S hS
    by_contra hcut
    have := small_vertex_cut_card_eq G hcore h_toCore hdegree hS.le hcut
    omega
  · obtain ⟨x, hxD⟩ := hD
    exact ⟨G.neighborFinset x, hdegree x hxD,
      attached_neighborhood_disconnects G hcore h_toCore hdegree hxD⟩

/-- The literal degree-four specialization used by the strict Parts-509 graph.
The concrete facts about its 503-vertex core and six degree-four vertices are
deliberately kept as explicit hypotheses. -/
theorem degree_four_attachment_vertex_cuts
    {D S : Finset V}
    (hcore : ∀ T : Finset V, T.card ≤ 4 → CoreDeleteConnected G D T)
    (h_toCore : ∀ ⦃x⦄, x ∈ D → ∀ ⦃y⦄, G.Adj x y → y ∉ D)
    (hdegree : ∀ x ∈ D, (G.neighborFinset x).card = 4)
    (hS : S.card ≤ 4) :
    ¬DeleteConnected G S ↔
      ∃ x ∈ D, x ∉ S ∧ S = G.neighborFinset x :=
  small_vertex_cut_iff_eq_neighborFinset G hcore h_toCore hdegree hS

#print axioms deleteConnected_of_core_and_attachments
#print axioms not_deleteConnected_of_neighborFinset_subset
#print axioms deleteConnected_iff_no_deleted_neighborhood
#print axioms small_vertex_cut_iff_eq_neighborFinset
#print axioms attached_neighborhood_disconnects
#print axioms small_vertex_cut_card_eq
#print axioms attachment_vertex_connectivity_threshold
#print axioms degree_four_attachment_vertex_cuts

end Parts509Attachment
