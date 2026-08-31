# Mod-7 obstruction to the QLP-42 `q=1`, `b=20` type branch

## Theorem

In the coupled norm-32 QLP-42 shell with total quarter-turn count `q=1`, let
`b` be the number of opposite non-quarter cells in family `B`.  Then

```text
b != 20.
```

The preceding third-order type classification left exactly one reflected
`B` mask at `b=20`, paired with 21 labeled family-`A` type masks forming one
rotation orbit.  The present obstruction removes that entire row.  Thus its
global third-order totals improve from

```text
480 B masks, 194,439 labeled pairs, 9,259 A-rotation orbits
```

to at most

```text
479 B masks, 194,418 labeled pairs, 9,258 A-rotation orbits.
```

This branch was sum-compatible only with canonical case 0, so that case now
has the same improved totals; the other five case totals are unchanged.

## Reduction to a one-word projection

When `b=20`, family `B` has twenty opposite cells and its unique quarter cell,
while family `A` has one opposite cell and twenty equal cells.  In the coupled
`H` component, `H_B` is supported only at the quarter center.  Hence its
nonzero-shift autocorrelations vanish.

Divide the twenty nonzero diagonal entries of `H_A` by `1+i`, and put zero at
its unique opposite cell.  After rotating that zero to position zero, this
would give a length-21 word

```text
U_0 = 0,        U_j in {1,i,-1,-i} for j != 0,
sum_j U_j = 0,
PAF(U,0) = 20,  PAF(U,s) = -1 for every s != 0.          (1)
```

The factor of two comes from `|(1+i)|^2=2`, and the coupled `H` target is
`-2` at every nonzero shift.

## Mod-7 compression obstruction

Compress `U` to length seven:

```text
C_r = U_r + U_(r+7) + U_(r+14).
```

The zero lies in `C_0`, so `C_0` is a sum of two fourth roots and every other
coordinate is a sum of three.  These exact Gaussian domains are

```text
D_n = {a+bi : |a|+|b| <= n, a+b = n (mod 2)},
|D_2|=9, |D_3|=16.
```

The compression identity applied to (1) requires

```text
sum_r C_r = 0,
PAF(C,0) = 18,
PAF(C,s) = -3 for s=1,...,6.                             (2)
```

There are `9*16^6 = 150,994,944` raw domain tuples.  Determining the last
coordinate from the zero sum leaves 2,795,584 tuples.  Exact enumeration
gives

```text
sum-zero tuples                         2,795,584
also satisfying center energy 18          60,024
also satisfying shift 1 = -3                  656
also satisfying shift 2 = -3                    0
```

Thus even the first two independent out-of-phase equations in (2) are
inconsistent, proving the theorem.

## Independent exact verification

The standard-library implementation and a separately written C++20 checker
perform the same finite classification with different control flow:

```bash
python3 verify_b20_mod7.py

docker run --rm -v "$PWD:/work" -w /work \
  golang:1.25.0-bookworm@sha256:81dc45d05a7444ead8c92a389621fafabc8e40f8fd1a19d7e5df14e61e98bc1a \
  bash -lc 'g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
    verify_b20_mod7.cpp -o /tmp/verify && /tmp/verify'
```

Both regenerate the root-sum domains, derive the compressed target, determine
the seventh coordinate from the sum, and reproduce every intermediate count.
All arithmetic is exact in `Z[i]`; no SAT status, floating point, or heuristic
search enters the result.

The result eliminates only the `b=20` third-order type row.  It does not
exclude the remaining `b=4,6,...,18` branches or settle QLP-42.  Primary
context is Djokovic--Kotsireas, *Compression of Periodic Complementary
Sequences and Applications*, arXiv:1302.0571, and
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
arXiv:2408.16318.  Apparent novelty is relative to those searched sources and
the committed Discovery Net graph, not a historical-priority claim.
