import GallaiBlockSpectrum
import Mathlib.Algebra.BigOperators.Fin

/-!
# Representation-neutral atomization of Gallai block summaries

This file closes the algebraic interface between a finite list of Gallai block
summaries and the clique-atom packing used by `GallaiBlockSpectrum`.  It does
not construct graph-theoretic blocks: a caller supplies a list tagged as
clique or odd cycle together with the elementary validity conditions.

Every clique block is one atom.  An odd cycle with increment `u` is replaced
by one size-2 atom and `u-2` size-1 atoms.  The construction preserves total
block increment and total edge count, including multiplicity.  Consequently
the Bellman certificates and the two relaxed spectrum gaps apply directly to
valid block-summary lists.
-/

open scoped BigOperators

namespace AlbertsonGallaiBlockSpectrum

/-- The only information about a Gallai block needed by the finite packing
argument: its type and its increment `|V(B)| - 1`. -/
inductive BlockSummary where
  | clique (increment : ℕ)
  | oddCycle (increment : ℕ)
  deriving DecidableEq, Repr

namespace BlockSummary

def units : BlockSummary → ℕ
  | .clique u => u
  | .oddCycle u => u

def edges : BlockSummary → ℕ
  | .clique u => cliqueEdges u
  | .oddCycle u => u + 1

/-- The canonical positive clique-atom expansion of a block summary. -/
def atoms : BlockSummary → List ℕ
  | .clique u => [u]
  | .oddCycle u => 2 :: List.replicate (u - 2) 1

/-- Clique increments are positive.  Odd-cycle increments are positive even
numbers, as their orders are odd and at least three. -/
def Valid : BlockSummary → Prop
  | .clique u => 0 < u
  | .oddCycle u => 2 ≤ u ∧ Even u

/-- A clique block must obey the supplied cap; an odd-cycle expansion needs
only room for its largest canonical atom, which has size two. -/
def FitsAtomCap (cap : ℕ) : BlockSummary → Prop
  | .clique u => u ≤ cap
  | .oddCycle _ => 2 ≤ cap

theorem atoms_sum_eq_units (block : BlockSummary) (hvalid : block.Valid) :
    block.atoms.sum = block.units := by
  cases block with
  | clique u => simp [atoms, units]
  | oddCycle u =>
      rcases hvalid with ⟨hu, _⟩
      simp [atoms, units]
      omega

theorem atoms_edge_sum_eq_edges (block : BlockSummary) (hvalid : block.Valid) :
    (block.atoms.map cliqueEdges).sum = block.edges := by
  cases block with
  | clique u => simp [atoms, edges]
  | oddCycle u =>
      rcases hvalid with ⟨hu, _⟩
      simpa [atoms, edges] using (oddCycle_compression u hu).2.symm

theorem atom_positive (block : BlockSummary) (hvalid : block.Valid)
    {u : ℕ} (hu : u ∈ block.atoms) : 0 < u := by
  cases block with
  | clique increment =>
      simp only [atoms, List.mem_singleton] at hu
      simpa [Valid, hu] using hvalid
  | oddCycle increment =>
      simp only [atoms, List.mem_cons, List.mem_replicate] at hu
      rcases hu with rfl | ⟨_, rfl⟩ <;> omega

theorem atom_le_cap (block : BlockSummary) {cap u : ℕ}
    (hcap : block.FitsAtomCap cap) (hu : u ∈ block.atoms) : u ≤ cap := by
  cases block with
  | clique increment =>
      simp only [atoms, List.mem_singleton] at hu
      simpa [FitsAtomCap, hu] using hcap
  | oddCycle increment =>
      simp only [atoms, List.mem_cons, List.mem_replicate] at hu
      rcases hu with rfl | ⟨_, rfl⟩ <;> simp only [FitsAtomCap] at hcap <;> omega

/-- Atoms larger than two come from, and only from, clique blocks of the same
increment.  In particular odd-cycle compression cannot manufacture a K25 or
K26-sized atom. -/
theorem large_mem_atoms_iff {k : ℕ} (hk : 2 < k) (block : BlockSummary) :
    k ∈ block.atoms ↔ block = .clique k := by
  cases block with
  | clique u => simp [atoms, eq_comm]
  | oddCycle u =>
      constructor
      · intro h
        simp only [atoms, List.mem_cons, List.mem_replicate] at h
        rcases h with h | ⟨_, h⟩ <;> omega
      · intro h
        cases h

end BlockSummary

/-- Expand a finite block-summary list, retaining multiplicity. -/
def atomize (blocks : List BlockSummary) : List ℕ :=
  blocks.flatMap BlockSummary.atoms

