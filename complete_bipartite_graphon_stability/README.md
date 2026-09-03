# Quantitative Jensen deficits for complete bipartite Sidorenko densities

## Status

This note proves an exact graphon inequality.  The accompanying Python program
is an exact-rational finite check of the formulas; it is not part of the proof.

## The scalar inequality

Let `X` be a nonnegative random variable with finite `m`-th moment, let
`a = E[X]`, and let the integer `m >= 2`.  Then

\[
  \mathbb E X^m
  \ge a^m+(m-1)a^{m-2}\operatorname{Var}(X).                 \tag{1}
\]

If `a=0`, then `X=0` almost surely.  If `a>0`, put `y=x/a`.  The
pointwise tangent-remainder identity is

\[
\begin{aligned}
 x^m-a^m-ma^{m-1}(x-a)&-(m-1)a^{m-2}(x-a)^2\\
 &=a^m y\bigl(y^{m-1}-(m-1)y+(m-2)\bigr)\ge0.              \tag{2}
\end{aligned}
\]

The last inequality is the tangent-line inequality for the convex function
`y -> y^(m-1)` at `y=1`.  Taking expectations cancels the linear term and
proves (1).  The coefficient `m-1` is best possible among inequalities of
this form for arbitrary nonnegative random variables: for a variable supported
on `{0,b}` with mean one, the quotient

\[
  \frac{\mathbb E X^m-1}{\operatorname{Var}(X)}
  =1+b+\cdots+b^{m-2}
\]

tends to `m-1` as `b` decreases to one.  For `m>2`, equality in (1) with
positive mean forces `X` to be constant; for `m=2`, (1) is the variance
identity.

## Main theorem

Let `W:[0,1]^2 -> [0,1]` be a symmetric measurable graphon and let integers
`s,t >= 2`.  Define

\[
\begin{aligned}
 p&=\int_{[0,1]^2}W(x,y)\,dx\,dy,\\
 d(y)&=\int_0^1 W(x,y)\,dx,\\
 v&=\int_0^1(d(y)-p)^2\,dy,\\
 q_s(x_1,\ldots,x_s)&=\int_0^1\prod_{i=1}^sW(x_i,y)\,dy,\\
 \mu_s&=\int_{[0,1]^s}q_s=\int_0^1d(y)^s\,dy,\\
 V_s&=\int_{[0,1]^s}(q_s-\mu_s)^2.
\end{aligned}
\]

Put

\[
 A_s=p^s+(s-1)p^{s-2}v.
\]

For `p=0`, all displayed claims are immediate because `W=0` almost
everywhere.  For `p>0`, one has

\[
\boxed{
 t(K_{s,t},W)
 \ge A_s^t+(t-1)\mu_s^{t-2}V_s
 \ge p^{st}+t(s-1)p^{st-2}v+(t-1)\mu_s^{t-2}V_s .}       \tag{3}
\]

Interchanging `s` and `t` gives a second valid bound, so the maximum of the
two oriented right-hand sides is also a lower bound.

### Proof

Fubini's theorem and independence of the `t` vertices in the second part give
the exact identities

\[
  t(K_{s,t},W)=\int q_s^t,
  \qquad
  \mu_s=\int d^s.                                        \tag{4}
\]

Apply (1) first to `q_s` and then to `d`:

\[
  \int q_s^t\ge\mu_s^t+(t-1)\mu_s^{t-2}V_s,
  \qquad
  \mu_s\ge A_s.                                          \tag{5}
\]

Since all quantities are nonnegative, the first inequality of (3) follows.
Finally, `(a+b)^t >= a^t+t a^(t-1)b` for nonnegative `a,b` gives

\[
 A_s^t
 \ge p^{st}+t(s-1)p^{st-2}v,
\]

which proves the second inequality.

### Equality

