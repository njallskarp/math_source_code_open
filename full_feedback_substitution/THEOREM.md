# Full-feedback localization under graph substitution

## Statements and scope

Write \(\zeta_d^*(G)\) for the full-feedback directional localization number.
A probe at \(p\) returns \(\{p\}\) if the robber is at \(p\), and otherwise
returns **all** neighbors of \(p\) that start a shortest path to the robber.
The cops choose all probes in a round before seeing any response. If the
robber is not localized, it may stay or move along one edge. These are the
rules of Jones and Kinnersley [1, Section 2.1].

Let \(G\) be a finite connected simple graph with at least two vertices.
For each \(v\in V(G)\), let \(H_v\) be an arbitrary finite nonempty simple
graph. The substitution \(X=G[H_v:v\in V(G)]\) has disjoint vertex sets
\(M_v=V(H_v)\), the edges of each \(H_v\), and all edges between \(M_u\)
and \(M_v\) precisely when \(uv\in E(G)\). Internal graphs may be
disconnected. Let \(\pi:V(X)\to V(G)\) be the module map.

**Theorem 1 (guarded substitution).**
\[
\zeta_d^*(X)\le 2\zeta_d^*(G).
\]
More precisely, a \(k\)-probe strategy winning on \(G\) in at most \(r\)
rounds lifts to a strategy with at most \(2k\) probes on \(X\), winning in
at most \(r+1\) rounds.

**Theorem 2 (sharpness already at one probe).** If \(Q_6\) is the binary
six-dimensional cube and \(\vee\) denotes graph join, then
\[
\zeta_d^*(Q_6)=\zeta_d^*(K_2)=1,
\qquad
\zeta_d^*(Q_6\vee Q_6)=2.
\]
The join has 128 vertices and is \(K_2[Q_6,Q_6]\). Thus the multiplicative
constant 2 in Theorem 1 cannot be replaced by any smaller universal
constant. This does not assert sharpness separately for every \(k>1\).
The class of one-probe graphs is not closed under join or substitution.

**Corollary.** Every substitution over a connected one-probe graph with at
least two vertices has full-feedback directional localization number at
most two. In particular this applies to every connected chordal quotient
of order at least two, by [1, Theorem 2.3]. It also applies to the
one-round-resolving quotients certified in the existing Discovery Net
random-graph and degree/codegree contributions. It places no conditions on
the sizes or internal edges of the substituted graphs.

These results do not decide whether any connected graph has
\(\zeta_d^*>2\), the question in [1, Question 6.4].

## Two local facts

For a graph \(Y\), let \(D_Y(p,x)\) denote the full response from a robber
at \(x\) to a probe at \(p\).

**Lemma 1 (guarded module detection).** Suppose \(uv\in E(G)\),
\(a\in M_u\), and \(b\in M_v\). For every \(x\in M_u\), its joint
response to \((a,b)\) is unique among all vertices of \(X\).

*Proof.* The response at \(b\) is \(\{x\}\). If \(x=a\), the response
at \(a\) itself singles out \(a\). Otherwise, suppose \(y\ne x\)
also had response \(\{x\}\) at \(b\). It cannot lie in \(M_u\), since
then its response at \(b\) would be \(\{y\}\). A shortest path from
\(b\) to \(y\) beginning with \(x\) must leave \(M_u\) immediately:
if it passed through a second vertex of \(M_u\), deleting its initial
visit to \(x\) would shorten it, since \(b\) is adjacent to that second
vertex. Replace \(x\) on this path by \(a\). The resulting path has the
same length: \(a\) has the same neighbors as \(x\) outside \(M_u\).
It is another shortest path, so the response at \(b\) also contains
\(a\ne x\), a contradiction. The path replacement cannot repeat \(a\):
a shortest path cannot return to \(M_u\), since \(b\) is adjacent to
its later vertex there. This proves the assertion. \(\square\)

**Lemma 2 (response projection and finishing).**

1. If \(a\in M_u\) and \(x\in M_w\) with \(w\ne u\), then
   \(\pi(D_X(a,x))=D_G(u,w)\).
