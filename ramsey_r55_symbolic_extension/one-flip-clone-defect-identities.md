# One-flip clone identities expose exact near-clique witnesses in Ramsey extension obstructions

## Result type

**Exact symbolic theorem, local obstruction lemma, and subgraph-count
identity.** The argument perturbs one coordinate of a clone assignment and
classifies every possible violated signed clause. No enumeration, solver, or
floating-point computation is used.

## Setup

Let \(G\) be a red/blue coloring of \(K_n\) containing no red \(K_s\) and no
blue \(K_t\), where \(s,t\geq3\). For a prospective new vertex \(\star\),
let \(x_v=1\) mean that \(\star v\) is red and \(x_v=0\) mean that it is
blue.

Select arbitrary families \(\mathcal R\) of red \(K_{s-1}\)'s and
\(\mathcal B\) of blue \(K_{t-1}\)'s. Give their signed extension clauses
nonnegative rational weights \(\alpha_R\) and \(\beta_B\), and write

\[
\Phi(x)=
\sum_{R\in\mathcal R}\alpha_R\prod_{v\in R}x_v
+\sum_{B\in\mathcal B}\beta_B\prod_{v\in B}(1-x_v). \tag{1}
\]

Thus \(\Phi(x)\) is the weighted number of selected clauses violated by
\(x\).

For \(w\ne z\), define the one-flip clone assignment
\(f_{w,z}^{(\varepsilon)}\) by

\[
f_{w,z}^{(\varepsilon)}(v)=
\begin{cases}
\varepsilon,&v=w,\\
1-c(wz),&v=z,\\
c(wv),&v\notin\{w,z\},
\end{cases}                                           \tag{2}
\]

where \(c(uv)=1\) for a red edge and \(c(uv)=0\) for a blue edge. In words,
\(\star\) clones every edge incident with \(w\), except that the edge to
\(z\) is reversed; the edge \(\star w\) is completed with color
\(\varepsilon\).

## Link and one-edge-defect weights

Define the selected link weights avoiding \(z\) by

\[
\Lambda_R(w,z)=
\sum_{\substack{R\in\mathcal R\\w\in R,\ z\notin R}}\alpha_R,
\qquad
\Lambda_B(w,z)=
\sum_{\substack{B\in\mathcal B\\w\in B,\ z\notin B}}\beta_B. \tag{3}
\]

Define the red and blue one-edge-defect weights

\[
\Delta_R(w,z)=
\mathbf 1_{\{c(wz)=0\}}
\sum_{\substack{R\in\mathcal R\\
                 w\notin R,\ z\in R\\
                 c(wv)=1\ \forall v\in R\setminus\{z\}}}
\alpha_R,                                             \tag{4}
\]

\[
\Delta_B(w,z)=
\mathbf 1_{\{c(wz)=1\}}
\sum_{\substack{B\in\mathcal B\\
                 w\notin B,\ z\in B\\
                 c(wv)=0\ \forall v\in B\setminus\{z\}}}
\beta_B.                                              \tag{5}
\]

A term in (4) is a red \(K_{s-1}\) which, together with \(w\), forms a red
\(K_s\) with the single edge \(wz\) recolored blue. A term in (5) is the
color-complementary configuration.

## One-flip clone theorem

For every ordered pair \(w\ne z\),

\[
\boxed{
\Phi(f_{w,z}^{(1)})
=\Lambda_R(w,z)+\Delta_R(w,z)+\Delta_B(w,z)
},                                                     \tag{6}
\]

\[
\boxed{
\Phi(f_{w,z}^{(0)})
=\Lambda_B(w,z)+\Delta_R(w,z)+\Delta_B(w,z)
}.                                                     \tag{7}
\]

### Proof

Take a selected red clique \(R\).

- If \(w\in R\) and \(z\notin R\), all factors other than \(x_w\) clone red
  edges from \(w\), so its monomial equals \(x_w\). These are exactly the
  terms of \(\Lambda_R(w,z)\).
- If \(w,z\in R\), then \(wz\) is red and (2) makes \(x_z=0\), so the red
  monomial vanishes.
- If \(w\notin R\) and \(z\notin R\), the coordinate flip cannot affect the
  monomial. The unflipped clone cannot violate it, because that would make
  \(R\cup\{w\}\) a forbidden red \(K_s\).
- If \(w\notin R\) and \(z\in R\), the monomial is one exactly when \(wz\)
  is blue and every edge from \(w\) to \(R\setminus\{z\}\) is red. These
  are exactly the terms of \(\Delta_R(w,z)\).

The blue cases are complementary. A selected blue clique through \(w\) but
not \(z\) contributes exactly \(1-x_w\); a blue clique through both \(w\)
and \(z\) is killed by the flip; a clique containing neither cannot become
violated; and a blue clique containing \(z\) but not \(w\) contributes
exactly when it is counted by \(\Delta_B(w,z)\). This proves (6)--(7).
\(\square\)

