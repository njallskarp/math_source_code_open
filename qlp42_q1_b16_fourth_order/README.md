# Fourth-order Gaussian filter for the QLP-42 `q=1`, `b=16` row

## Theorem

Continue the coupled norm-32 QLP-42 shell in the `q=1`, `b=16` branch.
The preceding exact mod-7 `H`-compression filter leaves

```text
18 reflected B masks, 756 labeled A/B type pairs,
36 A-rotation orbits.
```

Requiring the complete autocorrelation lift modulo `(1+i)^4` eliminates
exactly

```text
84 labeled type pairs in four complete A-rotation orbits,
```

and leaves

```text
18 reflected B masks, 672 labeled type pairs,
32 A-rotation orbits.                                      (1)
```

Thus the fourth-order layer removes two of the three surviving `A` orbits
over each of two `B` masks, but neither `B` mask disappears completely.
Together with the preceding `b=16`, `b=18`, and `b=20` filters, the running
global upper bounds improve to

```text
470 B masks, 193,473 labeled pairs, 9,213 A-rotation orbits.
```

## Complete fourth-order phase system

Put `pi=1+i`. At a non-quarter cell the active transformed component is
`pi*u`, where `u` is a Gaussian unit. The third-order theorem fixes, for
each reflected active pair of `B`, the XOR `theta_s` of its two unit-axis
bits. A complete phase assignment through that layer is therefore
parameterized by

```text
21 arbitrary A-axis bits,
10 common B reflected-pair axis bits,
20 individual B sign bits,
 2 independent signs at the exceptional B center.         (2)
```

The 21 signs of the active `A` entries are also free, but changing any of
them affects the original autocorrelation only by a multiple of `pi^4`, so
they are invisible in this layer.

For each component `K` in `{S,H}` and each shift `1<=s<=10`, let

```text
R_K(s) = PAF(K_A,s) + PAF(K_B,s) - target_K(s).
```

The third-order conditions say `pi^3` divides all 20 residuals. Define the
fourth-order obstruction vector

```text
r = (R_K(s)/pi^3 mod pi)_(K,s) in F_2^20.                 (3)
```

As the 53 variables in (2) change, (3) is an affine binary map. The checker
constructs its columns by direct exact Gaussian autocorrelation differences.
A type pair lifts modulo `pi^4` exactly when its baseline vector belongs to
the column span.

The rank and consistency strata are:

| rank | consistent? | labeled pairs | A-rotation orbits |
|---:|:---:|---:|---:|
| 18 | yes | 147 | 7 |
| 19 | yes | 105 | 5 |
| 19 | no  | 84  | 4 |
| 20 | yes | 420 | 20 |

The four excluded orbits and all 32 survivors are listed explicitly in
`orbit_table.tsv` by the four equal positions of `B` and a five-position
representative of the opposite support of `A`.

## Why the map is affine and complete

For two diagonal entries, the autocorrelation term is

```text
(pi*u) conjugate(pi*v) = 2*u*conjugate(v).
```

Modulo `pi^4`, its variation depends linearly only on the two unit axes;
both signs disappear. At the exceptional center, a shift has the two cross
terms

```text
c*conjugate(pi*u_+) + pi*u_-*conjugate(c).
```

The fixed third-order XOR of the axes of `u_+` and `u_-` makes the remaining
`pi^3` coefficient affine in the common pair axis, the two neighbor signs,
and the center sign. The verifier exhausts all 80 local assignments covering
both center axes and both values of `theta`, proving these claims directly
in `Z[i]`.

Every global third-order phase assignment occurs in (2): the common pair
axis realizes every pair with the prescribed XOR, the two signs are free,
and the two center signs generate all four oriented quarter states. Hence
the span-membership test is the complete fourth-order residue condition,
not only a selected family of lifts.

## Reproduction and trust boundary

Run:

```bash
python3 verify_b16_fourth_order.py
```

The standard-library checker:

- pins the prior mod-7 verifier to SHA-256
  `109e66dec98a02afef5ed017ca5d579dd18daca5ebd5765de43f647cd41bc5ab`;
- reconstructs its 756 labeled survivors and 36 complete rotation orbits;
- performs the 80 exhaustive local affinity checks described above;
- constructs every `20 x 53` binary system using direct exact length-21
  Gaussian autocorrelations;
- checks one deterministic full 53-bit assignment against the affine
  prediction for each of the 756 type pairs;
- verifies every row of `orbit_table.tsv` and all displayed counts.

The deterministic assignment checks audit formulas already proved by the
exhaustive local calculation; they are not probabilistic proof steps. The
pinned dependency was independently implemented in Python and C++20. No
floating point, SAT/SMT status, heuristic search, or assumed phase lift
enters the result.

This theorem concerns autocorrelations modulo `(1+i)^4`. It does not impose
the full exact Gaussian sums on the same phase assignment or the full
integer autocorrelation equations, so the 672 survivors are not claimed to
be QLP-42 solutions. The next useful layer is to intersect each affine
kernel with the exact four global sums before lifting to `(1+i)^5`.

Primary context: Djokovic--Kotsireas, *Compression of Periodic Complementary
Sequences and Applications*, <https://arxiv.org/abs/1302.0571>;
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; and Jedwab--Pender,
*Two constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>. A targeted primary-source and current
graph search found no matching `q=1`, `b=16` fourth-order classification;
apparent novelty is relative to that search, not a priority claim.
