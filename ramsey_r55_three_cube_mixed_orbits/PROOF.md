# Orbit-complete mixed-interface classification for three anchors

Let three fixed roots assign each nonroot vertex a signature in the cube
`Q_3={0,1}^3`. A five-signature multiset is **mixed** when both bits occur in
every coordinate, and **complement-free** when its support contains no
antipodal pair `s,1-s`.

These two conditions have the exact Ramsey interpretation:

- mixed means the five vertices are not all contained in any one of the six
  monochromatic root neighborhoods;
- complement-free means every pair of the five vertices agrees in some
  coordinate, so every edge is visible in at least one root neighborhood.

Thus these are precisely the signature patterns of fully visible global
five-set constraints that are not already local to one anchor.

## Support classification

Complement-freeness permits at most one vertex from each of the four
antipodal pairs of `Q_3`, so the support has size at most four. It has size at
least three: two noncomplementary cube vertices differ in at most two
coordinates and therefore cannot be mixed in all three. Since the multiset
has total size five, only the following cases occur.

### Three-point support

Translate one support point to `000`. The other two nonzero points must cover
all three coordinates, cannot be `111`, and cannot be complementary. Hence,
after permuting coordinates, the support is

```text
{000,011,101}.
```

It is an equilateral Hamming-distance-two triangle. There are eight such
supports. The positive multiplicity partitions of five into three parts are
`(3,1,1)` and `(2,2,1)`. The triangle symmetries are transitive on vertices,
so these give exactly two orbits:

```text
triangle_heavy: 000,000,000,011,101     (24 multisets),
triangle_double: 000,000,011,011,101    (24 multisets).
```

### Four-point support

The support chooses one point from every antipodal pair. The mixed choices
are exactly eight induced cube stars and the two parity tetrahedra. This can
also be seen by normalizing a point to `000` and checking the three remaining
antipodal choices. A star has one center and three symmetric leaves, while a
parity tetrahedron has four symmetric vertices. Exactly one support point is
doubled, giving three orbits:

```text
star_center:       000,000,001,010,100  (8 multisets),
star_leaf:         000,000,001,011,101  (24 multisets),
parity_tetrahedron:000,000,011,101,110  (8 multisets).
```

The five orbit sizes sum to `88`. Under the full cube group of three
coordinate permutations and three independent bit flips (order 48), their
stabilizer orders are respectively `2,6,2,2,6`. Orbit--stabilizer gives the
same sizes `24,8,24,24,8`.

## Complete cut schema

Let `C_s` be the cell of vertices with signature `s`, and let `x_uv` be the
red indicator of edge `uv`. For each of the five representatives, apply all
cube symmetries and choose distinct vertices from the indicated cells with
the stated multiplicities. On every resulting five-set `S`, impose

```text
1 <= sum_{uv in choose(S,2)} x_uv <= 9.
```

The lower inequality forbids a blue `K5`; the upper inequality forbids a red
`K5`. By the classification, these ten orbit-indexed one-sided templates are
exactly all fully visible, anchor-mixed `K5` cuts. No qualifying signature
multiset is omitted, and no template is already a single-anchor constraint or
uses a wholly unseen antipodal edge.

For contrast, the analogous two-bit class is empty: every subset mixed in
both coordinates contains an antipodal pair. This is why the diagonal-edge
interface is complete for two anchors but not for three.

The height-2907 witness realizes two different new templates: its first red
fully visible defect is `parity_tetrahedron`, and its first blue one is
`star_leaf`. The classification itself is independent of that witness and of
all degree/profile data.
