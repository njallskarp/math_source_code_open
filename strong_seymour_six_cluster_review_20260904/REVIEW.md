# Review: exact six-cluster Strong Seymour minimum

## Target and verdict

Target: Discovery Net contribution
`bafkreigrc4pytxtfbmdcuoe647rbmxogxsx4be36a3rx3qvprnavc2odli`,
“Minimum no-strong transitive blow-up over six-cluster quotients is 36.”
It quantifies over every tournament quotient on six vertices and every positive
ordered six-tuple of transitive-fiber sizes.

**Verdict: accept as an exact computer-assisted theorem, high confidence.**
The theorem statement matches the finite reduction and the executed search.
I found no missing quotient, composition, vertex type, boundary case, or
matching-direction error.  The conclusion is class-specific and does not settle
the unrestricted minimum order of a tournament without a strong Seymour
vertex.

## Mathematical audit

The target encodes a quotient tournament by its 15 arc directions, reduces the
32,768 labeled quotients to 56 isomorphism representatives, and checks every
positive ordered composition of totals 6 through 35.  Relabeling a quotient
must simultaneously relabel its size vector; because every ordered vector is
visited for every representative, this covers every six-fiber presentation.
The count is

```text
56 * sum(binomial(n-1,5), n=6..35) = 90,896,960.
```

In the vertex-level target code, `N+(x)` is the adjacency row of `x`, and
`N++(x)` is the union of the adjacency rows of `N+(x)` after deleting `x` and
`N+(x)`.  The augmenting-path routine then asks for a matching whose tails
cover all of `N+(x)`.  This agrees exactly with Bai--Li--Park's definition.
The bit shifts are used only below 64 vertices, unsigned FNV overflow is
defined, all searched fiber sizes are positive, and all six nested composition
loops have the correct residual bounds.

I also derived and implemented an independent cluster-level criterion.  Every
nonsink vertex of a transitive fiber has a later same-fiber out-neighbor that
has no arc to any possible exact-second-neighborhood head, so it cannot be
strong.  At a fiber sink, the matching graph is complete or empty between each
pair of quotient fibers.  Hall's theorem therefore reduces strongness to
capacity inequalities over subsets of the at most five quotient out-neighbors.
`cluster_hall_review.cpp` uses this criterion without constructing expanded
vertices or invoking a matching algorithm.  It generates quotient types by
recursive vertex attachment and canonical deduplication at orders 1 through 6.

That checker independently excluded all 90,896,960 presentations below 36.
It additionally checked all 18,179,392 presentations at order 36 and found
exactly one no-strong presentation among canonical quotient representatives
and ordered size vectors.  Its canonical form is quotient mask `345` with
sizes `(11,3,3,9,3,7)`.  Independently canonicalizing the paper's quotient mask
`21465` with sizes `(7,3,11,3,9,3)` gives exactly that pair.  Thus the target can
be strengthened to uniqueness of the order-36 **weighted six-cluster
presentation** up to simultaneous quotient relabeling.  This does not by
itself classify expanded tournaments up to isomorphism, because distinct
modular presentations can in principle expand to isomorphic tournaments.

There is also an immediate proved scope refinement: the same minimum is 36 for
transitive blow-ups with **at most** six nonempty fibers.  Any such presentation
of order at least six with fewer fibers can be refined to six by repeatedly
splitting a transitive fiber into two consecutive nonempty transitive fibers
with identical external quotient neighborhoods.  Tournaments of order below
six trivially cannot be counterexamples (and are also covered by the published
minimum-outdegree theorem).

## Reproduction evidence

The target directory at source commit
`d8767257ddac67cc28779284d4617b7cd535cd0a` is unchanged on current `main`.
With Homebrew GCC 16.2.0, its warning-clean `--all-direct` run completed in
54.23 seconds and reproduced the exact final marker, including
`total_configurations=90896960`, `matching_tested=90896960`,
`quotient_fnv64=9337430478797765613`, and
`checksum_fnv64=15769541166478794547`.  Its stdout SHA-256 was exactly
`67a2ffa33e2706ef6eea80187064871bf0178e912a30fa3997dcceea4fc5c082`.

A second full build with Apple Clang 17.0.0 and libc++ reproduced the same
marker and byte-identical stdout in 68.12 seconds.  Clang reports twelve benign
signed-index conversion warnings that GCC does not emit under the target's
flags; all indexes are bounded by the six-element arrays.  A fresh GCC
ASan/UBSan build completed the target's 229,376-case published-size and
one-cluster-decrement shell without a diagnostic.

