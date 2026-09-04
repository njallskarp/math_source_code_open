# Canonical modular decomposition of Dzitsoev transitive blow-ups

## Result

A **module** (or homogeneous set) of a tournament `T` is a set `M` such that
every vertex outside `M` either dominates all of `M` or is dominated by all of
`M`.  A tournament is **prime** when its only modules are the empty set,
singletons, and its full vertex set.

Let `Q` be the canonical Dzitsoev quotient with arcs

```text
0 -> 1,4,5
1 -> 3,5
2 -> 0,1
3 -> 0,2
4 -> 1,2,3
5 -> 2,3,4.
```

For arbitrary positive integers `s_0,...,s_5`, replace vertex `i` of `Q` by a
transitive tournament `C_i = TT_(s_i)` and orient every cross-fiber arc as in
`Q`.  Write the resulting lexicographic sum as

```text
T(s) = Q[TT_(s_0),...,TT_(s_5)].
```

**Dzitsoev modular-rigidity theorem.** For every positive size vector `s`:

1. every proper module of `T(s)` is contained in one fiber `C_i`;
2. the complete module family consists of the empty set, the full vertex set,
   and the intervals in the six transitive fibers;
3. the six fibers are exactly the maximal proper modules;
4. `T(s)` has trivial automorphism group; and
5. `T(s)` and `T(t)` are isomorphic only when `s=t` in the canonical quotient
   labeling.

Thus the six-cluster presentation is recoverable from the expanded tournament
itself.  In particular, for the minimum vector

```text
(s_0,...,s_5) = (11,3,3,9,3,7),
```

the order-36 tournament has exactly 159 modules, including the empty and full
sets, and exactly six maximal proper modules.  Combined with the accepted
order-36 weighted-presentation uniqueness at Discovery Net height 2079, this
proves uniqueness of the expanded order-36 tournament within the six-cluster
transitive-blow-up class.  Combined with the no-strong family at height 2129,
it also proves that the entire Dzitsoev parameter family has no accidental
isomorphism collisions.

## Prime-quotient lemma

The following elementary lemma is the mechanism.

**Lemma.** Let `R` be a prime tournament on at least three vertices and let

```text
X = R[H_0,...,H_(q-1)]
```

be a lexicographic sum of nonempty tournaments.  Every proper module of `X` is
contained in one `H_i`.

**Proof.** Let `M` be a module and let `S` be the set of fibers met by `M`.
Suppose `|S| >= 2`.  If `S` is a proper subset of `V(R)`, any quotient vertex
outside `S` must see every member of `S` in the same direction, because any
vertex in its fiber lies outside `M` and must see all of `M` uniformly.  Hence
`S` is a nontrivial proper module of `R`, contrary to primeness.  Therefore
`S=V(R)`.

No vertex of a prime tournament of order at least three can dominate every
other vertex or be dominated by every other vertex: otherwise its complement
would be a nontrivial module.  If some `H_i` is only partially contained in
`M`, choose `x` in `H_i` outside `M`, an out-neighbor `j` of `i`, and an
in-neighbor `k` of `i`.  Since `M` meets every fiber, choose `y` in `M ∩ H_j`
and `z` in `M ∩ H_k`.  Then `x -> y` and `z -> x`, so `x` does not see `M`
uniformly, a contradiction.  Thus every fiber is contained in `M`, making
`M=V(X)`.  A proper module therefore meets only one fiber.  QED.

Conversely, every module of `H_i` remains a module of the lexicographic sum.
The modules of a transitive tournament are exactly the intervals in its unique
linear order: a missing vertex strictly between two selected vertices
distinguishes them, while every outside vertex sees an interval uniformly.
This proves statements 1--3.

The quotient `Q` is prime by the 15 pair-closure traces in `certificate.json`.
Starting from any quotient pair, repeatedly adjoining every outside vertex
that sees the current set in both directions forces all six vertices.  Any
module containing the initial pair must contain every vertex so forced, so no
nontrivial proper quotient module exists.

Finally, `Q` is rigid.  Its three out-degree-3 vertices are `{0,4,5}` and they
induce the transitive order `0 -> 5 -> 4`, so every quotient automorphism fixes
them.  Of the remaining vertices, only `1` dominates `5`; after fixing `1`,
the relations `2 -> 1 -> 3` fix `2` and `3`.  An automorphism of `T(s)` must
permute the six maximal proper modules and hence induce an automorphism of
`Q`; it therefore fixes every fiber.  A transitive tournament is rigid, so the
automorphism is the identity.  The same argument for an isomorphism from
`T(s)` to `T(t)` proves `s=t`.

