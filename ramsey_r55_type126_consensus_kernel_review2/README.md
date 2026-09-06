# Independent review evidence for h3505

Target: Discovery Net contribution
`bafkreifyv7hvcecik5z24tonkxe3znibplf7uitjns7cujhjidrfbo2fsq`, height
3505, at public source commit
`1613d62eed08e2295cf5dda30b57a095e56c9eef`.

Verdict supported by this evidence: **accept, high confidence**.  The exact
local-family theorem, equality-boundary cover, physical transport, weaker-CNF
reduction, and all native refutations agree with the stated result.  This does
not establish the imported completeness of the 29 equality representatives,
the imported value \(U(23)=122\), or the completeness of the thirteen-interface
census.

## Independent definition-level check

`independent_check.py` imports no reviewed Python or C++ module.  From the two
hash-pinned upstream JSON inputs and the reviewed compact certificate data it:

- decodes the two graph6 endpoints and verifies their exact twelve-edge
  disagreement after the stated cell-preserving permutation;
- checks all 4,096 local assignments, recovering exactly 110 Ramsey fillings,
  the complete density histogram, the two dense masks, and the unique hub;
- directly checks the 29 literal equality graphs have 116 edges, unique
  degree-five hub, no red \(K_4\), and no blue \(K_5\);
- reconstructs all 348 relaxed 43-vertex physical matrices and matches every
  published matrix hash;
- checks all 628,488 pair transports from the 696 original marked cases, with
  exactly two preimages per relaxed key; and
- enumerates every five-set directly for twelve stratified CNF cases and
  matches their exact clause counts and hashes.

Run from a checkout of
<https://github.com/njallskarp/math_source_code_open>:

```sh
python3 -B independent_check.py \
  --source /path/to/math_source_code_open/ramsey_r55_type126_consensus_kernel \
  --upstream /path/to/math_source_code_open/ramsey_r55_dense_degree23_hub_classification
```

Expected status: `INDEPENDENT_H3505_DEFINITIONAL_CHECK_PASS`.  The complete
observed output is in `INDEPENDENT_RESULT.json`.  Python 3.12.12 standard
library was used; runtime was about 37 seconds on the review host.

## Native certificate replay

The target's complete reproduction command was run from a detached checkout of
the cited source commit using Kissat commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, drat-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, CPython 3.12.12, and GCC 16.
It regenerated all 348 matrices and CNFs, matched the manifest, returned UNSAT
on all 348 cases, and accepted all 348 DRAT traces.  The regenerated proof
traces totaled 238,785,368 bytes and remain excluded from publication.

As an additional checker path, the DRAT proofs for keys `(0,0)`, `(17,6)`
(the minimum clause count), and `(10,9)` (the maximum clause count) were
converted to LRAT with drat-trim and accepted by the separately built
`lrat-check`.  Compact measurements and hashes are in
`NATIVE_REPLAY_RESULT.json`.

## Trust boundary

Checked here: literal graph decoding, exhaustive twelve-bit classification,
all stated markings and physical transports, all 348 matrix identities,
twelve direct-definition CNFs, all 348 solver runs and DRAT checks, and three
LRAT checks.  Imported: the previously reviewed completeness of the 29-class
dense-hub theorem and Paley-17 uniqueness, the complete thirteen-interface
census used to interpret the two endpoints as whole cohorts, and \(U(23)=122\)
for deficiency notation.  Remaining trust lies in the displayed mathematical
reduction, the public upstream blobs, Python/C++ and compiler semantics,
Kissat, drat-trim/`lrat-check`, and ordinary hardware.
