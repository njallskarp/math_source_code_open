# Exact-H and sixth-order-H reduction for QLP-42 `q=1`, `b=12`

## Computational lemma

Continue the coupled norm-32 QLP-42 shell with `q=1`, `b=12`, canonical
order-two compression, and the previously certified eighth-order `S`
frontier. Its surviving A-rotation incidences by exact-sum case are

```text
case                              0    1   2  3  4  5
eighth-order S incidences       303  178  92  1  1  0
```

Fixing the exceptional `B` cell to `S_B(0)=-i` forces its `H_B(0)` sign by
case. The signs for cases 0 through 5 are respectively

```text
+1, -1, +1, +1, -1, -1.
```

Direct enumeration of all 98 reflected `B` masks shows that the negative
center admits no phase assignment satisfying `sum(H_B)=1`. The positive
center admits between 608 and 676 assignments per mask. Consequently the
exact `H` sum alone eliminates cases 1, 4, and 5. Case 5 was already empty in
the preceding `S` frontier.

The one eighth-order incidence in case 3 and the one in case 4 have the same
support data:

```text
B equal positions: 3,4,8,10,11,13,17,18
A S support:        0,1,2,3,4,5,10,13,16
```

For case 3, the positive center gives 608 exact `H_B` phase assignments and
304 distinct sixth-order fingerprints. The complementary twelve-cell
`H_A` support has 853,776 exact phase assignments with `sum(H_A)=0`, giving
101,390 distinct required fingerprints. Their intersection is empty.
Therefore case 3 also cannot lift. Case 4 has already failed its exact
`H_B` sum.

After these tests only cases 0 and 2 remain: 395 case incidences carried by
375 distinct mask/support rows. The complete sixth-order `H` scan of this
frontier leaves

```text
case                               0   2
sixth-order H incidences          61  18
supporting B masks                17   8
```

The 79 case incidences occupy 77 distinct rows. Thus the combined exact-sum,
eighth-order `S`, and sixth-order `H` frontier is 77 rows. This is a strict
intermediate reduction, not an exclusion of the complete `b=12` shell.

## Exact computation

Every active non-quarter `H` cell is `(1+i)` times a Gaussian unit. The
combined `H` autocorrelation target is `-2` at every nonzero shift. Since
`(1+i)^6=-8i`, sixth-order feasibility is equality of both Gaussian
coordinates modulo 8 at the ten independent shifts.

`prototype_sixth_h.cpp` reconstructs all 98 masks and the complete preceding
eighth-order `S` frontier. For the singleton cases it uses an exact 6+6
meet-in-the-middle enumeration of the twelve `H_A` phase signs. After the
third-order parity conditions, the sign-change PAF map is affine modulo 8;
the program directly audits this identity for all 2,048 admissible axis
assignments in the negative case-3 search.

`independent_numpy.py` does not use that affine interpolation. It evaluates
the PAF directly for all 853,776 exact `H_A` assignments and directly
enumerates every `H_B` phase assignment. It independently obtains the empty
case-3 intersection and scans both center orientations for all 98 masks.

`precomputed_full_h.cpp` groups the 375 remaining rows by their 345 distinct
`A` supports. For each support it enumerates all 853,776 exact zero-sum
`H_A` assignments once, builds the complete sixth-order fingerprint set, and
intersects it with all applicable exact `H_B` fingerprints. Across all
supports it exhausts 294,552,720 assignments and directly audits the affine
PAF identity for all 706,560 admissible axis systems.

`independent_full_numpy.py` consumes the reconstructed 375-row predecessor
but independently evaluates every one of those 294,552,720 PAFs directly,
without affine interpolation. It reproduces the 61 and 18 incidence counts,
the 17 and 8 mask counts, and the 77-row union exactly.

All arithmetic is integral and exhaustive. No floating point, random step,
SAT/SMT solver, heuristic pruning, or time limit is used.

## Reproduction and trust boundary

Install NumPy and run:

```bash
python3 verify_b12_h_frontier.py
```

The driver pins all implementations and the predecessor certificates,
compiles the C++20 route with assertions enabled, and checks the exact
outputs. The two routes share the coupled transform, support conventions,
and preceding eighth-order `S` statement; their new sixth-order `H`
arithmetic and enumeration strategies are independent. The C++ full scan
uses packed modulo-8 affine fingerprints; the NumPy full scan constructs and
evaluates every exact phase word directly. This certificate
proves a finite Gaussian-residue obstruction, not historical priority and
not nonexistence of all QLP-42 pairs.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Djokovic--Kotsireas, *Compression of
Periodic Complementary Sequences and Applications*,
<https://arxiv.org/abs/1302.0571>. A targeted primary-source and committed
graph search found no matching higher-order obstruction; apparent novelty is
relative to those searches.

The strongest next step is a seventh-order `H` scan of the 77 remaining rows,
using the exact quotient `Z[i]/((1+i)^7) ~= Z/8 x Z/16` and retaining the
direct NumPy route as an independent check.
