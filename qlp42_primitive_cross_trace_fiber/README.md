# Primitive cross-trace fibers for the coupled QLP-42 transform

## Theorem

Let \(X\in\{A,B\}\), and let \(S_X,H_X\in\mathbb Z[i]^{21}\) be coupled
pointwise through the established \(16\)-state half-difference/half-sum map.
For every divisor \(d\mid21\), let \(\zeta_d\) be a primitive \(d\)-th root
of unity and define

\[
\Gamma_d(X)=
\sum_{\substack{1\le k\le d\\(k,d)=1}}
S_X(\zeta_d^k)\,\overline{H_X(\zeta_d^k)}.
\]

For a local state define

\[
\epsilon_X(j)=-iS_X(j)\overline{H_X(j)}.
\]

Then \(\epsilon_X(j)\in\{-1,0,1\}\), and it is nonzero precisely at a
quarter-turn cell. If \(q\) is the total number of quarter-turn cells and

\[
\sigma=\sum_{X\in\{A,B\}}\sum_{j=0}^{20}\epsilon_X(j),
\]

then

\[
\sum_{X\in\{A,B\}}
\left(\Gamma_1(X)+\Gamma_3(X)+\Gamma_7(X)+\Gamma_{21}(X)\right)
=21i\sigma,
\]

where

\[
\sigma\in\{-q,-q+2,\ldots,q-2,q\}.
\]

In canonical exact-sum case \(c\), the imported transform gives
\(H_A(1)=0\), \(H_B(1)=1\), and the following values of
\(\beta_c=S_B(1)\):

| case \(c\) | \(\beta_c\) |
|---:|---:|
| \(0\) | \(4-5i\) |
| \(1\) | \(4-3i\) |
| \(2\) | \(-5i\) |
| \(3\) | \(4-i\) |
| \(4\) | \(4+i\) |
| \(5\) | \(-3i\) |

Consequently

\[
\Gamma_3^{\mathrm{tot}}+
\Gamma_7^{\mathrm{tot}}+
\Gamma_{21}^{\mathrm{tot}}
=-\beta_c+21i\sigma.
\]

Thus all support orbits in a fixed pair \((q,c)\) share one finite affine
cross-trace fiber. It has \(6\) possible points when \(q=5\) and \(38\)
possible points when \(q=37\). The real part is \(0\) in cases \(2,5\) and
\(-4\) in cases \(0,1,3,4\); the imaginary part occupies one fixed residue
class modulo \(21\).

## Proof

For an ordered fourth-root pair \((x_j,y_j)\),

\[
S_j=\frac{x_j-y_j}{1+i},\qquad
H_j=\frac{x_j+y_j}{1+i}.
\]

Therefore

\[
S_j\overline{H_j}
=\frac{x_j\overline{y_j}-y_j\overline{x_j}}{2}
=i\,\operatorname{Im}(x_j\overline{y_j}).
\]

This proves the local claim about \(\epsilon_j\). It also proves the parity
and bound for \(\sigma\), because \(\sigma\) is a sum of exactly \(q\) signs
in \(\{-1,1\}\).

For arbitrary length-\(21\) Gaussian words \(S,H\), expansion through the
Ramanujan sum \(c_d\) gives

\[
\Gamma_d(S,H)=
\sum_{r,t=0}^{20}S_r\overline{H_t}\,c_d(r-t).
\]

Character orthogonality on \(C_{21}\) gives

\[
\sum_{d\mid21}c_d(m)
=\begin{cases}
21,&m\equiv0\pmod{21},\\
0,&m\not\equiv0\pmod{21}.
\end{cases}
\]

Summing the four cross-traces therefore leaves only diagonal terms:

\[
\Gamma_1+\Gamma_3+\Gamma_7+\Gamma_{21}
=21\sum_{j=0}^{20}S_j\overline{H_j}.
\]

Applying the local identity and summing over \(A,B\) proves the first
formula. Finally,
\(\Gamma_1(A)=S_A(1)\overline{H_A(1)}=0\) and
\(\Gamma_1(B)=S_B(1)=\beta_c\), which proves the affine-fiber formula.

## Family-level leverage and limitations

This is a primitive-order-\(21\) compatibility theorem that genuinely uses
the pointwise \(16\)-state coupling. It is not implied by the earlier
coefficient-unrestricted specialization-image theorem. It replaces a
word-level condition by at most \(6\) or \(38\) Gaussian trace values for an
entire branch/case stratum, independently of the \(18\) support orbits.

The lemma does not by itself prove that any fiber is empty. A later argument
must combine the displayed affine lattice with a bound, norm, ideal, rank, or
representation-theoretic restriction on the primitive component. It does
not exclude any QLP-42 cell and does not resolve QLP-42.

The Discovery Net lemma is
bafkreiccjjgdr5n66zq7v5e2o3osr722mrtii4oarjgrwyoajkwd55rvle, committed at
height \(1264\) with a Markdown/LaTeX body. The file graph_receipt.json
records its transaction and five atomic relations.

No \((1+i)\)-adic lifting, cellwise SAT, residue census, or witness search is
used.

## Reproduction

Run with CPython \(3.12\) or later:

    ./verify.sh

The dependency-free checker verifies all \(16\) local states directly,
proves the Ramanujan kernel identity on all \(21\) difference classes,
reconstructs all six exact-sum values, and verifies the \(q=5\) and \(q=37\)
fiber sets. Its computation is a universal identity check, not an
enumeration of frontier cells.

## Dependencies and trust boundary

The algebraic theorem depends only on cyclic character orthogonality and the
displayed local transform. Its application to QLP-42 imports the canonical
norm-\(32\) shell, the coupled-transform theorem, and the six exact-sum cases.
The proof is human-checkable; the source provides redundant exact
verification. Interpreter, operating-system, and hardware trust applies only
to that verification. No floating point, external package, randomness,
solver status, or timeout enters the result.