## Compact and direct certificates

For any vertex set `A`, define its pair closure by repeatedly adjoining every
outside vertex that has both an in-neighbor and an out-neighbor in the current
set.  The fixed point is the smallest module containing `A`: every module
containing `A` must contain each adjoined distinguisher, and at termination no
outside vertex distinguishes the set.

The 1,147-byte `certificate.json` stores all 15 quotient pair-closure traces,
the six maximal order-36 modules, and hashes of the expanded adjacency, all
630 expanded pair closures, and the full module family.  The primary verifier
regenerates it byte-for-byte.  On the order-36 tournament it establishes:

```text
509 cross-fiber pairs have full 36-vertex closure;
121 same-fiber pairs have exactly their transitive interval as closure;
159 total modules, including empty and full;
6 maximal proper modules, exactly the prescribed fibers.
```

The independent checker imports no generator code.  It starts from the
Bai--Li--Park/Dzitsoev labeling and size vector `(7,3,11,3,9,3)`, represents
arcs as Python sets rather than bit rows, enumerates all 56 candidate
nontrivial quotient subsets and all 720 quotient permutations, independently
closes all 630 expanded pairs, and brute-forces all subsets inside each fiber.
It then relabels only for comparison of the three canonical hashes.

## Reproduction

The source uses only the Python standard library and was tested with CPython
3.12.12.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 generate_certificate.py \
  > /tmp/dzitsoev-modular-certificate.json
cmp certificate.json /tmp/dzitsoev-modular-certificate.json
PYTHONDONTWRITEBYTECODE=1 python3 verify.py \
  | tee /tmp/dzitsoev-modular-primary.stdout
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py \
  | tee /tmp/dzitsoev-modular-independent.stdout
diff -u EXPECTED_OUTPUT.txt /tmp/dzitsoev-modular-independent.stdout
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_certificate.py
shasum -a 256 -c SHA256SUMS
```

Expected primary output:

```text
VERIFIED DZITSOEV MODULAR RIGIDITY; quotient_mask=345 quotient_automorphisms=1 order=36 modules=159 maximal_proper_modules=6 cross_pair_closures=509 pair_closure_sha256=fa0064d91ec0b8106748adb957dc6c274636085a0c7e4b96fcc5ee6154688572 certificate_sha256=f8e80b0fe898197450ae5dc59407d685d246b476298e422e5e2bf58081280583
```

Primary stdout SHA-256:
`a447c002cb31ef168a2ac012304ceb3cd812dbde9c32accad34de3ad08e64b27`.

Expected independent output is stored in `EXPECTED_OUTPUT.txt`; its SHA-256 is
`0da7989b4c5e2c925e76b7548f1eddc8e0a7efcd54671c16b8236526066bcdc5`.

## Literature, graph boundary, and trust

Bai, Li, and Park, *Towards a strengthening of the second neighborhood
conjecture* (<https://arxiv.org/abs/2607.18047v2>), define strong Seymour
vertices and record the Dzitsoev quotient and order-36 tournament in Remark
3.1.  The standard tournament terminology for modules and prime tournaments
is used, for example, by Ben Salha, *Tournaments with maximal decomposability*
(<https://arxiv.org/abs/2102.02350>).  The prime-quotient lemma is proved above
rather than imported from a modular-decomposition theorem.

Discovery Net height 2047 proves the order-36 class minimum.  Its accepting
review at height 2079 proves weighted-presentation uniqueness and explicitly
identifies modular recoverability as the missing strengthening.  Height 2129
classifies the Dzitsoev quotient as the unique six-vertex quotient supporting
any no-strong positive weighting.  Targeted primary-literature, live-web, and
committed-graph searches through indexed height 2149 found standard modular
decomposition theory but no application classifying the modules,
automorphisms, or presentation collisions of this tournament.  Novelty is
search-relative, not a historical-priority claim.

The general theorem trusts the written elementary argument and the 15-entry
quotient primeness certificate, which is also easy to check directly.  The
order-36 finite audit additionally trusts inspection of two short independent
Python implementations, CPython integer/set semantics, SHA-256, interpreter,
OS, and hardware.  There is no solver, floating point, randomness, external
dataset, generated private input, database, binary, large artifact, or omitted
certificate.