Equality in the Sidorenko term of (3),
`t(K_(s,t),W)=p^(st)`, holds if and only if `W=p` almost everywhere.
The forward direction for `p>0` follows from (3): first `v=0`, hence
`d=p` and `mu_s=p^s`, and then `V_s=0`, hence `q_s=p^s` almost everywhere.
Integrating out `x_3,...,x_s` (with no integration needed when `s=2`) gives

\[
 q_2(x,z)=\int_0^1W(x,y)W(z,y)\,dy=p^2
\]

almost everywhere.  For `F=W-p`, the associated self-adjoint Hilbert--Schmidt
operator therefore satisfies `T_F^2=0`; consequently `T_F=0` and `F=0` in
`L^2`.  The reverse direction is immediate.  This also recovers the forcing
property of every `K_(s,t)` with `s,t>=2`.

## Explicit cut-norm stability for `K_(2,t)`

Let `t>=2`, `p>0`, and

\[
  \delta=t(K_{2,t},W)-p^{2t}.
\]

Specializing (3), with `mu_2=p^2+v`, gives

\[
 v\le \frac{\delta}{t p^{2t-2}},
 \qquad
 V_2\le\frac{\delta}{(t-1)p^{2t-4}}.                     \tag{6}
\]

Moreover,

\[
\boxed{
 \|W-p\|_\square
 \le
 \left[
   \sqrt{\frac{\delta}{(t-1)p^{2t-4}}}
   +\sqrt{\frac{2\delta}{t p^{2t-4}}}
   +\frac{\delta}{t p^{2t-2}}
 \right]^{1/2}.}                                         \tag{7}
\]

To prove (7), put `F=W-p`, `a(x)=d(x)-p`, and let `r` be the kernel of
`T_F^2`.  Expanding the codegree gives

\[
 q_2(x,z)-\mu_2=p(a(x)+a(z))+r(x,z)-v.
\]

Thus

\[
 \|r\|_2\le\sqrt{V_2}+p\sqrt{2v}+v.                     \tag{8}
\]

Since `T_F` is self-adjoint,

\[
 \|F\|_\square\le\|T_F\|_{2\to2}
 \le\|T_F^2\|_{HS}^{1/2}=\|r\|_2^{1/2}.                 \tag{9}
\]

Substitution of (6) into (8)--(9) proves (7).  In particular, at each fixed
positive edge density, a `K_(2,t)` Sidorenko deficit tending to zero forces
cut-norm convergence to the constant graphon, with an explicit
`O(delta^(1/4))` modulus.

## Cut-norm stability for every `K_(s,t)`

The preceding modulus extends to all `s,t>=2`.  For `p>0`, put

\[
 \delta=t(K_{s,t},W)-p^{st},\qquad
 \alpha=\frac{\delta}{t(s-1)p^{st-2}},\qquad
 \beta=\frac{\delta}{(t-1)p^{s(t-2)}}.                  \tag{10}
\]

Then

\[
\boxed{
 \|W-p\|_\square
 \le\left\{
 p^{2-s}\left[
   \sqrt\beta+(s-2)\sqrt\alpha+\frac{s(s-1)}2\alpha
 \right]
 +p\sqrt{2\alpha}
 \right\}^{1/2}.}                                      \tag{11}
\]

The same formula with `s,t` interchanged is valid, so their minimum gives the
better orientation.  Formula (7) is exactly the specialization `s=2`.

To prove (11), (3) first gives `v<=alpha` and `V_s<=beta`.  Let

\[
 H_s(x_1,x_2)=
 \int(q_s-\mu_s)\,dx_3\cdots dx_s.
\]

Conditional-expectation contraction gives `||H_s||_2<=sqrt(V_s)`, while

\[
 H_s(x,z)=
 \int W(x,y)W(z,y)d(y)^{s-2}\,dy-\mu_s.                \tag{12}
\]

Because `u -> u^(s-2)` is `(s-2)`-Lipschitz on `[0,1]` (with zero
difference when `s=2`), and because the second derivative of `u -> u^s` is
at most `s(s-1)`,

