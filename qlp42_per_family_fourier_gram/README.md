# Per-family Fourier–Gram sieve for the QLP-42 middle branches

## Theorem

For one family \(X\in\{A,B\}\), define

\[
a_X=\sum_{j=0}^{20}|S_X(j)|^2,\qquad
s_X=S_X(1),\qquad h_X=H_X(1),
\]

and let

\[
\sigma_X=\sum_{j=0}^{20}\epsilon_X(j),
\qquad
\epsilon_X(j)=-iS_X(j)\overline{H_X(j)}\in\{-1,0,1\}.
\]

The Gram matrix of the twenty nontrivial Fourier coefficients of \(S_X\)
and \(H_X\) is positive semidefinite. Consequently

\[
D_X=
\left(21a_X-|s_X|^2\right)
\left(21(42-a_X)-|h_X|^2\right)
-\left|21i\sigma_X-s_X\overline{h_X}\right|^2
\ge0.
\]

Across the two families,

\[
a_A+a_B=43.
\]

If \(q_X\) is the family quarter-turn count, its aggregate parameters obey

\[
a_X\equiv q_X\pmod2,\qquad
q_X\le a_X\le42-q_X,\qquad
\sigma_X\in\{-q_X,-q_X+2,\ldots,q_X\}.
\]

Applying these inequalities to all six canonical exact-sum cases gives the
following complete aggregate classification.

1. For \(q=5\), all \(6{,}120\) arithmetically admissible aggregate tuples
   satisfy both family Gram inequalities.
2. For \(q=37\), exactly \(26{,}796\) of \(27{,}240\) aggregate tuples
   survive. The \(444\) failures are precisely:
   - in every exact-sum case and for either family, a family with
     \(q_X=21\), \(a_X=21\), and \(|\sigma_X|=21\);
   - additionally, in canonical case \(0\), family \(B\) with
     \(q_B=20\), \(\sigma_B=20\), and either \(a_B=20\) or \(a_B=22\).
3. No total cross-trace fiber point is removed: every
   \(\sigma\in\{-q,-q+2,\ldots,q\}\) still has at least one surviving
   aggregate decomposition in every exact-sum case.

Thus the sieve excludes signed-orientation strata shared by entire support
families, but it does not exclude a complete support orbit or exact-sum cell.

## Proof of the Gram inequality

Let \(\zeta\) be a primitive \(21\)-st root of unity. Remove the trivial
Fourier coefficient and form the two vectors

\[
\mathbf s_X=\left(S_X(\zeta^k)\right)_{k=1}^{20},
\qquad
\mathbf h_X=\left(H_X(\zeta^k)\right)_{k=1}^{20}.
\]

Plancherel and the pointwise identity
\(|S_X(j)|^2+|H_X(j)|^2=2\) give

\[
\|\mathbf s_X\|^2=21a_X-|s_X|^2,
\]

\[
\|\mathbf h_X\|^2=21(42-a_X)-|h_X|^2.
\]

The primitive cross-trace identity, now summed over all nontrivial
characters, gives

\[
\langle\mathbf s_X,\mathbf h_X\rangle
=21i\sigma_X-s_X\overline{h_X}.
\]

The determinant of the \(2\times2\) Gram matrix of these vectors is
nonnegative, proving \(D_X\ge0\).

The constraints on \(a_X\) follow from

\[
a_X=2o_X+q_X,\qquad
21=o_X+q_X+e_X,
\]

where \(o_X,e_X\) count opposite and equal local cells. The constraint on
\(\sigma_X\) follows because it is a sum of \(q_X\) signs.

The remaining classification is a finite exact evaluation of these displayed
integer inequalities. It ranges only over the aggregate integers
\((q_A,a_A,\sigma_A,\sigma_B)\), with \(q_B=q-q_A\) and
\(a_B=43-a_A\). It never enumerates a support word, support orbit, local-state
word, residue cell, or SAT assignment.

For a fully quarter-turn family, \(q_X=a_X=21\). In family \(A\), the aligned
orientations give

\[
D_A=-441|s_A|^2<0.
\]

The family \(B\) values and the exceptional case-\(0\) family-\(B\) values
are obtained by direct substitution in the same determinant; the exact
checker verifies that the listed patterns are all failures and that no
others occur.

## Reproduction

Run with CPython \(3.12\) or later:

    ./verify.sh

The dependency-free checker uses arbitrary-precision integers, reconstructs
all six canonical sums from their defining representatives, evaluates every
admissible aggregate tuple, verifies the exact failure-pattern set, and
checks that every total \(\sigma\)-fiber remains represented.

## Scope and trust boundary

This result depends on the canonical norm-\(32\) shell, the coupled
half-sum/half-difference transform, its six exact-sum cases, and the preceding
cross-trace lemma. The Gram proof is exact and human-checkable; the small
aggregate classification is certified by the published standard-library
checker.

The result does not enumerate frontier cells, use a \((1+i)\)-adic layer,
run SAT, or produce isolated witnesses. It excludes no complete \(q=5\) or
\(q=37\) cell and does not resolve QLP-42. Interpreter, operating-system, and
hardware trust applies to the finite classification only.
