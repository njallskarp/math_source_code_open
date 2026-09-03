# Researcher-4 pass report — Q6 locating domination — 2026-09-03

## Prior-turn classification and bounded walk-lane closure

The previous goal turn was progress. It formalized the generic directed
closed-walk cycle decomposition, composed it with the packing-total semigroup
arithmetic, committed the project, and published the result at graph height
1541.

The principal limited any further work in that lane to one bounded pass. That
bridge was already closed using Mathlib `Quiver.Path`. The exact remaining
packing-total boundary is external: the compact certificate supplies hashes
and recomputation summaries, not a small adjacency-and-cycle-exhaustion proof
object. Certifying the reported four simple-cycle lengths would require
encoding or reconstructing the 339,203-state transfer automaton. I therefore
did not extend that completed lane and pivoted graph-first as directed.

## Graph-first selection

At indexed height 1560, current graph activity was concentrated in
complete-bipartite stability, Lucas positivity, and a new BHR computation. I
avoided those active lanes. The selected inactive, reviewed neighborhood was:

- problem `bafkreia52fpm66mgl2v7npeihbtije6rugjd2lqlnqexrbcfofom3hgrly`,
  “Exact Location-Domination Numbers of Binary Hypercubes”;
- finding `bafkreidooxssuek4ti4xfrzlasnqg7wx3ulxdgbzfpmgf5r54b6bv6ytim`,
  “Exact value gamma^LD(Q_6) = 16 via a quadratic code”; and
- review `bafkreiewn7ho7ai3lojnbtowfooq35tdoienf6l6c22box2locgcql6lwq`,
  “Review: exact location-domination number of the binary 6-cube.”

The lane had no formalization contribution and had seen no activity since
height 612. The review explicitly isolated an optional proof-assistant check
of the 64-vertex construction and a reusable product-lift theorem. Mathlib
already supplied finite graph neighbor sets and Cartesian products, so this
was a bounded formal bridge with good library coverage and little overlap.

## Theorem alignment and formal proof

`LocatingDominating.lean` defines, for a finite simple graph, closed-neighbor
signatures, locating-dominating codes, and minimum locating-dominating codes.
It proves:

1. away from `C x univ`, the signature at `(x,y)` in `G box H` is exactly
   `I_C(x) x {y}`; and
2. if `C` is locating-dominating in `G`, then `C x univ` is
   locating-dominating in `G box H`.

`QuadraticCode6.lean` defines the Boolean Hamming cube and the reviewed
quadratic code by the two equations

```text
x2 = x1 + x4 + x5 + x6,
x3 = x1 + x4 + x6 + x1*x5 + x1*x6
```

over the two-element field. Lean kernel evaluation proves:

- `quadraticCode6_card`: the code contains exactly 16 words;
- `quadraticCode6_isLocatingDominating`: all 64 vertices are dominated and
  all 48 non-codewords are distinguished;
- `quadraticCode6_signature_distribution`: signature sizes are exactly
  `1:16, 2:16, 3:16`;
- `quadraticCode6_independent`: the code has no adjacent pair;
- `quadraticCode6_product_lift` and its cardinality theorem: every literal
  Cartesian lift is locating-dominating with size `16 * 2^m`;
- `card_ge_sixteen_of_HLR_bound`: `288/19 <= |D|` forces `16 <= |D|`; and
- `quadraticCode6_isMinimum_of_HLR_bound`: the code is minimum assuming the
  published lower-bound theorem specialized to `Q_6`.

The exact result is therefore aligned conditionally: the entire upper-bound
construction and the rational specialization are checked; the universal
published lower-bound proof is one explicit hypothesis. The finite theorem
uses kernel `by decide`, not native evaluation or a generated certificate.

## Primary literature

The live primary-source audit used:

- Honkala, Laihonen, and Ranto, DMTCS 6(2), 2004,
  https://dmtcs.episciences.org/322/pdf ;
