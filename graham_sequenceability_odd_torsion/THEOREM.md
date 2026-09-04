# Odd-torsion false terminals in the rational-span sequencing search

Let a search node carry zero-sum interval rows in `Z^k`, as in Section 3 of
Costa--Della Fiore--Fontana--Vena.  A zero/equality terminal is *sound for
arbitrary abelian groups* only when the corresponding basis vector or basis
difference is in the **integer** row lattice.  Rational row-span membership
only places a nonzero integer multiple there and can therefore lose torsion.

## The certificate

For `k=6`, start at the identity ordering and make the five inclusive interval
moves

```text
[1,5], [2,4], [0,2], [2,3], [3,5].
```

Here a move records the labels in the displayed interval and then swaps the
left endpoint with its predecessor, except at left endpoint zero, where it
swaps the right endpoint with its successor.  The recorded rows are

```text
r1 = 0 1 1 1 1 1
r2 = 0 0 1 1 1 0
r3 = 1 1 1 0 0 0
r4 = 1 0 0 1 0 0
r5 = 1 0 0 0 1 1.
```

No proper prefix has a basis vector or basis difference in its rational row
span.  At depth five,

```text
-r1 + r3 + r4 + r5 = 3 e1,
 r1 - r3 + 2 r4 - r5 = 3 e4.
```

Consequently the rational rule declares zero-element terminals `e1` and
`e4`.  But over `F_3`, the five rows have rank four and their row space
contains no basis vector or basis difference.  In the quotient group

```text
G_6 = F_3^6 / row_F3(r1,...,r5),
```

the six labels `a_i=[e_i]` are therefore pairwise distinct and nonzero, while
every recorded row sums to zero.  Thus the terminal inference is false in an
odd-torsion group.

## Parameterized families

Append zero columns to the five rows.  The same five moves are legal in the
general search for every `k>=6`; extra labels remain fixed to the right.  The
quotient

```text
G_k = F_3^k / row_F3(r1,...,r5)
```

has dimension `k-4`, and all `a_i=[e_i]` remain distinct and nonzero.  This
gives a false rational terminal for every set size `k>=6`.

For `k>=8`, all five intervals also obey the paper's zero-sum restriction
`j-i <= floor(k/2)`.  Quotient further by the all-ones relation:

```text
G_k^0 = F_3^k / row_F3(r1,...,r5,(1,...,1)).
```

This group has dimension `k-5`.  The labels are still distinct and nonzero:
the at least two appended coordinates force the coefficient of the all-ones
row to vanish in any putative basis or basis-difference relation, reducing to
the already excluded six-coordinate case.  Moreover `sum_i a_i=0` by
construction.  Hence the rational zero/equality terminal rule fails on a
legal zero-sum branch for every `k>=8`, including every size in the claimed
range through 22.

This is not a counterexample to sequenceability, the Graham/Alspach
conjecture, or the paper's numerical theorems.  It is a parameterized
counterexample to the stated rational-row-span justification.  A repaired
proof computation must use integer-lattice membership (for example, Hermite
or Smith normal form) and provide auditable terminal/exhaustion certificates.
