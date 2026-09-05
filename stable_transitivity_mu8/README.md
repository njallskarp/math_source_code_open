# Exact stable-transitivity growth at order eight

This directory proves

    mu_8 = lim_(k -> infinity) m(8,k)/k = 7/6.

It bridges the affine semigroup of transitive-tournament decompositions to an
equal-margin variant of tournament predictability.  All 96 order-eight
one-summand obstructions have exact equal-margin predictability `13/20` and
stable rate `7/6`; every other nontransitive order-eight class has rate one.

The mathematical proof is in `THEOREM.md`.  The compact certificate contains
2,464 rationally weighted orders and one 20-arc dual obstruction for each of
the 96 classes.

The companion theorem `M6_THEOREM.md` strengthens this on the integral
semigroup.  A single canonical 20-arc partial tournament `G8` has exactly the
96 obstruction classes as its completion classes, and every completion `T`
satisfies

    m(6q T) = 7q  for every q>=1.

Thus every exceptional ray attains its asymptotic slope at scale six.

The final theorem `ALL_RAYS_THEOREM.md` determines the complete integral
growth along every exceptional ray:

    m(k T) = ceil(7k/6)  for every k>=1.

The new certificate supplies square-free sharp profiles for the four missing
residues `k=2,3,4,5`; addition of the scale-six profile proves all parameters.

## Verify

The correctness-boundary command uses only the Python standard library and
exact integer/rational arithmetic:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_certificate.py
    diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_certificate.py)
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
    shasum -a 256 -c SHA256SUMS

Expected summary:

    classes=96
    orders=40320
    dual_order_checks=3870720
    primal_terms=2464
    maximum_denominator=3940
    equal_margin=13/20
    stable_rate=7/6
    audit_sha256=968e123eaddbf7b227e7c8868512b06d128dbba020696fe5894bc09a09ee40fb

Recorded verification used CPython 3.12.12 on macOS.  No solver, randomness,
floating point, or external data is used by the verifier.

Verify the integral scale-six theorem with:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_m6.py
    diff -u EXPECTED_M6_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_m6.py)
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_m6.py

Its final lines are:

    exact_ray=m(6qT)=7q_for_all_q>=1
    audit_sha256=37a66ffb38a906c3f500306bc30207045533b1b6347574a20ec6a2abadb38a3a

Verify the complete exceptional-ray theorem with:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_residues.py
    diff -u EXPECTED_RESIDUE_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_residues.py)
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_residues.py

Its final lines are:

    residue_values=m(dT)=d+1_for_d=2,3,4,5
    exact_rays=m(kT)=ceil(7k/6)_using_d1_and_d6_dependencies
    audit_sha256=e5606e70fb271a9dc797728dd5fc3dbdd42a639585af55086aae83518e939851

## Regenerate

The deterministic certificate generator uses NumPy 2.5.2 and SciPy 1.18.1
(including HiGHS):

    UV_CACHE_DIR=/tmp/stable-mu8-uv-cache \
      uv run --with-requirements requirements.txt \
      python generate_certificate.py

Generation solves 96 LPs.  Each floating solution is reconstructed as
`fractions.Fraction` with denominator at most 100,000 and definition-checked
exactly before it is written.  Regeneration is useful provenance but is not
part of the proof trust boundary; `verify_certificate.py` independently
rebuilds the 40,320 orders and checks the committed rational witnesses.

The integral profiles and compact isomorphism maps can be regenerated with:

    UV_CACHE_DIR=/tmp/stable-mu8-uv-cache \
      uv run --with-requirements requirements.txt \
      python generate_m6_profiles.py
    PYTHONDONTWRITEBYTECODE=1 python3 generate_g8_maps.py

The MILP generator is discovery-only.  `verify_m6.py` independently decodes
the resulting integer profiles and permutation maps using a separate
definition-level implementation.

Regenerate the 384 square-free residue profiles serially with:

    UV_CACHE_DIR=/tmp/stable-mu8-uv-cache \
      uv run --with-requirements requirements.txt \
      python generate_residue_profiles.py

The generator also accepts half-open `--class-start` and `--class-stop`
ranges for deterministic parallel shards.  Merge a complete partition with:

    PYTHONDONTWRITEBYTECODE=1 python3 merge_residue_shards.py \
      --output residue_profiles.txt /tmp/residue-shard-*.txt

The recorded production run used eight disjoint 12-class shards.  A
post-cleanup regeneration of the first complete class was byte-identical to
the corresponding four certificate rows.  HiGHS is used only to discover
binary witnesses; `verify_residues.py` uses a separately implemented direct
order-mask enumeration and standard-library integer arithmetic.

## Input provenance

`obstructions.txt` was extracted from the independently reviewed order-eight
classification certificate `cert_n8_m01.txt`, SHA-256
`7db0569ad5ce8c0f150696272d80e09712d8da684da90e4c96e0b4403d763d38`,
at:

https://github.com/helgithorskarp/math_results/tree/main/graph_theory/stable_tournaments_order8

The corresponding Discovery Net theorem is at height 1669 and its
independent accepting review at height 1675.  This package relies on that
classification only to know that the displayed 96 masks exhaust the
exceptional isomorphism classes; it checks the new equal-margin claims for
every displayed mask directly.

## Primary sources and scope

- Matthew Davis and Michael W. Schroeder, *Relating tournaments and
  permutations with xrays*, arXiv:2606.21532v1 (2026):
  https://arxiv.org/abs/2606.21532v1
- Leonid Chindelevitch and Ararat Harutyunyan, *Tournaments determined by
  three and five voters*, arXiv:2607.26690v1 (2026):
  https://arxiv.org/abs/2607.26690v1

The second source gives the ordinary predictability minimax LP and identifies
the common 20-arc `G_8` obstacle at value `13/20`.  Ordinary predictability
only asks every arc probability to be *at least* a threshold.  Stable
transitivity requires the exact equal-margin slice treated here.  This
package proves `mu_8=7/6` and the exact formula on each of the 96 exceptional
ordinary-tournament rays.  It does not claim a finite formula for the maximum
`m(8,k)` over arbitrary mixtures of ordinary layer types, nor any value at
order nine.