def totalBlockUnits (blocks : List BlockSummary) : ℕ :=
  (blocks.map BlockSummary.units).sum

def totalBlockEdges (blocks : List BlockSummary) : ℕ :=
  (blocks.map BlockSummary.edges).sum

def ValidBlockList (blocks : List BlockSummary) : Prop :=
  ∀ block ∈ blocks, block.Valid

def BlockListFitsAtomCap (blocks : List BlockSummary) (cap : ℕ) : Prop :=
  ∀ block ∈ blocks, block.FitsAtomCap cap

theorem atomize_sum_eq_totalBlockUnits {blocks : List BlockSummary}
    (hvalid : ValidBlockList blocks) :
    (atomize blocks).sum = totalBlockUnits blocks := by
  induction blocks with
  | nil => simp [atomize, totalBlockUnits]
  | cons block blocks ih =>
      have hblock := hvalid block (by simp)
      have htail : ValidBlockList blocks := by
        intro tail hmem
        exact hvalid tail (by simp [hmem])
      change (block.atoms ++ atomize blocks).sum =
        block.units + totalBlockUnits blocks
      rw [List.sum_append, BlockSummary.atoms_sum_eq_units block hblock, ih htail]

theorem atomize_edge_sum_eq_totalBlockEdges {blocks : List BlockSummary}
    (hvalid : ValidBlockList blocks) :
    ((atomize blocks).map cliqueEdges).sum = totalBlockEdges blocks := by
  induction blocks with
  | nil => simp [atomize, totalBlockEdges]
  | cons block blocks ih =>
      have hblock := hvalid block (by simp)
      have htail : ValidBlockList blocks := by
        intro tail hmem
        exact hvalid tail (by simp [hmem])
      change ((block.atoms ++ atomize blocks).map cliqueEdges).sum =
        block.edges + totalBlockEdges blocks
      rw [List.map_append, List.sum_append,
        BlockSummary.atoms_edge_sum_eq_edges block hblock, ih htail]

theorem atomize_positive {blocks : List BlockSummary}
    (hvalid : ValidBlockList blocks) :
    ∀ u ∈ atomize blocks, 0 < u := by
  intro u hu
  rw [atomize, List.mem_flatMap] at hu
  obtain ⟨block, hblock, hu⟩ := hu
  exact block.atom_positive (hvalid block hblock) hu

theorem atomize_le_cap {blocks : List BlockSummary} {cap : ℕ}
    (hcap : BlockListFitsAtomCap blocks cap) :
    ∀ u ∈ atomize blocks, u ≤ cap := by
  intro u hu
  rw [atomize, List.mem_flatMap] at hu
  obtain ⟨block, hblock, hu⟩ := hu
  exact block.atom_le_cap (hcap block hblock) hu

/-- Large atoms in the flattened packing correspond exactly to clique block
summaries of the same increment. -/
theorem large_mem_atomize_iff {blocks : List BlockSummary} {k : ℕ}
    (hk : 2 < k) :
    k ∈ atomize blocks ↔ BlockSummary.clique k ∈ blocks := by
  rw [atomize, List.mem_flatMap]
  constructor
  · rintro ⟨block, hblock, hkblock⟩
    exact (block.large_mem_atoms_iff hk).mp hkblock ▸ hblock
  · intro hblock
    exact ⟨.clique k, hblock, (BlockSummary.large_mem_atoms_iff hk _).mpr rfl⟩

/-- Atomization also preserves the multiplicity of every atom larger than
two: such atoms count exactly the clique summaries of that increment. -/
theorem count_atomize_large (blocks : List BlockSummary) {k : ℕ}
    (hk : 2 < k) :
    (atomize blocks).count k = blocks.count (.clique k) := by
  induction blocks with
  | nil => simp [atomize]
  | cons block blocks ih =>
      cases block with
      | clique u =>
          change List.count k (u :: atomize blocks) =
            List.count (.clique k) (.clique u :: blocks)
          simp only [List.count_cons, ih, beq_iff_eq, BlockSummary.clique.injEq]
      | oddCycle u =>
          have hkTwo : k ≠ 2 := by omega
          have hkOne : k ≠ 1 := by omega
          change List.count k
              (2 :: (List.replicate (u - 2) 1 ++ atomize blocks)) =
            List.count (.clique k) (.oddCycle u :: blocks)
          simp [List.count_append, List.count_replicate, ih,
            Ne.symm hkTwo, Ne.symm hkOne]

