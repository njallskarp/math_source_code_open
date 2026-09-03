# Scope and formal theorem

This Lean 4 artifact independently checks the complete numerical-semigroup
post-processing in Discovery Net finding
`bafkreiavhgobrxrzgsbayatuxhrt5b3f2tvi37ynxfsehe2uqnuly22g4m`, whose
transfer computation reports closed-walk generators `54`, `106`, `107`, and
`108` for eight-color packing-total cycles.

Lean proves:

1. `2n` is a nonnegative combination of `54,106,107,108` if and only if `n`
   is a nonnegative combination of `27,53`.
2. With `r(n)=(27-(n mod 27)) mod 27`, one has
   `n in <27,53>` if and only if `53*r(n)<=n`.
3. Every `n>=1352` lies in `<27,53>`, while `1351` does not; hence the
   Frobenius number is exactly `1351`.
4. Exactly `663` integers in `[14,1351]` are not in `<27,53>`.

Parity supplies the first bridge: the coefficient of the odd generator `107`
must be even. The second is an exact Apéry-style residue criterion using
`53 == -1 mod 27`. The exceptional-order count is ordinary kernel-checked
`decide` over that proved criterion, not an imported table.

## Reproducibility

Source is in `research/packing_total_semigroup/`. The project pins Lean
4.33.1 and Mathlib tag v4.33.1, resolved to commit
`0df444a360eaa60ab8c11dca51a86af692955474`. After `lake clean`, the commands
`lake exe cache get`, `lake build`, and
`lake env lean SemigroupEndpoint.lean` completed successfully; all 8,707 build
jobs completed. The SHA-256 digest of `SemigroupEndpoint.lean` is
`2fefd6e42a05b8f3670d8e2d5d06820e415bdca17e52ba8e1e5fdc77e515d874`.

The constructive equivalence and conductor theorems report only
`[propext, Quot.sound]`; finite-set and `IsGreatest` wrappers additionally use
standard `Classical.choice`. The source contains no `sorry`, `admit`, custom
axiom, `unsafe`, or `native_decide`, and uses no external file, generated proof
data, solver, floating point, randomness, or nonstandard kernel/plugin.

## Exact trust boundary and literature status

This formalization does not import or verify the transfer automaton, its
339,203 reachable states, SCC decomposition, exhaustive cycle list, the
graph-coloring/closed-walk reduction, or seven-color impossibility. Those
remain explicit external bridges. Conditional on the reported
four-generator closed-walk classification, Lean proves every arithmetic
consequence above.

The primary source, Ferme and Mesarič Štesl, arXiv:2508.08691v2, gives exact
cycle values only through `C_13`, proves bounds for `n>=14`, records an
eight-color construction for multiples of `27`, and asks for exact values by
divisibility. It does not state the `<27,53>` classification. No novelty claim
is made for the elementary semigroup facts in isolation; the durable addition
is their reusable, independently kernel-checked composition and sharply
isolated trust boundary.
