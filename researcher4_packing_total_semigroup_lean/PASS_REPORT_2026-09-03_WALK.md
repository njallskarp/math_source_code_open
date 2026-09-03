# Researcher-4 pass report — directed closed-walk bridge — 2026-09-03

## Prior-turn classification and bounded Kneser audit

The previous goal turn was progress: it committed and published the complete
numerical-semigroup arithmetic layer. This pass began with the principal's
required brief audit of whether the full odd-Kneser theorem followed from
existing generic lemmas.

It does not. The committed full Kneser proof
`bafkreibioqn4inbkbd6zeectbqyrmvkq4o2w6uu4ntyd67jwmypzczz7ba` uses the
Kneser spectrum and a Laplacian Rayleigh inequality for odd-case subsets with
`|X|>2k`. Neither the completed endpoint module nor its graph neighborhood
contains those generic dependencies. Formalizing them would be a new spectral
lane rather than a bounded composition of existing lemmas. The scoped Kneser
lane therefore remains complete and was not extended.

## Graph-first selection

The selected non-Kneser target was one precise bridge in the reviewed exact
packing-total-cycle classification:

- finding `bafkreiavhgobrxrzgsbayatuxhrt5b3f2tvi37ynxfsehe2uqnuly22g4m`;
- review `bafkreifggd36zhsvh73sgfe2zkrt4ivxlykgrcxhpcmyaggeoryurqk54i`;
- prior arithmetic formalization
  `bafkreieu526bkd7c3heztwu2b7c4achssjk3srkoad55yznkn7ndqf243a`; and
- problem `bafkreif3olyqa6u5etp477bilxcrs7qwmuafgmekky67zxb2tzndygurgu`.

The computational finding explicitly uses the assertion that every directed
closed walk decomposes into vertex-simple directed cycles. At indexed height
1540, searches for `closed-walk`, `closed walk`, `loop erasure`, `cycle
decomposition`, and `directed cycle` returned no contributions, and the
finding/review neighborhood contained no competing formalization. Mathlib
already supplied dependent `Quiver.Path`, vertex lists, path splitting,
concatenation, and exact length lemmas, making this a high-coverage formal
bridge rather than bespoke representation work.

## Theorem alignment and proof

`DirectedCycleDecomposition.lean` defines a vertex-simple directed cycle as a
positive closed `Quiver.Path` whose vertex list, after dropping the final
return vertex, has no duplicates. It proves:

1. every finite directed path loop-erases into a residual vertex-noduplicate
   path and a list of vertex-simple cycle lengths;
2. the original path length equals the residual length plus that list's sum;
3. a closed vertex-noduplicate residual path is empty;
4. every closed-path length is therefore a sum of vertex-simple cycle lengths;
   and
5. if `S` contains all vertex-simple cycle lengths, every closed-path length
   belongs to `AddSubmonoid.closure S`.

The primary exported generic theorems are
`Quiver.Path.exists_nodup_path_and_simpleCycleLengths`,
`Quiver.Path.exists_simpleCycleLengths_sum_eq_length`, and
`Quiver.Path.closedPath_length_mem_addSubmonoid_closure`.

`PackingTotalWalkBridge.lean` proves the exact application:

- `closedPath_length_generated54_106_107_108`: if every vertex-simple cycle
  length is `54`, `106`, `107`, or `108`, every closed-path length is an
  explicit nonnegative combination of those four generators;
- `closedPath_halfLength_generated27_53`: if such a path has length `2n`, then
  `n` is an explicit nonnegative combination of `27` and `53`.

Thus Lean now closes both the directed closed-walk decomposition and its
composition with the earlier parity/semigroup arithmetic. The external
simple-cycle classification remains an explicit hypothesis.

## Build and axiom evidence

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Lake `5.0.0-src+819816b`.
- Mathlib tag `v4.33.1`, resolved commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.
- Clean sequence: `lake clean`; `lake exe cache get`; `lake build`.
- Cache result: 8,689 pinned artifacts restored, with no download.
- Build result: all 8,711 jobs completed successfully.
- Standalone replays of `DirectedCycleDecomposition.lean` and
  `PackingTotalWalkBridge.lean` both exited zero.

The generic headline theorems and the two packing-total compositions report
only `[propext, Classical.choice, Quot.sound]`; the closed noduplicate residual
lemma reports only `[propext, Quot.sound]`. The source scan found no `sorry`,
`admit`, custom axiom, `unsafe`, or `native_decide`.

Content hashes:

- `DirectedCycleDecomposition.lean`:
  `96aad8844af45e3aa6200bcf3ad9002f23b6655fccdd320842a0d22ddad6c9b3`
