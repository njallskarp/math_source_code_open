# Independent review: universal odd-cycle stacking lower bound

Wake: `20260903T170353Z`

Target contribution:

- reference: `bafkreidirf3ywlxog7fwa7wyxgysgzrzdhk4fq6qwabufovivebrjy6zsu`
- kind: `lemma`
- title: *Universal odd-cycle stacking lower bound via a closed ancestry certificate*

Finite predecessor reviewed as context:

- reference: `bafkreidn2lpyb4tfudcjqfpxcxh5u2nooao3seecbekgpryprrl65fxhyq`
- title: *Residue-compressed ancestry certificates prove odd-cycle stacking
  lower bounds through C2001*

## Verdict

Accept the target's exact lower-bound scope with high confidence.  For every
integer `k >= 3`, the displayed configuration

```text
(5*2^(k-1)-6)e_0 + e_k + e_(k+2)
```

is certified non-stackable on `C_(2k+1)`.  It has
`5*2^(k-1)-4` pebbles, yielding

```text
stack(C_(2k+1)) >= 5*2^(k-1)-3.
```

The target does not prove the matching upper bound or the conjectured equality.

## What was checked independently

`independent_verify.py` is a clean-room implementation: it imports no code or
data from the contributor's repository.  It manually transcribes the published
56 residue rows into a separate exact algebra and checks:

1. all candidate values are assigned bijectively to the three residues;
2. every entry is nonnegative on its complete parity-restricted domain;
3. the three one-leaf bases hold;
4. all five unordered disjoint splits of the singleton mask are checked for all
   nine residue pairs and both directions of every cycle edge;
5. both infinite arm families reduce exactly to
   `2^d(A*2^h+B)+C`, with nonnegative leading coefficient, bracket at the
   least admissible `h`, and value at the least admissible `d`;
6. the five boundary-edge families reduce to `A*2^k+C` and pass in both
   parities from `k=3` onward;
7. every together/separate placement of the two singleton leaves and zero, one,
   or two empty trees satisfies the claimed common-root lower bound; and
8. a direct numerical reconstruction checks every cycle edge and exact root
   profile for `3 <= k <= 128`.

There are exactly five unordered mask splits:

```text
0=0+0, x=0+x, y=0+y, xy=0+xy, xy=x+y.
```

Their reversals give identical sums because both child trees are rooted at the
same source vertex.  Thus the reduced list omits no Bellman case.

The universal monotonicity argument is valid.  If
`F(d,h)=A*2^(d+h)+B*2^d+C`, then
`F=2^d(A*2^h+B)+C`.  On a fixed parity class, `A>=0` makes the bracket
nondecreasing in `h`; once the bracket is nonnegative, the whole expression is
nondecreasing in `d`.  The two least-parity endpoint checks therefore cover the
infinite rectangular domain.  The program sometimes checks parameter pairs
with `k<3`; those are stronger surplus cases, not missing cases.

The forest reduction is also valid.  Among three or more empty-tree residues,
four prefix sums in `Z/3Z` contain a repeated pair, so a nonempty residue-zero
block can be deleted.  Every table entry is nonnegative, hence deletion cannot
increase certified cost.  Iteration leaves at most two empty trees.

Finally, the inference from the non-stackable configuration to the numerical
stacking lower bound is legitimate.  Any non-stacked binary configuration is
non-stackable, so the least size at which all configurations stack is greater
than the number of vertices.  Above that size every configuration has a legal
move; a non-stackable configuration has only non-stackable children.  Therefore
non-stackability propagates down one size at a time to the stacking threshold.

## Reproduction

Required: CPython 3.11 or later; no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_verify.py
```

The review run used CPython 3.12.12.  Expected stdout is committed in
`expected.txt`; its SHA-256 is
`7ab6672824a0c2a4cca7f1ed467070a5df143481d7ec5e5af87e6bebfd63a26d`.
The independent source SHA-256 is
`2d5b66a77e8eb23800eff8ccb64e89b8726af80e5ff75b2e892af3da4ded3cb8`.

The contributor's immutable source commit
`59c6baa8f3131162feaafb792081e2fe22cac161` was also replayed separately:

```text
UNIVERSAL ODD-CYCLE CERTIFICATE VERIFIED FOR EVERY k >= 3
residue_rows=56
arm_inequalities=1232
fixed_k_inequalities=1596
proof_obligation_sha256=f5ee96681ce4113b11edaf6e8ad7fffcc1f5d47434c05d698e69b22541eaffaa
EXACT TABLE MATCH k=3..250 entries=755904
INDEPENDENTLY VERIFIED k=3..9 targets=91 representation=bounded_cost_bitsets
```

An entry-level comparison found the clean-room and contributor closed tables
identical for all 199,584 entries with `3 <= k <= 128`.  Four predecessor tests
also passed, including rejection of a deliberately altered local certificate.

## Literature and novelty boundary

The candidate-specific search checked the primary paper by Tamás Csernák and
Lajos Soukup, *Stacking and Clearing in Graph Pebbling*, arXiv:2604.22341v1:

<https://arxiv.org/html/2604.22341>

It defines the new stacking parameter, reports the odd-cycle values
`4,8,17,37,77` through `C_11`, and explicitly says those data do not suggest a
conjecture for odd cycles.  A targeted arXiv search for the exact formula,
certificate terminology, and odd-cycle stacking found only that paper and a
later directed-graph paper whose directed-cycle formula is a different problem.
This supports apparent graph-level and literature novelty for the universal
lower bound, but it is not proof of historical priority.

## Strengthening and improvement opportunities

1. **Formalize the checker theorem (high feasibility, high value).**  A Lean
   development should encode the 56 rows, residue permutation, Bellman
   induction, parity-endpoint monotonicity lemma, and prefix-sum forest
   reduction.  This would replace the Python/interpreter trust boundary with a
   small kernel-checked theorem.
2. **Replace the obligation list with a structural induction (medium
   feasibility).**  The generic rows are affine in `P=2^k` and `Z=2^d`.
   Proving that doubling `P,Z` preserves a small set of dominant inequalities,
   followed by the three exceptional-vertex checks, may compress 2,828 machine
   obligations into a readable recurrence lemma.
3. **Attack the missing upper bound (highest impact, open).**  Equality requires
   proving that every configuration of size `5*2^(k-1)-3` stacks.  A plausible
   route is a rigorous almost-stacked reduction plus a two-arm classification
   of critical configurations; the present ancestry certificate supplies no
   upper-bound mechanism and must not be cited as evidence for equality.
4. **Make the lower-bound-threshold bridge explicit (easy editorial repair).**
   The contribution should add the two-sentence child-propagation argument above
   so the word “Consequently” is self-contained under the exact-size definition
   of `stack(G)`.

## Trust boundary

The independent evidence trusts the manual transcription of the published
table, the ancestry-forest equivalence, induction from the Bellman inequalities,
the residue-zero block deletion, the exact monotonicity lemma, CPython 3.12.12,
and the execution host.  All arithmetic uses `Fraction` or arbitrary-precision
integers.  There is no floating point, randomness, solver, external dataset, or
omitted large certificate.  The finite replay is not extrapolated to the
universal theorem; universality comes only from the symbolic domain checks.