2. After the robber has been confined to one module \(M_u\), two probes
   suffice in the next round, even after its move.

*Proof.* Distances between distinct modules equal their quotient distances.
If \(uw\) is an edge, the real response is \(\{x\}\), as required.
Otherwise the response is the union of the modules \(M_t\) for which
\(t\) starts a shortest \(u,w\)-path in \(G\). No internal edge can
start a shortest path to a different module: it would spend one step
without improving the quotient distance. This proves (1).

For (2), choose a neighbor \(v\) of \(u\) and representatives
\(a\in M_u,b\in M_v\). After the move, the territory is contained in
\(M_u\cup\bigcup_{t\in N_G(u)}M_t\). Vertices inside \(M_u\) are
recognized globally by Lemma 1. Each vertex \(x\) outside \(M_u\) in
this territory returns \(\{x\}\) at \(a\), so these outside vertices
are pairwise distinguished. Lemma 1 also rules out all cross-collisions.
Thus the response pair is injective on the territory. \(\square\)

## Proof of Theorem 1

Fix a winning quotient strategy. In each simulated round it requests
\(p_1,\ldots,p_k\). For every \(p_i\), choose a fixed neighbor \(q_i\)
and probe representatives of both \(M_{p_i}\) and \(M_{q_i}\).
This is a simultaneous choice of at most \(2k\) vertices; repetitions
can be omitted.

If the robber is in any \(M_{p_i}\), Lemma 1 identifies its actual
vertex immediately. Otherwise, project the responses of the primary
probes to \(G\), and feed those to the quotient strategy. By Lemma 2(1)
these are exactly the responses for the robber's quotient vertex.
A move inside a module projects to staying put; a move between modules
projects to a quotient edge. Therefore the actual projected history is
one legal history for the simulated game. Extra information from guard
probes can be discarded without invalidating the simulation.

Within \(r\) rounds the quotient strategy either led to an earlier
actual capture or identifies one quotient vertex \(u\). At that moment
the real robber is confined to \(M_u\). Lemma 2(2) wins in one further
round with two of the available probes. This proves the bound. The
assumptions \(|G|\ge2\) and connectedness supply every guard neighbor;
no statement for the one-vertex quotient is implicit. \(\square\)

A useful refinement follows from the same proof: if a quotient strategy
uses probe sets \(P\) with no isolated vertex in \(G[P]\), then each
primary probe already has another primary probe as its guard. Such a
\(k\)-probe strategy lifts with the same \(k\) probes and at most one
extra round. In particular, a strategy using the two ends of an edge in
every round lifts to all substitutions with two probes.

## An elementary cube neighborhood certificate

Let \(N_d[A]\) be the closed neighborhood of a subset of \(Q_d\).
The following recurrence gives a universal lower bound; it is not claimed
to give the exact isoperimetric profile at every argument.

Set \(L_0(0)=0,L_0(1)=1\). For \(d\ge1\), \(0\le m\le2^d\), put
\[
L_d(m)=\min_{\substack{a+b=m\\0\le a,b\le2^{d-1}}}
 \left(\max\{L_{d-1}(a),b\}+\max\{L_{d-1}(b),a\}\right).
\]
Then every \(m\)-set \(A\subseteq Q_d\) satisfies
\( |N_d[A]|\ge L_d(m)\). To prove this, split \(A\) into its two
coordinate slices \(A_0,A_1\), of sizes \(a,b\). The corresponding
neighborhood slices are
\(N_{d-1}[A_0]\cup A_1\) and \(N_{d-1}[A_1]\cup A_0\).
Their sizes are at least the two maxima in the recurrence. Induction on
\(d\), starting with the one-vertex cube, proves the claim.

The exact integer recurrence gives
\[
(L_5(0),\ldots,L_5(13))=
(0,6,10,13,15,16,16,19,21,22,22,24,25,25).
\]
For \(m=13\), the fourteen expressions in the minimum defining
\(L_6(13)\), ordered by \(a=0,\ldots,13\), are
\[
(38,37,35,35,37,37,35,35,37,37,35,35,37,38).
\]
Hence every 13-set in \(Q_6\) has at least 35 vertices in its closed
neighborhood. The same lower bound holds for any larger set by taking a
13-subset. It is attained: take the empty set, the six singletons, and
\(\{1,2\},\{1,3\},\{1,4\},\{1,5\},\{1,6\},\{2,3\}\).
Its neighborhood contains all 22 sets of size at most two, plus the ten
triples containing 1 and the three additional triples containing 2 and 3.

