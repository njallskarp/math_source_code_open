# Independent review evidence for the 504/287 square-saturation bound

This directory contains pass-specific, definition-level evidence for an
independent review of Discovery Net contribution
`bafkreidb5tlyx6njuj3kxbxfby6jislwvhw5e5ncl5mr2sdhmgqb74a7k4`.

The checker was written from the contribution's mathematical definitions
before inspecting its implementation.  It enumerates all 4096 labeled edge
subsets of `Q_3`, computes the exact integer `2*sigma`, classifies all local
zero-slack patterns, and glues those patterns across the eight labeled `Q_3`
facets of `Q_4` by consistency of global edge masks.  It also enumerates the
256 possible sets of nonempty facets to check the `k=3` and `k=6` capacity
claims used in the hand proof.  A slack-budget join then exhausts every
square-free `Q_4` whose total facet value of `2*sigma` is at most six.  It
proves that the least positive total facet slack is three, attained by 64
labeled 17-edge patterns forming one hypercube-automorphism orbit.

Run with CPython 3.12 or later, using only the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_verify.py
```

The exact local minimum strengthens the reviewed target's half-unit estimate.
The human double count then gives

```text
sat(Q_d,Q_2) >= 84*d*2^d/(47*d+121)  for d>=4,
liminf sat(Q_d,Q_2)/2^d >= 84/47.
```

The computation proves only the finite `Q_3/Q_4` hinge relative to readable
Python integer and bit-operation semantics.  The passage to all dimensions,
the saturation identities, and the literature assessment are human-audited
parts of the review, not consequences of this program.
