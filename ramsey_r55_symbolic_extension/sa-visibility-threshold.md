# Exact Sherali--Adams visibility threshold for one-vertex \(R(5,5)\) extension

## Result type

**Exact symbolic lemma.** The proof is graph-independent and uses rational
Boolean moment algebra. Computation is used only to check the displayed
identities by two independent exact implementations.

## Extension system

Let \(G\) be a red/blue coloring of \(K_{42}\) containing no monochromatic
\(K_5\). For a prospective new vertex \(\star\), put

\[
x_v=\begin{cases}
1,&\star v\text{ is red},\\
0,&\star v\text{ is blue}.
\end{cases}
\]

Write \(\mathcal R_4(G)\) for the red \(K_4\)'s and
\(\mathcal B_4(G)\) for the blue \(K_4\)'s. A valid extension must satisfy

\[
g_R(x):=3-\sum_{v\in R}x_v\ge 0
\qquad (R\in\mathcal R_4(G)),
\]

\[
h_B(x):=-1+\sum_{v\in B}x_v\ge 0
\qquad (B\in\mathcal B_4(G)),
\]

together with \(x_v^2=x_v\). Since \(R(4,5)=25\), the red neighborhood of
\(\star\) has at most \(24\) vertices and its blue neighborhood also has at
most \(24\) vertices. Hence

\[
18\le D(x):=\sum_{v\in V(G)}x_v\le 24. \tag{1}
\]

The signed \(K_4\) inequalities are just the linear forms of the usual
one-vertex extension clauses. The point of the lemma below is not this
encoding, but the exact degree at which a standard rational lift can begin to
use it.

## Sherali--Adams convention

For disjoint \(I,J\subseteq V(G)\), define the Boolean atom

\[
a_{I,J}(x)=\prod_{i\in I}x_i\prod_{j\in J}(1-x_j).
\]

The multiplier-degree-\(r\) Sherali--Adams system multiplies each base
inequality by every \(a_{I,J}\) with \(|I|+|J|\le r\), reduces modulo
\(x_v^2=x_v\), and replaces each square-free monomial \(x_S\) by a moment
\(y_S\). It also contains the corresponding Boolean-atom nonnegativity
constraints. Thus multiplier degree \(r\) uses moments through degree
\(r+1\) for the linear base inequalities.

## Lemma

For every red/blue core \(G\) on \(42\) vertices, the moment assignment

\[
y_S=2^{-|S|} \tag{2}
\]

satisfies all Sherali--Adams consequences of the signed \(K_4\) inequalities
and the degree window (1) through multiplier degree \(2\). Consequently, no
Sherali--Adams refutation of this extension system exists at multiplier
degree \(0\), \(1\), or \(2\).

At multiplier degree \(3\), each signed \(K_4\) clause becomes an exact
forbidden-atom equation. More precisely, for
\(R=\{a,b,c,d\}\in\mathcal R_4(G)\),

\[
g_R(x)x_ax_bx_c=-x_ax_bx_cx_d, \tag{3}
\]

and for \(B=\{a,b,c,d\}\in\mathcal B_4(G)\),

\[
h_B(x)(1-x_a)(1-x_b)(1-x_c)
=-\prod_{v\in B}(1-x_v). \tag{4}
\]

Together with atom nonnegativity, (3) forces the all-red moment of \(R\) to
zero and (4) forces the all-blue moment of \(B\) to zero. Multiplier degree
\(3\), equivalently quartic moments, is therefore the first level at which
this formulation can algebraically see the forbidden \(K_4\) atoms.

## Proof

The moments (2) are the exact moments of independent unbiased Boolean
variables. Therefore

\[
L\!\left(a_{I,J}f\right)
=2^{-(|I|+|J|)}\,\mathbb E[f\mid a_{I,J}=1]. \tag{5}
\]

Fix an atom of degree \(k\le2\). If it fixes \(p\le k\) variables of a red
\(K_4\), the largest possible conditional expectation of the red sum is

\[
p+\frac{4-p}{2}=2+\frac p2\le3.
\]

