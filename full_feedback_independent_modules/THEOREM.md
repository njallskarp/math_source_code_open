# Independent modules preserve a one-round quotient's one-probe localization

## Results

Use the full-feedback directional localization game of Jones and Kinnersley
[1, Section 2.1]. A probe at \(p\) returns \(\{p\}\) for a robber at
\(p\); otherwise it returns every neighbor starting a shortest path to the
robber. Probes in a round are simultaneous. After an unresolved round the
robber may stay or move along one edge. Winning means locating its current
vertex within a bounded number of rounds.

Call a vertex \(p\) a **one-round resolver** if the full responses
\(D_G(p,x)\), for \(x\in V(G)\), are pairwise distinct. This is stronger
than merely assuming that the graph admits an adaptive one-probe strategy.

Let \(G\) be a finite connected simple graph of order at least two, and
replace each vertex \(v\) by an independent nonempty module \(M_v\) of
size \(m_v\). Put all edges between \(M_u\) and \(M_v\) exactly when
\(uv\in E(G)\), and write the resulting graph as \(X=G[\overline K_{m_v}]\).
Set \(M=\max_v m_v\).

**Theorem 1.** If \(p\) is a one-round resolver of \(G\), then one
probe per round wins on \(X\) within
\[
m_p+M-1
\]
rounds. In particular \(\zeta_d^*(X)=1\).

**Theorem 2 (sharp uniform round bound).** For every integer \(m\ge1\),
one-probe play on
\[
X_m=Q_3[\overline K_m]
\]
has optimal worst-case duration exactly \(2m-1\) rounds. Here \(Q_3\)
is the binary three-cube. Its every vertex is a one-round resolver, and
\(X_m\) has \(8m\) vertices. Thus Theorem 1's uniform bound cannot be
improved in general.

The uniform round bound is also attained by the elementary control
\(Q_2[\overline K_m]=K_{2m,2m}\): scanning one part wins in
\(2m-1\) rounds, and before that a robber can keep at least two candidates
in the probed part. The three-cube result provides an exact duration for
a different family; it is not claimed to be the first sharpness witness.

This improves the prior substitution bound of two probes to one for
independent substitutions of these quotients. It applies in particular to
all quotient graphs certified by the existing one-round random-graph and
degree/codegree criteria. It does **not** prove that independent
substitution preserves the whole adaptive one-probe class, and it does not
settle whether a connected graph can have \(\zeta_d^*>2\).

## Locating a known independent module

**Lemma.** Suppose an unresolved probing phase has confined the robber to
a subset \(A\) of one independent module \(M_v\), with \(a=|A|\ge2\).
One cop can locate it within \(a-1\) further rounds, despite its ensuing
moves.

*Proof.* Let \(U=N_X(M_v)\), the common external neighborhood; it is
nonempty by connectedness of the quotient. If \(|U|=1\), probe its
unique vertex \(u\) next. The possible positions are \(A\cup\{u\}\),
and each has a distinct singleton response at \(u\).

Otherwise \(|U|\ge2\). Probe any \(a_0\in A\). Every possible vertex
outside \(A\) lies in \(U\) and returns its own singleton; a target
at \(a_0\) also returns its own singleton. Every remaining vertex in
\(A\setminus\{a_0\}\) returns exactly \(U\), a nonsingleton set.
Thus either the cop wins immediately or the posterior is precisely
\(A\setminus\{a_0\}\). During the next move this set can contaminate
\(U\), but it cannot refill cleared vertices of \(M_v\), which is
independent. Repeat. When one candidate remains after a response, the cop
wins immediately; it need not probe that last candidate. The bound is
\(a-1\). A singleton posterior is already a win and needs no extra round.
\(\square\)

This lemma concerns exact current territories, so a singleton response
need not be globally distinguishing to be sufficient here.

## Proof of Theorem 1

If \(\deg_G(p)=1\), every vertex other than \(p\) gives the same
singleton response at \(p\). Since \(p\) resolves in one round and
\(G\) is connected, \(G=K_2\). Its independent substitution is complete
bipartite. If either part is a singleton, probing that vertex resolves the
graph in one round. Otherwise probe a vertex in a smallest part. An
unresolved response confines the robber to the unprobed vertices of that
part; apply the lemma. At most \(\max\{1,\min(m_u,m_v)-1\}\) rounds
suffice, within the claimed bound.

Now assume \(\deg_G(p)\ge2\), and put
\[
U=\bigcup_{v\in N_G(p)}M_v.
\]
Every response to a probe in \(M_p\), for a robber in another module,
projects under the module map to its exact quotient response. This follows
because distances between different modules equal their quotient
distances. A shortest path to a different module cannot begin with an
internal step, and when the modules are adjacent the response is the
singleton containing the actual target.

Since all quotient responses at \(p\) are distinct, any response other
than \(U\) identifies a single quotient vertex (or is a self response
that already wins). The only ambiguity involving several modules can be
\[
(M_p\setminus\{\text{probed vertex}\})\cup M_q,
\]
where \(q\), if it exists, is the unique quotient vertex satisfying
\(D_G(p,q)=N_G(p)\). It is nonadjacent to \(p\): neighbor responses
are singletons, whereas \(|N_G(p)|\ge2\). For such \(q\), its actual
response is exactly \(U\), not merely a set with the same projection.
The subgraph on \(M_p\cup M_q\) is independent. If \(q\) does not
exist, take \(M_q=\varnothing\).

