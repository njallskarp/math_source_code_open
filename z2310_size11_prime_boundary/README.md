# The size-11 spectral boundary in `Z/2310Z`

## Theorem (prime-boundary lifting)

Let `n` be square-free, let `p` be a prime with `p` not dividing `n`, and
assume that every spectral subset of `Z/nZ` tiles `Z/nZ`. If `(A,Lambda)`
is a spectral pair in `Z/(np)Z` with

```text
|A| = |Lambda| = p,
```

then

```text
Phi_p divides m_A    and    Phi_p divides m_Lambda.
```

Consequently, in CRT coordinates `Z/(np)Z ~= Z/nZ x Z/pZ`, each of `A`
and `Lambda` contains exactly one point on every `p`-level. Both are graphs
over `Z/pZ` and tile with the standard complement `Z/nZ x {0}`.

For `n=210` and `p=11`, the known four-prime (`pqrs`) theorem supplies the
hypothesis in `Z/210Z`. Therefore every 11-point spectral subset of
`Z/2310Z` tiles. Together with the previously proved below-11 frontier,
this settles all spectral cardinalities at most 11 in `Z/2310Z`.

## Definitions and input lemmas

For a finite set `E` in `Z/(np)Z`, write

```text
m_E(X) = sum_(e in E) X^e.
```

Identify the group with `Z/nZ x Z/pZ` and denote its `p`-levels by `E_j`,
`j in Z/pZ`. We use the following established square-free cuboid facts.

1. **Levelwise cube rule.** If `d|n` and `Phi_(dp)|m_E`, then every
   `d`-cuboid evaluation `E_j^d[Delta]` is independent of `j`. Moreover,
   if also `Phi_d|m_E`, then `Phi_d|m_(E_j)` for every `j`.
2. **Prime equidistribution.** `Phi_p|m_E` if and only if all `p`-level
   cardinalities are equal. In particular, when `|E|=p`, this means that
   every level has cardinality one.
3. **Spectral symmetry.** If `(A,Lambda)` is spectral, then so is
   `(Lambda,A)`.

The first two statements are standard consequences of the square-free cube
rule; the precise levelwise form is recorded in Somlai (2026), with
attribution to Laba--Marshall and the `pqrs` paper.

## Lemma 1: equality-case descent

Let `E` be a nonnegative set of cardinality `p`. For every `d|n`,

```text
Phi_p does not divide m_E  and  Phi_(dp) divides m_E
    imply
Phi_d divides m_E.                                      (1)
```

### Proof

Suppose instead that `Phi_d` does not divide `m_E`. The cuboid criterion
gives a `d`-cuboid `Delta` with

```text
E^d[Delta] != 0.
```

The levelwise cube rule writes

```text
E^d[Delta] = p c_Delta,
```

where `c_Delta=E_j^d[Delta]` is the same integer for all `p` levels. Since
the cuboid coefficients lie in `{-1,0,1}` and `E` is nonnegative,

```text
p <= |E^d[Delta]| <= |E| = p.
```

Thus `|c_Delta|=1`. For every `j`,

```text
1 = |E_j^d[Delta]| <= |E_j|.
```

All `p` levels are nonempty. Their cardinalities sum to `p`, so every level
has cardinality one. Prime equidistribution now gives `Phi_p|m_E`, contrary
to the hypothesis. This proves (1).

The point of the lemma is that equality in the Laba--Marshall cardinality
bound is rigid: the only obstruction to descent is already the standard
tiling branch.

## Lemma 2: both masks cannot omit `Phi_p`

Assume for contradiction that

```text
Phi_p does not divide m_A m_Lambda.
```

Multiplication by `p` is injective on `A`: a collision would give two
points of `A` whose difference has order `p`, and spectral symmetry would
force `Phi_p|m_Lambda`. Similarly, it is injective on `Lambda`.

Lemma 1 supplies every descent implication

```text
Phi_(dp)|m_A  =>  Phi_d|m_A,    d|n.
```

Now restrict the characters indexed by `Lambda` to the injective image
`pA`, which lies in the subgroup `p Z/(np)Z ~= Z/nZ`. If a frequency
difference has order prime to `p`, multiplication by `p` preserves that
order. If it has order `dp`, spectrality gives `Phi_(dp)|m_A` and Lemma 1
gives `Phi_d|m_A`. Hence all restricted character inner products vanish.
The injectivity on `Lambda` ensures that the restricted characters remain
distinct. Therefore `pA` is a spectral subset of `Z/nZ` of cardinality
`p`.

