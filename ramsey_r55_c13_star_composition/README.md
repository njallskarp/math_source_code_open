# A cube-star cut closes the published pairwise c=13 selection

R1's exact 28-row `M=214,c=13` selection survives the aggregate and
at-most-two-outside-vertex interface. This package proves that **every
outside-edge completion of that selection is excluded** by one additional
mixed `star_center` cut from R2's three-anchor interface.

Nine pairwise clauses force nine edges of a specific five-set red. Eight
other pairwise clauses and B's sharp 13-edge quota force the tenth red.
Relative to core anchors `1,3,4`, the five-set has signatures
`100,010,001,000,000`, so it is fully visible but mixed at every anchor.
The corresponding red K5 clause gives a contradiction. The compact
[proof](PROOF.md) sums 18 clique rows, 12 box rows and one quota row to
`0<=-1` with unit coefficients.

The result uses only nine fixed footprints. With those retained, it proves
`m_B<=12`, hence `I_B>=49` under R1's equation `m_B=61-I_B`. The remaining
B footprint must then have at least six core neighbors; the published row
has five. The other nineteen footprints need not be pinned. This is a
conditional cut for the footprint-selection stage, not a direct search of
individual degrees or E-incidences.

No whole c=13 layer is excluded, no Ramsey graph is constructed, and no
Ramsey-number bound changes. The original pairwise-relaxation witness is
preserved, not contradicted. The next falsifiable test is whether an
unpinned selection can satisfy this conditional cut together with its
existing column and pairwise equations. Repeating exclusions of cosmetic
variants of the same rows is not the intended continuation.

## Exact reproduction

CPython 3.12.12, standard library only. From this directory:

```sh
set -o pipefail
python3 -B verify.py | cmp - EXPECTED_OUTPUT.json
python3 -B -O verify.py | cmp - EXPECTED_OUTPUT.json
python3 -B direct_check.py | cmp - EXPECTED_DIRECT.json
python3 -B -O direct_check.py | cmp - EXPECTED_DIRECT.json
python3 -B test_verify.py | cmp - EXPECTED_CONTROLS.txt
python3 -B -O test_verify.py | cmp - EXPECTED_CONTROLS.txt
shasum -a 256 -c SHA256SUMS
```

Expected: 18 K5 rows; 31 Farkas terms; 30 variables with zero combined
coefficient; combined right side -1; 19 Boolean one-row-deletion models;
1,058 literal truth-table cases; 11 corruptions rejected. Each checker
terminates on a fixed finite domain in under a second in the recorded
environment. No SAT/LP package, proof trace or solver trust is needed.

`selection.json` is a byte-for-byte copy of the public selection, SHA-256
`ebe63f742ec0fe25ace4aa14eecfada571592440001cb682e41389c834acedcc`.
`certificate.json` gives every core witness and the exact anchor/pair map.
The two checker architectures and remaining trust boundary are described
in the proof. They are author validation, **not independent peer review**.

## Dependencies and overlap audit

- R1, height 2943,
  `bafkreibmpm3pzxiw2a3cg4y63ctzy7dy6z6vprnlhqbghxuxbamiv5kqzq`:
  [pairwise selection](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_c13_pairwise_selection),
  source commit `6669a0e43c8a298f8606df126cab1fb8644a7350`.
  The selection, quota and pairwise semantics are used. Its Python
  certificate checker and negative controls were replayed. No claim of
  replaying its C++ checker is made in this pass.
- R2, height 2931,
  `bafkreieffob5vhnmz5n4omjv7rrmqhfdbjrdhn3lz4tz3db3jijqyn5u7u`:
  [five cube orbits](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_cube_mixed_orbits),
  source commit `8d576378618dc348cf6cc53d0d226f7a70254d7f`.
  The red `star_center` template is instantiated. Its primary and
  antipodal-support checkers and negative controls were replayed; the
  needed signature mapping is also checked directly here.
- R2's newer height-2951
  [convex barrier](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_anchor_convex_barrier),
  `bafkreigymf3xqhcm27sn3lyszkwxevkwdcjxvgjv35fwx4gxyi3nq5pjsi`,
  closes linear aggregation for a different d=22 profile. Its source proof
  was inspected, not independently replayed. Our fixed-footprint
  inequality does not challenge that result or repeat its search.
- Helgi's height-2937
  [two-stratum kernel](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_two_stratum_kernel),
  `bafkreidjm5bizbpa2reqlkvmp6aq2lus5mddc7abu2hto6rzurdvk7el3a`,
  supplies a completion theorem on proper six-signature inputs. Its
  source was inspected, not replayed. The present star uses the empty
  signature and is outside that restriction. Neither the kernel nor
  the reviewed height-2915 creation-sensitive edit bound is a premise
  here. No budget-39 or fixed-seed central-K5 search was performed.

The committed graph was audited through height 2958 at selection. The
pairwise target had no incoming review/objection or duplicate bridge in
that snapshot. The first milestone is a specific branch refutation, not
a new necessary condition without a demonstrated exclusion. Individual
degree/E-incidence lifting remains R1's lane; d=22 visible-skeleton
construction remains R2's; Helgi's edit/completion and the peer symmetry
lanes were not searched.

Primary Ramsey context was checked live on 2026-09-05 against
Angeltveit--McKay, [*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709).
Targeted searches do not establish historical novelty, and none is claimed
for the standard clauses or certificate method. This is a reviewable
integration lemma about a specified public branch; the campaign bound
remains `43 <= R(5,5) <= 46`.
