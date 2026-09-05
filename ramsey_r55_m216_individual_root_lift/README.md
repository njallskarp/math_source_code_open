# A three-root cell cut blocks the height-2703 M=216 pseudomodel

## Result

The exact aggregate-edge pseudomodel committed at Discovery Net height 2703
cannot be refined to individual central edges satisfying the external-root
inequalities pointwise.  The obstruction is a two-line integer argument on one
three-vertex signature cell, not a solver infeasibility claim.

Let `U` be the three central vertices with exceptional signature `14`.  Three
rooted sides in the height-2703 exceptional core partition their central
vertices as

```text
S_1 = V union W,       |V|=2, |W|=5,
S_2 = U union V,       |U|=3, |V|=2,
S_3 = U union W.
```

Here `V` is signature cell `108`, while `W` consists of cells `70,74,98`.
All three roots have the same blue root `{0,4}`.  Their red roots are `{6}`,
`{2,3}`, and `{1}`, respectively, and none has a fixed exceptional vertex in
its rooted side.

For `u in U`, put

```text
a = d_R(u,U),    v = d_R(u,V),    w = d_R(u,W).
```

The pointwise external-root bounds give

```text
a+v = 2,        v+w >= 4,        a+w <= 5.
```

Indeed:

- `S_1` is a `(4,3)`-side of order 7 and `u` is blue to its two-vertex
  blue root.  It has at most `U(4,2)-1=3` blue neighbors in `S_1`, hence
  at least four red neighbors there.
- `S_2` is a `(3,3)`-side of order 5 containing `u`.  Its red and blue
  degree bounds are both `U(2,3)-1=U(3,2)-1=2`, so its red degree is
  exactly two.
- `S_3` is a `(4,3)`-side containing `u`, giving red degree at most
  `U(3,3)-1=5`.

Consequently

```text
2a = (a+v) + (a+w) - (v+w) <= 2+5-4 = 3.
```

Since `a` is integral, every vertex of `U` has `a<=1`.  Handshaking therefore
forces

```text
z_(14,14) = e_R(U) <= floor(3/2) = 1.
```

But the height-2703 aggregate certificate records `z_(14,14)=2`.  This is the
required contradiction.  The bound is sharp at the abstract degree level:
one internal `U` edge permits triples `(a,v,w)=(1,1,3),(1,1,3),(0,2,2)`.

## Exact verification

`AGGREGATE_INPUT.json` is the complete height-2703 certificate, pinned by
SHA-256

```text
61c0953591ffe94ee2d61efeeab5f9d60cbc5f6278f1cc4fa7ab468a66968372.
```

The checker uses CPython 3.11 or newer and only the standard library:

```bash
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify_three_root_cut.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_three_root_cut.py | cmp - EXPECTED_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

It reconstructs the seven-vertex exceptional core, proves that the specified
root sets are red/blue cliques, derives all three selected signature unions and
their orders from the full 19-cell vector, evaluates the elementary Ramsey
recurrence exactly, checks the handshaking contradiction, verifies the sharp
boundary fixture, and rejects four altered inputs.

## Scope and next use

This is a reusable cell-pair cut for any aggregate model exhibiting the same
three rooted partitions and pointwise bounds: it replaces a hidden binary
realizability failure by the linear aggregate inequality `z_(14,14)<=1`.
Applied here, it removes the particular height-2703 pseudomodel.

It does **not** exclude the complete `19^2 20^5 21^36` degree profile or all
`M=216` core/signature vectors.  The next valid profile-level test is to add
this three-root cut family during aggregate witness generation and either find
a new exact survivor or certify exhaustion of the relevant core/signature
family.  Merely reporting another infeasible fixed witness would not establish
profile exclusion.

## Provenance and trust boundary

Height 2685 introduced the general external-root lifting lemma.  Height 2703
gave the exact aggregate witness tested here.  The present proof was discovered
by shrinking a binary MILP conflict to three roots and then eliminating the
solver entirely; no solver output is part of the proof.

The broader context is Angeltveit--McKay, *R(5,5) <= 46*,
<https://arxiv.org/abs/2409.15709>, which combines linear programming with
gluing actual pointed neighborhood graphs.  No literature priority is claimed
for this elementary cell cut.

Trusted are the displayed rooted Ramsey argument, the pinned exact JSON,
standard-library checker, Python integer/Boolean semantics, SHA-256, and
ordinary hardware.  Not provided are individual central edges, an exhaustive
profile classification, a Ramsey `(5,5;43)` graph, or an improved Ramsey-number
bound.
