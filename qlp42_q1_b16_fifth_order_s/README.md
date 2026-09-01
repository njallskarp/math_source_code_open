# Fifth-order `S`-component filter for QLP-42 `q=1`, `b=16`, case 5

## Theorem

Continue the coupled norm-32 QLP-42 shell in the `q=1`, `b=16` branch and
the canonical order-two compression case

```text
(p,q,x,y) = (4,1,2,-1).                              (1)
```

The exact mod-7 compression, complete fourth-order Gaussian conditions, and
four exact sum equations leave

```text
18 reflected B masks, 588 labeled A/B type pairs,
28 A-rotation orbits.                                 (2)
```

Requiring only the `S`-component autocorrelation equations modulo
`(1+i)^5`, while retaining the exact `S_A` and `S_B` sums, eliminates

```text
 7 B masks, 252 labeled pairs, 12 A-rotation orbits,
```

and leaves at most

```text
11 B masks, 336 labeled pairs, 16 A-rotation orbits.   (3)
```

This is a necessary one-component filter. It is already strict without the
`H` fifth-order equations, so every eliminated orbit is impossible in the
full case-5 branch. The 16 survivors are not claimed to lift through `H` or
to satisfy the integral autocorrelation equations.

Every input and output orbit, together with the number of reachable
fifth-order B-residue fingerprints, is recorded in `orbit_table.tsv`.

## Fifth-order residue algebra

Put `pi=1+i`. The third-order type theorem makes each combined
autocorrelation residual divisible by `pi^3`. Such a residual is divisible
by `pi^5` exactly when both Gaussian coordinates of its quotient by `pi^3`
are even. Thus every shift contributes a two-bit residue rather than the
single coordinate-sum bit used at fourth order.

The local fifth-order functions are quadratic over `F_2`, but become affine
in all sign bits once the unit axes are fixed. Explicitly, let `a,b` be the
axes and `s,t` the signs of two diagonal entries. For

```text
D(a,b,s,t) = 2*(-1)^(s+t)*i^(a-b),
```

the real and imaginary parities of `(D-D(0,0,0,0))/pi^3` are

```text
a + a*b + s + t,       b + a*b + s + t.             (4)
```

For a center-cross pair, let `a` be the common reflected-pair axis, `p,m`
the two neighbor signs, `z` the center sign, `c` the center axis, and
`theta` the fixed reflected-axis XOR. Put

```text
L = a + a*p + a*m + z + a*c + p*c + m*c
      + a*theta + m*theta + z*theta.
```

The corresponding two coordinate parities are

```text
L+p,       L+m.                                      (5)
```

Equations (4) and (5) show both completeness of the quadratic model and the
absence of sign-sign products. The verifier checks all 16 diagonal and all
64 center-cross assignments directly in `Z[i]`.

## Complete case-5 enumeration

In case 5 the exact sums are

```text
sum(S_A) = 5-3i,       sum(S_B) = -3i.               (6)
```

The five active entries of `S_A` belong to `pi*mu_4`. Equation (6) forces
exactly one entry to be `1+i` and the other four to be `1-i`. Hence every A
support has exactly five admissible phase assignments.

For each reflected B mask, the eight active reflected pairs have 256 common
axis assignments. Their 16 diagonal signs and the exceptional center sign
give 17 sign bits. Exhaustive meet-in-the-middle enumeration of the exact
`S_B` sum retains exactly

```text
804,968 phase assignments per B mask,
14,489,424 assignments across all 18 masks.          (7)
```

For each common-axis assignment, (4)-(5) make the 20-bit fifth-order residue
affine in those signs. The checker enumerates all exact-sum sign halves,
joins complementary Gaussian sums, and stores every reachable B residue.
It then tests the five exact A assignments against the combined baseline.
This is exhaustive: the common axes, all individual signs, both center
orientations, and every exact-sum join are covered.

Independent rotation of A preserves its sum and periodic autocorrelation,
so each tested representative certifies its full 21-element rotation orbit.

## Reproduction and trust boundary

Run:

```bash
python3 verify_b16_case5_fifth_s.py
```

The standard-library verifier:

- pins the preceding fourth-order verifier, exact-sum verifier, and excluded
  case-5 orbit table by SHA-256;
- reconstructs the 28 input orbits from the earlier certificates;
- exhaustively verifies the 80 local fifth-order formulas;
- performs 4,608 direct global sign-affinity audits, one for every common-axis
  assignment of every B mask;
- enumerates all 14,489,424 exact B phase assignments in (7);
- checks every orbit classification and all aggregate counts against the
  checked-in output files.

All arithmetic is exact in `Z[i]` and `F_2`. No floating point, heuristic
search, random proof step, SAT/SMT result, or time-limited status enters the
certificate. The new enumeration has one implementation; its local algebra
and representative global sign maps are directly audited, but an independent
reimplementation would further reduce implementation risk.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Kotsireas--Koutschan--Winterhof,
*On properties of Legendre pairs under compression*,
<https://doi.org/10.1145/3747199.3747549>. A targeted primary-source and
committed-graph search found no matching fifth-order case-5 classification;
apparent novelty is relative to that search, not a historical-priority
claim.

The strongest next step is to impose the exact `H_A,H_B` sums and fifth-order
`H` residues on the 16 surviving orbits.
