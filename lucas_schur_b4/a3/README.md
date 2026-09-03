# The complete canonical Lucas `b = 4` slice

## Result

Let `F_0=0`, `F_1=1`, and

```text
F_(n+1) = e1 F_n + e2 F_(n-1)
```

in `Z[e1,e2]`, and let `{n choose r}_F` be the associated Lucas
binomial.  The last unresolved canonical family at width four is

```text
E_k = {3k+4 choose 4}_F - {4k+3 choose 3}_F,       k >= 2.       (1)
```

Both terms have weighted degree `12k`, where `deg(e1)=1` and
`deg(e2)=2`.

**Theorem.**  For every `k >= 2`, `E_k` is Schur-positive in two
variables.  More precisely,

```text
[s_(12k-r,r)] E_k = 0       for 0 <= r <= 3,
[s_(12k-r,r)] E_k > 0       for 4 <= r <= 6k.       (2)
```

Together with the already proved `(a,b)=(2,4)` theorem and the immediate
even-shift KOH proof for `a=1`, this proves the complete canonical
nontrivial `b=4` slice of the Lucas--Bergeron--Vessenes conjecture.

The proof is a Schur-layer/KOH argument.  It neither asserts nor uses
elementary positivity.

## Ordinary Schur layers

Put

```text
H_k(q) = Gaussian(3k+4,4) - Gaussian(4k+3,3).
```

Let the homogeneous two-variable lift of `H_k` have Schur expansion

```text
Hhat_k = sum_(0 <= i <= 6k) h_k(i) s_(12k-i,i)
       = sum_i h_k(i) e2^i h_(12k-2i).                       (3)
```

Equivalently, because `H_k` is symmetric of degree `12k`, `h_k(i)` is
the `i`th first difference of its coefficient sequence:

```text
h_k(i) = [q^i] (1-q) H_k(q),                  0 <= i <= 6k.  (4)
```

The Gaussian product formula gives

```text
(1-q)H_k(q)
 = product_(nu=1..4)(1-q^(3k+nu)) / ((1-q^2)(1-q^3)(1-q^4))
   - product_(nu=1..3)(1-q^(4k+nu)) / ((1-q^2)(1-q^3)).     (5)
```

Define, with value zero for negative arguments,

```text
P(n) = #{(a,b,c) in N^3 : 2a+3b+4c=n},
Q(n) = #{(a,b)   in N^2 : 2a+3b=n}.                         (6)
```

For degrees at most `6k`, no product of two nonconstant numerator terms
in (5) can contribute: the two smallest exponents in the first product
sum to `6k+3`, and those in the second sum to `8k+3`.  Also
`P(n)-Q(n)=P(n-4)`.  Thus (5) yields the explicit all-parameter formula

```text
h_k(i) = P(i-4)
         - sum_(nu=1..4) P(i-3k-nu)
         + sum_(nu=1..3) Q(i-4k-nu),           0 <= i <= 6k. (7)
```

Formula (7) is already a finite exact Schur expansion of the ordinary
Gaussian difference.  The extra inequality below is what makes its
alternating Lucas image positive.

## The adjacent-layer inequality

Let

```text
R(n) = floor((n^2+6n+12)/12),
S(n) = floor(n/3)+1                                             (8)
```

for `n >= 0`, and set both functions to zero for `n < 0`.  Separating
the parity of the number of parts of size three in (6) gives

```text
P(2j)=R(j),       P(2j+1)=R(j-1),
Q(2j)=S(j),       Q(2j+1)=S(j-1).                           (9)
```

Here `R(n)` counts solutions of `a+2c+3b=n`, and `S(n)` counts solutions
of `a+3b=n`; the closed forms in (8) follow by summing over `b`.

Set

```text
A_j = h_k(2j),             C_j = 2h_k(2j)-h_k(2j+1).        (10)
```

The claim needed below is

```text
A_j >= 0       (0 <= j <= 3k),
C_j >= 0       (0 <= j < 3k).                              (11)
```

For completeness, (7)--(9) reduce (11) to the following two explicit
quasipolynomial calculations.  If `k=2t`, put `u=j-3t`, `v=j-4t`:

```text
A_j = R(j-2)-R(u-1)-2R(u-2)-R(u-3)
      +S(v-1)+S(v-2)+S(v-3),

C_j = 2R(j-2)-R(j-3)+R(u)-R(u-1)-3R(u-2)-R(u-3)
      -S(v)+S(v-1)+S(v-2)+2S(v-3).                         (12)
```

If `k=2t+1`, put `u=j-3t`, `v=j-4t-2`:

```text
A_j = R(j-2)-R(u-2)-R(u-3)-R(u-4)-R(u-5)
      +S(v-1)+S(v-2)+S(v-3),

C_j = 2R(j-2)-R(j-3)-R(u-2)-R(u-4)-2R(u-5)
      -S(v)+S(v-1)+S(v-2)+2S(v-3).                         (13)
```

