# Independent-audit roadmap

This file compresses the proof of the provisional canonical `(2,6)`
Lucas theorem into six independently checkable obligations. It is an
aid to a future reviewer, not an independent review and not a new
theorem. A reviewer should rebuild the fragile steps rather than
accepting the recorded hashes alone.

## Claim under review

For `c>=6`, let

```text
D_c={3c+2 choose 2}_F-{c+6 choose 6}_F.
```

The claim is

```text
[s_(6c-r,r)]D_c=0  for 0<=r<=2,
[s_(6c-r,r)]D_c>0  for 3<=r<=3c.
```

The coefficient at `r=3` is one. For `4<=r<=3c`, the claimed lower
bound is

```text
binom(6c-8,r-4)-binom(6c-8,r-5).
```

The complete formulas and conventions are in `README.md`.

## Proof compressed to six obligations

### 1. KOH tail alignment

Starting from the displayed width-six KOH identity and fifteen
iterations of the width-two identity, check by subtraction that for
every `c>=16`

```text
H_c=e2^30 H_(c-10)+e2^3 K_c,
H_c=B(c+6,6)-B(3c+2,2),
```

with `K_c` exactly as displayed in `README.md`. The tail alignment is

```text
e2^30(B(c-4,6)-B(3c-28,2))=e2^30 H_(c-10).
```

At exponent two, independently check

```text
h_(c-2)h_(5c-2)-h_(6c-4)=e2 h_(c-3)h_(5c-3),
```

which explains the odd factor `e2^3` in the remainder recurrence. An
independent audit should derive the width-six summands from partitions
of six rather than copying `width_six_koh`. `verify_layers.py` checks
the displayed identities against q-Pascal through `c=100`; this finite
run audits, but does not supply, the symbolic universal derivation.

### 2. Exact lower-half layer formula

Put `N=6c-6` and

```text
K_c=sum_(0<=r<=3c-3) k_c(r)e2^r h_(N-2r).
```

For a homogeneous symmetric polynomial `X` of degree `d`, the
coefficient of `e2^r h_(d-2r)` is `[q^r](1-q)X(q,1)`. Expanding the
Gaussian product numerator through lower-half degree `3c` gives

```text
k_c(r)=g_c(r+3)-g_(c-10)(r-27),
```

where

```text
g_c(i)=P(i)-V(i)
       -sum_(1<=nu<=6)P(i-c-nu)
       +sum_(1<=mu<nu<=6)P(i-2c-mu-nu).
```

At the endpoint `i=3c`, at most two width-six numerator factors can
activate: any triple has degree at least `3c+6`. This is the
algebraic bridge from KOH to the certificate. `verify_layers.py`
compares the formula with direct q-Pascal layers.

### 3. Quasipolynomial, affine translation, and width-two correction

Split parity in `P` to obtain the restricted-partition function `T`
in `README.md`. Independently multiply its thirty residue polynomials
by

```text
(1-z)(1-z^2)(1-z^3)^2(1-z^5).
```

The product must be one. This proves the quasipolynomial without
interpolation.

For `c=2t+rho`, substitute `T` term-by-term into `k_c(2j)` and
`2k_c(2j)-k_c(2j+1)`. The width-two term `V` must be handled
separately. It contributes nothing to `A_j=k_c(2j)`. In the odd layer
it contributes

```text
-V(2j+4)+V(2j-26)=-1+1_(j>=13),
```

and therefore contributes `+1` to `C_j` exactly for `0<=j<=12`.
This explains the explicit activation boundary `j=13`.

The bundled checkers compare the affine translation definitionally
through `c=200`; that range is diagnostic, so a reviewer should also
inspect the term builder for universal equality.

### 4. Four universal inequalities

Only four families remain:

```text
rho=0: A_j=k_c(2j),         j<3t-1,
rho=0: C_j=2A_j-k_c(2j+1), j<3t-1,
rho=1: A_j=k_c(2j),         j<3t+1,
rho=1: C_j=2A_j-k_c(2j+1), j<3t.
```

For `t>=60`, activation thresholds cut these domains as follows:

```text
family    cells  exact cells  Bernstein polynomials  least stored scalar
rho=0 A      32       3               145                    1/72
rho=0 C      32       6               130                    1/72
rho=1 A      32       3               145                    1/72
rho=1 C      36       6               150                    1/72
total       132      18               570
```

The 18 exact cells contain 66 explicitly evaluated values, all at
least one. Their `t=60` evaluation is universal because every active
`T` argument in those cells has zero `t`-slope. Both certificate
engines now assert this bridge explicitly.

On every other cell, substitute `t=60+x` and map the `j` interval to
`0<=z<=1`. Each lower bound has degree at most four in `z`; its five
Bernstein coefficients are polynomials in `QQ_+[x]`. A reviewer
should check completeness and stable ordering of activation
thresholds, the sign choice for upper/lower residue bounds, the
separate `j=13` correction boundary, and degree-four Bernstein
conversion after any degree drop.

The exact finite complement `16<=c<120` contains 20,852 `A`/`C`
values. Every value is strictly positive; the minimum is one in all
four families.

### 5. Lucas transport, pairing, and endpoints

Under `tau(e1)=e1`, `tau(e2)=-e2`, one has `tau(h_n)=F_(n+1)` and
`D_c=-tau(H_c)`. Since the recurrence shift is even,

```text
D_c=e2^30 D_(c-10)+e2^3 R_c,
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

For even `c`, the last complete pair has `m=3`; its smallest
finite-complement `A`/`C` endpoint coefficient is 8 at `c=16`. For odd
`c`, the last complete pair has `m=5` and minimum 21 at `c=17`, then
the unpaired middle term is `k_c(3c-3)e2^(3c-3)F_1`, with minimum one
at `c=17`. Universal endpoint coverage is part of the four domains in
obligation 4.

### 6. Bases and strict support

Check `D_6,...,D_15` directly from the lucasnomial recurrence. The
canonical JSON encoding of their ten full Schur rows has SHA-256

```text
fb0b357c4b0c616962253046f4f8510269a0cb4e6ea8427127ade7d1507198ff.
```

Their least nonzero triple is `(coefficient,c,r)=(1,6,3)`. For the
induction step, the first paired remainder terms are

```text
e2^3(F_(6c-5)-e2 F_(6c-7)).
```

Split this using the positive two-row kernel. The remaining
`e2^4 F_(6c-7)` supplies the ballot lower bound for every second part
from four through `3c`; the kernel supplies coefficient one at second
part three.

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
77593a7ce033cd31e707a541a5ece1e281af64d0502b931ade887bc3e6826368.
```

For genuine independence, rebuild obligations 1--5 from the displayed
mathematics without importing these modules, then compare the four
family counts, exact margins, correction boundary, ten-base row hash,
and endpoint witnesses. Matching summary values alone is not an
independent proof.

## Trust boundary

`audit_summary.py` imports the bundled `Fraction` and q-Pascal
implementations, so it deliberately has no independent evidentiary
weight. It is a deterministic exact projection intended to expose
silent coverage failures and boundary disagreements. The universal
proof still rests on inspection of the KOH and affine translations
plus exact arithmetic in the two certificate engines. No floating
point, randomness, interpolation, solver, modular reconstruction,
external generated data, or private state is used.
