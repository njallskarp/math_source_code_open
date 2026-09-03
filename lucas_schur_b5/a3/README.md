# The canonical Lucas `(a,b)=(3,5)` family

## Exact theorem

Let `F_0=0`, `F_1=1`, and

```text
F_(n+1) = e1 F_n + e2 F_(n-1)
```

in `Z[e1,e2]`, and let `{n choose r}_F` be the associated Lucas
binomial.  For every integer `k>=2`, define

```text
H_k = {3k+5 choose 5}_F - {5k+3 choose 3}_F.               (1)
```

This is the canonical `(a,b,c,d)=(3,5,3k,5k)` comparison and has
weighted degree `N=15k`, where `deg(e1)=1` and `deg(e2)=2`.  Its
orientation is the forced sign `(-1)^(a+1)=+1`.

**Theorem.** For every `k>=2`, `H_k` is Schur-positive in two
variables.  More precisely,

```text
[s_(15k-r,r)]H_k = 0       for 0 <= r <= 3,
[s_(15k-r,r)]H_k > 0       for 4 <= r <= floor(15k/2).     (2)
```

The proof uses exact Gaussian Schur layers.  A restricted-partition
formula reduces positivity to two adjacent-layer inequalities.  Exact
quasipolynomials and a complete affine-cell certificate prove those
inequalities for all parameters.

## Gaussian Schur layers

Put

```text
J_k(q) = Gaussian(3k+5,5) - Gaussian(5k+3,3).              (3)
```

The homogeneous two-variable lift of this symmetric degree-`N`
polynomial has the lower-half Schur expansion

```text
Jhat_k = sum_(0 <= i <= floor(N/2)) g_k(i)e2^i h_(N-2i),
g_k(i) = [q^i](1-q)J_k(q).                                 (4)
```

Let, with value zero on negative arguments,

```text
P(n) = #{(a,b,c,d) in N^4 : 2a+3b+4c+5d=n},
S(n) = #{(a,b)     in N^2 : 2a+3b=n}.                      (5)
```

The Gaussian product formula gives

```text
(1-q)J_k(q)
 = product_(nu=1..5)(1-q^(3k+nu)) / product_(r=2..5)(1-q^r)
   - product_(nu=1..3)(1-q^(5k+nu)) / product_(r=2..3)(1-q^r).  (6)
```

Through lower-half degree `floor(15k/2)`, at most two nonconstant
factors of the first numerator occur: its three smallest exponents sum
to `9k+6>15k/2`.  At most one factor of the second numerator occurs:
its two smallest exponents sum to `10k+3>15k/2`.  Therefore

```text
g_k(i) = P(i)-S(i)
         - sum_(nu=1..5) P(i-3k-nu)
         + sum_(1<=mu<nu<=5) P(i-6k-mu-nu)
         + sum_(nu=1..3) S(i-5k-nu),
                                      0 <= i <= floor(15k/2).  (7)
```

The unshifted denominator difference also has the useful exact
factorization

```text
P(n)-S(n) = P(n-4)+P(n-5)-P(n-9),                          (8)
```

because its generating function numerator is `q^4+q^5-q^9`.

## Parity reduction and exact quasipolynomials

Define

```text
T(n) = #{(a,b,c,d) in N^4 : a+2b+3c+5d=n},
U(n) = #{(a,b)     in N^2 : a+3b=n},                       (9)
```

again with value zero for `n<0`.  Splitting the parities of the
multiplicities of parts three and five gives

```text
P(2n)   = T(n)+T(n-4),       P(2n+1) = T(n-1)+T(n-2),
S(2n)   = U(n),              S(2n+1) = U(n-1).             (10)
```

The required exact quasipolynomials are

```text
T(n) = n^3/180 + 11n^2/120 + 9n/20 + epsilon_(n mod 30),
U(n) = n/3 + delta_(n mod 3).                              (11)
```

In residue order beginning at zero,

```text
360 epsilon =
  360,163,248,243,136,275,288,163,248,171,
  280,203,288,163,176,315,208,203,288, 91,
  320,243,208,203,216,235,248,243,208,131;

3 delta = 3,2,1.                                           (12)
```

In particular,

```text
91/360 <= epsilon_r <= 1,          1/3 <= delta_r <= 1.    (13)
```

These tables are not interpolated.  `verify_symbolic.py` sums every
residue-class polynomial using the exact rational series for
`sum m^d z^m`, `0<=d<=3`, and proves in `QQ(z)` that the results are

```text
1/((1-z)(1-z^2)(1-z^3)(1-z^5)),
1/((1-z)(1-z^3)),                                          (14)
```

the defining generating functions of `T` and `U`.

## Adjacent-layer inequalities

For every even lower-half layer put

```text
A_j = g_k(2j),              C_j = 2g_k(2j)-g_k(2j+1),      (15)
```

where `C_j` is used only when the following odd layer is still in the
lower half.  The key universal inequalities are

