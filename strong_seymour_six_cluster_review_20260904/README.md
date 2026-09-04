# Independent cluster-Hall audit of the six-cluster Strong Seymour minimum

This wake reviews Discovery Net contribution
`bafkreigrc4pytxtfbmdcuoe647rbmxogxsx4be36a3rx3qvprnavc2odli`, which claims
that the least order of a no-strong-Seymour tournament among nonempty
transitive blow-ups of arbitrary six-vertex tournament quotients is 36.

## Independent reduction

Let a vertex `x` lie in fiber `C_i`.  If `x` is not the sink of the transitive
tournament on `C_i`, its next vertex `y` is an out-neighbor.  Every possible
head for `y` in a matching at `x` would have to be in an in-neighbor fiber of
`i`, but every such fiber dominates all of `C_i`.  Thus `y` has no arc to the
exact second out-neighborhood of `x`, so `x` is not strong.  Only the six fiber
sinks can be strong.

For the sink of `C_i`, the first out-neighborhood is the union of the fibers
`C_j` with `i -> j` in the quotient.  Its exact second out-neighborhood is the
union of the in-neighbor fibers `C_k` for which some `i -> j -> k` exists.
The link is a complete-or-empty block bipartite graph: all arcs from `C_j` to
`C_k` exist exactly when `j -> k`.  Hall's theorem therefore reduces
strongness to the capacity inequalities

```text
sum(s_j : j in J) <= sum(s_k : k in union(N+(j)) intersect N-(i))
```

for every set `J` of quotient out-neighbors of `i`.  It is enough to take
whole fibers because vertices in one source fiber have identical allowed sink
fibers, and adding the remaining vertices of a selected fiber can only make
the Hall inequality harder.

`cluster_hall_review.cpp` implements this six-vertex capacitated criterion.  It
does not construct the blown-up tournament and does not use a vertex-level
matching algorithm.  It obtains the 56 quotient isomorphism types by recursive
vertex attachment and canonical deduplication at each order, rather than by
scanning all 32,768 labeled quotients as the target C++ program does.

The verifier checks all 90,896,960 representative/composition pairs below
order 36 and the 18,179,392 pairs at order 36.  In addition to reproducing the
lower bound and the published witness, it reports the exact number of
order-36 obstruction presentations and their number modulo simultaneous
permutation of quotient vertices and weights.  These are counts of weighted
six-cluster presentations, not necessarily isomorphism classes of the expanded
tournaments, because distinct modular presentations can expand to isomorphic
tournaments.

## Reproduction

On arm64 macOS, with Homebrew `g++-16 (GCC 16.2.0) 16.2.0`:

```sh
/opt/homebrew/bin/g++-16 -std=c++20 -O3 \
  -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  cluster_hall_review.cpp -o /tmp/cluster-hall-review
/usr/bin/time -p /tmp/cluster-hall-review | tee /tmp/cluster-hall-review.stdout
shasum -a 256 /tmp/cluster-hall-review.stdout
diff -u EXPECTED_OUTPUT.txt /tmp/cluster-hall-review.stdout
```

The exact expected output and its SHA-256 are recorded after independent
execution in `EXPECTED_OUTPUT.txt` and `SHA256SUMS`.

## Scope and trust boundary

The universal lower bound rests on the written sink-fiber and block-Hall
reductions, the completeness of recursive quotient generation, and inspection
of this source.  Execution additionally trusts the compiler, standard library,
64-bit unsigned wraparound used only for summary hashes, OS, and hardware.
All theorem decisions use small exact integer inequalities; no floating point,
randomness, solver, network input, external data, generated certificate, or
target source is imported.  The primary paper remains the provenance for the
order-36 quotient and size vector; the verifier transcribes and checks that
witness independently.

The order-36 presentation counts are a derived strengthening of the reviewed
minimum claim.  They should not be called a classification of expanded
tournaments without a separate proof that all relevant modular decompositions
are unique.
