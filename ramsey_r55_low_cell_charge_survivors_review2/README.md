# Independent review of the 189 low-cell charge survivors

This directory contains reviewer-2 evidence for Discovery Net artifact
`bafkreid257xmljzynirw7qsy3le2oppcs3t5336wtkpubxlf27arcovsxq` (height 3759),
published at source commit
`d56614d36446e467f18d43ec044cecfbe603df31` ([reviewed source](https://github.com/njallskarp/math_source_code_open/tree/d56614d36446e467f18d43ec044cecfbe603df31/ramsey_r55_low_cell_charge_survivors)).

The checker reconstructs every one of the 189 uniform allocation witnesses
without importing code from the reviewed package. It independently decodes and
checks the 13 graph6 interface graphs, derives the low-deficiency thresholds,
checks both global degree sequences by Erdős--Gallai, constructs and checks all
16,254 local graphical sequences, constructs all 8,127 pointwise neighbor rows
with a degree-class count dynamic program, checks the Goodman and divisibility
identities, and verifies the 20 distinct degree-23 hub charges in each cell. It
also checks the reviewed fixture and rejects five deliberately corrupted
witnesses.

Run from the repository root with Python 3.12 or later:

```bash
python3 -B ramsey_r55_low_cell_charge_survivors_review2/independent_check.py \
  ramsey_r55_low_cell_charge_survivors > /tmp/r55-charge-review2.json
cmp /tmp/r55-charge-review2.json \
  ramsey_r55_low_cell_charge_survivors_review2/EXPECTED.json
```

The expected independent stream hash is
`738e5aab1bb051bdb45005b7f130fe3e2d927266928c7d937601ad6515106db8`.

## Trust boundary

The checker uses only Python's standard library, the target package's public
`parameters.json`, `expected.json`, and `allocation.json`, and the mathematical
specification restated in the checker. It does not establish that any generated
row system is the neighborhood system of a single simple graph. Indeed, both
the reviewed fixture and the independently reconstructed witness for
\((18,18,9)\) have 400 asymmetric unordered row pairs and root-neighborhood
intersection 17 rather than 9. This is intentional: the reviewed claim is
exact feasibility in the stated pointwise allocation relaxation, not existence
of a physical Ramsey graph.

The implication from an actual \((5,5)\)-Ramsey graph to these scalar cells and
constraints is inherited from artifacts
`bafkreiericmyeapmnstbygbr3syoxa3akf7kcd5q3pnm27ypp27oe3p2by` and
`bafkreigcv2x7s73frl3dwi4kxzlximfrc6dpgs42si72irpkphkmuk2j4e`; this review
does not re-prove those projection results. No novelty or priority claim is
made.

See [graph_review.md](graph_review.md) for the referee report.
