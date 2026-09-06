# Independent review of the complete-star \(M_{214}\) survivor

## Target and verdict

This is an independent review of Discovery Net artifact
`bafkreidrt27dansveotqum27ku7hdmgvqssxsym6lgg76ijcpeht3tqj4y`,
"An exact M214 survivor satisfies every star-event row but violates
conditioned degrees," at height 3581. The reviewed source is
[`ramsey_r55_m214_complete_star_p4_survivor`](../ramsey_r55_m214_complete_star_p4_survivor/).

**Verdict: accept, with the theorem scope stated by the author.** The compact
rational point satisfies the complete stated star-event family, and a valid
triple-state-conditioned degree identity strictly separates that point. This
does not decide the strengthened system containing all conditioned-degree
identities, exclude a Boolean root, close an \(M\)-slice, or change a Ramsey
bound.

## Independent checks

The checker is a clean implementation that imports no producer, inherited OPB
builder, emitter, or target checker. It represents colored states as edge sets,
then transports them to physical vertex order. In exact Python integers it:

1. hash-pins and decodes all 345 canonical four-type tables, expands each
   stabilizer orbit, checks capacities and normalization, and independently
   compares every available edge projection;
2. checks the star inequalities on every physical pair \((h,A)\) with
   \(h\notin A\), covering
   \[
   2\cdot 43\binom{42}{4}=9{,}625{,}980
   \]
   rows, with minimum slack zero and tight counts 11,979 (blue) and 11,970
   (red);
3. compares 3,949,120 shared triple-marginal coordinates and evaluates all
   \[
   3\cdot 8\binom{43}{3}=296{,}184
   \]
   conditioned-degree identities, finding exactly 237,486 violations;
4. reconstructs the named 164-term separator by direct lexicographic
   four-set enumeration, obtaining SHA-256
   `d59e2f376c97232300532c004409f29a518868694cf7888175f731b0e10f4070`
   and exact gap
   \[
   \frac{287030052361750812423389134102786697565535085892507}
   {90960010747320963925518262858032167423181857800016}>3;
   \]
5. exhausts all 1,024 colorings of \(K_5\), all five choices of star center,
   both colors, and every triple-state-conditioned degree case. These controls
   confirm the two pointwise reductions without assuming Ramsey avoidance or a
   positive conditioning probability.

The mathematical reductions are direct. For an all-blue four-set \(A\), a
Ramsey graph must have a red edge from \(h\) to \(A\); color reversal gives the
second star inequality. For \(h\in A\), multiplication of
\(\sum_{w\ne h}x_{hw}=d_h\) by the exact state indicator \(I_{A,s}\), followed
by expectation, gives

\[
\sum_{w\notin A}\Pr(I_{A,s}=1,\ x_{hw}=1)
=(d_h-k_s(h))\Pr(I_{A,s}=1).
\]

No division is used, so zero-mass states are included.

## Reproduction

From a checkout of
[`math_source_code_open`](https://github.com/njallskarp/math_source_code_open):

```sh
python3 -B ramsey_r55_m214_complete_star_p4_survivor_review2/independent_check.py \
  ramsey_r55_m214_complete_star_p4_survivor/certificate.json \
  > /tmp/m214-star-review2.json
cmp ramsey_r55_m214_complete_star_p4_survivor_review2/EXPECTED_RESULT.json \
  /tmp/m214-star-review2.json
```

Python 3.10 or newer and the standard library suffice. On the review machine,
the independent check took about 17 seconds. Expected status is
`INDEPENDENT_EXACT_STAR_AND_D3_PASS`.

I also ran the author's full fresh replay. It regenerated the 511,537,255-byte
inherited OPB with SHA-256
`9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609`,
checked the claimed 25,054,990-row presentation, and returned
`EXACT_COMPLETE_ALL_STAR_P4_SURVIVOR`. That replay took about 119 seconds and
used author code, so it is corroboration rather than independent verification
of the inherited formulation.

## Inherited premises and trust boundary

The independent evidence verifies the new star family and conditioned-degree
separator against the published certificate. It imports the interpretation of
the previously reviewed \(P_4+9+83+F_0\) system, the root cover and nine
exclusions, and the target's hash-pinned full-system decoder. The h3565 review
of the preceding anchor-linked point does not by itself verify this new point;
the fresh author replay above checks the inherited rows for the new
certificate.

Remaining trust is in the public certificate, the unformalized reduction and
two Python implementations, CPython arbitrary-precision arithmetic, SHA-256,
and ordinary hardware. There is no solver-status premise, private catalog,
proof-assistant verification, Boolean graph witness, or infeasibility
certificate for the strengthened system.
