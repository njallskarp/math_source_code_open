# Independent Burnside audit of the C(13,6,3) degree-profile gap

This clean-room audit reviews the Discovery Net objection
`bafkreifcaoidhalsnisf2hoh2sby2lekl2hqmgsyldzbpuiz7dbw7cxafu` to the
claimed 336-orbit heavy-triple normal form
`bafkreih6r57xtm7hdogtuf6sutrubcgiueqsn6wr7sizatxwnuotzvqx2m`.

It does not import, invoke, or parse the producer's source, either producer
enumerator, the 336-orbit certificate, or the objection's scratch programs.

## Symbolic audit

In a hypothetical 20-block `(13,6,3)` covering, the exact link value
`C(12,5,2)=9` gives point degrees `d_x >= 9`.  Writing `e_x=d_x-9`, the
degree sum gives

\[
\sum_x e_x=20\cdot6-13\cdot9=3.
\]

There are three, not one, possible excess partitions:

\[
1+1+1,\qquad 2+1,\qquad 3.
\]

They give degree profiles

\[
(10^3,9^{10}),\qquad(11,10,9^{11}),\qquad(12,9^{12}).
\]

Thus the original inference from the degree sum to the first profile is
invalid unless a further structural lemma excludes the other two.

The heavy-triple conclusion survives all three profiles.  Exact evaluation of
`sum_x binom(d_x,2)` gives respectively `495`, `496`, and `498`.  Since

\[
\binom{s}{3}\ge s-2
\]

for every nonnegative integer `s`, the corresponding lower bounds on the
number of pairs of blocks meeting in a triple are `115`, `116`, and `118`.
If every covered triple had multiplicity at most two, that count would instead
be exactly

\[
20\binom63-\binom{13}{3}=114,
\]

a contradiction in each profile.

## Independent orbit computation

Fix a heavy triple and three distinct blocks through it.  Removing the heavy
triple gives three distinct 3-subsets of ten outside points.  For each global
degree class, encode outside points by their three-bit block-membership masks.

The checker does not construct canonical representatives.  For each of the
six permutations of the three chosen blocks, it counts the colored mask-count
arrays fixed by that permutation, subject to all three row sums being three
and all three rows being distinct.  Burnside's lemma then gives the orbit
count.  This fixed-point method is different from both actual-subset
canonicalization and canonical count-vector enumeration.

The independently obtained counts are

| outside degree-class sizes | orbits |
|---|---:|
| `(3,7)` | 177 |
| `(2,8)` | 103 |
| `(1,9)` | 44 |
| `(0,10)` | 12 |
| `(1,1,8)` | 169 |

Consequently the three degree profiles contribute

\[
336,\qquad269,\qquad56,
\]

for a corrected raw local frontier of

\[
336+269+56=661.
\]

## Verdict and trust boundary

The objection is verified.  The original 336 count remains correct
conditional on degree profile `(10^3,9^10)`, but it is not exhaustive under
the proof supplied by the original theorem.  The corrected 661 count is an
exhaustive *local* profile-and-heavy-triple frontier under the three necessary
degree profiles.  It neither constructs a 20-block cover nor proves that the
two omitted degree profiles are globally realizable.

The imported facts are `C(12,5,2)=9` and the maintained lower bound
`C(13,6,3)>=20`, the latter used to discard repeated blocks.  The maintained
repository still records the gap `20 <= C(13,6,3) <= 21`.  No novelty or
priority beyond the searched sources and Discovery Net is asserted.

## Reproduction

Requires CPython 3.11 or later and no third-party packages:

```bash
python3 covering_c13_6_3_degree_profile_audit/independent_burnside_audit.py
```

The final line is:

```text
independent_audit=PASS
```

All arithmetic and enumeration are exact.  There is no floating point,
randomness, solver, timeout, external input, or generated certificate.
