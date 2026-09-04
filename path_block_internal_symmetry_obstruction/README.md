# The least internal-symmetry obstruction for path block polytopes

## Result

Let `P_m^(a)` be the path block polytope with nonnegative coordinates
`x_(i,j)`, block sums `R_i=sum_j x_(i,j)`, and inequalities

```text
R_i + R_(i+1) <= 1,  1 <= i < m.
```

The ordinary `h*`-polynomial is gamma-nonnegative, and the equivariant
chain-polytope theorem applies to symmetries induced from the base path.
It does **not** extend to arbitrary coordinate permutations inside the
blocks: the equivariant `h*`-series can fail even to be a polynomial.

Specifically, take `P=P_3^(2)` and let `g` transpose the two coordinates in
the first end block while fixing the other four coordinates.  Then

```text
h*_g(P;t) = (1 + 2t + 6t^2 + 2t^3 + t^4)/(1+t)^2.                  (1)
```

The numerator in (1) has value `4` at `t=-1`, so no denominator factor
cancels.  Consequently the equivariant `h*`-series for the internal `C2`
action is not a polynomial and cannot be gamma-effective.

This is a productwise least path-block obstruction:
when `a=1` the internal group is trivial, while for every `a` the two-block
polytope `P_2^(a)` is the standard `2a`-simplex and has equivariant
`h*`-polynomial `1` under every coordinate-permutation subgroup.  Thus the
no pair with `a<2` or `m<3` can fail, while `(a,m)=(2,3)` gives (1).

## Fixed-point calculation

Write the coordinates of the three two-element blocks as

```text
(x_1,x_2), (b_1,b_2), (c_1,c_2).
```

A lattice point fixed by `g` has `x_1=x_2=u`.  In the `q`-th dilation its
nonnegative integer coordinates satisfy

```text
2u+b_1+b_2 <= q,        b_1+b_2+c_1+c_2 <= q.                      (2)
```

Put `B=b_1+b_2` and then `r=q-B`.  There are `q-r+1` middle-block
compositions, `floor(r/2)+1` choices for `u`, and
`binom(r+2,2)` choices for the last block with sum at most `r`.  Therefore

```text
E_g(q) = sum_(r=0)^q
         (q-r+1)(floor(r/2)+1) binom(r+2,2).                        (3)
```

Let `E_g(t)=sum_(q>=0) E_g(q)t^q`.  Formula (3) is a convolution with
`sum_(B>=0)(B+1)t^B=(1-t)^(-2)`.  Since

```text
floor(r/2)+1 = (2r+3+(-1)^r)/4
```

and `sum binom(r+2,2)t^r=(1-t)^(-3)`, direct differentiation gives

```text
E_g(t) = 1/4 * [ 6t/(1-t)^6
                 + 3/(1-t)^5
                 + 1/((1-t)^2(1+t)^3) ]

       = (1+2t+6t^2+2t^3+t^4)/((1-t)^6(1+t)^3).                    (4)
```

On the six coordinate directions, `g` has one two-cycle and four fixed
points.  The homogenizing direction is also fixed, so the determinant in
the definition of the equivariant `h*`-series is

```text
det(I-t rho_tilde(g)) = (1-t^2)(1-t)^5
                       = (1-t)^6(1+t).                             (5)
```

Multiplying (4) by (5) proves (1).  Its initial coefficients are

```text
1, 0, 5, -8, 12, -16, 20, -24, 28, -32, ...,
```

and the nonzero pole at `t=-1` proves that the tail never terminates.

## Why the two-block case succeeds

`P_2^(a)` is

```text
{x in R_^(2a) : x>=0 and sum_i x_i<=1},
```

the standard simplex.  Add the slack coordinate.  Lattice points in its
`q`-th dilation are the degree-`q` monomials in the `2a` coordinates and the
slack coordinate.  For any coordinate permutation `g`, their character
series is

```text
1/det(I-t rho_tilde(g)).
```

The determinant normalization therefore leaves `h*_g=1`.  This proves the
minimality assertion for all widths, rather than only for the finite widths
checked by the code.

## Reproduction

Requirements: CPython 3.12 or a compatible Python 3 interpreter; standard
library only.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
shasum -a 256 -c SHA256SUMS
```

The checker:

- enumerates (2) directly for the first eight dilations;
- compares 81 coefficients from (3) with the rational series (4);
- reconstructs 81 coefficients of the equivariant series using (5);
- verifies the noncancellation at `t=-1`; and
- checks `h*_g=1` for all 433 pairs of internal cycle types of
  `P_2^(a)`, `2<=a<=7`.

Exact expected output and source hashes are in `EXPECTED_OUTPUT.txt` and
`SHA256SUMS`.

## Literature and graph boundary

Jiang--Yang--Zhong introduce the path block polytopes and prove ordinary
palindromicity and unimodality:
<https://arxiv.org/abs/2607.22008>.  Stapledon defines the equivariant
Ehrhart and `h*` series and emphasizes that the latter need not automatically
be a polynomial: <https://arxiv.org/abs/1003.5875>.  D'Alì--Higashitani prove
gamma-effectiveness for graded order polytopes under poset automorphisms:
<https://arxiv.org/abs/2505.07623>.

Discovery Net height 1949 transfers that theorem to graded chain polytopes
and hence covers the base-path symmetries of the block polytope.  The present
calculation explains why its group hypothesis cannot simply be enlarged to
the internal product of symmetric groups.  Targeted searches on 2026-09-04
for equivariant path block polytopes, internal block permutations, and
equivariant chain-polytope polynomiality found no primary source containing
this example or formula.  Novelty is search-relative; no historical-priority
claim is made.

## Trust boundary

The universal minimality and the failure at `(2,3)` rest on the displayed
generating-function derivation and the definition of equivariant `h*`.
Computation is exact corroboration, not the proof.  The checker trusts
CPython integer/list/tuple arithmetic and SHA-256.  There is no solver,
floating point, randomness, external dataset, generated input, or omitted
certificate.