Here is a short universal verification, included to make clear that
(11) is not being inferred from a finite computation.  The sequence
`R` is nonnegative and nondecreasing, while

```text
T(v)=-S(v)+S(v-1)+S(v-2)+2S(v-3)
    = 0 (v<0), -1 (v=0), and v-1 (v>=1).                   (14)
```

Before the shifted `R` terms activate, (12) or (13) therefore reduces
to `A_j=R(j-2)` and `C_j=2R(j-2)-R(j-3)`, both nonnegative.  The only
partial-activation values are `u=0,1,2` in (12) and `u=2,3,4` in (13).
Direct substitution, using `T(v)>=-1`, reduces their lower bounds to

```text
even k: A >= R(3t-2), R(3t-1)-1, R(3t)-3;
        C >= R(3t-2), R(3t-1)-1, R(3t)-3;

odd  k: A >= R(3t)-1, R(3t+1)-2, R(3t+2)-4;
        C >= R(3t)-2, R(3t+1)-2, R(3t+2)-4.                (15)
```

All entries in (15) are nonnegative for `t>=1`.

It remains to check the intervals on which every shifted `R` argument
has activated.  For `n>=0`, write

```text
R(n)=(n^2+6n)/12+epsilon_n,       5/12 <= epsilon_n <= 1.  (16)
```

For even `k`, on `3t+3 <= j <= 4t+2`, deleting the nonnegative `S`
terms gives quadratic parts

```text
A0=-(3j^2-24jt+6j+36t^2-24t-22)/12,
C0=-(3j^2-24jt+36t^2-12t-31)/12.                           (17)
```

The errors in (16) give `A_j>=A0-43/12` and, by (14),
`C_j>=C0-69/12`.  Both quadratics are concave in `j`; their endpoint
values are respectively

```text
A0: (9t^2+24t-23)/12, (12t^2-2)/12;
C0: (9t^2+30t+4)/12,  (12t^2+12t+19)/12.                  (18)
```

For odd `k`, on `3t+5 <= j <= 4t+4`, the corresponding bounds are
`A_j>=A0-43/12`, `C_j>=C0-62/12`, with endpoint values

```text
A0: (9t^2+36t-23)/12, (12t^2+12t-2)/12;
C0: (9t^2+42t+4)/12,  (12t^2+24t+19)/12.                  (19)
```

All bounds in (18)--(19) are positive for `t>=3`.

On the final intervals, `v>=3` and the two `S` combinations in (12)
and (13) equal `v` and `v-1`, respectively.  For even `k`, the quadratic
parts including `S(n)=n/3` have endpoint values at
`j=4t+3,6t` for `A` and `j=4t+3,6t-1` for `C`:

```text
A0: (12t^2-11)/12, (6t-1)/6;
C0: (3t^2+3t+1)/3, (12t-5)/3.                              (20)
```

The exact `S` combinations exceed those quadratic parts by `2`.
Together with (16), this gives `A_j>=A0-19/12` and
`C_j>=C0-33/12`.  For odd `k`, at `j=4t+5,6t+3` for `A` and
`j=4t+5,6t+2` for `C`, the endpoint values are

```text
A0: (12t^2+12t-11)/12, (12t+1)/12;
C0: (3t^2+6t+1)/3,      (48t-5)/12,                        (21)
```

and `A_j>=A0-19/12`, `C_j>=C0-26/12`.  Concavity again reduces each
interval to its endpoints, and (20)--(21) are positive after the stated
errors for `t>=3`.  The four remaining values `k=2,3,4,5` are the exact
bases:

```text
k=2: 0,0,0,0,1,0,1,0,1,0,1,0,1
k=3: 0,0,0,0,1,0,1,1,2,1,2,1,2,1,2,1,2,0,1
k=4: 0,0,0,0,1,0,1,1,2,1,3,2,4,2,4,2,4,2,4,2,4,1,3,0,2
k=5: 0,0,0,0,1,0,1,1,2,1,3,2,4,3,5,4,6,4,6,4,6,4,6,4,6,3,5,2,4,0,2
```

These are the arrays `[h_k(0),...,h_k(6k)]`; adjacent inspection proves
(11) in the four bases.  This completes the all-parameter proof of
(11).

## Lucas image and positive block decomposition

Let `tau(e1)=e1`, `tau(e2)=-e2`.  It sends `h_n` to `F_(n+1)` and the
homogeneous Gaussian binomial to the corresponding Lucas binomial.
Applying it to (3) gives

```text
E_k = sum_(0 <= i <= 6k)
        (-1)^i h_k(i) e2^i F_(12k-2i+1).                   (22)
```

