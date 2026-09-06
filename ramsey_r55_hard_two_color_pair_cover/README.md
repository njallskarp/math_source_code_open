# Whole-hard-branch two-color exact pairs

Every 15 degree-21 vertices in any graph on 43 vertices contain a pair
with at least ten common neighbors in the color of that pair. A short
signed-row proof and an independent degree-moment derivation are in
[PROOF.md](PROOF.md).

Combined with the reviewed hard local-deficiency budget, every hypothetical
hard-branch $(5,5;43)$ coloring has at least 16 doubly exact pairs with
same-color codegree $10..13$. This gives a complete 56-family cover over
all $M=214..220$, both pair colors, and all four codegrees. The proof
specifies the complete finite formulas and their physical edge lift.
It does not generate or decide a Boolean backend or exclude an entire
$M$ slice. Optional historical core catalogs give 6034 unmarked core
templates, subject to their separate completeness boundary.

## Reproduction

Run from this directory with CPython 3.11 or newer, standard library only
(tested with CPython 3.12.12):

```sh
set -eu
set -o pipefail
python3 -B build.py | cmp - EXPECTED_OUTPUT.json
python3 -B check.py | cmp - EXPECTED_CHECK.json
python3 -B test_semantics.py | cmp - EXPECTED_SEMANTICS.json
python3 -B -O build.py | cmp - EXPECTED_OUTPUT.json
python3 -B -O check.py | cmp - EXPECTED_CHECK.json
python3 -B -O test_semantics.py | cmp - EXPECTED_SEMANTICS.json
shasum -a 256 -c SHA256SUMS
```

To reconstruct the certificate without changing the checked-in file:

```sh
python3 -B build.py --write /tmp/ramsey-hard-pair-certificate.json
cmp /tmp/ramsey-hard-pair-certificate.json certificate.json
```

Expected headline values: 949 as the 15-vertex pair-sum lower bound,
945 if all pairs had codegree at most nine, 16 forced high pairs in any
22 exact anchors, 56 scalar roots, and 6034 optional unmarked core
templates. Certificate SHA-256:
`92af1173b28d905d808ef40cac1dd644ceb60b7569b478f5681f873e97fe6572`.

`build.py` uses the Gram/parity bound. `check.py` does not import it and
recovers all 28 bound entries by exact integer minimization of balanced
degree lists at every internal edge count. It reconstructs all 56 roots,
rejects three damaged certificates, and checks the pair identity on every
balanced subset of every graph of orders 1,3,5 and of the Paley graph of
order 13: 13,226 subsets and 163,410 literal pair evaluations.

`test_semantics.py` compares the two representations, checks all 104
**unfiltered** hard degree-budget profiles, and includes a degree-only
blue-pair control. The 104 count precedes triangle-divisibility and later
local screens; it must not replace the cumulative 66-profile count.

The explicit 43-vertex fixture has degree profile $19^1 20^9 21^{33}$
and 446 red edges. It tests 267 full edge transports spanning both colors
and all four codegrees, including every unpinned shared edge. It contains
a monochromatic five-set, explicitly located by the checker, so it is
**not a Ramsey graph, hard-branch witness, or counterexample to a Ramsey
claim**. It is a concrete transport control. A second control, $K_{21,22}$,
shows that the degree-only lemma cannot silently demand a red pair;
that graph is also outside the Ramsey domain.

These are author-written exact checks, not independent peer review or a
formal proof. The optional core counts are imported metadata, not
re-enumerated catalogs. The exact local extrema and $R(4,5)=25$ used
to reach the hard branch remain upstream inputs. No solver, floating
point, external data download, private state, or large artifact is needed
for replay.

## Composition warning

The pair may be blue while the globally sparser color stays red. Its
normalization preserves the original $M$. The earlier red-only
$M=214$ cover cannot drop codegree-nine cases based on this theorem.
For $M=215$, choose the qualifying pair before an anchor normalization,
or use the complete raw 674-root cover; the earlier optional minimum
single-anchor comparator is not proved compatible with this pair choice.
