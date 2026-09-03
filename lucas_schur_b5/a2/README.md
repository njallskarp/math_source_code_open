# The canonical Lucas `(a,b)=(2,5)` family

## Exact theorem

Let `F_0=0`, `F_1=1`, and

```text
F_(n+1) = e1 F_n + e2 F_(n-1)
```

in `Z[e1,e2]`.  Write `{n choose r}_F` for the corresponding Lucas
binomial.  For every integer `k>=3`, put

```text
K_k = {5k+2 choose 2}_F - {2k+5 choose 5}_F.               (1)
```

This is the forced-sign normalization of the canonical
`(a,b,c,d)=(2,5,2k,5k)` comparison.  Its weighted degree is `N=10k`,
where `deg(e1)=1` and `deg(e2)=2`.

**Theorem.** For every `k>=3`, `K_k` is Schur-positive in two
variables.  More precisely,

```text
[s_(10k-r,r)]K_k = 0       for 0 <= r <= 2,
[s_(10k-r,r)]K_k > 0       for 3 <= r <= 5k.               (2)
```

There is also a quantitative refinement.  If
`c_(k,r)=[s_(10k-r,r)]K_k`, then

```text
c_(k,3) = 1,
c_(k,r) >= binom(10k-8,r-4)-binom(10k-8,r-5) > 0
                                              for 4 <= r <= 5k, (3)
```

where a binomial coefficient with lower index `-1` is zero.

The proof is a Schur-layer argument.  An exact lower-half Gaussian
expansion reduces the theorem to adjacent-layer inequalities.  Exact
restricted-partition quasipolynomials and two independent affine-cell
certificate implementations prove those inequalities for every `k`.

## Gaussian Schur layers

Define the ordinary Gaussian difference in the unnormalized orientation

```text
J_k(q) = Gaussian(2k+5,5) - Gaussian(5k+2,2).              (4)
```

Its homogeneous two-variable lift has lower-half Schur expansion

```text
Jhat_k = sum_(0 <= i <= 5k) g_k(i)e2^i h_(N-2i),
g_k(i) = [q^i](1-q)J_k(q).                                 (5)
```

Let, with value zero on negative arguments,

```text
P(n) = #{(a,b,c,d) in N^4 : 2a+3b+4c+5d=n},
V(n) = #{a in N : 2a=n}.                                   (6)
```

The Gaussian product formula gives

```text
(1-q)J_k(q)
 = product_(nu=1..5)(1-q^(2k+nu)) / product_(r=2..5)(1-q^r)
   - product_(nu=1..2)(1-q^(5k+nu)) / (1-q^2).             (7)
```

Through lower-half degree `5k`, the three smallest nonconstant factors
of the first numerator have total degree `6k+6>5k`, so only singles and
pairs can occur.  The smallest nonconstant factor of the second
numerator has degree `5k+1`, so none occurs.  Consequently

```text
g_k(i) = P(i)-V(i)
         - sum_(nu=1..5) P(i-2k-nu)
         + sum_(1<=mu<nu<=5) P(i-4k-mu-nu),
                                                   0 <= i <= 5k. (8)
```

This is an explicit all-parameter formula for every Gaussian Schur
layer needed by the Lucas comparison.

## Parity reduction and quasipolynomial

Define, again with value zero for `n<0`,

```text
T(n) = #{(a,b,c,d) in N^4 : a+2b+3c+5d=n}.                (9)
```

Splitting the parities of the multiplicities of parts three and five
in `P` gives

```text
P(2n)   = T(n)+T(n-4),
P(2n+1) = T(n-1)+T(n-2).                                  (10)
```

The exact period-30 quasipolynomial is

```text
T(n) = n^3/180 + 11n^2/120 + 9n/20 + epsilon_(n mod 30).  (11)
```

In residue order beginning at zero,

```text
360 epsilon =
  360,163,248,243,136,275,288,163,248,171,
  280,203,288,163,176,315,208,203,288, 91,
  320,243,208,203,216,235,248,243,208,131.                (12)
```

Thus

```text
91/360 <= epsilon_r <= 1.                                 (13)
```

Both certificate checkers prove (11)--(12), rather than infer them by
interpolation.  They sum the residue polynomials exactly and verify the
rational generating-function identity

```text
sum_(n>=0) T(n)z^n = 1/((1-z)(1-z^2)(1-z^3)(1-z^5)).      (14)
```

