# Sixth-order `S` obstruction for QLP-42 `q=1`, `b=16`, case 5

## Theorem

Continue the coupled norm-32 QLP-42 shell in the `q=1`, `b=16` branch and
the canonical order-two compression case

```text
(p,q,x,y) = (4,1,2,-1).
```

The exact mod-7 compression, complete fourth-order Gaussian conditions, four
exact sum equations, and fifth-order `S` equations leave 11 reflected `B`
masks, 336 labeled pairs, and 16 `A`-rotation orbits. Requiring the
`S`-component equations modulo `(1+i)^6` eliminates all of them. Therefore
no QLP-42 pair in this `q=1`, `b=16`, case-5 shell exists.

This closes the case-5 branch without using the separate fifth-order `H`
obstruction.

## Sixth-order residue calculation

Put `pi=1+i`. Since `pi^6=-8i`, a Gaussian residual is divisible by `pi^6`
exactly when both coordinates vanish modulo 8. The primary checker instead
divides the already `pi^3`-divisible residual by `pi^3` and works in

```text
Z[i]/(pi^3)  ~=  Z/2 x Z/4,
z=r+si  |->  (r mod 2, r+s mod 4).                  (1)
```

The kernel of (1) is precisely `(pi^3)`, so the two tests are equivalent.

The exact sum `S_A=5-3i` forces five phase assignments per `A` support: one
entry is `1+i` and the other four are `1-i`. For every reflected `B` mask,
the exact sum `S_B=-3i` retains exactly 804,968 of the `256*2^17` phase
assignments. Thus the certificate checks 8,854,648 exact `B` assignments in
total.

For a fixed choice of the eight reflected-pair axes, every autocorrelation is
quadratic in the 17 sign bits. The C++ checker obtains the 17 linear and 136
quadratic coefficients from direct Gaussian evaluations and checks 16
additional global sign assignments. Across 256 axes and 11 masks this gives
475,904 direct interpolation/audit evaluations. An exact 8+9 sign join,
keyed by the Gaussian sum, enumerates all 804,968 admissible assignments and
stores their ten-shift sixth-order fingerprints. None matches any of the five
exact `A` targets for any of the 16 input orbits.

`independent_numpy_audit.py` then repeats the negative computation by a
different route. It enumerates all `2^17` sign vectors for every axis choice,
selects the exact sums directly, evaluates the periodic autocorrelations, and
compares their real and imaginary coordinates modulo 8. It does not use the
quotient representation (1), polynomial interpolation, or meet-in-the-middle
join. Both implementations agree on every classification, the 804,968 count,
and every per-mask reachable-fingerprint count in `orbit_table.tsv`.

Independent rotation of `A` preserves its exact sum and periodic
autocorrelation, so eliminating each representative eliminates all 21 labeled
rotations.

## Reproduction and trust boundary

Install NumPy and run:

```bash
python3 verify_b16_case5_sixth_s.py
```

The driver pins the preceding fifth-order certificate and both new
implementations by SHA-256, compiles the C++ checker with assertions enabled,
and reproduces `orbit_table.tsv` and `verification_output.txt` byte for byte.
All mathematical arithmetic is integral. Neither implementation uses random
proof steps, a solver, heuristic pruning, floating-point comparisons, or a
time limit. The implementations share only the checked-in predecessor table
and the stated support/phase conventions; their sixth-order representations
and enumeration strategies are independent.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Kotsireas--Koutschan--Winterhof,
*On properties of Legendre pairs under compression*,
<https://doi.org/10.1145/3747199.3747549>. A targeted primary-source and
committed-graph search found no matching sixth-order case-5 obstruction;
apparent novelty is relative to that search, not a historical-priority claim.

The strongest next step is to apply the same independently checked
sixth-order filter to exact-sum cases 0--4 in the `q=1`, `b=16` shell.
