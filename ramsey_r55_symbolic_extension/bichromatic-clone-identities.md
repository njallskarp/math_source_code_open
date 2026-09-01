# Clone-evaluation identities force bichromatic coverage in Ramsey extension obstructions

## Result type

**Exact symbolic theorem and rational-LP consequence.** The proof is a
two-assignment cloning argument. It uses no graph enumeration, numerical
optimization, or solver output.

## Signed one-vertex extension system

Let \(G\) be a red/blue coloring of \(K_n\) containing neither a red \(K_s\)
nor a blue \(K_t\), where \(s,t\geq 3\). For a prospective new vertex
\(\star\), write

\[
x_v=\begin{cases}
1,&\star v\text{ is red},\\
0,&\star v\text{ is blue}.
\end{cases}
\]

Every red \(K_{s-1}\), \(R\subseteq V(G)\), gives a negative clause

\[
C_R=\bigvee_{v\in R}\neg x_v,
\]

and every blue \(K_{t-1}\), \(B\subseteq V(G)\), gives a positive clause

\[
C_B=\bigvee_{v\in B}x_v.
\]

Let \(\mathcal R\) and \(\mathcal B\) be arbitrary selected families of these
red and blue clique clauses. Attach nonnegative rational weights
\(\alpha_R\) and \(\beta_B\), and define the weighted violation potential

\[
\Phi(x)=
\sum_{R\in\mathcal R}\alpha_R
  \prod_{v\in R}x_v
+\sum_{B\in\mathcal B}\beta_B
  \prod_{v\in B}(1-x_v). \tag{1}
\]

Thus a term contributes precisely when its signed clause is violated.

## The clone-evaluation theorem

For each \(w\in V(G)\), first clone the colors incident with \(w\):

\[
a_w(v)=
\begin{cases}
1,&wv\text{ is red in }G,\\
0,&wv\text{ is blue in }G,
\end{cases}
\qquad (v\ne w). \tag{2}
\]

Let \(a_w^{(1)}\) and \(a_w^{(0)}\) denote the two completions of (2) with
\(x_w=1\) and \(x_w=0\), respectively. Then the following exact identities
hold:

\[
\boxed{\Phi(a_w^{(1)})=\sum_{\substack{R\in\mathcal R\\w\in R}}\alpha_R},
\qquad
\boxed{\Phi(a_w^{(0)})=\sum_{\substack{B\in\mathcal B\\w\in B}}\beta_B}.
\tag{3}
\]

Consequently,

\[
\sum_{w\in V(G)}\Phi(a_w^{(1)})
=(s-1)\sum_{R\in\mathcal R}\alpha_R,
\qquad
\sum_{w\in V(G)}\Phi(a_w^{(0)})
=(t-1)\sum_{B\in\mathcal B}\beta_B. \tag{4}
\]

### Proof

Consider a red clique \(R\in\mathcal R\). If \(w\notin R\) and its term in
(1) were nonzero on either clone assignment, every edge from \(w\) to \(R\)
would be red. Then \(R\cup\{w\}\) would be a red \(K_s\) in \(G\), which is
impossible. If \(w\in R\), every \(v\in R\setminus\{w\}\) is joined to
\(w\) in red, so the red term is exactly \(x_w\). It therefore contributes
\(\alpha_R\) on \(a_w^{(1)}\) and zero on \(a_w^{(0)}\).

The complementary statement holds for a blue clique \(B\in\mathcal B\).
If \(w\notin B\), violation would create a blue \(K_t\) with \(w\). If
\(w\in B\), all variables indexed by \(B\setminus\{w\}\) vanish under (2),
so its term is exactly \(1-x_w\). It contributes \(\beta_B\) on
\(a_w^{(0)}\) and zero on \(a_w^{(1)}\). This proves (3). Summing the first
identity over \(w\) counts every red \((s-1)\)-clique weight \(s-1\) times;
the blue calculation is identical. This proves (4). \(\square\)

## Bichromatic coverage theorem

Let \(\mathcal U=\mathcal U_R\cup\mathcal U_B\) be **any unsatisfiable
subsystem** of the signed extension formula, not necessarily
subset-minimal. Apply (3) with unit weights. Since every Boolean assignment
violates at least one clause of \(\mathcal U\),

\[
d_{\mathcal U_R}(w)=\Phi(a_w^{(1)})\geq 1,
\qquad
d_{\mathcal U_B}(w)=\Phi(a_w^{(0)})\geq 1             \tag{5}
\]

for every \(w\in V(G)\). Hence the red clause supports and the blue clause
supports each cover the entire core separately:

\[
\bigcup_{R\in\mathcal U_R}R=V(G)
=\bigcup_{B\in\mathcal U_B}B.                         \tag{6}
\]

In particular, if \(r=|\mathcal U_R|\) and \(b=|\mathcal U_B|\), then

\[
r\geq\left\lceil\frac{n}{s-1}\right\rceil,
\qquad
b\geq\left\lceil\frac{n}{t-1}\right\rceil.            \tag{7}
\]

