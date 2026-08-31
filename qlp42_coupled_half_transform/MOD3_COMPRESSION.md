# Exact mod-3 classification of the coupled QLP-42 shell

## Result

Compress each length-21 coupled word modulo 3, so each compressed coordinate
is the sum of seven original coordinates.  For the six canonical order-two
compression cases, the exact numbers of jointly admissible `(S,H)`
compression pairs are:

| case | matching descriptors | ordered pairs | independent-rotation orbits |
|---:|---:|---:|---:|
| 0 | 238 | 73,008 | 8,112 |
| 1 | 85 | 95,484 | 10,612 |
| 2 | 69 | 80,136 | 8,904 |
| 3 | 238 | 73,080 | 8,120 |
| 4 | 238 | 73,080 | 8,120 |
| 5 | 91 | 83,160 | 9,240 |

Here the two members of a pair may be rotated independently.  The orbit
counts therefore quotient by the exact `C_3 x C_3` action, including any
short orbits rather than dividing the ordered counts blindly by nine.

Every one of the eleven previously proved quarter-turn totals

```text
1,5,9,13,17,21,25,29,33,37,41
```

has at least one lift through each compressed case.  Thus mod-3 compression
does not improve the defect-count congruence by itself; its gain is the finite
classification above.

## Derivation

For a length-21 word `W`, define its length-3 compression by

```text
Q(W)_r = sum_(j congruent to r mod 3) W_j.
```

The standard compression identity is

```text
PAF(Q(W),r) = sum_(s congruent to r mod 3) PAF(W,s).
```

In the sparse `S` target, the values at shifts 4 and 10 cancel in residue
class 1, and the values at shifts 11 and 17 cancel in residue class 2.
Consequently the compressed combined targets are

```text
S: (43,0,0),
H: (29,-14,-14).
```

It is useful to enumerate through the two original CRT rows `x,y`.  A sum of
seven fourth roots is exactly a Gaussian integer `a+bi` satisfying

```text
|a|+|b| <= 7,       a+b = 7 (mod 2).
```

This domain has 64 points.  Conversely, any pair of domain points can be
realized as the sums of seven ordered `x`- and `y`-roots: choose the two root
lists independently and pair their positions.  The compressed transform is
then exact:

```text
S=(x-y)/(1+i),      H=(x+y)/(1+i).
```

For each family, the verifier chooses the first two length-3 `x` cells from
the 64-point domain and forces the third from the prescribed total sum; it
does the same for `y`.  Each resulting pair is summarized by its `S` and `H`
energies and its two complex shift-one autocorrelations.  Complementary
descriptors are matched against the displayed targets.  Canonical cyclic
representatives give the independent-rotation orbit counts.

The verifier also performs a seven-step dynamic program over all 16 local
ordered-root states.  For every compressed `(x,y)` cell it records the exact
set of realizable quarter-turn counts, convolves those sets across the three
cells and both families, and checks which global totals survive.  This closes
the potential gap between an admissible pair of Gaussian sums and a coupled
seven-state lift.

## Reproduction and trust boundary

Run the verifier in the pinned Debian image used for the preceding exact
QLP-42 enumeration:

```bash
docker run --rm -v "$PWD:/work" -w /work \
  golang:1.25.0-bookworm@sha256:81dc45d05a7444ead8c92a389621fafabc8e40f8fd1a19d7e5df14e61e98bc1a \
  bash -lc 'g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
    qlp42_coupled_half_transform/verify_mod3_coupled_compression.cpp \
    -o /tmp/verify_mod3 && /tmp/verify_mod3'
```

The certificate uses integer Gaussian arithmetic, finite sets, and exhaustive
iteration.  No floating-point calculation, heuristic trajectory, or SAT
outcome is used for the classification.

`solve_coupled_half_transform_sat.py` separately encodes the uncompressed
16-state problem using one-hot Boolean variables and exact finite-state sum
automata.  Initial 30-second case-0 runs at the extreme defect totals 1 and 41
both returned `UNKNOWN`; those bounded outcomes are smoke tests only and are
not evidence for existence or nonexistence.

## Scope and primary context

This is an exact search-space reduction for the norm-32 residual shell.  It
does not produce a length-42 realization, exclude a canonical case, or settle
the QLP-42 existence problem.  The strongest next step is to feed the listed
compression orbits into the full coupled solver, or combine them with the
independent length-7 compression.

The compression identity and its use for periodic complementary collections
appear in D. Z. Djokovic and I. S. Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, <https://arxiv.org/abs/1302.0571>.
QLP-42 context is in Kotsireas--Koutschan--Winterhof, *Quaternary Legendre
pairs II*, <https://arxiv.org/abs/2408.16318>.  A targeted search of those
primary sources and the committed Discovery Net graph did not locate this
coupled mod-3 classification; apparent novelty is relative to that search,
not a literature-priority claim.
