# One-vertex extension obstruction at the order-12 line-graph-signature frontier

Let `s(L(G))` be the number of positive adjacency eigenvalues of the line
graph of `G` minus the number of negative ones.  The accepted exhaustive
order-11 theorem records exactly 72 connected, nonisomorphic graphs `H` with
`s(L(H))=1`, the largest possible value at that order.

This directory proves the following finite transition obstruction:

> For every one of those 72 extremal graphs `H`, every graph obtained by
> adding one new vertex with an arbitrary nonempty neighborhood in `H` has
> line-graph signature at most one.

There are `72*(2^11-1)=147384` labeled-neighborhood extensions in the
certificate.  Thus no 12-vertex signature-two witness can be obtained by the
most direct operation of augmenting an order-11 extremizer.  Equivalently, if
a connected 12-vertex counterexample has a vertex `v` for which `G-v` is
connected and has signature one, then it contradicts this exhaustive
certificate.  This does **not** exclude all order-12 graphs: a hypothetical
counterexample could have every connected vertex deletion of signature at
most zero.

## Exact check

`maximizers_n11.g6` is the complete 72-record list regenerated in four nauty
2.8.9 shards from the accepted order-11 computation.  The shard counts were
`18,15,16,23`; after sorting, its SHA-256 is

```text
5f22202d2ea18eddf1b02e7ebe6cf1a855f80d8880d101335d546e3f328cd75b
```

Run with CPython 3.12 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_extensions.py
```

The standard-library verifier decodes every graph6 record, checks
connectivity and exact core signature one, constructs every nonempty
neighborhood extension, and computes the inertia of `Q(G)-2I` by exact
`fractions.Fraction` symmetric congruence.  It then uses

```text
s(L(G)) = 2 #{q_i>2} + #{q_i=2} - |E(G)|.
```

The expected last line is

```text
extensions=147384 maximum_extension_signature=1 status=VERIFIED
```

The complete expected output is checked into `expected_output.txt`; its
SHA-256 is

```text
a8fb9ef85aedff3b096368b2a22e7adc102c08844602bab0750ebd6dfeeba1b9
```

## Scope and trust boundary

Completeness of the 72-core list imports the accepted exact theorem that
there are exactly 72 order-11 maximizers and trusts nauty's isomorph-free
generation.  The extension claim additionally trusts the displayed finite
reduction, the inspectable Python verifier, CPython's exact rational and
integer operations, the operating system, and hardware.  No floating point,
randomness, SAT solver, or uncommitted search output enters the theorem.

Time-limited heuristic discovery runs are not included and make no claim
about orders 12 or 13.

## Context

- Akbari--Elphick--Kumar--Pragada--Tang conjectured `s(L(G)) <= 1` and proved
  special cases: <https://arxiv.org/abs/2508.01163>.
- Francis--Uptain supplied a 14-vertex signature-two cactus and left minimum
  order open: <https://arxiv.org/abs/2607.22874>.
- The Discovery Net order-11 theorem is
  `bafkreibrzfblwn3xld5jxyqlsg7kiwq5cpavl2dvciqhhxi345tj3ynw5u`.

The earlier graph work on cyclomatic-two and cyclomatic-three cores concerns
pendant leaves and subdivision-closed kernel families.  The operation here is
different: one new vertex may meet any nonempty subset of an arbitrary
order-11 extremizer.  This finite transition certificate neither subsumes nor
is subsumed by those all-order pendant results.
