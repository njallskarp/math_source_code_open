# Lean certificate for `30 ∈ ML(3,4)`

This Lean 4 project proves that an order-four maximal partial Latin cube with
30 entries exists.  It formalizes the graph-theoretic bridge and checks the
complete 30-word witness inside Lean's ordinary kernel.

An entry is a word in `(Fin 4)^4`, interpreted as
`(layer, row, column, symbol)`.  Distinct entries are compatible exactly when
their Hamming distance is at least two.  Maximality means that every one of
the 256 words is at distance at most one from a selected entry.

The endpoint theorem is:

```lean
theorem thirty_mem_orderFourSpectrum : InOrderFourSpectrum 30
```

Here `InOrderFourSpectrum k` is the existence of a duplicate-free list of
`k` entries whose underlying set is a maximal partial Latin cube.  Thus the
theorem is the formal statement `30 ∈ ML(3,4)` under the standard coordinate
encoding.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`.

```sh
lake update
lake exe cache get
lake clean
lake build MPLCOrder4
lake env lean MPLCOrder4.lean
```

Expected build conclusion:

```text
Build completed successfully
```

The final command prints the axiom audits.  All exported theorems use only a
subset of `propext`, `Classical.choice`, and `Quot.sound`.

## Theorem map

- `hammingGraph` is an actual Mathlib `SimpleGraph Word4`, with adjacency at
  Hamming distance one.
- `isPartialLatinCube_iff_isIndepSet` proves that coordinate compatibility is
  exactly independence in `H(4,4)`.
- `isMaximalPartialLatinCube_iff_independentDominating` proves the standard
  independent-dominating-set formulation.
- `isMaximalPartialLatinCube_iff_no_addable` proves that the closed-neighborhood
  condition is exactly the literal statement that no absent word can be added.
- `partialCheck_eq_true_iff` and `coverCheck_eq_true_iff` prove that the two
  Boolean checks reflect the mathematical predicates.
- `certificate30_length`, `certificate30_nodup`, and
  `certificate30_checks` kernel-check the embedded witness.
- `certificate30_isMaximal`, `certificate30_independentDominating`,
  `certificate30_no_addable`, and `thirty_mem_orderFourSpectrum` assemble the
  mathematical conclusions.

The computation uses `by decide`, not `native_decide`.  The 30 words and all
256 ambient words reduce in Lean; there is no imported parser, SAT proof, or
external certificate oracle.

## Alignment, provenance, and scope

Britz--Cavenagh--Sørensen define a partial Latin cube of order `n` as a subset
of `[n]^4` in which distinct entries agree in at most two coordinates, and
define maximality by impossibility of adding another entry.  Their 2015
Theorem 11 left membership of 28, 29, and 30 in `ML(3,4)` open.  The 2024
paper of Donovan--Grannell--Yazıcı gives the equivalent independent
dominating set and covering-code formulations and records the equality
`f(3,4)=28` as already known from coding-theoretic computation.

This project formalizes only the reviewed 30-entry positive witness.  It does
not claim novelty for 28, does not prove the published exclusion below 28,
and does not decide whether `29 ∈ ML(3,4)`.

The embedded list is the size-30 certificate independently reviewed in
Discovery Net.  Its canonical selected-word SHA-256 is
`aaeef4b34fc12ef5fcebeac6f1b46c072ec6260dc57c254e18d3dfc3f6c7f073`.
The SAT search used to discover it is outside the correctness boundary.

Discovery Net references:

- problem, height 1693:
  `bafkreigglwsodqfc45gh7agvxlhqb5donaiv3ci54ocikbxppaal43fkdu`;
- 28/30 witness lemma, height 1695:
  `bafkreidvbmvrdra3ab4qpsior57uarvyqyla32pbkuaieqqmhiuwv2apsy`;
- independent review and novelty correction, height 1699:
  `bafkreifpx2f6jthxi2e3hvcasdixo2zzmxjivcu6excfegocppn254g3au`.

Primary literature:

- T. Britz, N. J. Cavenagh, and H. K. Sørensen, *Maximal Partial Latin
  Cubes*, Electronic Journal of Combinatorics 22(1), P1.81 (2015),
  <https://doi.org/10.37236/4726>.
- D. M. Donovan, M. J. Grannell, and E. Ş. Yazıcı, *On maximal partial Latin
  hypercubes*, Designs, Codes and Cryptography 92, 419--433 (2024),
  <https://doi.org/10.1007/s10623-023-01314-5>.

## Trust boundary

The universal graph/coordinate equivalences and the concrete 30-entry
membership theorem are checked by Lean with the pinned Mathlib dependency.
The remaining trust base is Lean, Mathlib, the compiler/toolchain, and ordinary
hardware.  The literature claims and historical status are not formalized.
No floating point, randomness, network input, solver result, generated code,
custom axiom, `sorry`, `admit`, `unsafe` declaration, or `native_decide` occurs
in the proof.
