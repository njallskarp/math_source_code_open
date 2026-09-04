# Cycle-power packing transfer theorem

This directory proves that, for every fixed cycle power `r` and packing
palette `{1,...,k}`, the number of admissible cyclic words of length `L>r*k`
is exactly `trace(A^L)` for an explicit finite zero-one transfer matrix.
Consequently its tail generating function is rational, and the feasible
lengths are eventually a finite union of divisibility classes.

The specialization `T(C_n) = C_(2n)^2` gives the same conclusions for
packing-total colorings of cycles with any fixed palette size.  This is a
general structural theorem; it deliberately does not duplicate the previously
reviewed exact eight-colour semigroup computation.

## Reproduce

Run from this directory:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_transfer.py
    diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_transfer.py)
    shasum -a 256 -c SHA256SUMS

The verifier uses only Python's standard library and exact integer and tuple
operations.  It compares direct cyclic-word enumeration with the trace/closed-
walk count in 21 small cases, verifies the cycle-power distance formula in 117
parameter cases, and checks the total-cycle specialization directly.  The
universal trace, rationality, recurrence, and eventual-divisibility statements
are proved symbolically in `THEOREM.md`.

## Context and scope

The motivating primary source is Jasmina Ferme and Daša Mesarič Štesl,
*On packing total coloring*, arXiv:2508.08691v2 (2026):

https://arxiv.org/abs/2508.08691

The independent Discovery Net review of the exact eight-colour cycle result
explicitly proposed a general automata theorem for packing colorings of cycle
powers and identified the rigorous eventual closed-walk-length classification
as the missing bridge.  The theorem here supplies that bridge.  Transfer
matrices and finite-digraph period theory are classical; no novelty is claimed
for those tools in isolation.
