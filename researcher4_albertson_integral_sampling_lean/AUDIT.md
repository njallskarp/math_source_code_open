# Formalization audit

## Exact interface

The finite types in the headline theorem have distinct roles:

- `α` identifies vertices;
- `ε` identifies edges, with `edgeSupport : ε -> Finset α`; and
- `χ` identifies individual crossings, with
  `crossingSupport : χ -> Finset α`.

This representation permits two distinct crossings to have the same
four-vertex support.  A plain `Finset (Finset α)` representation would erase
that multiplicity and would not faithfully model every good drawing.

For a universe `U`, sample size `s`, and features all having support size `k`,
`sum_supportedCount_powersetCard` uses Mathlib's theorem
`Finset.card_filter_powersetCard_subset` to prove

```text
sum_{S in powersetCard s U} supportedCount features support S
  = |features| * choose (|U|-k) (s-k).
```

Consequently, if every sample satisfies

```text
a * edgeCount(S) <= crossingCount(S) + d,
```

then `fixed_support_sampling_bound` proves

```text
a*|edges|*choose(|U|-2,s-2)
  <= |crossings|*choose(|U|-4,s-4) + d*choose(|U|,s).
```

For `|U|=54`, `|edges|=726`, `s=24`, `a=5`, and `d=496`, the final arithmetic
is therefore

```text
5*726*choose(52,22)
  <= |crossings|*choose(50,20) + 496*choose(54,24).
```

Lean proves this implies `6076 <= |crossings|` and independently normalizes
the corresponding rational average to `10759164/1771`.

With local deficit 495, the same generic theorem instead yields

```text
5*726*choose(52,22)
  <= |crossings|*choose(50,20) + 495*choose(54,24).
```

`order54_local495_average_value` normalizes the average to
`1965795/322`, and `albertson_order54_of_local495` proves the resulting
integer conclusion `6105 <= |crossings|`.

For vertex deletion, `sum_supportedCount_erase` proves the second reusable
identity

```text
sum_{v in U} supportedCount features support (U.erase v)
  = |features| * (|U|-k).
```

Thus four-supported crossing occurrences on 54 vertices survive exactly 50
deletions each, with multiplicity preserved even when supports coincide.

The height-1771 review supplies the local inequality in subtraction-free form

```text
5650 <= deletedCrossings(v) + 27*excess(v)
```

and the degree-excess total `sum_v excess(v)=48`.  Lean's
`order54_deleted_sum_lower_bound` sums these to at least 303804.  The headline
`albertson_order54_two_stage_deletion` combines this with the deletion identity
and proves

```text
303804 <= 50*|crossings|  and  6077 <= |crossings|.
```

The companion `order54_degree_excess_total` verifies the finite handshake
arithmetic: on 54 vertices, degree sum 1452 and
`degree(v)=26+excess(v)` imply total excess 48.

## Published-bound conversion

Büngener--Kaufmann's local theorem at 24 vertices reads

```text
cr(H) >= 5|E(H)| - (203/9)*22.
```

Because both counts are natural numbers, the local contribution can be
rounded before averaging.  `local_integral_rounding_24` formally proves

```text
5*m - (203/9)*22 <= c  ==>  5*m <= c+496.
```

The theorem `albertson_order54_of_published_local_bound` combines this exact
rational-to-natural step with both incidence identities and the order-54
arithmetic.  It has no hidden uniqueness assumption on vertex supports.

## What is and is not formalized

Formalized:

- fixed-support incidence over all fixed-cardinality samples;
- multiplicity-safe edge and crossing aggregation;
- the exact local ceiling at sample size 24;
- the specialized order-54, 726-edge inequality;
- the exact rounded average and the lower bound 6076; and
- the exact deficit-495 average and its lower bound 6105;
- the generic single-vertex-deletion support identity;
- the degree-excess aggregation to 303804; and
- the exact two-stage conclusion `50*|crossings| >= 303804`, hence 6077.

Not formalized:

- definitions of drawings, good drawings, or crossing number;
- existence of a crossing-minimal good drawing;
- the fact that restricting such a drawing to `S` inherits precisely the
  crossings whose four endpoints lie in `S`;
- the analogous topological interpretation after deleting one vertex;
- Büngener--Kaufmann's crossing-number theorem itself; or
- Sadhu's reduction of a hypothetical `r=27` counterexample to the orders 53
  and 54; or
- the height-1765 reduction from `cr(24,132) >= 165` to a uniform local
  deficit of 495; or
- the height-1771 pointwise lower bound for `cr(G-v)`, critical-graph minimum
  degree, and the graph-theoretic handshake identity.

These remaining statements form the declared external mathematical boundary.
There is no external executable or data boundary.

## Verification record

The clean commands in `README.md` completed 8,707 build jobs.  Standalone Lean
replay exited zero.  The fifteen audited declarations use only
`propext`, `Classical.choice`, and `Quot.sound`, except that the pure final
natural-number implication omits `Classical.choice`.

The source scan found none of `sorry`, `admit`, custom `axiom`, `unsafe`, or
`native_decide`.  Source SHA-256:

```text
80e08174923b16e99bfd040ff5cda87c911a19a4a203c7163b8aefe5ddcc6f9c
```
