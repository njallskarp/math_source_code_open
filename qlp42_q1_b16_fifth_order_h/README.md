# Fifth-order `H`-component filter for QLP-42 `q=1`, `b=16`, case 5

## Theorem

Continue the coupled norm-32 QLP-42 shell in the `q=1`, `b=16` branch and
the canonical order-two compression case

```text
(p,q,x,y) = (4,1,2,-1).
```

The exact mod-7 compression, complete fourth-order Gaussian conditions, four
exact sum equations, and fifth-order `S` equations leave 11 reflected `B`
masks, 336 labeled pairs, and 16 `A`-rotation orbits. Requiring in addition
the `H`-component autocorrelation equations modulo `(1+i)^5`, with the exact
`H_A,H_B` sums, eliminates exactly one full orbit:

```text
B equal positions:                  6,9,12,15
A opposite orbit representative:    0,3,6,12,15
fourth-order rank:                  19
```

It therefore leaves at most

```text
10 B masks, 315 labeled pairs, 15 A-rotation orbits.
```

This is a strict necessary filter, not an integral construction or a
nonexistence result for the remaining orbits.

## Exact phase enumeration

The 16 active entries of `H_A` lie in `pi*mu_4`, where `pi=1+i`, and have
exact sum zero. Write an entry as `pi*(-1)^s*i^a`. The two Gaussian sum
coordinates vanish exactly when the signed sums in each of the axis classes
`a=0` and `a=1` vanish separately. Thus each class has even size and half of
its signs are negative. The complete number of exact-sum phase assignments
per `A` support is

```text
sum over even n of C(16,n) C(n,n/2) C(16-n,(16-n)/2)
  = 165,636,900.
```

Only two reflected pairs and the real center are active in `H_B`. Direct
enumeration of all `8*8*2=128` local assignments leaves exactly 20 with
`sum(H_B)=1`, forming 10 distinct fifth-order residue fingerprints for each
of the 11 input masks.

## Complete fifth-order search

Every shift supplies the real and imaginary parity of the combined
autocorrelation residual divided by `pi^3`, hence a 20-bit fifth-order
fingerprint. For two diagonal entries with axes `a,b` and signs `s,t`, the
two local parities relative to the all-zero choice are

```text
a + a*b + s + t,       b + a*b + s + t.
```

The analogous center-cross formula is checked for all 64 local assignments.
Consequently the global fingerprint is quadratic in the 16 axis and 16 sign
bits and has no sign-sign monomials. For every orbit the checker obtains all
32 linear and 496 quadratic coefficients from direct Gaussian arithmetic,
checks 16 further global assignments, and verifies the vanishing of all 120
sign-sign coefficients.

The search then enumerates all 32,768 even axis patterns. For each pattern,
the remaining sign dependence is affine. An exact 8+8 meet-in-the-middle
join is keyed simultaneously by the two required sign cardinalities and the
20-bit residue. This covers all 165,636,900 exact `A` assignments without
heuristic pruning. The rejected orbit exhausts all 32,768 axis patterns. The
other 15 rows have explicit witnesses in `witnesses.tsv`; the driver rebuilds
each witness independently in Python and verifies the two exact sums and all
ten autocorrelation residuals modulo `pi^5` directly in `Z[i]`.

Rotation of `A` preserves its exact sum and periodic autocorrelation, so an
orbit representative establishes the classification for all 21 labeled
rotations.

## Reproduction and trust boundary

Run:

```bash
python3 verify_b16_case5_fifth_h.py
```

The driver pins the preceding fourth-order and fifth-`S` certificates and
the C++ checker by SHA-256, compiles with assertions enabled, reproduces
`orbit_table.tsv`, `witnesses.tsv`, and `verification_output.txt` byte for
byte, and directly rechecks all positive witnesses. Arithmetic is exact in
`Z[i]` and `F_2`; there is no floating point, random proof step, solver,
heuristic, or time limit. The negative classification has one exhaustive C++
implementation. Its local algebra is exhaustively checked and its polynomial
coefficients come from direct Gaussian evaluations, but an independent full
negative reimplementation would reduce the remaining implementation risk.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Kotsireas--Koutschan--Winterhof,
*On properties of Legendre pairs under compression*,
<https://doi.org/10.1145/3747199.3747549>. A targeted primary-source and
committed-graph search found no matching fifth-order case-5 classification;
apparent novelty is relative to that search, not a historical-priority claim.

The strongest next step is to impose sixth-order Gaussian residues on the 15
survivors, while independently reimplementing the single negative orbit.
