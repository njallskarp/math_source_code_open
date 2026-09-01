# Every one-vertex Ramsey extension obstruction covers the whole core

## Result type

**Exact symbolic lemma.** This statement is independent of computation and
applies to every classical two-color Ramsey extension problem.

## Signed extension clauses

Let \(G\) be a red/blue coloring of \(K_n\) with no red \(K_s\) and no blue
\(K_t\). To add a prospective vertex \(\star\), introduce a Boolean variable
\(x_v\) for each \(v\in V(G)\), with \(x_v=1\) when \(\star v\) is red and
\(x_v=0\) when it is blue.

Each red \(K_{s-1}\), say \(R\), supplies the clause

\[
C_R=\bigvee_{v\in R}\neg x_v,
\]

and each blue \(K_{t-1}\), say \(B\), supplies the clause

\[
C_B=\bigvee_{v\in B}x_v.
\]

The complete signed-clause system is satisfiable exactly when \(G\) admits a
one-vertex extension with no red \(K_s\) and no blue \(K_t\).

## Lemma

Let \(\mathcal U\) be any unsatisfiable subset of the signed extension clauses
of a Ramsey \((s,t,n)\)-coloring \(G\). Then

\[
\bigcup_{C\in\mathcal U}\operatorname{var}(C)=V(G). \tag{1}
\]

Equivalently, every core vertex occurs in every unsatisfiable extension-clause
subsystem.

## Proof

Suppose a vertex \(w\in V(G)\) is absent from every clause in \(\mathcal U\).
For each \(v\ne w\), define

\[
x_v=\begin{cases}
1,&wv\text{ is red in }G,\\
0,&wv\text{ is blue in }G.
\end{cases} \tag{2}
\]

Set the unused variable \(x_w\) arbitrarily.

Consider a red clause \(C_R\in\mathcal U\). Since \(w\notin R\), violation of
\(C_R\) would mean that \(R\) is a red \(K_{s-1}\) and every edge from \(w\)
to \(R\) is red. Then \(R\cup\{w\}\) would be a red \(K_s\) in \(G\), a
contradiction. Thus every red clause in \(\mathcal U\) is satisfied by (2).

The complemented argument handles a blue clause: if a blue
\(K_{t-1}\), \(B\), violated \(C_B\), then all edges from \(w\) to \(B\)
would be blue, producing a blue \(K_t\) in \(G\). Hence (2) satisfies every
clause of \(\mathcal U\), contradicting its unsatisfiability. Therefore no
such \(w\) exists, proving (1). \(\square\)

## Consequence for \(R(5,5)\)

For every Ramsey \((5,5,42)\)-coloring, any symbolic nonextension certificate
formed solely from signed \(K_4\) clauses must collectively mention all 42
core vertices. This is a structural lower bound on the support of a clause
obstruction, even though it does not bound the number of clauses.

The accompanying 74-clause obstruction for authoritative graph 0 attains this
coverage bound: its clauses contain exactly 42 distinct variables.

## Novelty and scope

The committed Discovery Net graph and the searched primary \(R(5,5)\)
literature contained one-vertex extension algorithms and nonextendibility
statements, but no matching support lemma was found. The cloning argument is
elementary, so no broad priority claim is made; its value is as a reusable
proof-design constraint and an exact optimality baseline for compact
extension certificates.

This lemma does not assert that every full extension system is unsatisfiable,
give a lower bound on the number of clauses in an obstruction, or determine a
Ramsey number.
