# Independent review: rank-width four and the rank-four zero-pair reduction

This directory contains reviewer-written evidence for two inseparable
structural contributions:

1. every 43-vertex graph with no red or blue $K_5$ has binary rank-width at
   least four in each color; and
2. on a fixed labelled $20+23$ cut, the rank-four cross matrices having both a
   zero row and a zero column form an exactly counted, completely excluded
   branch.

The checker imports no module from either reviewed package.  It exhausts the
rank-three label triples and all bounded abstract class-population profiles,
actively searching for a profile that survives the three cyclic contact-cell
caps.  It separately derives the rank-four counts by dynamic programming,
finite-field Möbius inversion, surjection inclusion-exclusion, and direct
enumeration of all binary matrices through $4\times4$.  It also decodes the
published physical fixtures and certificates independently.

Run with CPython 3.11 or later and the two reviewed directories at their pinned
commits:

```sh
python3 -B independent_check.py \
  <rank-width-source>/ramsey_r55_rank_width_four \
  <rank-four-cut-source>/ramsey_r55_rank4_cut_search_reduction
python3 -O -B independent_check.py \
  <rank-width-source>/ramsey_r55_rank_width_four \
  <rank-four-cut-source>/ramsey_r55_rank4_cut_search_reduction
```

The pinned commits are respectively
`931cd80b76854a3d42f605839508d4a72848fc7c` and
`c9a59be222cb0ce9a2ec7e9411a05441a2a7f261`.  Both modes report
`INDEPENDENT_CLUSTER_ACCEPTED`, with deterministic evidence SHA-256
`6936c2b7e1306957802c146d020a1997ccfa61b0b7cc0cf2f7785408730b49e6`.

The run checked all 210 ordered nonzero label triples, 17,529 bounded A-side
profiles, 16,654,050 B-profile/contact-cell combinations, 32,768 six-vertex
graphs, 74,954 binary matrices through $4\times4$, 1,470 rank-two factor
fibers, 231 centroid triples, the two complete source manifests, 84 physical
tree/cut ranks, and 201,376 five-subsets of the 32-vertex core.  It independently
reproduced the exact removed cross-matrix count

$$
166472869961950839672373904116655134899335779200
$$

and the reduced fraction

$$
\frac{11082739332310042690903561559441706322}
{19768120928371528230187646401013892765}.
$$

## Scope and trust boundary

The first theorem imports the previously reviewed balanced-cut lower bounds and
their ultimate classical premise $R(4,5)\leq25$.  The second theorem needs only
that Ramsey premise, elementary consequences including $R(4,4)\leq18$, and
finite-field linear algebra.  Neither theorem establishes that rank width four
is attainable, decides the surviving rank-four cross matrices, constructs a
43-vertex Ramsey graph, or changes the known Ramsey bounds.

The remaining trust boundary is the written unformalized arguments, the pinned
source and fixture bytes, this reviewer-written CPython checker, SHA-256, and
ordinary hardware.  Source manifests, physical graph encodings, cut sides,
tree cuts, ranks, row-space certificates, and literal monochromatic five-sets
are independently checked.
