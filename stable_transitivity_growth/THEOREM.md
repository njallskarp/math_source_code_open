# Subadditivity, exact small orders, and radial limits for stable transitivity

## 1. Order-vector notation

Fix a labeled `n`-vertex set and one reference direction on every unordered
pair.  Write `E=binom(n,2)`.  A `k`-tournament `T` is represented by its vector

    x(T) in {0,1,...,k}^E,

whose coordinate is the weight in the reference direction; the opposite
weight is `k-x_e(T)`.  Every total order `pi` gives a zero-one vector `v_pi`,
the associated transitive tournament.  Put

    S_d = {v_(pi_1)+...+v_(pi_d) : pi_i total orders},

with `S_0={0}`.  Thus `T` has a transitive tournament decomposition (TTD)
exactly when `x(T)` belongs to `S_k`, and

    m(T) = min {a>=0 : some y in S_a has x(T)+y in S_(k+a)}.   (1)

## 2. Additive inequalities

**Theorem 1 (subadditivity).**  If `T` and `U` are respectively a
`k`-tournament and an `l`-tournament on the same vertex set, then

    m(T+U) <= m(T)+m(U).                                  (2)

Consequently

    m(n,k+l) <= m(n,k)+m(n,l),                            (3)

the limit

    mu_n = lim_(k->infinity) m(n,k)/k

exists and equals `inf_(k>=1) m(n,k)/k`, and

    m(n,k) <= k m(n,1).                                   (4)

**Proof.**  If `y in S_a` stabilizes `T` and `z in S_b` stabilizes `U`,
then `y+z in S_(a+b)` and

    x(T+U)+y+z = (x(T)+y)+(x(U)+z) in S_(k+l+a+b),

which proves (2).

Every `(k+l)`-tournament `W` can be split coordinatewise as `T+U`: for a
coordinate `w`, take `t=min(k,w)` and `u=w-t`.  Then `0<=t<=k`, `0<=u<=l`,
and the opposite-direction weights split automatically.  Maximizing (2)
gives (3), and Fekete's lemma gives the limit.

Finally, every `k`-tournament is a sum of `k` ordinary tournaments.  In a
coordinate of weight `w`, orient that pair in the reference direction in
exactly the first `w` layers.  Applying (2) to these layers proves (4).
`square`

## 3. A universal linear lower bound and exact values through order seven

Let `C` be the directed triangle, and let `kC` put weight `k` on each of its
three cyclic arcs.

**Lemma 2.**  For every `k>=1`,

    m(kC)=k.                                               (5)

**Proof.**  Let `ell` sum weights on the three cyclic arcs.  Every transitive
tournament on three vertices contains either one or two of these arcs.  Hence
every `d`-tournament with a TTD has

    d <= ell <= 2d.                                       (6)

If an `m`-TTD `A` stabilizes `kC`, then

    3k+m <= ell(kC+A) <= 2(k+m),

where the first inequality uses (6) on `A`.  Thus `m>=k`.

For the reverse inequality, in coordinates along the cyclic arcs take the
four tournaments

    C=(1,1,1), A=(1,0,0), B=(1,1,0), D=(1,0,1).

The last three are transitive and `C+A=B+D`.  Summing `k` copies gives a
`k`-summand stabilizer, so `m(kC)<=k`.  `square`

Restriction of every order in a TTD to an induced vertex set is again a total
order.  Extending `kC` arbitrarily to `n` vertices therefore gives

    m(n,k) >= k for every n>=3.                            (7)

The Discovery Net theorem at height 1661, independently accepted at height
1667, proves `m(n,1)=1` for `3<=n<=7`.  Combining it with (4) and (7) yields a
full all-multiplicity classification.

**Corollary 3 (exact small orders for every multiplicity).**

    m(n,k) = 0  for n<=2,
    m(n,k) = k  for 3<=n<=7.                              (8)

The height-1669 theorem `m(8,1)=2`, independently accepted at height 1675,
similarly gives the first uniform interval at order eight:

    k <= m(8,k) <= 2k.                                    (9)

## 4. A general explicit upper bound

For an ordinary tournament `T` and a total order `pi`, let `b_pi(T)` be the
number of arcs pointing backward in `pi`.

**Lemma 4.**  `m(T)<=min_pi b_pi(T)`.

**Proof.**  Let `X` be the transitive tournament of `pi`.  For each backward
pair `e`, choose two total orders `P_e,Q_e` that agree on every pair except
`e`, with their difference in the direction `x(T)-x(X)` at `e`.  This is done
by making the endpoints of `e` adjacent and swapping them.  Coordinatewise,

    x(T) + sum_e v_(Q_e) = v_pi + sum_e v_(P_e).

Both sums other than `T` are TTDs, so the left added tournament stabilizes
`T` with `b_pi(T)` summands.  `square`

Greedily place first a maximum-outdegree vertex of the remaining tournament.
On `s` remaining vertices it contributes at least `ceil((s-1)/2)` forward
arcs.  The resulting order has at least

    sum_(j=1)^(n-1) ceil(j/2) = floor(n^2/4)

forward arcs.  Lemma 4, followed by (4), proves:

**Corollary 5 (explicit improvement of the source bound).**

    m(n,k) <= k floor((n-1)^2/4).                         (10)

