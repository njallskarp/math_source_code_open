# Ramsey R(5,5): a compact third-anchor exclusion

This package closes the exact two-anchor incidence represented by the
height-2851 degree-compatible short-clause survivor.  The base coloring has
452 red edges, degree profile `20^8 21^26 22^9`, and four valid monochromatic
neighborhoods at roots `0` and `3`.  Fixing those neighborhoods leaves exactly
210 doubly unseen edges.

Reanchoring vertex `1` and imposing its full red and blue neighborhood
conditions produces a deletion-minimal core of eight ordinary Ramsey clauses
on seven unseen edges.  A direct unit-propagation chain makes the core
inconsistent.  Therefore all `2^210` completions of this fixed incidence are
excluded, independently of degree or total-edge constraints on the completion.

This is not a new upper bound for `R(5,5)`, does not classify all possible
two-anchor incidences, and does not exclude the whole `d=22,t>=108` branch.
It shows exactly where the height-2851 limitation witness stops: its four
valid neighborhoods cannot be extended even to the full local constraints at
the selected third anchor.  The remaining family-wide problem is incidence
classification, not a longer fixed-width clause census for this instance.

## Exact replay

The primary checker uses only the Python standard library.  It reconstructs
the base graph, all four fixed neighborhoods, each of the eight local clauses,
the 210-edge interface, and the complete seven-variable truth table.

```sh
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | cmp - EXPECTED_OUTPUT.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py | cmp - EXPECTED_OUTPUT.json
shasum -a 256 -c SHA256SUMS
```

An independent checker uses NetworkX's graph6, complement, and maximal-clique
implementations and tests the eight forbidden colored configurations directly:

```sh
uv run --no-project --cache-dir /tmp/r55-third-anchor-nx-cache \
  --with networkx==3.6.1 --python python3 independent_check.py \
  | cmp - EXPECTED_INDEPENDENT.json
```

The optional discovery scripts require python-sat 1.9.dev15:

```sh
uv run --no-project --cache-dir /tmp/r55-third-anchor-sat-cache \
  --with python-sat==1.9.dev15 --python python3 core_search.py --root 1
```

The SAT search and its extracted core are outside the proof boundary.  The
stored certificate is accepted only after the solver-free exhaustive replay.

## Compact invariants

- base local profiles: `(22,108,6)`, `(20,100,0)`, `(21,99,8)`, `(21,98,9)`;
- two-anchor cells `(10,11,10,10)` and 210 unseen diagonal edges;
- third anchor `1`, eight clauses, seven variables, zero of 128 assignments;
- every one-clause deletion is satisfiable;
- base edge SHA-256:
  `1910c00f11e247f45ccea2508784d01eb87f5ac3e7511b1ee134566a06e6df73`;
- clause SHA-256:
  `bf5d83bd2d6bca4faea493bb7ed74feb8f0bf1d6390848b36b9bfd88274e4ff4`.

## Trust boundary and provenance

The proof certificate consists of the two compact graph6 cores, six listed
deletions, the explicit cross matrix, and eight local clauses with their vertex
origins.  Trusted are the short source, ordinary CPython semantics, hardware,
and SHA-256 collision resistance.  The independent replay additionally trusts
NetworkX 3.6.1.  Python-sat and every solver verdict are explicitly untrusted.

The graph6 records originate in [Brendan McKay's `(4,5)` Ramsey
data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html) used by the
height-2851 package.  Their exact properties needed here are checked directly;
catalog completeness is not used.  Primary methodological context is
Angeltveit and McKay, [*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709),
arXiv:2409.15709v2, especially its pointed-neighborhood gluing framework.  No
novelty is claimed for the general gluing or CNF reductions.  These primary
sources were checked live on 2026-09-05.
