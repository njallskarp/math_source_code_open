# Formal audit

## Pins

- Lean toolchain: `leanprover/lean4:v4.33.1`
- Lean commit: `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Mathlib release: `v4.33.1`
- Mathlib manifest commit: `0df444a360eaa60ab8c11dca51a86af692955474`
- Lake manifest format: `1.2.0`

## Proof policy

- no `sorry`;
- no `admit`;
- no custom `axiom` declarations;
- no native or external proof oracle;
- no concrete graph data or generated certificate;
- all graph reachability and finite-set facts are checked by Lean and Mathlib.

## Axiom audit

`Parts509Attachment.lean` ends with `#print axioms` for all eight public
theorems. The expected dependency set is:

```text
[propext, Classical.choice, Quot.sound]
```

These are standard Mathlib/Lean principles. The clean rebuild completed
successfully with 986 jobs. The audited Lean source SHA-256 is
`7e40efde830d2415e5e452da6b7bcf531bf25fad077f69608933488861446943`.

## External mathematical premises

The formalization proves the abstract implication only. A concrete Parts-509
instantiation still needs the certificate-backed premises:

- the induced core on 503 vertices remains connected after at most four vertex
  deletions;
- the six attachment vertices have degree four;
- every attachment edge enters the core;
- for the count of six distinct minimum cuts, the six neighborhoods are
  pairwise distinct.

The first and last items are not derived from the published coordinates here.
The edge-connectivity and minimum-edge-cut classification are also not claimed.
