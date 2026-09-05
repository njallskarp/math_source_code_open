import Mathlib.Combinatorics.SimpleGraph.Matching

/-!
# A conformal-triangle separator lemma

This file isolates the graph-theoretic matching bridge used in the Albertson
counterexample analysis.  Drawings, crossing numbers, criticality, and the
theorem that produces factor-critical complements remain outside this file.
-/

open Set

namespace AlbertsonConformalSeparator

variable {V : Type*} {H : SimpleGraph V}

/-- `H` has a matching saturating every vertex except `a`.  The matching is
represented by Mathlib's native matching subgraph. -/
def HasNearPerfectMatchingAt (H : SimpleGraph V) (a : V) : Prop :=
  ∃ M : H.Subgraph, M.verts = ({a} : Set V)ᶜ ∧ M.IsMatching

/-- Explicit matching interface for factor-criticality. -/
def IsFactorCritical (H : SimpleGraph V) : Prop :=
  ∀ a, HasNearPerfectMatchingAt H a

/-- `H` has a matching saturating exactly the vertices outside `a`, `b`, and
`c`. -/
def HasPerfectMatchingOffThree (H : SimpleGraph V) (a b c : V) : Prop :=
  ∃ M : H.Subgraph, M.verts = ({a, b, c} : Set V)ᶜ ∧ M.IsMatching

/-- A triangle whose complementary vertex set has a perfect matching. -/
def IsConformalTriangleAt (H : SimpleGraph V) (a b c : V) : Prop :=
  H.Adj a b ∧ H.Adj a c ∧ H.Adj b c ∧ HasPerfectMatchingOffThree H a b c

/-- A graph contains no conformal triangle. -/
def HasNoConformalTriangle (H : SimpleGraph V) : Prop :=
  ∀ a b c, ¬ IsConformalTriangleAt H a b c