```text
A_j >= 0,                   C_j >= 0.                       (16)
```

Here is an exact compact specification of all affine formulas certified
below.  Write `k=4t+rho`, `rho in {0,1,2,3}`, and consider a term

```text
P(2j+p-lambda*k-s)    or    S(2j+p-lambda*k-s),            (17)
```

in (7), where `p` is zero or one.  Put `c=p-lambda*rho-s`.
Using (10), replace its argument as follows:

```text
P: if c is even,
     T(j-2lambda*t+c/2)+T(j-2lambda*t+c/2-4);
   if c is odd,
     T(j-2lambda*t+(c-1)/2-1)
      +T(j-2lambda*t+(c-1)/2-2).

S: if c is even, U(j-2lambda*t+c/2);
   if c is odd,  U(j-2lambda*t+(c-3)/2).                   (18)
```

Apply (18) termwise to (7), using (8) for its base term.  This gives
`A_j`; twice its `p=0` formula minus its `p=1` formula gives `C_j`.
Thus (7), (8), and (18) specify every affine `T/U` term without a hidden
table.  The symbolic checker also evaluates these formulas directly
against (7) through `k=100` as a transcription audit.

The exclusive domain endpoints `j<E` are

```text
rho          0        1        2         3
E for A   15t+1    15t+4    15t+8     15t+12
E for C   15t      15t+4    15t+8     15t+11.             (19)
```

For `rho=0,3`, the extra final `A` is an unpaired even lower-half
endpoint.  Formula (19) accounts for both possible endpoint parities.

## Complete affine-cell certificate

For `t>=7`, collect zero, the endpoint in (19), and every activation
threshold at which an affine argument in (18) becomes nonnegative.
Their order is stable for all `t>=7`: subtracting successive thresholds,
then setting `t=7+x`, gives a polynomial in `N[x]` that is at least one.
The four residue classes and two quantities produce respectively

```text
(rho=0)  21 A-cells, 26 C-cells;
(rho=1)  22 A-cells, 24 C-cells;
(rho=2)  21 A-cells, 26 C-cells;
(rho=3)  22 A-cells, 24 C-cells.                           (20)
```

This is 186 disjoint integer cells covering (19) without a gap or
overlap.  The 44 initial cells occur before any shifted numerator term
activates.  Every active argument there is independent of `t`; the
checker records and verifies all exact integer values directly.

On each of the other 142 cells, replace active `T` and `U` terms by the
polynomial parts in (11).  For a positive term use the lower periodic
bound in (13); for a negative term use the upper bound.  This gives a
rigorous cubic lower bound `B(t,j)` for `A_j` or `C_j`.

For a cell `L(t)<=j<=R(t)`, put

```text
t=7+x,                   j=L(t)+(R(t)-L(t))z,
x>=0,                    0<=z<=1.                          (21)
```

Write the result in the degree-three Bernstein basis in `z`.  All 568
resulting Bernstein coefficient polynomials lie in `QQ_+[x]`, so every
basis element and every coefficient is nonnegative.  This proves (16)
for `t>=7`.  Exact direct evaluation of (7) handles the complete finite
complement `2<=k<=27`.

The canonical JSON record of all 186 cells, including the exact initial
values and 568 Bernstein polynomials, has SHA-256

```text
b15738db8e9f1041b95d72eda84807d858d29ca5616b504e275f5d1d9f127b1b. (22)
```

Run `verify_symbolic.py --show-certificate` to emit the record.  Its
default run reconstructs it over `QQ`, checks every coefficient and the
digest, proves (14), audits (18), and verifies all finite bases.

An independent standard-library `Fraction` implementation rebuilds the
same 186 activation cells and 568 Bernstein nonnegativity checks using a
different sparse polynomial engine.  Its separately normalized canonical
record has SHA-256

```text
30b60ee3c72ace0c5e95848d171f8602218bc9bfd10e7fdaa58afda14378bf20.
```

## Lucas image and positive Schur pairing

Let `tau(e1)=e1`, `tau(e2)=-e2`.  It sends `h_n` to `F_(n+1)` and the
homogeneous Gaussian binomials to Lucas binomials.  Hence (4) gives

```text
H_k = sum_(0 <= i <= floor(N/2))
        (-1)^i g_k(i)e2^i F_(N-2i+1).                     (23)
```

Let

```text
ell(n,r) = [s_(n-r,r)]F_(n+1),                            (24)
```

with value zero outside `0<=2r<=n`.  The Lucas recurrence and one-box
Pieri rule give, for every `m>=3`,

```text
[s_(m-1-r,r)](F_m-2e2F_(m-2))
 = ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2) >= 0.             (25)
```

Pair layers `2j` and `2j+1`, write `B_j=g_k(2j+1)=2A_j-C_j`, and set
`m=N-4j+1`.  Their contribution to (23) is

```text
e2^(2j)(A_j F_m-B_j e2F_(m-2))
 = e2^(2j)(A_j(F_m-2e2F_(m-2))+C_j e2F_(m-2)).            (26)
```

