# Cyclomatic-two line-graph core stability

This directory proves a bounded case of the open fixed-cyclomatic line-graph
signature program: an extremal minimum-degree-two core with cyclomatic number
two cannot gain line-graph signature from one attached leaf.

`TWO_LEAF_STABILITY.md` strengthens this to any two simultaneous leaves,
including two leaves at the same support.  Its rank-two response identity and
a zero-response kernel-difference lemma cover every singular case.  It does
not claim stability for three leaves or arbitrary deeper pendant trees.

The main argument is in `CYCLOMATIC_TWO_CORE_STABILITY.md`.  It combines an
exact leaf rank-one criterion with a four-subdivision congruence that
preserves inertia and every defined/undefined vertex response.  A modulo-four
reduction then leaves four extremal dumbbell bases.

## Reproduce

The two production checkers require CPython 3.11 or later and no third-party
packages.  The optional independent characteristic-polynomial audit requires
SymPy 1.14.x.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_c2_core.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_two_leaf.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_two_leaf_charpoly.py
```

Expected final lines:

```text
result_sha256=92b3ea8ffb472f39aaf452b83549404246772fe0b4cb67ea70979dffb35c70e8
VERIFIED
result_sha256=c80a82442617de3292cef4a807c76d1f6bc6ce5d399c3c62d08955592b16767c
VERIFIED
result_sha256=010f70c2a3f809ac8058173550f86f7baeecec02bcaebe9135c6128948f6cfc1
VERIFIED
```

The output records 16 reduced rose cases, 64 reduced theta cases, both exact
dumbbell signature tables, 46 four-subdivision checks, 714 leaf checks, and
the nonextremal response `-3/4` sharpness witness.

## Trust boundary

The proof is symbolic and human-readable.  The checker uses exact
`fractions.Fraction` arithmetic and a direct symmetric-congruence inertia
algorithm.  Its finite calculations corroborate the displayed residue and
response tables.  It does not replace the graph-topology classification or
the general block-congruence proof, and it makes no claim about multiple or
iterated pendant attachments beyond the separately proved two-leaf theorem.
