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

This is a reduction of the possible counterexample class, not a proof that
the class is empty.

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
integer bounds, cardinality estimate, nonsuspension implication, and path
escape witness.  The generalized-homology-sphere theorems of Labbé--Nevo,
Gal, and Davis--Okun are named hypotheses, not kernel axioms.  The final
three-antipode path/triangle statement uses the cited Alexander-duality input
and is documented here; Mathlib does not yet provide the required integrated
homology-sphere/link/deletion API.

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
