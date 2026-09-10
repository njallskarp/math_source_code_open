# Two unrestricted probes can win when every adjacent pair loses

## Statement

Let \(T\) be the Tutte 12-cage on 126 vertices. In the full-feedback directional localization game:

1. Two unrestricted probes locate the robber within three rounds.
2. If the two probes must be adjacent in every round, the robber can evade forever.
3. Consequently \(\zeta_d^*(T)=2\), and the adjacent-pair restriction cannot be imposed without loss of winning power.

This is an exact computer-assisted finite theorem. Three rounds is an upper bound, not a claimed optimum. The graph is not an example with unrestricted parameter greater than two. No substitution over it is claimed to have parameter greater than two.

## Explicit graph and game

The vertices are \(0,\ldots,125\), with a cycle in that order. Add the chord from \(i\) to \(i+L_{i\bmod18}\pmod{126}\), where

\[
L=(17,27,-13,-59,-35,35,-11,13,-53,53,-27,21,57,11,-21,-57,59,-17).
\]

Edges are undirected and duplicate descriptions give one edge. This is the standard LCF description with the shift list repeated seven times, also used by the [SageMath generator](https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/generators/smallgraphs.html#sage.graphs.generators.smallgraphs.Tutte12Cage). The verifier constructs the graph directly, and checks order 126, size 189, degree three, bipartiteness, diameter six, and girth twelve. From every vertex the distance-layer sizes are \((1,3,6,12,24,48,32)\). The [DistanceRegular.org entry](https://www.math.mun.ca/distanceregular/graphs/tutte12.html) identifies the graph as the incidence graph of \(GH(2,2)\); that identification is not used in the proof.

For a probe \(p\) and target \(x\), the response is

\[
D(p,p)=\{p\},\qquad
D(p,x)=\{w\in N(p):d(w,x)=d(p,x)-1\}\quad(x\ne p).
\]

All shortest-path directions are returned simultaneously. A territory \(B\) is the set of possible positions immediately before probing. A joint response class \(C\) gives the posterior \(B\cap C\). A singleton posterior wins immediately. Otherwise the robber can stay or move along one edge, giving next territory \(N[B\cap C]\). This is the model of [Jones and Kinnersley, Section 2.1](https://arxiv.org/html/2609.01745v1).

The adjacency restriction applies only within each round. The cops may choose an entirely different edge in the next round; no movement restriction between rounds is imposed.

## Evasion against every adjacent pair

Define the family

\[
\mathcal F=\{N[\{a,b\}]:2\le d(a,b)\le4\}.
\]

The following finite property is checked exhaustively:

> For every unordered pair \(\{a,b\}\) with \(2\le d(a,b)\le4\), and every edge \(pq\), there are vertices \(x,y\in N[\{a,b\}]\) such that \(2\le d(x,y)\le4\), \(D(p,x)=D(p,y)\), and \(D(q,x)=D(q,y)\).

There are 378, 756, and 1512 unordered core pairs at distances two, three, and four respectively. The checker enumerates all 2646 pairs and all 189 edge actions, without using graph automorphisms or identifying symmetry classes. It therefore verifies 500,094 obligations. For each obligation it checks every potential witness in lexicographic order until one succeeds. It uses exact breadth-first distances and actual response sets, with no estimated or partial directions.

This property proves evasion. Initially the full territory contains a member \(F\in\mathcal F\). If a current territory contains \(F=N[\{a,b\}]\), and the cops probe any edge \(pq\), choose the joint response shared by the certified \(x,y\). Both are possible, so the posterior is not a singleton. After the legal robber move, the next territory contains \(N[\{x,y\}]\), another member of \(\mathcal F\). The invariant can be repeated indefinitely.

The invariant concerns legal histories, not an evader that can jump between arbitrary vertices. Every selected posterior is contained in the current territory, and every following territory is produced by a closed-neighborhood move. For any deterministic cop strategy the resulting infinite response history has a legal robber walk: the tree of consistent finite walks is finitely branching, has nodes at every depth, and thus has an infinite branch. This is the usual belief-state interpretation of indefinite evasion.

The certificate is the explicit graph and the formula for \(\mathcal F\); no large stored list of territories or action witnesses is needed. A digest of all 500,094 selected witness rows is printed for reproducibility. The digest is not substituted for checking the obligations.

## Winning with unrestricted pairs

`policy.json` contains 122 rows \((B,r,p,q)\). Here \(B\) is the integer mask of a territory, \(r\) is a positive decreasing rank, and \(p,q\) are the probes. Bit \(v\) of \(B\) represents vertex \(v\).

The root is the full territory at rank three, probing vertices 0 and 5. For every reachable row the verifier partitions the entire territory by the actual ordered response pair. Every singleton class wins. Every nonsingleton posterior has its exact closed neighborhood present as a row of rank \(r-1\). No nonsingleton posterior is permitted at rank one. All listed rows must be reachable.

The complete policy check covers 123 nonsingleton response branches and 1011 singleton response branches. Rank induction proves a win within three rounds. The policy was found with symmetry-assisted search, then expanded into concrete vertex masks and probe pairs. Neither the symmetry reduction nor its search code is used by the verifier.

Finally, one unrestricted probe cannot win: if it could, adding a neighboring second probe each round and ignoring its answer would give a winning adjacent-pair strategy. Every vertex of \(T\) has a neighbor. This contradicts the evasion certificate, establishing the claimed exact value two.

## Meaning for substitution amplification

The earlier [adjacent-probe substitution theorem](https://github.com/njallskarp/math_source_code_open/tree/main/full_feedback_projective_substitution) gives a universal bound of two for arbitrary substitutions over quotients that admit adjacent-pair winning strategies. Its guard applies beyond the projective-plane family. The present graph does not meet that hypothesis. This is a concrete boundary of that construction obstruction, not a counterexample to the theorem.

The more general [factor-two substitution bound](https://github.com/njallskarp/math_source_code_open/tree/main/full_feedback_substitution) still bounds every substitution over \(T\) by four. Whether a specific substitution over \(T\) needs three or four probes is a separate question. A lower bound there must cover all unrestricted probe pairs in the expanded graph.

## Evidence, literature, and limits

The graph is classical. The new claim is the finite separation between unrestricted pairs and adjacent pairs in this game. The primary game paper, its Question 6.4, the committed graph neighborhood, and narrow searches for directional localization with Tutte cages, adjacent probes, and generalized hexagons were checked on 2026-09-10. No matching separation was identified. This supports search-relative novelty only, not historical priority.

The proof depends on the written invariant and rank arguments, the explicit LCF input, `policy.json`, and the exact finite checks in `verify.py`. The checker uses only Python's standard library, integer/set operations, and breadth-first search; there is no floating point, external graph catalogue, solver, symmetry library, or network input in reproduction. CPython and hardware correctness and the unformalized mathematical bridge remain the trust boundary. The author-run independent checker is validation, not external peer review. This result has not yet received an independent peer review.
