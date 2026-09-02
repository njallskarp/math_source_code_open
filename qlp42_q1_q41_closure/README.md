# QLP-42 extreme-branch closure package

This directory consolidates two exact computer-assisted results inside the
canonical norm-32 residual shell for length-42 quaternary Legendre pairs:

1. the complete `q=1` branch is empty; and
2. the complete `q=41` branch is empty.

Here `q` is the total number of quarter-turn cells in the established
coupled length-21 half-sum/half-difference transform. These are conditional
branch-closure theorems. They do **not** resolve QLP-42 and do not exclude the
separate `q=5` or `q=37` frontiers.

## Package contents

- [`MANUSCRIPT.md`](MANUSCRIPT.md): paper-ready mathematical narrative and
  precise theorem statements.
- [`DEPENDENCY_MAP.md`](DEPENDENCY_MAP.md): proof DAG and complete stratum
  partitions.
- [`SOURCE_PINS.json`](SOURCE_PINS.json): immutable Git commits, Git tree IDs,
  and committed graph artifact references.
- [`GRAPH_RELATIONS.md`](GRAPH_RELATIONS.md): proof dependencies versus graph
  edges, including the two graph gaps found during consolidation.
- [`TRUST_BOUNDARIES.md`](TRUST_BOUNDARIES.md): assumptions and remaining
  implementation, reduction, and provenance boundaries.
- [`ERRATA.md`](ERRATA.md): the corrected all-weight labeled-word aggregate
  and why the typo does not affect manifest coverage or exclusion.
- [`PRIOR_ART.md`](PRIOR_ART.md): positioning against primary literature.
- [`references.bib`](references.bib): compact bibliography.
- [`verify_package.py`](verify_package.py): dependency-free consistency check.

Run the package audit from this directory:

```bash
python3 verify_package.py
shasum -a 256 -c SHA256SUMS
```

The verifier checks every pinned commit and directory tree against the local
public-source repository, verifies the exhaustive stratum partitions, checks
the exceptional weight-12 orbit arithmetic, and validates the graph-reference
syntax. It does not rerun the underlying multi-billion-assignment proofs.
Those proof packages remain independently reproducible at their immutable
source pins.

## Fourth-layer q=5/q=37 scope at the pivot

The completed positive-only fourth-layer package is published at immutable
commit
[`0470cd6544de8ac51f2e77a861715a7e4bc50adb`](https://github.com/njallskarp/math_source_code_open/tree/0470cd6544de8ac51f2e77a861715a7e4bc50adb/qlp42_q5_q37_pi4_census).
It contains 67 definitionally checked witnesses: 38 in `q=5` and 29 in
`q=37`. It proves at least those survivals and proves **no exclusions**.
Every remaining cell is unknown at that layer; no timeout or bounded search
is a negative certificate. The committed graph lemma is
`bafkreie24um5q3mw3yv6sbor6l3zve7xemsjmcoy2wkfexgp365i5bwttu`.

No `pi^5` census or other cell-by-cell residue-depth search is part of this
package. Any return to `q=5/q=37` should begin from a falsifiable structural
lemma with family-level leverage.