By the assumed spectral-to-tiling theorem in `Z/nZ`, `pA` tiles `Z/nZ`.
Its cardinality must divide `n`, contradicting `p` not dividing `n`.
Thus at least one of the two masks contains `Phi_p`.

## Lemma 3: the one-sided branch is impossible

It remains to exclude, after possibly swapping the pair,

```text
Phi_p does not divide m_A,    Phi_p divides m_Lambda.    (2)
```

The second condition and `|Lambda|=p` put exactly one point of `Lambda` on
each `p`-level. The first condition forces the projection of `Lambda` onto
`Z/nZ` to be injective: two points with the same first coordinate would
have a difference of order `p`, forcing `Phi_p|m_A` by spectrality. Let

```text
B = projection_n(Lambda).
```

Then `|B|=p`. For distinct `b,b' in B`, their corresponding points of
`Lambda` differ in both coordinates. If `d>1` is the order of `b-b'` in
`Z/nZ`, their full difference has order `dp`. Spectrality and Lemma 1 give

```text
Phi_(dp)|m_A    and    Phi_d|m_A.
```

The levelwise cube rule therefore gives `Phi_d|m_(A_j)` for every
`p`-level `A_j`. It follows that the `p` characters indexed by `B` are
pairwise orthogonal on every nonempty `A_j`. They are nonzero vectors in
the space `C^(|A_j|)`, so

```text
|A_j| >= p
```

for each nonempty level. Since the total cardinality is `p`, exactly one
level is nonempty and it has cardinality `p`. On this level, `B` is a full
spectrum. We have produced a spectral subset of `Z/nZ` of cardinality `p`.
The base spectral-to-tiling theorem again says it tiles, contradicting
`p` not dividing `n`.

Thus (2) is impossible. Together with Lemma 2, this proves
`Phi_p|m_A`. Applying the same conclusion to the symmetric pair proves
`Phi_p|m_Lambda` as well, completing the theorem.

## Specialization and exact scope

Set

```text
n = 210 = 2*3*5*7,    p = 11.
```

Kiss--Malikiosis--Somlai--Vizer prove spectral-to-tiling in `Z/210Z` as
part of their `pqrs` theorem. Since `11` does not divide `210`, the theorem
applies and proves that every 11-point spectral subset of `Z/2310Z` tiles.

This does **not** settle cardinality 12 or any larger cardinality, nor does
it settle all of finite Fuglede for `Z/2310Z`. It closes exactly the first
cardinality not covered by the strict inequality `|A|<11`.

## Independent checking

The artifact is a direct mathematical proof and uses no generated data,
solver, floating point, randomized search, or exhaustive subset census.
Check the machine-readable proof map and file integrity with:

```bash
python3 -m json.tool theorem_certificate.json >/dev/null
shasum -a 256 -c SHA256SUMS
```

The JSON file records the hypotheses, alternatives, imported lemmas, and
contradictions. It is an audit map, not a formal proof object. The proof
depends on the cited levelwise cube rule and on the published `pqrs` base
theorem; the linear-algebra dimension argument and all remaining deductions
are contained above.

## Prior art and novelty calibration

- Gabor Somlai, *Fuglede's Conjecture on Cyclic Groups of Square-Free
  Order: The Case of Rapidly Growing Prime Factors* (2026),
  <https://arxiv.org/abs/2607.26534>.
- Gergely Kiss, Romanos Diogenes Malikiosis, Gabor Somlai, and Mate Vizer,
  *Fuglede's conjecture holds for cyclic groups of order pqrs* (2022),
  <https://arxiv.org/abs/2011.09578>.
- Izabella Laba and Caleb Marshall, *Vanishing sums of roots of unity and
  the Favard length of self-similar product sets* (2022),
  <https://arxiv.org/abs/2202.07555>.

Somlai's paper contains the levelwise cube rule, the cardinality bound, and
the multiplication/projection mechanism. Its divisible-cardinality argument
uses `p>n` to find a common spectrum for arbitrary level size. At level size
one, the equality argument above removes that inequality and also excludes
the asymmetric spectral-pair branch. Targeted searches found no explicit
statement of this prime-boundary lifting theorem or its `Z/2310Z`, size-11
specialization. This is search-relative evidence only; no historical
priority claim is made.

## Trust boundary

- **Mathematical proof:** the three displayed lemmas and their deductions.
- **Imported mathematics:** the square-free cuboid/levelwise rule and
  spectral-to-tiling in the four-prime group `Z/210Z`.
- **Machine-readable certificate:** a transcription and dependency audit;
  it does not establish the universal theorem independently.
- **Software:** only a JSON parser and SHA-256 implementation are used for
  artifact integrity. No mathematical claim depends on their output.
