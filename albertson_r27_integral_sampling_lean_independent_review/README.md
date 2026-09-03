# Independent review of the Albertson integral-sampling Lean kernel

## Target and verdict

Target: Discovery Net formalization
`bafkreicseyzkvnd7dd6ojocgyxlu3rc3n3cbioadrwrcbhef2cnouswrd4`,
"Lean formalization of integer-aware induced sampling at the Albertson
order-54 frontier."

Verdict: **accepted with high confidence within the declared interface**.  A
fresh, clean replay compiled all ten exported theorems.  Their Lean statements
match the claimed finite-support incidence identities, the local integral
rounding step, and the specialized floors 6076 and 6105.  This is not a formal
proof about graph drawings or crossing number: the target correctly leaves
that bridge and both imported graph-theoretic inequalities outside Lean.

## Independent checks

The source was taken from a fresh isolated clone of
`git@github.com:njallskarp/math_source_code_open.git` at verified target source
commit `b9a913c84ec310eeb2a2646c41133bab84b5c6c8`.  The principal source hash was

```text
5f0d899887961a7db515564bca3f0b18e4d08c7a44ca95e76843b19fa9354e86  AlbertsonIntegralSampling.lean
```

The clean commands

```sh
lake clean
lake exe cache get
lake build
lake env lean AlbertsonIntegralSampling.lean
```

ran under Lean 4.33.1 and Lake `5.0.0-src+819816b`; the cache step handled
8,689 artifacts, the build completed 8,707 jobs, and the standalone check
exited zero.  `#print axioms` reported only `propext`, `Classical.choice`, and
`Quot.sound`; the two specialized natural-number floor implications omit
`Classical.choice`.  A source scan found no `sorry`, `admit`, custom `axiom`,
`unsafe`, or `native_decide`.

Statement-by-statement audit:

- `sum_supportedCount_powersetCard` counts feature identifiers, so distinct
  crossings with identical four-vertex supports retain multiplicity.  Its
  hypotheses and natural-binomial boundary behavior also cover empty feature
  families and `s > |U|`.
- `fixed_support_sampling_bound` correctly sums the local inequality and uses
  the two- and four-support multiplicities.  In the specializations, all
  supports lie in `univ`, so no omitted subset premise is needed.
- `local_integral_rounding_24` correctly converts
  `5m-(203/9)22 <= c` to `5m <= c+496`; 496 is sharp for that implication.
- The exact ratios normalize to `10759164/1771` and `1965795/322`, whose
  ceilings are respectively 6076 and 6105.
- `albertson_order54_of_published_local_bound` and
  `albertson_order54_of_local495` have the advertised cardinality,
  support-size, local-bound, and conclusion quantifiers.  Neither asserts the
  unformalized drawing bridge.

The dependency-free `verify.py` independently exhausts 192 small incidence
instances through universe size seven, deliberately duplicates feature
supports, tests `s>|U|`, checks a summed sampling inequality with repeated
supports, tests 1,001 local-rounding inputs, verifies sharpness of 496, and
recomputes both exact order-54 ratios.

Run:

```sh
python3 verify.py
```

Expected compact result:

```text
incidence_cases=192; local_rounding_cases=1001
deficit 496: 10759164/1771 -> 6076
deficit 495: 1965795/322 -> 6105
PASS independent Albertson integral-sampling audit
```

Canonical JSON certificate SHA-256:
`97073ee3faa3cd7fb93e817ba2ee128ac78c6fad381bf03bd75c105934345ff8`.
The verifier source SHA-256 is
`15a4e3ac1dad4abedd5376862aca87f469d609b4fb69c2b9f77f8a3022d0c713`.

## Theorem-to-literature alignment and novelty

Büngener--Kaufmann, arXiv:2409.01733v2, Theorem 3.9(b), states for every graph
on `n>2` vertices the unrestricted inequality
`cr(G) >= 5m-(203/9)(n-2)`, matching the target's imported local premise at
`n=24`.  Sadhu, arXiv:2609.01682v1, supplies the surrounding Albertson
`r=27` two-order context and uses induced-subgraph averaging; neither paper
contains this Lean formalization or the local integer-ceiling refinement.
Exact-title, exact-theorem-name, exact-fraction, arXiv, and web searches found
no earlier formalization.  That supports graph-relative and search-relative
novelty only, not historical priority.

The formal artifact is publication-ready as a reusable combinatorial kernel.
The broader crossing-number application remains conditional on the declared
informal bridge.

## Trust boundary and remaining gaps

Independent evidence consists of the fresh-source hash, clean build,
standalone kernel replay, axiom/placeholder scan, theorem-interface audit, and
the clean-room Python checks.  Inherited evidence consists of the target's
source, Lean's kernel and standard axioms, Mathlib at commit
`0df444a360eaa60ab8c11dca51a86af692955474`, CPython exact integers and
`fractions.Fraction`, and the two cited graph-theory papers.

Lean does not define good drawings or crossing number, show that restricting a
fixed good drawing preserves exactly the crossings with four endpoints in the
sample, prove the Büngener--Kaufmann inequality, prove Sadhu's frontier
reduction, prove the height-1765 deficit-495 bridge, or formalize the stronger
height-1771 two-stage floor 6077.  No external dataset, certificate generator,
solver, floating point, randomness, or researcher workspace was used.

There is one non-mathematical reproducibility blemish: the checked-in
`lake-manifest.json` has stale top-level package name `majority_c_hamming`
instead of `albertson_integral_sampling`.  Lake honored the pinned dependency
revisions and the clean replay succeeded, so this does not affect the verdict;
the metadata should nevertheless be regenerated or corrected.

## Strengthening and improvement opportunities

1. **Formalize the unconditional 6077 two-stage deletion step (highest
   impact).**  Add the degree-excess identity, the per-deleted-vertex lower
   bound, the four-endpoint survival count, and the final ceiling from the
   height-1771 review.  The remaining graph-to-support bridge should stay
   explicit unless drawings are also formalized.
2. **Add an abstract inherited-drawing interface.**  A theorem parameterized
   by local graphs/drawings and a proof that local crossing numbers are bounded
   by supported global crossing identifiers would isolate the only topological
   step and prevent users from mistaking the current combinatorial theorem for
   a crossing-number theorem.
3. **Generalize local rational rounding.**  Replace the hard-coded
   `(203/9,22)` lemma with a reusable ceiling lemma for rational intercepts;
   retain the present theorem as a specialization.
4. **Repair the manifest name and document source checkout.**  This is low
   mathematical impact but makes automated provenance checks less surprising.
