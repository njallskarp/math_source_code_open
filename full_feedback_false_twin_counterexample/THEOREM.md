# A single false twin can increase full-feedback localization

## Statement

There is a connected cubic graph \(G\) on 12 vertices with
\(\zeta_d^*(G)=1\) such that replacing just one vertex by two
nonadjacent false twins produces a graph with \(\zeta_d^*=2\).
More precisely, let \(V(G)=\{0,\ldots,11\}\) and

\[
\begin{split}
E(G)=\{&04,05,06,13,17,18,25,26,2\mathbin{-}10,36,
3\mathbin{-}11,45,4\mathbin{-}11,\\
&79,7\mathbin{-}10,89,8\mathbin{-}11,9\mathbin{-}10\}.
\end{split}
\]

Here an entry such as \(04\) denotes the edge \(\{0,4\}\);
hyphens disambiguate endpoints with two digits. The ordered endpoint
pairs are also explicitly listed in `certificate.json`.

Let \(H_m\) replace vertex 5 by an independent module of size
\(m\ge1\), each member adjacent exactly to vertices 0, 2, and 4.
All other vertices remain singletons. Then

\[
\zeta_d^*(H_m)=
\begin{cases}
1,&m=1,\\
2,&m\ge2.
\end{cases}
\]

The graph \(H_m\) has \(11+m\) vertices. For every \(m\ge2\),
probes at vertices 2 and 7 resolve every location in one round.
For \(G=H_1\), an explicit adaptive one-probe strategy uses at most
10 rounds. No vertex resolves \(G\) in one round: a degree-three probe
has at most \(2^3=8\) distinct responses, fewer than its 12 targets.
This disproves preservation of adaptive one-probe localization
under arbitrary nonempty independent substitutions. It also makes the
factor-two substitution bound sharp using only one independent module
of size two. It does not produce a graph with parameter greater than two.
No smallest-counterexample claim is made.

## Game and finite proof rules

For a connected simple graph \(X\), a probe at \(p\) returns
\(D_X(p,p)=\{p\}\) when the robber is at \(p\). Otherwise it returns

\[
D_X(p,x)=\{u\in N_X(p):d_X(u,x)=d_X(p,x)-1\}.
\]

A territory \(B\) is the set of possible locations immediately before
a probe. A response class \(C\) gives posterior \(B\cap C\).
If that posterior is a singleton, the cop wins immediately. Otherwise
the next territory is \(N_X[B\cap C]\), because the robber may stay
or traverse one edge. Every calculation here uses this move rule.

A finite winning certificate assigns a probe and positive integer rank
to each listed territory. Every nonsingleton response posterior must
have a next territory listed with smaller rank. A finite evasion
certificate is a nonempty family \(\mathcal F\) such that, for every
\(F\in\mathcal F\) and every probe \(p\), some exact response class
\(C\) satisfies

\[
|F\cap C|\ge2,
\qquad N_X[F\cap C]\supseteq F'
\quad\text{for some }F'\in\mathcal F.
\]

