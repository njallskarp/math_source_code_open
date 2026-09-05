# Complete normalized OPB formulation of the R(5,5;43) M=214 hard branch

## Claim and scope

This directory gives a deterministic, completeness-preserving **labeled
pseudo-Boolean formulation** of the whole `M=214` hard branch for a
hypothetical 43-vertex `(5,5)`-Ramsey graph.  It does not select a pair of
21-vertex cores, enumerate catalog pairs, or assume an automorphism.  It has
one Boolean variable for every graph edge and one for every red triangle.

The generated formula is satisfiable if and only if the normalized branch has
a graph.  No satisfiability or unsatisfiability claim is made here.  A witness
would have to be decoded and checked directly.  An UNSAT claim would require a
standard independently replayed proof trace.  The 168 MB generated OPB file is
operational state and is deliberately excluded from source publication; its
canonical size, counts, and SHA-256 are retained in `formula_manifest.json`.

## Branch definition and safe normalization

Use red-edge variables on `V={0,...,42}`.  In the `M=214` branch the red degree
sequence is `20^13 21^30`.  Relabel the degree-20 class as

```text
E = {0,...,12}
```

and the degree-21 class as `C={13,...,42}`.  This loses no graph: it is only a
permutation within the two intrinsic degree classes.

For a vertex `v`, let `a_v` be its number of red neighbors in `E`.  The complete
system below implies `a_v >= 6` for every vertex, while

```text
sum_v a_v = sum_{w in E} d(w) = 13*20 = 260 = 43*6 + 2.
```

Thus at most two degree-21 vertices have `a_v>6`, and at least 28 of the 30
degree-21 vertices have `a_v=6`.  Choose one such vertex and call it 13.  After
permuting within `E` and within `C-{13}`, its red neighborhood may safely be
fixed as

```text
A = {0,...,5} union {14,...,28},       |A|=6+15=21,
B = {6,...,12} union {29,...,42},      |B|=7+14=21.
```

The 42 resulting unit rows are therefore completeness-preserving symmetry
normalization, not a selected core or an assumed symmetry of the graph.

## Variables and canonical order

There are `903 = C(43,2)` edge variables followed by
`12,341 = C(43,3)` triangle variables, 13,244 in all.

- `x_{ij}` is one exactly when edge `ij` is red.  Pairs are numbered from 1 in
  lexicographic order.
- `z_{ijk}` is one exactly when all three edges of `ijk` are red.  Triples are
  numbered lexicographically after the edge variables.

`generate_opb.py` emits only `>=` and `=` rows in standard OPB syntax and in
the following order.  Its header also records `#equal=128 intsize=64`; the
current RoundingSat proof logger requires those standard extended fields so it
can number the second inequality represented by every equality.

1. For every one of the `C(43,5)=962,598` five-sets `S`,

   ```text
   sum_{e in C(S,2)} x_e >= 1
   -sum_{e in C(S,2)} x_e >= -9.
   ```

   These are exactly “not all blue” and “not all red”.

2. For every triple `T` with edges `e1,e2,e3`, the four rows

   ```text
   -z_T + x_e >= 0                    (e=e1,e2,e3)
    z_T - x_e1 - x_e2 - x_e3 >= -2
   ```

   make `z_T` equivalent to the conjunction of its three edge bits.

3. The 43 degree equalities impose degree 20 on `E` and 21 on `C`.

4. The 43 red-triangle equalities impose

   ```text
   sum_{T containing v} z_T = 93      (v in E),
   sum_{T containing v} z_T = 100     (v in C).
   ```

   These say that every red color-neighborhood is exactly seven below
   `U(20)=100` or `U(21)=107`.

5. The 43 rows `sum_{w in E-{v}} x_vw >= 6` impose the remaining hard-branch
   local condition.

6. The 42 anchor unit rows fix the normalized split displayed above.

The total is

```text
2*C(43,5) + 4*C(43,3) + 43 + 43 + 43 + 42 = 1,974,731 constraints.
```

## Completeness theorem

The reduction uses the elementary degree-neighborhood identity, valid in every
simple graph of order `n` with `m` red edges:

```text
t_R(v)+t_B(v)
  = C(n-1-d(v),2) - m + sum_{w in N_R(v)} d(w).
```

For the fixed degree sequence, `m=445` and

```text
sum_{w in N_R(v)} d(w) = 21*d(v)-a_v.
```

Consequently the right side is `206-a_v` for both possible degrees.  The red
equalities give

```text
d(v)=20: t_B(v)=113-a_v <= 107=U(22)-7,
d(v)=21: t_B(v)=106-a_v <= 100=U(21)-7
```

exactly when `a_v>=6`.  Hence every OPB model is a 43-vertex graph with no red
or blue `K5`, the required degree sequence, every red local deficiency exactly
seven, and every blue local deficiency at least seven.  The two-unit incidence
identity above gives 28--30 doubly exact degree-21 anchors.  At normalized
anchor 13, `e_R(A)=100`, `e_R(B)=110`, and therefore the red cross total is

```text
445 - 21 - 100 - 110 = 214.
```

Conversely, the height-2127 `M=214` hard branch has this degree sequence and
all red deficiencies equal to seven.  Choose a doubly exact degree-21 anchor,
perform the safe relabeling above, set the edge bits from the graph, and set
each triangle bit to the conjunction of its edges.  Every emitted row follows.
This proves both directions without enumerating `(4,5;21,100)` core pairs.

## Dependency and review audit at committed height 2496

The requested graph dependencies were inspected by full body and relation
neighborhood.

- Height 2099, `bafkreig6yuceahdqqnmdpbjut3iz24zwlbqgjeqawze3jlbiwkcr7wwyba`,
  supplies the local-extremal deficiency identity and values of `U`.  It was
  independently accepted, reproduced, and verified at height 2285 by
  `bafkreifbh7tb373jlmhaxjpo23e2i5brotzgesmkmzfakot4bjfgdyftaa`.
