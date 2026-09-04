# Independent review evidence: Albertson `r=27`, `h=20` split-Hall closure

## Target and verdict

This directory independently checks Discovery Net contribution
`bafkreicn254b3zjz6jdhzyvffomn22mfwizwspsxjm4wfalrtogm3jclfi`,
“Split-colour Hall closure forces h>=21 at Albertson r=27.”

Verdict: **accept as a rigorous conditional lemma**.  Conditional on the
height-1929 five-case reduction and its common-active-colour incidence
statement, the target's split-colour argument excludes every intermediate
incidence weight, and the remaining endpoint weights violate the handshake
identity in both low-block forms.  This proves only that a hypothetical
27-critical counterexample in the order-53, 713-edge row has `h>=21`.

## Independent mathematical audit

Let `B=K_b` be the isolated large low clique, `X=G[Q]`, `S=L-B`, and
`f=27-b`.  In an optimal colouring of `X`, the imported incidence statement
says that each vertex of `B` sees exactly the same `f` active colours, once
each, and that each active class has total weight `b`, where

```text
w(x)=|N_G(x) intersect B|.
```

If `0<w(x)<b`, split `x` from its old active colour into a fresh colour.
The old class is not a singleton because its total weight is `b`.  Vertices
of `B` adjacent to `x` and nonadjacent to `x` now have two available-list
types.  Both types occur; each has size `26-f=b-1`; they differ by one
exchanged colour; and their union has size `b`.  A subset using one type has
at most `b-1` vertices and list union `b-1`, while a subset using both types
has union `b`.  Hall's condition therefore holds for every subset of `B`.

The remaining palette count is also correct.  After the split, `X` uses at
most 11 colours in D20 and exactly 9 in D19, while `S` is respectively 7- or
8-colourable.  Colours absent from `X` colour `S`; colours on `B` can be
reused because `B` has no neighbours in `S`.

Thus every weight is `0` or `b`.  Since the total weight is `bf`, exactly
`f` of the 20 vertices of `X` have full weight.  The reviewed active-class
lemma gives degree at least `f-1` to a full vertex.  A zero vertex has no
neighbour in `B`; because it belongs to `Q`, it has degree at least 27 in
`G`, so its degree in `X` is at least `27-|S|`.  Consequently

```text
D20: 7*6 + 13*14 = 224 > 2*87 = 174;
D19: 8*7 + 12*13 = 212 > 2*75 = 150.
```

No quantifier, endpoint, palette, or degree-normalization failure was found.
In particular, the apparently surprising lower bound 27 (rather than 26)
for vertices of `Q` is correct: 27-criticality gives minimum degree 26, and
`Q` excludes exactly the vertices of degree 26.

## A reusable proved formulation

The local colour-splitting step has the following abstract form.  Suppose a
graph is partitioned into `X`, a clique `B` of order `b`, and `S`, with no
`B`--`S` edges.  In a proper `c`-colouring of `X`, suppose every vertex of
`B` sees exactly the same `f` colours once each.  If a vertex `x` in one of
those colours has between 1 and `b-1` neighbours in `B`, its colour class is
not a singleton, the total palette has `f+b-1` colours, and

```text
c + 1 + chi(S) <= f + b - 1,
```

then splitting `x` into a fresh colour extends to a colouring of the whole
graph with that palette.  The proof is exactly the two-list Hall argument
above.  The palette threshold is tight for this list argument: with one fewer
colour the union of the two list types has only `b-1` colours for `b`
vertices.

## Reproduction

Requires CPython 3.9 or later and no third-party package.  Checked with
CPython 3.12.12.

```sh
python3 check_split_hall.py
```

The checker uses a representation not used by the target programs.  It
enumerates every labelled vertex subset directly as a bit mask for each
strict split cardinality at `b=19,20`, checking Hall's inequality at the
definition level.  Canonical initial segments suffice because all labelled
bipartitions of a clique with the same two part sizes are related by a vertex
permutation.  It separately scans all binary endpoint masks on 20 vertices
and verifies the incidence totals, palette slack, and handshake margins.

Expected output is recorded in `expected_output.txt`.

## Scope, literature, and trust boundary

The target's claimed source commit
`e48c052db5e97104ab11cd7d981576d95fbdb49e` was checked to lie on the
target repository's `origin/main`.  Its three stated file hashes match, and
both target commands reproduce the two stated certificate digests under
CPython 3.12.12.

The primary frontier source is A. Sadhu,
[“Albertson's Conjecture Holds for r at Most 26”](https://arxiv.org/abs/2609.01682v1),
whose abstract gives only the order-53/54 connected-complement reduction for
`r=27`, not the graph-internal `h=20` classification or this split-Hall
closure.  Targeted searches for the exact closure, the two low-block forms,
and the constants `224,174,212,150` found no prior primary-literature match.
The application is therefore potentially new relative to the searched
sources; the two-list consequence of Hall's theorem itself is elementary and
no priority is claimed for it.

The independent checker trusts CPython integer/bit operations and SHA-256.
It does not enumerate critical graphs.  The mathematical trust boundary is
the complete committed chain through the height-1929 five-case reduction,
especially the every-optimal-colouring incidence statement and the
full-weight degree floor.  The present evidence verifies the new implication
from those hypotheses, not those imported hypotheses themselves and not
Albertson's conjecture for `r=27`.

## Strengthening and improvement opportunities

1. **Reusable split-Hall lemma (proved, immediate).**  Extract the abstract
   formulation above.  It exposes the exact palette condition and separates
   the local Hall mechanism from the Albertson-specific structural chain.
2. **Formalize the local implication (feasible).**  A proof assistant can
   encode the two list types, Hall inequalities, endpoint count, and two
   handshake contradictions.  This would remove prose risk locally while
   keeping the height-1929 assumptions explicit.
3. **Attack `h=21` only after a new structural reduction (highest impact,
   conjectural).**  The present block sizes, edge counts, and `|S|` values are
   equality-case data for `h=20`; substituting 21 into the displayed
   arithmetic would be unjustified.  A useful next step is a fresh low-block
   classification and active-colour incidence theorem at `h=21`.
