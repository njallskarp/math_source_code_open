# A sharp substitution bound for full-feedback localization

For every connected finite quotient graph \(G\) with at least two vertices
and arbitrary nonempty internal graphs \(H_v\),
\[
\zeta_d^*(G[H_v])\le2\zeta_d^*(G).
\]
The factor is sharp already at \(\zeta_d^*(G)=1\): the 128-vertex graph
\(Q_6\vee Q_6=K_2[Q_6,Q_6]\) has full-feedback directional localization
number exactly two. Each cube separately is resolvable in one round by one
probe. All substitutions over connected one-probe quotients, including
chordal quotients, are therefore excluded from the greater-than-two frontier.

[THEOREM.md](THEOREM.md) gives the complete strategy simulation, its final
localization step, a stronger result for strategies whose probe sets have no
isolated vertices, and an indefinite-evasion proof for the sharp example.
The evasion proof uses the elementary bound that every 13 vertices of
\(Q_6\) have at least 35 vertices in their closed neighborhood. A small
integer recurrence proves that bound without assuming a graph catalogue,
a solver verdict, or an external isoperimetric theorem.

## Reproduce

Run from this directory, with Python 3.10 or later and no extra packages:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
shasum -a 256 -c SHA256SUMS
```

The first command must match `EXPECTED_OUTPUT.txt` and end with

```text
result_sha256=d118f42c7cb5fb2d763287ab3d118882abed4e1f05694f431de448dfbcdec67c
VERIFIED
```

The deterministic audit checks 14,027 substitutions, 1,211,592 guarded
module targets, 487,074 projected responses, and 393,768 final probe pairs.
It additionally checks every subset of the cubes of dimensions zero through
four (65,814 sets), the required recurrence at dimension six, all 128 far
response classes in the join, and its explicit one-round two-probe strategy.
The finite domain for the substitution audit is stated in the code; these
counts do not assert an exhaustive search over arbitrary graph orders.

The discovery prototypes are excluded. The published checker computes
responses directly from shortest-path distances and tests the local
structural lemmas, rather than trusting the exploratory game search.
Validation used CPython 3.12.12. An additional run with `python3 -B -O`
matched the expected output, taking 3.002 seconds with 38,731,776 bytes
peak child RSS on the validation host; these measurements are not stable
mathematical outputs. Computation audits the proof's interfaces
and arithmetic; the universal theorem rests on the displayed proofs.
This is not a proof-assistant formalization or an independently reviewed
result. Novelty is relative to the graph and primary sources searched on
2026-09-09; no historical priority is asserted. The existence of a graph
with \(\zeta_d^*>2\) remains open in the inspected source.
