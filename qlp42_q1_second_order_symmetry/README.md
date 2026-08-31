# Second-order Gaussian symmetry in the QLP-42 `q=1` branch

## Statement

Let `(S_A,H_A,S_B,H_B)` be the exact coupled length-21 transform of a
canonical norm-32 QLP-42 candidate.  Write `pi=1+i`.  At every local cell:

- an equal phase pair has `S=0` and `H` in `pi*mu_4`;
- an opposite phase pair has `S` in `pi*mu_4` and `H=0`;
- a quarter-turn phase pair has orthogonal `S,H` in `mu_4`.

Let `q_X` be the number of quarter-turn cells in family `X`.  The fixed
coupled sums imply

```text
q_A = 0 (mod 2),       q_B = 1 (mod 2).
```

Suppose the total quarter-turn count is the extreme allowed value `q=1`.
Then `q_A=0` and `q_B=1`.  Let `t` be the unique quarter-turn position of
family `B`, and for `j != t` put

```text
epsilon_j = 1  if the cell is opposite (S_B(j) != 0),
epsilon_j = 0  if the cell is equal    (S_B(j)  = 0).
```

Then

```text
epsilon_(t+s) = epsilon_(t-s)  for every s in Z/21Z.       (1)
```

Thus the 20 non-quarter cells form ten reflected pairs of the same type.
Both the equal and opposite counts in family `B` are even.  The center
energy equations give 21 opposite and 20 equal cells globally, so family
`A` has an odd opposite count and an even equal count.

The canonical sums orient the exceptional local state further:

```text
S_B(t) in {+i,-i},       H_B(t) in {+1,-1}.                (2)
```

Equivalently, the original ordered root pair at `t` is one of

```text
(1,i), (i,1), (-1,-i), (-i,-1).
```

After an independent rotation of family `B`, take `t=0`.  If `k_r` is the
number of opposite non-quarter cells in the three positions congruent to
`r mod 7` (omitting the quarter cell at zero), then (1) gives the
solver-ready restriction

```text
(k_0,k_1,k_2,k_3,k_4,k_5,k_6)
  = (k_0,k_1,k_2,k_3,k_3,k_2,k_1),
k_0 in {0,2},   k_1,k_2,k_3 in {0,1,2,3}.                 (3)
```

This leaves only `2*4^3=128` possible opposite-count patterns before the
remaining energy, sum, and autocorrelation constraints.

## Proof of the reflection law

The combined `S` autocorrelation target is an even Gaussian integer at every
nonzero shift: it is zero except for four values equal to `+2` or `-2`.
All `S_A` entries, and every non-quarter `S_B` entry, belong to `pi*Z[i]`.
Consequently every autocorrelation product not involving `t` belongs to
`(pi^2)=(2)`.

At a nonzero shift `s`, the only possibly nonzero terms modulo `pi^2` are

```text
S_B(t) conjugate(S_B(t+s))
  + S_B(t-s) conjugate(S_B(t)).                            (4)
```

If exactly one of the two reflected cells is opposite, (4) is `pi` times a
Gaussian unit and is not divisible by `pi^2`.  If neither is opposite, it is
zero.  If both are opposite, it is `pi` times a sum of two Gaussian units;
all Gaussian units are one modulo `pi`, so that sum is divisible by `pi`.
The even target therefore makes (4) divisible by `pi^2` exactly when the two
types agree, proving (1).

For (2), each reflected pair contributes an even real part and an even
imaginary part to both coupled sums.  In all six canonical cases,
`sum(S_B)` has even real part and odd imaginary part, while `sum(H_B)=1`.
The unique unit entries must therefore be imaginary in `S_B` and real in
`H_B`.  Checking the 16-state local map gives the four ordered root pairs
displayed above.

## Exact certificate

Run:

```bash
python3 verify_q1_second_order_symmetry.py
```

The standard-library verifier:

- reconstructs all 16 coupled local states from the ordered fourth roots;
- checks the equal/opposite/quarter classification and both energy counts;
- derives the family orientation parity in all six canonical sum cases;
- checks all `8*8*8=512` choices of the unique quarter state and two
  reflected non-quarter states, for both `S` and `H`, confirming that their
  cross term is divisible by `2` exactly when the two types agree;
- verifies the four oriented exceptional states and all 128 compressed count
  patterns in (3).

All arithmetic is exact in `Z[i]`.  No SAT status, floating-point
computation, or heuristic search is used.

## Scope and primary context

This eliminates type-asymmetric lifts inside the `q=1` branch; it does not
prove that the remaining symmetric lifts exist or that they extend to a
QLP-42 solution.  It is a second-order `(1+i)`-adic constraint, stronger
than the binary quarter-turn shadow alone.

Primary background: Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, <https://arxiv.org/abs/1302.0571>;
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>; and Jedwab--Pender, *Two constructions of
quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>.  The proof above is self-contained once
the committed coupled QLP-42 identities are given.
