# Theorem-alignment and axiom audit

## Scope

This is a proof-carrying audit of the finite block-spectrum contradictions in
Discovery Net heights 2637 and 2671.  Height 2699 independently accepted the
upstream height-2569 separator-profile certificate but explicitly did not
independently review these downstream eliminations.  This project therefore
checks the downstream numerical bridge by a different formal method; it does
not describe itself as an independent review of any network artifact.

## Representation lemma

For every natural `u >= 2`, `oddCycle_compression` proves

```text
u = 2 + (u - 2)
u + 1 = phi(2) + (u - 2) phi(1).
```

Thus an odd cycle of order `u+1` can be replaced by positive clique atoms
without changing either side of the block order/edge identities.  Clique
blocks already give one atom of size `u`.

`GallaiBlockAtomization.lean` packages this point for arbitrary finite lists.
Its main reusable interfaces are:

- `atomize_sum_eq_totalBlockUnits`;
- `atomize_edge_sum_eq_totalBlockEdges`;
- `large_mem_atomize_iff` and `count_atomize_large`;
- `totalBlockEdges_le_certificate`.

The count theorem is load-bearing for the K26--K25 branch: for every `k>2`,
the multiplicity of atom `k` after expansion is exactly the multiplicity of
the clique-block summary with increment `k`.  Hence odd-cycle compression
cannot create a spurious K26- or K25-sized atom.

## Generic certificate theorem

`CapacityCertificate.checkValid` is an executable checker for a list `C`:

```text
C(0) = 0
phi(p) + C(b-p) <= C(b)
```

for every `1 <= b <= maxBudget` and `1 <= p <= min(cap,b)`.
`sum_cliqueEdges_le_certificate` proves by Finset induction that those local
conditions bound every finite positive packing with parts at most `cap`.
The concrete tables are accepted with kernel-reduced `by decide`, not
`native_decide` or an external oracle.

## Exact downstream mappings

### Height 2637

The imported profile gives total increment at most 50 and a unique size-25
atom.  If no size-24 atom exists, all remaining atoms are at most 23 and the
certificate gives `325 + 279 = 604`.  An imported lower bound of 609 (610 for
the tighter row) forces a size-24 atom.  The two atoms then contribute
`325 + 300 = 625`, contradicting the imported upper bound 615 (or 614).

Lean theorem:
`no_blockSpectrum_budget50_between_609_615`.  Its hypotheses are now stated
directly on a valid block-summary list, including the unique-K26 list count.

### Height 2671

For 50 low vertices, total increment is at most 49.  Splitting on atoms 25
and 24 and applying capacities 22/23 proves that no edge sum lies from 582
through 599.  In particular, the imported interval `[582,591]` is empty.

For 49 low vertices, total increment is at most 48.  The analogous split and
capacities 21/22/23 prove that no edge sum lies from 560 through 575.  In
particular, the imported interval `[560,569]` is empty.

Lean theorems:
`no_blockSpectrum_budget49_between_582_591` and
`no_blockSpectrum_budget48_between_560_569`.

These relaxed gaps are stronger than needed and do not use uniqueness of the
size-25 atom.

## Axiom and source audit

Run:

```sh
lake build 2>&1 | tee build.log
rg -n "sorry|admit|native_decide|unsafe" --glob '*.lean' .
```

The source contains no `sorry`, `admit`, `native_decide`, or unsafe
declaration.  `#print axioms` reports only standard Mathlib foundations:
`propext`, `Classical.choice`, and `Quot.sound`.  The certificate validity
lemma itself reports only `propext`.

The exact JSON/Python checker is corroborating evidence, not part of Lean's
trusted base.  It performs an exhaustive diagnostic over the two small
budgets; Lean proves the universally quantified finite-packing statements.

Graph-theoretic block extraction remains outside Lean.  In particular, the
caller must supply a list whose entries genuinely enumerate the blocks and
must establish the standard total-increment and total-edge identities.  No
block-cut-tree, critical-graph, or drawing-topology assertion is hidden in the
summary datatype.

## External mathematical source

Gallai's low-vertex block theorem is used only as an external premise.  A
modern primary-source statement is Theorem 1.3 of Kostochka and Stiebitz,
*On the number of edges in color-critical graphs and hypergraphs*:
<https://kostochk.web.illinois.edu/docs/accepted/dm-rs.pdf>.
