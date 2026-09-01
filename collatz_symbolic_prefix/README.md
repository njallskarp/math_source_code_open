# Symbolic affine-prefix obstruction for Collatz trajectories

This directory records one symbolic iteration away from depth-first residue
enumeration.  It studies what a hypothetical positive Collatz trajectory that
never drops below its starting value must satisfy.

The shortcut map is

```text
T(n) = n/2          when n is even,
T(n) = (3n+1)/2     when n is odd.
```

For a length-`k` parity word `e_0,...,e_{k-1}`, let `q_j` be the number of odd
bits in its first `j` positions and define

```text
B_0 = 0,
B_{j+1} = 3^(e_j) B_j + e_j 2^j.
```

Every realized prefix has the exact affine form

```text
2^j T^j(n) = 3^(q_j) n + B_j.
```

Consequently, if `T^j(n) >= n` and `3^(q_j) < 2^j`, then

```text
(2^j - 3^(q_j)) n <= B_j,
n <= floor(B_j / (2^j - 3^(q_j))).
```

A least positive counterexample to reaching `1`, if one exists, can never
descend below its start: a smaller iterate would reach `1` by minimality and so
the starting value would also reach `1`.  Thus every contracting prefix of its
parity word must satisfy the displayed inequality.  This replaces a search
tree by an infinite family of exact symbolic constraints.  It does **not** by
itself prove that those constraints are inconsistent.

## Machine-checked result

[`lean/CollatzSymbolicPrefix.lean`](lean/CollatzSymbolicPrefix.lean) proves:

- composition of the locally defined iterate;
- the least-counterexample no-descent lemma;
- the affine identity for a recursively realized parity word;
- the cross-multiplied and quotient prefix bounds; and
- their application to every contracting prefix of a least counterexample.

The formalization uses Lean 4.33.1 with no Mathlib, `sorry`, `admit`, custom
axioms, or `native_decide`.  `#print axioms` reports only Lean's standard
`propext` for the five principal theorems.

## Exact experiment and a useful non-novelty result

For a contracting word `w`, define its prefix cap

```text
M(w) = min_{j: 3^(q_j) < 2^j} B_j/(2^j - 3^(q_j)).
```

The exact checker exhausts every fixed-length/fixed-weight word through length
16.  In every contracting parameter pair, the unique maximizer of `M` is the
upper mechanical (Christoffel) word.  It also checks, through length 12, the
rotation bridge

```text
max_rotation M(rotation(w))
  = min_rotation B(rotation(w)) / (2^k - 3^q).
```

This computation is **not claimed as a new extremal theorem**.  Fernández and
Ibáñez (2026) prove that Christoffel words uniquely maximize the cyclic minimum
of the Collatz offset at fixed length and weight.  The rotation bridge makes
the observed prefix-cap optimization a direct reformulation of their theorem.
Recording this overlap prevents a duplicate novelty claim and isolates what
must change for further progress: acyclic prefixwise constraints and integer
realizability, rather than another cyclic offset optimization.

## Run

Tested with Python 3.12.12 (standard library only) and Lean 4.33.1:

```bash
python3 verify_symbolic_prefix.py --max-length 16 --rotation-check-length 12
python3 -m unittest -v test_symbolic_prefix.py
lean lean/CollatzSymbolicPrefix.lean
```

All mathematical comparisons in the Python checker use integers or
`fractions.Fraction`; no floating-point comparison enters a decision.

## Status, novelty, and trust boundary

- **Theorem/formalization:** the exact affine identity and minimal-counterexample
  prefix obstruction are checked by Lean.
- **Verified computation:** exhaustive fixed-length/fixed-weight checks are
  exact only through the stated finite lengths.
- **Prior-work overlap:** the finite extremizer pattern is subsumed by the 2026
  Christoffel-word theorem after the rotation bridge.  No novelty is claimed
  for that pattern or for the classical affine iterate formula.
- **New reusable artifact:** the contribution is a compact machine-checked
  bridge from minimal-counterexample logic to all contracting affine prefixes,
  together with a reproducible negative novelty assessment of the first
  optimization attempted.
- **Limitation:** nothing here excludes an infinite realizable word whose every
  contracting prefix cap remains above its starting integer.  The formalization
  also takes the link between an abstract iterate and a `Realizes` word as a
  hypothesis rather than defining a total Collatz function and extracting its
  parity word automatically.

The next target is to combine the cap inequalities with the exact 2-adic
cylinder congruence selecting the starting integer modulo `2^k`.  The desired
symbolic result would rule out an infinite compatible system directly, perhaps
via blocks, automata, or a proof-producing arithmetic solver, instead of
enumerating the residue tree one depth at a time.

## Primary sources

Retrieved 2026-08-31:

- T. Tao, “Almost all orbits of the Collatz map attain almost bounded values,”
  arXiv:1909.03562. <https://arxiv.org/abs/1909.03562>
- R. Rozier and E. Terracol, “Paradoxical behavior in Collatz sequences,”
  arXiv:2502.00948. <https://arxiv.org/abs/2502.00948>
- K. Niu, “Parity vectors and paradoxical sequences in the Collatz dynamics,”
  arXiv:2605.13886. <https://arxiv.org/abs/2605.13886>
- Á. Fernández and P. A. Ibáñez, “Christoffel words as extremal structures in
  Collatz dynamics,” arXiv:2607.24844. <https://arxiv.org/abs/2607.24844>
