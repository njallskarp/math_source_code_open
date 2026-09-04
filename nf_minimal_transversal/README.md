# NF facets as complements of minimal transversals

This Lean 4 project formalizes the blocker identity underlying one step of
the NF operator on a finite simplicial complex.  For a family `C` of subsets
of an ambient vertex set `V`, it defines:

- `Avoids C S`: no member of `C` is contained in `S`;
- `IsTransversal C T`: `T` meets every member of `C`;
- `IsMaximalAvoider V C S` and `IsMinimalTransversal V C T`;
- `NFFacets V C`: the maximal faces of the avoiding complex.

The main theorem is

```lean
theorem nfFacets_eq_complements_minimalTransversals
    (hC : FamilyOn V C) :
    NFFacets V C = (fun T => V \ T) '' minimalTransversals V C
```

Thus the maximal faces avoiding `C` are exactly the relative complements in
`V` of the inclusion-minimal transversals of `C`.  The proof is stronger than
the finite application: it needs no finiteness, nonemptiness, or antichain
hypothesis, so it also handles empty families and families containing the
empty set.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`.

```sh
lake update
lake exe cache get
lake clean nf_minimal_transversal
lake build NFMinimalTransversal
```

Expected final line:

```text
Build completed successfully (434 jobs).
```

The build prints axiom audits for the four exported proof theorems.  They use
only the standard Mathlib axioms `propext`, `Classical.choice`, and
`Quot.sound`.  The source declares no project axiom and contains no `sorry`,
`admit`, `native_decide`, or `unsafe` declaration.

## Theorem alignment

Hibi--Mahmood define the NF complex as the Stanley--Reisner complex of the
facet ideal.  Their Equation (2) identifies its facets with the complements
of the minimal vertex covers.  In purely combinatorial terms, membership in
that Stanley--Reisner complex means avoiding every input facet, and a vertex
cover is a transversal.  The theorem above proves exactly this complement
duality.

The independently reviewed all-width hubbed three-clique recurrence uses the
same identity to replace five startup NF computations by classifications of
minimal transversals.  This project formalizes the generic identity, not those
five family-specific classifications and not the recurrence.  Consequently
it supports, but does not by itself prove, the claimed NF number
`n + m + ell + 2`.

Discovery Net references:

- all-width theorem, height 1931:
  `bafkreifgg5ktpj5taip5bujptbthqxg5h2oprw5smkpklkhi2bvv2sfsxy`;
- independent review, height 2007:
  `bafkreidkugk5m2udkgw4lawily7byl5tkif2zbrp5wvrzrzybt5ijdc2lq`.

Primary source:

- Takayuki Hibi and Hasan Mahmood, *The NF-Number of a Simplicial
  Complex*, Algebra Colloquium 29 (2022), 73--80,
  https://arxiv.org/abs/2005.01247.

## Trust boundary

There is no external data or computation.  The formal theorem begins with an
abstract family `C` whose members lie in `V`.  Applying it to an NF complex
still requires identifying `C` with the actual facet family; applying it to
the height-1931 recurrence additionally requires the external blocker tables,
the lossless six-coordinate quotient, rank filling, and the recurrence/return
argument.  The polynomial facet-ideal and Stanley--Reisner definitions are
not encoded.
