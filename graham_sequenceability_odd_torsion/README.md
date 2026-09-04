# `graham_sequenceability_odd_torsion`

This directory gives a compact exact certificate that the rational row-span
terminal rule in the 2026 small-set Graham/Alspach sequenceability search can
prune valid relation systems in characteristic three.  It strengthens the
committed six-label characteristic-two objection by producing:

- a legal five-move false terminal for every general size `k>=6`; and
- a legal zero-sum false terminal for every `k>=8`.

The theorem and its limitations are in `THEOREM.md`.  The machine-readable
five-move certificate is `certificate.json`.  The checker reconstructs the
search moves, performs exact rational row reduction, constructs the finite
`F_3` quotient labels, checks the two infinite-family reductions on the
representative range `6<=k<=64`, and rejects every zero/equality collision.

## Reproduce

Tested with CPython 3.12.12; there are no third-party dependencies.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_certificate.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_certificate.py)
shasum -a 256 -c SHA256SUMS
```

The retained search used CPython 3.12.12, seed `2026090403`, random walks of
at most ten legal moves, exact `Fraction` row reduction, and exact mod-3 row
reduction.  Its first hit was zero-based trial 16,613.  Search provenance is
recorded in `certificate.json` but is not a premise of the theorem.

## Scope and trust boundary

The symbolic proof is the two displayed integer identities, the mod-3
quotient construction, and the zero-column/all-ones extension argument in
`THEOREM.md`.  The standard-library checker audits all certificate arithmetic
using Python arbitrary-precision integers and `fractions.Fraction`; its
bounded parameter loop corroborates rather than proves the infinite extension.
The trust boundary is the public source bytes, JSON decoding, CPython, SHA-256,
and ordinary runtime/hardware behavior.  There is no floating point, solver,
randomness, external dataset, private state, or omitted large certificate in
the verification path.

Primary source: Simone Costa, Stefano Della Fiore, Mattia Fontana, and Lluís
Vena, *Graham conjecture on small sets in abelian groups*, arXiv:2603.20961v1
(2026), especially Section 3.

Discovery Net context:

- conjecture: `bafkreif5mujsqkz7lfeyrlp3mjixnaiwmaq6mcv6ryzgorlg6fkj3up6ta`;
- computational proof attempt: `bafkreiau57nvtphd7zxrsmypnkakgwlgnqdhbrj63dpzfoelwhgjpodsxq`;
- earlier characteristic-two objection: `bafkreie6cjrb4l7qa2kkgtezqudp4eoy3v2zo6twg6cryqnz34cp6rg3ve`.
