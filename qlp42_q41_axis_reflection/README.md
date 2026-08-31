# Gaussian-axis reflection in the QLP-42 `q=41` branch

## Statement

Let `(S_A,H_A,S_B,H_B)` be the exact coupled length-21 transform of a
canonical norm-32 QLP-42 candidate, and suppose that the total number `q` of
quarter-turn local cells is 41.  The family orientation and the center
energies then force

```text
(q_A,q_B) = (20,21),
(number of opposite cells, number of equal cells) = (1,0).
```

Thus family `B` consists entirely of quarter-turn cells, while family `A`
has one opposite cell at some `t` and 20 quarter-turn cells.  In particular,
`H_A(t)=0`, and every other entry of `H_A` and every entry of `H_B` is a
fourth root of unity.

For a fourth root `z`, write

```text
beta(z) = 0  if z is on the real axis  (z in {+1,-1}),
beta(z) = 1  if z is on the imaginary axis (z in {+i,-i}).
```

Then the axes of the quarter-turn cells in family `A` reflect about the
unique opposite cell:

```text
beta(H_A(t+s)) = beta(H_A(t-s)),
beta(S_A(t+s)) = beta(S_A(t-s))       for every nonzero s in Z/21Z.   (1)
```

After rotating family `A`, take `t=0`.  If `m_r` is the number of
imaginary-axis `H_A` entries among the positions congruent to `r mod 7`,
with the zero entry at the center omitted, then

```text
(m_0,m_1,m_2,m_3,m_4,m_5,m_6)
  = (m_0,m_1,m_2,m_3,m_3,m_2,m_1),
m_0 in {0,2},   m_1,m_2,m_3 in {0,1,2,3}.                (2)
```

There are exactly `2*4^3=128` vectors in (2).  Reducing these counts modulo
two leaves exactly eight length-7 axis masks:

```text
00, 18, 24, 3c, 42, 5a, 66, 7e   (hexadecimal).          (3)
```

Equivalently, bit zero vanishes and bits `r` and `-r` agree.  This is a
second-order restriction inside the unique oriented mod-7 quarter-support
branch `(v_A,v_B)=(0x3f,0x7f)`; the first-order binary shadow alone does not
see the axis labels.

## Proof

Put `pi=1+i`, so the ideal `(pi^2)` equals `(2)`.  Every fourth root obeys

```text
z = 1 + beta(z)*pi  (mod pi^2).                           (4)
```

For any odd-length word of 21 fourth roots, (4) makes every nonzero periodic
autocorrelation congruent to `1 mod pi^2`: the constant part sums to 21,
and every axis bit occurs twice in the linear term.

Temporarily fill the zero `H_A(t)` with any fourth root `c`.  At a nonzero
shift `s`, the filled `H_A` word and the all-unit `H_B` word each contribute
`1 mod pi^2`.  Returning the filler to zero removes exactly

```text
c*conjugate(H_A(t+s)) + H_A(t-s)*conjugate(c).             (5)
```

The exact coupled target is

```text
PAF(H_A,s) + PAF(H_B,s) = -2,
```

which is zero modulo `pi^2`.  By (4), expression (5) is divisible by
`pi^2` exactly when the two neighboring roots have the same axis.  This
proves the first equation in (1), independently of their signs and of the
chosen filler.  At a quarter-turn local state, `S_A(j)` and `H_A(j)` are
orthogonal fourth roots, so their axis bits are complementary.  The second
equation follows.

Reflection pairs the positions `s` and `-s`.  Sorting the ten pairs by their
residues modulo seven gives (2): the residue-zero pair contributes zero or
two, while each of the other three reflected residue pairs has three free
binary choices.  Taking parities gives (3).

## Exact certificate

Run:

```bash
python3 verify_q41_axis_reflection.py
```

The standard-library verifier:

- reconstructs all 16 coupled local states from ordered fourth roots;
- checks the `q=41` family and energy counts;
- checks that the `S,H` axes are complementary in every quarter state;
- exhaustively checks all `4*4*4=64` filler/neighbor root triples, proving
  that (5) is divisible by two exactly for equal axes;
- enumerates all `2^10=1,024` reflected axis assignments and verifies the
  128 count vectors and eight parity masks in (2)--(3).

All arithmetic is exact in `Z[i]`.  No floating-point computation, SAT
status, or heuristic search is used.

## Scope and primary context

The result eliminates axis-asymmetric lifts in the `q=41` branch.  It does
not prove that any of the 128 count vectors extends through the remaining
Gaussian sums and autocorrelations, nor that a QLP-42 exists.

Primary background: Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, <https://arxiv.org/abs/1302.0571>;
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>; and Jedwab--Pender, *Two constructions of
quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>.  A targeted search of these primary
sources and the current Discovery Net graph did not locate this
`(1+i)^2`-adic `q=41` reflection law.  Apparent novelty is relative to that
search, not a priority claim.
