# Third-order type classification for the QLP-42 `q=1` branch

## Exact residue theorem

Assume the coupled norm-32 QLP-42 shell has total quarter-turn count `q=1`.
Rotate family `B` so its unique quarter cell is at zero.  The second-order
reflection theorem says that its remaining 20 cells occur in ten reflected
equal/opposite pairs.

Let `a` be the length-21 opposite-cell indicator of family `A`.  Let `b` be
the opposite-cell indicator of family `B`, with `b_0=0` and
`b_s=b_(-s)`.  Let `f` be the equal-cell indicator of the non-quarter part of
`B`, so `f_0=0` and `f_j=1-b_j` for `j != 0`.  For a binary word `w`, put

```text
c_w(s) = sum_j w_j w_(j+s)  in F_2,       1 <= s <= 10.
```

Finally, put `tau_s=1` for `s=4,10` and `tau_s=0` otherwise.  These are the
parities of the divided `S`-autocorrelation targets.

Then the coupled autocorrelation equations after division by `2` and
reduction modulo `pi=1+i` are soluble in local phase-axis bits if and only if

```text
c_a(s) = tau_s + c_b(s),   when b_s=0,
c_a(s) = c_f(s),           when b_s=1.                   (1)
```

The exact XOR of the real/imaginary axes in the active reflected `B` pair is
then forced, uniformly in both cases, to

```text
theta_s = 1 + tau_s + c_b(s) + c_f(s).                  (2)
```

Thus this is the complete third-order `(1+i)`-adic type condition, rather
than only a necessary one: once (1) holds, each of the ten disjoint reflected
pairs can realize its independently prescribed XOR in (2).

## Exhaustive classification

The center energies give

```text
wt(a) + wt(b) = 21.
```

Before (1), the 1,024 reflected `B` type words and complementary-weight `A`
words give exactly

```text
215,008,364 labeled type pairs,
 10,239,544 orbits under cyclic rotation of A.
```

Exhaustively applying (1) leaves

```text
480 reflected B words,
194,439 labeled type pairs,
  9,259 independent-rotation orbits.
```

This is an exact reduction by a factor greater than 1,105.  In particular,
family `B` cannot have zero or two opposite non-quarter cells.  The complete
weight distribution is:

| opposite cells in `B` | `B` masks | labeled pairs | rotation orbits |
|---:|---:|---:|---:|
| 4  | 10  | 420    | 20   |
| 6  | 50  | 3,402  | 162  |
| 8  | 98  | 49,350 | 2,350|
| 10 | 140 | 56,490 | 2,690|
| 12 | 98  | 76,377 | 3,637|
| 14 | 56  | 6,762  | 322  |
| 16 | 25  | 1,575  | 75   |
| 18 | 2   | 42     | 2    |
| 20 | 1   | 21     | 1    |

## Exact sums and exceptional orientation

Equation (2) also determines whether the two roots in each reflected active
pair lie on the same axis or on different axes.  A same-axis pair has sum in

```text
{0, +2, -2, +2i, -2i},
```

whereas a different-axis pair has sum in `{+1+i,+1-i,-1+i,-1-i}`.
Exact dynamic programming through these pair-sum domains, together with all
four coupled Gaussian sum equations, has two consequences:

1. the sum-compatible case totals are 9,259 orbits for case 0, 9,258 for
   cases 1 and 2, and 9,256 for cases 3, 4, and 5;
2. for every surviving `B` mask in every compatible canonical case, exactly
   one of the four previously allowed ordered root pairs at the quarter cell
   remains.

The detailed case and exceptional-orientation counts are in
`case_table.tsv` and `orientation_table.tsv`.

## Proof of (1)

At a non-quarter cell the active transformed component is `pi` times a
Gaussian unit.  Therefore, after dividing an autocorrelation equation by
`2=pi*conjugate(pi)`, every product not involving the quarter center reduces
to one modulo `pi` precisely when both endpoint cells are active.

At shift `s`, reflection makes the two center-cross terms divisible by two.
If `b_s=0`, the `S` cross term is zero, so the divided `S` target directly
forces `c_a(s)+c_b(s)=tau_s`.  If `b_s=1`, the `H` cross term is zero.  The
complement identity for odd length 21 is

```text
c_(1-a)(s) = 1 + c_a(s),
```

and the divided `H` target is one modulo `pi`, giving `c_a(s)=c_f(s)`.
This proves (1).  In the other component the cross term can take either
residue, and direct Gaussian-unit reduction gives (2).

## Reproduction and trust boundary

Run:

```bash
python3 verify_q1_third_order_types.py
```

The standard-library certificate:

- reconstructs all 16 coupled local states and checks the divided cross-term
  residues exactly in `Z[i]`;
- enumerates all `2^21` family-`A` masks and all `2^10` reflected family-`B`
  masks;
- independently obtains the rotation-orbit counts by Burnside's lemma;
- verifies both machine-readable count tables;
- performs exact pair-sum dynamic programming for all six canonical sum
  cases and all four exceptional states.

No floating point, SAT status, heuristic search, or unverified phase lift is
used.  This classifies a finite Gaussian-residue relaxation.  Surviving type
pairs need not satisfy the next `(1+i)`-adic layer or the full integer
autocorrelation equations, so the result does not settle QLP-42.

Primary context: Djokovic--Kotsireas, *Compression of Periodic Complementary
Sequences and Applications*, <https://arxiv.org/abs/1302.0571>;
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>; and Jedwab--Pender, *Two constructions of
quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>.  A targeted primary-source and current
graph search found no matching third-order type classification; apparent
novelty is relative to that search, not a historical-priority claim.