/-- List form of the reusable Bellman theorem.  Indexing by `Fin` preserves
multiplicity and is discharged internally. -/
theorem sum_cliqueEdges_le_certificate_list
    (cert : CapacityCertificate) (cap maxBudget : ℕ)
    (hcert : cert.IsValid cap maxBudget)
    (atoms : List ℕ) (budget : ℕ)
    (hbudget : budget ≤ maxBudget)
    (hpos : ∀ u ∈ atoms, 0 < u)
    (hcap : ∀ u ∈ atoms, u ≤ cap)
    (hsum : atoms.sum ≤ budget) :
    (atoms.map cliqueEdges).sum ≤ cert.value budget := by
  have hfin := sum_cliqueEdges_le_certificate cert cap maxBudget hcert
    (Finset.univ : Finset (Fin atoms.length))
    (fun i ↦ atoms[i.1]) budget hbudget
    (by
      intro i _
      exact hpos atoms[i.1] (List.getElem_mem i.2))
    (by
      intro i _
      exact hcap atoms[i.1] (List.getElem_mem i.2))
    (by simpa using hsum)
  simpa using hfin

/-- List/multiplicity form of the height-2637 capacity kernel. -/
theorem capacity_of_count25_without24_list
    (atoms : List ℕ)
    (hpos : ∀ u ∈ atoms, 0 < u)
    (hmax : ∀ u ∈ atoms, u ≤ 25)
    (hsum : atoms.sum ≤ 50)
    (hcount25 : atoms.count 25 ≤ 1)
    (h25 : 25 ∈ atoms)
    (hno24 : 24 ∉ atoms) :
    (atoms.map cliqueEdges).sum ≤ 604 := by
  let tail := atoms.erase 25
  have hperm : atoms.Perm (25 :: tail) := by
    simpa [tail] using List.perm_cons_erase h25
  have hunitSplit : atoms.sum = 25 + tail.sum := hperm.sum_eq
  have htailSum : tail.sum ≤ 25 := by omega
  have htailPos : ∀ u ∈ tail, 0 < u := by
    intro u hu
    exact hpos u (List.mem_of_mem_erase hu)
  have hcountEq : atoms.count 25 = 1 := by
    have hcountPos : 0 < atoms.count 25 := List.count_pos_iff.mpr h25
    omega
  have hno25Tail : 25 ∉ tail := by
    rw [← List.count_eq_zero]
    simp [tail, hcountEq]
  have htailCap : ∀ u ∈ tail, u ≤ 23 := by
    intro u hu
    have huMax := hmax u (List.mem_of_mem_erase hu)
    have huNe25 : u ≠ 25 := by
      intro hEq
      exact hno25Tail (hEq ▸ hu)
    have huNe24 : u ≠ 24 := by
      intro hEq
      exact hno24 (hEq ▸ List.mem_of_mem_erase hu)
    omega
  have htailEdges := sum_cliqueEdges_le_certificate_list
    cap23 23 49 cap23_valid tail 25 (by norm_num)
    htailPos htailCap htailSum
  rw [cap23_value_25] at htailEdges
  have hedgeSplit : (atoms.map cliqueEdges).sum =
      cliqueEdges 25 + (tail.map cliqueEdges).sum :=
    (hperm.map cliqueEdges).sum_eq
  norm_num [cliqueEdges] at hedgeSplit
  omega

/-- Full height-2637 interval contradiction for lists, using count rather than
an index-level uniqueness predicate. -/
theorem no_spectrum_budget50_between_609_615_count25_list
    (atoms : List ℕ)
    (hpos : ∀ u ∈ atoms, 0 < u)
    (hmax : ∀ u ∈ atoms, u ≤ 25)
    (hsum : atoms.sum ≤ 50)
    (hcount25 : atoms.count 25 ≤ 1)
    (h25 : 25 ∈ atoms)
    (hedgeLow : 609 ≤ (atoms.map cliqueEdges).sum)
    (hedgeHigh : (atoms.map cliqueEdges).sum ≤ 615) : False := by
  by_cases h24 : 24 ∈ atoms
  · let tail25 := atoms.erase 25
    have hperm25 : atoms.Perm (25 :: tail25) := by
      simpa [tail25] using List.perm_cons_erase h25
    have h24Tail : 24 ∈ tail25 := by
      have hmem : 24 ∈ 25 :: tail25 := hperm25.mem_iff.mp h24
      simpa using hmem
    let tail24 := tail25.erase 24
    have hperm24 : tail25.Perm (24 :: tail24) := by
      simpa [tail24] using List.perm_cons_erase h24Tail
    have hedgeSplit25 : (atoms.map cliqueEdges).sum =
        cliqueEdges 25 + (tail25.map cliqueEdges).sum :=
      (hperm25.map cliqueEdges).sum_eq
    have hedgeSplit24 : (tail25.map cliqueEdges).sum =
        cliqueEdges 24 + (tail24.map cliqueEdges).sum :=
      (hperm24.map cliqueEdges).sum_eq
    norm_num [cliqueEdges] at hedgeSplit25 hedgeSplit24
    omega
  · have hcapacity := capacity_of_count25_without24_list
      atoms hpos hmax hsum hcount25 h25 h24
    omega