\[
\begin{aligned}
 \left\|\int WW\bigl(d^{s-2}-p^{s-2}\bigr)\right\|_2
   &\le(s-2)\sqrt v,\\
 0\le\mu_s-p^s&\le\frac{s(s-1)}2v.
\end{aligned}                                           \tag{13}
\]

Writing `q_2(x,z)=integral W(x,y)W(z,y) dy`, equations (12)--(13) yield

\[
 \|q_2-p^2\|_2
 \le p^{2-s}\left[
   \sqrt{V_s}+(s-2)\sqrt v+\frac{s(s-1)}2v
 \right].                                               \tag{14}
\]

Finally, the kernel `r` of `T_(W-p)^2` is
`r=q_2-p^2-p(a(x)+a(z))`, where `a=d-p`, so

\[
 \|r\|_2\le\|q_2-p^2\|_2+p\sqrt{2v}.
\]

The operator-to-cut estimate (9), followed by `v<=alpha` and
`V_s<=beta`, proves (11).  This estimate is uniform over graphons at each
fixed `p>0`; its explicit powers also record the loss as `p` approaches zero.

## Literature boundary

The qualitative complete-bipartite Sidorenko inequality is classical; it is
among the cases treated by Sidorenko's correlation inequality:

- A. F. Sidorenko, *A correlation inequality for bipartite graphs*, Graphs and
  Combinatorics 9 (1993), 201--204,
  <https://link.springer.com/article/10.1007/BF02988307>.

The qualitative forcing property of complete bipartite graphs is also prior
art:

- J. Skokan and L. Thoma, *Bipartite subgraphs and quasi-randomness*, Graphs
  and Combinatorics 20 (2004), 255--262,
  <https://digitalcommons.uri.edu/math_facpubs/249/>.

The targeted searches performed on 2026-09-02 also inspected modern analytic
Sidorenko work, including Li--Szegedy's Jensen-based logarithmic calculus
<https://arxiv.org/abs/1107.1153> and Zhao's recent quantitative
near-equality framework <https://arxiv.org/abs/2607.02260>.  They confirm that
complete bipartite graphs and their equality/forcing behavior are known.  They
did not locate the exact two-level variance bound (3), the best scalar
coefficient used in it, or the elementary explicit cut-norm modulus (7).
Those formulas are therefore described only as apparently new to the searched
sources, with no historical priority claim.

## Reproduction

The checker uses only the Python standard library and exact `Fraction`
arithmetic.

```text
python3 verify_finite_graphs.py --max-n 5 --max-part 4
python3 -m unittest -v test_verify_finite_graphs.py
```

It exhausts all labelled simple graphs through the requested order, checks
both orientations of (3), checks the linearized bound, and independently
compares the common-neighborhood formula with definition-level homomorphism
enumeration for all graphs through order four and `2<=s,t<=3`.  It also
checks, exactly, the conditional Fubini identity, conditional-expectation
contraction, degree-moment Taylor bound, and weighted-codegree Lipschitz bound
used in (11).

The recorded full run used CPython 3.12.12 and returned

```text
labelled_graphs=1099
oriented_inequalities=9891
record_sha256=2775efa3619834b9472b015414a15025131834512a2fddc1b2023874861a8b2d
status=PASS
```

## Sharpness companion

The fourth-root cut-norm exponent in (11) is optimal for every fixed
`0<p<1` and every `s,t>=2`.  The proof, exact asymptotic coefficient, and an
independent exact-rational checker are in `RANK_ONE_SHARPNESS.md`.  In brief,
the regular rank-one perturbations

\[
 W_\varepsilon=p+\varepsilon f\otimes f,
 \qquad \int f=0,
\]

satisfy

\[
 t(K_{s,t},W_\varepsilon)-p^{st}
 =\binom{s}{2}\binom{t}{2}p^{st-4}
   \left(\int f^2\right)^4\varepsilon^4+O(\varepsilon^6),
\]

while

\[
 \|W_\varepsilon-p\|_\square
 =|\varepsilon|\left(\int|f|\right)^2/4.
\]