Probe the vertices of \(M_p\) in a fixed order, continuing this scan only
while the response is \(U\) and the robber has not yet been localized.
Two successive \(U\) responses cannot bring a new candidate into
\(M_p\cup M_q\): both endpoints of the intervening robber move would
belong to that independent set, so the move must be a stay. Thus a cleared
vertex of \(M_p\) stays clear throughout an uninterrupted scan. This
accounts explicitly for every extra robber move during the scan.

At the first different response, the cop knows the robber's module.
If all \(m_p\) probes have returned \(U\), no candidate in \(M_p\)
remains, so the robber is confined to \(M_q\). (If \(q\) is absent,
that response history is impossible.) In either case a module is known
within \(m_p\) rounds. Its remaining candidate set has at most \(M\)
vertices, and the lemma adds at most \(M-1\) rounds. \(\square\)

## Exact duration for the three-cube substitution

Label cube vertices by \(v\in\{0,1\}^3\), and write
\(\bar v=v\mathbin\oplus111\) for the antipode. Vertices of \(X_m\)
are \((v,i)\), \(0\le i<m\). Two vertices are adjacent precisely when
their cube labels differ in one coordinate.

For a probe \(a\in M_w\), its response classes are:

- Every vertex in a neighboring module is identified by its own singleton.
- Each module \(M_z\) at cube distance two from \(w\) is a separate
  response class: its response is the union of their two common-neighbor
  modules.
- The class
  \[
  (M_w\setminus\{a\})\cup M_{\bar w}
  \]
  responds with the union of the three neighbor modules of \(w\).
- The probe itself has its self response.

These descriptions hold for \(m\ge2\), when the displayed unions have
sizes \(2m\) and \(3m\), distinct from singletons. For \(m=1\), the
quotient cube is itself one-round resolving, so the optimal duration is
one, as claimed.

The upper bound \(2m-1\) follows from Theorem 1. For the lower bound,
assume \(m\ge2\). A **core** is a nonempty set
\[
C=A\cup B,\qquad A\subseteq M_u,\quad B\subseteq M_{\bar u}.
\]
The robber maintains a territory \(N_X[C]\), and its progress measure
is the number \(|C|\). Initially take both antipodal modules in full,
so \(|C|=2m\) and \(N_X[C]=V(X_m)\).

We show that whenever \(|C|\ge3\), after any one probe the robber can
choose an unresolved response whose posterior is another core \(C'\)
with \(|C'|\ge|C|-1\). Its next territory is exactly \(N_X[C']\).

If both \(A\) and \(B\) are nonempty, all six other modules are fully
contaminated; in the two antipodal modules the contaminated subsets are
exactly \(A,B\). A probe in either of these two modules can be answered
with the three-neighbor-module response, leaving
\(C'=C\setminus\{\text{probe}\}\). A probe in some other module
\(M_w\) can receive that same type of response, now leaving
\(C'=(M_w\setminus\{\text{probe}\})\cup M_{\bar w}\), of size
\(2m-1\ge|C|-1\).

Otherwise the core lies in one module \(M_v\), say \(|C|=s\le m\).
Its territory contains exactly \(C\) and the three full neighbor modules
of \(v\). There are four cases for the probe's module \(M_w\):

1. If \(w=v\), the three-neighbor response leaves \(C\) minus the
   probed vertex, if present.
2. If \(w=\bar v\), that response leaves \(C\) unchanged.
3. If \(w\) is a neighbor of \(v\), choose a different neighbor
   \(z\) of \(v\). The distance-two response for \(M_z\) leaves the
   entire module \(M_z\), of size \(m\ge s-1\).
4. If \(w\) is at distance two from \(v\), its antipode \(\bar w\)
   is a neighbor of \(v\). The three-neighbor response leaves exactly
   \(M_{\bar w}\), again of size \(m\ge s-1\); the probe's own
   module is outside the current territory.

Every selected posterior has at least two vertices when \(|C|\ge3\),
so it cannot localize the robber. Starting at \(2m\), the measure stays
at least three before each of the first \(2m-2\) probes, and the robber
survives all of them. At least \(2m-1\) rounds are therefore required.
These are exact response intersections and closed-neighborhood moves;
no teleportation is implicit. Every finite history has a compatible
robber walk. Together with the upper bound this proves Theorem 2.
\(\square\)

## Dependencies, evidence, and novelty

These are written combinatorial proofs, not formalizations. The main
arguments import no external theorem beyond the game definition; the
quotient-response projection is also proved here. The first pass's general
substitution lemma supplies context, not an unproved premise. The
random-graph and degree/codegree corollaries additionally rely on those
specific criteria to provide one-round resolvers.

The accompanying standard-library checker computes responses from graph
distances, explores every branch of the constructive policy on a stated
finite domain, checks the core response invariant directly on small cube
substitutions, and independently solves their complete finite belief games.
The infinite families and the optimal-duration lower bound rest on the
universal proofs above, not on extrapolation from the finite runs.

The graph was refreshed through indexed height 4116 at the start of this
pass. Targeted searches on 2026-09-09 found no overlapping independent-module
theorem or this exact duration formula. The proposed novelty is relative
to the graph and primary sources searched, not a historical-priority claim.
The general assertion that independent substitution preserves arbitrary
adaptive one-probe localization remains unresolved in this work.

## Reference

[1] John Jones and William B. Kinnersley, *The Directional Localization Game
on Graphs*, arXiv:2609.01745v1 (2026), Section 2.1 and Question 6.4.
<https://arxiv.org/html/2609.01745v1>
