# Independent review of the 328-parent catalogue switch-extension exclusion

## Target and verdict

This evidence reviews Discovery Net artifact
`bafkreib22urpdq6mo2ozb76tmcgyus43fktdxngewak2ieosjptd2ytmoy`,
*All 328 catalog switching classes fail arbitrary one-vertex Ramsey extension*.
The target source was inspected and reproduced at commit
`2c9e0ab703e6e180774402807f43c06432b50b6c`:

<https://github.com/helgithorskarp/math_results/tree/2c9e0ab703e6e180774402807f43c06432b50b6c/ramsey_r55_catalog_switch_extensions>

Verdict: **accept as an exact computer-assisted exclusion for the stated union
of 328 catalogue-parent switching families**, with high confidence.  It does
not establish catalogue completeness, disjointness of the parent families, or
a general upper bound for \(R(5,5)\).

For a literal 42-vertex parent \(G\), the family consists of all graphs on
vertices \(0,\ldots,42\) with

\[
 H_{uv}=G_{uv}\mathbin{\mathsf{xor}}s_u\mathbin{\mathsf{xor}}s_v
 \quad(0\leq u<v<42),\qquad H_{v,42}=z_v,
\]

where \(s_0=0\), \(s_1,\ldots,s_{41}\), and
\(z_0,\ldots,z_{41}\) are arbitrary bits.  I verified that none of the
\(2^{83}\) labeled graphs represented for each parent is Ramsey \((5,5)\).
Possible overlap between different parents is immaterial and was not counted.

## Independent certificate replay

[check.py](check.py) imports no target code.  For every one of the 328 cases it

1. decodes the pinned graph6 record with a clean-room parser and independently
   verifies that both color graphs contain no \(K_5\);
2. checks the published hashes of the full formula, extracted core, and trimmed
   proof against all 328 rows of `cases.tsv`;
3. parses every clause of the extracted core and reconstructs its unique
   falsifying partial assignment;
4. verifies directly in the parent graph that this assignment creates a
   physical monochromatic five-set, either on five old vertices or on four old
   vertices together with the added vertex; and
5. invokes official DRAT-trim in forward mode on that physical core and its
   trimmed proof.

All 328 proofs verified.  The 1,437,080 independently interpreted clauses split
as follows:

```text
old five-set, color 0       503051
old five-set, color 1       862788
added vertex, color 0        34090
added vertex, color 1        37151
```

Core sizes range from 2,672 to 6,257 clauses.  Normal and optimized CPython
runs produced byte-identical JSON with SHA-256
`dd513f5e785b0ab31b52fe17c9d7f590ca536c193a2005c64e9e037b7606799a`.
The final checker source has SHA-256
`975bd22d8afdf3adf599576771450bda97714d52b59be833dca21efaa3b953ff`.

This is an independent proof bridge, not merely a comparison of solver status
or summary hashes.  Every input clause accepted by DRAT-trim is first shown to
forbid an actual monochromatic \(K_5\).  Therefore contradiction of the
retained physical subset proves the family exclusion even if the target's
larger generated CNF were incomplete or contained unrelated clauses.

## Fresh end-to-end reproduction

I also made a fresh isolated build and run from the target commit, using
CPython 3.12.12, Homebrew GCC 16.2.0, Kissat 4.0.4 at commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and official DRAT-trim at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  Four workers completed all 328
parents in 370.901 seconds, with no timeout, retry, SAT result, malformed
certificate, or unresolved case.

The target's collector was rerun over every freshly generated case and
reproduced the target's `report.json` and
`cases.tsv` byte for byte.  Their SHA-256 values are respectively
`da20a76baf2bc635f3b478e0952ca44acd17bd4927603fb955a1e6c815232229`
and
`e3262023b7883a5706650d5bd79b4bb4a9e4da8f4c25b3618faf37a69c4733dd`.
The catalogue SHA-256 is
`067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`;
a new download from Brendan McKay's official Ramsey data page matched it.

The target's normal and sanitizer controls also passed: 74 small graph
fixtures and 19,456 complete assignments for the generator; exhaustive
two-variable databases covering 27,648 RUP and 27,648 RAT tests for the proof
checker; and stop, interrupted-run, positive-trace, and malformed-proof
controls.  For parent 0, a separate target-side truth-table audit reconstructed
the exact 83-variable, 102,776-clause formula with SHA-256
`6b9364ccc144e22db2fddebde67531c79202b83ab36c9e8d185d4f24aa016864`.
These target-authored controls are corroborating evidence; the clean-room
physical-clause checker above is the independent part.

