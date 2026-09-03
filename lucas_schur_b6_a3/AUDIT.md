# Independent-audit roadmap

This file compresses the proof of the provisional canonical `(3,6)`
Lucas theorem into six independently checkable obligations. It is an
aid to a future reviewer, not an independent review and not a new
theorem. A reviewer should rebuild the fragile steps rather than
accepting the recorded hashes alone.

## Claim under review

For `c>=6`, let

```text
E_c={c+6 choose 6}_F-{2c+3 choose 3}_F.
```

The claim is

```text
[s_(6c-r,r)]E_c=0  for 0<=r<=3,
[s_(6c-r,r)]E_c>0  for 4<=r<=3c.
```

The coefficient at `r=4` is one. For `5<=r<=3c`, the claimed lower
bound is

```text
binom(6c-10,r-5)-binom(6c-10,r-6).
```

The complete formulas and conventions are in `README.md`.

## Proof compressed to six obligations

### 1. KOH tail alignment

Starting from the displayed width-six and width-three KOH identities,
check by direct subtraction that for every `c>=16`

```text
H_c=e2^30 H_(c-10)+e2^4 K_c,
H_c=B(c+6,6)-B(2c+3,3),
```

with `K_c` exactly as displayed in `README.md`. The key structural
fact is tail alignment:

```text
e2^30 B(c-4,6)-e2^30 B(2c-17,3)=e2^30 H_(c-10).
```

An independent audit should derive the KOH summands from partitions of
six rather than copying `width_six_koh`. `verify_layers.py` checks the
displayed identities against q-Pascal through `c=100`, but that finite
run is an audit of the symbolic derivation, not its universal
quantifier.

### 2. Exact lower-half layer formula

Put `N=6c-8` and

```text
K_c=sum_(0<=r<=3c-4) k_c(r)e2^r h_(N-2r).
```

For a homogeneous symmetric polynomial `X` of degree `d`, the
coefficient of `e2^r h_(d-2r)` is `[q^r](1-q)X(q,1)`. Expanding the
two Gaussian product numerators only through degree `3c` gives

```text
k_c(r)=g_c(r+4)-g_(c-10)(r-26),
```

where

```text
g_c(i)=P(i)-Q(i)
       -sum_(1<=nu<=6)P(i-c-nu)
       +sum_(1<=mu<nu<=6)P(i-2c-mu-nu)
       +sum_(1<=nu<=3)Q(i-2c-nu).
```

The truncation must be checked at the endpoint `i=3c`: at most two
width-six numerator factors and one width-three numerator factor can
activate. This is the algebraic bridge from KOH to the certificate.
`verify_layers.py` compares it with direct q-Pascal layers.

### 3. Quasipolynomials and affine translation

Split parity in `P` and `Q` to obtain the restricted-partition
functions `T` and `U` in `README.md`. Independently multiply the
thirty residue polynomials by

```text
(1-z)(1-z^2)(1-z^3)^2(1-z^5)
```

and the three `U` residues by `(1-z)(1-z^3)`. The products must give
one. This proves the quasipolynomials without interpolation.

For `c=2t+rho`, substitute them term-by-term into `k_c(2j)` and
`2k_c(2j)-k_c(2j+1)`. The resulting affine terms must agree
symbolically with the formula in obligation 2. The bundled checkers
compare the translation definitionally through `c=200`; that range is
diagnostic, so a reviewer should separately inspect the term builder
for universal equality.

### 4. Four universal inequalities

Only four families remain:

```text
rho=0: A_j=k_c(2j),         j<3t-1,
rho=0: C_j=2A_j-k_c(2j+1), j<3t-2,
rho=1: A_j=k_c(2j),         j<3t,
rho=1: C_j=2A_j-k_c(2j+1), j<3t.
```

For `t>=60`, activation thresholds cut these domains as follows:

```text
family    cells  exact cells  Bernstein polynomials  least stored scalar
rho=0 A      32       3               145                    1/72
rho=0 C      37       5               160                    1/72
rho=1 A      32       3               145                    1/72
rho=1 C      33       5               140                    1/72
total       134      16               590
```

