# Theorem alignment and trust audit

## Checked objects

All declarations are in namespace `AlbertsonNeighborhoodObstruction`.

| Declaration | Exact role |
|---|---|
| `foldHom` | Native homomorphism G → G-a under a≠w and N(a)⊆N(w). |
| `chromaticNumber_delete_eq_of_neighborSet_subset` | Native chromatic-number equality via homomorphisms in both directions. |
| `not_neighborSet_subset_of_chromatic_drop` | Strict drop at a rules out the inclusion. |
| `neighborSet_subset_of_compl_domination` | Actual complement adjacency translates domination to neighborhood inclusion. |
| `exists_compl_neighbor_not_adjacent` | Explicit complement non-domination witness under strict drop at a. |
| `not_isClique_of_neighborSet_subset` | A nonempty complement neighborhood cannot be contained in a clique when every deletion drops χ. |

No finite vertex-order, fixed r, palette, matching, Stehlik theorem, or special
class-size hypothesis appears in these declarations. They use native Mathlib
definitions. The graph G-a is exactly `G.induce {x | x ≠ a}`.

The universal criticality premise in the last theorem is written explicitly
as strict chromatic drop at every vertex; there is no custom critical-graph
axiom. The witness theorem only requires the drop at the named vertex a.

## Boundary checks

* Distinctness a≠w is essential for a fold onto a surviving vertex and is an
  explicit premise of `foldHom`. In the complement witness it follows from
  the assumed complement edge wa.
* Adjacent original vertices cannot have the stated open-neighborhood
  inclusion: it would put w into its own open neighborhood. No missing
  nonadjacency premise is hidden in the constructor.
* The clique-barrier theorem requires a nonempty neighborhood. This must not
  be dropped: complete graphs are vertex-critical and their complements have
  isolated vertices. This boundary example is explanatory prose, not an extra
  formally instantiated test graph.
* Finiteness is not necessary: Mathlib's chromatic number lies in ℕ∞ and
  graph-homomorphism monotonicity applies directly. Strict drop remains an
  explicit hypothesis, not a conclusion about arbitrary infinite graphs.
* The complement-domination translation uses actual adjacency, not free
  degree values or asserted component summaries.

## Verification

Pinned Lean 4.33.1 / Lake 5.0.0-src+819816b, Mathlib revision
`0df444a360eaa60ab8c11dca51a86af692955474`.

Commands:

    lake build
    lake env lean Audit.lean

Workspace and fresh isolated publication-directory builds passed without
project warnings: 1004 jobs each; the project module was recompiled in the
fresh directory. All five theorems and the constructor have been audited in
both locations; each depends exactly on `propext`, `Classical.choice`, and
`Quot.sound`. Only pinned own-workspace dependency caches were reused.

Trust comprises Lean's kernel, those standard axioms, pinned Mathlib proofs,
and the ordinary toolchain. No external data or certificate is consumed and
no unsafe reduction, sorry, admit, custom axiom, or native_decide is used.
The proof is classical; it is not an executable coloring optimizer.

## Scope

The local non-domination bridge at height 2933 is kernel-checked with weaker
hypotheses. Neither that artifact's entire alpha>=4 elimination nor any other
campaign result is independently reviewed here. In particular its remaining
two-singleton, separator-enumeration, Gallai, and crossing dependencies are
not imported into this Lean source or silently certified by it.
