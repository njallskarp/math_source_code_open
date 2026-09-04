# A sub-double-prime Gram-descent theorem

## Definitions

Let `p` be an odd prime, let `gcd(n,p)=1`, and identify

    Z/(np)Z = Z/nZ x Z/pZ.

For a set `E` in this product, write `E_j` for its section on level
`j in Z/pZ`, and write `m_E` for its mask polynomial.  Say that `E` has the
**p-descent property** if, for every divisor `d|n`,

    Phi_(dp) | m_E  implies  Phi_d | m_E.                 (1)

A pair `(A,Lambda)` is spectral when the characters indexed by `Lambda` are
an orthogonal basis on `A`.  Spectral-pair symmetry means that
`(Lambda,A)` is spectral as well.

## Theorem 1: sub-double-prime descent

Let `(A,Lambda)` be a spectral pair in `Z/(np)Z`, and put
`k=|A|=|Lambda|`.  If

    p < k <= 2p-2,                                        (2)

then at least one of `A,Lambda` has the p-descent property.  Moreover, the
projections of `A` and `Lambda` to `Z/nZ` are injective and form a spectral
pair there.

Consequently, if every `k`-point spectral subset of `Z/nZ` tiles `Z/nZ`,
then every `k`-point spectral subset of `Z/(np)Z` tiles `Z/(np)Z`.  If no
`k`-point spectral subset exists in `Z/nZ`, none exists in `Z/(np)Z`.

### Proof

Because `p` does not divide `k`, neither `m_A` nor `m_Lambda` is divisible by
`Phi_p`: evaluating a putative divisibility at `1` would give `p|k`.  If two
points of `A` had the same `Z/nZ` coordinate, their difference would have
order `p`; spectral-pair symmetry would then force `Phi_p|m_Lambda`, a
contradiction.  Thus `A` projects injectively.  The same argument with the
two members exchanged proves injectivity of `Lambda`.

Suppose, for contradiction, that both p-descent properties fail.  For
`E=A` and then for `E=Lambda`, choose `d|n` such that

    Phi_(dp) | m_E,        Phi_d does not divide m_E.       (3)

By the cuboid criterion there is a `d`-cuboid `Delta` with
`E^d[Delta] != 0`.  The levelwise cuboid identity says that all integers
`E_j^d[Delta]` are equal, say to `c`, and hence

    E^d[Delta] = p c.                                     (4)

The cuboid coefficients belong to `{-1,0,1}` and `E` is a set, so

    p <= |p c| <= |E| = k < 2p.                           (5)

Therefore `|c|=1`.  In particular every level `E_j` is nonempty.  We have
proved that both `A` and `Lambda` meet all `p` levels.

Since `p<k<2p`, the level sizes of `A` include a singleton and a
non-singleton.  Choose

    A_s={a_0},        A_t={a_1,...,a_r},        r>=2.       (6)

The total surplus over the `p` nonempty levels is `k-p`, so

    r <= k-p+1 <= p-1.                                    (7)

Choose one point `(b_u,u)` of `Lambda` on every level `u in Z/pZ`.  Fix
distinct `u,v`, put `x=b_u-b_v`, and let `d=ord_n(x)`.  Projection
injectivity gives `d>1`.  Orthogonality on `A`, grouped by its levels, is

    sum_j zeta_p^((u-v)j) S_j(x) = 0,
    S_j(x)=sum_(a in A_j) zeta_n^(x a).                    (8)

Every coefficient lies in `K=Q(zeta_d)`.  Since `gcd(d,p)=1`,

    [K(zeta_p):K] = phi(dp)/phi(d) = p-1.                  (9)

After reindexing the levels by the nonzero residue `u-v`, the left side of
(8) is a polynomial of degree at most `p-1` over `K` vanishing at `zeta_p`.
Its coefficients are therefore all equal, because the minimal polynomial is
`Phi_p=1+X+...+X^(p-1)`.  In particular `S_t(x)=S_s(x)`, so

    sum_(i=1)^r zeta_n^(x(a_i-a_0)) = 1.                  (10)

For every `u in Z/pZ`, define

    v_u=(zeta_n^(b_u(a_i-a_0)))_(i=1)^r in C^r.           (11)

Equation (10) gives `<v_u,v_v>=1` when `u!=v`, while
`<v_u,v_u>=r`.  The Gram matrix of these `p` vectors is

    G=(r-1)I_p+J_p.                                       (12)

Its eigenvalues are `r-1` with multiplicity `p-1` and `r+p-1` once.  Since
`r>=2`, it has rank `p`.  But a Gram matrix of vectors in `C^r` has rank at
most `r<=p-1`, the desired contradiction.

Thus one member, say `E`, has the p-descent property.  Somlai's projection
lemma applied to `E` shows that its image under multiplication by `p`,
equivalently its projection to `Z/nZ`, is spectral with the restricted
characters indexed by the projection of the other member.  Hence the two
projections form a spectral pair.

If the projected `A` tiles `Z/nZ` with complement `T`, write the injective
lift as

    A={(a,f(a)):a in pi(A)}.

Then `A` tiles the product with complement `T x Z/pZ`: the first coordinate
chooses a unique `a+t`, and the second coordinate then chooses a unique
vertical translate.  This proves all conclusions.  QED

## Theorem 2: the first boundary

If instead `k=2p-1`, then either one mask has the p-descent property, or both
`A` and `Lambda` have level-size multiset

    (p,1,1,...,1).                                        (13)

Indeed, (3)--(5) still force all levels to be nonempty.  If the profile of
`A` is not (13), it has a non-singleton section of size at most `p-1`, and
the same Gram contradiction applies.  Thus simultaneous descent failure
forces (13) for `A`; spectral-pair symmetry forces it for `Lambda`.

This is an obstruction, not a claim that the exceptional profile is
realizable.

## Corollary for Z/2310Z

Take `n=210` and `p=11`.  Fuglede's conjecture holds in `Z/210Z` by the
published `pqrs` theorem.  Theorem 1 gives spectral-to-tiling for every
cardinality `12<=k<=20` in `Z/2310Z`.  A translational tile has cardinality
dividing `2310`, and among these nine integers only `14` and `15` divide
`2310`.  Subgroups realize both.  Therefore the exact spectral-cardinality
classification in this interval is

    possible (and tiling): 14,15;
    impossible:             12,13,16,17,18,19,20.          (14)

At cardinality `21=2p-1`, any spectral non-tile must lie in the exceptional
profile (13) on both sides of a spectral pair.

The individual cardinalities 12, 13, and 14 were already proved in the graph;
the new applications of Theorem 1 are size 15 and sizes 16 through 20.

