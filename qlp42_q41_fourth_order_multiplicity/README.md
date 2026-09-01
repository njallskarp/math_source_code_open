# Exact sign-lift multiplicities in the QLP-42 `q=41` fourth-order layer

## Multiplicity theorem

Continue the exact fourth-order classification in the `q=41` branch of the
coupled norm-32 QLP-42 shell.  Let `a in F_2^10` be the reflected family-`A`
axis word and `b in F_2^21` the unrestricted family-`B` axis word.  Write

```text
D_b : F_2^21 -> F_2^10
```

for the fourth-order `B` sign map, and let `r=rank(D_b)`.  The preceding
classification proved that exactly 1,717,504,656 labeled axis pairs, or
81,785,936 pairs modulo cyclic rotation of `B`, admit a lift through the
autocorrelation equations modulo `(1+i)^4`.

For **every** surviving axis pair, the number of complete transformed sign
lifts is exactly

```text
2^(64-2r).                                                   (1)
```

Here a complete sign lift includes all 10 free reflected-pair signs and all
21 unpaired signs independently in each of the `H` and `S` systems, together
with the phase of the exceptional norm-two entry `S_A(0)=(1+i)c`.

More precisely, if `U_H(a),U_S(a)` are the images of the ten reflected-pair
sign flips in `A`, exhaustive exact linear algebra proves, on every survivor,

```text
rank(U_H(a)+image(D_b)) = r,
rank(U_S(a)+image(D_b)) = r,                                (2)
```

and all four possible unit phases `c` are admissible.  Equation (2) is
equivalent to

```text
U_H(a) subset image(D_b),   U_S(a) subset image(D_b)
```

on the surviving locus.  Hence the affine `H` system has `2^(31-r)`
solutions, while the `S` system has `4*2^(31-r)` solutions.  Their local
sign variables are independent, giving (1).

The complete spectrum is unusually sparse:

| `r` | surviving labeled axis pairs | surviving `B`-rotation axis orbits | sign lifts per axis pair |
|---:|---:|---:|---:|
| 4  | 672           | 32         | 72,057,594,037,927,936 |
| 6  | 43,344        | 2,064      | 4,503,599,627,370,496 |
| 7  | 368,928       | 17,568     | 1,125,899,906,842,624 |
| 9  | 132,031,872   | 6,287,232  | 70,368,744,177,664 |
| 10 | 1,585,059,840 | 75,479,040 | 17,592,186,044,416 |

Summing axis-pair multiplicities gives exactly

```text
37,834,587,347,152,206,299,136 labeled transformed sign lifts,
 1,801,647,016,531,057,442,816 after factoring B rotations.
```

These counts are for the fourth-order autocorrelation relaxation.  They are
not counts of QLP-42 solutions.

## Why the formula counts actual local states

After the third-order theorem fixes one sign XOR in each reflected pair, the
fourth-order `H` system has 10 remaining `A` pair signs and 21 `B` signs.
It is therefore an affine system in 31 binary variables.  A consistent
rank-`r` system has exactly `2^(31-r)` solutions.  The `S` system has the
same variable count, plus four possible phases at its exceptional center.
The exact classification finds all four center phases consistent and finds
the same rank `r`, giving `4*2^(31-r)` `S` lifts.

At every quarter-turn local state, the `S` and `H` axes are complementary
and their two signs range independently over `F_2^2`.  Thus multiplying the
two affine counts neither misses a local state nor introduces a spurious
coupling.  At the exceptional opposite cell, `H_A(0)=0` and the four
admissible `S_A(0)` phases are exactly the four opposite local states.

## Reproduction

Run:

```bash
python3 verify_q41_fourth_order_multiplicity.py
```

The standard-library certificate pins the SHA-256 of the preceding exact
rank verifier, reruns its full construction and direct Gaussian audits, and
then:

- recomputes all 99,880 cyclic `B`-axis orbits;
- recomputes the exact orthogonal complements of `image(D_b)`, `U_H(a)`,
  and `U_S(a)`;
- obtains the ranks in (2) from the cardinalities of the corresponding
  orthogonal intersections;
- checks consistency for each of the four exceptional center phases;
- verifies `multiplicity_table.tsv` and the independently rank-indexed
  `rank_multiplicity_table.tsv`;
- recovers the prior survivor totals and the two displayed sign-lift sums.

The dependency is pinned to SHA-256
`cefc2f614980396aaecc9894733e3e8840658966b5d33e1ae6811a7bcc4b3d69`.
That dependency checks the Gaussian residue formulas directly, exhausts all
`2^21` axis words, and compares 200 deterministic cases with direct
length-21 Gaussian PAF computations.  This extension contains no floating
point, SAT/SMT status, heuristic search, or probabilistic proof step.

## Scope and next step

This theorem classifies multiplicity inside the fourth-order residue layer.
It does not impose the four exact frequency-zero Gaussian sum equations or
the full integer nonzero-shift autocorrelations.  Several binary sign lifts
may also reconstruct sequences related by symmetries not factored here; the
only quotient counted is cyclic rotation of family `B`, after the unique
exceptional `A` cell fixes the rotation of `A`.

The structural concentration in (2) identifies the next useful target:
intersect the affine kernels with the exact global-sum domains.  Since the
`A` sign directions add no new fourth-order image direction on survivors,
the exact-sum dynamic program can be organized by `rank(D_b)` and its kernel
rather than by all sign assignments.

Primary context remains Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications* (arXiv:1302.0571);
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*
(arXiv:2408.16318); Kotsireas--Winterhof, *Quaternary Legendre Pairs*
(arXiv:2212.10953); and Jedwab--Pender, *Two constructions of quaternary
Legendre pairs of even length* (arXiv:2408.08472).  The result is apparently
new relative to the targeted primary-source and current-graph search, not a
historical-priority claim.
