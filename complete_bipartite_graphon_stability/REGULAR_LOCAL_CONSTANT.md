# The sharp regular-local constant for complete-bipartite forcing

## Theorem

Fix integers `s,t>=2` and `0<p<1`, and put

\[
 e=st,\qquad N=\binom{s}{2}\binom{t}{2},\qquad
 B_e(r)=\sum_{k=6}^{e}\binom{e}{k}r^{k-4},               \tag{1}
\]

where an empty sum is zero.  Let `W:[0,1]^2->[0,1]` be a symmetric
`p`-regular graphon, put `F=W-p`, and suppose

\[
 \|F\|_\infty\leq rp,\qquad 0\leq r\leq1.
\]

With

\[
 \delta=t(K_{s,t},W)-p^e,
\]

one has the relative fourth-order estimate

\[
\boxed{
 \left|\delta-Np^{e-4}t(C_4,F)\right|
 \leq B_e(r)p^{e-4}t(C_4,F)
 \leq 2^e r^2p^{e-4}t(C_4,F).}                          \tag{2}
\]

Every regular symmetric kernel also satisfies the sharp inequality

\[
\boxed{
 \|F\|_\square\leq\frac14t(C_4,F)^{1/4}.}              \tag{3}
\]

Consequently, whenever `B_e(r)<N`,

\[
\boxed{
 \|W-p\|_\square
 \leq
 \frac{\delta^{1/4}}
 {4\,[N-B_e(r)]^{1/4}p^{(e-4)/4}}.}                    \tag{4}
\]

The completely explicit sufficient range

\[
 0\leq r<\sqrt{N/2^e}
\]

ensures the denominator in (4) is positive.

The leading constant is optimal.  More precisely, let

\[
 \mathcal C_{s,t,p}(r)=
 \sup\frac{\|W-p\|_\square}
 {[t(K_{s,t},W)-p^e]^{1/4}},                             \tag{5}
\]

where the supremum is over nonconstant symmetric `p`-regular graphons with
`||W-p||_infinity<=rp`.  Then

\[
\boxed{
 \lim_{r\downarrow0}\mathcal C_{s,t,p}(r)
 =\frac1{4N^{1/4}p^{(e-4)/4}}.}                         \tag{6}
\]

Thus this theorem determines both the exponent and the asymptotically best
constant in the regular `L^infinity`-local slice.  For `s=t=2`, `B_4=0` and
the conclusion is exact without a locality assumption:

\[
 \|W-p\|_\square\leq\frac14
 [t(C_4,W)-p^4]^{1/4}
\]

for every `p`-regular graphon, with best constant `1/4`.

## Exact density expansion

The spanning-subgraph expansion gives

\[
 t(K_{s,t},p+F)=
 \sum_{J\subseteq E(K_{s,t})}p^{e-|J|}t(J,F).           \tag{7}
\]

If `J` has a vertex of degree one, integrating the corresponding variable
first gives `t(J,F)=0`, because `T_F 1=0`.  Thus every surviving nonempty
`J` has minimum positive degree at least two.  The only four-edge survivors
are the `N` copies of `C_4`, and no five-edge survivor exists.  Therefore

\[
 \delta=Np^{e-4}t(C_4,F)+R,                             \tag{8}
\]

where `R` is a sum over leafless edge-subgraphs having at least six edges.

Put `eta=||F||_infinity`.  The case `eta=0` is immediate, so suppose
`eta>0` and set `U=F/eta`.  Then `||U||_infinity=1`.  Every leafless simple
bipartite graph has at least two nonadjacent vertices of degree at least two:
each bipartition class has at least two vertices, and two vertices in one
class are nonadjacent.  Lovasz's signed-density domination and its absolute
form therefore give

\[
 |t(J,U)|\leq t(C_4,U).
\]

For `k=|E(J)|`, homogeneity yields

\[
 |t(J,F)|=\eta^k|t(J,U)|
 \leq\eta^{k-4}t(C_4,F).                                \tag{9}
\]

