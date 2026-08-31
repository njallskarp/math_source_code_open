# Third-order axis/sign classification in the QLP-42 `q=41` branch

## Exact residue theorem

Assume the coupled norm-32 QLP-42 shell has total quarter-turn count `q=41`.
Rotate family `A` so its unique opposite cell is at zero.  Put `pi=1+i`.
The second-order reflection theorem says that the 20 unit entries of `H_A`
have reflected axes.

Let `a_0=0` and, for `1 <= s <= 10`, define `a_s=a_(-s)` to be the axis bit
of `H_A(s)`: zero for a real unit and one for an imaginary unit.  Let `b` be
the arbitrary length-21 axis word of the all-unit word `H_B`.  Put

```text
f_0=0,  f_j=1+a_j for j != 0,
c_w(s)=sum_j w_j w_(j+s) in F_2,
E_b(s)=wt(b)+c_b(s) in F_2,
tau_s=1 for s in {4,10}, and tau_s=0 otherwise.
```

Here `f` is the axis word of the 20 unit entries of `S_A`; the axis word of
`S_B` is the complement of `b`.  If `theta_H(s)` and `theta_S(s)` are the
XORs of the two signs at positions `s` and `-s`, then the coupled
autocorrelation equations modulo `pi^3` hold if and only if

```text
theta_H(s) = 1+a_s+c_a(s)+E_b(s),
theta_S(s) = 1+f_s+c_f(s)+E_b(s)+tau_s.                 (1)
```

Consequently the third-order residue layer eliminates no axis pair: all

```text
2^10 * 2^21 = 2,147,483,648
```

labeled pairs `(a,b)` lift, and (1) uniquely fixes the 20 reflected sign
XORs.  The ten reflected pairs are disjoint, and the `S,H` signs in a
quarter local state are independent, so all prescribed XORs are attained.
Modulo cyclic rotation of family `B`, there are exactly

```text
2^10 * 99,880 = 102,277,120
```

axis orbits at this layer.

This no-pruning result is structural, not a failed search: unlike the
`q=1` branch, the next Gaussian residue is absorbed completely by reflected
sign choices.

## Exact-sum intersection

The four Gaussian sum equations do prune these residue lifts.  Let
`n=wt(b)`, the number of imaginary-axis entries of `H_B`.  A necessary
condition, independent of the canonical sum case, is

```text
n = 0 (mod 4).                                           (2)
```

It has a short proof.  The equation `sum(H_A)=0` requires an even number of
nonzero reflected-pair sums on each axis.  Hence the total number of zeros
among the ten `theta_H(s)` is even, equivalently `sum_s theta_H(s)=0`.
If `r=sum_s a_s`, the reflected word `a` has weight `2r`, and

```text
sum_s c_a(s) = binom(2r,2) = r (mod 2).
```

Summing the first line of (1) therefore gives

```text
0 = sum_s E_b(s) = binom(n,2) = n/2 (mod 2),
```

where `n` is even because `sum(H_B)=1`.  This proves (2).

Exact dynamic programming through the forced reflected-pair sum domains,
together with the four Gaussian sum targets, gives the complete counts
below.  A `B`-rotation orbit means that the center of `A` is fixed at zero
and cyclic rotation is factored only in family `B`.

| case | representative `(p,q,x,y)` | possible `n` | labeled axis pairs | `B`-rotation orbits |
|---:|---|---|---:|---:|
| 0 | `(1,0,5,0)`  | `4,8,12,16`    | 268,258,816 | 12,775,936 |
| 1 | `(3,0,4,1)`  | `4,8,12,16`    | 234,375,638 | 11,162,142 |
| 2 | `(3,0,3,-2)` | `0,4,8,12,16`  | 234,376,110 | 11,162,614 |
| 3 | `(3,2,3,2)`  | `4,8,12,16,20` | 200,734,037 | 9,559,985 |
| 4 | `(3,2,2,3)`  | `4,8,12,16,20` | 200,734,037 | 9,559,985 |
| 5 | `(4,1,2,-1)` | `0,4,8,12,16`  | 183,929,820 | 8,759,980 |

The finer distributions by `n` are in `weight_table.tsv`.

## Proof of the residue equations

Write a Gaussian unit as `z=(-1)^sigma i^beta`, with sign bit `sigma` and
axis bit `beta`.  Modulo `pi^3`,

```text
z = 1 + beta*pi + (sigma+beta)*pi^2.
```

For a full odd word of 21 units this gives

```text
PAF(W,s) = 1 + pi^2*(wt(beta)+c_beta(s))  (mod pi^3).    (3)
```

All sign bits cancel in (3).  Fill the zero `H_A(0)` temporarily by a unit.
Removing its two cross terms and using reflected axes gives the first line
of (1); the filler axis cancels.  For `S_A`, replace a temporary unit filler
by the actual opposite-cell entry `pi*u`.  The two `pi*u` cross terms always
contribute one after division by `pi^2` and reduction modulo `pi`, which
gives the second line.  Finally, for odd length 21 the complemented axis
word of `S_B` has the same invariant `wt+c(s)` as `b`.  These reductions are
checked directly in exact Gaussian arithmetic by the certificate.

For the sum intersection, a reflected pair with sign XOR one sums to zero;
with XOR zero it sums to `+2` or `-2` on its prescribed axis.  The verifier
performs exact finite dynamic programming over these domains.  The 21
unpaired signs in each component of family `B` are feasible precisely by
the elementary parity-and-bound criterion for a sum of `n` values in
`{+1,-1}`.

## Reproduction and trust boundary

Run:

```bash
python3 verify_q41_third_order_axes.py
```

The standard-library certificate:

- reconstructs all 16 coupled local states;
- exhaustively checks the removed-unit and `pi*u` cross-term residues in
  exact `Z[i]` arithmetic;
- enumerates all `2^21` family-`B` axis words, grouping them by weight and
  ten-bit autocorrelation signature;
- independently verifies the total `99,880` binary necklaces of length 21
  by Burnside's formula;
- enumerates all `2^10` reflected family-`A` axes against every realized
  signature and all six canonical sum cases;
- verifies `case_table.tsv`, `weight_table.tsv`, and (2).

This classifies the third-order Gaussian residue plus the exact global sums.
It does not impose the full integer nonzero-shift autocorrelations, and it
does not prove that any surviving axis pair extends to a QLP-42 solution.
No floating point, SAT status, heuristic search, or claimed phase lift
beyond the stated layer is used.

Primary context: Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, <https://arxiv.org/abs/1302.0571>;
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; and Jedwab--Pender,
*Two constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>.  A targeted primary-source and current
graph search found no matching third-order `q=41` axis/sign classification;
apparent novelty is relative to that search, not a priority claim.
