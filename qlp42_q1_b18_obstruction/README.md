# Mod-7 obstruction to the QLP-42 `q=1`, `b=18` type row

## Theorem

In the coupled norm-32 QLP-42 shell with total quarter-turn count `q=1`, let
`b` be the number of opposite non-quarter cells in family `B`. Then

```text
b != 18.
```

The preceding third-order type classification left exactly two reflected
`B` masks at `b=18`, paired with 42 labeled family-`A` masks in two cyclic
orbits. The present obstruction eliminates that entire row. Together with
the independent `b=20` obstruction, the surviving third-order master totals
therefore improve from

```text
480 B masks, 194,439 labeled pairs, 9,259 A-rotation orbits
```

to at most

```text
477 B masks, 194,376 labeled pairs, 9,256 A-rotation orbits.
```

The `b=18` row was sum-compatible only with canonical cases 0, 1, and 2;
the `b=20` row was compatible only with case 0. Consequently all six
canonical cases now have the same upper bounds in `case_table.tsv`.

## Two residual support patterns

Rotate the unique quarter cell of `B` to position zero. Re-evaluating the
third-order binary conditions at weight `b=18` leaves the two `B` masks whose
equal-cell positions are

```text
{10,11} and {4,17}.
```

The corresponding weight-three opposite-cell words of `A` form the two
rotation orbits represented by

```text
{0,1,11} and {0,4,8}.
```

Modulo seven, both `B` equal pairs occupy residues `{3,4}`. Both `A` triples
occupy a translate of `{0,1,4}`. Hence, up to cyclic rotation, the number of
nonzero `H_A` entries in the seven compression fibers is

```text
(2,2,3,3,2,3,3).                                      (1)
```

Periodic autocorrelation is invariant under that rotation, so one support
word covers every relative rotation and both third-order orbits.

## Exact compression obstruction

Compress the length-21 `H` words by a factor of three:

```text
C_X(r) = H_X(r) + H_X(r+7) + H_X(r+14).
```

For a non-quarter equal cell, `H=(1+i)u` with `u` a fourth root. Therefore
the coordinate domains for `C_A` are `(1+i)D_n`, where

```text
D_n = {a+bi : |a|+|b| <= n, a+b = n (mod 2)},
|D_2|=9, |D_3|=16.
```

The exact sum `sum(H_A)=0` becomes `sum(C_A)=0`. The compressed combined
autocorrelation target is

```text
PAF(C_A,0)+PAF(C_B,0) = 37,
PAF(C_A,s)+PAF(C_B,s) = -6,  s=1,...,6.                (2)
```

Indeed, the original target is 41 at zero and -2 at every nonzero shift;
compression adds the three shifts congruent modulo seven.

The word `C_B` has support `{0,3,4}`. Its center is `+1` or `-1`, and the
other two values are `(1+i)` times fourth roots. Imposing `sum(C_B)=1`
leaves exactly six candidates: four with center `+1` and two with center
`-1`. Every candidate has energy five, so (2) forces

```text
PAF(C_A,0)=32.                                         (3)
```

There are `9^3*16^4 = 47,775,744` raw domain words allowed by (1). Determining
the seventh coordinate from the zero sum and filtering exactly gives

| filter | center `+1` | center `-1` |
|---|---:|---:|
| sum zero | 1,028,196 | 1,028,196 |
| also energy 32 | 33,072 | 33,072 |
| also shift 1 | 664 | 536 |
| also shifts 1 and 2 | 16 | 24 |
| also shifts 1, 2, and 3 | 0 | 0 |

The counts in the last three rows are per compressed `B` candidate; they are
constant within each center class. Thus no pair satisfies even the `H`
projection of (2), proving the theorem. This is an obstruction in a relaxed
projection, so omitted `S`-component and local-coupling constraints cannot
restore a solution.

## Independent exact verification

Run the standard-library checker:

```bash
python3 verify_b18_mod7.py
```

It independently reconstructs the two third-order masks and two rotation
orbits, derives their common mod-7 supports, generates all Gaussian domains,
and performs the exhaustive compression test.

A separately structured C++20 checker begins from the proved support pattern
and performs the same finite obstruction with recursive enumeration:

```bash
docker run --rm -v "$PWD:/work" -w /work \
  gcc:14@sha256:88134abee5c979390be4fedf9af2635e324004f0f3c1266a8c924c7a08e69500 \
  bash -lc 'g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
    verify_b18_mod7.cpp -o /tmp/verify && /tmp/verify'
```

Both outputs must equal `verification_output.txt`. All arithmetic is exact in
`Z[i]`; there is no floating point, SAT status, heuristic search, or assumed
phase lift.

This eliminates only the `b=18` type row and does not settle the remaining
`b=4,6,...,16` branches or QLP-42. Primary context is
Djokovic--Kotsireas, *Compression of Periodic Complementary Sequences and
Applications*, <https://arxiv.org/abs/1302.0571>, and
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>. Apparent novelty is relative to those
searched sources and the committed Discovery Net graph, not a claim of
historical priority.
