# Five three-cube templates for the mixed three-anchor interface

This package proves an orbit-complete classification of the signature patterns
identified by the height-2907 `R(5,5)` three-anchor limitation witness.

For three fixed anchors, consider size-five multisets in `{0,1}^3`. The
patterns that are mixed in every coordinate but contain no complementary
signature pair are exactly the five orbits below under coordinate permutations
and independent coordinate flips:

```text
triangle_heavy:     000,000,000,011,101
triangle_double:    000,000,011,011,101
star_center:        000,000,001,010,100
star_leaf:          000,000,001,011,101
parity_tetrahedron: 000,000,011,101,110
```

Their orbit sizes are `24,24,8,24,8`, totaling all 88 qualifying multisets.
Equivalently, the support is one of eight Hamming-distance-two triangles,
eight induced cube stars, or two parity tetrahedra, with the displayed
multiplicity choices.

In Ramsey terms, coordinate-mixed means that a five-set is not contained in
any one anchor neighborhood. Complement-free means that every edge is visible
in at least one of the six anchor neighborhoods. Therefore these five orbits,
with red and blue inequalities, give exactly ten invariant templates for the
complete fully visible mixed-interface cut family:

```text
1 <= sum_{uv in choose(S,2)} x_uv <= 9.
```

This is a structural classification, not a larger graph census. It explains
why two-anchor diagonal reasoning ceases to be complete at three anchors and
provides a finite invariant interface that exact searches can instantiate.
It does not assert that these cuts exclude the `d=22` family or improve a
Ramsey bound.

## Exact replay

The standard-library verifier enumerates all 792 five-multisets, constructs
the full 48-element cube action, checks orbit--stabilizer, and proves that the
five disjoint orbits equal the 88 qualifying patterns:

```sh
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | cmp - EXPECTED_OUTPUT.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py | cmp - EXPECTED_OUTPUT.json
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py \
  | cmp - EXPECTED_INDEPENDENT.json
PYTHONDONTWRITEBYTECODE=1 python3 test_verify.py | cmp - EXPECTED_CONTROLS.txt
shasum -a 256 -c SHA256SUMS
```

The independent checker does not enumerate all multisets first. It chooses
at most one endpoint from each of the four antipodal pairs, enumerates positive
compositions of five over the resulting support, and classifies by induced
cube geometry and the location of the doubled point. Both routes obtain the
full-list SHA-256

```text
2ada2c0b14a0cb3a3ba96a9dc3b06d969e30e4e6c1817fce23bec1d857a5a9c3.
```

## Trust boundary and context

The theorem has the elementary proof in `PROOF.md`; computation audits its
finite normal forms. Trusted are the short standard-library Python source,
ordinary runtime/hardware, and SHA-256 collision resistance. There is no
solver, imported graph catalog, floating-point computation, or external data.

Primary Ramsey context was checked live on 2026-09-05 against Angeltveit and
McKay, [*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709),
arXiv:2409.15709v2. No novelty is claimed for the ordinary no-monochromatic-
`K5` inequalities or the general pointed-neighborhood method; the contribution
is the exact three-anchor orbit classification and interface reduction.
