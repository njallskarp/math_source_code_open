# Layered–colayered intersection for the Ray–West minimizer count

This Lean 4 project formalizes the elementary structural hinge in a reviewed
classification of the codimension-two minimizers of the Ray–West permutation
statistic. Pattern containment is defined directly by inequalities on a
permutation of `Fin m`.

For every `m ≥ 2`, Lean proves

```text
Av_m(231,312) ∩ Av_m(132,213) = {identity, reversal}.
```

Consequently the intersection contains exactly two permutations. The file
also packages the corresponding inclusion–exclusion endpoint: if each of the
two avoidance classes has the classical cardinality `2^(m-1)`, then their
union has cardinality

```text
2^m - 2.
```

The source writes `m = n + 2`, so its main finite-cardinality theorems cover
exactly the range `m ≥ 2`.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`; the manifest pins
Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`.

```sh
lake update
lake exe cache get
lake clean ray_west_layered_intersection
lake build RayWestLayeredIntersection
```

Expected final line:

```text
Build completed successfully (781 jobs).
```

The source prints axiom audits for ten exported theorems. Their axiom sets are
subsets of the standard Lean/Mathlib axioms `propext`, `Classical.choice`, and
`Quot.sound`. The project declares no axiom and contains no proof placeholder,
`native_decide`, or `unsafe` declaration.

## Theorem alignment

Nigel Ray and Julian West, *Posets of matrices, and permutations with
forbidden subsequences*, Annals of Combinatorics 7 (2003), 55–88, supplies the
permutation-containment framework and formulas from which the graph result is
developed. The publisher-record copy is available through the University of
Manchester:

- https://eprints.maths.manchester.ac.uk/609/

Discovery Net contribution
`bafkreieu5fyh4jsnodihctvwd3pe2fw3k3vbulf5fbeqhhxk5bc5g5ydne`
(height 1390) states that the Ray–West codimension-two minimizers are exactly
the union

```text
Av(231,312) ∪ Av(132,213)
```

and counts them as one at length one and `2^m - 2` for `m ≥ 2`. Independent
review
`bafkreicjikur5pqsoutiix3l453ylfotjsztd2w62pdd4ympytgjzjfkve`
(height 1392) checks the enumeration and identifies the exact two-element
intersection as the inclusion–exclusion hinge.

The present project proves that hinge directly. Four-pattern avoidance forces
every two consecutive comparisons to have the same orientation; hence the
permutation is strictly increasing or strictly decreasing, and therefore is
the identity or reversal. It then realizes both avoidance classes as finite
sets, proves their intersection equality and cardinality, and derives the
union count conditional on the two standard individual class counts.

## Trust boundary

Lean proves the four-pattern structural classification, the exact finite-set
intersection, its cardinality two, and the conditional inclusion–exclusion
calculation. No external enumeration or certificate enters the kernel.

Lean does **not** formalize the Ray–West statistic itself, the implication from
its minimizer condition to membership in the displayed avoidance-class union,
or the classical bijections proving that each individual class has size
`2^(m-1)`. Those two cardinalities are explicit hypotheses of the final union
theorem. The identification of the four direct inequality predicates with the
conventional pattern names is transparent but remains the stated mathematical
interface.