The recurrence, its induction, and its displayed small integer evaluations
suffice here. Harper's classical vertex-isoperimetric theorem independently
implies the same local bound, but is not a premise of this proof. No novelty
is claimed for this cube-neighborhood value or the elementary slicing
bound. See [2, Theorem 1] for the classical context.

## Proof of Theorem 2

A probe at a vertex of \(Q_6\) returns exactly the neighbors obtained by
flipping coordinates in which the robber differs from the probe. This
recovers all six bits; the special self response identifies the probe
itself. Thus \(\zeta_d^*(Q_6)=1\); clearly \(\zeta_d^*(K_2)=1\).

Write the two cube modules of their join as \(A\) and \(B\). Two
probes, one in each module, identify every vertex in one round by Lemma 1
applied in both directions.

For the lower bound, the robber maintains this invariant at the start of
each round: **at least 35 vertices of each cube are contaminated**. This
holds initially. If the cop probes \(p\in A\), respond with the entire
other module \(B\). A vertex \(x\in A\) produces exactly this response
if and only if its internal cube distance from \(p\) is at least three.
Indeed, the join distance is then two and there is no internal common
neighbor; distance two in the cube would contribute an internal common
neighbor, while distances zero and one give singleton responses. A vertex
in \(B\) gives its own singleton response, not \(B\).

The cube ball of radius two about \(p\) has
\(1+6+\binom62=22\) vertices. Consequently at least \(35-22=13\)
currently contaminated vertices give the chosen response. The cop has not
localized the robber. After the move, every vertex of \(B\) is again
contaminated, and the closed neighborhood within \(A\) of those at least
13 vertices has size at least 35 by the preceding certificate. This
restores the invariant. The same argument applies to a probe in \(B\).

This is an invariant for the exact belief-state game, not a claim that
the robber teleports among candidate positions. Each updated territory is
precisely a response-class intersection followed by a closed-neighborhood
move. Every finite response history has a compatible robber walk; finite
branching yields a compatible infinite walk if an infinite play is needed.
Thus one cop cannot force localization in bounded time, proving
\(\zeta_d^*(Q_6\vee Q_6)=2\). \(\square\)

## Evidence, novelty, and dependencies

The substitution theorem and robber invariant are mathematical proofs.
`verify.py` audits the local lemmas on a deterministic finite domain, checks
the small cube recurrence, exhaustively compares its lower bounds with all
subsets of cubes through dimension four, and checks the response classes
and two-probe certificate on the explicit 128-vertex graph. Computation
does not replace the universal proofs, and no bounded search is interpreted
as an evasion proof. The checker uses Python standard-library integer and
set arithmetic, without solvers, floating point, downloaded data, or graph
catalogues. Remaining trust is the written proof, Python, and hardware.
There is no formal proof-assistant verification or independent peer review
at initial publication.

The graph neighborhood through indexed height 4102 contained the open
question and two one-round criteria, but no substitution result. A targeted
primary-literature check on 2026-09-09 found [1] posing the greater-than-two
question and no overlapping substitution or join result. The proposed
novelty is the strategy-lifting theorem and sharp full-feedback join
example, relative to the graph and sources searched; this is not a priority
claim. The chordal corollary additionally uses [1, Theorem 2.3].

## References

1. John Jones and William B. Kinnersley, *The Directional Localization Game
   on Graphs*, arXiv:2609.01745v1 (2026), Sections 2.1–2.2 and Question 6.4.
   <https://arxiv.org/html/2609.01745v1>
2. Eero Räty, *Uniqueness in Harper's vertex-isoperimetric theorem*,
   arXiv:1806.11061v2 (2019), Theorem 1 and the definition preceding it.
   <https://arxiv.org/html/1806.11061v2>
