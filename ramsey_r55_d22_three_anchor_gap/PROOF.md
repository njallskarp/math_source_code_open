# The seven-variable third-anchor obstruction

Let `x_ab=1` mean that edge `{a,b}` is red.  Fix the four complete
monochromatic neighborhoods of roots `0` and `3` from `BASE_WITNESS.json`.
The 210 edges whose endpoint signatures are complementary in both root
coordinates remain free.  Every other edge is fixed.

Promote vertex `1` to a third anchor.  Its red neighborhood must contain
neither a red `K4` nor a blue `K5`, and its blue neighborhood must contain
neither a blue `K4` nor a red `K5`.  Eight instances of these four conditions
give the following clauses.  Their exact vertex origins are in
`CERTIFICATE.json` and are reconstructed by `verify.py`.

```text
(1)   x_1,27
(2)  !x_20,32 or !x_1,32
(3)  !x_16,32 or !x_1,32
(4)  !x_1,37  or !x_1,31
(5)  !x_1,30  or !x_1,27
(6)   x_1,30  or  x_1,37
(7)  !x_1,32  or  x_16,32 or x_20,32
(8)   x_1,30  or  x_1,31  or x_1,32
```

These clauses contradict by unit propagation.  Clause (1) and then (5)
force `x_1,30=0`; (6) forces `x_1,37=1`; (4) forces `x_1,31=0`; and (8)
forces `x_1,32=1`.  Clauses (2) and (3) then force both `x_20,32=0` and
`x_16,32=0`, making (7) false.

Thus no coloring of all 210 free edges makes vertex `1` a valid third anchor.
The other 203 free edges do not occur in the proof.  Since every `R(5,5;43)`
coloring would satisfy the local conditions at every vertex, no completion of
this fixed two-anchor incidence can be a Ramsey coloring.  This conclusion
does not use a degree bound or total-edge equation after the incidence is fixed.

The core is deletion-minimal.  The standard-library checker enumerates all
`2^7=128` assignments, finds no satisfying assignment, and finds a satisfying
assignment after deleting any one clause.  The independent NetworkX checker
instead instantiates the seven edge colors and directly observes a forbidden
colored set at vertex `1` for every assignment.

This is an exact-instance exclusion, not a classification of all two-anchor
incidences and not an exclusion of the full `d=22,t>=108` family.  Its useful
boundary is that the height-2851 short-clause survivor fails immediately when
one full third-anchor interface is imposed.  A family-wide argument must now
control which two-anchor incidences can occur; increasing the clause-width
prefix on this one incidence is unnecessary.
