# A two-hop certificate makes every vertex a full-feedback resolver in dense random graphs

## 1. Setting

Let `G` be a finite simple graph.  In the full-feedback directional
localization game, a probe at `v` returns `v` when the robber is at `v` and,
otherwise, returns the set of all neighbours of `v` that begin a shortest path
from `v` to the robber.

For `x` outside the closed neighbourhood `N[v]`, put

    C_v(x) = N(v) intersect N(x).

Call `v` **two-hop resolving** when the sets `C_v(x)`, for
`x notin N[v]`, are pairwise distinct and every one has cardinality at least
two.  This is a local, directly checkable certificate; in particular, it
does not quantify over game strategies.

## 2. Deterministic certificate

**Lemma 1.**  If `v` is two-hop resolving, then `G` is connected and a single
full-feedback probe at `v` identifies every possible robber location.  Hence
`zeta_d^*(G)=1`.

**Proof.**  Every vertex outside `N[v]` has a neighbour in `N(v)`, so it is at
distance two from `v`; consequently all vertices lie in the component of `v`.
The response at `v` is:

* `{v}` when the robber is at `v`;
* `{x}` when the robber is at a neighbour `x` of `v`; and
* exactly `C_v(x)` when the robber is at `x notin N[v]`.

The first response contains `v`, the second responses are distinct
singletons in `N(v)`, and the last responses are distinct subsets of `N(v)`
of size at least two.  Thus all responses are different.  `square`

The size-two requirement is sharp for this certificate: if
`C_v(x)={a}`, then the robber at `x` and the robber at the neighbour `a` give
the same response `{a}`.  More generally, among graphs with eccentricity at
most two from `v`, the conditions in the definition are also necessary for a
probe at `v` to resolve immediately.

## 3. Exact random-graph law

Let `G` have the Erdos--Renyi law `G(n,p)`, let `v` be one fixed labelled
vertex, and write `N=n-1`.  Conditional on `d=deg(v)`, there are
`m=N-d` vertices outside `N[v]`.  Their sets `C_v(x)` are independent random
subsets of a fixed `d`-set, including each element independently with
probability `p`.

For a formal power series, `[z^m]` denotes coefficient extraction.

**Theorem 2 (exact certificate probability).**  For `0<p<1`, the probability
`P_n(p)` that the fixed vertex `v` is two-hop resolving is

    P_n(p)
      = sum_{d=0}^N binom(N,d) p^d (1-p)^(N-d) (N-d)!
          * [z^(N-d)] product_{k=2}^d
              (1 + z p^k (1-p)^(d-k))^binom(d,k).

For `p=1/2` this specializes to

    P_n(1/2)
      = sum_{d=0}^N binom(N,d) 2^(-N)
          * (2^d-d-1)_(N-d) / 2^(d(N-d)),

where `(a)_m=a(a-1)...(a-m+1)` and `(a)_0=1`.

**Proof.**  Condition on the particular `d`-set `N(v)`.  A subset `S` of
size `k` occurs as `C_v(x)` with probability
`w_S=p^k(1-p)^(d-k)`.  The two-hop condition says that the `m` labelled
vertices choose distinct subsets from the allowed family `|S|>=2`.  The
probability of this event is `m!` times the degree-`m` elementary symmetric
polynomial in the weights `w_S`.  Its generating function is

    product_{|S|>=2} (1+z w_S),

and grouping equal weights by `|S|` gives the displayed product.  Averaging
over the binomial degree of `v` proves the first formula.  When `p=1/2`, all
`2^d` subset vectors are equiprobable and exactly `2^d-d-1` have size at
least two, so the conditional probability is the displayed falling-factorial
ratio.  `square`

## 4. An explicit collision bound

Put

    rho = 1 - 2 p^2 (1-p).

**Theorem 3 (finite bound).**  For every `n>=2` and `0<p<1`,

    1-P_n(p) <= B_n(p),

