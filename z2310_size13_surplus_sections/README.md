# The size-13 surplus-section obstruction in `Z/2310Z`

## Theorem

There is no spectral pair `(A,Lambda)` in `Z/2310Z` with

```text
|A| = |Lambda| = 13.
```

Consequently, `Z/2310Z` has no spectral subset of cardinality 13. The
proof is exact and structural. It uses no raw subset enumeration, solver,
floating point, or unproved phase classification.

## Setup and imported inputs

Write

```text
2310 = 210*11,
Z/2310Z ~= Z/210Z x Z/11Z.
```

For a set `E`, let `E_j` denote its section on level `j in Z/11Z`, and
let `m_E` be its mask polynomial. We use the following published facts.

1. Spectral-to-tiling holds in `Z/210Z` by the four-prime theorem of
   Kiss--Malikiosis--Somlai--Vizer.
2. If `Phi_(11d)|m_E`, the levelwise cuboid lemma makes every `d`-cuboid
   evaluation on the eleven sections equal. In particular,

   ```text
   E^d[Delta] = 11 E_j^d[Delta].
   ```

3. In a spectral pair, every nonzero difference in either member gives a
   mask zero of the opposite member at the corresponding character order.

The remaining arguments are contained below.

## Step 1: exact surplus-section frontier

Neither mask contains `Phi_11`: evaluating a putative divisibility at one
would make `11` divide `13`. Projection of each set to `Z/210Z` is
therefore injective. Indeed, a collision in the projection of one member
would be an order-11 difference and would force `Phi_11` into the other
mask.

If the projected restrictions of the spectrum characters were pairwise
orthogonal, they would give a spectral 13-set in `Z/210Z`. The four-prime
theorem would make that set tile, impossible because `13` does not divide
`210`. Hence some projected inner product fails. Its first-coordinate
difference has an order `d|210`, its second-coordinate difference is
nonzero, and

```text
Phi_(11d) divides m_A,     Phi_d does not divide m_A.       (1)
```

The levelwise cuboid lemma supplies a cuboid with

```text
0 != A^d[Delta] = 11 c,     c=A_j^d[Delta] in Z.
```

Nonnegativity and the `{-1,0,1}` cuboid coefficients give

```text
11 <= |A^d[Delta]| <= 13.
```

Thus `|A^d[Delta]|=11` and `|c|=1`. Every one of the eleven sections is
nonempty. Distributing thirteen points into eleven nonempty sections gives
exactly one of the two multisets

```text
D = (2,2,1,1,1,1,1,1,1,1,1),
T = (3,1,1,1,1,1,1,1,1,1,1).                            (2)
```

Applying the same argument to the symmetric pair proves that `Lambda`
also has one of the two patterns in (2). In particular, `Lambda` has a
singleton level, and after choosing a point on it, the other twelve points
occupy all ten other levels.

## Step 2: coefficient equality for every cross-level difference

Take two `Lambda` points on distinct 11-levels. Write their
first-coordinate difference as `x` and their nonzero level difference as
`t`. If `omega` is a primitive eleventh root, orthogonality gives

```text
sum_(j=0)^10 omega^(t j) S_j(x) = 0,
S_j(x) = sum_(a in A_j) exp(2*pi*i*x*a/210).               (3)
```

Let `d` be the order of `x` in `Z/210Z`. Every `S_j(x)` lies in
`K=Q(zeta_d)`. Since `gcd(d,11)=1`,

```text
[Q(zeta_(11d)):Q(zeta_d)] = phi(11d)/phi(d) = 10.
```

Thus `Phi_11` is the minimal polynomial of `omega` over `K`. Reindex (3)
by the permutation `j -> t j` of `Z/11Z`. The resulting degree-at-most-10
polynomial over `K` vanishes at `omega`, so it is a scalar multiple of
`Phi_11`. Therefore

```text
S_0(x)=S_1(x)=...=S_10(x).                                (4)
```

Both patterns in (2) have singleton sections. Hence the common value in
(4) has modulus one.

## Step 3: the two-double pattern has only four phase cells

Assume first that `A` has pattern `D`. Let the first-coordinate
differences inside its two double sections be `u` and `v`. For every
cross-level difference `x` of `Lambda`, equation (4) says that the sum of
the two unit phases in each double section has modulus one. If `z` is the
ratio of those phases, then

```text
|1+z|=1,     |z|=1,
```

so `Re(z)=-1/2` and `z` is a primitive cube root. With
`mu=exp(2*pi*i/3)`,

```text
(exp(2*pi*i*x*u/210), exp(2*pi*i*x*v/210))
    lies in {mu,mu^2}^2.                                  (5)
```

Choose `lambda_0` on a singleton level of `Lambda`. Relative to
`lambda_0`, every other point belongs to one of the four cells in (5).
Two points in the same cell cannot lie on different levels: their mutual
phase pair would be `(1,1)`, while (5), applied to that cross-level pair,
requires both coordinates to be primitive cube roots. Thus each cell can
meet at most one `Lambda` level.

The other twelve points would consequently occupy at most four levels.
They must occupy all ten levels other than the singleton base level. This
contradiction excludes pattern `D` for `A`.

## Step 4: a four-unit-vector lemma

We need one elementary geometric fact.

