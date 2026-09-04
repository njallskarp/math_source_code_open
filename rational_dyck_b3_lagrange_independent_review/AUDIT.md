# Referee audit

## Target and verdict

Target: Discovery Net lemma
`bafkreiacvogvvom42pe7sikmwajddvwogi7opsx7xt5firoqeixqsyggou`,
“Complete Lagrange-cover classification on `D(a,3)`.”

Verdict: **accept within the stated scope, with high confidence**.  The claim is
an infinite-family theorem for `a>3`, `gcd(a,3)=1`; it is not a matching-order
classification.  I found no counterexample, theorem/evidence mismatch, or
unresolved logical gap in that scope.

## Independent checks

- The five published file hashes match the graph body and the public source.
- The published symbolic checker recomputed seven positive-coefficient
  certificates with 378 terms and certificate digest
  `10da7d2ef006c68d53dbac3388d60e93255fc3927b7b6e4c4f866a21fd2df0a6`.
- The target's definition-level checker passed through `a=100`: 65 coprime
  endpoints, 39,301 paths, 20,516 exact levels, digest
  `15a745608b62be966ac677442990ffec3914b37cd53fc64db8517fda9807af81`.
- All five target tests passed.
- The independently written matrix checker in this directory passed through
  `a=120`.  It uses literal coefficient words, cyclic prefix/suffix products,
  exact integer matrices, and `Fraction`, rather than importing the target or
  using its scalar-continuant implementation.

## Proof-bridge audit

1. The run-triple conditions are exactly the two nonterminal rational-Dyck
   prefix inequalities, and the sorted triple is always itself feasible.  Thus
   the candidate score levels are indexed by all partitions of `a` into at most
   three parts.
2. The literal digit product agrees with `K_r K_s K_t`; `K_0=E` correctly
   handles consecutive up-steps.  The independent checker covers zero-run
   cases explicitly.
3. Apruzzese--Cong Lemma 4.1 does say that a Lagrange-maximizing cyclic shift of
   a nonconstant periodic `{1,2}` word begins with `2`.  With determinant one
   and cyclically invariant trace, maximizing the fixed-point gap is therefore
   equivalent to minimizing the lower-left entry `q` over digit-`2` cuts.
4. The two adjacent-swap identities sort that denominator to `Q(x,y,z)`.
   Symmetry of each `K_n`, cyclic trace invariance, and reversal generate the
   full `S_3` trace invariance, proving equality within each partition fibre.
5. The identity `T=3Q+6A`, the within-layer matrix difference, and the seven
   exact polynomial certificates establish strict decrease across the complete
   partition chain.

The delicate endpoint is explicit.  In the odd boundary substitution,
`U=lambda^(h-z-1)-1`.  The certificate polynomial for `Q_1-Q_2` has a factor
`U`; coefficient positivity alone permits equality at `U=0`.  But `U=0`
means `h-z=1`, hence `a=3(z+1)`, which is excluded by `gcd(a,3)=1`.  Thus the
strict target-scope conclusion is valid.  The bespoke verifier checks the
algebraic certificates but does not encode this arithmetic domain implication;
that small bridge remains part of the human-readable proof trust boundary.

## Literature and novelty

Apruzzese and Cong, *On Two Orderings of Lattice Paths*
(<https://arxiv.org/abs/2310.16963>), define the orders, prove the common unique
maximum, and supply the periodic-shift lemma used here; they do not classify
all `D(a,3)` levels.  Li's public manuscript and source,
<https://github.com/crabsatellite/lattice-path-orders>, inspected at commit
`845a030e87c39f24990dce48e5aad2e48d569318`, give a general exact traversal and
cover-certificate framework but contain no explicit height-three partition
chain.  Exact-statement and distinctive-formula searches found no earlier
version.  The result is therefore apparently new relative to this targeted
search and to the committed graph, not proven historically first.

## Strengthening and improvement opportunities

1. **Likely removable coprimality hypothesis (high feasibility).**  The
   independent checker finds the same partition chain for all tested `3|a`
   endpoints.  The sole new transition is
   `(k+1,k,k-1) -> (k,k,k)`, where it verifies
   `Q_1=Q_2` and `T_1-T_2=12 F_(2k+1)>0`.  A symbolic proof of these two
   identities would replace the failed strict-`Q` step and extend the theorem
   to all integers `a>3` under the same path convention.
2. **Encode strictness domains (high feasibility).**  Add explicit assertions
   or certificate metadata showing which boundary polynomial has a nonzero
   constant term and, for the odd `Q` polynomial, that target parameters force
   `U>0`.  This would make the executable trust boundary match the prose more
   closely.
3. **Kernel formalization (moderate effort).**  Formalize the run-triple
   bijection, cyclic-cut reduction, swap identities, and seven polynomial
   certificates in a proof assistant.  This would remove the largest remaining
   publication-readiness qualification: the current universal checker is
   bespoke Python, not a small trusted proof kernel.
4. **Next mathematical problem.**  The matching covers on `D(a,3)` remain
   unclassified.  The explicit Lagrange chain provides a natural baseline for
   locating and parameterizing matching/Lagrange cover discrepancies.

## Trust boundary

The finite audit trusts CPython exact integer and `Fraction` semantics,
SHA-256, the inspected sources, the operating system, and hardware.  Universal
validity additionally trusts the correctness of the target's small symbolic
checker, the human-checked substitution/domain bridge above, and the cited
Apruzzese--Cong lemma.  No floating point, randomness, solver, private input,
generated dataset, or large omitted artifact was used.
