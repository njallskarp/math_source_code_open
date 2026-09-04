# Full-feedback directional localization in random graphs

This directory contains a self-contained theorem suite showing that, in a
broad Erdos--Renyi regime, every vertex is with high probability a winning
one-round probe for the full-feedback directional localization game.  It also
contains a deterministic degree--maximum-codegree criterion that forces the
same conclusion, a quasirandom corollary, and a diameter-two obstruction.

## Reproduce

From this directory, run:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_random_graph_certificate.py
    diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_random_graph_certificate.py)
    PYTHONDONTWRITEBYTECODE=1 python3 verify_codegree_obstruction.py
    diff -u EXPECTED_CODEGREE_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_codegree_obstruction.py)
    shasum -a 256 -c SHA256SUMS

The verifier uses only Python's standard library and exact integer/rational
arithmetic.  It exhausts every labelled simple graph through six vertices for
the deterministic implication, checks the coefficient law against direct
weighted enumeration at three rational probabilities, and checks the explicit
union bound.  The second verifier exhausts the local and global codegree
criteria through six vertices, checks the Petersen-complement equality case,
and audits a family showing that diameter two does not imply simultaneous
two-probe resolution.  These finite audits validate the implementation and
displayed identities; the theorems themselves are proved symbolically in
`THEOREM.md` and `CODEGREE_OBSTRUCTION.md`.

## Primary source and scope

The motivating primary source is John Jones and William B. Kinnersley,
*The directional localization game on graphs*, arXiv:2609.01745v1 (2026),
Question 6.4.  The result here constrains possible examples with
`zeta_d^*>2`; it does not resolve their existence.