There are at most `binom(e,k)` edge sets of size `k`.  Since
`eta/p<=r`, equations (8)--(9) imply the first inequality in (2).  For
`0<=r<=1`, every `r^(k-4)` with `k>=6` is at most `r^2`, and summing all
binomial coefficients proves the second inequality.

## The sharp centered cut--Schatten inequality

Let `T_F` be the self-adjoint Hilbert--Schmidt operator with kernel `F`.  If
`a=lambda(S)` and `b=lambda(T)`, regularity gives

\[
 \int_{S\times T}F
 =\left\langle 1_S-a1,T_F(1_T-b1)\right\rangle.         \tag{10}
\]

The two centered indicators have `L^2` norms
`sqrt(a(1-a))` and `sqrt(b(1-b))`, each at most `1/2`.  Hence

\[
 \left|\int_{S\times T}F\right|
 \leq\frac14\|T_F\|_{2\mathbin{\to}2}
 \leq\frac14\|T_F\|_{S_4}
 =\frac14t(C_4,F)^{1/4}.                                \tag{11}
\]

Taking the supremum proves (3).  Combining the lower half of (2) with (3)
gives (4).

The factor `1/4` in (3) is best possible.  Let `f` be `1` on one half of the
unit interval and `-1` on the other half, and put `F_epsilon=epsilon f tensor
f`.  Then

\[
 \|F_\varepsilon\|_\square=|\varepsilon|/4,
 \qquad t(C_4,F_\varepsilon)=\varepsilon^4.             \tag{12}
\]

For `W_epsilon=p+F_epsilon`, the rank-one expansion proved in the companion
note gives

\[
 t(K_{s,t},W_\varepsilon)-p^e
 =Np^{e-4}\varepsilon^4+O(\varepsilon^6).               \tag{13}
\]

These graphons are admissible for all sufficiently small `epsilon`.  The
upper bound in (4) tends to the right side of (6), while (12)--(13) give the
matching lower limit.  This proves (6).

## Literature boundary

The ingredients from signed-graphon theory are prior art.  Lovasz records the
ordinary cut/`C_4` inequality, the absolute form of signed-density ordering,
the domination of a graph containing two nonadjacent degree-at-least-two
vertices by `C_4`, and the spanning-subgraph expansion used in local
Sidorenko arguments:

- L. Lovasz, *Subgraph densities in signed graphons and the local Sidorenko
  conjecture*, 2010, <https://arxiv.org/abs/1004.3026>.

The qualitative forcing property of complete bipartite graphs is classical:

- J. Skokan and L. Thoma, *Bipartite subgraphs and quasi-randomness*, Graphs
  and Combinatorics 20 (2004), 255--262,
  <https://digitalcommons.uri.edu/math_facpubs/249/>.

Targeted primary-source searches through 2026-09-03 did not locate (2)--(6),
in particular the sharp centered factor `1/4` combined with the explicit
complete-bipartite remainder and limiting best constant.  These formulas are
claimed only as an apparently new refinement of the preceding committed
modulus and sharpness companion; no historical-priority claim is made.

## Validation and trust boundary

`verify_regular_local_constant.py` constructs rational regular step kernels,
including higher-rank examples, by double-centering every labelled simple
graph through four vertices.  It scales each kernel at two exact local radii, computes
`K_(s,t)` densities from the common-neighborhood definition, computes
`t(C_4,F)` directly, and enumerates all atom-subset pairs for the cut norm.
Exact `Fraction` comparisons check (2), (3), and (4) for every requested
parameter pair.  This calculation is independent of the signed-density
subgraph domination used in the universal proof.

```text
python3 verify_regular_local_constant.py --max-atoms 4 --max-part 4
python3 -m unittest -v test_regular_local_constant.py
```

The exact checker audits normalization and constants.  It does not replace
the analytic proof of the universal theorem.

The recorded CPython 3.12.12 run returned

```text
p=2/5
radii=1/50,1/100
max_atoms=4
max_part=4
nonzero_regular_kernels=71
rank_greater_than_one=60
checked_instances=1278
record_sha256=7ca615830544c83598d562083561ecdb3850e1f419cb0f738c2e98506bd6d861
status=PASS
```
