# Exact Collatz parity-cylinder transport

This directory carries the symbolic affine-prefix program one step beyond a
raw depth-first residue tree.  A length-`k` parity word with `q` odd steps
determines one residue class modulo `2^k`.  Let `r` be its least nonnegative
representative and let `s=T^k(r)`.  Every nonnegative lift in the same cylinder
then obeys the exact transport law

```text
n_t = r + 2^k t,
T^k(n_t) = s + 3^q t.
```

Thus an infinite arithmetic progression of starts is represented by the four
integers `(r,s,2^k,3^q)` and one parameter `t`.  If the word is contracting,
`3^q < 2^k`, and the base endpoint does not descend, `r <= s`, then

```text
T^k(n_t) >= n_t
  iff (2^k - 3^q)t <= s-r,

t <= floor((s-r)/(2^k-3^q)).
```

This is the promised combination of the affine prefix formula with its exact
2-adic residue cylinder.  It is a compression theorem, not a proof that all
infinite compatible cylinders are impossible.

## Machine-checked theorem

[`lean/CollatzCylinderTransport.lean`](lean/CollatzCylinderTransport.lean)
defines realized shortcut-Collatz parity words and proves:

- `realizes_lift`: every start `r+2^k t` realizes the same word and ends at
  `s+3^q t`;
- `linearContractingLiftIff`: the general arithmetic endpoint equivalence;
- `contractingLiftIff`: its exact Collatz specialization; and
- `contractingLiftParameterBound`: the quotient bound on `t`; and
- `realizedContractingCylinder`: the packaged realization-and-bound theorem.

Lean 4.33.1 checks the file without Mathlib, `sorry`, `admit`, custom axioms, or
`native_decide`.  `#print axioms` reports Lean's standard `propext` and
`Quot.sound` only.

## Exact finite computations

The Python checker independently constructs the least cylinder representative

```text
r = -B * (3^q)^(-1) mod 2^k,
s = (3^q r+B)/2^k,
```

simulates the requested parity word, and checks the lift formula.  Its default
run exhausts every nonempty binary word through length 12 and lifts `t=0,...,5`.

It also tests a structural warning about optimizing only the real affine cap.
For every high-density contracting pair

```text
N/2 < q,  3^q < 2^N,  N <= 500,
```

the upper Christoffel word is the canonical maximizer of the prefix cap, and
the checker verifies exactly that

```text
least positive residue > C/(2^N-3^q).
```

Hence none of those 16,274 extremal words is realized by a positive integer
that is non-descending over the full block; every nonnegative cylinder lift is
still worse because the block is contracting.  A Ruby checker independently
recomputes the numerator from the Christoffel one-positions, uses a separate
extended-Euclidean modular inverse, and checks the same gap through length 300.

## Interpretation and novelty assessment

- **Theorem/formalization:** exact transport and the lift-parameter endpoint
  criterion are machine checked.
- **Verified computation:** the Christoffel realizability gap is finite, exact,
  and restricted to the displayed ranges.
- **Prior work:** parity-vector residue cylinders, the lift identity, and affine
  iterate formulas go back to the Terras/Everett framework; no novelty is
  claimed for them or for the elementary rearranged lift inequality.
  Fernández and Ibáñez (2026) prove the Christoffel extremal theorem for the
  cyclic numerator, Knight (2026) proves that nontrivial Christoffel high cycles
  cannot be entirely integral, and Rozier and Terracol (2025/2026) study the
  related finite paradoxical paths.
- **New reusable artifact and cautious finite finding:** the machine-checked
  packaging and independent finite screen expose a concrete mismatch between
  the real-valued extremizer and integer realizability.  The searched primary
  sources did not state this finite acyclic screen, but that negative search is
  not a priority proof.
- **Limitation:** the screen does not prove the gap for arbitrary lengths or
  arbitrary parity words.  Non-Christoffel words can be paradoxical; for
  example, the length-eight word `11101001` maps `7` to `8` despite
  `3^5 < 2^8`.

The main implication for the research program is methodological: maximizing
the affine offset or cap first and imposing congruence afterward can select an
arithmetically empty cylinder.  A viable symbolic proof must optimize the cap
and residue together, or aggregate cylinder states under block composition.

## Run

Tested with Python 3.12.12, Ruby 2.6.10, and Lean 4.33.1:

```bash
python3 verify_cylinder_transport.py
python3 -m unittest -v test_cylinder_transport.py
ruby verify_christoffel_gap.rb 300
lean lean/CollatzCylinderTransport.lean
```

The computational decisions use only exact integers and
`fractions.Fraction`; no floating-point arithmetic is used.

## Primary sources

Retrieved 2026-08-31:

- R. Terras, “A stopping time problem on the positive integers,” *Acta
  Arithmetica* 30 (1976), 241–252.
- R. Rozier and E. Terracol, “Paradoxical behavior in Collatz sequences,”
  arXiv:2502.00948. <https://arxiv.org/abs/2502.00948>
- K. Knight, “Collatz high cycles do not exist,” *Discrete Mathematics* 349(3)
  (2026), 114812. <https://doi.org/10.1016/j.disc.2025.114812>
- C. Fernández and S. Ibáñez, “Christoffel words as extremal structures in
  Collatz dynamics,” arXiv:2607.24844.
  <https://arxiv.org/abs/2607.24844>