Thus no locally uniform forcing modulus with exponent greater than `1/4` can
hold at fixed density.  The general spanning-subgraph expansion used in this
argument is prior methodology from Lovasz's local Sidorenko work; the companion
is scoped specifically as a sharpness result for (11).

## Sharp regular-local constant

`REGULAR_LOCAL_CONSTANT.md` strengthens the preceding companion from the
exponent to the asymptotically best constant.  For a `p`-regular graphon
`W=p+F` with `||F||_infinity<=rp`, put

\[
 e=st,\quad N=\binom{s}{2}\binom{t}{2},\quad
 B_e(r)=\sum_{k=6}^e\binom{e}{k}r^{k-4}.
\]

Then

\[
 \left|t(K_{s,t},W)-p^e-Np^{e-4}t(C_4,F)\right|
 \le B_e(r)p^{e-4}t(C_4,F),
\]

and regularity gives the sharp centered operator inequality

\[
 \|F\|_\square\le\frac14t(C_4,F)^{1/4}.
\]

It follows that the best local constant tends, as `r` decreases to zero, to

\[
 \frac1{4N^{1/4}p^{(st-4)/4}},
\]

with equality asymptotically along balanced rank-one two-step graphons.  The
exact finite-step checker is `verify_regular_local_constant.py`.

## Sharp unrestricted local constant

`NONREGULAR_LOCAL_CONSTANT.md` removes exact regularity without losing the
limiting constant.  For an arbitrary edge-density-`p` graphon `W=p+F`, set

\[
 a=T_F1,\qquad D(x,y)=a(x)+a(y),\qquad U=F-D.
\]

Then `U` is regular.  The new uniform colored-subgraph expansion separates
the positive quadratic degree contribution from the regular fourth-order
contribution:

\[
 t(K_{s,t},W)-p^{st}
 =\left[s\binom{t}{2}+t\binom{s}{2}\right]p^{st-2}\|a\|_2^2
 +\binom{s}{2}\binom{t}{2}p^{st-4}t(C_4,U)
 +o\!\left(\|a\|_2^2+t(C_4,U)\right)
\]

uniformly as `||W-p||_infinity` tends to zero.  An explicit error polynomial
and finite-radius forcing inequality are given in the note.  The rooted
signed-density estimate controlling terms with exactly one degree edge is the
main new analytic bridge.

Consequently the best constant over all nearby graphons of edge density `p`
has the same limit as in the regular slice:

\[
 \lim_{r\downarrow0}\mathcal C^{\rm all}_{s,t,p}(r)
 =\frac1{4[\binom{s}{2}\binom{t}{2}]^{1/4}p^{(st-4)/4}}.
\]

The exact checker `verify_nonregular_local_constant.py` audits 1,278 general
finite-step instances and independently extracts 558 two-scale perturbation
polynomials through fourth order.

## Asymptotic extremizer classification

`ASYMPTOTIC_EXTREMIZERS.md` proves that equality and near equality in the
centered cut--fourth-Schatten inequality are rigid.  If a nonzero regular
symmetric kernel `K` satisfies

\[
 \|K\|_\square\geq(1-\varepsilon)t(C_4,K)^{1/4}/4,
\]

then, after fourth-Schatten normalization, its integral operator is within
`10 epsilon^(1/4)` in operator norm of a signed balanced rank-one two-block
kernel.  Equality holds only for those kernels, and the fourth-root stability
exponent is optimal by an orthogonal rank-one spectral-tail family.

Combining this rigidity with the unrestricted two-component expansion gives
the requested classification of all sequences attaining the limiting local
`K_(s,t)` forcing constant.  Their degree energy is `o(delta)`, their degree
kernel is `o(delta^(1/4))` in operator and cut norm, and their normalized
regular core converges in operator norm to a signed balanced rank-one kernel.
The exact checker `verify_extremizer_profiles.py` audits both the optimal
spectral-tail scale and the distinction between critical and negligible
degree modes.

