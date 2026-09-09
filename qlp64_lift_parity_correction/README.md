# Correction: invalid quarter-entry parity in the QLP(64) cover

**The full-family exclusion in `qlp64_fixed_multiplier_exclusion` is withdrawn.**
Its generator discarded valid compressed children. This invalidates the claimed
coverage and leaves its nontrivial-fixed-multiplier exclusion and affine
corollary unsupported. The computed zero-witness results still describe the
supplied queues. This correction does not exhibit a QLP(64), and it does not
show that the withdrawn mathematical conclusion is false.

The [earlier elementary half-period lemma](../qlp_power_two_multiplier_obstruction)
is independent and unaffected. Unrestricted QLP(64) existence remains unresolved.

## The error

In a symmetric lift from length \(d\) to length \(2d\), folding forces
\[
z_{d/2}=z_{3d/2}=p_{d/2}/2.
\]
The valid endpoint parity condition is on the **child midpoint** \(z_d\).
There is no corresponding parity requirement on its **quarter entry**
\(z_{d/2}\). The published `compress.py:lifts` nevertheless used

```python
if mid % 2 or abs(mid//2) > bound or (mid//2-bound) % 2:
    return ()
```

The last disjunct is unjustified. The integral and bound checks are valid;
the extra parity check is not. The same defect occurred in the unpublished
mixed-symmetry pilot, whose apparent empty cover is also unsupported.

## An explicit omitted child

Consider these four half-compressed binary rows at length 8:

```text
(-2,  0,  1,  0,  0,  0,  1,  0)
(-2,  3, -1, -1,  0, -1, -1,  3)
(-2, -1,  0,  1,  2,  1,  0, -1)
(-1,  0,  2,  0, -2,  0,  2,  0)
```

They are symmetric, bounded by 4, and have sums \(0,0,0,1\).
Their zero-index parities are respectively even, even, even, odd; all midpoint
entries are even. Their combined periodic autocorrelations are
\[
(57,-8,-8,-8,-8,-8,-8,-8),
\]
exactly the required length-8 necessary equations for QLP(64).
Folding gives the valid length-4 parent

```text
(-2,  0,  2,  0)
(-2,  2, -2,  2)
( 0,  0,  0,  0)
(-3,  0,  4,  0)
```

whose combined autocorrelations are \((49,-16,-16,-16)\).
The first two child quarter entries are odd, so the invalid guard discards
both despite their satisfying every stated child condition.

`verify.py` checks these equations directly. It also constructs a length-64
binary realization of each child by independent multiplier-orbit enumeration
within residue classes. The full rows are reversible and have sums
\(0,0,0,2\), and their half-compressions are exactly the displayed rows.
These arbitrary full realizations fail the full combined correlation equations;
they are not asserted to form a quaternary Legendre pair.

## Reproduce

Python 3.10 or later, standard library only:

```sh
python3 verify.py --check
```

`expected.json` records the exact output, including the four full binary words
in hexadecimal (bit 1 means entry \(-1\)). Expected essentials: valid parent
length 4, valid child length 8, discarded rows `[0,1]`, and
`is_qlp_counterexample: false`.

This is an exact, independently inspectable counterexample to the implemented
lift-coverage assertion. It is not an independent peer review and does not
certify a corrected full search. A corrected complete cover and all required
final lifts must be checked before any full-family theorem is restored.

The old package's README now prominently withdraws its claim, and its `run.py`
exits with a withdrawal notice. Historical source and summaries remain available
for inspection. No new family exclusion is claimed by this correction.
