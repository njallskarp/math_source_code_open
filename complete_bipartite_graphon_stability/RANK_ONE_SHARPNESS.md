# Sharp fourth-root forcing scale for complete bipartite densities

## Status and theorem

This note closes the exponent question left by the explicit cut-norm modulus in
`README.md`.  The spanning-subgraph expansion used below is standard; the
result is recorded as a sharpness companion to that modulus, with no historical
priority claim.

Fix integers `s,t>=2` and `p` with `0<p<1`.  Let
`f:[0,1]->R` be bounded, nonzero, and mean zero.  Write

\[
 M=\|f\|_\infty,\qquad m_k=\int_0^1 f(x)^k\,dx,
\]

and, for

\[
 |\varepsilon|M^2\leq\min\{p,1-p\},
\]

define the graphon

\[
 W_\varepsilon(x,y)=p+\varepsilon f(x)f(y).
\]

Then `W_epsilon` has edge density `p` and is `p`-regular.  As
`epsilon` tends to zero,

\[
\boxed{
 t(K_{s,t},W_\varepsilon)-p^{st}
 =\binom{s}{2}\binom{t}{2}p^{st-4}m_2^4\varepsilon^4
  +O(\varepsilon^6). }
\tag{1}
\]

There is no fifth-order term.  Moreover, for the standard graphon cut norm,

\[
\boxed{
 \|W_\varepsilon-p\|_\square
 =\frac{|\varepsilon|}{4}\left(\int_0^1|f|\right)^2. }
\tag{2}
\]

Consequently, if

\[
 \delta_\varepsilon=t(K_{s,t},W_\varepsilon)-p^{st},
\]

then

\[
 \lim_{\varepsilon\to0,\ \varepsilon\ne0}
 \frac{\|W_\varepsilon-p\|_\square}{\delta_\varepsilon^{1/4}}
 =
 \frac{\|f\|_1^2}
 {4\binom{s}{2}^{1/4}\binom{t}{2}^{1/4}
  p^{(st-4)/4}m_2}>0.                                      \tag{3}
\]

Thus the `O(delta^(1/4))` exponent in the previously proved uniform modulus is
optimal at every fixed `p` and for every `K_(s,t)`: no estimate
`||W-p||_square <= C delta^gamma`, locally uniform over graphons of edge
density `p`, can hold with `gamma>1/4`.

## Exact expansion

The edge density and degree statements follow immediately from `integral f=0`:

\[
 \int W_\varepsilon=p,
 \qquad
 \int_0^1W_\varepsilon(x,y)\,dy=p
 \quad\hbox{for almost every }x.                         \tag{4}
\]

For any finite simple graph `H`, expand one factor
`p+epsilon f(x_u)f(x_v)` at every edge and use Fubini.  If
`J` ranges over the edge-subgraphs of `H`, then the exact finite polynomial is

\[
 t(H,W_\varepsilon)
 =\sum_{J\subseteq E(H)}
 p^{|E(H)|-|J|}\varepsilon^{|J|}
 \prod_{v\in V(H)}m_{d_J(v)},                             \tag{5}
\]

where `m_0=1`.  Since `m_1=0`, an edge set contributes only if its
non-isolated vertices all have degree at least two.

Take `H=K_(s,t)`.  Every nonempty bipartite simple graph with at most three
edges has a degree-one vertex.  With four edges, the only possibility having
minimum positive degree at least two is a four-cycle.  There are exactly
`binom(s,2)binom(t,2)` such edge sets, and each contributes
`p^(st-4) epsilon^4 m_2^4`.

There is no contributing five-edge set.  Indeed, a leafless bipartite graph
with five edges contains a cycle.  It cannot contain a cycle of length at
least six, while a four-cycle already contains all four possible edges between
its two vertices in each part.  A fifth simple edge either introduces a new
vertex of degree one or is impossible.  This proves (1), including the absent
fifth-order coefficient.

