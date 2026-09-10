# Two adjacent probes obstruct projective-plane substitution amplification

## Main statement

Let \(G_i\) be the incidence graph of any finite projective plane of
order \(q_i\ge2\), for \(1\le i\le d\), where \(d\ge1\). Put

\[
Q=G_1\mathbin\square\cdots\mathbin\square G_d.
\]

Replace each vertex \(v\) of \(Q\) by an arbitrary nonempty finite
simple graph \(H_v\), with all possible edges between two modules
exactly when their quotient vertices are adjacent. For the resulting
substitution graph \(X=Q[H_v]\),

\[
\boxed{\ \zeta_d^*(X)\le2.\ }
\]

There is a strategy using two **adjacent** probes in every round and
at most

\[
1+\sum_{i=1}^d q_i
\]

rounds. The quotient \(Q\) itself can be localized by adjacent probes
within \(\sum_i q_i\) rounds. These are upper bounds, not claims of
optimal duration. The module graphs may be disconnected, have arbitrary
orders, and have arbitrary internal edges.

The original projective-plane parameter two and the unrestricted
Cartesian-product formula are due to Jones and Kinnersley. The new
ingredient here is a full-feedback strategy that retains adjacency of
the two probes, allowing the substitution upper bound to remain two.
Thus these constructions cannot answer their question asking for
parameter greater than two. This is a structural obstruction to that
amplification route, not a solution of the general question.

## Model and notation

A probe at \(p\) returns \(\{p\}\) for target \(p\). Otherwise its
full response is

\[
D(p,x)=\{u\in N(p):d(u,x)=d(p,x)-1\}.
\]

If the possible locations before a probe are \(T\), and its response
class is \(C\), the posterior is \(T\cap C\). A singleton is already
a win. Otherwise the robber may stay or move over one edge, giving
the next territory \(N[T\cap C]\). With two probes, use their joint
response class. All strategies below use this exact move rule.

In a projective plane, every point lies on \(q+1\) lines and every
line contains \(q+1\) points. Distinct points have a unique joining
line, and distinct lines a unique intersection point. In its incidence
graph, two distinct vertices of the same type have distance two and
the response between them is their unique common neighbor. A point
and a nonincident line have distance three: every neighbor of either
probe starts a shortest path to the other, so the full response is
the probe's entire neighborhood.

## A shrinking set on one line or through one point

Call a nonempty set \(A\) a core if it is contained in \(N(z)\)
for some vertex \(z\). Thus it consists entirely of points on one
line, or entirely of lines through one point. When \(|A|\ge2\),
the vertex \(z\) is uniquely determined by \(A\).

**Lemma 1.** Suppose the previous posterior is contained in a core
\(A\), with \(s=|A|\ge2\). Two adjacent probes can either locate
the robber next round or leave a new core of size at most \(s-1\).

**Proof.** It suffices to consider the full territory \(N[A]\)
after the move; a smaller actual territory only improves the bounds.
By duality assume that \(A\) consists of points on line \(z\).
Choose any \(a\in A\), and any line \(b\) through \(a\) other
than \(z\). Probe the adjacent pair \((a,b)\).

The only possible point targets are in \(A\). Target \(a\) is
located. Every other point in \(A\setminus\{a\}\) gives responses
\(\{z\}\) and \(N(b)\), since \(b\) intersects \(z\) only at
\(a\). This is one core of size \(s-1\).

The possible line targets are the lines meeting \(A\). Any line
\(\ell\) through \(a\) gives first response \(\{\ell\}\).
If \(\ell\ne b\), its second response is \(\{a\}\); target
\(b\) gives its self response. These line targets are individually
identified. Their signatures cannot coincide with the preceding point
class, whose second response has \(q+1\) elements.

A remaining line target \(\ell\) is not through \(a\). Its first
response is \(N(a)\), with \(q+1\) elements, and its second is
\(\{c\}\), where \(c=b\cap\ell\ne a\). This signature cannot
coincide with any point-target or incident-line signature, whose first
response is a singleton. For a fixed \(c\), every such \(\ell\)
meets \(z\) in some point of \(A\setminus\{a\}\). For each
of those points there is at most one joining line to \(c\). Thus
the response class has at most \(s-1\) members, all lines through
\(c\). It is another core. Duality gives the other case. \(\square\)

**Lemma 2.** Two adjacent probes localize the incidence graph within
\(q\) rounds.

**Proof.** First probe any incident point-line pair \((p,L)\).
The point \(p\), the line \(L\), points on \(L\), and lines
through \(p\) are individually distinguished by the joint response.
For a point \(x\notin L\), the response is
\((\{px\},N(L))\). It specifies the \(q\)-point core
\(px\setminus\{p\}\). For a line \(\ell\) not through \(p\),
the response is \((N(p),\{L\cap\ell\})\). It specifies the
\(q\) lines through \(L\cap\ell\) other than \(L\).
The two response types are distinct because \(q+1>1\).

Every unresolved first posterior is therefore a core of size \(q\).
Lemma 1 reduces its size by at least one each subsequent round until
a singleton is reached. This takes at most \(q-1\) further rounds,
and all probe pairs are adjacent. \(\square\)

The argument uses full feedback essentially: the nonsingleton full
neighborhood distinguishes the two types of target. It is not claimed
as a strategy for the partial-feedback game.

## Cartesian products preserve this probe restriction

**Lemma 3.** Suppose each connected graph \(F_i\) has a two-probe
winning strategy using adjacent probes in every round, within \(r_i\)
rounds. Their finite Cartesian product has such a strategy within
\(\sum_i r_i\) rounds.