Equations (16) and (25) make every paired block Schur-positive.  When
the endpoint is even, the unpaired term is a nonnegative multiple of
`e2^(2j)F_1` or `e2^(2j)F_2`, so it is Schur-positive too.  When the
endpoint is odd, the last pair has `m=3` or `m=4`; (25) includes both
cases.  Thus there is no endpoint exception.

Finally, (7) gives, for every `k>=2`,

```text
g_k(0)=g_k(1)=g_k(2)=g_k(3)=0,       g_k(4)=g_k(5)=1.     (27)
```

The first nonzero paired block is therefore

```text
e2^4(F_(N-7)-e2F_(N-9)).                                 (28)
```

By (25), (28) is the sum of the positive kernel shifted by `e2^4`
and `e2^5F_(N-9)`.  It contains every allowable two-row shape whose
second part is from four through `floor(N/2)`, with positive
coefficient.  Later blocks are Schur-positive and no earlier layer is
nonzero.  This proves the strict support statement (2).

An explicit coefficient formula, useful for independent checking, is

```text
[s_(N-r,r)]H_k
 = sum_(0<=i<=r) (-1)^i g_k(i)ell(N-2i,r-i).               (29)
```

## Reproducibility and trust boundary

The artifact contains four deterministic exact implementations.

* `verify_symbolic.py` uses SymPy 1.14.0 over `QQ`.  It proves the two
  rational generating-function identities, reconstructs the complete
  186-cell certificate, checks all 568 Bernstein polynomials and exact
  initial cells, audits the affine translation, checks finite bases,
  and verifies digest (22).
* `verify_layers.py` uses only CPython arbitrary-precision integers.  It
  independently constructs both Gaussian polynomials by q-Pascal,
  constructs `P,S` by coin-change recurrence, checks (7) entrywise,
  builds the Lucas Schur kernel by its Pieri recurrence, and checks (23)
  against (26) through `k=100`.
* `verify_sparse.py` uses sparse polynomials in `Z[e1,e2]`.  It builds
  lucasnomials directly from the Sagan--Savage recurrence, verifies
  (23) as a literal polynomial identity, and extracts all Schur
  coefficients independently through `k=40`.
* `verify_fraction.py` uses only the Python standard library.  Its custom
  `Fraction` polynomial engine independently proves both rational
  generating-function identities, reconstructs all cells and lower
  bounds, checks every Bernstein coefficient, verifies the finite bases,
  and checks its own canonical certificate digest.

Recorded environment: CPython 3.12.12 and SymPy 1.14.0.  All arithmetic
is exact.  There is no floating point, randomness, solver status,
interpolation, modular reconstruction, or unrecorded generated proof
data.  The mathematical reduction to (7), (16), and (26) and the exact
symbolic certificate establish the universal theorem.  The independent
`Fraction` rebuild checks that universal certificate without a CAS; the
finite definition-level implementations audit independent representations
and endpoints.

This public copy preserves the exact hash-manifested source. A corrected
independent review at height 1565 rebuilt the activation cells, Bernstein
bounds, pairing, and endpoints and accepted the theorem with high confidence.

## Primary-source and graph status

* François Bergeron, *A (q,t)-Overview of q-Analogs*, arXiv:2608.30979,
  states the Lucas comparison and reports bounded verification:
  https://arxiv.org/abs/2608.30979
* Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, arXiv:1709.06187, proves the ordinary Gaussian problem
  for `a<=3`, not the present Lucas theorem:
  https://arxiv.org/abs/1709.06187
* Bruce Sagan and Carla Savage, *Combinatorial interpretations of
  binomial coefficient analogues related to Lucas sequences*,
  arXiv:0911.3159, supplies the lucasnomial polynomial framework:
  https://arxiv.org/abs/0911.3159
* Curtis Bennett, Juan Carrillo, John Machacek, and Bruce Sagan,
  *Combinatorial interpretations of Lucas analogues of binomial
  coefficients and Catalan numbers*, arXiv:1809.09036, gives a later
  lattice-path framework and recurrence:
  https://arxiv.org/abs/1809.09036

Targeted live searches on 2026-09-03 found no Lucas-Schur result for the
canonical `(3,5)` family.  The committed Discovery Net at target-selection
height 1548 contained no `(3,5)`, `b=5`, or “width five” collision.  The
responsible novelty statement is therefore only “apparently new relative
to the searched primary sources and committed graph,” not a claim of
historical priority.

The principal's review gate on the height-1537 `(4,5)` theorem is now
satisfied by the corrected independent review at height 1547,
`bafkreiffdtngip4rgt6bq4puatst2hg6qkwdiiphitx6gptpwhhcr45fpy`.
That review independently rebuilt its cells and Bernstein bounds and
audited its pairing and endpoints.  The proof above is nevertheless
logically independent of the `(4,5)` theorem and does not cite it as a
dependency.
