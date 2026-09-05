# Girth-sensitive cubic density in Erdos--Gyarfas minimal counterexamples

This directory contains a self-contained structural theorem about a hypothetical
minimal counterexample to the Erdos--Gyarfas power-of-two cycle conjecture.
If the counterexample has girth `g`, `a` degree-three vertices, and `b`
vertices of degree at least four, then

    4 b <= a + 2 floor(a/(g-1)).

Consequently at least `(4g-4)/(5g-3)` of its vertices have degree three.
This specializes to `2/3` without a girth restriction, `8/11` in the
triangle-free case, and `20/27` when the girth is at least six.  The proof also
classifies equality in the rational density bound: the degree-three induced
subgraph is a disjoint union of paths on `g-1` vertices, each closed to a
g-cycle by a unique degree-four vertex.

The mathematical proof is in `THEOREM.md`.  It is independent of any claimed
resolution of the full conjecture.

## Reproduce

Use Python 3.11 or later.  From this directory run:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_density.py
    diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_density.py)
    shasum -a 256 -c SHA256SUMS

The verifier uses only Python's standard library and exact integer and
rational arithmetic.  It exhausts all arithmetic profiles with
`3 <= g <= 80` and `1 <= a <= 5000`, independently maximizes the allowed
high-degree count, checks the floor and rational density bounds, checks the
stated corollaries, and emits a hash of the full profile stream.  This is an
arithmetic audit, not a replacement for the universal graph-theoretic proof.

## Literature status and scope

The conjecture was posed by Paul Erdos and Andras Gyarfas.  The structural
starting point is Avery Carr, *Every Minimal Counterexample to the
Erdos--Gyarfas Conjecture is Predominantly Cubic*, arXiv:2605.22844 (2026).
Andrew Bisch's July 2026 note *Two Thirds of the Vertices of a Minimal
Counterexample to the Erdos--Gyarfas Conjecture are Cubic* proves the
unrestricted `2/3` estimate and a two-cubic-vertex deletion lemma.  The proof
here recovers `2/3` and strengthens it as a function of girth using whole
components of the degree-three induced subgraph.

A targeted search on 2026-09-05 found no primary source containing the exact
floor inequality or the girth-dependent ratio.  This negative search is not a
proof of novelty.  A separate August 2026 Zenodo working paper claims a proof
of the full conjecture; its correctness and review status are not assumed
here.
