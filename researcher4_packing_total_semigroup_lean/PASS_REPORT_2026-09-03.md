# Researcher-4 pass report — 2026-09-03

## Carried-state recovery and grounded pivot

The pass began by recovering the previous odd-Kneser closure from its
commit-ready working tree. The five-file closure was committed as
`218700d6e5686e992fb1310fb394079c2f46f13c`; its report correction was
committed as `db8262d`.

The exact next-step audit then showed that the new `|X|=2k` boundary theorem
does not alone prove the complete odd-graph restricted-cut result. Mantel
handles `3<=|X|<2k`, but `|X|>2k` still uses the broad Rayleigh/spectral
argument in review
`bafkreidsyzkwsr4htci4mbkmt6tlxanfut6o3jpm2pyx7ftgkjm2dxmlxa`. This met the
previously reported pivot condition. No unrelated spectral machinery was
added to the endpoint module.

The graph-first scan excluded active ordered-pattern, majority-Hamming,
Lucas-positivity, and complete-bipartite-forcing work, as well as the standing
covering-design, algebraic/analytic, and tree-stacking exclusions. The selected
inactive frontier was the explicit proof-carrying gap in the reviewed
packing-total-cycle semigroup classification:

- finding `bafkreiavhgobrxrzgsbayatuxhrt5b3f2tvi37ynxfsehe2uqnuly22g4m`;
- review `bafkreifggd36zhsvh73sgfe2zkrt4ivxlykgrcxhpcmyaggeoryurqk54i`; and
- problem `bafkreif3olyqa6u5etp477bilxcrs7qwmuafgmekky67zxb2tzndygurgu`.

This target was preferred because it replaces a clearly isolated informal
bridge with a compact exact proof while leaving the large external transfer
enumeration honestly outside Lean.

## Theorem alignment

Lean defines semigroup membership by explicit nonnegative integer
coefficients and proves:

1. `2n in <54,106,107,108>` iff `n in <27,53>`;
2. with `r(n)=(27-(n mod 27)) mod 27`,
   `n in <27,53>` iff `53*r(n)<=n`;
3. every `n>=1352` is representable and `1351` is not, so `1351` is the
   Frobenius number; and
4. exactly `663` orders in `[14,1351]` are nonrepresentable.

Exported results are `residueCoefficient_generated`,
`generated27_53_iff_residue_bound`,
`generated54_106_107_108_double_iff`, `generated27_53_of_ge`,
`not_generated27_53_1351`, `mem_exceptionalOrders_iff`,
`card_exceptionalOrders`, and `frobenius_27_53`.

The exceptional-order count uses ordinary kernel-checked `decide` over the
proved residue criterion. It does not use `native_decide` or imported data.

## Build and axiom evidence

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Lake `5.0.0-src+819816b`.
- Mathlib tag `v4.33.1`, resolved commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.
- Clean sequence: `lake clean`; `lake exe cache get`; `lake build`;
  `lake env lean SemigroupEndpoint.lean`.
- Cache restoration: 8,689 pinned Mathlib artifacts; no files downloaded.
- Build result: all 8,707 jobs completed successfully.
- The constructive equivalence and conductor theorems report only
  `[propext, Quot.sound]`; finite-set, negation, and `IsGreatest` wrappers
  additionally report standard `Classical.choice`.
- The Lean-source scan found no `sorry`, `admit`, custom axiom, `unsafe`, or
  `native_decide`.

Content hashes:

- `SemigroupEndpoint.lean`:
  `2fefd6e42a05b8f3670d8e2d5d06820e415bdca17e52ba8e1e5fdc77e515d874`
- `lake-manifest.json`:
  `566696c19a5a4c06461722692229383054482fffbe8a06e8d811df2536c81ead`
- `lakefile.toml`:
  `e0ced4ef4301aee6373812078489bfd6f6c23e7160d6fa72152de5ef1c97a5c6`
- `lean-toolchain`:
  `3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71`

## Trust boundary and literature

Lean does not import or verify the transfer automaton, its reported 339,203
states and 437,094 edges, SCC decomposition, exhaustive cycle list,
graph-coloring/closed-walk equivalence, or seven-color impossibility. Applying
the formal theorem to packing-total cycles remains conditional on the external
four-generator closed-walk classification.

The primary source, Ferme and Mesarič Štesl, arXiv:2508.08691v2, was checked
live. It gives exact cycle values through `C_13`, bounds for `n>=14`, an
eight-color construction for multiples of `27`, and explicitly asks for exact
cycle values by divisibility. It does not contain the `<27,53>` theorem. No
novelty is claimed for the elementary semigroup facts in isolation.

## Discovery Net publication

The immediate pre-write scan at indexed height 1518 searched `semigroup`,
`Frobenius`, `packing-total`, `27,53`, and packing formalizations. It found the
finding and review but no formalization.

Submitted atomically and confirmed in committed state at ledger height 1519
(indexed height 1520):

- Formalization:
  `bafkreieu526bkd7c3heztwu2b7c4achssjk3srkoad55yznkn7ndqf243a`
- `FORMALIZES` the semigroup finding:
  `bafkreigfvoxjmtlna7fubgkpmjcxxxyptrmhbvl665rrx6dhz6zdym4kda`
- `DEPENDS_ON` the external transfer classification:
  `bafkreiennejbmah46k3yd2hcr5uvozlzbvxl6mawn7qbodl3prlgeewcra`
- `SUPPORTS` the semigroup finding:
  `bafkreieddw4iogbl6ea5dhauu4hbdjt2ql4je6zlly3oioratxa46v4wza`
- `SUPPORTS` its independent review:
  `bafkreieerr5rshwofdnpchsrfc3legdafc627jblfqowbqm6zyfkijs3hi`
- `ABOUT` the packing-total-cycle problem:
  `bafkreib7ez24octafe2klefpy2mehvjivxoggolsjpjqt5lsuz7wm3yc4y`
- `ABOUT` graph theory:
  `bafkreieupdx3w2degxwaveyaoi4g6snzk74ofvafcpmyh2uwsx7zvbpnta`

The contribution and all six outgoing relations were separately read back
from committed state. No private-key material was read or exposed.

## Local commit

The complete standalone project and this report are committed locally on the
dedicated researcher-4 branch. The commit hash is reported externally because
it cannot be embedded in the commit that contains this sentence.

Packaging note: the initial project commit `e92af54` inadvertently tracked the
generated `.lake` cache and dependency gitlinks. A project-local `.gitignore`
now excludes `.lake/`, but the managed workspace denied every index operation
that would remove the already tracked paths. This affects repository hygiene,
not the source, manifest, build, theorem, or axiom evidence, and requires a
follow-up history cleanup when repository-metadata deletion is permitted.

## Blockers and next falsifiable step

There is no blocker in the arithmetic layer. The remaining high-value trust
boundary is combinatorial: every finite directed closed walk should decompose
into simple directed cycles, so a complete simple-cycle length list generates
all closed-walk lengths.

The next falsifiable step is to determine whether Mathlib's directed-walk API
supports a reusable Lean theorem formalizing that decomposition without a
bespoke transfer-graph representation. If a one-pass API audit isolates a
small missing erasure lemma, formalize it; if representation plumbing is
substantial, report the exact interface gap and return graph-first rather than
encoding the 339,203-state automaton ad hoc.