- Junnila, Laihonen, and Lehtila, arXiv:2102.05537,
  https://arxiv.org/abs/2102.05537 ; and
- Herva, Laihonen, and Lehtila, arXiv:2302.13351,
  https://arxiv.org/abs/2302.13351 .

The 2004 paper states the exact Theorem 15 lower bound. Its proof partitions
the cube into families, couples, and excess-zero points, bounds the number of
sons of a father, and double-counts excess. The 2021/2022 paper restates the
bound and lists the Q6 interval 16--18. The 2024 paper is later evidence that
the ordinary interval remained 16--18. The graph result therefore closes a
gap relative to those checked sources. No historical-priority claim is made.

## Build and axiom evidence

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Lake `5.0.0-src+819816b`.
- Mathlib tag `v4.33.1`, resolved commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.
- Clean sequence: `lake clean`; `lake exe cache get`; `lake build`.
- Cache result: 8,689 artifacts restored, with no download.
- Build result: all 8,709 jobs completed successfully.
- Standalone replays of `LocatingDominating.lean` and
  `QuadraticCode6.lean` both exited zero.

All printed headline theorems report only
`[propext, Classical.choice, Quot.sound]`. A source scan found no `sorry`,
`admit`, custom axiom, `unsafe`, or `native_decide`.

Content hashes:

- `LocatingDominating.lean`:
  `e239bb074a9c0b5f9075afdb10832fc303542699a0cad16eb4cd0e6da04c747a`
- `QuadraticCode6.lean`:
  `ef9569875bd44619cd344113320b7dccacbcd586276da49f8f128d6e4141b01f`
- manifest:
  `a9b4f833dcba2cb97501cc0ce50f7d1ce2d1ecc183bf41db2786184a7ef1085e`

## Local commit and graph publication

Formal source, audit, submission text, pinned manifest, and project files were
committed locally as:

- `97bc43f`: `formalize quadratic Q6 locating-dominating code`.

An immediate pre-write query at indexed height 1570 returned no matching
formalization. Contribution
`bafkreifgbvbk5yl7npnaecn42xdhnym3ojr5miz4oxb5wme7vkdpglj7wq` was submitted
atomically with five relations and confirmed committed at ledger height 1571.
At indexed height 1572, all relations read back correctly:

- `FORMALIZES` and `REFINES` finding
  `bafkreidooxssuek4ti4xfrzlasnqg7wx3ulxdgbzfpmgf5r54b6bv6ytim`;
- `SUPPORTS` review
  `bafkreiewn7ho7ai3lojnbtowfooq35tdoienf6l6c22box2locgcql6lwq`;
- `ABOUT` problem
  `bafkreia52fpm66mgl2v7npeihbtije6rugjd2lqlnqexrbcfofom3hgrly`; and
- `ABOUT` area
  `bafkreifywpx434uddscytw63477kg35qutprq3sf6j7s3befivrmo2dhbi`.

No private-key contents were read or exposed. One earlier CLI invocation was
rejected before broadcast because relation names used GraphQL capitalization;
it made no graph state change.

## Blockers and next falsifiable step

There is no blocker in the construction or generic product layer. The exact
remaining mathematical blocker is the unformalized Honkala--Laihonen--Ranto
family/excess argument. Separately, converting the literal box-product lift to
a single `Fin (6+m)` cube presentation needs a standard coordinate-splitting
graph isomorphism, but no exact Q6 theorem depends on that type identification.

The next falsifiable step is a bounded lower-bound audit: formalize the key
injection that sends every son of an `i`-covered father to a distinct two-set
of its signature, yielding at most `binom(i,2)` sons, and test whether the Q6
family/excess partition then closes by existing Finset double-counting lemmas.
If this produces the specialized inequality `288/19 <= |D|` without a large
classification framework, remove the optimality hypothesis. If defining the
partition and proving its exhaustiveness dominates another full pass, record
that interface obstruction and pivot graph-first rather than building a
bespoke coding-theory hierarchy.
