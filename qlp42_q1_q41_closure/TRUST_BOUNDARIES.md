# Trust boundaries

## 1. Mathematical reduction boundary

The result is conditional on the previously established canonical norm-32
residual shell, the six canonical order-two sum cases, and the exact coupled
half-sum/half-difference transform. The transform is a bijective theorem
inside that shell, but this package does not independently rederive the
earlier claim that every candidate under discussion reaches the selected
shell representative.

Consequently the conclusion is:

```text
no q=1 or q=41 lift in the established canonical norm-32 shell,
```

not:

```text
no quaternary Legendre pair of length 42.
```

## 2. Imported coupled-transform bridge

The bridge is pinned at commit
`f220c6bb1d11da07d24a816e82be2ead985c7052`, directory
`qlp42_coupled_half_transform`, Git tree
`4c53d38ce84c83d2769475a5e58be86e6d783c0f`, and graph artifact
`bafkreias46qnx32stuc7ej6akxloxuadbg5mfdzdixjl7bch7ufr5f2wyi`.

Its certificate checks the 16 local states, exact inverse formulas, the two
autocorrelation identities on all 4,096 fourth-root words of length six, the
norm-32 targets, and all six global-sum cases. A graph review independently
verifies the result. Remaining trust includes the general symbolic expansion
from the finite tests, the adopted indexing conventions, the preceding shell
reduction, and the absence of a proof-assistant formalization.

The CP-SAT smoke runs in that directory returned `UNKNOWN` and are not used.

## 3. q=1 completeness boundary

The q=1 theorem trusts the complete third-order classifier for the exhaustive
`b` partition and nine separately pinned finite obstructions. The classifier
uses exact integer and bit arithmetic and independently checks orbit counts by
Burnside’s lemma. Every final row certificate is exact; none relies on a
timeout or heuristic trajectory.

At the initial graph audit, the final `b=20` and `b=16` source theorems lacked
their own graph contributions, and the existing graph node claiming q=1
closure therefore did not have explicit edges to them. This is a graph-
provenance gap, not a source-certificate gap. `GRAPH_RELATIONS.md` records it.

## 4. q=41 weight-12 boundary

Weight 12 has non-free cyclic action: five orbits have size 7 and 13,995
have size 21. The exact coverage identity is

```text
5*7 + 13,995*21 = 293,930 = C(21,12).
```

The production coordinator reconstructs these multiplicities and rejects
missing, duplicate, unexpected, or wrongly sized records. The independent
NumPy implementation also reconstructs all 24,946 all-weight orbits and the
weight-12 short-orbit structure.

The full production C++ sweep enumerates all 1,629,936,000 exact `H_B` sign
assignments at weight 12. The independent NumPy verifier fully recomputes the
order-4-through-order-12 `H` ladder for all terminal family-B orbits and
deterministic empty controls, then checks every terminal exact-`S` case. It
does **not** duplicate the complete preterminal `H` enumeration for all
14,000 weight-12 orbits. Thus a systematic false negative in the production
code outside the independent terminal/control replay remains within the
software trust boundary.

The production source also hard-codes the mistyped aggregate
`manifest_b_axis_words=524776`; the correct sum is 523,776. The coordinator's
definition-level orbit dictionary still proves exact record coverage and
orbit multiplicities. This QA miss is documented in `ERRATA.md` and is one
reason not to treat a printed aggregate as a coverage certificate.

Mitigations are deterministic 8- and 3-worker sweeps with identical complete
stream hashes, an independently constructed orbit manifest, 369,577 stable
definition-level PAF audits across the all-weight run, a complete two-worker
sanitizer sweep with the same digest, and independent terminal replay. This
is strong evidence, not proof-assistant-level elimination of implementation
trust.

## 5. Exactness of the order-12 cutoff

The use of `pi^12`, `pi=1+i`, is not a heuristic residue cutoff. Every `H`
residual coordinate has real and imaginary magnitudes at most 43 and 41;
every `S` residual coordinate has component bounds 44 and 42. Hence each
residual has modulus below 64. A nonzero Gaussian integer divisible by
`pi^12` has modulus at least 64. Therefore a matching `pi^12` fingerprint is
an exact equality in `Z[i]` for this problem.

## 6. Runtime and platform boundary

The finite certificates trust source inspection, Python and NumPy integer
semantics, C++ fixed-width and signed-integer semantics within documented
bounds, compilers, interpreters, operating system, and hardware. Sanitizers
reduce but do not remove that trust. No floating point, randomized proof
step, solver status, or time limit enters either branch-closure claim.

The 2026-09-02 replay of the `b=16` driver completed successfully under Apple
clang 17, but compilation emitted two pre-existing warnings that embedded
non-void helper mains can reach their closing brace without an explicit
return. The certificate invocations follow the returning paths and reproduced
all recorded outputs. The warnings are source-quality debt and should be
removed in a future release; they are not silently suppressed here.

## 7. Publication and graph boundary

Git commit hashes and Git tree IDs provide immutable source addressing. Graph
receipts demonstrate committed ledger inclusion, not mathematical truth.
Conversely, a missing graph relation does not erase a published source proof.
The package keeps these two provenance layers separate.

## 8. Literature boundary

Prior-art searches can support an apparent-novelty statement but cannot prove
historical priority. The manuscript therefore makes no priority claim.