**Proof.** Cartesian distances add. From a full response at a product
vertex, collect the returned neighbors differing from the probe in
coordinate \(i\). Their \(i\)-coordinates form exactly the shortest
directions in that factor. If this collection is empty, the target's
\(i\)-coordinate equals the probe's \(i\)-coordinate; decode the
factor response as the self response. This also handles a product
self response. Thus each actual full response determines every factor
response exactly.

Process the factors one at a time. During phase \(i\), use the
adjacent pair prescribed by the strategy on \(F_i\) in coordinate
\(i\). Give both probes equal coordinates in every other factor.
The product probes are adjacent. The robber's projection in the active
factor either stays or moves along one edge between rounds, so it is
a valid factor game. Coordinate \(i\) is located within \(r_i\)
rounds.

After locating a coordinate at \(x\), keep both probes at its last
known value in every later round. After the robber's next move that
coordinate lies in \(N[x]\). Restricted to \(N[x]\), probing \(x\)
distinguishes every vertex: the response is its own singleton label.
The cops can therefore update this coordinate's exact location each
round while processing later factors. Both probes use the same updated
coordinate, so adjacency is retained.

After all phases every coordinate is known at the same probing phase,
and hence so is the product vertex. There are at most \(\sum_i r_i\)
rounds. \(\square\)

This phase-by-phase version preserves adjacency of the probes. It uses
the factor-response and coordinate-tracking mechanisms of the original
Cartesian-product argument; the original unrestricted max formula is
not being claimed anew.

## Adjacent probes lift through arbitrary modules

The following is the adjacent-pair special case of the preceding
[substitution theorem](../full_feedback_substitution/), restated with
its proof so the present bound is self-contained.

**Lemma 4.** If a connected quotient \(Q\) of order at least two has
a two-probe strategy using adjacent probes in every round and at most
\(r\) rounds, then every substitution \(Q[H_v]\) has such a strategy
within \(r+1\) rounds.

**Proof.** Replace adjacent quotient probes \(u,v\) by representatives
\(a\in H_u\), \(b\in H_v\). They are adjacent. They globally
distinguish every target in either probed module. To see this for
\(x\in H_u\), the response at \(b\) is \(\{x\}\). Another
target in \(H_u\) gives its own distinct singleton. If a target
\(y\notin H_u\) also gives \(\{x\}\), then every vertex of
\(H_u\) is equally valid as a shortest first step from \(b\) to
\(y\), because all vertices of a module have the same distances to
external targets. Hence \(H_u\) would have to be the singleton
\(\{x\}=\{a\}\). In that case the probe at \(a\) distinguishes
\(x\) by its self response. The proof for \(H_v\) is symmetric.

Unless the actual game has already ended, the target is therefore
outside both probed modules. Project each returned neighbor to its
quotient module. The projected response is exactly the quotient full
response. For an adjacent target module the actual response is the
singleton target; for a more distant module, it is the union of the
modules along all quotient shortest first steps. Internal steps cannot
start a shortest path to an external module.

The projected robber history has at most one edge-or-stay move per
actual round. The cops can therefore follow the quotient strategy
without inserting any extra rounds. Within \(r\) rounds it either
locates the actual vertex or identifies its module \(H_w\).

After the next move, the target lies in \(H_w\) or one of its adjacent
modules. Probe a representative of \(H_w\) and a representative of
any adjacent module. The guard argument globally identifies targets
inside \(H_w\). All other possible targets are adjacent to the first
probe and give distinct singleton responses. This final pair locates
the target. \(\square\)

Combining Lemmas 2, 3, and 4 proves the main statement.

## Verification and scope of the evidence

The theorem is a written combinatorial proof for every finite projective
plane, including non-Desarguesian planes, every finite number of factors,
and every choice of nonempty finite internal graphs. It is not an
extrapolation from the following finite audits.

`verify.py` generates the classical planes over the prime fields of
orders 2, 3, and 5, checks their incidence axioms, and derives responses
from breadth-first graph distances. It audits every incident first probe,
every nonsingleton subset of every line or point pencil, and every
allowed pair in Lemma 1. It also explores every response branch of the
stated policy on the 196-vertex Cartesian product of two Fano incidence
graphs, with exact one-edge recontamination, and on eight substitutions
over the order-2 and order-3 planes. Those include empty, complete,
path, and mixed singleton/nontrivial modules.

The product audit independently checks response projection on all
probe-target-coordinate triples before running the history-sensitive
policy. The substitution audit checks the module guard, quotient history,
and final module resolution against responses in the actual expanded
graph. No search cap or timeout is interpreted as a theorem.

The remaining trust boundary is the written mathematics, Python's exact
integer/set operations, the finite graph generators, and hardware. No
solver, floating point, external graph catalogue, downloaded input, or
formal proof assistant is used. No independent peer review has occurred.

## Literature and research consequence

Jones and Kinnersley,
[*The Directional Localization Game on Graphs*](https://arxiv.org/html/2609.01745v1),
Theorems 3.7 and 5.9, establish the unrestricted product formula and the
projective-plane value two. Their Question 6.4 asks for a graph with full
parameter above two. Those results and the game definition are prior work.

The proposed new contribution is the adjacent-probe core-shrinking
strategy and the resulting two-probe bound for arbitrary substitutions
over products of projective-plane incidence graphs. It is new to the
graph and primary sources searched on 2026-09-10; no historical priority
claim is made. Round optimality is not asserted.

This closes a natural amplification family based on genuine two-probe
quotients. A subsequent substitution search must first escape the
adjacent-pair strategy property, as well as the earlier one-probe-quotient
bound. A failure under the adjacent-pair restriction alone would still
not prove failure of unrestricted two-probe strategies.
