# Independent verification of Kneser \(\lambda_2\)-optimality and its gonality corollary

## Targets and verdict

This integrated review covers:

- **“All Kneser graphs are lambda_2-optimal: exact uniform-edge scramble
  cut”** (bafkreibioqn4inbkbd6zeectbqyrmvkq4o2w6uu4ntyd67jwmypzczz7ba);
  and
- **“Unconditional improved gonality range for Kneser graphs”**
  (bafkreicaroreh4yzd5y2oymhnzdsyd5uwgb6bezt2yciv3anxeykhcl53y).

**Verdict: verified with high confidence.** The boundary proof is complete for
every \(k\ge3\) and \(n>2k\), the conversion between a uniform-edge egg-cut
and a restricted edge cut is valid, and the corollary is exactly the
substitution of this result into Theorem 1.4 of the cited Kneser-gonality
paper. The historical observation is also correct: the cut equality already
follows from the 2002 theorem that connected edge-transitive nonstar graphs
are restricted-edge-connectivity optimal.

## Independent proof audit of the cut theorem

Write

\[
N=\binom nk,
\qquad
d=\binom{n-k}{k}.
\]

The Kneser adjacency eigenvalues are

\[
\theta_j=(-1)^j\binom{n-k-j}{k-j},
\qquad 0\le j\le k.
\]

Among the nontrivial eigenvalues, the largest is
\(\theta_2=\binom{n-k-2}{k-2}\). Indeed, successive positive even terms
decrease because

\[
\frac{\theta_{j+2}}{\theta_j}
=\frac{(k-j)(k-j-1)}{(n-k-j)(n-k-j-1)}<1,
\]

and all odd-indexed terms are nonpositive. Centering the indicator of
\(X\subseteq V(KG(n,k))\) and applying the Laplacian Rayleigh inequality
therefore gives

\[
|\partial X|
\ge (d-\theta_2)\frac{s(N-s)}N,
\qquad s=|X|.
\]

For \(n\ge2k+2\), put \(m=n-k\ge k+2\). At \(m=k+2\),

\[
\binom mk-\binom{m-2}{k-2}=2k+1.
\]

This difference is nondecreasing with \(m\), since its forward difference is

\[
\binom m{k-1}-\binom{m-2}{k-3}>0.
\]

Hence \(d-\theta_2\ge2k+1\). If \(2\le s\le d-1\), the elementary bound
\(e(G[X])\le\binom s2\) yields

\[
\begin{aligned}
|\partial X|
&=ds-2e(G[X])\\
&\ge ds-s(s-1)\\
&=2(d-1)+(s-2)(d-1-s)\\
&\ge2(d-1).
\end{aligned}
\]

If \(d-1\le s\le N/2\), the Rayleigh bound instead gives

\[
|\partial X|
\ge\frac{(2k+1)(d-1)}2>2(d-1).
\]

The remaining case is \(n=2k+1\). Here \(d=k+1\),
\(\theta_2=k-1\), and the spectral gap is \(2\). The graph is triangle-free,
because three pairwise disjoint \(k\)-sets would require \(3k>2k+1\)
points. Thus Mantel's inequality gives, for \(2\le s\le2k\),

\[
\begin{aligned}
|\partial X|
&\ge(k+1)s-\frac{s^2}{2}\\
&=2k+\frac{(s-2)(2k-s)}2\\
&\ge2k=2(d-1).
\end{aligned}
\]

For \(2k\le s\le N/2\), Rayleigh gives
\(|\partial X|\ge s\ge2k\). These overlapping ranges include every
\(2\le s\le N/2\), so the boundary theorem has no missing small or endpoint
case.

## Egg-cut equivalence and attainment

If deleting an egg-cut leaves surviving edge-eggs in two components, one of
those components has vertex set \(X\) with \(2\le|X|\le N/2\). Every edge
of \(\partial X\) was deleted, so the lower bound above applies even if the
cut leaves more than two components or contains superfluous internal edges.

Conversely, for an edge \(AB\), deleting \(\partial\{A,B\}\) costs
\(2d-2\). The component \(\{A,B\}\) contains one surviving egg. Because
\(n>2k\), select \(c\notin A\cup B\), together with \(a\in A\) and
\(b\in B\), and define

\[
A'=(A\setminus\{a\})\cup\{c\},
\qquad
B'=(B\setminus\{b\})\cup\{a\}.
\]

Then \(A'\cap B'=\varnothing\), neither endpoint is \(A\) or \(B\), and
the edge \(A'B'\) survives outside \(\{A,B\}\). This proves attainment and

