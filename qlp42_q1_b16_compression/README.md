# Mod-7 compression filter for the QLP-42 `q=1`, `b=16` row

## Exact filtering theorem

In the coupled norm-32 QLP-42 shell, assume the total quarter-turn count is
`q=1` and let `b=16` be the number of opposite non-quarter cells in family
`B`. The complete third-order type condition leaves

```text
25 reflected B masks, 1,575 labeled A/B type pairs,
75 A-rotation orbits.
```

Exact factor-three compression of the `H` component to length seven removes

```text
7 B masks, 819 labeled type pairs, 39 A-rotation orbits,
```

leaving at most

```text
18 B masks, 756 labeled type pairs, 36 A-rotation orbits.       (1)
```

Together with the preceding `b=18` and `b=20` obstructions, the master
third-order upper bounds therefore improve to

```text
470 B masks, 193,557 labeled type pairs, 9,217 A-rotation orbits.
```

This is a strict finite filter, not an exclusion of the entire `b=16` row.

## Compression reduction

For `b=16`, family `A` has five opposite cells and sixteen equal cells.
Thus `H_A` has sixteen nonzero entries, each `(1+i)` times a fourth root.
Family `B` has four equal cells in addition to its unique quarter center, so
`H_B` has four diagonal entries and one center entry in `{+1,-1}`.

Compress each length-21 word by a factor of three:

```text
C_X(r) = H_X(r) + H_X(r+7) + H_X(r+14),  r in Z/7Z.
```

If a fiber contains `n` diagonal entries, its compressed value lies in
`(1+i)D_n`, where

```text
D_n = {a+bi : |a|+|b| <= n, a+b = n (mod 2)},
|D_0|,|D_1|,|D_2|,|D_3| = 1,4,9,16.
```

The exact sums and compressed autocorrelation equations are

```text
sum(C_A)=0,  sum(C_B)=1,
PAF(C_A,0)+PAF(C_B,0)=37,
PAF(C_A,s)+PAF(C_B,s)=-6,  s=1,...,6.                 (2)
```

The target `37` is `41-2-2`, and each nonzero compressed target is the sum
of three original `-2` targets. Because length-seven periodic
autocorrelation has conjugate symmetry, shifts 1, 2, and 3 determine all
six nonzero equations.

## Exhaustive quotient and certificate

The checkers independently reconstruct the third-order binary conditions,
then group the 1,575 labeled pairs into 57 simultaneous dihedral support
types. There are nine distinct `A` fiber-count words. For each one, the
seventh compressed coordinate is determined from `sum(C_A)=0`; across the
nine words this examines 6,373,296 six-coordinate prefixes and retains
2,539,032 sum-zero words. Their exact energy and three complex
autocorrelations collapse to 364,917 pattern-local fingerprints.

Across the 57 support types, the exact `B` sum leaves 1,407 pattern-local
compressed words. Complementing their fingerprints against (2) gives:

```text
57 support types  -> 24 surviving, 33 eliminated;
25 B masks        -> 18 surviving,  7 eliminated;
1,575 pairs       -> 756 surviving, 819 eliminated;
75 rotation orbits -> 36 surviving, 39 eliminated.
```

Every surviving or eliminated labeled set is checked to be a union of full
21-element `A` rotation orbits.

## Independent exact verification

Run the standard-library Python checker:

```bash
python3 verify_b16_mod7.py
```

Run the separately written C++20 checker in the pinned image:

```bash
docker run --rm -v "$PWD:/work" -w /work \
  gcc:14@sha256:88134abee5c979390be4fedf9af2635e324004f0f3c1266a8c924c7a08e69500 \
  bash -lc 'g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
    verify_b16_mod7.cpp -o /tmp/verify && /tmp/verify'
```

Both outputs must equal `verification_output.txt`. All arithmetic is exact
in `Z[i]`; no floating point, SAT status, heuristic search, or unverified
phase lift enters the certificate.

This computation works in a relaxation: it uses exact compressed sums and
the full compressed `H` autocorrelation, but omits the `S` component and the
pointwise coupling of phase choices. Therefore eliminated types are
rigorously impossible, while the 756 survivors are only candidates for a
stronger lift. The result does not exclude `b=16`, the lower rows, or a
QLP-42 construction.

Primary context is Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, <https://arxiv.org/abs/1302.0571>,
and Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>. Apparent novelty is relative to those
searched sources and the committed Discovery Net graph, not a historical
priority claim.