Put `B_j=h_k(2j+1)=2A_j-C_j`.  Pairing adjacent terms in (22) gives the
explicit all-parameter recurrence-free expansion

```text
E_k = sum_(0 <= j < 3k) e2^(2j)
        (A_j F_(12k-4j+1)-B_j e2 F_(12k-4j-1))
      + A_(3k)e2^(6k).                                    (23)
```

The two-row Lucas kernel proved in the `(a,b)=(2,4)` work is

```text
F_m-2e2 F_(m-2) is Schur-positive for every m>=3.           (24)
```

Indeed, if `ell(n,r)=[s_(n-r,r)]F_(n+1)`, one-box Pieri and the Lucas
recurrence give

```text
[s_(m-1-r,r)](F_m-2e2F_(m-2))
 = ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2) >= 0.              (25)
```

By (11), every block of (23) is

```text
A_j(F_m-2e2F_(m-2)) + C_j e2F_(m-2),                       (26)
```

and is therefore Schur-positive.  The unpaired final term is also
positive.  This proves (1).

The first nonzero ordinary layers are `h_k(4)=1`, `h_k(5)=0` for every
`k>=2`.  Thus the `j=2` block in (23) is exactly
`e2^4F_(12k-7)`.  The Delannoy formula

```text
ell(n,r)=Del(n-r,r)-Del(n-r+1,r-1)
```

or recurrence (25) shows that `F_(12k-7)` contains every allowable
two-row Schur shape positively.  After shifting by `e2^4`, this proves
the strict statement (2).

For an entirely explicit Schur coefficient, combine (7) with

```text
[s_(12k-r,r)]E_k
 = sum_(0 <= i <= r) (-1)^i h_k(i) ell(12k-2i,r-i).         (27)
```

Equations (6)--(9) and the finite Delannoy sum make (27) an
all-parameter formula involving only integer arithmetic.

## Completion of width four

In a canonical nontrivial width-four comparison, `1<=a<4<=c<d` and
`ad=4c`, so `a` is `1`, `2`, or `3`.

* For `a=1`, `d=4c`; the width-four KOH identity

  ```text
  {c+4 choose 4}_F = F_(4c+1)
    +e2^2 F_(c-1)F_(3c-1)
    +e2^4 {2c-2 choose 2}_F
    +e2^6 {c-2 choose 2}_F F_(2c-3)
    +e2^12 {c-2 choose 4}_F
  ```

  makes `{c+4 choose 4}_F-F_(4c+1)` elementary-positive.
* For `a=2`, the earlier six-step KOH/Schur theorem proves
  `{2c+2 choose 2}_F-{c+4 choose 4}_F` Schur-positive for every `c>=4`.
* For `a=3`, integrality forces `c=3k`, `d=4k`, with `k>=2`, and the
  present theorem applies.

Thus there is no remaining canonical `b=4` parameter family.

## Reproducibility and trust boundary

`verify_pairing.py` uses exact q-Pascal arrays and an independently
generated Lucas Schur kernel.  It checks (7), (9), (11), (22), the
positive block reconstruction, the four bases, and strict positivity.
`verify_sparse.py` constructs Lucas binomials directly in `Z[e1,e2]`
from the Sagan--Savage recurrence and verifies (22) as a literal
polynomial identity before converting independently to Schur
coefficients.  Both use arbitrary-precision integers only: no floating
point, randomness, solver, or modular reconstruction.

The computations corroborate the algebra; they are not the universal
proof.  The universal steps are the numerator cutoff leading to (7),
the quasipolynomial bounds (12)--(21), and the Schur kernel (24)--(26).
This public copy preserves the exact source later committed for open access.
The complete slice theorem received a corrected independent accepting review
at height 1525; the checkers remain corroboration rather than the universal
proof.

## Primary-source status

* François Bergeron, *A (q,t)-Overview of q-Analogs*, arXiv:2608.30979,
  states the Lucas comparison and reports bounded verification only:
  https://arxiv.org/abs/2608.30979
* Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, arXiv:1709.06187, proves ordinary unimodality for
  `a<=3` and `b,c>=4` by KOH methods:
  https://arxiv.org/abs/1709.06187
* Bruce Sagan and Carla Savage, *Combinatorial interpretations of
  binomial coefficient analogues related to Lucas sequences*,
  arXiv:0911.3159, supplies the Lucas-binomial polynomial framework and
  recurrence: https://arxiv.org/abs/0911.3159

A fresh arXiv API query on 2026-09-03 found Bergeron's source conjecture
but no paper proving this Lucas `(3,4)` family or the complete Lucas
`b=4` slice.  The committed Discovery Net at height 1506 likewise had no
overlapping result.  The novelty claim is therefore only “apparently new
relative to the searched primary sources and committed graph,” not a
historical-priority claim.