/-- A valid block-summary list is bounded directly by any Bellman
certificate.  This is the representation-neutral bridge from Gallai blocks
to the packing theorem. -/
theorem totalBlockEdges_le_certificate
    (cert : CapacityCertificate) (cap maxBudget : ℕ)
    (hcert : cert.IsValid cap maxBudget)
    (blocks : List BlockSummary) (budget : ℕ)
    (hbudget : budget ≤ maxBudget)
    (hvalid : ValidBlockList blocks)
    (hcap : BlockListFitsAtomCap blocks cap)
    (hsum : totalBlockUnits blocks ≤ budget) :
    totalBlockEdges blocks ≤ cert.value budget := by
  have hatomSum : (atomize blocks).sum ≤ budget := by
    rw [atomize_sum_eq_totalBlockUnits hvalid]
    exact hsum
  have hbound := sum_cliqueEdges_le_certificate_list cert cap maxBudget hcert
    (atomize blocks) budget hbudget (atomize_positive hvalid)
    (atomize_le_cap hcap) hatomSum
  rwa [atomize_edge_sum_eq_totalBlockEdges hvalid] at hbound

theorem spectrum_gap_budget49_list
    (atoms : List ℕ)
    (hpos : ∀ u ∈ atoms, 0 < u)
    (hmax : ∀ u ∈ atoms, u ≤ 25)
    (hsum : atoms.sum ≤ 49) :
    (atoms.map cliqueEdges).sum ≤ 581 ∨
      600 ≤ (atoms.map cliqueEdges).sum := by
  have hgap := spectrum_gap_budget49
    (Finset.univ : Finset (Fin atoms.length))
    (fun i ↦ atoms[i.1])
    (by
      intro i _
      exact hpos atoms[i.1] (List.getElem_mem i.2))
    (by
      intro i _
      exact hmax atoms[i.1] (List.getElem_mem i.2))
    (by simpa using hsum)
  simpa using hgap

theorem spectrum_gap_budget48_list
    (atoms : List ℕ)
    (hpos : ∀ u ∈ atoms, 0 < u)
    (hmax : ∀ u ∈ atoms, u ≤ 25)
    (hsum : atoms.sum ≤ 48) :
    (atoms.map cliqueEdges).sum ≤ 559 ∨
      576 ≤ (atoms.map cliqueEdges).sum := by
  have hgap := spectrum_gap_budget48
    (Finset.univ : Finset (Fin atoms.length))
    (fun i ↦ atoms[i.1])
    (by
      intro i _
      exact hpos atoms[i.1] (List.getElem_mem i.2))
    (by
      intro i _
      exact hmax atoms[i.1] (List.getElem_mem i.2))
    (by simpa using hsum)
  simpa using hgap

/-- The 50-low-vertex Gallai gap, now stated directly for valid block
summaries rather than already-atomized data. -/
theorem blockSpectrum_gap_budget49
    (blocks : List BlockSummary)
    (hvalid : ValidBlockList blocks)
    (hcap : BlockListFitsAtomCap blocks 25)
    (hsum : totalBlockUnits blocks ≤ 49) :
    totalBlockEdges blocks ≤ 581 ∨ 600 ≤ totalBlockEdges blocks := by
  have hatomSum : (atomize blocks).sum ≤ 49 := by
    rwa [atomize_sum_eq_totalBlockUnits hvalid]
  have hgap := spectrum_gap_budget49_list (atomize blocks)
    (atomize_positive hvalid) (atomize_le_cap hcap) hatomSum
  rwa [atomize_edge_sum_eq_totalBlockEdges hvalid] at hgap