The initial territory contains every family member. Inductively, a
territory containing \(F\) admits that unresolved response and its
next territory contains \(F'\). This certifies indefinite evasion
against any adaptive probe choices. It does not allow teleportation:
each update is an actual closed neighborhood, and every finite response
history has a compatible legal robber walk. The finite-branching
compactness argument gives a compatible infinite walk.

## The finite certificates for \(G\) and \(H_2\)

For a vertex set \(B\), write its integer mask as
\(\sum_{v\in B}2^v\). The one-probe winning certificate for \(G\)
is the following table. Its initial territory is mask 4095.

| Territory mask | Rank | Probe |
|---:|---:|---:|
| 4095 | 10 | 3 |
| 1149 | 9 | 4 |
| 1930 | 8 | 8 |
| 2361 | 4 | 11 |
| 3970 | 6 | 7 |
| 125 | 1 | 5 |
| 1781 | 8 | 11 |
| 1924 | 7 | 3 |
| 2165 | 3 | 4 |
| 2842 | 5 | 1 |
| 1141 | 2 | 1 |

The verifier checks every response, including all 16 unresolved
branches, directly from graph distances. Thus \(\zeta_d^*(G)=1\).

In \(H_2\), keep label 5 for the original vertex and label its new
twin 12. The following 18 masks form an evasion family:

```text
1670 1924 2127 6257 2394 2842 2506 1930 3970
463 4221 5229 1741 6457 5860 447 4511 6963
```

All 234 obligations (18 territories times 13 probes) satisfy the
displayed evasion rule. The checker searches actual response classes
for each obligation and checks actual neighborhood containment; it
does not accept a solver verdict in place of these checks. Hence
\(\zeta_d^*(H_2)\ge2\).

Here are the response signatures of probes 2 and 7 on \(H_2\):

| Target | Response at 2 | Response at 7 |
|---:|---|---|
| 0 | \(\{5,6,12\}\) | \(\{1,10\}\) |
| 1 | \(\{6,10\}\) | \(\{1\}\) |
| 2 | \(\{2\}\) | \(\{10\}\) |
| 3 | \(\{6\}\) | \(\{1\}\) |
| 4 | \(\{5,12\}\) | \(\{1,9,10\}\) |
| 5 | \(\{5\}\) | \(\{10\}\) |
| 6 | \(\{6\}\) | \(\{1,10\}\) |
| 7 | \(\{10\}\) | \(\{7\}\) |
| 8 | \(\{10\}\) | \(\{1,9\}\) |
| 9 | \(\{10\}\) | \(\{9\}\) |
| 10 | \(\{10\}\) | \(\{10\}\) |
| 11 | \(\{5,6,12\}\) | \(\{1,9\}\) |
| 12 | \(\{12\}\) | \(\{10\}\) |

These signatures are pairwise distinct, proving the matching upper bound.

## Replication lemma

**Lemma.** Let \(X\) be a finite connected simple graph containing an
independent false-twin class \(T\) with \(|T|\ge2\): its members
have the same open neighborhood. Let \(Y\) add any number of further
false twins to this class, changing no other adjacency. Then

\[
\zeta_d^*(X)\le\zeta_d^*(Y).
\]

**Proof.** Adding the twins preserves all distances between old
vertices. A path using a new twin can be replaced by an old-vertex walk
of no greater length, and \(X\) is an induced subgraph of \(Y\).

First consider a probe at an old vertex \(p\notin T\), with the
robber restricted to old vertices. Its old response \(R\) changes to
\(R\cup(T_Y\setminus T)\) if \(T\subseteq R\), and otherwise
does not change. Indeed, a response containing a member of \(T\)
is either the singleton identifying that adjacent target, or contains
all of \(T\) as shortest-path first steps. These cases are distinct
because \(|T|\ge2\). Thus equal old responses remain equal (in fact,
this transformation is injective).

For an old probe \(p\in T\), responses to old targets do not change:
the probe's neighborhood contains no twins. For a new probe, use any
fixed old twin \(t\in T\) as its virtual probe in \(X\). The responses
coincide on all old targets except \(t\) itself. At \(t\), the old
self response \(\{t\}\) becomes the common neighborhood of the twin
class. Since the self response was a singleton class of targets, this
only merges response classes; it never splits one.

Consequently each actual probe, restricted to old robber positions,
has a response partition coarser than or equal to its virtual old probe.
The same holds jointly for any set of \(k\) probes. Repeated virtual
probes can be discarded, leaving at most \(k\) probes. A robber evading
\(k\) probes in \(X\) can follow the same old-vertex moves in \(Y\):
each virtual response class remains inside one actual response class,
so a compatible set of at least two old locations remains unresolved.
The old edges supply all the required moves. Therefore a winning
\(k\)-probe strategy on \(Y\) implies one on \(X\), proving the lemma.
\(\square\)

Apply the lemma to the twin class \(\{5,12\}\) in \(H_2\) to obtain
\(\zeta_d^*(H_m)\ge2\) for all \(m\ge2\). For the upper bound,
in the displayed response table replace every occurrence of
\(\{5,12\}\) as a nonsingleton set by the entire enlarged module.
An individual module target \(x\) has signature
\((\{x\},\{10\})\), because it is adjacent to probe 2. All signatures
remain distinct, proving \(\zeta_d^*(H_m)\le2\).

The hypothesis \(|T|\ge2\) is needed for the response-partition
argument: when a singleton vertex is duplicated, an adjacent singleton
response can split from a more distant response that previously named
that same vertex. The lemma does not assert monotonicity for the first
duplication.

## The specific adaptive obstruction

In \(G\), the targets giving the full-neighborhood response at probe 5
are precisely vertices 1 and 3, which are adjacent. The rank-one
territory 125 in the upper certificate is
\(B=\{0,2,3,4,5,6\}\). Within \(B\), the full response
\(\{0,2,4\}\) uniquely identifies vertex 3.

In its independent substitution, probe 5 in territory
\(B\cup\{12\}\) instead leaves posterior \(\{3,12\}\) on that
response. After the move, probing 12 can give the same full response
with posterior \(\{1,3\}\): the robber can move along edge \(31\),
reintroducing a quotient vertex excluded by the original adaptive history.
Thus scanning the two twins does not simulate the original terminal
probe. This explains a concrete failure of the proposed scan mechanism;
the evasion certificate separately proves that **every** one-probe
strategy fails on \(H_2\).

## Evidence, context, and scope

The finite base case is an exact computer-assisted result, certified
by an 11-state winning strategy, an 18-state evasion family, and a
two-probe response table. The extension to every \(m\ge2\) follows
from the written replication lemma and response table, not extrapolation.

`verify.py` uses breadth-first distances, explicit vertex sets, and the
certificate rules above. `solve.py` independently regenerates the
certificate using Floyd--Warshall distances, integer masks, and a
synchronous fixed point over **all** \(2^{12}\) and \(2^{13}\) subsets.
The latter finds initial rank 10 for \(G\), all 4,096 base beliefs
winning, and 3,552 of the 8,192 enlarged-graph beliefs losing. It agrees
with the supplied certificate exactly. The theorem only needs the
compact certificate checks, not enumeration completeness.

The trust boundary is the displayed finite input, the verifier, exact
Python operations, hardware, and the unformalized mathematical bridge
from certificate rules and response coarsening to the game. There is
no floating point, solver, external graph catalogue, or downloaded
input in reproduction. This work has not been independently reviewed.

Primary context is Jones and Kinnersley,
[*The Directional Localization Game on Graphs*](https://arxiv.org/html/2609.01745v1),
Section 2.1 and Question 6.4. The game definition and the open question
above two belong to that paper. The present result complements the
earlier [general substitution bound](../full_feedback_substitution/)
and [one-round independent-substitution theorem](../full_feedback_independent_modules/).
It does not contradict the latter's stronger hypothesis.

The counterexample, replication lemma, and exact parameter family are
new to the graph and primary sources searched on 2026-09-09; no
historical priority claim is made. General adaptive independent
preservation is now refuted. Uniform substitution, where every quotient
vertex receives the same nontrivial module size, is not decided here.
