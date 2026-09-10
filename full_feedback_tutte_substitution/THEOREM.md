# Arbitrary substitutions over the Tutte 12-cage need at most two probes

## Main result

Let \(T\) be the Tutte 12-cage on 126 vertices. For every family of nonempty finite simple graphs \((H_v)_{v\in V(T)}\),
\[
\zeta_d^*(T[H_v])\le2.
\]
The strategy below locates the robber within five rounds. The internal graphs may have arbitrary orders and edges and may be disconnected. The substituted graph has disjoint vertex sets \(M_v=V(H_v)\), retains each internal graph, and joins every vertex of \(M_u\) to every vertex of \(M_v\) exactly when \(uv\in E(T)\).

The result combines a universal simulation lemma with an exact finite policy certificate. The universal quantifier over internal graphs follows from the written proof, not extrapolation from finite tests. Five rounds is an upper bound, not a claim of optimal duration. No equality is asserted for every substitution.

The earlier [adjacent-pair separation](https://github.com/njallskarp/math_source_code_open/tree/main/full_feedback_adjacent_pair_separation) proves that \(T\) itself has full-feedback parameter two while every strategy using adjacent probes loses. Thus adjacent-pair failure does not suffice to make a quotient useful for amplification above two. The present result closes the arbitrary-substitution route over this quotient.

## Full responses and a weaker auxiliary rule

For any connected graph \(G\), the ordinary full response is
\[
D_G(p,p)=\{p\},\qquad
D_G(p,x)=\{w\in N_G(p):d_G(w,x)=d_G(p,x)-1\}\quad(x\ne p).
\]
The actual game is the simultaneous full-feedback game of [Jones and Kinnersley, Section 2.1](https://arxiv.org/html/2609.01745v1). A pre-probe territory \(B\) and joint response class \(C\) give posterior \(B\cap C\). A singleton wins immediately. Otherwise the next territory is \(N_G[B\cap C]\), allowing one edge or a stay.

Define an auxiliary feedback rule by
\[
E_G(p,x)=D_G(p,x)\quad(x\ne p),\qquad E_G(p,p)=N_G(p).
\]
Only the self response is changed. In this auxiliary game a probe at the target is not an automatic win: victory still requires a singleton posterior under the \(E_G\) responses. This is deliberately weaker information. The robber movement rule is unchanged. The ordinary substituted game always retains its genuine self response \(\{p\}\).

## Universal simulation lemma

**Lemma.** Suppose \(G\) is finite, connected, and has at least two vertices. If \(k\) probes win the auxiliary \(E_G\) game within \(r\) rounds, then every substitution \(G[H_v]\) with nonempty finite internal graphs has
\[
\zeta_d^*(G[H_v])\le\max\{k,2\},
\]
with duration at most \(r+1\).

**Proof.** Write \(\pi\) for the known map from actual vertices to their quotient modules. The cops simulate the auxiliary strategy, choosing a representative \(a\in M_p\) whenever it asks for a quotient probe \(p\). Repeated quotient probes may use the same representative; repetitions provide no extra auxiliary information. Any extra cops can be ignored until the finishing round.

We first analyze one actual response \(D(a,x)\).

**Internal labels identify a module.** If \(x\notin M_p\), every vertex of \(M_p\) has the same distance to \(x\), namely the distance between the two quotient modules. A first step remaining inside \(M_p\) therefore cannot shorten the path to \(x\). Consequently, if the response contains any vertex of \(M_p\), the target is in \(M_p\). This includes a direct self hit, which already wins the actual game. Other internal labels may identify only the module, which is sufficient for the finishing step below.

**Responses without internal labels project to \(E_G\).** If \(x\notin M_p\), projecting the response gives exactly \(D_G(p,\pi(x))\). For adjacent modules the actual response is the target singleton \(\{x\}\); for quotient distance at least two, every vertex in a shortest first-step module is a possible first step, and no other module is. Internal first steps cannot help, as just shown.

If \(x\in M_p\) and no internal label occurs, then \(x\ne a\) and \(x\) is not internally adjacent to \(a\). Since \(G\) is connected and nontrivial, \(p\) has a neighbor, so a two-edge path through an external module is available. The actual distance is therefore two. Every external neighbor of \(a\) is also adjacent to \(x\), so the response contains the entire union of the neighboring modules. By the assumed absence of internal labels it contains nothing else. Its projection is precisely \(N_G(p)=E_G(p,p)\).

Thus either a response already identifies the target's module, or every response in that actual round projects to the auxiliary response for the actual quotient position. Until early module identification, the cops can follow the auxiliary strategy exactly. An actual edge or stay projects to a quotient edge or stay, so one actual round implements one auxiliary round without inserting any extra robber move. Inductively the auxiliary territory contains the actual quotient position. A singleton auxiliary posterior therefore identifies the actual module. This happens by round \(r\), unless the module was identified earlier.

**One finishing round identifies the actual vertex.** Suppose the target is known to lie in \(M_w\). After its next legal move it lies in \(N[M_w]\), which is \(M_w\) together with all neighboring modules. Choose any quotient neighbor \(v\) of \(w\), and probe representatives \(a\in M_w\), \(b\in M_v\).

For a target \(y\in M_w\), the response at \(b\) is \(\{y\}\). If an external target \(x\notin M_w\) shared that singleton response, all vertices of \(M_w\) would be equally short first steps from \(b\) to \(x\), because they are all neighbors of \(b\) at the same distance from \(x\). Thus \(M_w\) would have to be the singleton \(\{y\}\). In that case \(a=y\), and the self response at \(a\) distinguishes \(y\) from \(x\). Hence targets in \(M_w\) are globally distinguished by the pair. Every possible target outside \(M_w\) is adjacent to \(a\), so gives its own singleton at \(a\). These outside targets are distinguished from one another and, by the preceding argument, from every inside target.

This final round therefore wins. It uses two probes, and occurs no later than round \(r+1\). The argument covers singleton modules and every internal edge pattern. \(\square\)

The adjacent finishing observation already appears in the earlier [general substitution bound](https://github.com/njallskarp/math_source_code_open/tree/main/full_feedback_substitution); it is included here to make the proof interface self-contained. The new simulation step permits arbitrary probe pairs in the auxiliary game.

The condition is sufficient, not necessary. On \(K_2\), the auxiliary responses reveal no position even if every vertex is probed, whereas every substitution over \(K_2\) is localizable with two adjacent probes. Failure in the auxiliary game alone would therefore not establish a lower bound for a real substitution.

## Why distance-two probes are useful here

**Geometric lemma.** Let \(G\) be connected and bipartite, with diameter \(D\ge3\), girth at least \(2D\), and minimum degree at least two. For any probes \(p,q\) at distance two, the ordinary and auxiliary joint response partitions of \(V(G)\) are identical.

**Proof.** A target at positive distance less than \(D\) has a unique shortest path from a probe: two different shortest paths would contain a cycle shorter than \(2D\). A target at distance \(D\) returns the probe's entire neighborhood, since bipartiteness forces every neighbor to have distance \(D-1\) or \(D+1\), and the latter is impossible. Thus only opposite targets return a nonsingleton full neighborhood in the ordinary game.

Let \(c\) be the unique common neighbor of \(p,q\). Only the response vectors of targets \(p,q\) change when passing from \(D_G\) to \(E_G\); all other vectors are unchanged. In the auxiliary game the vector for target \(p\) is \((N(p),\{c\})\). Suppose an external target \(x\notin\{p,q\}\) had this vector. Then \(d(p,x)=D\), so \(d(c,x)=D-1\). Its singleton response \(\{c\}\) at \(q\) would force \(d(q,x)=D\), but at that distance the response is all of \(N(q)\), not a singleton. This is a contradiction. The two changed vectors are distinct because every neighborhood has size at least two. The symmetric argument handles target \(q\). Both probed vertices remain singleton classes, and all other classes are unchanged. \(\square\)

The Tutte 12-cage satisfies these hypotheses with \(D=6\). The code checks the partition identity separately for all 378 distance-two actions. This lemma motivates the search restriction; the certificate is also checked directly with the auxiliary responses and does not depend on trusting the search or the lemma's implementation.

## The finite four-round certificate

The verifier constructs the Tutte 12-cage from the standard LCF sequence
\[
(17,27,-13,-59,-35,35,-11,13,-53,53,-27,21,57,11,-21,-57,59,-17)^7.
\]
Vertices are \(0,\ldots,125\), joined in a cycle and with the specified chord shifts. This matches the [SageMath generator](https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/generators/smallgraphs.html#sage.graphs.generators.smallgraphs.Tutte12Cage). Order 126, size 189, degree three, bipartiteness, diameter six, and girth twelve are checked directly.

`policy.json` contains 312 rows \((B,r,p,q)\), with bit-mask territories and decreasing ranks. There are 1, 14, 108, and 189 rows at ranks four, three, two, and one. The root probes 0 and 2, and every probe pair is at distance two. The checker partitions each reachable territory using \(E_G\), accepts every singleton, and requires the exact closed neighborhood of every nonsingleton posterior to have a row with rank lowered by one. All 332 unresolved branches and 2177 singleton branches are checked. No unresolved posterior is permitted at rank one, and all certificate rows must be reachable.

Rank induction gives a four-round auxiliary winning strategy. Apply the simulation lemma with \(k=2\) and \(r=4\) to obtain the main five-round substitution bound.

## Actual expanded-game audits and trust boundary

`audit_expansion.py` implements full responses directly in actual substituted graphs by propagating shortest first steps in breadth-first search. It does not replace the actual self response. It follows the simulated quotient policy while exhaustively branching on actual response classes, checks internal module identification, checks quotient projection and legal moves, and checks the final adjacent pair. Its response computation differs from the quotient checker's direct distance-table definition.

Seven scenarios cover singleton modules, independent pairs, clique triples, four-vertex paths, four-vertex stars probed at a leaf, three-dimensional cubes, and mixed internal graphs of orders one through five, including disconnected modules. The largest actual graph has 1008 vertices. The star case exercises nonsingleton responses with internal labels. These are complete histories for the specified strategy, not sampling of robber walks or optimization of duration.

A separate local audit uses every connected labeled quotient of orders two through four: 43 quotients and four explicit module assignments each, totaling 172 expanded graphs. It checks every actual probe/target projection and every choice of representatives in the adjacent finishing step. These cover 12,246 projection identities, 3984 internal-label cases, and 7190 finishing actions, including leaf and singleton boundary cases.

The universal conclusion rests on the written simulation; finite audits support its interfaces. The published programs use Python's standard library, exact integers and sets, and no solver, floating point, external graph catalogue, or downloaded input. The policy was discovered with symmetry-assisted search, but its concrete verification imports no symmetry library and uses no orbit reduction. Three corrupted policy files are rejected. The mathematical proof and checker remain unformalized; trust remains in the explicit input, written arguments, Python implementation and semantics, and hardware.

## Status and construction consequence

The graph, original full-feedback model, and preceding adjacent-pair separation are prior context. The new results are the universal auxiliary-feedback simulation, the distance-two partition lemma, and the certified substitution bound for this quotient. The primary game paper and narrow searches were checked on 2026-09-10; no matching result was identified. Novelty is relative to those checked sources, not a historical-priority claim.

This contribution awaits independent peer review. Reviews of the earlier projective-plane theorem or the Tutte adjacent-pair separation do not review this new simulation interface. Every arbitrary substitution over the Tutte quotient is now excluded as a route to an unrestricted parameter greater than two. The original greater-than-two question remains unresolved.
