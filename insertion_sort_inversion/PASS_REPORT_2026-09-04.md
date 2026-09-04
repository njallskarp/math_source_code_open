# Pass report: insertion-sort shifts and inversions

Date: 2026-09-04.

## Graph-first selection

The committed ledger and dedicated RPC agreed at heights 2346, 2354, and
2363 during selection.  New reviews after the preceding pass concerned only
the excluded Parts certificate and Ramsey lanes.  The older reviewed frontier
was therefore audited for a short structural bridge.

The selected target is the height-1891 proof “Exact categorical
insertion-sort expectations and finite-population correction”
(`bafkreifqgcnaghfxkdt2uhmgg75irhe3mcziprhv22jnzbxjop6vqa7wue`), about the
height-144 problem
`bafkreihticuj5bxt3myqflkenjuhlyakbtditioffxg6ui7j46wq3l3mnu`, and accepted
by the independent height-1895 review
`bafkreidnnm33pbkmb34frdbvlasvxbk3om6hewfjnyx77bwgzphu4zuhxm`.
No graph contribution with “insertion” in its title was a formalization, and
the “inversion” search returned no insertion-sort formalization through
indexed height 2354.

The rejected alternatives were an analytic graphon/cut-modulus theorem, the
already-closed stable-tournament and line-graph results, a representation-heavy
Ray--West construction, and the current certificate-heavy Parts and Ramsey
frontiers.

## Exact theorem and formal architecture

The informal bridge says that strict adjacent insertion-sort swaps equal the
number of pairs `i < j` with `A_i > A_j`, including words with repeated
categories.  The Lean file represents words as `List α` for an arbitrary
`LinearOrder α`; `inversionCount` recursively counts the later entries below
each head, exactly enumerating those ordered position pairs with occurrence
multiplicity.

Seven exported theorems establish:

1. weakly increasing lists have inversion count zero;
2. swapping any strictly inverted adjacent pair removes exactly one inversion;
3. the insertion cost is the length of the prefix moved by Mathlib's
   `orderedInsert` decomposition;
4. on a sorted list that cost is the number of entries below the inserted key;
5. sorting preserves that number by Mathlib's permutation theorem;
6. the total stable insertion-sort shift count equals the inversion count; and
7. Mathlib's insertion-sort output has inversion count zero.

Canfield--Janson--Zeilberger, arXiv:0908.2089, Section 1, independently fixes
the same strict position-pair definition, q-multinomial enumerator, and
fixed-multiplicity mean `e₂/2`.  These facts and both probability models are
external context, not premises of the Lean theorem.

## Build and axiom audit

- Lean `v4.33.1`, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`;
- Mathlib `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`;
- clean build:
  `lake clean insertion_sort_inversion && lake build InsertionSortInversion`;
- result: `Build completed successfully (580 jobs).`;
- all seven axiom sets are subsets of `propext`, `Classical.choice`, and
  `Quot.sound`;
- forbidden-token scan: clean;
- source SHA-256:
  `b3caf0efe588aa03419753a7fb6b7e4a6cc831bc44ba0cde9fe8caf6bad055d1`.

## Trust boundary

No external data or computation enters the proof.  The formalized counter is
the adjacent-shift/one-position-shift cost of Mathlib's stable fold-right
insertion sort; it is not the comparison count of an imperative implementation.
The expectation identities, probability-space encodings, q-multinomial
formula, and variance claims remain unformalized.

## Publication, graph, and local commit

Public source commit:
`6459167fcea7eb3a0aab8bde997549b9287a3d0f`.

Public directory:
`https://github.com/njallskarp/math_source_code_open/tree/main/insertion_sort_inversion`.
The remote `main`, directory response, and raw source SHA-256 were verified
after pushing from a fresh isolated clone.

The final duplicate audit found no insertion/inversion formalization through
indexed height 2410; the ledger and RPC both reported height 2410 immediately
before submission.  Graph formalization:
`bafkreia4i6ihndb6f6j446sx5aguyfslhr6qzayucxdhw42euthh7vshbq`, confirmed
committed at height 2411 (queried from the ledger at height 2412).

Atomic relation artifacts:

- `bafkreihswrws7nqzw7l6rb53ymckkcm2syv5hremufw6u7whvnqv7fyk2y`;
- `bafkreihjxbnr273ds6aw4y3p2sgldodek6niql7rjbe3prttjhmwv5vs6i`;
- `bafkreibhuqesntfqod7w45fassfbkkseheq574djhgagvwsdssztuh6lf4`;
- `bafkreibo3hsudecduijjksyhwrtdz6gtfiec3awkt4prpktrln56j4qcki`.

Local campaign commit blocker: this session exposes the campaign repository's
root `.git` directory as read-only.  Explicit-path `git add` failed with
`Unable to create .git/index.lock: Operation not permitted`; a subsequent
`git commit --only` correctly refused the still-unindexed new paths.  The
project therefore remains an isolated untracked directory in the campaign
worktree.  No unrelated tracked or untracked work was staged or changed.

## Next falsifiable step

Close this bounded deterministic lane after submission.  In the next graph-first
pass, prefer a reviewed finite-graph/finite-set theorem with a native Mathlib
statement.  Reopen the categorical expectation lane only if Mathlib's uniform
finite probability API makes the fixed-count expectation a short theorem;
do not expand into q-multinomial or variance infrastructure merely to remain in
this lane.
