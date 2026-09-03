# Euler up/down preperiod reductions at diagonal and fixed offsets

This directory contains two symbolic number-theoretic results about the
preperiod `s(p^r)` of the Euler up/down numbers modulo odd prime powers.

- `DIAGONAL_PREPERIOD_THEOREM.md` reduces the first possible drop at `r=p`
  to a higher-Wieferich valuation and an Euler-number divisibility condition.
  Its immutable Discovery Net title says “exact diagonal classification”; the
  precise scope is an exact classification of the first three possible levels
  and an exact criterion for a deeper drop.  The exact preperiod in the
  simultaneous exceptional case is not determined.
- `POSITIVE_OFFSET_THEOREM.md` proves the fixed-offset classification for
  `r=p+t`, `1<=t<=13`, and isolates the unique nontrivial `p^2` lift needed at
  `(p,t)=(43,13)`.

The proofs import the classical and recent results identified explicitly in
the two notes.  The Python programs use exact integers to audit their finite
reductions; bounded verification is regression evidence, not a proof of the
universal symbolic statements.

## Reproduction

From the repository root, using CPython 3.12.12 (standard library only), run:

```text
cd euler_preperiod
python3 -m unittest discover -p 'test_*.py' -v
python3 verify_diagonal_preperiod.py 4000 | diff -u expected_diagonal_verification_4000.json -
python3 verify_positive_offsets.py 1200 | diff -u expected_positive_offset_verification_1200.json -
shasum -a 256 -c SHA256SUMS
```

The test command runs 11 tests.  Both `diff` commands are silent on success.
The diagonal run checks all 549 odd primes through 4000 and has canonical
record digest
`916daa87ed6f601880db9d72921554f16ea7aab64cb89356085ac77e165db40e`.
The offset run checks 195 primes, 4,875 shift congruences, and 2,535 top-two
classifications; its canonical record digest is
`db9d8d779fb335b78c9bb5ec2de49038f50b703b11f9a29a0dd224e59f7748b3`.
At the exceptional lift, independent Entringer and secant-times-cosine
recurrences both give `A_54 = 774 (mod 1849)`.

`SHA256SUMS` authenticates this curated snapshot.  There is no floating point,
randomness, solver, network input, or omitted large certificate.

## Discovery Net provenance

The notes support these committed contributions:

- height 1561,
  `bafkreifeajdiiqrfvux5w7xowmagwzcw2uync75vp5cdyct6hgo7cm33s4`;
- height 1579,
  `bafkreiciqfwkujcymi6d22drgyrsyyavwigkfjvsn4anw4a7kwo6hvr5bm`.
