# Mod-7 binary-shadow classification for the norm-32 QLP-42 shell

## Exact reduction

Let `(S_A,H_A,S_B,H_B)` be the coupled length-21 transform of a canonical
norm-32 QLP-42 candidate.  For a length-21 word `W`, define its length-7
compression by

```text
C(W)_r = W_r + W_(r+7) + W_(r+14),  r in Z/7Z.
```

The compression identity and the two coupled target profiles give

```text
PAF(C(S_A)) + PAF(C(S_B)) = (43, 0, 0, 0, 0, 0, 0),
PAF(C(H_A)) + PAF(C(H_B)) = (37,-6,-6,-6,-6,-6,-6).       (1)
```

Put `pi=1+i`.  On each of the 16 exact local states, `S mod pi` and
`H mod pi` are equal: they are one precisely for a quarter-turn phase pair
and zero for an equal or opposite pair.  If `u_A,u_B` are these length-21
binary shadows and

```text
v_X(r) = u_X(r) + u_X(r+7) + u_X(r+14)  in F_2,
```

then both compressed Gaussian words reduce coordinatewise to `v_X` modulo
`pi`.  Reducing either line of (1) therefore yields

```text
v_A v_A* + v_B v_B* = 1
    in F_2[x]/(x^7-1),                                  (2)
```

where `*` sends `x` to `x^(-1)`.  Equivalently, the combined periodic binary
autocorrelation is one at shift zero and zero at every nonzero shift.

There are exactly 1,008 ordered pairs satisfying (2), and exactly 24 orbits
under independent cyclic rotation of `v_A` and `v_B`.  The complete
solver-ready representative table is in `orbit_table.tsv`.

## Algebraic count and orbit proof

Over `F_2`,

```text
x^7-1 = (x+1)(x^3+x+1)(x^3+x^2+1).
```

Thus the group algebra is `F_2 x F_8 x F_8`.  The involution fixes the first
factor and exchanges the two cubic factors.  After identifying the two
copies of `F_8`, equation (2) becomes

```text
epsilon_A + epsilon_B = 1,
a_A b_A + a_B b_B = 1  in F_8.
```

There are two choices for the epsilon pair.  The coefficient pair
`(a_A,a_B)` may be any of the `8^2-1=63` nonzero pairs, and each such choice
leaves eight solutions for `(b_A,b_B)`.  Hence the ordered count is
`2*63*8=1008`.

For the independent `C_7 x C_7` rotation action, the identity fixes all
1,008 pairs.  Each of the 12 group elements that rotates exactly one word
fixes 14 pairs: the fixed word is constant, while the other word is a
singleton or its complement.  The 36 elements nontrivial on both words fix
none.  Burnside's lemma gives

```text
(1008 + 12*14)/49 = 24
```

orbits.

## Exact lift spectrum

Let `q` be the total number of quarter-turn cells in the two original
length-21 shadows, and let `r=wt(v_A)+wt(v_B)`.  The 24 orbit representatives
have `r` equal to 1, 5, 9, or 13, with orbit multiplicities 2, 10, 10, and 2.
For every individual ordered pair satisfying (2), exhaustive signature
matching proves that its exact binary-shadow lift spectrum is

```text
q = r, r+4, r+8, ..., r+28.                             (3)
```

The necessity in (3) is transparent: each of the 14 residue blocks contains
three binary cells, its parity is the compressed bit, and both the original
and compressed complementary shadows have total weight one modulo four.
The exhaustive length-21 computation proves sufficiency at the binary-shadow
level.  Consequently the numbers of mod-7 orbits surviving the eleven
previously allowed quarter-turn totals are

```text
q:          1  5  9 13 17 21 25 29 33 37 41
orbits:     2 12 22 24 24 24 24 24 22 12  2.
```

In particular, the extreme branches `q=1` and `q=41` each retain only two
of the 24 mod-7 shadow orbits.  This is an exact branching constraint for the
coupled SAT/CP-SAT search.

## Reproduction and trust boundary

Run:

```bash
python3 verify_mod7_binary_shadow.py
```

The standard-library verifier:

- checks the local `S mod pi = H mod pi` quarter-turn indicator on all 16
  ordered phase pairs;
- derives both compressed targets in (1);
- directly checks all `2^14=16,384` length-7 binary pairs;
- verifies the 24 canonical independent-rotation representatives and the
  Burnside fixed-point counts;
- enumerates all `2^21` binary words, groups their ten independent
  autocorrelation parities, exact weights, and mod-7 shadows, and performs
  the exact complementary-signature join proving (3).

All computations use integer and bit arithmetic.  No floating-point result,
heuristic search, or SAT status enters the classification.

This result classifies the binary residue of the independent length-7
compression, not the full Gaussian compressed words.  Surviving shadows need
not lift through equations (1), the 16-state table, or the original QLP-42
autocorrelations.

Primary context for complementary-sequence compression is Djokovic and
Kotsireas, *Compression of Periodic Complementary Sequences and
Applications*, <https://arxiv.org/abs/1302.0571>.  Binary periodic
complementary sets and cyclic difference-family context appear in Djokovic,
*Periodic complementary sets of binary sequences*,
<https://arxiv.org/abs/0708.0053>.  QLP-42 context is in
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>.  A targeted search of these primary
sources and the current graph did not locate this coupled mod-7 shadow
classification; apparent novelty is relative to that search, not a priority
claim.
