# A sharp common-core footprint bound for every \(M=214\) pair root

## Result and scope

This directory proves a uniform all-root attachment constraint for the
complete \(M=214\) branch of a hypothetical Ramsey \((5,5;43)\) graph.

For a selected red-adjacent anchor pair \(u,v\), let

\[
H=N_R(u)\cap N_R(v),\qquad |H|=c\in\{9,\ldots,13\}.
\]

Every vertex \(z\notin H\cup\{u,v\}\) has at least \(c-8\) red neighbors
in \(H\). More strongly, its red footprint meets every red-independent
four-set of \(H\). The cardinality bound is sharp for every admitted value of
\(c\), using one explicit nested family inside the cyclic thirteen-vertex
Ramsey graph.

Applying the bound to all 389 roots of the independently accepted
height-3160 integrated formula gives 11,672 selector-guarded rows. This is a
completeness-preserving strengthening of one complete decision instance, not
a selected-core enumeration, SAT/UNSAT result, root exclusion, Ramsey graph,
or improved Ramsey-number bound.

The full proof is in [PROOF.md](PROOF.md).

## Exact artifacts

`build.py` independently enumerates the 389 root keys, writes the compact
`roots.tsv` certificate, and generates the omitted OPB suffix. The suffix is
generated state rather than repository content.

```text
roots                         389
root counts by c              78,78,78,78,77
footprint lower bounds        1,2,3,4,5
guarded suffix rows           11,672
suffix bytes                  1,215,392
suffix SHA-256                ff2e24eaf16cc07435ef53b651474d812ad600ac403660722e60e6ebddd20ff1
root certificate SHA-256      d50e8ba32f31acdbe707da9779ecfb8bf57d65b310a74f369dc6cc76248ad8a7
sharpness certificate SHA-256 5d586c6e635f6ccd2646df2c12a7f06a7556a69679bc5da4dab559f449518136
```

Appending the suffix to the exact height-3160 formula produces:

```text
variables       13,633
constraints  2,056,093
equalities           87
lines        2,056,094
bytes      174,004,384
SHA-256 e8ac0385c3654aa6106922bcb32d0e19832b6e8331a17d9aa55b44f7f3a8747a
```

The 174 MB formula is operational generated state and is deliberately not
committed. Its exact provenance and dimensions are in
`formula_manifest.json`.

## Compact reproduction

With CPython 3.12 and a C++20 compiler, run from this directory:

```sh
set -o pipefail
python3 -B build.py --certificate /tmp/all_c_roots.tsv \
  --suffix /tmp/all_c_suffix.opbpart | cmp - EXPECTED_RESULT.json
cmp /tmp/all_c_roots.tsv roots.tsv
python3 -B -O build.py --certificate /tmp/all_c_roots_opt.tsv \
  --suffix /tmp/all_c_suffix_opt.opbpart | cmp - EXPECTED_RESULT.json
cmp /tmp/all_c_roots.tsv /tmp/all_c_roots_opt.tsv
cmp /tmp/all_c_suffix.opbpart /tmp/all_c_suffix_opt.opbpart
python3 -B test_build.py | cmp - EXPECTED_TEST_OUTPUT.txt
c++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  independent_check.cpp -o /tmp/all_c_check
/tmp/all_c_check /tmp/all_c_roots.tsv /tmp/all_c_suffix.opbpart \
  | cmp - EXPECTED_CHECK_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

The C++ checker imports no Python module or certificate logic. It independently
enumerates the root keys and labeled common cores, re-emits the 11,672 rows
byte for byte, and separately verifies the cyclic sharpness family.

## Full-formula reproduction

First generate the accepted height-3160 formula with its
[public source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_integrated_pair_roots):

```sh
python3 -B ../ramsey_r55_m214_integrated_pair_roots/generate_opb.py \
  --output /tmp/m214_height3160.opb
python3 -B build.py --certificate /tmp/all_c_roots.tsv \
  --suffix /tmp/all_c_suffix.opbpart \
  --prior-opb /tmp/m214_height3160.opb \
  --output-opb /tmp/m214_all_c_footprints.opb
/tmp/all_c_check /tmp/all_c_roots.tsv /tmp/all_c_suffix.opbpart \
  /tmp/m214_height3160.opb /tmp/m214_all_c_footprints.opb \
  | cmp - EXPECTED_FULL_CHECK_OUTPUT.txt
shasum -a 256 /tmp/m214_all_c_footprints.opb
```

The final hash must equal the value in `formula_manifest.json`.

## Validation and trust boundary

Normal and optimized Python produce byte-identical artifacts. The independent
C++20 implementation passes strict compilation, AddressSanitizer, and
UndefinedBehaviorSanitizer. The semantic tests check all 11,672 generated
rows, all 903 edge-variable identifiers, all 120 guard truth assignments,
15 sharpness deletion controls, and eight corrupted artifacts. Both C++
layers are source-independent: the accepted base checker reconstructs its
formula, while this checker re-emits the new suffix and compares the complete
base-to-strengthened stream.

The universal proof trusts the classical equality \(R(3,4)=9\), established
by Greenwood and Gleason in
[Combinatorial Relations and Chromatic Graphs](https://doi.org/10.4153/CJM-1955-001-4).
Formula completeness trusts the height-3148 root theorem and the independently
accepted height-3160 selector semantics. The explicit sharpness family is
checked directly and does not trust a graph catalog or classification.

Trusted remain the displayed proof, exact source and language semantics,
ordinary hardware, and SHA-256 collision resistance. The two implementations
are author-written cross-checks, not external peer review or proof-assistant
formalization. No solver status, generated full formula, private state, or raw
search dump is evidence.

## Relationship to adjacent work

The codegree-thirteen result at Discovery Net height 2823 proved the stronger
complete three-orbit footprint classification for the unique thirteen-vertex
core. The present result generalizes its catalog-free cardinality argument to
all five codegrees and every one of the 389 roots; it does not reproduce that
classification. Height 3192's third-anchor quotient is compatible with these
rows but is not a premise and remains independently reviewable.

The next terminal milestone remains a directly checked 903-edge model or a
standard replayable UNSAT certificate for one complete integrated formula.