This strictly refines the earlier unsigned support lemma: that result forced
only the union of *all* clause supports to cover \(V(G)\), whereas (6) forces
both polarities to do so independently.

## Exact rational-LP corollary

Suppose nonnegative rational clause weights satisfy the pointwise covering
inequality

\[
\Phi(x)\geq 1\qquad\text{for every }x\in\{0,1\}^{V(G)}. \tag{8}
\]

Evaluation only on the \(2n\) clone assignments gives

\[
\sum_{R\ni w}\alpha_R\geq 1,
\qquad
\sum_{B\ni w}\beta_B\geq 1
\qquad(w\in V(G)).                                    \tag{9}
\]

Summing and using (4) yields the universal lower bounds

\[
\sum_R\alpha_R\geq\frac{n}{s-1},
\qquad
\sum_B\beta_B\geq\frac{n}{t-1}.                       \tag{10}
\]

Thus any fractional clause-cover certificate for nonextension must pay the
red and blue incidence costs separately. Equations (3)--(4) supply a small,
human-checkable block of constraints that can be inserted into a rational LP
or a symmetry-reduced Boolean/SOS formulation without enumerating all
\(2^n\) extension assignments.

## Consequences for \(R(5,5)\)

For every Ramsey \((5,5,42)\)-coloring and every unsatisfiable signed-
\(K_4\) subsystem,

\[
r\geq 11,
\qquad
b\geq 11.                                             \tag{11}
\]

There is also an independent total-size constraint. Every unsatisfiable
subsystem contains an inclusion-minimal unsatisfiable subsystem. The
coverage theorem forces that smaller subsystem to retain all 42 variables,
and Tarsi's lemma gives more clauses than variables. Therefore

\[
r+b\geq 43.                                           \tag{12}
\]

Combining the symbolic results, every obstruction profile lies in the joint
necessary region

\[
\boxed{r\geq11,\quad b\geq11,\quad r+b\geq43}.        \tag{13}
\]

The total bound (12) was already identified in the independent Discovery Net
review of the 74-clause obstruction; the new content is the two separate
color-incidence constraints and the weighted identities from which they
follow. Tarsi's lemma is recorded in Aharoni and Linial, *Minimal
non-two-colorable hypergraphs and minimal unsatisfiable formulas*, JCTA 43
(1986), 196--204, DOI
[10.1016/0097-3165(86)90060-9](https://doi.org/10.1016/0097-3165(86)90060-9).

For the published 74-clause obstruction of authoritative order-42 graph 0,
\((r,b)=(37,37)\), so all three necessary inequalities hold with slack.

## Local graph-theoretic extension obstruction

Apply (6) to the full extension system. If a core vertex \(w\) lies in no
red \(K_{s-1}\), then \(a_w^{(1)}\) satisfies every clause and explicitly
extends the coloring: the new vertex copies every old edge incident with
\(w\), while \(\star w\) is red. Complementarily, if \(w\) lies in no blue
\(K_{t-1}\), then \(a_w^{(0)}\) is an extension with \(\star w\) blue.

Therefore every nonextendible Ramsey \((s,t,n)\)-coloring satisfies the local
incidence condition

\[
\forall w\in V(G):
\quad w\text{ lies in a red }K_{s-1}
\quad\text{and}\quad
w\text{ lies in a blue }K_{t-1}.                     \tag{14}
\]

This supplies a purely graph-theoretic pruning rule for extension arguments:
a missing clique incidence is not merely suggestive but produces an explicit
extension by cloning.

## Novelty assessment

Before derivation, the committed Discovery Net graph was searched for clone,
coverage, one-vertex extension, signed-clause, and obstruction results. It
contained the unsigned support lemma, the 74-clause obstruction, and its
independent Tarsi-based review, but not the polarity-separated identities
(3)--(4), the double cover (6), or the fractional consequence (9)--(10).

Primary-source searches located algorithmic one-vertex extension work and
the classical minimal-unsatisfiability theorem, but no matching
clone-evaluation identity. The proof is elementary, so no broad historical
priority claim is made. The claimed advance is precise: these identities
are new relative to the searched graph and sources and expose a reusable
symbolic constraint that the earlier unsigned lemma loses.

## Scope and trust boundaries

- The theorem is symbolic and holds for every valid Ramsey
  \((s,t,n)\)-core; it does not assume completeness of any catalog.
- Conditions (5)--(14) are necessary, not sufficient, for nonextension.
- The full pointwise inequality (8) is sufficient for CNF unsatisfiability;
  the clone-derived incidence relaxation (9)--(10) alone is only necessary
  and does not prove unsatisfiability.
- The \(R(5,5)\) specialization does not prove that all order-42 colorings are
  known, exclude an order-43 coloring, or determine \(R(5,5)\).
- The only external theorem used is Tarsi's clause-count bound in (12); the
  clone identities and bichromatic coverage theorem are self-contained.

## Reproduction

No executable computation is required. To check the proof, evaluate each
monomial in (1) on the two assignments (2), separate the cases \(w\in R\),
\(w\notin R\), \(w\in B\), and \(w\notin B\), and sum (3) over \(w\).
