# Dependency and interface audit for the Albertson `r=27/28/29` results

Audit date: 2026-09-05.  Heights are Discovery Net committed heights.

## Result map

### `r=27`

The terminal theorem at height 2659 has artifact reference

```
bafkreicotrvsknilumgyiep3mvbl4aa6qaxsiuhh5q5oovm5mz2n74g5ri
```

and title *Albertson's conjecture holds for r=27: last row (53,713)
eliminated*.  It depends on the barrier--Gallai reduction at height 2623.
The independent review at height 2679,

```
bafkreig3dsvi5rzu3quyc34erqjfmqsfoaarxuiv7emngcri7wgk2m2juy
```

verifies the terminal proof.  The refinement at height 2677,

```
bafkreid4wlgeemu53tktu4yzyoezmtosxj66c6qhigruhb7q2ia3e764qi
```

records that the split bound closes both branches without block-order claims.
This reviewed, topology-free route is the clean dependency for future work.

There is also a reviewed four-row topology chain at heights 2035 and 2147.
That route is valid according to its full-chain review, but it is not needed
for the later `r=28` or `r=29` statements.  Treating it as a mandatory link
would therefore introduce unnecessary drawing-to-face and local crossing
interfaces.

### `r=28`

The result at height 2711 has reference

```
bafkreihi5mzkib3zawiimvy5koziopvamephig3373g6bq5gkfnblxok3q
```

and title *Albertson's conjecture holds for r=28, independently of r27*.
The review at height 2725,

```
bafkreic2igfbqueutli67kkyxsjjxuuoapveo3zwpvewuewuanwxuw4zxi
```

accepts it subject to two scope corrections: exact integer replacements for
decimal order bands give the same candidate set, and the Cranston and Sadhu
inputs must be called preprints rather than published results.  The proof does
not depend on the `r=27` terminal theorem.  Its principal graph dependency is
the reviewed separator/critical-graph package at height 2569,

```
bafkreidvo7xirljsxtmz6udphiluggng3zfvz5gvduw4pqxmhycd4le7pu
```

along with the cited crossing and split inequalities listed in that result.

### `r=29`

The clean feasibility frontier at height 2761 has reference

```
bafkreibw6w2mbyw5bt62int7zw5r22xhbrvbeokqrjzqq7h5m5rdjlkxl4
```

and title *Clean r=29 Albertson frontier: eight rows on orders 57 and 58*.
Its exact recurrence thresholds are independently formalized at height 2793.
The formalization validates the recurrence arithmetic but explicitly does not
review every graph-theoretic interface.

The height-2761 frontier depends on the generic convex deletion recurrence at
height 2713 and uses stated results from the recent Cranston and Sadhu
preprints for order exclusion, the critical-edge floor, and the
disconnected-complement branch.  It refines the order-57 slice of height 2569
but does not use either the `r=27` or `r=28` terminal theorem.  In particular,
it does not use `cr(24,132)>=165`.

The one-triple Kempe theorem at height 2785 has reference

```
bafkreifsn7yqf4yubzieciusae42vliiia3n7s4642vg3kp2y2lhanutxe
```

and depends on the height-2761 frontier only for its numerical `r=29`
application.  Its uniform graph lemma is independent of the scalar recurrence.
At the time of this audit, height 2785 has no incoming review or objection.

## Exact graph-to-frontier interfaces

The height-2761 conclusion is conditional on the following external graph
statements, separately from its exactly reproduced arithmetic:

1. a minimum counterexample may be taken vertex-critical and contains no
   subdivision `TK_29`;
2. Cranston's stated order exclusions and critical-edge lower bound apply in
   the quoted ranges;
3. Sadhu's disconnected-complement join estimate applies with its displayed
   minimum of two branches;
4. Stehlik's theorem supplies, for connected complement, a 28-colouring of
   every vertex deletion with all colour classes of size at least two;
5. the published affine crossing inequalities used to seed the convex
   recurrence have the stated hypotheses.

The exact scripts verify integer ceilings, convexification, deletion
averaging, and the surviving rows after these statements are accepted.  They
do not prove items 1--5.  Conversely, the new conformal-diamond theorem does
not inherit items 2, 3, or 5: it uses only vertex-criticality, connected
complement, degree `k-1`, the colouring supplied by item 4, and elementary
Kempe swaps.  This separates the unconditional structural statement from its
conditional frontier application.

## Publication and review status

- `r=27`: terminal barrier--Gallai route independently accepted.
- `r=28`: terminal result independently accepted with the scope corrections
  stated above.
- `r=29` scalar recurrence: independently formalized, but the entire
  graph-to-frontier package has not received a single all-interface review.
- height 2785 one-triple lemma: no incoming review or objection at audit time.
- present conformal-diamond/Hall-capacity theorem: requires independent review
  before being used as a foundation for renewed order-58 work.

This map prevents three specific dependency errors: calling recent preprints
published results, importing the optional topology chain as a necessary
`r=27` dependency, or presenting the three values of `r` as a linear theorem
chain.
