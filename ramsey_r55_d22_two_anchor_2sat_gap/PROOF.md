# A degree-compatible width-two survivor

Fix roots `0` and `3`, and encode red by one.  For every nonroot vertex `z`,
write

```text
sigma(z) = (color(0,z), color(3,z)).
```

An edge between nonroots is **diagonal** if its endpoints differ in both
coordinates.  It then occurs in none of the four monochromatic neighborhoods
of the roots.  Conversely, every nondiagonal edge occurs in at least one of
those neighborhoods.  Thus fixing the four neighborhoods leaves precisely the
diagonal edges as residual variables.

For a five-set `S`, let `D(S)` be its diagonal edges.  If every edge outside
`D(S)` is red, avoiding a red `K5` gives the residual clause

```text
OR_{e in D(S)} (not x_e).
```

If every edge outside `D(S)` is blue, the analogous clause is

```text
OR_{e in D(S)} x_e.
```

Here `x_e` is the red indicator.  These are all constraints on diagonal edges
that can be inferred from the four fixed neighborhoods alone.

The supplied matrix has cell sizes `(10,11,10,10)`, hence 210 diagonal edges.
Its exact red degree multiset is `20^8 21^26 22^9`, with 452 red edges.  The
four neighborhood profiles are

```text
(0,R,22,108,6), (0,B,20,100,0),
(3,R,21,99,8),  (3,B,21,98,9).
```

Direct enumeration produces 413 distinct residual clauses of width one or
two.  The diagonal colors already stored in the matrix satisfy every one of
them.  Thus this is not merely an abstract 2-SAT assignment: the same assignment
also realizes the exact global edge count and degree bounds.

The first remaining defects have width three.  For example, the red `K5`

```text
{1,9,16,27,40}
```

has diagonal edges `{1,27}`, `{9,40}`, `{16,27}` and violates the ternary
red clause saying that at least one must be blue.  The blue `K5`

```text
{1,2,6,13,34}
```

has diagonal edges `{1,34}`, `{2,34}`, `{6,34}` and violates the analogous
ternary blue clause.  Exhaustive enumeration finds no monochromatic `K5` with
fewer than three diagonal edges.

The construction is therefore an exact limitation witness: even the complete
width-at-most-two residual system, together with the original edge and degree
requirements, does not exclude this `d=22`, deficiency-six incidence family.
The next omitted global interface has arity at least three.  The construction
is not a Ramsey graph; it has 162 red and 204 blue monochromatic five-sets, all
of diagonal width three, four, or six.