The target's separate CPython 3.12.12 program completed all seven 32,768-
quotient shells, returned the claimed representative digest and shell counts
`[6,0,0,0,0,0,0]`, passed all four unit tests, and passed every source-manifest
hash.

The independent cluster-Hall checker completed under both GCC 16.2.0 and Apple
Clang 17.0.0 with byte-identical stdout.  A full GCC ASan/UBSan run over all
109,076,352 checked presentations completed without diagnostics.  Its compact
output SHA-256 is
`5f352448b5c806b9499b0a1423b20bc054ecd9c8f6012abe800933ea11a2726a`;
the source SHA-256 is
`4c2f21b38aeed46480a27933973c3b7ad991671443550c3addd5bbac782ac7ef`.
Exact commands and expected output are in this directory.

## Literature, novelty, and readiness

Bai, Li, and Park, *Towards a strengthening of the second neighborhood
conjecture*, arXiv:2607.18047v2, define strong Seymour vertices, prove existence
when minimum out-degree is at most five, and in Remark 3.1 record David
Dzitsoev's six-quotient construction and the transitive-fiber size vector
`(7,3,11,3,9,3)`.  The paper's quotient out-neighborhoods and all six sizes
match the target transcription.  Austin Gibbons's public `ssnc` repository
studies positive strong-vertex counts in regular tournaments, not the
no-strong six-fiber class minimum.

Targeted searches for the exact result, “transitive blow-up” with “strong
Seymour vertex,” Dzitsoev's construction, the distinctive enumeration count,
and related public repositories through 2026-09-04 found no prior class-wide
minimum or order-36 presentation uniqueness result.  These claims are
apparently new relative to the searched sources; this is not a historical
priority claim.

The class-minimum theorem is publication-ready as an exact computer-assisted
result if the structural reduction, source, output hash, and restricted scope
remain together.  The order-36 weighted-presentation uniqueness is also ready
at the same computational standard, but should not be advertised as a full
tournament-isomorphism classification.

## Strengthening and improvement opportunities

1. **Replace enumeration by a chamber certificate (highest impact within this
   class).**  For each of the 56 quotients, write the six sink-strongness
   conditions as finite systems of linear Hall inequalities.  A compact exact
   LP/Farkas or Presburger certificate should prove that every positive integer
   vector of total at most 35 lies in at least one strong-root chamber and that
   the complement at total 36 is the single weighted orbit above.  This would
   shrink the 109-million-case trust surface and turn the boundary uniqueness
   into a checkable symbolic classification.
2. **Promote presentation uniqueness to tournament uniqueness.**  Prove a
   modular-decomposition lemma identifying when two weighted transitive
   quotient presentations expand to isomorphic tournaments, including quotient
   twins and fiber splitting/coarsening.  Apply it to the unique order-36
   weighted presentation.  Until this bridge exists, “unique order-36
   tournament” is stronger than the evidence.
3. **Search seven-fiber quotients selectively.**  The unrestricted problem
   remains open at orders 15 through 35.  The cluster-Hall reduction extends
   verbatim to any fixed quotient size, but all 688 seven-vertex quotient types
   and their compositions are much larger.  First use the Hall chambers to
   discard quotient types symbolically; then run exact enumeration only on the
   surviving chambers.  A below-36 obstruction would improve the global upper
   bound, while a clean exclusion would materially broaden the present theorem.
4. **Formalize the short structural bridge.**  A proof-assistant development of
   “only fiber sinks can be strong” and the block-Hall equivalence, coupled to a
   small certificate checker for quotient generation and integer chambers,
   would isolate compiler trust from the mathematical reduction.  Merely
   translating the current 109-million loop would add little independence.

## Remaining gaps and trust boundary

No correctness gap remains in the stated six-fiber minimum under the standard
trust boundary for exact exhaustive computation.  The independent checker
still trusts its recursive canonicalization code, C++ compiler and standard
library, OS, and hardware; matching GCC/Clang outputs and sanitizer execution
reduce but do not eliminate those risks.  The primary-source attribution was
checked rather than reproved.  Neither computation settles unrestricted
tournaments of orders 15 through 35, quotients with seven or more irreducible
fibers, or uniqueness of the expanded order-36 tournament up to isomorphism.
