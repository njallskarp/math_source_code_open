# Three valid anchors and the fully visible mixed-signature interface

Fix roots `r_1,...,r_k` and write the incidence signature of every other
vertex as

```text
sigma(v) = (color(r_1,v),...,color(r_k,v)) in {0,1}^k,
```

with red encoded by one. Two nonroots lie together in a monochromatic
neighborhood of some root exactly when their signatures agree in at least one
coordinate. Consequently their edge is unseen by all `2k` root neighborhoods
exactly when their signatures are bitwise complements.

A five-set lies wholly in one of the two neighborhoods of root `r_i` exactly
when its signatures are constant in coordinate `i`. Therefore, once both
local Ramsey conditions hold at every root, any surviving monochromatic `K5`
must be mixed in every signature coordinate.

For two roots these facts force a diagonal edge: a subset of `{0,1}^2` mixed
in both coordinates contains an antipodal pair. This is the two-anchor
diagonal principle used at heights 2811--2851. It does not extend to three
roots. For example, `{000,011,101}` is mixed in every coordinate but contains
no complementary pair. Thus a three-anchor obstruction can be globally mixed
while every one of its edges is visible in at least one fixed neighborhood.

The stored order-43 coloring realizes this failure inside the assigned hard
branch. Root `0` has a 22-vertex red neighborhood with 108 red edges, hence
deficiency six from the exact maximum 114. Vertices `3` and `9` both have red
degree ten inside that core, both are red-adjacent to `0`, and `3--9` is red.
All six monochromatic neighborhoods at roots `0,3,9` satisfy the required
`(4,5)` conditions. The complete coloring has 452 red edges and degree profile
`20^8 21^26 22^9`.

Nevertheless it contains the red five-clique

```text
{4,12,14,24,31}, signatures {100,100,111,001,010},
```

and the blue five-clique

```text
{1,7,8,18,34}, signatures {101,101,110,111,011}.
```

Each signature multiset is mixed in every coordinate and its support is
complement-free. Hence neither five-clique lies in any one anchor neighborhood,
yet every one of its ten edges appears in at least one of the six fixed
neighborhoods. These are exact width-zero defects relative to the 96 edges
unseen by all three anchors.

This proves an insufficiency result, not a Ramsey construction: three full
anchors, exact edge count, and the hard degree profile can coexist with global
monochromatic five-cliques. It also pinpoints the next omitted interface.
Beyond two anchors, controlling only edges unseen by every anchor is inadequate;
one must constrain mixed-coordinate five-sets assembled from edges visible in
different anchor neighborhoods.
