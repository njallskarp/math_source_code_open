# Sixth/seventh-order obstruction for the QLP-42 `q=1`, `b=16` shell

## Theorem

In the coupled norm-32 QLP-42 shell with `q=1`, `b=16` and canonical
order-two compression, none of the six exact-sum cases can lift to a
quaternary Legendre pair.

The preceding exact mod-7, fourth-order, and exact-sum certificates leave 32
`A`-rotation orbits in each of cases 0--4. The sixth-order `S` equations
eliminate every orbit in cases 0, 2, 3, and 4 and leave only two case-1
orbits, both over the same reflected `B` mask:

```text
B equal positions:  2,6,15,19
A supports:          0,2,4,10,12
                     0,2,4,13,15
```

The seventh-order `S` equations eliminate both. Case 5 was independently
closed by the preceding sixth-order certificate. Thus the full
`q=1`, `b=16` shell is impossible.

## Exact-sum cases and sixth order

For `(p,q,x,y)` the exact `S` sums are

```text
case   (p,q,x,y)       sum(S_A)   sum(S_B)
0      (1,0,5,0)       1-i        4-5i
1      (3,0,4,1)       3-3i       4-3i
2      (3,0,3,-2)      3-3i       -5i
3      (3,2,3,2)       5-i        4-i
4      (3,2,2,3)       5-i        4+i
```

The five-entry `A` supports have respectively 100, 25, 25, 10, and 10 exact
phase assignments. Each reflected `B` mask has 500,992 exact assignments in
cases 0 and 1 and 804,968 in cases 2--4.

Since `(1+i)^6=-8i`, sixth-order divisibility is equivalent to both Gaussian
coordinates vanishing modulo 8. `prototype_numpy.py` enumerates all
`256*2^17` `B` phase choices per mask, selects the exact sums, and directly
computes periodic autocorrelations modulo 8. `independent_sixth_cpp.cpp`
instead divides the known `(1+i)^3` factor and computes in

```text
Z[i]/((1+i)^3) ~= Z/2 x Z/4,
r+si |-> (r mod 2, r+s mod 4).
```

For each of 18 masks, five cases, and 256 axis assignments, the C++ checker
obtains the complete quadratic sign polynomial from 17 linear and 136
quadratic evaluations and performs 16 additional global audits: 3,893,760
direct checks. Its exact 8+9 join and the direct NumPy enumeration agree on
every orbit classification and every per-mask fingerprint count in
`sixth_orbit_table.tsv`.

## Seventh-order closure

For the last case-1 mask, 500,992 exact `B` assignments produce 500,740
distinct seventh-order fingerprints. Because `(1+i)^7=8-8i`, equality modulo
`((1+i)^7)` is represented exactly by

```text
r+si |-> (r mod 8, r+s mod 16).
```

None of the 25 exact `A` assignments for either remaining support matches a
`B` fingerprint. `prototype_seventh_s.py` obtains this by direct vectorized
autocorrelation. `independent_seventh_cpp.cpp` independently interpolates the
full quadratic sign polynomial in the quotient group and exhausts an exact
8+9 Gaussian-sum join. Both reproduce the same 500,992 assignments, 500,740
fingerprints, and two negative classifications.

The exploratory `prototype_sixth_h.cpp` records that both intermediate
case-1 candidates pass sixth-order `H`; their rejection genuinely occurs at
seventh-order `S`, not at the preceding component test.

## Reproduction and trust boundary

Install NumPy and run:

```bash
python3 verify_q1_b16_shell.py
```

The driver pins all predecessor and implementation files by SHA-256,
reconstructs `input_orbits.tsv` from the earlier exact-sum verifier, compiles
both C++ implementations with assertions enabled, and reproduces every
checked-in table and output byte for byte. All mathematical arithmetic is
integral. The two routes use different quotient representations and
enumeration strategies; neither uses random proof steps, a solver, heuristic
pruning, floating-point comparisons, or a time limit. They share the pinned
fourth-order support table and the stated phase conventions.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Kotsireas--Koutschan--Winterhof,
*On properties of Legendre pairs under compression*,
<https://doi.org/10.1145/3747199.3747549>. A targeted primary-source and
committed-graph search found no matching higher-order obstruction; apparent
novelty is relative to that search, not a historical-priority claim.

The strongest next step is to move to the next unresolved `(q,b)` shell in
the QLP-42 norm equation and reuse the certified sixth/seventh-order engine.
