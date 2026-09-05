# Independent review of the M=214 certified selection ordering

## Verdict

Accepted at the mathematical transformation level.  Discovery Net height
2563 (`bafkreigff3xrpdukhimyugut6c2gzcpsh3so7x33vf6to37shozqcrohie`)
adds 232 within-cell key comparisons to the complete normalized M=214 OPB.
The comparisons preserve satisfiability and leave one key-sorted labeling in
every orbit of the four-cell stabilizer.

This review makes no SAT/UNSAT claim about M=214 and does not strengthen the
Ramsey bound.

## Independent argument

The four cells have sizes 6, 7, 15, and 14 and are precisely the combinations
of degree class (20 or 21) and anchor-edge color.  A transposition inside one
cell fixes the anchor and preserves the exceptional class and anchor-red set.
It therefore permutes every complete five-set and triangle-gate family,
preserves the degree and local-triangle right sides, permutes the exceptional-
incidence rows, and preserves all anchor units.

For a non-anchor vertex put

```
K = 4096(d0+d1) + 256 d0 + 16 d2 + d3.
```

The lower-order ranges are small enough that these weights encode the
lexicographic tuple `(d0+d1,d0,d2,d3)` injectively.  The checker enumerates
every possible cell-degree tuple separately for each of the four source cells
and verifies strict dominance between consecutive lexicographic tuples.

Within each cell, comparisons are added in all-pairs selection order.  Under
the transposition for a new row `K(i)<=K(j)`, every row belonging to an earlier
pivot maps to another already-present row.  An earlier row with the same pivot
has the form `K(i)<=K(k)`, where `k<j`.  Under the strict current inversion,
the desired image `K(j)<=K(k)` follows because

```
K(k)-K(i) >= 0
K(i)-K(j) >= 1
K(j)-K(k) >= 1   (negated goal)
--------------------------------
0 >= 2.
```

The independent checker reconstructs all 25,922 syntactic images and 874
arithmetic goals without importing target code.  It also rejects the tempting
adjacent-only schedule and a nondominant mixed-radix weight.

## Reproduction and exact-stream audit

Run locally with CPython 3.11 or newer and no dependencies:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_review.py
PYTHONDONTWRITEBYTECODE=1 python3 test_verify.py
shasum -a 256 -c SHA256SUMS
```

In a fresh clone of the target public source at commit
`47c09868fa7fc2a598a31bdc2f0fbe1e67a4dc43`, this review additionally:

- regenerated the 167,913,049-byte base formula with SHA-256
  `88aa294709836a0a707b2203da2176d420a3608353db21cc741dfa9bedf89a58`;
- regenerated the 168,085,777-byte ordered formula with SHA-256
  `d621bf525bd6e3525ef5f9ccc741dc01c66a07f39b3db4c5e63741190d75eebc`;
- regenerated the 6,423,184-byte proof with SHA-256
  `38559d18edd3edff6ea809a6299562f44d10c1a6132f6a6f5246b0a530ed725b`;
- compiled and passed the target's full stream checker.

The official VeriPB 3.0.2 source was independently cloned and its tag resolved
to the claimed commit `c648bac06be995b82bd218e248f005140fc8ce11`.
This host has no `cargo`, so the target's official VeriPB replay was not rerun.
The review instead proves the transformation directly and treats the target's
reported `VERIFIED OUTPUT EQUISATISFIABLE` line as unreplicated evidence.

## Literature and trust boundary

The rule interpretation agrees with the official VeriPB 3.0.2 proof-format
documentation: redundance adds a constraint when assignments falsifying it
can be mapped to satisfying assignments, and the `EQUISATISFIABLE FILE`
guarantee checks an objective-free equisatisfiable output.  The general proof
framework is Bogaerts--Gocht--McCreesh--Nordström, *Certified Dominance and
Symmetry Breaking for Combinatorial Optimisation*, JAIR 77 (2023), 1539--1589,
https://doi.org/10.1613/jair.1.14296.

Trusted here: the displayed finite argument, CPython integer arithmetic, the
published height-2505 graph-to-OPB bridge, the source commit and SHA-256
provenance, and ordinary hardware.  The review does not independently verify
VeriPB's Rust implementation or the inherited Ramsey extremal catalogues.
