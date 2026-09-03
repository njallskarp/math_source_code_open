## Scope and theorem

This Lean 4 formalization closes the common-neighbor bridge used at the only
delicate endpoint of the direct equality-case proof for odd Kneser graphs.
Let `α` be finite with `|α| = 2k+1`, and let `A,B` be distinct `k`-subsets.
If a `k`-subset `C` is disjoint from both, Lean proves

`C = (A ∪ B)ᶜ` and `|(A ∪ B)| = k+1`.

Consequently any two common disjoint `k`-sets are equal. With
`KneserVertex α k := {A : Finset α // A.card = k}` and adjacency defined
literally by `Disjoint`, the exported theorem `oddKneser_no_K22` proves that
four cross-adjacencies between distinct pairs `A ≠ B` and `C ≠ D` imply
`False`. Thus `KG(2k+1,k)` has no `K₂,₂`. This is exactly the obstruction used
in the target refinement: equality in the Mantel bound at `|X|=2k` would
force `G[X] ≅ K_{k,k}`, which contains a `K₂,₂` for `k≥2`.

## Exported Lean results

- `common_disjoint_kset_eq_compl`
- `common_disjoint_kset_union_card`
- `common_disjoint_kset_unique`
- `oddKneser_commonNeighbor_unique`
- `oddKneser_no_K22`

The set-level statements are slightly stronger than needed: they do not
assume `k≥2`.

## Reproducibility and audit

Source is in `research/kneser_endpoint/` of the researcher-4 local working
tree. The project pins Lean 4.33.1 and Mathlib tag v4.33.1, resolved to
Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`. From that directory the
verified clean sequence is `lake update`, `lake clean`, `lake exe cache get`,
and `lake build`. The build completed all 8707 jobs successfully.

`#print axioms` reports exactly `[propext, Classical.choice, Quot.sound]` for
each exported theorem. The Lean source contains no `sorry`, `admit`, custom
axiom, `unsafe`, or `native_decide`; no generated data, external computation,
certificate, oracle, or nonstandard kernel/plugin is used.

The parent repository commit could not be created because this workspace's
`.git` metadata is mounted read-only (`index.lock: Operation not permitted`);
the source and manifest are therefore present in the local working tree but
not yet bound to a commit.

## Alignment and trust boundary

The definitions use Mathlib `Finset` cardinality and `Disjoint` directly, so
there is no custom-encoding equivalence bridge. Lean proves the finite-set
classification and no-`K₂,₂` result only. It does not formalize the Kneser
spectrum, Rayleigh inequality, Mantel's theorem/equality case, or the
scramble-to-restricted-cut translation, and it therefore does not claim a
formal proof of the full super-`λ₂` theorem.

Primary-status check: Ballinas--Caine--Hopkins--Rivera Laboy,
arXiv:2609.00258v1 (https://arxiv.org/abs/2609.00258), poses the
uniform-edge-scramble direction (the relevant item is Conjecture 5.3); Wang,
Discrete Mathematics 289 (2004)
(https://doi.org/10.1016/j.disc.2004.08.011), gives the vertex-transitive
degree/girth precedent; Balbuena--Marcote, Applied Mathematics and Computation
343 (2019) (https://doi.org/10.1016/j.amc.2018.09.072), treats restricted
connectivity for Kneser graphs. No novelty claim is made for the combinatorial
fact; the new artifact is the aligned reusable kernel-checked formalization.
