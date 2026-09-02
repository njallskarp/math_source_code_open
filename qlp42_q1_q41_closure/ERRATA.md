# Erratum: q=41 labeled-word aggregate

The immutable source package
`qlp42_q41_all_weight_exact_sweep` at commit
`349a8f3fc5d46a0427e5434ef2177d8405a4d6ff` displays and emits

```text
manifest_b_axis_words=524776.
```

The correct sum of its six per-weight counts is

```text
C(21,0)  + C(21,4) + C(21,8)
+ C(21,12) + C(21,16) + C(21,20)
= 1 + 5,985 + 203,490 + 293,930 + 20,349 + 21
= 523,776.
```

The discrepancy is exactly 1,000 and is confined to a hard-coded aggregate
summary field and the corresponding README total. It does not change the
enumerated orbit set:

- `expected_orbits()` generates every fixed-weight word from combinations,
  canonicalizes it, and records its actual orbit multiplicity;
- `check_manifest()` requires the production record keys to equal that
  independently generated 24,946-key dictionary exactly;
- the independently written NumPy verifier reconstructs the same 24,946
  orbits;
- at weight 12, the five size-7 and 13,995 size-21 orbit multiplicities sum
  to `C(21,12)=293,930`.

The exclusion theorem uses the exact orbit records, per-weight sign
enumerations, and terminal intersections. It does not use 524,776 as a loop
bound or mathematical premise. The proof conclusion is therefore unchanged,
but the source summary should be corrected in any future release.
