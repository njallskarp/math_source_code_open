# Polar-size-three reduction at the 17-vertex boundary

## Exact conditional theorem

Let `Delta` be a flag generalized homology 5-sphere on 17 vertices.  If
`gamma_3(Delta) < 0`, then all of the following hold.

1. Its polar size is exactly `pi(Delta) = 3`.
2. Every vertex has between three and six antipodes, hence degree between 10
   and 13.
3. `1 <= gamma_2(Delta) <= 5` and `-6 <= gamma_3(Delta) <= -1`.
4. At least eight vertices have exactly three antipodes.
5. For every such vertex `v`, its 13-vertex flag homology 4-sphere link has
   `gamma_1(link(v)) = 3`, `0 <= gamma_2(link(v)) <= 2`, and is not a
   suspension.
6. The three antipodes of `v` induce either a path or a filled 2-simplex.

The complement face-count identity sharpens items 3--4 to the exact profile

```text
gamma_2(Delta) = 5,                  gamma_3(Delta) = -6,
degrees in the complement = 3^16 4^1,
number of complement triangles = 0,
sum_v gamma_2(link(v)) = 2.                                      (3)
```

These necessary conditions are inconsistent: the unique complement-degree-
four vertex has a 12-vertex link with `gamma_2=-2`, contradicting the known
nonnegativity for flag homology 4-spheres. Thus the argument closes the
17-vertex boundary, subject only to the cited topological inputs.

## Proof and source dependencies

Write `17 = 2d + ell` with `d = 6` and `ell = 5`, and let `iota(v)` be the
number of antipodes of `v`.

Labbé--Nevo Lemma 3.2 gives `1 <= pi <= 6`,
`gamma_1(link(v)) = 6 - iota(v)`, the suspension characterization at
`pi = 1`, and the octahedral characterization at `pi = 6`.  The last case is
impossible because `ell = 5`, not zero.  At `pi = 2`, their Lemma 3.4 supplies
an edge not contained in an induced four-cycle, while the previously
formalized admissible-edge reduction makes `gamma_3` nonnegative.  Finally,
their Corollary 4.3 says that, when `pi >= 4`, all `gamma_j` with
`j >= ell - pi + 2` vanish; in particular `gamma_3 = 0`.  Thus a negative
example has `pi = 3` exactly.

Gal's nonnegativity result in dimensions below five makes every
`gamma_2(link(v))` nonnegative.  The standard vertex-link identity

```text
sum_v h_link(v)(t) = 6 h_Delta(t) + (1-t) h'_Delta(t)
```

can be differentiated at `t = -1`.  In the gamma basis it gives

```text
sum_v gamma_2(link(v)) = 3 gamma_3(Delta) + 4 gamma_2(Delta).       (1)
```

Lean proves this extraction directly from the polynomial identity.  Since the
left side of (1) is nonnegative, negativity of `gamma_3` forces
`gamma_2 >= 1`.

Labbé--Nevo Lemma 2.2 and the antipode count give

```text
sum_v iota(v) = 62 - 2 gamma_2(Delta).                              (2)
```

Every `iota(v)` is at least three, so (2) gives `gamma_2 <= 5`.  Moreover,

```text
sum_v (iota(v)-3) = 11 - 2 gamma_2(Delta) <= 9.
```

Every vertex with more than three antipodes contributes at least one to this
sum.  Therefore at most nine vertices have more than three antipodes, and at
least eight attain the minimum three.  Equation (1) and `gamma_2 <= 5` also
give `gamma_3 >= -6`.

## Exact complement rigidity

Let `H` be the complement of the one-skeleton, let `q_v = iota(v)` be its
degrees, let `m` be its number of edges, and let `T` be its number of
triangles. Inclusion--exclusion on triples gives

```text
f_2(Delta) = C(17,3) - 15m + sum_v C(q_v,2) - T.
```

Indeed, each complement edge spoils 15 triples, pairs of complement edges in
a triple are restored through their common vertex, and exactly the
three-edge complement triangles must be removed once more. Comparing the
coefficient of `t^3` in the degree-six h-polynomial with its gamma expansion,
and using `m = 31-gamma_2`, gives

```text
2 gamma_3 = 348 + sum_v q_v(q_v-10) - 2T.                         (4)
```

For `3 <= q_v <= 6`, every summand in (4) is at most `-21`. Equation (2)
and `gamma_2 <= 5` imply `sum q_v >= 52`, so at least one degree exceeds
three and its summand is at most `-24`. Hence `gamma_3 <= -6`. The earlier
lower bound makes equality compulsory. Then (1) forces `gamma_2 = 5`, so
`sum(q_v-3)=1`: exactly one complement degree is four and the other sixteen
are three. Their summands total `-360`; (4) forces `T=0`, and (1) leaves
total link `gamma_2` equal to two.

Lean theorem `negative_forces_rigid_complement_profile` checks this entire
integer squeeze from the named missing-edge, vertex-link, and complement-
triangle identities. In particular, the degree classification and the
vanishing of `T` are kernel checked; the face-count derivation of (4) remains
the explicit human-auditable combinatorial input.

## Closing contradiction at the degree-four vertex

Let `r` be the unique vertex of degree four in `H`, and let `N=N_H(r)`.
Triangle-freeness makes `N` independent. Every vertex in `N` has complement
degree three, so after its edge to `r` it has exactly two edges into
`B=V(H)\(N union {r})`. The 26 complement edges therefore split as

