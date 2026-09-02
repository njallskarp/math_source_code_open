# Local-character image obstruction for the QLP-42 middle branches

## Theorem

For one ordered phase pair \((x,y)\in\mu_4^2\), define

\[
S=\frac{x-y}{1+i},
\qquad
H=\frac{x+y}{1+i},
\qquad
\epsilon=-iS\overline H,
\]

and let \(\delta=|\epsilon|\). The sixteen local states split canonically
into:

- four opposite states with \(H=0\) and
  \(S\in\{\pm1\pm i\}\);
- four equal states with \(S=0\) and
  \(H\in\{\pm1\pm i\}\);
- eight quarter-turn states with \(S=u\in\mu_4\),
  \(\epsilon\in\{\pm1\}\), and \(H=-i\epsilon u\).

Let

\[
\Phi(U,V,P,Q,Z,W)
=\sum_{(x,y)\in\mu_4^2}
U^{\operatorname{Re}S}
V^{\operatorname{Im}S}
P^{\operatorname{Re}H}
Q^{\operatorname{Im}H}
Z^\delta W^\epsilon .
\]

For fixed exact sums \(s_X,h_X\), the support in \((q_X,\sigma_X)\) of the
coefficient of \(U^{\operatorname{Re}s_X}V^{\operatorname{Im}s_X}
P^{\operatorname{Re}h_X}Q^{\operatorname{Im}h_X}\) in \(\Phi^{21}\) is
exactly the set of pointwise \(16\)-state multisets with
\[
q_X=\sum_j\delta_X(j),
\qquad
\sigma_X=\sum_j\epsilon_X(j).
\]

Applying this character-image theorem to both families and the six canonical
exact-sum cases gives:

1. Every one of the \(36\) case/fiber points for \(q=5\) survives.
2. Exactly \(210\) of the \(228\) case/fiber points for \(q=37\) survive.
3. The following \(18\) points are impossible:

| case \(c\) | excluded \(\sigma\) |
|---:|:---|
| \(0\) | \(37\) |
| \(1\) | \(-37,35,37\) |
| \(2\) | \(-37,35,37\) |
| \(3\) | \(-37,-35,35,37\) |
| \(4\) | \(-37,-35,35,37\) |
| \(5\) | \(-37,35,37\) |

Each exclusion removes a complete affine cross-trace fiber point in its
case, simultaneously for every positional arrangement and every support
orbit. This is an aggregate local-state theorem, not a support or cell
census.

## Structural factorization

Let

\[
\mathcal U_n=
\left\{a+bi:\ |a|+|b|\le n,\quad
n-|a|-|b|\equiv0\pmod2\right\}
\]

be the sums of \(n\) fourth roots, and let

\[
\mathcal D_n=
\left\{a+bi:\ |a|,|b|\le n,\quad
a\equiv b\equiv n\pmod2\right\}
\]

be the sums of \(n\) diagonal elements from \(\{\pm1\pm i\}\).

If a family has \(q\) quarter cells, signed imbalance \(\sigma\), \(o\)
opposite cells, and \(e=21-q-o\) equal cells, set

\[
q_+=\frac{q+\sigma}{2},
\qquad
q_-=\frac{q-\sigma}{2}.
\]

Then its exact sums are attainable if and only if there exist
\(u_+\in\mathcal U_{q_+}\) and \(u_-\in\mathcal U_{q_-}\) such that

\[
s_X-u_+-u_-\in\mathcal D_o,
\]

\[
h_X+i u_+-i u_-\in\mathcal D_e.
\]

This reduces the sixteen-state coefficient problem to two planar lattice
walks and two independent diagonal boxes. The verifier constructs an
explicit sixteen-state count vector for every retained fiber from this
factorization.

## Five-cell diagonal budget

At \(q=37\), exactly five cells are nonquarter. For one family,

\[
S_X+iH_X=2U_{X,+}+R_{X,+},
\]

\[
S_X-iH_X=2U_{X,-}+R_{X,-},
\]

where \(U_{X,\pm}\) is a sum of the \(q_{X,\pm}\) quarter-cell fourth roots
and \(R_{X,\pm}\) is a sum of the family nonquarter diagonal elements.

For \(z=a+bi\), define \(\mu_k(z)\) as the least \(m\) for which

\[
z-2u\in\mathcal D_m
\]

for some \(u\in\mathcal U_k\). Distributing \(k\) oriented quarter cells
between the two families gives a sharp necessary diagonal budget. In every
one of the eighteen excluded fibers the required budget is at least seven,
exceeding the available five. At every retained \(q=37\) fiber both signed
budgets are at most five.

## Reproduction

Run with CPython \(3.12\) or later:

    ./verify.sh

The dependency-free verifier reconstructs all sixteen local states,
independently verifies the formulas for \(\mathcal U_n\) and
\(\mathcal D_n\) through \(n=21\), computes the factorized coefficient
support, constructs count-vector witnesses for every retained fiber, and
checks the five-cell budgets for every excluded fiber.

## Scope and trust boundary

This theorem uses only exact sums and the pointwise sixteen-state coupling.
It does not use autocorrelation beyond importing the branch and case data,
and it uses no Gram matrix, \((1+i)\)-adic layer, support word, support orbit
enumeration, residue cell, SAT result, floating point, randomness, or
timeout.

The result imports the canonical norm-\(32\) shell, the coupled transform,
the six exact-sum cases, and the primitive cross-trace interpretation of
\(\sigma\). The structural factorization is human-checkable; completeness
of the finite case classification trusts the published standard-library
checker, CPython interpreter, operating system, and hardware. The remaining
\(210\) aggregate fibers need not satisfy positional autocorrelation
constraints. QLP-42 remains unresolved.