## Finite-radius extremizer stability

`FINITE_RADIUS_EXTREMIZERS.md` turns the preceding sequential classification
into an explicit theorem at fixed locality radius.  If

\[
 \|W-p\|_\square/\delta^{1/4}
 \geq(1-\tau)
 \{4N^{1/4}p^{(st-4)/4}\}^{-1}
\]

and `||W-p||_infinity<=rp`, then, for fixed `s,t,p` and sufficiently small
`tau+r`, the degree energy is `O((tau+r)delta)`, the normalized degree
operator is `O(sqrt(r(tau+r)))`, and the full perturbation is within
`O((tau+r)^(1/4))` in operator norm of a balanced signed rank-one model.  The
note gives completely explicit constants and side conditions.  An orthogonal
spectral-tail family shows that the final fourth-root exponent is optimal.

`verify_finite_radius_extremizers.py` validates the radical envelopes through
exact rational interval endpoints and independently checks direct finite-step
`K_(s,t)` profiles without floating point.

## Reproducing the complete suite

The proof notes are the mathematical source of the universal statements.  The
programs are deterministic exact-arithmetic audits of the finite identities,
coefficient extractions, extremal profiles, and radical envelopes used by the
proofs; finite computation is not substituted for any graphon limit argument.

From the repository root, using CPython 3.12.12 (standard library only), run:

```text
cd complete_bipartite_graphon_stability
python3 verify_finite_graphs.py --max-n 5 --max-part 4
python3 verify_rank_one_sharpness.py --max-part 5
python3 verify_regular_local_constant.py --max-atoms 4 --max-part 4
python3 verify_nonregular_local_constant.py --max-atoms 4 --max-part 4
python3 verify_extremizer_profiles.py
python3 verify_finite_radius_extremizers.py
python3 -m unittest discover -p 'test_*.py' -v
shasum -a 256 -c SHA256SUMS
```

The six canonical record digests, in the same order, are:

```text
2775efa3619834b9472b015414a15025131834512a2fddc1b2023874861a8b2d
7e659afcaf886590db953d27c22d4a7ea1eff31924d307cc0cf6ca47c2ad051d
7ca615830544c83598d562083561ecdb3850e1f419cb0f738c2e98506bd6d861
f83875da4a0266200659f917a250d93a69d50fcdaa60633f61b7602ca0c6c981
ec9d3acdb9d2c84f09db38987c55cc7d1ab20eb53a60e39ec3114b025dc12e10
29dd73a1a31c287a33bc393c9c8cd3be2fab0f622b3a961aa24360ab15e4fc08
```

The unit-test command runs 40 tests.  Every verifier terminates with
`status=PASS`.  `SHA256SUMS` authenticates the curated source snapshot but is
not a proof certificate.  The analytic proofs also use the explicitly cited
prior graphon results in their literature and trust-boundary sections.

## Discovery Net provenance

This directory supports the complete-bipartite sequence committed at heights
1438, 1449, 1457, 1481, 1505, 1521, and 1545.  Their artifact references are,
respectively:

```text
bafkreiaup4htkgrnxthic2i4c3dn7qoxgxeyyyf2jrhx3fk7vzfjjnwfkm
bafkreifvxdcjzqtr6houfh2eiak3pl6fdmmippxbfj3ms2wzc4a4nxdpde
bafkreifelydmyzmf7qvdidhr36afankf6w3vqlgoj3gnjpckeywhiwjd3i
bafkreifyr6la4nbbvy6zjrk3j3c24binajnvtzgkdzol5qzxnkunmv3m5q
bafkreig6uwsexevsatxxo2iyo6jugj24ljkj4entpegcynwccpptv6hdum
bafkreiarfornxcaydnajmrv7u27ngyx2gsb3rinybdufekqjycgpp6da2a
bafkreiach44w2guofifgcsczvwjosgga47qerk3vxfokvkjyqopwrgygru
```
