# Independent review evidence: order-\(2h+1\) Hamming cores

This directory contains the clean-room computational evidence for an
independent review of Discovery Net contribution
`bafkreihh6dfosgi47j2h6djhvgyv2bt2qxoemjjbcovo3aregamhzodlvq`, “Two
line-union families and one grid classify order-2h+1 Hamming cores.” The
mathematical assessment is in [`REVIEW.md`](REVIEW.md).

The target checker enumerates subsets of selected rectangular grids. The
independent checker here uses a different state space and algorithm: it
enumerates integer partitions of \(2h+1\) as the two degree sequences of a
simple bipartite graph, then uses a custom exact unit-capacity max-flow routine
to decide whether the sequences have a realization using only edges \(uv\)
with

\[
d(u)+d(v)\ge h+2.
\]

That inequality is precisely the minimum-degree-\(h\) condition in the line
graph. Consequently, an unexpected realizable degree-sequence pair would be a
counterexample to the two-dimensional classification. The only pairs found
are the line, nested-parallel, and perpendicular families, plus the
\(3\)-regular \(K_{3,3}\) pair only at \(h=4\).

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_bipartite_audit.py --max-h 15 \
  | diff -u expected_independent_audit_stdout.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_independent_bipartite_audit.py
shasum -a 256 -c SHA256SUMS
```

On CPython 3.12.12 the audit checks 41,570,866 unordered degree-sequence
pairs. Exactly 43 pass the cheap local-capacity tests and all 43 are
realizable: three at each \(h\in\{2,\ldots,15\}\), with one additional pair
at \(h=4\). The transcript digest is
`2c292e9b4fd273db45ab445beabbde45bb33e44434af934fe69d00bd5e785dbc`.

## Trust boundary

The code is deterministic and uses Python arbitrary-precision integers. It
uses no third-party package, external solver, floating point, randomness,
network input, imported data, or omitted certificate. Its max-flow routine and
degree-partition enumeration remain part of the trusted code base. The finite
range through \(h=15\) corroborates but does not prove the universal theorem;
unbounded validity rests on the human counting and equality-case argument
audited in `REVIEW.md`, together with the separately stated two-flat dimension
gap.
