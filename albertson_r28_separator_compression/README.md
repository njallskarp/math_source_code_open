# Small-separator compression at the Albertson r=28 frontier

This directory gives a structural postprocessing theorem for the two exact
Albertson `r=28` rows.  Its main new ingredient is a matching argument on a
four-vertex separator, not a larger degree-profile search.

## Upstream input

Height 2523 reduces an `r=28` counterexample to `(n,m)=(55,768)` or
`(55,769)`, with total excess

    x_v = d_G(v)-27,        sum_v x_v = 51 or 53.

Write `H=bar(G)`.  The corrected finite certificate underlying height 2569
proves that `H` is factor-critical, has no conformal triangle, and has a
triangle `T` whose associated Tutte set `B` has size three or four.  Every
surviving size-three component multiset contains a singleton.  At size four,
the only surviving component multiset is

    H-B: 49,1,1.

This exact upstream classification was independently replayed from public
commit `c9cdabd4b8bc17ff5e87293077eb017fc88407a5`; both expected-output diffs
were empty and every manifest hash passed.  It is nevertheless kept explicit
as an external dependency rather than silently copied into this checker.

## Separator lemma

Let `H` be factor-critical and have no conformal triangle.

First suppose a triangle `T` separates a singleton vertex `w`, so
`N_H(w) subset T`.  Pick `a in N_H(w)` and a perfect matching `M` of `H-a`.
The vertex `w` must be matched to another `b in N_H(w)`.  Since `T` is a
clique, `a,b,w` is a triangle, while `M-{wb}` is a perfect matching of
`H-{a,b,w}`.  This is a conformal triangle, a contradiction.  Hence the
height-2569 branch `|B|=3` is impossible.

Now let `B=T union {s}`, and suppose `H-B` has two singleton components
`w_1,w_2`.  Each `w_i` has at least two neighbours in `B`: delete one of its
neighbours and use factor-criticality.  Moreover:

1. `s` belongs to both singleton neighbourhoods.  Otherwise some `w_i` has
   two neighbours in the triangle, and the same matching argument makes a
   conformal triangle.
2. The sets `N_T(w_1)` and `N_T(w_2)` are nonempty and disjoint.  If they share
   `a`, then in a perfect matching of `H-a` both singleton vertices would have
   to use the sole potentially safe vertex `s`, which is impossible.
3. The vertex `s` is nonadjacent in `H` to every vertex in
   `N_T(w_1) union N_T(w_2)`.  In a perfect matching of `H-a`, the singleton
   adjacent to `a` must use `s`; an edge `as` would again close a conformal
   triangle.

The two disjoint nonempty subsets of the three-element set `T` therefore have
sizes `(1,1)` or `(1,2)`.  Consequently

    {d_H(w_1),d_H(w_2)} is {2,2} or {2,3},

and their excesses are `{25,25}` or `{24,25}`.  Up to permutations of `T` and
interchange of the singletons there are exactly three local types: two for
degree pair `(2,2)` (according as `s` is or is not joined to the unused
triangle vertex) and one for `(2,3)`.

The verifier checks a relaxation of this proof directly.  It enumerates the
eleven optional edges inside `B` and between the two singletons and `B`.  For
each deleted separator vertex it requires an injective singleton-to-separator
matching that does not immediately certify a conformal triangle.  Among 2048
labelled edge sets, only 18 survive, forming exactly the three claimed
symmetry orbits and the two claimed degree pairs.  Because this is a
relaxation of the global matching problem, excluding every other local type is
a rigorous necessary-condition argument.

## Exact profile compression

Subtracting the two forced singleton excesses from the row totals leaves at
most four units.  Their integer partitions give exactly the following degree
profiles.

For row 768 there are three:

    0^52 1 25^2,
    0^52 2 24 25,
    0^51 1^2 24 25.

For row 769 there are eight:

    0^52 3 25^2,          0^51 1 2 25^2,
    0^50 1^3 25^2,
    0^52 4 24 25,         0^51 1 3 24 25,
    0^51 2^2 24 25,       0^50 1^2 2 24 25,
    0^49 1^4 24 25.

Thus the 232,605 and 318,199 relaxed histograms at height 2523 collapse to
three and eight canonical excess profiles.  This crosses the predeclared
continuation gate of at most 30 profiles without copying the `r=27` case tree.

Reconstructing the exact rounded convex deletion tables gives

    row 768: minimum deletion sum 360156, bound 7062;
    row 769: minimum deletion sum 361740, bound 7093.

These improve the previous 7060 and 7092 bounds but do not close either row.
They sharpen the missing-inequality certificate: a uniform lift of seven on
the five queried order-54 values suffices to raise row 768 to 7070, while a
uniform lift of four on the seven queried values suffices to eliminate row
769.  Six and three, respectively, do not suffice.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd albertson_r28_separator_compression
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

Expected runtime is about fourteen seconds.  The canonical certificate digest
is

    6000d19605a542df816052cb5704fddde3590d7197143c4923ea47cd81e4eb20.

## Trust boundary

The checker uses exact Python integers, `fractions.Fraction`, deterministic
edge-set enumeration, integer partitions, and SHA-256.  It independently
checks the local separator relaxation, its symmetry orbits, every listed
profile, and the rounded convex deletion values.  It does not re-prove the
height-2569 crossing/component classification, the published crossing
inequalities, Stehlik's critical-complement theorem, or the generic deletion
recurrence.

Stehlik's primary theorem is
[Critical graphs with connected complements](https://doi.org/10.1016/S0095-8956(03)00069-8).
Targeted primary-source and committed-graph searches through 2026-09-05 found
the factor-critical and Gallai-Edmonds frameworks, but no prior statement of
this singleton-triangle separator lemma or the resulting exact `r=28`
three/eight-profile compression.  This is a search-relative novelty statement,
not a claim of historical priority.

## Conditional claims

The separator lemma itself is unconditional.  Its Albertson application is
logically conditional on the corrected height-2569 finite component
classification until that upstream result receives independent review.  No
`r=27` terminal theorem, `cr(24,132)>=165`, or local crossing conjecture is
used.
