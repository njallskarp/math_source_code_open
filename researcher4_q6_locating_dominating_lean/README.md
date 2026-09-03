# Locating-dominating codes in finite graphs and the quadratic Q6 code

This pinned Lean project formalizes the upper-bound half of the reviewed
Discovery Net theorem `gamma^LD(Q_6) = 16` and packages both its product
mechanism and a central lower-bound family lemma as reusable finite-graph
infrastructure.

`LocatingDominating.lean` defines closed-neighborhood signatures,
locating-dominating codes, and minimum codes for finite `SimpleGraph`s. It
proves that if `C` is locating-dominating in `G`, then `C x univ` is
locating-dominating in the Cartesian graph product `G box H`.

`QuadraticCode6.lean` defines the binary Hamming cube and the exact quadratic
16-word code from Discovery Net finding
`bafkreidooxssuek4ti4xfrzlasnqg7wx3ulxdgbzfpmgf5r54b6bv6ytim`. Lean checks:

- the code has 16 words;
- it is locating-dominating in `Q_6`;
- the 48 non-codewords have 16 signatures of each size 1, 2, and 3;
- the code is independent;
- every Cartesian product lift is locating-dominating and has size
  `16 * 2^m`; and
- the published rational lower bound `288/19` forces cardinality at least 16.

`LowerBoundInfrastructure.lean` formalizes the father/son counting bridge in
the published lower bound. In any finite graph where two distinct closed
neighborhoods intersect in at most two vertices, it proves:

- signatures are injective on all sons of a father, including codeword sons;
- a son has at most one father;
- an `i`-covered father has at most `Nat.choose i 2` sons;
- family average excess is at least `5/4` for `3 <= i <= 6`; and
- the resulting specialized incidence/coverage inequalities force a `Q_6`
  code to have at least 16 words.

The exact optimality theorem is deliberately conditional on the
Honkala--Laihonen--Ranto lower bound. Lean does not formalize that paper's
complete families/couples/excess partition. The son cap, unique-father
disjointness, family-ratio arithmetic, every finite construction claim, and
the numerical specialization are checked. The elementary closed-neighborhood
intersection fact for the current `Q_6` representation remains explicit:
direct reduction through nested `Finset` filters was not a suitably small
checker, so a coordinate-level Hamming-distance proof is the next bridge.

Build and audit with:

```sh
lake clean
lake exe cache get
lake build
lake env lean LocatingDominating.lean
lake env lean LowerBoundInfrastructure.lean
lake env lean QuadraticCode6.lean
```

See `AUDIT.md` for the construction audit and `AUDIT_LOWER_BOUND.md` for the
family-infrastructure theorem alignment and exact remaining trust boundary.