/-- The 49-low-vertex Gallai gap, stated directly for valid block summaries. -/
theorem blockSpectrum_gap_budget48
    (blocks : List BlockSummary)
    (hvalid : ValidBlockList blocks)
    (hcap : BlockListFitsAtomCap blocks 25)
    (hsum : totalBlockUnits blocks ≤ 48) :
    totalBlockEdges blocks ≤ 559 ∨ 576 ≤ totalBlockEdges blocks := by
  have hatomSum : (atomize blocks).sum ≤ 48 := by
    rwa [atomize_sum_eq_totalBlockUnits hvalid]
  have hgap := spectrum_gap_budget48_list (atomize blocks)
    (atomize_positive hvalid) (atomize_le_cap hcap) hatomSum
  rwa [atomize_edge_sum_eq_totalBlockEdges hvalid] at hgap

/-- The exact height-2637 contradiction stated at the block-summary boundary.
Uniqueness of K26 is expressed as a list multiplicity bound, and atomization
proves that the same multiplicity is seen by the packing kernel. -/
theorem no_blockSpectrum_budget50_between_609_615
    (blocks : List BlockSummary)
    (hvalid : ValidBlockList blocks)
    (hcap : BlockListFitsAtomCap blocks 25)
    (hsum : totalBlockUnits blocks ≤ 50)
    (hcount25 : blocks.count (.clique 25) ≤ 1)
    (h25 : BlockSummary.clique 25 ∈ blocks)
    (hedgeLow : 609 ≤ totalBlockEdges blocks)
    (hedgeHigh : totalBlockEdges blocks ≤ 615) : False := by
  have hatomSum : (atomize blocks).sum ≤ 50 := by
    rwa [atomize_sum_eq_totalBlockUnits hvalid]
  have hatomCount : (atomize blocks).count 25 ≤ 1 := by
    rwa [count_atomize_large blocks (by norm_num : 2 < 25)]
  have hatom25 : 25 ∈ atomize blocks :=
    (large_mem_atomize_iff (by norm_num : 2 < 25)).mpr h25
  have hatomEdgeLow : 609 ≤ ((atomize blocks).map cliqueEdges).sum := by
    rwa [atomize_edge_sum_eq_totalBlockEdges hvalid]
  have hatomEdgeHigh : ((atomize blocks).map cliqueEdges).sum ≤ 615 := by
    rwa [atomize_edge_sum_eq_totalBlockEdges hvalid]
  exact no_spectrum_budget50_between_609_615_count25_list
    (atomize blocks) (atomize_positive hvalid) (atomize_le_cap hcap)
    hatomSum hatomCount hatom25 hatomEdgeLow hatomEdgeHigh

theorem no_blockSpectrum_budget49_between_582_591
    (blocks : List BlockSummary)
    (hvalid : ValidBlockList blocks)
    (hcap : BlockListFitsAtomCap blocks 25)
    (hsum : totalBlockUnits blocks ≤ 49)
    (hedgeLow : 582 ≤ totalBlockEdges blocks)
    (hedgeHigh : totalBlockEdges blocks ≤ 591) : False := by
  rcases blockSpectrum_gap_budget49 blocks hvalid hcap hsum with hlow | hhigh
  · omega
  · omega

theorem no_blockSpectrum_budget48_between_560_569
    (blocks : List BlockSummary)
    (hvalid : ValidBlockList blocks)
    (hcap : BlockListFitsAtomCap blocks 25)
    (hsum : totalBlockUnits blocks ≤ 48)
    (hedgeLow : 560 ≤ totalBlockEdges blocks)
    (hedgeHigh : totalBlockEdges blocks ≤ 569) : False := by
  rcases blockSpectrum_gap_budget48 blocks hvalid hcap hsum with hlow | hhigh
  · omega
  · omega

end AlbertsonGallaiBlockSpectrum

#print axioms AlbertsonGallaiBlockSpectrum.BlockSummary.atoms_sum_eq_units
#print axioms AlbertsonGallaiBlockSpectrum.BlockSummary.atoms_edge_sum_eq_edges
#print axioms AlbertsonGallaiBlockSpectrum.large_mem_atomize_iff
#print axioms AlbertsonGallaiBlockSpectrum.count_atomize_large
#print axioms AlbertsonGallaiBlockSpectrum.totalBlockEdges_le_certificate
#print axioms AlbertsonGallaiBlockSpectrum.blockSpectrum_gap_budget49
#print axioms AlbertsonGallaiBlockSpectrum.blockSpectrum_gap_budget48
#print axioms AlbertsonGallaiBlockSpectrum.no_blockSpectrum_budget50_between_609_615
#print axioms AlbertsonGallaiBlockSpectrum.no_blockSpectrum_budget49_between_582_591
#print axioms AlbertsonGallaiBlockSpectrum.no_blockSpectrum_budget48_between_560_569
