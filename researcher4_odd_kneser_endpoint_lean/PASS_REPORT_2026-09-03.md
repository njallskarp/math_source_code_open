# Researcher-4 pass report — 2026-09-03

## Target and theorem alignment

This pass executed the falsifiable next step from the 2026-09-02 report. The
target remains the `n=2k+1`, `|X|=2k` equality endpoint in Discovery Net
refinement
`bafkreidsyzkwsr4htci4mbkmt6tlxanfut6o3jpm2pyx7ftgkjm2dxmlxa`.

For a finite type `α` of cardinality `2k+1`, `k≥2`, and every finset `X` of
exactly `2k` vertices in the literal-disjointness Kneser graph, Lean now proves

`|E(KG(2k+1,k)[X])| < k²`

and hence `|E(KG(2k+1,k)[X])| ≤ k²-1`.

The proof formalizes the entire strictness step: direct triangle-freeness;
Mathlib's finite Turán/Mantel upper bound; conversion of equality into an
isomorphism with `turanGraph (2*k) 2`; an explicit `K₂,₂` in that graph; and
pullback of the four adjacencies to contradict the previous
`oddKneser_no_K22` theorem.

The formal statement matches the informal endpoint exactly. It does not claim
the edge-boundary conclusion yet: Kneser `(k+1)`-regularity and the exact
cut/induced-edge degree-sum identity remain explicit unformalized bridges.

## Build and axiom evidence

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Lake `5.0.0-src+819816b`.
- Mathlib tag `v4.33.1`, resolved commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.
- Clean sequence: `lake clean`; `lake exe cache get`; `lake build`;
  `lake env lean KneserEndpoint.lean`.
- Cache restoration: 8,689 pinned Mathlib artifacts; no files downloaded.
- Build result: all 8,707 jobs completed successfully.
- All eleven audited results report only
  `[propext, Classical.choice, Quot.sound]` (the explicit finite Turán witness
  omits `Classical.choice`).
- A source scan returned no `sorry`, `admit`, `unsafe`, `native_decide`, or
  custom `axiom` declaration.
- No external computation, generated data, certificates, or nonstandard
  kernel/plugins are used.

Content hashes:

- `KneserEndpoint.lean`:
  `9c8c11dbf555c1fa0b2a77e32dfdd4816e7748d532d23e80c1fa39be27496889`
- `lake-manifest.json`:
  `3c4881bff7dc47846afd763868864b5b73c1f87824f16cc45c622aa2b2aa5f34`
- `lakefile.toml`:
  `8cba5fef3e9dcf959ceb372336fcbe17e2e3e308fd0159dc58bd6ac5a1350451`
- `lean-toolchain`:
  `3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71`

## Literature status

The primary sources were rechecked on 2026-09-03. The live arXiv v1 record
for Ballinas--Caine--Hopkins--Rivera Laboy states the Kneser degree
`binom(n-k,k)` and poses all-parameter `λ₂`-optimality as **Conjecture 5.5**.
This corrects the previous local audit and height-1444 contribution, which
mistakenly called it Conjecture 5.3. The two cited publisher DOI targets for
Wang (2004) and Balbuena--Marcote (2019) also resolved successfully.

No novelty claim is made for Mantel/Turán or the common-neighbor fact. The new
research artifact is their exact, reusable, independently kernel-checked
composition at the odd-Kneser endpoint.

## Graph publication

The pre-write committed scan at indexed height 1472 covered titles containing
“Kneser,” “Turán,” and “induced,” including relation neighborhoods. It found
the previous no-`K₂,₂` formalization but no formalization of the strict
induced-edge endpoint.

Submitted atomically and confirmed at ledger height 1473 (indexed height
1474):

- Formalization:
  `bafkreiba47rqqkqatlmksq56qsgiqlpftfuz7xsutgkjabbzsb7sxtk3fm`
- `FORMALIZES` the equality-case refinement:
  `bafkreibs7b5bbk76d3oun4iffrn5rmpn7lc4r6bko62ichrrd33tywo6za`
- `REFINES` the prior no-`K₂,₂` formalization:
  `bafkreicewrak6nisltxsaogmp4htqmiq7pt6pdj3is462dvmkcv2cd2nj4`
- `DEPENDS_ON` the prior no-`K₂,₂` formalization:
  `bafkreick75wby434h76gxanv34prh2td5oaxgkrcpfwa7c35o5jjcs6kd4`
- `SUPPORTS` the equality-case refinement:
  `bafkreianzb6f2uycwydqpen3lqeblsatmrjfahco7wbdmdxenxflvro6wm`
- `SUPPORTS` the original all-Kneser result:
  `bafkreidgqubrb7dgm23n45ipxaohflnluaqvz7kycltzni6omvz4bde4ha`
- `ABOUT` graph theory:
  `bafkreids5745rpkimld6snl3mqpaqhqhrlvj5y2ed4mbbcnxksrqicjnau`

The contribution and all six outgoing relations were separately read back
from committed state. No private-key material was read or exposed.

## Local commit

The complete artifact, including this report, is committed locally on the
dedicated researcher-4 branch. The commit hash is necessarily reported in the
external pass handoff rather than inside the commit that contains this file.

## Blockers and next falsifiable step

There is no blocker to the strict internal-edge theorem. The next bridge is
now sharply isolated:

1. prove `kneserGraph` is regular of degree `k+1` when `|α|=2k+1`, by a
   cardinality-preserving equivalence between neighbors of `A` and `k`-sets
   in `Aᶜ`;
2. prove the generic finite-graph identity
   `|E(G.between X Xᶜ)| + 2|E(G[X])| = ∑v∈X deg_G(v)`;
3. combine those with `|E(G[X])|≤k²-1` and `|X|=2k` to obtain
   `|E(G.between X Xᶜ)|≥2k+2>2k`.

Falsifier/pivot: if the neighbor equivalence does not reduce to Mathlib's
existing finset-cardinality lemmas without a large bespoke enumeration layer,
formalize the generic cut degree-sum identity first and report the precise
missing finite-set counting lemma rather than claiming the boundary result.
