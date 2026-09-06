# Defect-compatible pairs in the full M215 profile-B branch

A high-codegree doubly exact pair can always be selected with both
endpoints blue to the degree-19 vertex $z$ and with equal colors to the
degree-20 defect $y$. All four intrinsic defect cases and both pair
colors are covered. There are at least two vertex-disjoint compatible
pairs; when $z$ is defective there are at least three.

The new mechanism is a sharp uniform-signature lemma: nine degree-21
vertices sharing two external adjacency patterns force same-edge-color
codegree at least ten. An explicit eight-vertex witness shows the
threshold is sharp under those hypotheses. A second-star moment bound
strictly separates a named scalar/PSD projection. It is not a survivor
or separator of the complete Ramsey formula or researcher 1's LP.

[PROOF.md](PROOF.md) proves the pair theorem, the stronger same-color
moment bound, the $3,5,7$ multiplicity table, and exact composition of
720 marked-cell formulas. No backend is emitted or solved; no entire
degree profile or $M$ slice is excluded. The common core remains
variable, with all 820 non-anchor physical edges retained.

## Reproduce

From this directory, with CPython 3.11 or newer and the standard library
only (tested with CPython 3.12.12):

~~~sh
set -eu
set -o pipefail
python3 -B build.py | cmp - EXPECTED_OUTPUT.json
python3 -B check.py | cmp - EXPECTED_CHECK.json
python3 -B test_semantics.py | cmp - EXPECTED_SEMANTICS.json
python3 -B -O build.py | cmp - EXPECTED_OUTPUT.json
python3 -B -O check.py | cmp - EXPECTED_CHECK.json
python3 -B -O test_semantics.py | cmp - EXPECTED_SEMANTICS.json
shasum -a 256 -c SHA256SUMS
~~~

To regenerate the compact certificate without modifying the repository:

~~~sh
python3 -B build.py --write /tmp/m215-defect-pair-certificate.json
cmp /tmp/m215-defect-pair-certificate.json certificate.json
~~~

Expected: nine-vertex pair sum at least 328 versus 324 if every pair
had codegree at most nine; 720 marked-cell keys; compatible-pair
multiplicities $3,5,7$ and matching sizes $2,2,3$ for blue-to-$z$
exact sets of sizes $19,20,21$.

Certificate SHA-256:
9dcb80ade7e904b4849094a0bbf2cfed7e07ea0aa5c07ee44752d30824e3afaa.

The independent checker imports no producer. It obtains all 44 bound
rows by balancing integer incidence lists at each internal edge total,
reconstructs all 720 keys through a different enumeration, verifies the
sharpness graph and the exact scalar PSD separator, and rejects three
damaged certificates. Semantic controls cover 13,012 uniform-star
subsets in 1,032 small graphs and 720 complete marked edge transports
(650,160 physical pairs), including 720 damaged-star controls.

The sharpness graph has eight balanced vertices and independent outside
vertices; it is not a Ramsey or profile-B graph. The scalar separator
has no asserted graph realization. The arbitrary edge-transport controls
are implementation checks, not feasibility witnesses.

## Trust and composition

The displayed proofs are unformalized and the checks are author-written.
The Ramsey application inherits the reviewed local extrema and
$R(4,5)=25$. The uniform-signature bound, sharpness graph, and scalar
separator need no catalog or solver. No private state, external download,
floating-point computation, omitted large artifact, or generated SAT
formula is needed for replay.

The new pair is selected before an anchor normalization. It retains
the 12 raw single-anchor B keys with the anchor blue to $z$; it does
not prove that the other 12 cannot occur at other anchors. Preserve
both colors at $y$, both pair colors, all four central-defect cells,
and every shared edge. Keep the original sparse-red total 446 when
the selected pair is blue.
