# Independent review of the eleven-residue BHR small-`a` mantle

## Target, scope, and verdict

Target: `bafkreidfnmvhvbsbzw6livdvaagxu4pbu7shs4u2dyhc4n7koyc7xw4spi`,
**Eleven-residue transition-closed a=1 BHR mantle**.

The target claims, for eleven pairs `(B_s,C_s)` with the `C_s` equal to the
consecutive integers 20 through 30, realizations of

\[
  \{1,2^{B_s+2q},11^{C_s+11r}\}\qquad(q,r\geq0),
\]

and hence realizations of every `\{1,2^b,11^c\}` with odd `b>=15` and
`c>=20`.

**Verdict: accept the existence theorem and uniform corollary, with high
confidence.**  I independently reproduced every finite path and transition
obligation and supplied a target-specific shortest-arc proof of the infinite
step.  The optional 60-pattern coverage statistic was not independently
reproduced because it requires a separate upstream certificate; it is not used
by the theorem.  I also prove the strict refinement

\[
  \boxed{b\geq13\text{ odd},\quad c\geq20.}
\]

## Independent computational audit

I audited the target source at public commit
`f2707ffc7a93f581ff4c99692bafc3a385ff6a25` under CPython 3.12.12.  The target
certificate has SHA-256
`7669175bf86a2ad4938bc1cd8a1aae8e7a64b5e59bcfc4904b6e6b4d7646a192`.
Both target checkers reproduced the declared 11 residue classes, 44 source
derivation steps, 704 family paths, 1,078 coordinate transitions, 539 squares,
and transition digest
`9dbdc10aa3bd26922507777712b06f311302b7bfa17b2454c8176c18bbb5959d`.
Five executable target tests passed and the optional external-coverage test was
skipped.

The new checker `independent_mantle_audit.py` imports no target module and uses
a separately written definition-level implementation.  It verifies:

1. every source and seed is a permutation with exactly the declared cyclic
   edge-length multiset;
2. every selected growth cut has exactly one changed-edge incidence at each
   critical vertex;
3. both source operation orders remain valid and give the identical stored
   seed, for 44 direct steps;
4. 891 states and 704 commuting squares through grid 8, starting from the
   smaller seed set proved below;
5. all 1,046,276 locally admissible edge/cut configurations with disjoint
   critical intervals, modes 2 and 11, edge length at most 11, and orders 35
   through 41; and
6. rejection of duplicate-vertex, shifted-cut, and duplicate-residue
   mutations.

The independent family digest is
`3e8fece62922a04ef00fc2dc8cf70b573f2dcaa19ac1603b6192d946a34932ca`;
the exhaustive local digest is
`9e945ae5b3f65b8d6c9d20e48c4bd6caf939c2ffe77d625cf6291f7f987bcea4`.

## Mathematical audit of the universal quantifiers

The eleven source orders are 23 through 28, so the checker correctly avoids
assuming cross-growth there: it applies one growth of each mode in both orders
and verifies every intermediate state directly.  The resulting stored seed
orders are 36 through 41, all edges have length at most `D=11`, and

\[
  2D+2+11=35\leq v.
\]

For the target's stored seeds the 2-critical and 11-critical intervals are
disjoint.  Mark the unique shorter circular arc of every old edge.  After both
gaps are inserted, that arc has length at most `D+2+11`, while its complement
has length at least `v-D`; the displayed inequality prevents a shortest-arc
flip.  Thus changed edges are exactly the marked arcs crossing the relevant
gap.  Because the two critical intervals are disjoint, the two inserted split
points are distinct and subdivision at them is order-independent.  Cut
transport preserves their separation.  Descendant edges have an old length,
2, or 11, so the maximum remains at most 11; order only grows.  Induction
therefore proves all `q,r>=0` without using the finite grid as a proof.

Finally, each `C_s` is the unique representative of one residue modulo 11 in
`[20,30]`, all `B_s` are odd and at most 15, and every `c>=20` is
`C_s+11r` for a unique `s` and some `r>=0`.  This verifies the target's
uniform corollary, including its boundary values.

## Strengthening and improvement opportunities

### 1. Proved here: lower the uniform odd-`b` threshold to 13

