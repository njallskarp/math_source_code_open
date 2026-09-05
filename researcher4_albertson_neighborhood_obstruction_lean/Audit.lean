import AlbertsonNeighborhoodObstruction
import AlbertsonReservoirCapacity
import AlbertsonSingletonComponents

#print axioms AlbertsonNeighborhoodObstruction.foldHom
#print axioms AlbertsonNeighborhoodObstruction.chromaticNumber_delete_eq_of_neighborSet_subset
#print axioms AlbertsonNeighborhoodObstruction.not_neighborSet_subset_of_chromatic_drop
#print axioms AlbertsonNeighborhoodObstruction.neighborSet_subset_of_compl_domination
#print axioms AlbertsonNeighborhoodObstruction.exists_compl_neighbor_not_adjacent
#print axioms AlbertsonNeighborhoodObstruction.not_isClique_of_neighborSet_subset

#check AlbertsonNeighborhoodObstruction.exists_compl_neighbor_not_adjacent
#check AlbertsonNeighborhoodObstruction.not_isClique_of_neighborSet_subset

#print axioms AlbertsonNeighborhoodObstruction.extendDeletionColoring
#print axioms AlbertsonNeighborhoodObstruction.exists_neighbor_of_color
#print axioms AlbertsonNeighborhoodObstruction.exists_reservoir_same_color
#print axioms AlbertsonNeighborhoodObstruction.exists_reservoir_injection
#print axioms AlbertsonNeighborhoodObstruction.reservoir_card_bound
#print axioms AlbertsonNeighborhoodObstruction.not_common_neighbor_of_singleton_reservoir
#print axioms AlbertsonNeighborhoodObstruction.disjoint_clique_neighbors_of_singleton_reservoir
#print axioms AlbertsonNeighborhoodObstruction.disjoint_clique_neighbors_of_chromatic_drop

#check AlbertsonNeighborhoodObstruction.exists_reservoir_injection
#check AlbertsonNeighborhoodObstruction.reservoir_card_bound
#check AlbertsonNeighborhoodObstruction.disjoint_clique_neighbors_of_chromatic_drop

#print axioms AlbertsonNeighborhoodObstruction.neighborSet_subset_of_singleton_component
#print axioms AlbertsonNeighborhoodObstruction.card_add_card_le_of_singleton_overlap
#print axioms AlbertsonNeighborhoodObstruction.disjoint_clique_neighbors_of_singleton_components
#print axioms AlbertsonNeighborhoodObstruction.degree_add_degree_le_of_singleton_components

#check AlbertsonNeighborhoodObstruction.degree_add_degree_le_of_singleton_components

-- The height-2933 four-clique consumer, with all structural premises still explicit.
example {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] {k : ℕ} (hchi : G.chromaticNumber = (k : ℕ∞) + 1)
    (Q : Finset V) (s : V) (hQ : Gᶜ.IsClique (Q : Set V)) (hcard : Q.card = 4)
    (hdrop : ∀ a ∈ Q, (G.induce {x | x ≠ a}).chromaticNumber < G.chromaticNumber)
    (w z : ↑(((Q : Set V) ∪ {s})ᶜ)) (hwz : w ≠ z)
    (hw : ((Gᶜ.induce ((Q : Set V) ∪ {s})ᶜ).connectedComponentMk w).supp = {w})
    (hz : ((Gᶜ.induce ((Q : Set V) ∪ {s})ᶜ).connectedComponentMk z).supp = {z}) :
    Gᶜ.degree w.val + Gᶜ.degree z.val ≤ 6 := by
  simpa [hcard] using
    AlbertsonNeighborhoodObstruction.degree_add_degree_le_of_singleton_components
      hchi Q s hQ hdrop w z hwz hw hz
