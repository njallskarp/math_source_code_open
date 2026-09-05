# Gallai block-spectrum capacity certificates

This standalone Lean 4 project formalizes the finite packing bridge used in
the low-vertex Gallai eliminations for the `r = 28` Albertson frontier.  It is
a conditional downstream audit, not a proof of the Albertson conjecture for
`r = 28` and not an independent review of the cited Discovery Net artifacts.

## Result

For a block increment `u = |V(B)| - 1`, a clique block contributes
`phi(u) = u(u+1)/2` edges.  An odd-cycle block of increment `u >= 2`
contributes `u+1` edges and is compressed exactly to one increment-2 clique
atom and `u-2` increment-1 atoms.  This preserves both total increment and
edge count.

`GallaiBlockSpectrum.lean` proves a reusable theorem: any finite packing is
bounded by a supplied finite Bellman supersolution.  Three small certificates
then prove:

- a unique increment-25 atom, total increment at most 50, and no increment-24
  atom imply at most 604 edges;
- total increment at most 49 and atom size at most 25 imply an edge total at
  most 581 or at least 600;
- total increment at most 48 and atom size at most 25 imply an edge total at
  most 559 or at least 576.

The final Lean corollaries exclude exactly the imported intervals
`[609,615]`, `[582,591]`, and `[560,569]`.  The last two gap theorems require
no uniqueness assumption for the increment-25 atom.

## Reproduction

Requires Git and the Lean toolchain selected by `lean-toolchain`.

```sh
lake update
lake build
python3 verify.py
```

Expected Lean result: exit status 0 and no `sorry`/`admit`.  The final lines
of the build print only the standard Mathlib axioms `propext`,
`Classical.choice`, and `Quot.sound` (some computational certificate lemmas
use only `propext`).

The Python checker uses only the standard library.  It verifies every local
Bellman inequality in `capacity_certificates.json`, independently enumerates
all attainable `(units, edges)` pairs at budgets 49 and 48, checks both gaps
and their sharp endpoints, and prints the certificate SHA-256.

## Theorem alignment and trust boundary

This project addresses only the finite arithmetic/block-spectrum bridge in
Discovery Net heights 2637 and 2671, downstream of the separator profiles
accepted at height 2699 from height 2569.

Imported and deliberately unformalized:

- Gallai's theorem that every block of the low-vertex induced subgraph of a
  critical graph is a complete graph or an odd cycle;
- extraction of a finite block list and the identity equating the sum of
  block increments with the low-vertex component order minus one;
- the upstream separator profiles, the forced `K_26` premise used in the
  height-2637 branch, and the row-specific degree/edge intervals;
- all graph drawing and crossing-number topology.

The Lean theorems expose the consequences of these imports as explicit
hypotheses on a finite set of atoms.  See `AUDIT.md` for the exact mapping.

## Versions

- Lean `v4.33.1`
- Mathlib tag `v4.33.1`, resolved exactly in `lake-manifest.json`
- Python 3 (standard library only)
