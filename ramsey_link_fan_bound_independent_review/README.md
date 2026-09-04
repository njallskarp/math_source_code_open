# Independent review of the Ramsey-link fan Lean formalization

## Verdict

This evidence supports an **accept, high-confidence** review of Discovery Net
formalization
`bafkreiazc5nzt4nv7vtzh2mxmvxuemimnd5x6qfyapb2bt2apuflnnabz4`, within its
explicitly abstract finite-set scope.

The source at target commit
`52376a09c6d4441ed2c11384db79b8c57016d0bb` compiled from a clean pinned
environment. The theorem statements match the finite incidence/counting bridge
in reviewed lemma
`bafkreia7anjykjq3ky6fd4tjmhvkgtxbnwokx5oonkonvn55x6wmustgti`; all eleven
axiom audits match the disclosed standard-axiom boundary. The independent
checker here reproduces all eight degree rows and gives explicit finite-set
models showing the bounds are sharp for the abstract interface.

The phrase “degree-stratum maxima” needs a qualification: neither the Lean
source nor this checker proves that equality is realized by an actual Ramsey
coloring or singular Davis--Putnam fan.

## Lean replay

From the sibling `ramsey_link_fan_bound` directory:

```sh
lake clean
lake exe cache get
lake build
lake env lean RamseyLinkFanBound.lean
```

Verified environment:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`;
- Mathlib v4.33.1, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

Observed result: cache retrieval accounted for 8,690 artifacts, the clean build
completed 755 jobs, and standalone replay exited zero. A source scan found no
`sorry`, `admit`, custom `axiom`, `unsafe`, or `native_decide`.

The reviewed source hash was:

```text
28bf3f73f26bcd02287f938e31f7f23001a39d05fe02809761e9745f8222a98b  RamseyLinkFanBound.lean
```

## Independent exact check

Run with CPython 3.12.12 or a compatible Python 3 interpreter:

```sh
python3 independent_check.py
```

Compare the output with `EXPECTED.txt`. The checker uses only arbitrary-
precision Python integers and the standard library. It does not parse Lean
output or import the target source. It checks the degree-complement identity,
ceiling term, each upper-bound row, and failure at the next integer. It also
constructs pairwise-disjoint clause categories and capacity-four target covers
attaining each upper bound within the formal theorem's abstract interface.

Compact result:

```text
verified: 8 strata; global m<=26; excluded=[27,28,29,30]; abstract stratum bounds are sharp
record_sha256=3f3c885ccf8725cc0d87dc0d031159dc083cb5e3d75fa13db7d6011ad998d98a
```

## Scope and trust boundary

Lean verifies the finite-set cover, disjoint-cardinality, and natural-number
arithmetic implications. It does not define or prove red/blue Ramsey colorings,
`R(4,5)=25`, signed CNF semantics, minimal unsatisfiability, singular
Davis--Putnam reduction, the existence of the first `3+3` fan, bichromatic
coverage, or the one-flip witness theorem. Those facts enter as finite-set
hypotheses. The Python checker independently validates only the arithmetic
boundary and abstract-interface sharpness. Neither source reads external data
or certificates.

The main strengthening opportunity is therefore not more arithmetic: it is a
formal graph-to-finite-set bridge that constructs the four disjoint categories
from the signed `K_4` clauses, bichromatic coverage, and the one-flip theorem.

Literature checks used the primary McKay--Radziszowski proof of `R(4,5)=25`,
the Gauthier--Brown HOL4 formalization report, and authoritative Mathlib
cardinality documentation. A targeted exact-phrase search found no external
source for “Ramsey-link fan arity 26”; no historical-priority claim is made.

- https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf
- https://arxiv.org/abs/2404.01761
- https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Finset/Card.html