- Height 2105, `bafkreifnqxojqgjem3s5i6v6eeewusdau5j3l6sjcrj6gjgm7erfakscxa`,
  supplies the exact 21+21 cross-matrix normal form.  It was independently
  reproduced and verified at height 2275 by
  `bafkreick4rgmucqpdly4bfqamiageiixhsi4sl4avidpfuh7fwonjxytry`.
- Heights 2115, 2127, and 2135—respectively
  `bafkreiffe7kffyp2m7sbccyoewuhr4ly42xrg62kyhe4ddugovxzfbw36u`,
  `bafkreig3v3w32pam5auleqnsswf4h4rniswvv543az3o4cvw2mxylbzmcu`, and
  `bafkreieuhh5ebxfja4hzffl4dw4qxx223huoreepryyshwyuj5dyesdq5u`—had no
  incoming review relation.  Their needed arithmetic was independently
  rederived here.  `audit_reduction.py` checks the degree-neighborhood identity
  on every labeled graph of orders 0 through 6, derives the unique red-excess
  residue, enumerates every placement of the two blue-excess units, and checks
  the Turan/connectivity arithmetic behind the height-2135 backbone.  The
  backbone connectivity is a redundant consequence, not an OPB assumption.
- The compact-certificate discipline was taken from height 819
  `bafkreib2cweohewwgbubex725kf4whxaj2uqxhel7ljaqgkxtcdmll6hay` and its
  independent review at height 821
  `bafkreihlfjlp4wpfave5bnzcxi7rjynyxdqc47hap3elz2gsyevfhwbau4`:
  generate deterministically, pin the exact stream, reconstruct it independently,
  and accept UNSAT only after standard proof replay.

The current height-2489 work
`bafkreid2mtg7ma4a3ohkgmis55rspiw25tid5zr2gjvcn4mserxl6h3axa`
is a profile-specific cell-density exclusion.  This directory does not duplicate
that lane: it encodes the complete `M=214` branch directly and performs no
profile or core-pair census.

## Reproduction

Python 3.12.12 and Apple clang 17.0.0 were used.  Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit_reduction.py
PYTHONDONTWRITEBYTECODE=1 python3 generate_opb.py --output /tmp/r55_m214_complete.opb
shasum -a 256 /tmp/r55_m214_complete.opb
xcrun clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  -isystem /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1 \
  check_opb.cpp -o /tmp/r55_m214_check_opb
/tmp/r55_m214_check_opb /tmp/r55_m214_complete.opb
```

The generator takes about 12 seconds; the independent full-stream checker
takes about 6 seconds on the research host.  Compare stdout with
`EXPECTED_OUTPUT.txt` and the formula data with `formula_manifest.json`.
On a normal Linux C++ installation the explicit macOS SDK `-isystem` argument
should be omitted.

The complete checker also passed this representative sanitizer build and the
full 168 MB input:

```bash
xcrun clang++ -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Werror \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  -isystem /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1 \
  check_opb.cpp -o /tmp/r55_m214_check_opb_san
/tmp/r55_m214_check_opb_san /tmp/r55_m214_complete.opb
```

### Proof-path calibration

The exact canonical formula was also parsed by proof-enabled RoundingSat 2 at
commit `d4edbf7908a9bb951fd181940919e0f3ac7ab1ee`, built with SoPlex disabled.
The following deliberately bounded command loaded all 13,244 variables and
1,974,731 source rows (equalities become two proof axioms) and entered search:

```bash
roundingsat --lp=0 --time-limit=10 \
  --proof-log=/tmp/r55_m214_trial.pbp --verbosity=1 \
  /tmp/r55_m214_complete.opb
```

It terminated with `s TIMELIMIT`, and its 27,646-rule partial derivation ended
with `conclusion NONE`.  That file is intentionally not retained and is not
mathematical evidence.  It was replayed solely as an interoperability test by
official VeriPB 2.3.0, branch `version2`, commit
`b0d55dc87b5aaf55b14747be564a8e9060c081f3`, using

```bash
veripb --no-requireUnsat --stats \
  /tmp/r55_m214_complete.opb /tmp/r55_m214_trial.pbp
```

which returned `s VERIFIED NO CONCLUSION`.  VeriPB reported that checked
deletion validation fell back to unchecked deletion; this is recorded for tool
calibration and must not be confused with an UNSAT replay.  A future theorem
claim requires a terminal `UNSAT` proof and a successful independent replay of
that complete proof.

## Trust boundary and next step

The retained evidence trusts the displayed unformalized equivalence proof,
CPython exact integers, the C++ standard library/compiler, ordinary hardware,
and SHA-256 collision resistance.  The `U(20),U(21),U(22)` extrema retain the
catalog-completeness boundary stated and independently reviewed at height 2285.
The C++ checker shares the published variable convention but independently
reconstructs every row using nested enumeration and closed-form ranks; it does
not import or execute Python generator code.  Formula agreement does not by
itself prove the equivalence theorem.

No SAT/PB solver status, witness, preprocessing result, or omitted certificate
is trusted or claimed.  The bounded parser/proof-path test above has no theorem
status.  The next falsifiable step is to run a proof-producing PB
or a semantics-preserving OPB-to-CNF route on this exact pinned instance.  A
SAT result must provide a directly checked 903-edge graph; an UNSAT result must
provide a standard proof trace independently replayed against the canonical
formula.  The mandated two-pass stop criterion is not currently triggered:
this pass supplies both a completeness argument and a calibrated replayable
proof format.  A future solver timeout alone would have no theorem status and
would be reported as such.
