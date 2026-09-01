# Symbolic coefficient-stopping frontier

This artifact develops two exact consequences of the affine residue-cylinder
view of shortcut Collatz.

## 1. Downward closure of contracting cylinders

Suppose a length-`k` parity cylinder has least representative `r`, endpoint
`s`, and `q` odd steps. Its lifts obey

```text
r_t = r + 2^k t,
T^k(r_t) = s + 3^q t.
```

When `3^q<2^k`, non-descent at one lift is downward-closed:

```text
r_t <= T^k(r_t),  0 <= u <= t
    implies
r_u <= T^k(r_u).
```

In particular, every putative counterexample to Terras's coefficient
stopping-time conjecture reduces to the least positive representative of its
coefficient-first-crossing cylinder. A positive lift counterexample forces
strict growth at the base. Lean proves the algebraic base-forcing, strictness,
and downward-closure lemmas without `sorry`, `admit`, custom axioms,
`native_decide`, or Mathlib.

This also exposes a circular step in a 2025 claimed strong-induction proof of
the coefficient stopping-time conjecture; see
[`LITERATURE_AUDIT.md`](LITERATURE_AUDIT.md). The audit identifies a logical
gap and does not refute the conjecture.

## 2. Cap-maximizing first-crossing family

Let a coefficient-first-crossing word have `q` odd bits and length

```text
K = floor(q log_2(3)) + 1.
```

Coefficient safety at every proper prefix forces the `m`-th odd bit to occur
no later than position

```text
i_m^* = floor((m-1) log_2(3)),  1 <= m <= q.
```

Since the affine offset is

```text
C(w) = sum_m 2^(i_m) 3^(q-m),
```

the characteristic upper mechanical word of irrational slope `log_3(2)`, with
positions `i_m^*`, maximizes `C` and therefore the real non-descent cap
`C/(2^K-3^q)` among all such words. This is a Sturmian/mechanical extremizer;
at rational approximant blocks it is closely related to Christoffel words, but
it is not generally the fixed-slope Christoffel word of slope `q/K`.

The exact Python recurrence screens the least residue cylinder of this
cap-maximizing word for every first crossing through `K<=200,000`: 126,186
cases, of which 126,184 are nontrivial. Every nontrivial extremal base
descends. Independently written Ruby checks the crossings through
`K<=100,000`. Both implementations use exact integers and agree on a
canonical bounded-record SHA-256 at length 100,000:
`0385dd55507a4c689689f84a83b82ec5e5b483d83102d2b1304d8422d76ba660`.
The Python length-200,000 digest is
`109f7c9258d03bb58828fab74c494e27ccb9bf102befdf46c321c65fdf5ed25a`.

This complements the earlier fixed-slope Christoffel cylinder screen through
length 500 with a much deeper audit of the distinct coefficient-first-crossing
mechanical extremizer. It does **not** prove the coefficient stopping-time
conjecture: another word can have a smaller real cap but an unrelated 2-adic
residue. The result excludes the most tempting cap-only extremizer and further
isolates joint cap/residue control as the missing invariant.

## Reproduction

Tested with Python 3.12.12, Ruby 2.6.10, and Lean 4.33.1:

```bash
python3 verify_mechanical_first_crossing.py
python3 -m unittest -v test_symbolic_frontier.py
ruby verify_mechanical_first_crossing.rb 100000
lean lean/CollatzCSTCylinder.lean
```

## Primary sources and relation to prior work

- R. Terras, “A stopping time problem on the positive integers,” *Acta
  Arithmetica* 30 (1976), 241–252.
- L. E. Garner, “On the Collatz 3n+1 algorithm,” *Proceedings of the AMS* 82
  (1981), 19–22, DOI 10.1090/S0002-9939-1981-0603593-2.
- T. Laarhoven and B. de Weger, “The Collatz conjecture and De Bruijn graphs,”
  *Indagationes Mathematicae* 24 (2013), 971–983.
- O. Rozier and C. Terracol, “Paradoxical behavior in Collatz sequences,”
  *Discrete Mathematics* 349 (2026), 115167; arXiv:2502.00948v5.
- T. Niu, “Parity vectors and paradoxical sequences in the accelerated Collatz
  map,” arXiv:2605.13886. Niu already gives exact fixed-length endpoint counts;
  no novelty is claimed for that endpoint inequality.
- C. Fernández and S. Ibáñez, “Christoffel words as extremal structures in
  Collatz dynamics,” arXiv:2607.24844.
- L. Laurore, “On the Link Between Stopping Time and Non-Trivial Cycles in the
  Collatz Problem” (2025), DOI 10.4236/apm.2025.156018.