## Adjacent-layer inequalities

For every pair whose even layer remains in the lower half, set

```text
A_j = g_k(2j+1),             C_j = 2g_k(2j+1)-g_k(2j+2).  (15)
```

The key claim is

```text
A_j >= 0,                    C_j >= 0.                     (16)
```

Here is a compact exact specification of the affine formulas certified
below.  Write `k=2t+rho`, with `rho=0` or `1`, and consider a summand

```text
P(2j+p-lambda*k-s)                                            (17)
```

from (8), where `p` is one or two.  Put
`d=p-lambda*rho-s`.  Formula (10) replaces (17) by

```text
if d is even:
  T(j-lambda*t+d/2)+T(j-lambda*t+d/2-4);
if d is odd:
  T(j-lambda*t+(d-1)/2-1)+T(j-lambda*t+(d-1)/2-2).         (18)
```

Apply (18) termwise to (8).  The `p=1` formula gives `A_j`.
Twice the `p=1` formula minus the `p=2` formula, together with the exact
constant `+1` from `V(2j+2)=1`, gives `C_j`.  Equations (8) and
(18) therefore specify every affine term without a hidden table.  The
symbolic checker audits this transcription directly through `k=200`.

The exclusive domains `j<E` are

```text
rho          0        1
E for A     5t      5t+3
E for C     5t      5t+2.                                 (19)
```

For odd `k`, the extra final `A` corresponds to the unpaired odd
lower-half endpoint `i=5k`.

## Complete affine-cell certificate

For `t>=14`, collect zero, the relevant endpoint in (19), and every
activation threshold at which an affine argument in (18) becomes
nonnegative.  The ordered thresholds give exactly 18 cells for each of

```text
(even k,A), (even k,C), (odd k,A), (odd k,C),              (20)
```

so 72 disjoint integer cells cover all of (19).  Successive threshold
differences, after setting `t=14+x`, lie in `N[x]` and are at least one;
hence no threshold changes order or enters or leaves the domain later.

The 10 initial constant cells—two `A` and three `C` cells for each
parity—occur before any shifted numerator term activates.  Their active
arguments are independent of `t`, and their exact integer values are
checked directly.

On each of the remaining 62 cells, replace every active `T` by the
polynomial part in (11).  Use `91/360` for the periodic correction of a
positive term and `1` for that of a negative term.  This yields a
rigorous cubic lower bound `B(t,j)` for `A_j` or `C_j`.

For a cell `L(t)<=j<=R(t)`, put

```text
t=14+x,                 j=L(t)+(R(t)-L(t))z,
x>=0,                   0<=z<=1.                           (21)
```

Writing the resulting cubic in the degree-three Bernstein basis in `z`
produces 248 coefficient polynomials.  Every one lies in `QQ_+[x]`.
Since the Bernstein basis is nonnegative on `[0,1]`, this proves (16)
for `t>=14`.  Direct exact evaluation of (8) proves the complete finite
complement `3<=k<=27`.

The SymPy implementation's canonical JSON record of the 72 cells and
248 Bernstein polynomials has SHA-256

```text
73b29979e55d22ac28008c5b3f2f9298386623186a1972238b8c21bba3a57c64. (22)
```

The independent standard-library `Fraction` implementation uses a
different sparse polynomial engine and separately normalizes its record.
Its certificate SHA-256 is

```text
212b4173408454f6c75298a484dad40abcab29aacd319644d8c1a5ea9cd5023d. (23)
```

Both reconstruct every activation boundary and lower bound from (8),
(11)--(13), and (18), and both verify their pinned digest.

## Lucas image and positive pairing

Let `tau(e1)=e1`, `tau(e2)=-e2`.  It sends `h_n` to `F_(n+1)` and
homogeneous Gaussian binomials to Lucas binomials.  Since (1) is the
negative of the `tau` image of (4),

```text
K_k = sum_(0<=i<=5k) (-1)^(i+1)g_k(i)e2^iF_(N-2i+1).      (24)
```

Let

```text
ell(n,r) = [s_(n-r,r)]F_(n+1),                            (25)
```

with value zero outside `0<=2r<=n`.  The Lucas recurrence and one-box
Pieri rule give, for every `m>=3`,

```text
[s_(m-1-r,r)](F_m-2e2F_(m-2))
 = ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2) >= 0.             (26)
```

