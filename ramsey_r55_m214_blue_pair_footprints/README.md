# Sharp blue-pair footprint cuts for the (M=214) branch

## Result and scope

For a red anchor pair with common-red core \(H\) of size \(c\), every blue
edge \(zz'\) outside the core satisfies

\[
|(N_R(z)\cap H)\cup(N_R(z')\cap H)|\geq c-5.
\]

The bound follows from \(R(3,3)=6\) and is sharp for every
\(c=9,\ldots,13\). Its auxiliary-free sum projection is strictly stronger
than the individual height-3228 footprint cuts exactly at \(c=9,10\), where
explicit disjoint footprint pairs also prove the projected right-hand side
sharp.

The source generates the resulting 74,958 selector-guarded rows for all 156
codegree-nine and codegree-ten roots. This is a completeness-preserving
strengthening of the single integrated (M=214) decision formula, not a
SAT/UNSAT result, solved root, Ramsey graph, or improved Ramsey-number bound.

The mathematical argument and explicit witnesses are in [PROOF.md](PROOF.md).

## Exact artifacts

```text
all roots                     389
active c=9,10 roots           156
active family counts          24,34,28,42,28
guarded pair rows             74,958
suffix bytes                  13,205,308
suffix SHA-256                a2d49a13493739d62cac8d81d43bf56b3d9c518e337304b0228c742b2485f91c
root certificate SHA-256      3d9033713e11f4109910b8de8c9ffed51de01cb61ed666a6e15e68cc762e1cf8
sharpness certificate SHA-256 d5b350c7cd7900e703ad7aeb752dd3f76351d477cef9c8396bfff215ca46beab
```

The generated suffix and full OPB are deliberately excluded from source
control. Appending the suffix to the height-3228 all-codegree formula gives:

```text
variables       13,633
constraints  2,131,051
equalities           87
lines        2,131,052
bytes      187,209,692
SHA-256 298aed6afa61eff55c21a96dae8af49d24a8c67d13d5d611e342a127c417c997
```

## Compact reproduction

With CPython 3.12 and a C++20 compiler, run from this directory:

```sh
set -o pipefail
python3 -B build.py --certificate /tmp/blue_pair_roots.tsv \
  --suffix /tmp/blue_pair_suffix.opbpart | cmp - EXPECTED_RESULT.json
cmp /tmp/blue_pair_roots.tsv roots.tsv
python3 -B -O build.py --certificate /tmp/blue_pair_roots_opt.tsv \
  --suffix /tmp/blue_pair_suffix_opt.opbpart | cmp - EXPECTED_RESULT.json
cmp /tmp/blue_pair_roots.tsv /tmp/blue_pair_roots_opt.tsv
cmp /tmp/blue_pair_suffix.opbpart /tmp/blue_pair_suffix_opt.opbpart
python3 -B test_build.py | cmp - EXPECTED_TEST_OUTPUT.txt
c++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  independent_check.cpp -o /tmp/blue_pair_check
/tmp/blue_pair_check /tmp/blue_pair_roots.tsv \
  /tmp/blue_pair_suffix.opbpart | cmp - EXPECTED_CHECK_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

The C++ checker imports no Python code or root certificate logic. It
independently enumerates the root labels, emits every suffix row byte for byte,
and verifies the cyclic sharpness, disjoint equality, and strictness witnesses
with thirteen-bit subsets.

## Full-formula reproduction

Generate the accepted height-3160 base, then the height-3228 all-codegree
formula using their adjacent public source directories:

```sh
python3 -B ../ramsey_r55_m214_integrated_pair_roots/generate_opb.py \
  --output /tmp/m214_height3160.opb
python3 -B ../ramsey_r55_m214_all_c_footprint_bound/build.py \
  --prior-opb /tmp/m214_height3160.opb \
  --output-opb /tmp/m214_height3228.opb
python3 -B build.py --certificate /tmp/blue_pair_roots.tsv \
  --suffix /tmp/blue_pair_suffix.opbpart \
  --prior-opb /tmp/m214_height3228.opb \
  --output-opb /tmp/m214_blue_pair.opb
/tmp/blue_pair_check /tmp/blue_pair_roots.tsv \
  /tmp/blue_pair_suffix.opbpart /tmp/m214_height3228.opb \
  /tmp/m214_blue_pair.opb | cmp - EXPECTED_FULL_CHECK_OUTPUT.txt
shasum -a 256 /tmp/m214_blue_pair.opb
```

The final hash must equal `formula_manifest.json`.

## Validation and trust boundary

Normal and optimized Python output is byte-identical. The semantic tests
inspect all 74,958 rows, all 903 edge identifiers, all 160 guard truth
assignments, five sharp union cases, two sharp projected cases, two strictness
witnesses, and eight corruptions. Strict C++20, AddressSanitizer,
UndefinedBehaviorSanitizer, and complete prior-to-strengthened stream
comparison pass.

The union theorem uses only the elementary equality \(R(3,3)=6\), whose short
proof is included. Formula completeness trusts the height-3148 root cover,
the independently accepted height-3160 selector semantics, and the published
height-3228 individual-footprint source and formula identity. Trusted remain
the displayed proof, exact source/language semantics, hardware, and SHA-256.
The implementations are author-written cross-checks, not peer review or formal
proof. No solver status, large generated formula, private state, or raw search
dump is evidence.

For historical context only: F. P. Ramsey,
[On a Problem of Formal Logic](https://doi.org/10.1112/plms/s2-30.1.264),
Proceedings of the London Mathematical Society s2-30 (1930), 264–286. No
priority claim is made for the elementary exterior-pair argument.

## Stopping condition

The pair-cardinality mechanism is complete: its exact union bound is sharp,
and its auxiliary-free projection is redundant for (c\geq11). Further
cardinality variants are frozen. A stronger continuation must use actual core
adjacency, cell capacities, or a different exact certificate mechanism. The
whole (M=214) branch remains undecided pending a checked graph or replayable
UNSAT proof.