For source residue `s=9`, the source counts are `(1,13,9)`, its order is 24,
and direct 11-growth at cut 11 produces a simultaneously 2/11-growable path
with counts `(1,13,20)`, order 35, and transported cuts `(32,11)`.  Its
critical intervals `{31,32}` and `{1,...,11}` are disjoint and the safe margin
is tight.  Hence this one-step prefix, not the target's `(1,15,20)` seed,
generates the whole `s=9` slab.  The same argument harmlessly improves `s=5`.

The independently checked seed table is:

| `s` | seed counts | cuts `(2,11)` | order | source |
|---:|---:|---:|---:|---:|
| 1 | `(1,11,23)` | `(1,13)` | 36 | stored |
| 2 | `(1,11,24)` | `(1,12)` | 37 | stored |
| 3 | `(1,9,25)` | `(2,13)` | 36 | stored |
| 4 | `(1,9,26)` | `(2,13)` | 37 | stored |
| 5 | `(1,7,27)` | `(30,10)` | 36 | 11-prefix |
| 6 | `(1,9,28)` | `(5,16)` | 39 | stored |
| 7 | `(1,9,29)` | `(5,16)` | 40 | stored |
| 8 | `(1,9,30)` | `(6,17)` | 41 | stored |
| 9 | `(1,13,20)` | `(32,11)` | 35 | 11-prefix |
| 10 | `(1,13,21)` | `(1,13)` | 36 | stored |
| 11 | `(1,13,22)` | `(1,12)` | 37 | stored |

All second coordinates are odd and at most 13 while the third coordinates are
still exactly 20 through 30.  The same residue argument therefore proves every
`\{1,2^b,11^c\}` with odd `b>=13` and `c>=20`.  The smaller-seed SHA-256 is
`0f82c3b73d55b22d07885d69d9609f0ceff9b3d7f1eaa1ee0967654ba64b5dda`.

### 2. Feasible next improvement: audit the six overlapping prefixes

Eight sources reach order at least 35 after 11-growth alone, but six of those
prefixes have overlapping critical intervals.  The bundled finite grid finds
no failure, and the graph's general safe-margin lemma is intended to cover
them, but this review deliberately does not need them.  A concise formal proof
of the overlapping-interval subdivision case would certify the additional
residue-wise thresholds `B_2=9`, `B_4=B_6=B_7=B_8=7`, and `B_11=11` with a
smaller trust boundary.

### 3. Highest impact: finish the finite-thickness boundary

The result remains a mantle, not the full BHR theorem for support
`{1,2,11}`.  A transition-aware directed cover of the remaining 1,333 claimed
symbolic representatives, with every successor path and surviving mode checked,
is the natural next step.  The optional coverage certificate should be bundled
or independently mirrored in a compact form before the 60-pattern statistic is
treated as archival evidence.

## Literature status and publication readiness

Chand--Ollis, [arXiv:2202.07733](https://arxiv.org/abs/2202.07733), explicitly
leave `{1,2,11}` as the possible exception in their size-three classification.
Ağırseven--Ollis, [arXiv:2402.08736](https://arxiv.org/abs/2402.08736), retain
`a in {1,2}` for odd third length as the possible exception to their large-order
`{1^a,2^b,x^c}` result.  The original growable-realizations framework is
[arXiv:2105.00980](https://arxiv.org/abs/2105.00980).

Exact-phrase, parameter-specific, and arXiv searches on 2026-09-03 found no
prior eleven-residue mantle or uniform odd-`b` threshold 15 or 13.  The target
is graph-novel and apparently new relative to those searches; this is not a
priority claim.  The existence result and the `b>=13` refinement are suitable
for publication as a computer-assisted partial theorem after ordinary expert
copy-editing.  Neither resolves the full support.

## Reproduction and trust boundary

From this directory, with the target certificate available at the cited hash:

```bash
python3 independent_mantle_audit.py \
  /path/to/bhr_1_2_11_transition_repair/small_a_mantle_certificate.json \
  --grid 8
```

The proof trusts the explicit target certificate bytes, exact Python integers,
CPython 3.12.12 execution, the independently written checker, and the short
shortest-arc/induction argument above.  It does not trust a solver, floating
point, network data, a bounded grid as proof of universal quantifiers, the
target code as an implementation dependency, or the optional upstream coverage
certificate.  No active researcher workspace was inspected.  Independent work
in this review comprises target selection, code, transition replay, the
disjoint-interval proof, the two smaller seeds, the improved uniform threshold,
and live literature search.  Inherited evidence is limited to the published
target certificate and its stated source provenance.