/-- If `x-y` is an edge of a matching, deleting `x` and `y` leaves a matching.
This is the reusable Mathlib-native matching restriction lemma needed below. -/
theorem matching_deletePairOfAdj
    {M : H.Subgraph} (hM : M.IsMatching) {x y : V} (hxy : M.Adj x y) :
    (M.deleteVerts ({x, y} : Set V)).IsMatching := by
  intro v hv
  rw [SimpleGraph.Subgraph.deleteVerts_verts] at hv
  obtain ⟨u, huv, huniq⟩ := hM hv.1
  have hux : u ≠ x := by
    intro h
    subst u
    have hvy : v = y := (hM.eq_of_adj_left hxy huv.symm).symm
    exact hv.2 (by simp [hvy])
  have huy : u ≠ y := by
    intro h
    subst u
    have hvx : v = x := (hM.eq_of_adj_left hxy.symm huv.symm).symm
    exact hv.2 (by simp [hvx])
  refine ⟨u, ?_, ?_⟩
  · exact SimpleGraph.Subgraph.deleteVerts_adj.mpr
      ⟨hv.1, hv.2, huv.snd_mem, by simp [hux, huy], huv⟩
  · intro z hz
    exact huniq z ((SimpleGraph.Subgraph.deleteVerts_le
      (G' := M) (s := ({x, y} : Set V))).2 hz)

/-- Restricting a near-perfect matching off `a` by deleting one matched edge
`w-d` gives a perfect matching off the three vertices `a,w,d`. -/
theorem matchingOffThree_of_matchingOffOne_of_adj
    {M : H.Subgraph} {a w d : V}
    (hverts : M.verts = ({a} : Set V)ᶜ) (hM : M.IsMatching)
    (hwd : M.Adj w d) :
    HasPerfectMatchingOffThree H a w d := by
  refine ⟨M.deleteVerts ({w, d} : Set V), ?_,
    matching_deletePairOfAdj hM hwd⟩
  rw [SimpleGraph.Subgraph.deleteVerts_verts, hverts]
  ext v
  simp only [mem_sdiff, mem_compl_iff, mem_singleton_iff, mem_insert_iff]
  tauto

/-- A factor-critical graph gives every vertex a neighbor, provided there is
another vertex available to delete. -/
theorem IsFactorCritical.exists_adj
    (hfc : IsFactorCritical H) {t w : V} (htw : t ≠ w) :
    ∃ a, H.Adj w a := by
  obtain ⟨M, hverts, hM⟩ := hfc t
  have hw : w ∈ M.verts := by
    rw [hverts]
    simpa using htw.symm
  obtain ⟨a, hwa, -⟩ := hM hw
  exact ⟨a, hwa.adj_sub⟩

/-- If a factor-critical graph has a triangle `a-b-c` separating the singleton
vertex `w`, then it contains a conformal triangle.  The separator hypothesis is
stated pointwise: every neighbor of `w` lies in `{a,b,c}`. -/
theorem conformalTriangle_of_singleton_triangle_separator
    (hfc : IsFactorCritical H)
    {a b c w : V}
    (hab : H.Adj a b) (hac : H.Adj a c) (hbc : H.Adj b c)
    (hwa : w ≠ a) (hwb : w ≠ b) (hwc : w ≠ c)
    (hsep : ∀ d, H.Adj w d → d = a ∨ d = b ∨ d = c) :
    ∃ x y z, IsConformalTriangleAt H x y z := by
  obtain ⟨x, hwx⟩ := IsFactorCritical.exists_adj hfc (t := a) (w := w) hwa.symm
  rcases hsep x hwx with hx | hx | hx
  · subst x
    obtain ⟨M, hverts, hM⟩ := hfc a
    have hwM : w ∈ M.verts := by
      rw [hverts]
      simpa using hwa
    obtain ⟨d, hwd, -⟩ := hM hwM
    have hHd : H.Adj w d := hwd.adj_sub
    rcases hsep d hHd with hd | hd | hd
    · subst d
      have haM := hwd.snd_mem
      rw [hverts] at haM
      simp at haM
    · subst d
      exact ⟨a, w, b, hwx.symm, hab, hwd.adj_sub,
        matchingOffThree_of_matchingOffOne_of_adj hverts hM hwd⟩
    · subst d
      exact ⟨a, w, c, hwx.symm, hac, hwd.adj_sub,
        matchingOffThree_of_matchingOffOne_of_adj hverts hM hwd⟩
  · subst x
    obtain ⟨M, hverts, hM⟩ := hfc b
    have hwM : w ∈ M.verts := by
      rw [hverts]
      simpa using hwb
    obtain ⟨d, hwd, -⟩ := hM hwM
    have hHd : H.Adj w d := hwd.adj_sub
    rcases hsep d hHd with hd | hd | hd
    · subst d
      exact ⟨b, w, a, hwx.symm, hab.symm, hwd.adj_sub,
        matchingOffThree_of_matchingOffOne_of_adj hverts hM hwd⟩
    · subst d
      have hbM := hwd.snd_mem
      rw [hverts] at hbM
      simp at hbM
    · subst d
      exact ⟨b, w, c, hwx.symm, hbc, hwd.adj_sub,
        matchingOffThree_of_matchingOffOne_of_adj hverts hM hwd⟩
  · subst x
    obtain ⟨M, hverts, hM⟩ := hfc c
    have hwM : w ∈ M.verts := by
      rw [hverts]
      simpa using hwc
    obtain ⟨d, hwd, -⟩ := hM hwM
    have hHd : H.Adj w d := hwd.adj_sub
    rcases hsep d hHd with hd | hd | hd
    · subst d
      exact ⟨c, w, a, hwx.symm, hac.symm, hwd.adj_sub,
        matchingOffThree_of_matchingOffOne_of_adj hverts hM hwd⟩
    · subst d
      exact ⟨c, w, b, hwx.symm, hbc.symm, hwd.adj_sub,
        matchingOffThree_of_matchingOffOne_of_adj hverts hM hwd⟩
    · subst d
      have hcM := hwd.snd_mem
      rw [hverts] at hcM
      simp at hcM

/-- Hence a factor-critical graph with no conformal triangle has no triangle
separator whose removal leaves a singleton component. -/
theorem no_singleton_triangle_separator
    (hfc : IsFactorCritical H) (hnct : HasNoConformalTriangle H)
    {a b c w : V}
    (hab : H.Adj a b) (hac : H.Adj a c) (hbc : H.Adj b c)
    (hwa : w ≠ a) (hwb : w ≠ b) (hwc : w ≠ c) :
    ¬(∀ d, H.Adj w d → d = a ∨ d = b ∨ d = c) := by
  intro hsep
  obtain ⟨x, y, z, hxyz⟩ := conformalTriangle_of_singleton_triangle_separator
    hfc hab hac hbc hwa hwb hwc hsep
  exact hnct x y z hxyz

end AlbertsonConformalSeparator

#print axioms AlbertsonConformalSeparator.matching_deletePairOfAdj
#print axioms AlbertsonConformalSeparator.matchingOffThree_of_matchingOffOne_of_adj
#print axioms AlbertsonConformalSeparator.IsFactorCritical.exists_adj
#print axioms AlbertsonConformalSeparator.conformalTriangle_of_singleton_triangle_separator
#print axioms AlbertsonConformalSeparator.no_singleton_triangle_separator
