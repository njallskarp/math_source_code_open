# Size-14 descent or Gram-rank lifting in `Z/2310Z`

## Theorem

Every spectral subset of `Z/2310Z` having cardinality `14` tiles
`Z/2310Z`.

More precisely, let `(A,Lambda)` be a spectral pair with

```text
|A| = |Lambda| = 14.
```

Relative to

```text
Z/2310Z ~= Z/210Z x Z/11Z,
```

either the prime descent succeeds for at least one mask, in which case the
projected pair is spectral in `Z/210Z` and the graph lift `A` tiles, or both
descents fail.  The latter alternative is impossible: it would produce
eleven vectors in `C^r`, with `2 <= r <= 4`, whose Gram matrix is

```text
(r-1) I_11 + J_11.
```

That matrix has rank `11`, whereas a Gram matrix of vectors in `C^r` has
rank at most `r`.

This corrects an arithmetic premise in the motivating wake: `14` **does**
divide `210`.  Thus projected spectrality is not forbidden; it is exactly
the branch that proves tiling.

## Setup and imported inputs

For `E subset Z/210Z x Z/11Z`, let `E_j` be its section on level
`j in Z/11Z`, and let `m_E` be its mask polynomial.  We use the following
published facts.

1. Spectral-to-tiling holds in `Z/210Z` by the four-prime theorem of
   Kiss--Malikiosis--Somlai--Vizer.
2. If `Phi_(11d) | m_E`, the levelwise cuboid lemma makes every suitable
   `d`-cuboid evaluation on the eleven sections equal:

   ```text
   E^d[Delta] = 11 E_j^d[Delta].
   ```

3. Differences in either member of a finite cyclic spectral pair force the
   corresponding cyclotomic zero of the opposite mask.

The descent formulation and section-coefficient argument below are the same
prime-coordinate mechanisms audited in the preceding size-11 through
size-13 results.  The Gram-rank closure is elementary and is proved here.

## Step 1: absence of `Phi_11` and injective projections

Neither mask contains `Phi_11`.  Indeed, `Phi_11(1)=11`, so divisibility
would imply

```text
11 divides m_E(1) = 14,
```

which is false.  Projection of both `A` and `Lambda` to `Z/210Z` is
therefore injective: a collision in one projection would be an order-11
difference and would force `Phi_11` into the other mask.

For `E` equal to `A` or `Lambda`, call the following the descent condition:

```text
Phi_(11d) | m_E  implies  Phi_d | m_E    for every d | 210.       (D_E)
```

## Step 2: either successful descent proves that `A` tiles

Suppose first that `(D_A)` holds.  Take two distinct projected spectrum
points.  If their original level difference is zero, their orthogonality
already gives a `Phi_d` zero of `m_A`.  If their level difference is
nonzero, orthogonality gives `Phi_(11d) | m_A`, and `(D_A)` supplies the
`Phi_d` zero.  Hence the projected pair is spectral in `Z/210Z`.

If `(D_Lambda)` holds instead, the same argument with the pair reversed
makes the reversed projected pair spectral.  A square Fourier submatrix has
orthogonal rows if and only if it has orthogonal columns, so in either case
the projected sets form a spectral pair.

The four-prime theorem now makes the projection `bar(A)` tile `Z/210Z`.
If `T` is a tiling complement, injectivity writes `A` as a graph

```text
A = {(a,f(a)) : a in bar(A)}.
```

Then

```text
T x Z/11Z
```

is a tiling complement for `A`: the first coordinate has a unique
decomposition `x=a+t`, and the second coordinate uniquely determines the
remaining `Z/11Z` translate.  Thus either successful descent proves the
theorem.

## Step 3: two failed descents force the surplus-section frontier

Assume for contradiction that both descent conditions fail.  For each
`E in {A,Lambda}` there is a divisor `d | 210` with

```text
Phi_(11d) | m_E,       Phi_d does not divide m_E.           (1)
```

The levelwise cuboid lemma gives a cuboid `Delta` with

```text
0 != E^d[Delta] = 11 c,       c = E_j^d[Delta] in Z.
```

Since the cuboid coefficients lie in `{-1,0,1}`,

