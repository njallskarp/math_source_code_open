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
transitivity requires the exact equal-margin slice treated here.  The claim
is `mu_8=7/6`; no value for order nine or a finite formula for `m(8,k)` is
asserted.