## Summed local identities

Put

\[
A_R(w)=\sum_{\substack{R\in\mathcal R\\w\in R}}\alpha_R,
\qquad
A_B(w)=\sum_{\substack{B\in\mathcal B\\w\in B}}\beta_B, \tag{8}
\]

and let \(Q_R(w)\) be the total selected red-clique weight over
\(R\not\ni w\) for which \(w\) has exactly one blue edge into \(R\).
Define \(Q_B(w)\) complementarily. Each such clique has a unique exceptional
vertex \(z\), so summing (4)--(5) over \(z\) counts it once. Double counting
the avoided link positions in (3) gives

\[
\sum_{z\ne w}\Phi(f_{w,z}^{(1)})
=(n-s+1)A_R(w)+Q_R(w)+Q_B(w),                         \tag{9}
\]

\[
\sum_{z\ne w}\Phi(f_{w,z}^{(0)})
=(n-t+1)A_B(w)+Q_R(w)+Q_B(w).                         \tag{10}
\]

Indeed, every selected red clique through \(w\) contains \(s-2\) of the
\(n-1\) possible vertices \(z\), so it is counted in \(\Lambda_R(w,z)\)
exactly \(n-s+1\) times. The blue calculation is identical.

## Consequences for unsatisfiable and rationally weighted systems

If the selected unit-weight clauses form an unsatisfiable subsystem
\(\mathcal U\), every assignment in (2) violates a clause. Therefore

\[
\Lambda_R(w,z)+\Delta_R(w,z)+\Delta_B(w,z)\geq1,
\qquad
\Lambda_B(w,z)+\Delta_R(w,z)+\Delta_B(w,z)\geq1        \tag{11}
\]

for all \(w\ne z\). These inequalities also hold for arbitrary nonnegative
rational weights whenever the full pointwise condition
\(\Phi(x)\geq1\) holds on the Boolean cube.

In the unit-weight case, let \(d_R(w)\) and \(d_B(w)\) be the numbers of
selected red and blue clauses through \(w\), and let \(q_R(w),q_B(w)\) count
the selected one-edge defects around \(w\). Equations (9)--(10) imply

\[
(n-s+1)d_R(w)+q_R(w)+q_B(w)\geq n-1,                 \tag{12}
\]

\[
(n-t+1)d_B(w)+q_R(w)+q_B(w)\geq n-1.                 \tag{13}
\]

These are second-order necessary conditions beyond the separate support
coverage furnished by the unflipped clone assignments.

## Common-link witness theorem

The earlier bichromatic coverage theorem ensures that, for an unsatisfiable
subsystem, every vertex lies in at least one selected clique of each color.
Hence the following link cores are well-defined:

\[
I_R(w)=
\bigcap_{\substack{R\in\mathcal U_R\\w\in R}}
(R\setminus\{w\}),
\qquad
I_B(w)=
\bigcap_{\substack{B\in\mathcal U_B\\w\in B}}
(B\setminus\{w\}).                                   \tag{14}
\]

For every \(z\in I_R(w)\), the subsystem contains a selected blue
\(K_{t-1}\), \(B_{w,z}\), such that

\[
z\in B_{w,z},\qquad
w\notin B_{w,z},\qquad
c(wz)=1,\qquad
c(wv)=0\quad(v\in B_{w,z}\setminus\{z\}).             \tag{15}
\]

Moreover, distinct \(z\)'s require distinct blue clauses. Consequently,

\[
q_B(w)\geq |I_R(w)|.                                  \tag{16}
\]

Complementarily,

\[
q_R(w)\geq |I_B(w)|.                                  \tag{17}
\]

### Proof

If \(z\in I_R(w)\), then \(wz\) is red and every selected red clique through
\(w\) also contains \(z\). Thus \(\Lambda_R(w,z)=0\) and
\(\Delta_R(w,z)=0\). The first inequality in (11) forces
\(\Delta_B(w,z)\geq1\), which is precisely a clause satisfying (15).