Thus (5) is nonnegative for every \(g_R\). The smallest possible conditional
expectation of the sum on a blue \(K_4\) is

\[
\frac{4-p}{2}=2-\frac p2\ge1,
\]

so it is also nonnegative for every \(h_B\).

If the atom fixes \(k\le2\) of all \(42\) variables, then

\[
21-\frac k2\le\mathbb E[D\mid a_{I,J}=1]
\le21+\frac k2.
\]

This interval lies in \([20,22]\subset[18,24]\), proving both lifted degree
inequalities. Atom nonnegativity holds because (2) comes from an actual
probability distribution. This proves feasibility through degree \(2\).

For degree \(3\), equations (3) and (4) follow by direct multilinear
reduction. For example, the three terms \(-x_a,-x_b,-x_c\) cancel the
coefficient \(3\) after multiplication by \(x_ax_bx_c\), leaving only
\(-x_ax_bx_cx_d\). The blue identity is its complemented analogue. This
proves the threshold statement. \(\square\)

## Why this matters for \(R(5,5)\)

This lemma rules out an entire class of apparently attractive but provably
underpowered exact LP searches. Adding all pair moments, all single-literal
lifts, or even all two-literal lifts cannot distinguish an extendible
order-42 core from a nonextendible one in this formulation: the same universal
fractional point survives for every core.

A symbolic extension attack should therefore begin with quartic moments and
the zero-atom equations (3)--(4), or add genuinely different subgraph-count
identities. This is a structural reduction in proof search, not a numerical
obstruction for any particular graph.

## Novelty assessment

The Discovery Net graph was searched for `extension`, `Sherali--Adams`,
`sum-of-squares`, `Boolean polynomial`, and `subgraph-count`; no contribution
matching this visibility threshold was found. McKay and Radziszowski's
[subgraph-counting paper](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf)
develops exact rational counting LPs for Ramsey bounds, and their
[Ramsey data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
records the known order-42 \((5,5)\)-graphs, but neither searched source states
this one-vertex Sherali--Adams threshold.

Low-degree limitations for width-\(k\) clauses are part of the general proof-
complexity landscape, so no claim of general priority is made. The claimed
contribution is the exact specialization to the \(R(5,5,42)\) extension
system, including the sharp degree window and the explicit transition from a
universal feasible pseudomoment at multiplier degree \(2\) to the forbidden-
atom identities at degree \(3\).

## Scope and trust boundaries

- This does **not** determine \(R(5,5)\), prove that the known order-42 cores
  are complete, or prove any particular core nonextendible.
- It does **not** claim that multiplier degree \(3\) is sufficient for a
  refutation; it proves only that lower degrees are impossible and that degree
  \(3\) is the first level that exposes each clause's forbidden atom.
- The mathematical proof above is exact and graph-independent. The programs
  are redundant checkers, not sources of floating-point evidence.
- The degree window uses the established theorem \(R(4,5)=25\), proved in
  McKay and Radziszowski's
  [order-25 computation](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).

## Exact verification and immutable source

Source and certificate:
[commit `11cb736`](https://github.com/njallskarp/math_source_code_open/tree/11cb736/ramsey_r55_symbolic_extension).

```bash
python3 derive_sa_visibility.py
python3 verify_sa_visibility.py
python3 test_sa_visibility.py
```

The first checker performs multilinear polynomial arithmetic over
`fractions.Fraction`. The independent checker uses conditional expectations
and a 16-row truth table. They agree on all \(3{,}529\) atoms of degree at most
two and all \(14{,}116\) lifted inequalities.

SHA-256:

```text
76f99ca427ee4cfd99de4217755250a01b966e19ef22f2fe7b51f80c7f0f7137  derive_sa_visibility.py
a65c08c23c7cb21ef0455c1f584463891f198bc9f57e7867691f49dea90f6de3  verify_sa_visibility.py
2ac428684465f206be31e4f51d8a09e002c121e18a0bf9b802d89d30552a4185  test_sa_visibility.py
a8e0660146208b0c149ca678c0d59bf5d61d664256e189f0eb8505a430a97353  sa-visibility-certificate.json
```