The primary source gives the direct bound `k*binom(n,2)/2`.  Formula (10)
improves it by `k*n/4` when `n` is even and by `k*(n-1)/4` when `n` is odd.
For `3<=n<=8`, (8)--(9) are much stronger.

## 5. Exact asymptotic rate as a radial polytope gauge

Let

    P_n = conv{v_pi : pi a total order}

be the linear-ordering polytope, let `c=(1/2,...,1/2)`, and put
`K_n=P_n-c`.  Reversing an order replaces `v_pi` by `1-v_pi`, so `K_n` is
centrally symmetric.  It is full-dimensional: swapping two adjacent entries
of a suitable order produces each coordinate unit vector as a difference of
vertices.  Hence `c` is an interior point of `P_n`.

For a fixed `k`-tournament `T`, define its radial gauge

    gamma(T) = inf{s>=0 : x(T)-k*c belongs to s*K_n}.      (11)

**Theorem 6 (exact dilation rate).**  The limit

    lambda(T) = lim_(q->infinity) m(qT)/q

exists and satisfies

    lambda(T) = max(0,(gamma(T)-k)/2).                    (12)

Equivalently, `lambda(T)` is the minimum `alpha>=0` such that

    x(T) belongs to (k+alpha)P_n - alpha P_n,             (13)

or, equivalently,

    (x(T)+alpha*1)/(k+2alpha) belongs to P_n.             (14)

Thus the stable rate is exactly the amount by which the normalized tournament
must move radially toward the center of the linear-ordering polytope.

**Proof.**  The sequence `m(qT)` is subadditive by Theorem 1, so its normalized
limit exists.  Relax (1) by allowing nonnegative real multiplicities of total
orders.  If `alpha` is the relaxed stabilizer size, this is the rational linear
program

    x(T) + sum_pi b_pi v_pi = sum_pi a_pi v_pi,
    sum_pi b_pi=alpha,  sum_pi a_pi=k+alpha,
    a_pi,b_pi>=0.                                        (15)

Every integral stabilization of `qT` with size `h`, divided by `q`, is feasible
in (15) with `alpha=h/q`; therefore the relaxation optimum `sigma(T)` is at
most `lambda(T)`.

Conversely, (15) has rational data, is feasible, and attains a rational basic
optimal solution.  Clear a common denominator `D`.  The numbers `D a_pi` and
`D b_pi` are nonnegative integers and their vector equality says exactly that
`DT` has a stabilizer of size `D sigma(T)`.  Hence

    lambda(T)=inf_q m(qT)/q <= m(DT)/D <= sigma(T),

so equality holds.

The feasible-vector condition in (15) is (13).  Since `-P_n=P_n-1` and the
Minkowski sum of positive scalar multiples of one convex set satisfies
`aP_n+bP_n=(a+b)P_n`,

    (k+alpha)P_n-alpha P_n=(k+2alpha)P_n-alpha*1.

This gives (14); subtracting `(k/2+alpha)*1` gives

    x(T)-k*c in (k+2alpha)K_n.

Minimizing `alpha>=0` proves (12).  `square`

This formula is effective: (15) is a finite rational LP.  It also isolates
integrality exactly.  A tournament can have positive one-copy stabilization
cost but zero dilation rate precisely when its vector lies in `kP_n`;
equivalently, some finite dilation of it has a TTD.

## 6. Worst-case asymptotic growth

**Theorem 7.**  For each fixed `n`,

    mu_n = max{lambda(T) : T an ordinary n-vertex tournament}.  (16)

**Proof.**  The lower bound follows from
`m(n,q)>=m(qT)` for every ordinary `T`.

For the upper bound, decompose an arbitrary `k`-tournament into `k` ordinary
labeled tournaments and group identical layers:

    W = sum_T q_T T,   sum_T q_T=k.

There are only finitely many labeled ordinary tournaments.  Given `epsilon>0`,
for every type `T` and all sufficiently large `q`,

    m(qT) <= q(lambda(T)+epsilon).

Choose a common threshold over the finite type set.  The groups below that
threshold contribute only a constant depending on `n` and `epsilon`, while
all other groups contribute at most
`q_T(max_T lambda(T)+epsilon)`.  By subadditivity,

    m(W) <= k(max_T lambda(T)+epsilon)+O_(n,epsilon)(1).

Divide by `k`, take the worst case and the limit, then let `epsilon` tend to
zero.  `square`

Consequently

    mu_n=1 for 3<=n<=7,   and   1<=mu_8<=2.               (17)

## 7. Literature, novelty, and trust boundary

Davis and Schroeder, *Relating tournaments and permutations with xrays*,
arXiv:2606.21532v1 (2026), introduce stable transitivity, prove finiteness, and
state `m(n,k)<=k*binom(n,2)/2`.  Their paper does not state Theorems 1, 6, or
7, the all-`k` classification (8), or bound (10).  Exact-phrase searches for
"transitive tournament decomposition" found only that primary paper.

The results through ordinary order seven and the exact ordinary order-eight
value are independently reviewed Discovery Net dependencies, not reproved
here.  Everything else is a symbolic, self-contained argument.  The companion
standard-library checker audits the three-vertex semigroup, subadditivity, the
triangle certificates, and two independent computations of the feedback-arc
bound through order six.  Its finite output corroborates but does not replace
the universal proofs.
