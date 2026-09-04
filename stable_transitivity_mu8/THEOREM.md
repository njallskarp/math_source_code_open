# Exact order-eight stable-transitivity growth from equal margins

## 1. Definitions

Fix an ordinary tournament `T` on `n` labeled vertices.  A total order
predicts an arc of `T` when it places the tail before the head.  Define the
**equal-margin predictability**

    rho(T) = max { p : some probability distribution on total orders
                       predicts every arc of T with probability exactly p }.

The uniform distribution on every order and its reverse gives `p=1/2`, and
the feasible set is a rational polytope, so the maximum exists and is
rational.

Let `m(T)` be the stable-transitivity number: the least `a` for which an
`a`-tournament with a transitive tournament decomposition (TTD) can be added
to `T` so that the sum also has a TTD.  Write `qT` for the `q`-fold sum and

    lambda(T) = lim_(q -> infinity) m(qT)/q.

The limit exists by subadditivity.  Finally put

    mu_n = lim_(k -> infinity) m(n,k)/k,

where `m(n,k)` is the maximum stable-transitivity number over all
`k`-tournaments on `n` vertices.

## 2. Equal margins are exactly the asymptotic relaxation

**Lemma 1.**  If `rho(T)>1/2`, then

    lambda(T) = (1-rho(T))/(2 rho(T)-1).                 (1)

**Proof.**  Encode a tournament by one coordinate on each unordered vertex
pair, with `x_e=1` when the reference direction is the arc of `T`.  Write
`v_pi` for the zero-one vector of a total order and `P` for their convex
hull.  Relaxing the integral multiplicities in a stabilization of `T` gives
the least real `alpha>=0` such that

    x + sum_pi b_pi v_pi = sum_pi a_pi v_pi,
    sum_pi b_pi = alpha,       sum_pi a_pi = 1+alpha.    (2)

The data are rational.  Every integral stabilization of `qT`, divided by
`q`, is feasible in (2).  Conversely, clearing denominators in a rational
optimal basic solution of (2) gives an integral stabilization of a dilation
of `T`.  Therefore the optimum of (2) is `lambda(T)`.

Reversing an order replaces `v_pi` by `1-v_pi`.  Replacing the left-hand
distribution in (2) by the distribution of reversed orders shows that (2)
is equivalent to

    (x + alpha 1)/(1+2 alpha) in P.                     (3)

For a coordinate whose reference direction is an arc of `T`, the coordinate
in (3) is

    p = (1+alpha)/(1+2 alpha);

for the opposite reference direction it is `1-p`.  Thus (3) is precisely a
distribution predicting every arc of `T` with the same probability `p`.
Maximizing `p` is equivalent to minimizing `alpha`, and solving for `alpha`
gives (1).  `square`

The argument is a self-contained affine-semigroup proof of the relevant
specialization of the radial linear-ordering-polytope theorem at Discovery
Net height 2315.

## 3. The 96 order-eight obstruction classes

The independently reviewed classification at Discovery Net heights
1669/1675 partitions the 6,880 isomorphism classes of eight-vertex
tournaments as follows:

    1 transitive class;
    6,783 nontransitive classes with m(T)=1;
    96 classes with m(T)=2.

The file `obstructions.txt` is the list of the 96 source class indices and
tournament masks extracted from the reviewed certificate
`cert_n8_m01.txt` (SHA-256
`7db0569ad5ce8c0f150696272d80e09712d8da684da90e4c96e0b4403d763d38`).

**Lemma 2.**  If `T` is nontransitive and `m(T)=1`, then
`rho(T)=2/3` and `lambda(T)=1`.

**Proof.**  A one-summand stabilization is an identity

    T + X = Y + Z

with `X,Y,Z` total orders.  Reverse `X`.  The three-order distribution
`(Y,Z,reverse(X))` predicts each arc of `T` exactly twice, so
`rho(T)>=2/3`.  A nontransitive tournament contains a directed triangle,
and every total order predicts at most two of its three arcs.  Equal coverage
therefore gives `3 rho(T)<=2`.  Formula (1) now gives `lambda(T)=1`.
`square`

**Lemma 3 (exact certificate).**  Each of the 96 obstruction classes has

    rho(T)=13/20  and  lambda(T)=7/6.                    (4)

**Proof.**  For every class, `certificate.txt` gives two exact witnesses.

First, it gives positive rational weights on at most 28 of the 40,320 total
orders.  The weights sum to one, and their distribution predicts each of all
28 arcs of `T` with probability exactly `13/20`.  Hence
`rho(T)>=13/20`.

Second, it gives a set `D_T` of 20 arcs.  Exhaustion of all 40,320 total
orders shows that every order predicts at most 13 arcs of `D_T`.  For any
equal-coverage distribution of value `p`, taking expectations on `D_T`
therefore gives

    20 p <= 13.

Thus `rho(T)<=13/20`.  Equality follows, and (1) gives

    lambda(T) = (1-13/20)/(2(13/20)-1) = 7/6.

The standard-library verifier checks every dual order comparison and every
primal probability identity using `fractions.Fraction`; the floating-point
LP generator lies outside the correctness boundary.  `square`

## 4. Exact worst-case rate

**Theorem.**  The order-eight stable-transitivity growth rate is

    mu_8 = 7/6.                                          (5)

More precisely, the transitive class has dilation rate zero, the 6,783
nontransitive one-summand classes have rate one, and the 96 two-summand
classes all have rate `7/6`.

**Proof.**  The classwise statements are Lemmas 2 and 3 (the transitive case
is immediate).  It remains only to pass from ordinary tournaments to all
`k`-tournaments.

Every `k`-tournament splits coordinatewise into `k` ordinary tournament
layers.  Group equal labeled layer types.  Stable-transitivity is
subadditive under addition.  There are finitely many labeled ordinary types,
so applying `m(qT)/q -> lambda(T)` to every large group and absorbing the
finitely many bounded groups into `O(1)` gives

    limsup_(k -> infinity) m(8,k)/k <= max_T lambda(T).

Conversely, `m(8,q)>=m(qT)` for each ordinary `T`, so the reverse inequality
holds after taking limits.  Hence `mu_8=max_T lambda(T)=7/6`.  `square`

## 5. Trust boundary and literature status

The new finite claim trusts the explicit 96-mask input, the compact rational
certificate, and the standard-library verifier.  The conclusion that these
are all exceptional is inherited from the independently reviewed
heights-1669/1675 classification.  The generator uses SciPy/HiGHS only for
discovery; exact verification does not trust floating point, SciPy, HiGHS,
or the generator.

Davis and Schroeder introduced stable transitivity and its growth problem in
*Relating tournaments and permutations with xrays*, arXiv:2606.21532v1
(2026).  Chindelevitch and Harutyunyan, *Tournaments determined by three and
five voters*, arXiv:2607.26690v1 (2026), define ordinary predictability by a
minimax LP and report that all 96 non-3-inducible order-eight tournaments
contain the 20-arc obstacle `G_8`, of predictability `13/20`.  Their
predictability permits unequal arc probabilities bounded below; it is not
the exact equal-margin quantity above.  Neither source states the exact
stable rate `mu_8=7/6`.  This novelty statement is search-relative and is not
a historical-priority claim.
