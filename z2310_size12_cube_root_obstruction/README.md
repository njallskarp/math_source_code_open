# The size-12 cube-root obstruction in `Z/2310Z`

## Theorem

There is no spectral pair `(A,Lambda)` in `Z/2310Z` with

```text
|A| = |Lambda| = 12.
```

Consequently, `Z/2310Z` has no spectral subset of cardinality 12. Together
with the previously published strict-below-11 descent and size-11
prime-boundary theorem, every spectral cardinality at most 12 is now settled:
the possible sizes below 12 tile, and sizes `4, 8, 9, 12` do not occur.

The proof is structural. It uses no subset enumeration, numerical Fourier
evaluation, solver, or unproved classification.

## Setup

Write

```text
N = 2310 = 210*11
Z/NZ ~= Z/210Z x Z/11Z.
```

For a subset `E`, write `E_j` for its section on the second-coordinate
level `j in Z/11Z`, and write `m_E` for its mask polynomial. We use three
published inputs.

1. Spectral-to-tiling holds in `Z/210Z` by the four-prime theorem of
   Kiss--Malikiosis--Somlai--Vizer.
2. If `Phi_(11d)|m_E`, the levelwise cuboid lemma makes every `d`-cuboid
   evaluation on the eleven sections equal. In particular,

   ```text
   E^d[Delta] = 11 E_j^d[Delta].
   ```

3. The mask-zero characterization of a spectral pair: every nonzero
   difference of one member gives a cyclotomic zero of the other member.

All masks below are masks of ordinary sets, so their coefficients are
nonnegative and every cuboid coefficient belongs to `{-1,0,1}`.

## Step 1: both projections are injective

Neither mask contains `Phi_11`. Indeed, `Phi_11(1)=11`, so
`Phi_11|m_E` would imply that `11` divides `|E|`, whereas `|E|=12`.

Projection of each set to `Z/210Z` is injective. If two elements of `A`
had the same first coordinate, their difference would have order 11;
spectral-pair symmetry would force `Phi_11|m_Lambda`, a contradiction.
The same argument with the pair interchanged proves injectivity for
`Lambda`.

## Step 2: both masks have section pattern `(2,1,...,1)`

Consider the restrictions to `A` of the characters indexed by `Lambda`
after projection to `Z/210Z`. The projected frequency labels remain
distinct. If they were pairwise orthogonal, the projected image of `A`
would be a spectral 12-subset of `Z/210Z`. It would tile by the four-prime
theorem, which is impossible because `12` does not divide `210`.

Therefore some pair of frequencies is orthogonal before projection but
not after projection. Their projected difference has an order `d|210`,
and their second coordinates are different. Equivalently,

```text
Phi_(11d) divides m_A,     Phi_d does not divide m_A.       (1)
```

The levelwise cuboid lemma and the failure in (1) give a `d`-cuboid
`Delta` such that

```text
0 != A^d[Delta] = 11 c,     c = A_j^d[Delta] in Z
```

for every `j`. Nonnegativity gives

```text
11 <= |A^d[Delta]| <= |A| = 12.
```

The only nonzero multiple of 11 in this interval is 11. Thus `|c|=1`,
so every section is nonempty. Twelve points in eleven nonempty sections
have the unique cardinality multiset

```text
(2,1,1,1,1,1,1,1,1,1,1).                              (2)
```

Applying the identical projection argument to the symmetric spectral pair
shows that `Lambda` also has pattern (2).

## Step 3: every cross-level difference sees a primitive cube root

Let the unique double section of `A` contain first coordinates `a_1,a_2`
and put

```text
u = a_2-a_1 in Z/210Z.
```

Injectivity of the projection gives `u != 0`.

Take any two elements of `Lambda` on different 11-levels. Write their
first-coordinate difference as `x` and their nonzero second-coordinate
difference as `t`. With `omega` a primitive eleventh root, spectral
orthogonality says

```text
sum_(j=0)^10 omega^(t j) S_j(x) = 0,
S_j(x) = sum_(a in A_j) exp(2*pi*i*x*a/210).              (3)
```