```text
11 <= |E^d[Delta]| <= |E| = 14.
```

Consequently `|E^d[Delta]|=11` and `c=+1` or `-1`.  Every one of the
eleven sections is nonempty.  Distributing fourteen points among them
gives exactly one of

```text
Q  = (4,1,1,1,1,1,1,1,1,1,1),
M  = (3,2,1,1,1,1,1,1,1,1,1),
D3 = (2,2,2,1,1,1,1,1,1,1,1).                             (2)
```

This holds for both masks.  In particular, `A` has a singleton section and
a non-singleton section of size `r` with `2 <= r <= 4`, while `Lambda`
meets all eleven levels.

## Step 4: cross-level coefficient equality

For each level `s`, choose one spectrum point

```text
lambda_s = (b_s,s) in Lambda.
```

For `s != t`, put `x=b_s-b_t` and `q=s-t`.  Projection injectivity gives
`x != 0`.  Orthogonality gives

```text
sum_(j=0)^10 omega^(qj) S_j(x) = 0,
S_j(x) = sum_(a in A_j) exp(2*pi*i*x*a/210),                (3)
```

where `omega` is a primitive eleventh root.  If `d` is the order of `x`
in `Z/210Z`, then every coefficient belongs to `K=Q(zeta_d)`.  Since
`gcd(d,11)=1`,

```text
[Q(zeta_(11d)):Q(zeta_d)] = 10.
```

Thus `Phi_11` is the minimal polynomial of `omega` over `K`.  Reindexing
by the permutation `j -> qj` shows that the degree-at-most-ten polynomial
in (3) is a scalar multiple of `Phi_11`.  Therefore

```text
S_0(x) = S_1(x) = ... = S_10(x)                            (4)
```

for every pair of chosen points on distinct spectrum levels.

## Step 5: the Gram-rank contradiction

Let `a_0` be the first coordinate in a singleton section of `A`, and let
`a_1,...,a_r` be the first coordinates in any non-singleton section, where
`2 <= r <= 4`.  Define

```text
v_s = (
  exp(2*pi*i*b_s*(a_1-a_0)/210),
  ...,
  exp(2*pi*i*b_s*(a_r-a_0)/210)
) in C^r.
```

For `s != t`, equation (4), applied to `x=b_s-b_t`, equates the Fourier
sum of the `r`-point section with the singleton phase.  Division by that
phase yields

```text
<v_s,v_t> = 1.
```

Also `<v_s,v_s>=r`.  The Gram matrix of the eleven vectors is therefore

```text
G = (r-1) I_11 + J_11.
```

Its eigenvalues are

```text
r+10       with multiplicity 1,
r-1        with multiplicity 10.
```

For `r>=2` both are nonzero, so

```text
det(G) = (r+10)(r-1)^10 != 0,
rank(G) = 11.
```

But eleven vectors in `C^r` have a Gram matrix of rank at most
`r <= 4`.  This contradiction excludes the branch in which both descents
fail.  At least one descent succeeds, and Step 2 proves that `A` tiles.

## Independent checking

The accompanying JSON file records the hypotheses, branch split, and exact
Gram determinant.  It is a dependency audit, not a formal proof object.
Check its syntax and all source hashes with:

```bash
python3 -m json.tool theorem_certificate.json >/dev/null
shasum -a 256 -c SHA256SUMS
```

Only the Python standard library and the system SHA-256 implementation are
used.  No mathematical claim depends on their output.

## Prior art and novelty calibration

Primary inputs refreshed for this wake:

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

Targeted searches on 2026-09-02 found no exact `Z/2310Z` size-14 result or
this descent-or-Gram-rank closure.  The result is therefore presented only
as a search-relative specialization.  No historical priority claim is
made.

## Trust boundary

- **Mathematical proof:** the descent dichotomy, graph-lift tiling, and
  Gram-rank contradiction are written above.
- **Imported literature:** the four-prime `Z/210Z` theorem and levelwise
  cuboid mechanism are cited inputs.
- **Exact computation:** none.
- **Software:** used only to parse the JSON audit and verify file hashes.
- **Enumeration/solver/floating point:** none.

