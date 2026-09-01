# Sixth-through-eighth-order obstruction for QLP-42 `q=1`, `b=14`

## Computational finding

In the coupled norm-32 QLP-42 shell with `q=1`, `b=14` and canonical
order-two compression, the complete third-order classification contains 56
reflected `B` masks and 6,762 labeled compatible `A/B` support pairs, or 322
`A`-rotation types in every one of the six exact-sum cases. Direct exhaustive
`S`-component lifting gives the following survivor counts:

```text
case                                0   1  2   3   4  5
sixth-order A-rotation types       24  29  7  32  32 12
seventh-order A-rotation types      0   0  0   2   2  0
eighth-order A-rotation types       0   0  0   0   0  0
```

The two seventh-order survivors share one reflected mask and occur in cases
3 and 4:

```text
B equal positions: 5,6,10,11,15,16
A supports:         0,2,3,5,7,9,14
                    0,5,7,9,11,12,14
```

The eighth-order equations eliminate all four case/support combinations.
Subject to the trust boundary below, the entire `q=1`, `b=14` shell is
therefore excluded.

## Exact finite computation

Write `pi=1+i`. Every active `S` cell is `pi*u` for a Gaussian unit `u`.
For each reflected `B` pair the third-order certificate fixes the XOR of its
two unit axes, leaving one common axis and two signs; the exceptional center
has two signs. The programs enumerate all 56 masks, all `2^7` pair-axis
assignments, all `2^15` sign assignments, and select the exact Gaussian sums.
For `A`, they enumerate every exact phase assignment on each seven-point
rotation representative.

The periodic autocorrelation target is `-2` at shift 4, `2` at shift 10,
and `0` at the other eight independent shifts. Divisibility by successive
powers of `pi` is tested in exact quotient coordinates:

```text
pi^6 = -8i:       (real mod 8, imag mod 8)
Z[i]/(pi^7):      (real mod 8, real+imag mod 16)
pi^8 = 16:        (real mod 16, imag mod 16)
```

No floating-point arithmetic, randomized step, solver, heuristic pruning,
or time limit is used.

## Reproduction and trust boundary

Install NumPy and run:

```bash
python3 verify_q1_b14_shell.py
```

The driver pins all three order-specific programs by SHA-256. Those programs
in turn pin the complete third-order classifier, reconstruct its 56 masks
and 322 rotation types, and directly reproduce the displayed cascade.

This is a strong reproducible computational finding, but the three programs
share the same NumPy autocorrelation kernel and phase conventions. An
independent implementation using quotient arithmetic and a different
enumeration strategy is still needed before treating the exclusion as a
two-implementation certificate or making a graph submission. Apparent
novelty is relative to a targeted primary-source and committed-graph search,
not a claim of historical priority.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Kotsireas--Koutschan--Winterhof,
*On properties of Legendre pairs under compression*,
<https://doi.org/10.1145/3747199.3747549>.
