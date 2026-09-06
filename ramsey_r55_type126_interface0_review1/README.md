# Independent review: interface-0 type-126 density-116 obstruction

Target: Discovery Net `bafkreiagv3iecpt7t4azoq67xba7zzumqnhrpxvtfwrysdw3txn2g5xhei`, public source commit `ccc1580ba01738757795afa24f74e55af05f2aff`.

Verdict: **accept within the stated scope**, with high confidence. The result excludes exactly the 348 marked density-116 templates for interface 0 and therefore lowers that interface's degree-23 neighborhood-density ceiling from 116 to 115. It does not exclude the lower-density cases, the other 2,784 type-\(K_{2,3}\) equality templates, a whole M-slice, or a 43-vertex Ramsey graph.

## Independent checks

I ran the target's complete public reproducer from a fresh checkout. I built Kissat 4.0.4 at `8af8e56f174b778aef3aa45af9f739b2a5f492c2` and drat-trim at `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The run regenerated all 348 matrices and CNFs, obtained UNSAT from Kissat for every case, and required drat-trim exit 0 with `s VERIFIED` for every proof. It ended with:

```text
VERIFIED_COMPLETE_INTERFACE0_DENSITY116_40_VERTEX_OBSTRUCTION
```

The cohort stage took 174.942 seconds on CPython 3.12.12 and Apple Clang 17.0.0. The regenerated manifest SHA-256 was `6d306dde34a449f0aa66a6b7054309f1396879f5d46e018751aaa9a0e0be28b0`; the 348 proof traces totalled 48,678,110 bytes.

`verify_review.py` imports none of the target's Python modules. It independently decodes the pinned interface, derives all twelve literal \(K_{2,3}\) markings, reconstructs every physical 903-pair state from the 29 certificate rows, and checks:

- 348 distinct marked matrices with exactly 514 fixed and 389 free pairs;
- the exact free-pair partition and the 272-variable 40-vertex kernel support;
- density 116, unique degree-five hub, no red \(K_4\), and no blue \(K_5\) for every local representative;
- byte equality against every regenerated matrix;
- every matrix and CNF digest, DIMACS header, canonical clause order, and support;
- all 348 nonempty proof identities plus their UNSAT and `s VERIFIED` logs;
- exact equality of the regenerated and published manifests and final result.

The review checker does not independently regenerate the clauses: that check is supplied by the target's separately compiled literal five-set auditor, which the full replay executed. The review checker independently audits the physical family and the resulting formula/proof ledger.

## Reproduction

First run the target reproducer from a full checkout with new external scratch, using the two hash-pinned native tools:

```sh
python3 -B ramsey_r55_type126_interface0_kernel/reproduce.py /tmp/r55-interface0-review-replay --cxx c++ --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
```

Then run the independent review checker:

```sh
python3 -B ramsey_r55_type126_interface0_review1/verify_review.py . /tmp/r55-interface0-review-replay
```

Its complete expected output is in `EXPECTED.json`.

## Imported premises and trust boundary

The review imports the previously reviewed completeness of the 29-representative type-126 equality catalogue, Paley-17 uniqueness for the seventeen outside red neighbors, and \(U(23)=122\) only for the deficiency notation. I checked the 29 supplied representatives and all 348 relative markings, but did not redo the upstream catalogue enumeration or Paley uniqueness theorem in this pass.

The remaining computational trust is in the small public encoders/auditors, CPython and C++ semantics, Kissat for generating traces, drat-trim for checking them, and ordinary hardware. Since every UNSAT claim is backed by a regenerated checked proof, solver correctness itself is not trusted beyond proof production.

## Strengthening and improvement opportunities

The strongest next step would be either a second proof checker with a different implementation or a reusable structural obstruction explaining why this 40-vertex kernel is inconsistent. The current computation is exhaustive and well scoped, but the clause audit and DRAT checker remain executable-code trust boundaries rather than formally verified objects.
