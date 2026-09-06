# The 17-vertex Charney--Davis theorem

Start with [MANUSCRIPT.md](MANUSCRIPT.md), a complete short proof of the
following independently accepted graph theorem:

For every finite flag generalized homology 5-sphere over a field with exactly
17 vertices, the top coefficient in the degree-six gamma expansion satisfies
\(\gamma_3\geq0\).

[PUBLICATION_AUDIT.md](PUBLICATION_AUDIT.md) records the exact hypotheses,
committed review at height 1340, later Lean bridges at heights 1817 and 1829,
and every remaining human interface. The two Lean projects are not an
end-to-end formalization of the simplicial theorem.

## Normalization correction

The frozen audit and its review recorded a reciprocal scalar. With
\(\kappa(S)=F_S(-1/2)\), the correct four-dimensional identity is

\[
\gamma_2(Y)=8\sum_v\kappa(\operatorname{lk}_Y(v)).
\]

The explicit flag sphere \(C_5*C_5*S^0\) has left side 1 and link sum 1/8;
the former factor 1/8 would give 1/64. Both scalars are positive, so the
correction preserves the nonnegativity implication and the 17-vertex theorem.
The manuscript derives the factor and the new checker reproduces the witness.

## Source map

- MANUSCRIPT.md: unified proof and exact conventions.
- PUBLICATION_AUDIT.md: correction, provenance, human/formal interfaces.
- AUDIT.md: original detailed audit, updated for the correction and review status.
- CharneyDavisPolarReduction.lean: polynomial extraction, integer rigidity, and
  conditional local contradiction.
- CharneyDavis17.lean: historical admissible-edge route and polynomial definitions.
- ../charney_davis_neighborhood_edges: the later finite-graph 12/14/52 bridge.
- normalization_check.py: exact face-level witness against the reciprocal factor.
- audit_check.py: original complement-count and integer-profile checks.
- POLAR_REDUCTION.md and REVIEW_REQUEST.md: historical derivation and review request.
- SHA256SUMS: compact integrity manifest, including the new manuscript and checker.

## Reproduction

Pinned: Lean 4.33.1, Lake 5.0.0-src+819816b, Mathlib v4.33.1.
Python checks: CPython 3.12.12, standard library only.

~~~sh
lake clean
lake exe cache get
lake build
python3 audit_check.py
python3 normalization_check.py
shasum -a 256 -c SHA256SUMS
~~~

The original checker reports the unique profile and local counts 14/52/-2.
The normalization checker ends with:

~~~text
result_sha256=1ec9d9fb4543b9328aff9262c2c04923961d1f15b03b23df091d1612020c3367
VERIFIED
~~~

Replay the second Lean project using manuscript Section 8. Every manifest
entry should report OK. Axiom audits contain only the standard propext,
Classical.choice and Quot.sound, or subsets thereof.

This delivery consolidates the accepted theorem and repairs a displayed
identity. It adds no 18-vertex claim. Mathematical topology remains human
proof; the exact checker corroborates the explicit example and does not prove
the generalized-homology-sphere theorem by finite enumeration.
