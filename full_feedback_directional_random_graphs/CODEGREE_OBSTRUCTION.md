# A degree--codegree obstruction to difficult full-feedback localization

## 1. Setting

Let `G=(V,E)` be a finite simple graph of order `n>=2`.  Write

    d(x) = |N(x)|,
    c(x,y) = |N(x) intersect N(y)|,
    delta = min_x d(x),
    C = max_{x!=y} c(x,y).

For a proposed full-feedback probe `v` and a vertex `x notin N[v]`, its
two-hop trace is

    T_v(x) = N(v) intersect N(x).

The response to a probe at `v` is `{v}` for a robber at `v`, `{x}` for a
robber at a neighbour `x`, and `T_v(x)` for a robber at distance two.  Thus
`v` resolves in one round whenever all of its nonneighbour traces have size
at least two and are pairwise distinct.

## 2. Local and global criteria

**Theorem 1 (local symmetric-difference criterion).**  Fix `v in V` and
suppose that

1. `c(v,x)>=2` for every `x notin N[v]`; and
2. for every distinct `x,y notin N[v]`,

       d(x)+d(y)-2c(x,y) >= n-d(v).

Then `v` is a winning one-round full-feedback probe.

**Proof.**  The first hypothesis says that every nonneighbour of `v` is at
distance two and has a trace of size at least two.  Suppose two distinct
nonneighbours `x,y` had equal traces.  Then `N(v)` would miss
`N(x) symmetric-difference N(y)`.  The vertex `v` also does not belong to
that symmetric difference, because it is adjacent to neither `x` nor `y`.
Consequently

    |N(x) symmetric-difference N(y)| <= n-d(v)-1.

On the other hand its cardinality is

    d(x)+d(y)-2c(x,y) >= n-d(v),

a contradiction.  The traces are therefore pairwise distinct, and the
one-round certificate described above applies.  `square`

**Theorem 2 (degree--codegree criterion).**  Suppose every nonedge `xy` of
`G` has at least two common neighbours and

    3 delta - 2 C >= n.                                  (1)

Then every vertex is a winning one-round full-feedback probe.  In
particular, `G` is connected and its full-feedback directional localization
number is

    zeta_d^*(G)=1.

**Proof.**  Fix any `v`.  The nonedge hypothesis supplies the first condition
of Theorem 1.  For distinct `x,y notin N[v]`,

    d(x)+d(y)-2c(x,y)
       >= 2 delta-2C
       >= n-delta
       >= n-d(v),

where the middle inequality is (1).  Theorem 1 applies to every `v`.
Connectivity follows as well: every nonneighbour of any vertex has a common
neighbour with it.  `square`

The integer boundary in (1) is attained by a nontrivial example.  The
complement of the Petersen graph is strongly regular with parameters
`(n,d,lambda,mu)=(10,6,3,4)`.  Hence every nonedge has four common neighbours,
`C=4`, and

    3d-2C = 18-8 = 10 = n.

Theorem 2 therefore certifies every vertex of this graph.

More generally, a strongly regular graph with parameters
`(n,d,lambda,mu)`, `mu>=2`, and

    3d - 2 max(lambda,mu) >= n

has every vertex as a one-round resolver.

## 3. A pseudorandom corollary

**Corollary 3.**  Let `1/2<p<1`, let `eta>=0`, and suppose

    d(v) >= (p-eta)n                         for every v,
    c(x,y) <= (p^2+eta)n                    for every x!=y,

while every nonedge has at least two common neighbours.  If

    5 eta <= 3p-2p^2-1 = (2p-1)(1-p),                    (2)

then every vertex is a winning one-round full-feedback probe.

**Proof.**  The two displayed uniform estimates and (2) give

    3 delta-2C
       >= (3p-2p^2-5eta)n
       >= n.

Apply Theorem 2.  `square`

In particular, any graph sequence with edge-density parameter bounded in a
compact subinterval of `(1/2,1)`, minimum degree `(p-o(1))n`, maximum
codegree at most `(p^2+o(1))n`, and nonedge codegrees at least two eventually
has `zeta_d^*=1`.  This is a deterministic quasirandom-style conclusion; no
probability is used in its proof.

The contrapositive is a useful obstruction for the open problem.  If a graph
has `zeta_d^*>1` and all nonedges have at least two common neighbours, then

    3 delta-2C <= n-1.

Thus any putative graph with `zeta_d^*>2` must either contain a nonedge with
at most one common neighbour or have enough degree/codegree irregularity to
violate this inequality.

## 4. Why diameter two alone is insufficient

The minimum-codegree and separation hypotheses cannot be replaced merely by
diameter two.  For every `m>=3`, let

    H_m = C_5[independent set of size m],

the graph obtained by replacing every vertex of a 5-cycle by an independent
fiber of `m` twins and every cycle edge by a complete bipartite graph.  Then
`H_m` has diameter two, but no pair of simultaneous first-round probes
distinguishes all vertices.

Indeed, record only the base-cycle fibers containing the two probes.  If the
fibers coincide, a fiber at cycle-distance two from them is unprobed and all
of its clones have the same response pair.  If the fibers are adjacent, the
unique fiber at distance two from both supplies the same collision.  If the
fibers are at distance two, at least `m-1>=2` unprobed clones in one probe
fiber have identical response pairs.  These cases include coincident probe
vertices.

This obstruction is specifically to *simultaneous one-round* resolution, not
to the two-cop game.  Probing adjacent fibers `F_0,F_1` leaves only `F_3`
ambiguous.  After the robber's move, its territory is contained in
`F_2 union F_3 union F_4`; probing one vertex in each of `F_2,F_3` then
identifies every vertex in that territory because each is a probe or is
adjacent to a probe.  Hence two probes win in at most two rounds.

## 5. Relation to locating codes and novelty boundary

Open-neighbourhood locating-dominating (OLD) sets are the closest classical
notion found in the primary literature search.  An OLD set `D` requires the
sets `N(x) intersect D` to be nonempty and different for *all* vertices `x`.
Here `D=N(v)`, only vertices outside `N[v]` need distinct traces, and those
traces must have size at least two so that they do not collide with the
singleton responses of neighbours of `v`.  The hypotheses and conclusion
are therefore related to, but not instances of, the standard OLD-set
definition.

The primary sources checked were:

* John Jones and William B. Kinnersley, *The directional localization game
  on graphs*, arXiv:2609.01745v1 (2026), especially Question 6.4;
* Mustapha Chellali, Nader Jafari Rad, Suk Jai Seo, and Peter J. Slater,
  *On open neighborhood locating-dominating in graphs*, Electronic Journal
  of Graph Theory and Applications 2 (2014), DOI
  `10.5614/ejgta.2014.2.2.1`.

No degree--maximum-codegree criterion for the new full-feedback directional
parameter was found.  The result is therefore a candidate-new,
search-relative structural obstruction, not a claim of exhaustive priority.

## 6. Trust boundary

The three universal statements above have symbolic proofs.  The companion
standard-library verifier exhausts small labelled graphs for both criteria,
checks the Petersen-complement boundary example, and audits the blow-up
family.  Exact computation tests the definitions and displayed constants;
it is not used to prove any universal claim.
