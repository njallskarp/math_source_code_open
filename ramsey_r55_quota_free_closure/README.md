# Quota-free closure of a fixed Ramsey core pair

Every completion of the 503 colors in [PARTIAL.json](PARTIAL.json), with the
degree intervals below, contains a monochromatic \(K_5\). All 36 cell quotas
from the earlier fixed-profile theorem are removed jointly. This is an exact
computer-assisted **conditional family exclusion**, not a full
\(d=22\) or deficiency-six classification and not a Ramsey-bound improvement.

## Family and proof

Vertices are \(0,\ldots,42\). In the partial matrix, `1` is red, `0` is blue,
`.` is free and `-` is diagonal. The 400 free pairs run between
\(\{1,\ldots,22\}\setminus\{3,9\}\) and \(\{23,\ldots,42\}\).
Require red degree 22 at vertex 0, degree 21 or 22 at vertices 1 through 22,
and degree 20 or 21 at vertices 23 through 42. There are no cell counts, total
edge counts, six local edge-count equations, or additional normalizations.

[PROOF.md](PROOF.md) gives the exact graph-to-CNF and modular certificate
arguments. The base has 400 primary variables, 8,320 total variables and
67,384 clauses: 51,624 global clique clauses and 15,760 clauses for 80 degree
bounds. The base auditor imports neither PySAT nor the producer and checks
the exact clause multiset.

Discovery uses fresh gate definitions and twenty root assertions. Each root
is separately proved from a subset of the base and definition clauses by a
RUP refutation of its negation. A 21st RUP refutation closes the full formula.
The interface auditor verifies conservative definitions and every local
premise literally. Thus column-domain completeness is not a proof premise.

The proof is modular, not a successfully replayed flattened trace. The direct
base search was `UNKNOWN` at a 240-second limit, and two flattened DRAT
replays hit 180-second limits. Those trials are not evidence of exclusion.
The successful evidence is the 21 RUP replays plus exact base/interface audits.

## Reproduction

Use CPython 3.12.12 and `python-sat==1.9.dev15`. Build
[DRAT-trim](https://github.com/marijnheule/drat-trim) at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` outside this directory. The work
directory below must not already exist and must be outside the source tree.

```sh
uv run --no-project --with python-sat==1.9.dev15 python -B run.py \
  --work /tmp/new-r55-quota-free-proof --drat-trim /path/to/drat-trim
python3 -B audit.py /tmp/new-r55-quota-free-proof/base.cnf
python3 -B interface.py /tmp/new-r55-quota-free-proof
python3 -B controls.py /tmp/new-r55-quota-free-proof
shasum -a 256 -c SHA256SUMS
```

Expected: `VERIFIED`, 21 RUP replays, `all_checks: true`, 2,304 counter
extensions, 144 gate truth-table rows and 12 rejected corruptions. The base
SHA-256 is `8f5d82a701d578b51f0f8f51f6c28b624335d2f107e9356f93405d1d3900b030`.
The full formula SHA-256 is
`834e7bb53a1e749ad2c36319801c717bf65a56fb9577553fa440ab58a5406894`.
[verification.json](verification.json) records every checked local/global
formula and proof hash. A hash or a solver verdict alone is not a certificate.

The global solve cap is 240 seconds, local solve caps are 20 seconds, local
replay caps are 30 seconds, and global replay has a 120-second cap. A timeout
must fail reproduction rather than be reported as a theorem. Large generated
CNFs, proofs, logs and caches are deliberately omitted and regenerated outside
Git. No external graph catalogue is downloaded by the reproduction.

## Provenance and limitations

The literal partial matrix is byte-identical to the
[height-3003 source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_fixed_core_closure),
previously published at commit `7a0064314f61056e21372a132dfc0c458f38312e`.
No prior exclusion or profile file is imported. The new proof does not clear
the independent-review gate of height 3003; both results retain their honest
review status. Standard gluing context is
[Angeltveit–McKay](https://arxiv.org/html/2409.15709v2); the encoding and proof
composition mechanisms carry no historical-priority claim.

The stated intervals necessarily allow only the numerical forms
\(20^{16-x}21^{26}22^{x+1}\), with \(0\le x\le16\), and
\(444+x\) red edges. This bookkeeping does not claim all seventeen forms
are realizable. The theorem excludes only completions of this literal matrix,
not all graphs with those degree multisets.

Trust boundaries are the unformalized reduction and modular composition,
exact auditors, RUP checker, runtime, input identity and hardware. Fresh
regeneration and different algorithms are author validation, not independent
peer review or formalization. Do not extend to other core pairs or remove the
remaining fixed incidences merely from this certificate.