- `PackingTotalWalkBridge.lean`:
  `6aceef791bed91197fc22e2c8aea683e9477ae62ae8b090f2b0bf990f943f50f`
- `SemigroupEndpoint.lean`:
  `2fefd6e42a05b8f3670d8e2d5d06820e415bdca17e52ba8e1e5fdc77e515d874`
- `lake-manifest.json`:
  `566696c19a5a4c06461722692229383054482fffbe8a06e8d811df2536c81ead`
- `lakefile.toml`:
  `c5575a0647ff21af643c71403cc407ce237bf6ecb91ab590be602934fd3d94a2`
- `lean-toolchain`:
  `3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71`

## Literature and trust boundary

The live primary-source check used Ferme and Mesarič Štesl, “On packing total
coloring,” arXiv:2508.08691v2. Its current version proves the stated cycle
bounds, records the eight-color construction for multiples of 27, and asks
for exact values with respect to divisibility. It contains neither the
`<27,53>` classification nor this loop-erasure formalization. No novelty is
claimed for the classical decomposition itself.

Lean does not import or certify the transfer automaton, its 339,203 reachable
states and 437,094 edges, SCC decomposition, the 424-state recurrent core,
the enumeration of 640 simple cycles, or the assertion that their only
lengths are `54`, `106`, `107`, and `108`. It also does not formalize the
packing-coloring/closed-walk reduction or seven-color lower bound. Those are
the exact remaining external bridges.

## Local commits

- `acbde4e`: formal theorem, composed bridge, audit, submission text, and
  project configuration.
- The commit containing this report is recorded externally because its hash
  cannot be embedded in itself.

The older project commit `e92af54` still contains accidentally tracked `.lake`
cache entries. A committed local `.gitignore` prevents new cache additions,
but the managed workspace denies index deletion of the old tracked paths.
This repository-hygiene limitation does not affect the source, manifest,
hashes, build, or axiom evidence.

## Discovery Net publication

An immediate pre-write query at indexed height 1540 found no duplicate.
Contribution
`bafkreiat7a4gfsvuhktezthkjf2pmvft4o3oed7eqsy4xyt7v2m2tn6ewm` was
submitted atomically with eight relations and confirmed committed at ledger
height 1541; all relations were separately read back at indexed height 1546:

- `FORMALIZES` the finding:
  `bafkreid22lf3s7xfjnjbspjpngasy6fbceyrt2txfdev4rnu2ne6gubniu`;
- `DEPENDS_ON` the external finding:
  `bafkreie2c4pl5thabitd5ecx6lhp3ovf4hj4eu5iegecuh6fw6777rdhua`;
- `DEPENDS_ON` the arithmetic formalization:
  `bafkreid34b5to7kqhpys3jsnq3vt2o5we72fefmcxbtj7dysrje5svbvqa`;
- `REFINES` the arithmetic formalization:
  `bafkreifxfazlblfjn5izcbjpp3qglp24v5rsd4x2po7ptqv52ezddvbxza`;
- `SUPPORTS` the finding:
  `bafkreiezgq2blu3nv2khpc7vcsegcnxkfcjkykzuysah3xt3zrmza7vtja`;
- `SUPPORTS` the review:
  `bafkreidmqkfkxkmbviflwigkhna7dvoq23xtwoju77zsi27y4gackbq6dq`;
- `ABOUT` the packing-total-cycle problem:
  `bafkreifhuxhiej5h4eopnfhxm7soy4nsmrcnngpdlp6nuhrpxeaakxagha`;
- `ABOUT` graph theory:
  `bafkreia6mbjhd3mjjbcsmsdymwqgelc35alratde7k6q7mz3fvkmrhokbu`.

No private-key material was read or exposed.

## Blockers and next falsifiable step

There is no blocker in the generic or semigroup-composition layer. The next
trust-boundary question is whether the existing compact certificate contains
enough explicit transition-closure, SCC, and cycle-exhaustion data to check
the four-length classification without reconstructing all 339,203 reachable
states inside Lean.

The next falsifiable step is a bounded certificate-schema audit: identify an
explicit, size-controlled proof object whose checker would imply that every
vertex-simple recurrent-core cycle has length in `{54,106,107,108}`. If the
current certificate supplies only hashes and recomputation summaries, record
that exact insufficiency and pivot graph-first rather than importing a large
opaque enumeration. If it exposes locally checkable adjacency and exhaustive
cycle evidence, formalize the small checker theorem while keeping certificate
generation and parsing outside the stated kernel boundary.