where

    B_n(p)
      = (n-1)(1-p) [
            (1-p^2)^(n-2)
          + (n-2)p^2(1-p^2)^(n-3)
        ]
        + binom(n-1,2)(1-p)^2 rho^(n-3).

Terms with zero polynomial coefficient are interpreted as zero, so the
formula also covers `n=2`.

**Proof.**  Fix `x != v`.  The event that `x` lies outside `N[v]` and that
`|C_v(x)|<=1` has probability

    (1-p) [
        (1-p^2)^(n-2)
        + (n-2)p^2(1-p^2)^(n-3)
    ],

because each of the other `n-2` vertices is a common neighbour of `v,x`
independently with probability `p^2`.

Next fix distinct `x,y != v`.  The probability that both lie outside `N[v]`
and `C_v(x)=C_v(y)` is

    (1-p)^2 rho^(n-3).

Indeed, for each `u notin {v,x,y}`, equality at coordinate `u` holds either
when `vu` is absent, or when `vu` is present and `xu,yu` agree.  The resulting
one-coordinate probability is

    (1-p) + p(p^2+(1-p)^2) = 1-2p^2(1-p) = rho.

All relevant edge triples for different `u` are independent.  A union bound
over the `n-1` possible bad vertices and the `binom(n-1,2)` possible collision
pairs gives the claim.  `square`

**Corollary 4 (varying-density regime).**  If `p=p_n` satisfies

    p_n^2 (1-p_n) n / log n -> infinity,

then, with probability tending to one, *every* vertex of `G(n,p_n)` is
two-hop resolving.  Consequently every vertex is a winning one-round probe,
the graph is connected, and `zeta_d^*(G(n,p_n))=1`.

**Proof.**  Apply Theorem 3 and then a union bound over the `n` choices of
`v`.  The elementary estimates

    1-p^2 <= exp(-p^2),
    rho <= exp(-2p^2(1-p))

show that `n B_n(p_n)` tends to zero under the displayed hypothesis; every
polynomial prefactor is swallowed by the assumed superlogarithmic exponent.
`square`

In particular, for each fixed `0<p<1`, all vertices are one-round resolvers
with probability `1-exp(-Omega_p(n))`.

## 5. Meaning for the open problem

Jones and Kinnersley ask whether any finite connected graph has
`zeta_d^*>2`.  The results above do not answer that question, but they rule
out a broad source of candidates much more strongly: throughout the stated
Erdos--Renyi regime the full-feedback number is not merely at most two but is
one, and every possible first probe works.

Thus a counterexample with `zeta_d^*>2`, if one exists, must have a persistent
and highly structured collision system among the two-hop codes `C_v(x)`.
The collision formula in Theorem 3 isolates the relevant obstruction: many
vertices must have repeated common-neighbour traces, or traces of size at
most one, from every plausible probe.

## 6. Literature and novelty boundary

The primary source is Jones and Kinnersley, *The directional localization game
on graphs*, arXiv:2609.01745v1 (2026), especially the full-feedback definition
in Section 2.1 and Question 6.4.  That paper introduces the parameter, proves
results for chordal graphs, Cartesian products, treewidth, and incidence
graphs of projective planes, and asks for any graph with full-feedback number
greater than two.  It does not state a random-graph theorem for the new
full-feedback parameter.  Its bibliography includes work on the older
distance-response localization game; those results concern a different probe
response.

An arXiv exact-phrase search on 2026-09-04 found the Jones--Kinnersley paper as
the only combinatorial result for "directional localization".  The theorem
suite here is therefore candidate-new relative to the searched primary
literature.  No claim of exhaustive historical priority is made.

## 7. Trust boundary

The proof is symbolic and self-contained.  The companion verifier exhausts
small labelled graphs and independently evaluates the coefficient formula
with exact rational arithmetic.  Those computations test definitions and
algebra; they are not used to prove the universal or asymptotic claims.