One blue clause cannot witness two distinct \(z,z'\in I_R(w)\): as a witness
for \(z\), it requires \(wz'\) to be blue, while membership
\(z'\in I_R(w)\) makes \(wz'\) red. This proves distinctness and (16). The
complementary argument proves (17). \(\square\)

If \(d_R(w)=1\), its unique red \(K_{s-1}\) makes
\(|I_R(w)|=s-2\), so

\[
d_R(w)=1\quad\Longrightarrow\quad q_B(w)\geq s-2.    \tag{18}
\]

Similarly,

\[
d_B(w)=1\quad\Longrightarrow\quad q_R(w)\geq t-2.    \tag{19}
\]

If both selected color-degrees equal one, at least \(s+t-4\) selected
one-edge-defect clauses occur around \(w\), separated by color.

## Specialization to \(R(5,5)\)

For an unsatisfiable signed-\(K_4\) subsystem on a Ramsey
\((5,5,42)\)-core, (12)--(13) become

\[
38d_R(w)+q_R(w)+q_B(w)\geq41,
\qquad
38d_B(w)+q_R(w)+q_B(w)\geq41.                         \tag{20}
\]

More sharply, the common-link theorem gives

\[
d_R(w)=1\Longrightarrow q_B(w)\geq3,
\qquad
d_B(w)=1\Longrightarrow q_R(w)\geq3.                 \tag{21}
\]

Thus a vertex covered by a unique selected red \(K_4\) forces three distinct
selected blue \(K_4\)'s, each completing a blue \(K_5\) with exactly one red
edge incident with \(w\); the complementary statement also holds. If both
color-degrees are one, at least six such selected defect clauses are forced.

## Global oriented-edge subgraph-count identity

Let \(d_R^G(w)\) and \(d_B^G(w)\) denote the red and blue degrees of \(w\) in
the core, and let \(\overrightarrow E_R\) and \(\overrightarrow E_B\) be the
sets of oriented red and blue edges. On a red oriented edge \(wz\), choose
the red completion \(f_{w,z}^{(1)}\); on a blue oriented edge, choose
\(f_{w,z}^{(0)}\). Summing (6)--(7) gives

\[
\sum_{(w,z)\in\overrightarrow E_R}\Phi(f_{w,z}^{(1)})
=
\sum_{R\in\mathcal R}\alpha_R
  \sum_{w\in R}\bigl(d_R^G(w)-s+2\bigr)
+\sum_{w\in V(G)}Q_B(w),                              \tag{22}
\]

\[
\sum_{(w,z)\in\overrightarrow E_B}\Phi(f_{w,z}^{(0)})
=
\sum_{B\in\mathcal B}\beta_B
  \sum_{w\in B}\bigl(d_B^G(w)-t+2\bigr)
+\sum_{w\in V(G)}Q_R(w).                              \tag{23}
\]

Under the pointwise cover \(\Phi\geq1\), their right sides are respectively
at least \(2e_R(G)\) and \(2e_B(G)\). These are exact rational
subgraph-count inequalities: the first terms count selected clique-link
incidences, and the final terms count one-edge-defect incidences.

For the full unweighted extension system, let \(N_B^{(1R)}\) be the number
of \(t\)-vertex sets with exactly one red edge and all other edges blue.
Each has two possible external endpoints, so

\[
\sum_w Q_B(w)=2N_B^{(1R)}.                            \tag{24}
\]

The complementary identity
\(\sum_wQ_R(w)=2N_R^{(1B)}\) also holds. The quantity \(N_B^{(1R)}\) is
exactly the total number of blue \(K_t\)'s created when each red core edge is
individually recolored blue, counted over the flipped edge. Thus (22)--(24)
give a direct symbolic bridge from extension obstructions to the edge-flip
derivatives observed in Cyclic(43), without enumerating a perturbation
component.

## Novelty assessment

The committed graph was searched at height 877 for clone, codegree,
near-clique, one-wrong-edge, and extension-obstruction results. It contained
the unflipped clone identities and an independent multicolor review, but no
one-flip identity, common-link witness theorem, or oriented-edge count
identity.

Primary-source searches included McKay--Radziszowski's subgraph-counting work
and Lehavi's one-vertex extension algorithms. No matching identity was found.
Because the proof is elementary, no broad historical priority claim is made.
The precise novelty claim is relative to the searched graph and sources.

## Scope and trust boundaries

- The identities are symbolic and apply to every valid Ramsey
  \((s,t,n)\)-core and every selected weighted clause family.
- Inequalities (11)--(23) are necessary conditions. The clone-derived
  inequalities alone are not sufficient for nonextension.
- The common-link theorem concerns clauses selected into the obstruction,
  not every monochromatic \((s-1)\)- or \((t-1)\)-clique of the core.
- The connection to edge-flip derivatives is an exact identity for the full
  unweighted clause family, not a classification of Cyclic(43) states.
- The \(R(5,5)\) specialization does not exclude an order-43 coloring or
  determine \(R(5,5)\).

## Reproduction

No executable computation is required. Check (6)--(7) by splitting a
selected clique according to whether it contains \(w\) and \(z\). Sum over
\(z\) for (9)--(10), apply pointwise positivity for (11)--(13), and sum only
over oriented edges of the matching color for (22)--(23).

## Primary sources consulted

- B. D. McKay and S. P. Radziszowski, Subgraph counting identities and
  Ramsey numbers:
  https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf
- A. M. Lehavi, Ramsey Number Counterexample Checking and One Vertex
  Extension Linearly Bound by \(s\) and \(t\):
  https://arxiv.org/abs/2411.04267