If `d` is the order of `x` in `Z/210Z`, every coefficient `S_j(x)` lies
in `K=Q(zeta_d)`. Since `11` does not divide `d`, the cyclotomic fields
`Q(zeta_d)` and `Q(zeta_11)` are linearly disjoint. Hence the minimal
polynomial of `omega^t` over `K` is still

```text
Phi_11(Y) = 1+Y+...+Y^10.
```

The left side of (3), viewed as a polynomial in `omega^t`, has degree at
most 10. It is therefore a scalar multiple of `Phi_11`, and all eleven
coefficients are equal:

```text
S_0(x)=S_1(x)=...=S_10(x).                               (4)
```

Ten sections of `A` are singletons, so the common value in (4) has
modulus one. On the double section, (4) says that the sum of two unit
complex numbers also has modulus one. Consequently their ratio has real
part `-1/2`, and hence is a primitive cube root of unity. If
`mu=exp(2*pi*i/3)`, then every cross-level pair of `Lambda` satisfies

```text
exp(2*pi*i*x*u/210) in {mu,mu^2}.                         (5)
```

## Step 4: the two-phase capacity contradiction

Define a phase on the first-coordinate projection of `Lambda` by

```text
f(b) = exp(2*pi*i*u*b/210).
```

Choose an element `lambda_0` from any singleton 11-level of `Lambda`.
Every one of the other eleven elements lies on a different 11-level from
`lambda_0`. Equation (5) confines all eleven phases to the two values

```text
mu f(lambda_0),     mu^2 f(lambda_0).                    (6)
```

Two elements on different 11-levels cannot share a phase: their phase
ratio would be 1, contradicting (5). By (2), among the ten levels other
than the level of `lambda_0`, exactly one level has two points and every
other level has one. Therefore one of the two values in (6) can occur at
most twice (only inside the double level), and the other can occur at
most once. The two values can accommodate at most three points, not the
eleven points required. This contradiction proves the theorem.

## Dependency and edge-case audit

- `Phi_11` cannot divide a 12-point mask because evaluation at one gives
  the integer divisibility `11|12`.
- A failed projected inner product must come from distinct 11-levels. A
  same-level difference has the same order before and after projection,
  so original spectral orthogonality would persist.
- The field argument is exact: for `d|210`, `gcd(d,11)=1`, so
  `[Q(zeta_d,zeta_11):Q(zeta_d)]=10`.
- The singleton base level exists because the forced section pattern has
  ten singleton levels.
- The final capacity bound allows the most favorable possible repetition
  inside the unique double level; it still gives only three slots.

The accompanying JSON file is a machine-readable dependency and branch
map. It is not a formal proof object.

## Reproduction and integrity

From this directory run:

```bash
python3 -m json.tool theorem_certificate.json >/dev/null
shasum -a 256 -c SHA256SUMS
```

No package beyond the Python standard library is needed. The proof does
not depend on the software output; these commands only check syntax and
file integrity.

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
- Tao Zhang, *A group ring approach to Fuglede's conjecture in cyclic
  groups* (2022), <https://arxiv.org/abs/2210.15174>.

Somlai records the levelwise cube rule, the one-prime cardinality bound,
and the projection mechanism. Kiss--Malikiosis--Somlai--Vizer supply the
base theorem in `Z/210Z`. Targeted searches of these sources and arXiv did
not find the size-12 two-phase capacity argument or a statement excluding
12-point spectral subsets of `Z/2310Z`. The theorem is therefore described
only as a search-relative application; no historical priority claim is
made.

## Trust boundary

- **Contained proof:** projection failure, forced section patterns,
  cyclotomic-field coefficient equality, cube-root geometry, and the
  capacity contradiction.
- **Imported mathematics:** spectral-to-tiling in `Z/210Z`, the
  cyclotomic mask-zero characterization, and the levelwise cuboid lemma.
- **Exact algebra:** the field-disjointness and unit-circle calculations
  are written explicitly and use no numerical approximation.
- **Certificate:** the JSON is an audit map only, not a machine proof.
- **Software:** Python JSON parsing and SHA-256 verify packaging only; no
  mathematical conclusion depends on them.
