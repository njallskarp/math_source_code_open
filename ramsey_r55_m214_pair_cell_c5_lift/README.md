# Exact pair-cell \(C_5\) lift for the \(M=214\) branch

## Result and scope

This directory gives a complete, shared-variable extended formulation of the
blue exterior-pair footprint theorem for all 389 roots of the integrated
\(M=214\) decision.

For a selected red anchor edge with common red core \(H\), and a blue exterior
edge \(zz'\), let \(M\) be the core vertices blue to both endpoints. If
\(m=|M|\) and \(e\) is the number of red edges induced by \(M\), then

\[
m\leq5,\qquad e\geq m-2,qquad e\geq3m-10.
\]

At \(m=5\), the missed cell is exactly a red \(C_5\). The proof and sharp
cyclic witnesses are in [PROOF.md](PROOF.md).

The lift introduces exact Boolean variables for membership in \(M\) and for a
red edge lying wholly inside \(M\). These variables are indexed by physical
vertices and shared across every root that uses them. The resulting formula is
equisatisfiable with the complete height-3254 formula. It is not a SAT/UNSAT
result, a solved root, a Ramsey graph, or an improved Ramsey-number bound.

## Exact identities

```text
roots                                      389
root/exterior-pair instances           169,662
shared missed-vertex variables          10,612
shared missed-red-edge variables        74,513
new auxiliary variables                 85,125
definition rows                         329,888
guarded root rows                       508,986
total new rows                          838,874
generated suffix bytes              264,632,589
generated suffix SHA-256 cc8bb5681bc56fcf042a3cd51e0b1ddd92d077e933593384c3a4d924e4879ad3
```

Appending the generated suffix to the height-3254 formula gives:

```text
variables          98,758
constraints     2,969,925
equalities              87
lines           2,969,926
bytes          451,842,281
SHA-256 c0afe63fb47a3941481154addcbf383be134eeee0861afbd8451eb5eba19050c
```

The generated suffix and full OPB are deliberately excluded from source
control. Their identities are fixed by `EXPECTED_RESULT.json` and
`formula_manifest.json`.

## Compact reproduction

With CPython 3.12 and a C++20 compiler, run from this directory:

```sh
set -o pipefail
python3 -B build.py --certificate /tmp/pair_cell_roots.tsv \
  --suffix /tmp/pair_cell_suffix.opbpart | cmp - EXPECTED_RESULT.json
cmp /tmp/pair_cell_roots.tsv roots.tsv
python3 -B -O build.py --certificate /tmp/pair_cell_roots_opt.tsv \
  --suffix /tmp/pair_cell_suffix_opt.opbpart | cmp - EXPECTED_RESULT.json
cmp /tmp/pair_cell_roots.tsv /tmp/pair_cell_roots_opt.tsv
cmp /tmp/pair_cell_suffix.opbpart /tmp/pair_cell_suffix_opt.opbpart
python3 -B test_build.py | cmp - EXPECTED_TEST_OUTPUT.txt
c++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  independent_check.cpp -o /tmp/pair_cell_check
/tmp/pair_cell_check /tmp/pair_cell_roots.tsv \
  /tmp/pair_cell_suffix.opbpart | cmp - EXPECTED_CHECK_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

The default Apple Command Line Tools installation on the author machine was
missing its standard C++ headers during the final replay. The recorded strict
and sanitizer checks used Homebrew GCC 16.2.0 as
`/opt/homebrew/bin/g++-16`; this is an environment detail, not an additional
dependency of the source.

## Full-formula reproduction

The adjacent public directories reconstruct each accepted predecessor:

```sh
python3 -B ../ramsey_r55_m214_integrated_pair_roots/generate_opb.py \
  --output /tmp/m214_height3160.opb
python3 -B ../ramsey_r55_m214_all_c_footprint_bound/build.py \
  --prior-opb /tmp/m214_height3160.opb \
  --output-opb /tmp/m214_height3228.opb
python3 -B ../ramsey_r55_m214_blue_pair_footprints/build.py \
  --prior-opb /tmp/m214_height3228.opb \
  --output-opb /tmp/m214_height3254.opb
python3 -B build.py --certificate /tmp/pair_cell_roots.tsv \
  --suffix /tmp/pair_cell_suffix.opbpart \
  --prior-opb /tmp/m214_height3254.opb \
  --output-opb /tmp/m214_pair_cell.opb | cmp - EXPECTED_FULL_RESULT.json
/tmp/pair_cell_check /tmp/pair_cell_roots.tsv \
  /tmp/pair_cell_suffix.opbpart /tmp/m214_height3254.opb \
  /tmp/m214_pair_cell.opb | cmp - EXPECTED_FULL_CHECK_OUTPUT.txt
shasum -a 256 /tmp/m214_pair_cell.opb
```

The last hash must match `formula_manifest.json`.

## Independent checks

The Python generator and C++20 checker independently enumerate all root labels,
derive the union of physically used auxiliary coordinates, assign identifiers,
and emit all 838,874 rows. The checker compares every row byte for byte and,
when given the two formulas, compares the entire prior body and appended suffix.

Both implementations verify the two conjunction truth tables, all selector and
pair-edge guard states, the exact lower hull

\[
(e_{\min}(0),\ldots,e_{\min}(5))=(0,0,0,1,2,5),
\]

and the three cyclic sharpness witnesses. Normal and optimized CPython outputs
are byte-identical. Strict GCC 16.2.0, AddressSanitizer, and
UndefinedBehaviorSanitizer checks pass. Empty-certificate, truncated-suffix,
wrong-prior, and wrong-final-formula controls are rejected.

## Trust boundary and stopping condition

Formula equivalence trusts the accepted height-3148 root cover, the independently
accepted height-3160 selector semantics, and the published height-3228 and
height-3254 formula identities. Trusted remain the displayed elementary proof,
exact Python/C++ semantics, the compiler and ordinary hardware, and SHA-256.
The two implementations are author-run cross-checks, not external review or
proof-assistant formalization. No solver status, generated OPB, private state,
database, raw dump, or binary is evidence or published.

For historical provenance of the finite Ramsey argument, see F. P. Ramsey,
[On a Problem of Formal Logic](https://doi.org/10.1112/plms/s2-30.1.264),
*Proceedings of the London Mathematical Society* s2-30 (1930), 264–286. The
short equality proof needed here is included in `PROOF.md`; no priority claim is
made for it.

This closes the pair-cardinality and missed-cell edge-hull mechanisms. The full
\(M=214\) branch remains undecided. A further pass must consume the lifted
pair-cell variables in a genuinely global degree/deficiency or multi-anchor
certificate, or leave this mechanism rather than adding another local facet.