```text
4 edges from r to N + 4*2 edges from N to B + 14 edges within B.
```

The link of `r` in `Delta=Ind(H)` is the flag complex on the 12 vertices of
`B`; the complement of its one-skeleton is exactly `H[B]`. It consequently
has `C(12,2)-14=52` edges. For its degree-five h-polynomial,

```text
h_2 = 52 - 4*12 + 10 = 14,
h_2 = 10 + 3 gamma_1 + gamma_2,
gamma_1 = 12 - 10 = 2.
```

Hence `gamma_2(link_Delta(r))=-2`, contradicting Gal's nonnegativity theorem
for flag generalized homology 4-spheres. Therefore no negative 17-vertex
counterexample exists and `gamma_3(Delta)>=0`.

Lean theorem `degreeFour_linkGammaTwo_eq_negTwo` checks the edge-count-to-
gamma conversion. The theorem
`negative_counterexample_impossible_from_degreeFour_link` combines that local
count with the full rigid-profile theorem and the link nonnegativity premise
to derive `False`.

For a minimum-antipode vertex, `gamma_1(link(v)) = 3`.  The real-root
inequality used by Zheng for four-dimensional flag homology-sphere links is

```text
4 gamma_2(link(v)) <= gamma_1(link(v))^2.
```

Together with integrality and nonnegativity this yields
`0 <= gamma_2(link(v)) <= 2`.

If such a link were a suspension over a flag homology 3-sphere `Gamma`,
Labbé--Nevo Theorem 3.5 would give
`Delta = Gamma * C_6`.  Multiplicativity of gamma-polynomials and the
Davis--Okun theorem would then give
`gamma_3(Delta) = 2 gamma_2(Gamma) >= 0`.  Thus every one of the at least
eight minimum-antipode links is a nonsuspension.

Lastly, Labbé--Nevo Lemma 2.1(iv) applied to the equator `link(v)` says that
its deletion has the reduced homology of a 0-sphere.  Its vertices are the
isolated vertex `v` and its three antipodes.  Hence the induced complex on the
three antipodes is connected.  A connected flag complex on three vertices is
either a path or a filled 2-simplex.

## Exact failure of the direct `pi = 3` contraction argument

The two-antipode proof does not imply that three antipodes force an admissible
edge.

If the antipodes induce the path `x-y-z`, then for the antipode edge `xy` the
equator argument excludes induced four-cycles which avoid `z`; it does not
exclude the escape cycle

```text
x - y - z - w - x,
```

where `w` lies in `link(v)`, is adjacent to `x` and `z`, and is nonadjacent to
`y`.  The no-axiom Lean theorem
`pathAntipodes_force_link_escapeWitness` checks that this witness is forced by
contraction irreducibility once the separator conclusion for cycles avoiding
`z` is supplied.

If the antipodes form a filled triangle, the obstruction is earlier and more
fundamental: for an antipode edge `xy`, its link contains the third antipode
`z`, while `z` is not in `link(v)`.  Thus `link(xy)` is not a subcomplex of
`link(v)` and cannot be used as the equator in the published two-antipode
Jordan--Alexander argument.

The next proof obligation is therefore sharply delimited: eliminate either
the path escape configuration or the triangle configuration by additional
homological incidence information.  Merely repeating the two-antipode
separator proof omits exactly this obligation.

## Formal trust boundary

`CharneyDavisPolarReduction.lean` contains no `sorry`, `admit`, custom axiom,
`unsafe`, or `native_decide`.  Lean checks the polynomial differentiation,
integer bounds, exact complement-degree/triangle rigidity, the final
degree-four link contradiction, cardinality estimate, nonsuspension
implication, and path escape witness.  The
generalized-homology-sphere theorems of Labbé--Nevo,
Gal, and Davis--Okun are named hypotheses, not kernel axioms.  The final
three-antipode path/triangle statement uses the cited Alexander-duality input
and is documented here; Mathlib does not yet provide the required integrated
homology-sphere/link/deletion API.

The graph incidence facts used to obtain the displayed 14-edge link count are
proved directly above but are passed to Lean as an equality. Thus Lean checks
the algebraic implication and contradiction, while a future fully internal
formalization would still need finite simplicial complexes, links, complement
graphs, and the cited homology-sphere preservation/results inside Mathlib.

## Primary sources

- J.-P. Labbé and E. Nevo, *Bounds for entries of gamma-vectors of flag
  homology spheres*, especially Lemmas 2.1, 2.2, 3.2, 3.4, Theorem 3.5, and
  Corollary 4.3: <https://arxiv.org/abs/1612.01169>
- S. R. Gal, *Real Root Conjecture fails for five and higher dimensional
  spheres*, especially Corollaries 2.2.2--2.2.3:
  <https://arxiv.org/abs/math/0501046>
- M. Davis and B. Okun, *Vanishing theorems and conjectures for the
  L2-homology of right-angled Coxeter groups*:
  <https://arxiv.org/abs/math/0102104>
- H. Zheng, *The upper bound theorem for flag homology 5-manifolds*, whose
  proof of Theorem 3.6 records the four-dimensional link real-root inequality:
  <https://arxiv.org/abs/1805.09179>

## Novelty status

The cited ingredients are established results.  The combined 17-vertex
coefficient/count reduction and its Lean package were not found stated in
this form in the searched primary sources or Discovery Net.  This is a
search-relative novelty statement, not a priority claim.