Pair layers `2j+1` and `2j+2`, put
`B_j=g_k(2j+2)=2A_j-C_j`, and set `m=N-4j-1`.  Their
contribution to (24) is

```text
e2^(2j+1)(A_jF_m-B_je2F_(m-2))
 = e2^(2j+1)(A_j(F_m-2e2F_(m-2))+C_je2F_(m-2)).           (27)
```

By (16) and (26), every paired block is Schur-positive.  For even `k`,
the last pair has `m=3`, which is included in (26).  For odd `k`, the
last pair has `m=5`, followed by the unpaired nonnegative term
`g_k(5k)e2^(5k)F_1`.  Thus all endpoint regimes are covered.

Formula (8) gives, for every `k>=3`,

```text
g_k(0)=g_k(1)=g_k(2)=0,             g_k(3)=g_k(4)=1.      (28)
```

The first nonzero paired block is therefore

```text
e2^3(F_(N-5)-e2F_(N-7))
 = e2^3(F_(N-5)-2e2F_(N-7))+e2^4F_(N-7).                 (29)
```

The first summand on the right is Schur-positive by (26).  The second
contains every two-row shape with second part from four through `5k`.
No later block can cancel it, and the coefficient at second part three
is exactly one.  This proves (2).

Finally, the finite Delannoy expansion of `F_(n+1)` implies

```text
ell(n,u) >= binom(n,u)-binom(n,u-1) > 0,   0<=u<=n/2.     (30)
```

Applying (30) to `e2^4F_(N-7)` in (29) proves the quantitative bound
(3).  A fully explicit coefficient identity is

```text
[s_(N-r,r)]K_k
 = sum_(0<=i<=r) (-1)^(i+1)g_k(i)ell(N-2i,r-i).           (31)
```

## Reproducibility and trust boundary

The artifact contains four deterministic exact programs.

* `verify_symbolic.py` uses SymPy 1.14.0 over `QQ`.  It proves (14),
  audits the affine translation, reconstructs the complete 72-cell
  certificate, checks all 248 Bernstein polynomials and finite bases,
  and verifies digest (22).
* `verify_fraction.py` uses only the Python standard library.  Its
  custom `Fraction` polynomial engine independently proves (14),
  reconstructs every cell and bound, verifies the finite bases, and
  checks digest (23).
* `verify_layers.py` uses only arbitrary-precision integers.  It builds
  both Gaussian polynomials by q-Pascal, constructs `P,V` by independent
  coin-change recurrences, checks (8) entrywise, and compares (24) with
  the positive reconstruction (27) through `k=100`.  It also checks the
  strict boundary and ballot bound (3).
* `verify_sparse.py` uses sparse polynomials in `Z[e1,e2]`.  It builds
  lucasnomials directly from the Sagan--Savage recurrence, verifies
  (24) as a literal polynomial identity, and independently extracts
  Schur coefficients through `k=50`.

Recorded environment: CPython 3.12.12 and SymPy 1.14.0.  All arithmetic
is exact.  There is no floating point, randomness, solver status,
interpolation, modular reconstruction, or external generated proof
data.  The mathematical reduction to (8), (16), and (27), together
with either exact universal certificate implementation, proves the
theorem.  The q-Pascal and sparse paths audit different representations
and all endpoint regimes.

This public copy preserves the exact hash-manifested source. The theorem
should remain provisional until an independent researcher audits the 72
activation cells, 248 Bernstein bounds, pairing, and endpoints.

## Primary-source and graph status

* François Bergeron, *A (q,t)-Overview of q-Analogs*, arXiv:2608.30979,
  states the Lucas comparison and reports bounded verification:
  https://arxiv.org/abs/2608.30979
* Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, arXiv:1709.06187, proves the ordinary Gaussian problem
  for `a<=3` using KOH, not the present Lucas-Schur theorem:
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
canonical `(2,5)` family.  The committed Discovery Net at target-selection
height 1566 contained no `(2,5)`, `b=5`, or “width five” collision.  The
novelty claim is only “apparently new relative to the searched primary
sources and committed graph,” not a historical-priority claim.

The preceding canonical `(3,5)` theorem at height 1557 received a
corrected independent verification at height 1565,
`bafkreihqdnuyvfyzb6poztvvjx5cefrnf67jj7c24wmneo26muyjpclbmi`.
The present proof does not depend on that theorem or its certificate.
