# Translation obstruction to compressed fiber-norm detection

## Disproved detector

Write a sixteen-state word on \(C_7\times C_3\), and compress the
\(S\)- and \(H\)-coordinates along the three-cell fibers to vectors
\(U_S,U_H\in\mathbb Z[i][C_7]\). The proposed detector asserted that
exchanging two monochromatic fibers whose states lie in opposite quarter
classes must change at least one of

\[
U_SU_S^*,
\qquad
U_HU_H^*.
\]

This assertion is false.

## General counterexample family

Let \(a,b\) be any two local states and consider the compressed state words

\[
F=(a,b,b,b,b,b,b),
\qquad
G=(b,a,b,b,b,b,b).
\]

The second word is a cyclic translate of the first. For any group-ring
element \(U\) and any \(t\in C_7\),

\[
(tU)(tU)^*=tUU^*t^{-1}=UU^*,
\]

because \(C_7\) is abelian. Applying the two coordinate maps from the local
alphabet gives

\[
U_S(F)U_S(F)^*=U_S(G)U_S(G)^*,
\]

\[
U_H(F)U_H(F)^*=U_H(G)U_H(G)^*.
\]

If \(a\) is a quarter state and \(b\) is not, or conversely, lifting each
compressed coordinate to a monochromatic \(C_3\)-fiber produces a
cross-category exchange. The lifted words have the same state counts and
their quarter supports have symmetric difference six. Every state-indicator
difference is constant on each three-cell fiber, so every primitive
order-\(21\) indicator coefficient also agrees.

Thus adding translation-invariant compressed norms to the primitive
indicator package cannot yield a universal fiber-trade detector.

## QLP scope

The family is a structural obstruction to the proposed mechanism, not a
QLP-42 construction. Its exact \(S/H\) sums need not be one of the six
canonical cases, and it does not assert the full coupled QLP identities.
The result leaves open whether the canonical exact sums plus some further
non-aggregate, rotation-covariant QLP invariant can prohibit all relevant
cross-category trades.

An invariant forced to take one absolute character phase cannot solve this
problem because cyclic translation is a QLP symmetry. A viable replacement
must either be rotation-covariant and compared modulo that action, or use a
relative invariant coupling several nonconstant fibers.

## Verification

Run:

    ./verify.sh

The checker reconstructs the sixteen exact local states and verifies the
construction for all \(128\) ordered cross-class state pairs. It evaluates
both periodic group-ring norms directly with Gaussian integers, checks the
translation identity, expands the monochromatic fibers, checks the primitive
fiber-factor condition, and confirms the six-position support change. The
general proof above, rather than the finite check, establishes the theorem
for arbitrary coordinate maps and any cyclic group size.
