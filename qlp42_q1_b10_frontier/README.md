# Sixth-order `H` frontier for QLP-42 `q=1`, `b=10`

## Computational lemma

In the canonical order-two-compression branch of the norm-32 quaternary
Legendre-pair problem at length 42 with `q=1` and `b=10`, the exact sums and
sixth-order Gaussian `H` autocorrelation equations reduce the 2,690
third-order rotation-orbit pairs in each of the six exact-sum cases to the
same 198 orbit pairs on 64 reflected `B` masks. Thus any lift of this shell
must occur among 1,188 case incidences, rather than the original 16,140.
This is a frontier reduction, not an exclusion of the shell and not a
resolution of QLP-42.

The exact-sum calculation also resolves the exceptional quarter cell. For all
140 admissible `B` masks, the orientation `H_B(0)=+1` has no exact phase
assignment, while `H_B(0)=-1` has exactly 3,384. Consequently the surviving
orientation has `S_B(0)=+i` in cases 0, 2, and 3 and `S_B(0)=-i` in cases 1,
4, and 5. The corresponding exact `S_B` phase counts are respectively 360,
636, 1,552, 1,552, 1,552, and 3,384, so no exact-sum case is silently lost.

## Sixth-order quotient and exhaustive search

Every active non-quarter `H` cell is `(1+i)` times a Gaussian unit and the
combined nonzero-shift `H` autocorrelation target is `-2`. Since
`(1+i)^6=-8i`, the sixth-order quotient is represented by reducing both
Gaussian coordinates modulo 8.

The C++ route reconstructs all 140 masks, 56,490 labeled type pairs, and
2,690 rotation-orbit pairs from the third-order equations. It enumerates all
3,384 exact `H_B` words per mask and all 63,504 zero-sum `H_A` phase words per
support. Over the 1,972 distinct `A` supports this exhausts 125,229,888 exact
`H_A` assignments. The sign-change PAF map is evaluated affinely modulo 8,
with one direct identity audit for each of 1,009,664 axis/support systems.
The `H_B` complement sets contain 1,564--1,692 fingerprints per mask.

The independent NumPy route reconstructs the inputs separately, generates
the 63,504 zero-sum ten-cell words as all independent choices of five positive
real and five positive imaginary coordinates, and directly evaluates every
PAF coordinate without affine interpolation. Both implementations return the
same sorted list of 198 `(A-support,B-mask)` frontier pairs byte for byte.
All arithmetic is integral and exhaustive; there is no floating point,
randomness, solver, heuristic pruning, or time limit.

## Reproduction and trust boundary

Install NumPy and run:

```bash
python3 verify_b10_sixth_h.py
```

The driver pins both implementations and their inherited third-order and
Gaussian-residue dependencies by SHA-256, compiles C++20 with assertions
enabled, checks the certified counts, and compares the exact frontier. The
two routes share the mathematical transform and support conventions. Their
new phase generation and autocorrelation evaluation are independent: an
affine meet-in-the-middle computation with direct audits versus direct
vectorized PAF evaluation. This is an exact finite computer-assisted lemma,
not a formal proof-assistant theorem or a historical-priority claim.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Djokovic--Kotsireas, *Compression of
Periodic Complementary Sequences and Applications*,
<https://arxiv.org/abs/1302.0571>. A targeted primary-source and committed
graph search found no matching `q=1`, `b=10` sixth-order frontier; apparent
novelty is relative to those searches.

The strongest next step is a seventh-order `H` scan on the certified 198-pair
frontier, followed by the higher-order `S` equations only if needed.