**Lemma.** If four unit complex numbers `w_1,w_2,w_3,w_4` have sum zero,
then their multiset is a union of two antipodal pairs.

**Proof.** Put `P=w_1*w_2*w_3*w_4`. Because every `w_i` is a unit,

```text
sum_(i<j<k) w_i w_j w_k
    = P sum_i (1/w_i)
    = P conjugate(sum_i w_i)
    = 0.
```

Hence the monic polynomial with roots `w_1,...,w_4` has neither a cubic
nor a linear term:

```text
prod_i (Y-w_i) = Y^4 + e_2 Y^2 + P.
```

It is even, so its roots are invariant, with multiplicity, under
`Y -> -Y`. This is exactly the asserted antipodal pairing. `QED`

In particular, if three unit complex numbers have a unit sum `c`, then
the three numbers are

```text
{c,w,-w}
```

as a multiset: apply the lemma to the three numbers together with `-c`.

## Step 5: the triple pattern has only three branches

It remains to assume that `A` has pattern `T`. Fix a first coordinate
`a_0` from any singleton section, and write `a_1,a_2,a_3` for the first
coordinates in the triple section. Define the phase-vector homomorphism

```text
F(b) = (
  exp(2*pi*i*(a_1-a_0)*b/210),
  exp(2*pi*i*(a_2-a_0)*b/210),
  exp(2*pi*i*(a_3-a_0)*b/210)
).
```

For every cross-level difference `x` of `Lambda`, the singleton section
in (4) contributes a unit value `c`, while the triple section contributes
three unit values with sum `c`. The lemma shows that, after division by
`c`, the vector `F(x)` lies in the union of three branches

```text
B_1 = {(1,z,-z): |z|=1},
B_2 = {(z,1,-z): |z|=1},
B_3 = {(z,-z,1): |z|=1}.                                 (6)
```

Choose `lambda_0` on a singleton level of `Lambda`. Every other point is
cross-level from it, so every relative vector

```text
F(lambda-lambda_0)
```

lies in at least one branch in (6). Assign each point to one branch that
contains its vector.

Two points assigned to the same branch cannot lie on different levels.
Indeed, if `y,y' in B_r`, then their coordinatewise quotient `q=y/y'`
has

```text
q_r=1,     q_s=q_t
```

for the other two indices. Such a unit vector lies in none of the three
branches:

- membership in `B_r` would require `q_s=-q_t`, contradicting
  `q_s=q_t!=0`;
- membership in `B_s` would force `q_s=1`, hence `q_t=1`, and then require
  `q_r=-q_t`, i.e. `1=-1`;
- membership in `B_t` is symmetric.

But a quotient coming from points on different levels must again satisfy
(6). Therefore each branch can contain points from at most one level.
The other twelve `Lambda` points would occupy at most three levels,
whereas they occupy all ten levels other than the singleton base level.
This contradiction excludes pattern `T`.

Patterns `D` and `T` exhaust (2), so no spectral pair of cardinality 13
exists.

## Independent checking

The accompanying JSON file records the assumptions, branch split, and
contradictions. It is a dependency audit, not a formal proof object. Check
its syntax and the source hashes with:

```bash
python3 -m json.tool theorem_certificate.json >/dev/null
shasum -a 256 -c SHA256SUMS
```

Only the Python standard library and the system SHA-256 implementation are
used. No mathematical claim depends on their output.

## Prior art and novelty calibration

Primary inputs checked:

- Gabor Somlai, *Fuglede's Conjecture on Cyclic Groups of Square-Free
  Order: The Case of Rapidly Growing Prime Factors* (2026),
  <https://arxiv.org/abs/2607.26534>.
- Gergely Kiss, Romanos Diogenes Malikiosis, Gabor Somlai, and Mate Vizer,
  *Fuglede's conjecture holds for cyclic groups of order pqrs* (2022),
  <https://arxiv.org/abs/2011.09578>.
- Izabella Laba and Caleb Marshall, *Vanishing sums of roots of unity and
  the Favard length of self-similar product sets* (2022),
  <https://arxiv.org/abs/2202.07555>.
- Ruxi Shi, *Fuglede's conjecture holds on cyclic groups Z_pqr* (2018),
  <https://arxiv.org/abs/1805.11261>.
- Tao Zhang, *A group ring approach to Fuglede's conjecture in cyclic
  groups* (2022), <https://arxiv.org/abs/2210.15174>.

Somlai records the levelwise cuboid and projection machinery;
Kiss--Malikiosis--Somlai--Vizer supply the base theorem in `Z/210Z`.
Targeted searches found neither an exclusion of 13-point spectral subsets
of `Z/2310Z` nor the four-cell/three-branch surplus-section argument. This
supports only a search-relative application claim. No historical priority
claim is made.

## Trust boundary

- **Contained proof:** the exact section frontier, coefficient equality,
  primitive-cube-root cells, four-unit-vector lemma, branch quotient
  obstruction, and level-count contradictions.
- **Imported mathematics:** spectral-to-tiling in `Z/210Z`, the spectral
  mask-zero characterization, and the levelwise cuboid lemma.
- **Certificate:** the JSON is an audit map only, not a machine proof.
- **Software:** used only for JSON syntax and file integrity; there is no
  enumeration, solver, floating point, or generated mathematical data.