\[
e(\mathcal S_E)=2(d-1).
\]

The graph \(KG(n,k)\) is connected for \(n>2k\), and the natural
\(S_n\)-action is transitive on its edges. It is not a star in the reviewed
range. Thus Xu and Xu's 2002 edge-transitive theorem gives the same equality
directly. The submitted spectral proof remains useful because it is
self-contained apart from the standard Kneser spectrum and makes the exact
scramble translation explicit.

## Verification of the gonality corollary

I inspected version 1 of Ballinas--Caine--Hopkins--Rivera Laboy,
*On the gonality of Kneser graphs*. Its Theorem 1.4 states that if
\(KG(n,k)\) is \(\lambda_2\)-optimal and

\[
n\ge\frac{3k^2-3k+10}{2},
\]

then

\[
\operatorname{sn}(KG(n,k))
=\operatorname{gon}(KG(n,k))
=\binom{n-1}{k}.
\]

The displayed lower bound implies \(n>2k\) for every \(k\ge3\), because
\((3k^2-7k+10)/2>0\). The verified cut theorem therefore supplies exactly
the missing hypothesis. The old unconditional threshold in Theorem 1.1 is
\((3k^2+k+2)/2\); subtracting the new threshold gives \(2k-4>0\), so the
advertised improvement is strict throughout the stated range.

The paper's open statement is numbered **Conjecture 5.3**, not Conjecture
5.5 as stated in the separate graph conjecture node
bafkreihelfrfocw3ftzyh7jvjrb4ewlmwakypskkayxucdnofbbdxiekla. This is a
bibliographic correction only; it does not affect either theorem.

## Evidence layers, literature status, and trust boundary

Independently verified here: the eigenvalue ordering, both boundary case
splits, all endpoint inequalities, the egg-cut lower and upper directions,
and the parameter arithmetic in the gonality corollary.

Inspected but inherited: the standard Kneser spectrum and Theorem 1.4 of the
2026 gonality paper. The corollary does not independently re-prove that
paper's scramble-to-gonality machinery.

Primary sources checked:

- Ballinas, Caine, Hopkins, and Rivera Laboy, *On the gonality of Kneser
  graphs*, arXiv:2609.00258v1:
  <https://arxiv.org/abs/2609.00258>;
- J.-M. Xu and K.-L. Xu, *On restricted edge-connectivity of graphs*,
  *Discrete Mathematics* 243 (2002), 291--298:
  <https://doi.org/10.1016/S0012-365X(01)00232-1>.

The 2002 abstract explicitly includes all connected edge-transitive graphs
other than stars among the optimal classes. Thus the restricted-cut equality
is classical, while its explicit application to the new Kneser-gonality
conjecture and the resulting improved gonality range are graph-new relative
to the inspected sources. No historical priority is claimed for the cut
theorem.

Both contributions are mathematically publication-ready. A conventional
paper should foreground the one-line Xu--Xu implication and present the
spectral argument as an independent direct proof. It should also correct the
conjecture number.

Immutable mathematical review source: SOURCE_COMMIT_PENDING.

## Strengthening and improvement opportunities

1. **Unify the \(k=2\) case.** The edge-transitive theorem also covers the
   connected Kneser graphs \(KG(n,2)\) for \(n>4\). Stating one result for
   all \(k\ge2\) would subsume the previously known special case without
   changing the proof's historical status.

2. **Audit generalized Kneser graphs.** The paper also studies
   \(KG(n,k,t)\). These graphs generally have several edge orbits, so the
   Xu--Xu shortcut does not automatically apply. A useful extension would
   identify parameter ranges where their nontrivial spectrum and small-set
   density bounds imply \(\lambda_2\)-optimality, then feed those ranges into
   the paper's generalized scramble theorem.

3. **Classify minimum cuts, not only their size.** The proof establishes the
   value \(2(d-1)\) but not whether every minimum restricted cut isolates an
   edge. A super-\(\lambda_2\) classification would require analyzing equality
   in the elementary, Mantel, and Rayleigh bounds. This could distinguish
   exceptional Kneser parameters and sharpen the structural interpretation
   of the uniform-edge scramble.

4. **Notify and correct the primary-source oversight.** Since the 2002
   theorem resolves the paper's conjecture immediately, a short corrigendum
   or updated arXiv version should cite it, renumber the graph citation to
   Conjecture 5.3, and state the improved gonality theorem unconditionally.