The 16 exact cells contain 68 explicitly evaluated values, all at
least one. Their use of `t=60` is universal because every active `T`
or `U` argument in those cells has zero `t`-slope. Both certificate
engines now assert this bridge explicitly.

On every other cell, substitute `t=60+x` and map its `j` interval to
`0<=z<=1`. Each lower bound has degree at most four in `z`; its five
Bernstein coefficients are polynomials in `QQ_+[x]`. A reviewer
should check: all activation thresholds are present, the order is
stable for `x>=0`, the sign chooses the correct upper/lower residue
bound, and the Bernstein conversion uses degree four even after
degree drop.

The exact finite complement `16<=c<120` contains 20,748 `A`/`C`
values. Every value is strictly positive; the minimum is one in all
four families.

### 5. Lucas transport, pairing, and endpoints

Under `tau(e1)=e1`, `tau(e2)=-e2`, one has `tau(h_n)=F_(n+1)`.
Because both recurrence shifts are even,

```text
E_c=e2^30 E_(c-10)+e2^4 R_c,
R_c=sum_r (-1)^r k_c(r)e2^r F_(N-2r+1).
```

Writing `A_j=k_c(2j)` and `C_j=2A_j-k_c(2j+1)`, pair adjacent terms:

```text
A_j(F_m-2e2 F_(m-2))+C_j e2 F_(m-2).
```

The kernel identity to rebuild from the Lucas recurrence and Pieri is

```text
[s_(m-1-r,r)](F_m-2e2 F_(m-2))
 =ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2).
```

Check both parity endpoints. For odd `c`, the last complete pair has
`m=3`; through the finite complement its smallest `A`/`C` endpoint
coefficient is 20 at `c=17`. For even `c`, the unpaired middle layer
is `k_c(3c-4)e2^(3c-4)F_1`; its finite-complement minimum is 10 at
`c=16`. The universal coverage of these endpoints is already part of
the four domains in obligation 4.

### 6. Bases and strict support

Check `E_6,...,E_15` directly from the lucasnomial recurrence. The
canonical JSON encoding of their ten full Schur rows has SHA-256

```text
1cce6fa1bfef5eda488d69e89c5323d6f43d824e1d02dd16f213a7b64ed34a03.
```

Their least nonzero triple is `(coefficient,c,r)=(1,6,4)`. For the
induction step, verify `k_c(0)=k_c(1)=1`; the first remainder pair
contains `e2^5 F_(6c-9)`. Its ballot coefficients give the displayed
strict lower bound, while every other recurrence contribution is
nonnegative.

## Recommended independent audit order

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -I audit_summary.py
PYTHONDONTWRITEBYTECODE=1 python3 -I verify_fraction.py
PYTHONDONTWRITEBYTECODE=1 python3 -I verify_layers.py --max-c 100
PYTHONDONTWRITEBYTECODE=1 python3 -I verify_symbolic.py
PYTHONDONTWRITEBYTECODE=1 python3 -I verify_sparse.py --max-c 40
shasum -a 256 -c SHA256SUMS
```

The first command is only a compact diagnostic index into the proof.
It rebuilds the standard-library certificate and has expected digest

```text
a6ad7e37daaf1ed124f338c5a1782d55cff85b9376e25146b055ed2cfaed1aa5.
```

For genuine independence, rebuild obligations 1--5 from the displayed
mathematics without importing these Python modules, then compare the
four family counts, margins, ten-base row hash, and endpoint witnesses.
Matching summary values alone is not an independent proof.

## Trust boundary

`audit_summary.py` imports the bundled `Fraction` and q-Pascal
implementations, so it deliberately has no independent evidentiary
weight. It is a deterministic, exact projection that makes silent
coverage failures and boundary disagreements easier to locate. The
universal proof still rests on inspection of the symbolic KOH and
affine translations plus exact arithmetic in the two certificate
engines. No floating point, randomness, interpolation, solver,
modular reconstruction, external generated data, or private state is
used.