The error can be made explicit.  Each coefficient attached to a `k`-edge set
has absolute value at most `M^(2k)`.  Hence, when `st>=6` and
`|epsilon|M^2<=p`, the remainder `R_epsilon` in (1) satisfies

\[
 |R_\varepsilon|
 \leq
 2^{st}p^{st-6}M^{12}|\varepsilon|^6.                    \tag{6}
\]

For `s=t=2`, the polynomial has degree four and the remainder is identically
zero.

## Exact cut norm

Put `F_epsilon=W_epsilon-p`.  For measurable `S,T` one has

\[
 \int_{S\times T}F_\varepsilon
 =\varepsilon\left(\int_Sf\right)\left(\int_Tf\right).
\]

Since `integral f=0`,

\[
 \sup_S\left|\int_Sf\right|
 =\int f_+=\int f_- =\frac12\int|f|.
\]

Taking `S` and `T` to be positive or negative level sets gives equality, and
(2) follows.  Because `f` is nonzero, `m_2>0` and `||f||_1>0`; combining
(1) and (2) proves (3).  If an exponent `gamma>1/4` were valid, the ratio of
the two sides along this family would grow like
`|epsilon|^(1-4 gamma)`, a contradiction.

## Concrete two-step witness

One may take `f=-2` on a set of measure `1/3` and `f=1` on its complement.
Then `m_2=2`, `||f||_1=4/3`, and any

\[
 |\varepsilon|\leq\frac14\min\{p,1-p\}
\]

gives a valid two-step graphon.  This asymmetric choice also has
`m_3=-2`, so the vanishing fifth-order coefficient is not an artifact of an
odd-moment-free perturbation.

## Literature boundary

Lovasz's signed-graphon treatment of the local Sidorenko conjecture already
uses the exact expansion over spanning subgraphs, so (5) is prior methodology:

- L. Lovasz, *Subgraph densities in signed graphons and the local Sidorenko
  conjecture*, 2010, <https://arxiv.org/abs/1004.3026>.

Complete-bipartite forcing itself is also classical:

- J. Skokan and L. Thoma, *Bipartite subgraphs and quasi-randomness*, Graphs
  and Combinatorics 20 (2004), 255--262,
  <https://digitalcommons.uri.edu/math_facpubs/249/>.

Zhao's 2026 quantitative near-equality theorem gives entropy or `L^2` control
of the degree function for broad Sidorenko classes.  The perturbations here
are exactly regular by (4), so that result does not control their cut norm:

- Y. Zhao, *Tensor Amplification and Spectral Transfer for Sidorenko-Type
  Inequalities*, 2026, <https://arxiv.org/abs/2607.02260>.

Targeted searches through 2026-09-03 did not locate the explicit coefficient
in (1) paired with (2) as a matching sharpness result for the fourth-root
complete-bipartite forcing modulus.  The claim is therefore limited to closing
the exponent question for the preceding result, without a broader novelty or
priority assertion.

## Exact finite validation

`verify_rank_one_sharpness.py` performs a definition-level calculation on the
asymmetric two-step witness above.  It enumerates all assignments of the
vertices of `K_(s,t)` to the two atoms, multiplies the resulting linear edge
polynomials with exact `Fraction` arithmetic, and checks the coefficients
through order five for every `2<=s,t<=5`.  It also enumerates all pairs of
atom subsets to compute the cut norm directly.  This is independent of the
leafless-subgraph classification used in the proof.

```text
python3 verify_rank_one_sharpness.py --max-part 5
python3 -m unittest -v test_rank_one_sharpness.py
```

The checker validates normalization and the coefficient calculation.  The
universal theorem rests on the analytic proof above, not on finite testing.

The recorded CPython 3.12.12 run returned

```text
p=2/5
values=-2,1
weights=1/3,2/3
max_part=5
oriented_polynomials=16
record_sha256=7e659afcaf886590db953d27c22d4a7ea1eff31924d307cc0cf6ca47c2ad051d
status=PASS
```
