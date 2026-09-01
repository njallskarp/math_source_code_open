# Sixth/seventh-order S frontier for QLP-42 `q=1`, `b=12`

## Computational finding

In the coupled norm-32 QLP-42 shell with `q=1`, `b=12` and canonical
order-two compression, the complete third-order classification contains 98
reflected `B` masks and 76,377 labeled compatible `A/B` support pairs, or
3,637 `A`-rotation types in each of the six exact-sum cases. Direct exhaustive
`S`-component lifting gives:

```text
case                                0     1     2    3    4   5
sixth-order A-rotation types      1686  1398  1427  850  850 304
seventh-order A-rotation types     303   180    92    5    5   0
seventh-order B masks               29    27    20    3    3   0
```

Across cases, 2,523 distinct mask/support rows survive sixth order and only
499 survive seventh order. In particular, the exact-sum case 5 branch is
excluded by the seventh-order `S` equations alone. This is a strict
intermediate reduction, not an exclusion of the complete `b=12` row.

## Exact finite computation

Write `pi=1+i`. Every active `S` cell is `pi*u` for a Gaussian unit `u`.
For each reflected `B` pair the third-order certificate fixes the XOR of its
two unit axes, leaving one common axis and two signs; the exceptional center
has two signs. The programs reconstruct all 98 masks and all weight-nine
cyclic support representatives, enumerate every exact phase assignment, and
impose the periodic-autocorrelation target `-2` at shift 4, `2` at shift 10,
and `0` at the other eight independent shifts.

Sixth order is checked coordinatewise modulo 8 because `pi^6=-8i`.
Seventh order uses the exact quotient representation

```text
Z[i]/(pi^7) -> Z/8 x Z/16,
r+si         -> (r mod 8, r+s mod 16).
```

All arithmetic is integral. No floating point, randomized step, solver,
heuristic pruning, or time limit is used.

## Reproduction and trust boundary

Install NumPy and run:

```bash
python3 verify_q1_b12_frontier.py
```

The driver pins both programs by SHA-256. They pin the preceding third-order
classifier, reconstruct the 98 masks, 2,802 unique support-orbit
representatives and 3,637 mask/support orbit types, and reproduce every
displayed count.

This result currently has one direct NumPy implementation. An independent
quotient-arithmetic implementation is required before promoting it to a
two-implementation graph theorem. The strongest next computation is the
eighth-order `S` lift of the 499-row seventh-order frontier, beginning with
the ten case-3/4 orbit incidences on six masks. Apparent novelty is relative
to a targeted primary-source and committed-graph search, not a claim of
historical priority.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; and Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>.