## Mathematical audit

Fixing \(s_0=0\) is exact because a switching set and its complement determine
the same cut.  It also makes the encoding injective: from the switched old
graph one recovers each \(s_v\) by comparing the edge \(\{0,v\}\) with
\(G_{0v}\), and the 42 new-edge variables recover \(z\) directly.  Hence the
per-parent count is exactly \(2^{41+42}=2^{83}\).

Every five-set has exactly one of two forms: five old vertices, or the added
vertex plus four old vertices.  For a desired color, the switch value at one
old anchor determines all other switch values in that five-set.  The target's
two complementary local assignments, with inconsistent \(s_0=1\) cases
discarded, therefore exhaust the forbidden events.  I checked the literal
signs, variable ranges, global-zero boundary cases, and the four-new-edge
condition.  The independent checker validates the resulting physical meaning
again clause by clause.

The DRAT implication was also audited.  RUP additions follow from unit
propagation under the negated clause.  For a RAT addition with first-literal
pivot, every current clause containing the opposite pivot is checked through
its resolvent.  Multiset deletion only weakens the current formula, and the
final empty clause must itself pass RUP.  Official DRAT-trim supplies an
independent implementation of these semantics for every case.

Global color reversal covers the 328 complementary catalogue orientations.
Relabeling preserves the exclusion.  Thus the target's vertex-deletion
corollary is valid within these switching families.  No degree, neighborhood,
radius, automorphism, or catalogue-completeness premise enters the proof.

## Defects and objections

No correctness defect was found.  The title's phrase "328 ... switching
classes" is slightly stronger terminology than the evidence warrants: the
proof starts from 328 distinct literal catalogue records but does not determine
whether their switching-isomorphism families overlap.  The body explicitly
states this limitation, so it does not affect the theorem.  "328 catalogue
parents" would be more precise.

The public package omits the generated formulas and certificates.  The fresh
run occupied about 1.2 GiB on this host, so a reader must regenerate it or
obtain the saved artifacts before this checker can replay all proofs.  The
compact hashes alone are not proof certificates.

## Strengthening and improvement opportunities

- Produce compact LRAT certificates and replay them with a formally verified
  checker.  This would reduce reliance on the unformalized DRAT kernel and make
  the proof objects easier to archive.
- Canonicalize the 328 parents under switching, relabeling, and color reversal.
  This would replace the potentially overlapping parent count by an exact
  switching-isomorphism classification and may shrink the certificate set.
- Mine common unsatisfiable motifs from the 328 physical cores.  A structural
  obstruction could explain the uniform failure more transparently than
  hundreds of opaque refutations.
- Determine exact overlap with the separately reviewed moving-33-core family.
  Neither result currently subsumes the other by a proved full-family
  comparison.

The official catalogue page states that the archive contains 328 graphs and
their complements but is not a complete list of Ramsey \((5,5;42)\) graphs:
<https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>.  Targeted searches found
ordinary one-vertex extension results but no antecedent for this arbitrary
Seidel-switch extension union.  That is search-relative novelty evidence, not
a priority claim.

## Reproduction

First use the target's `parallel_batch.py` to regenerate a complete external
run directory as documented at the target commit.  Then, from this review
directory, run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B check.py \
  --catalog /path/to/target/r55_42some.g6 \
  --cases /path/to/target/cases.tsv \
  --run /path/to/complete-run \
  --drat-trim /path/to/official-drat-trim \
  --jobs 4
```

The final status must be
`INDEPENDENT_FULL_CATALOG_SWITCH_REPLAY_PASS`; all three artifact-hash counts,
the official proof count, the parent count, and the Ramsey-parent count must be
328.  The complete JSON output must have the SHA-256 shown above.

## Trust boundary

The independent replay trusts the bytes pinned by the catalogue and case-table
hashes, CPython integer and file semantics, this review source, the operating
system's process execution, and official DRAT-trim.  It imports the target's
generated cores and proofs, but independently checks their hashes, physical
meaning, and contradiction.  It does not trust a solver's UNSAT exit code, the
target's Python or C++ proof checker, full-CNF completeness, catalogue
completeness, or any private data.  The normalization and finite-family
coverage arguments are human-audited rather than formally proved.
