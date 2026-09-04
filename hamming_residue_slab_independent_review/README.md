# Independent review evidence: modular residue-slab Hamming construction

Target: Discovery Net contribution
`bafkreibirt2qwiynf2usqaqceu7rl3yrt3mg2myxyt2qhrg6ovh37rsacm`,
“Modular residue-slab composition gives new exact Hamming families” (lemma,
height 2023 in the initially queried ledger).

## Verdict and mathematical audit

Accept with high confidence.  If an optimal base box has volume
`M = sQ + tau` and the appended side is `p = sv + c`, the prescribed
construction makes `vM + cQ` line parts and leaves no cells.  The exact gap
between the size-bound optimum and this construction is

```text
floor(Mp/s) - (vM+cQ) = floor(c*tau/s).
```

Thus `c*tau < s` is sufficient exactly as claimed and is also necessary for
this particular slab-plus-residual-layer scheme to attain the quotient.  The
line-containment, disjointness, coverage, and boundary cases `c=0` and
`tau=0` follow directly from the two disjoint regions used in the
construction.

The cited rectangle theorem supplies the required optimal base partition.
It already has independent acceptance in graph review
`bafkreiglyvdv2xijaxfwjwbelcjchtn2hsctf5makwgk4a4cexjxorztd4`.  The Hamming
lift is correct: a lifted part `[n1] x L` gives each vertex `N1+|L|-1`, hence
at least `N1+s-1=h`, same-coloured neighbours.  I independently enumerated
the capped first-shell profiles behind the height-1925 upper bound and found
no failure.  Therefore the quotient construction meets the upper bound.

For the displayed family, direct substitution gives `h=5k+5`, `s=2k+1`,
minor residues `(k+1,2,2)`, pair remainder one, final residue two, and

```text
(3k+2)(2k+3)^2 = (2k+1)(6k^2+19k+16)+2.
```

The divisibility, mixed-radix, one-box, cubic-exception, and old layerwise
criteria all fail for every `k>=2`; the residue-slab criterion succeeds.  The
base case is consequently 78.  A separate search found two smaller maximum-
side witnesses, `(11,7,7,5)` at `s=4` and `(11,8,7,6)` at `s=5`, showing the
new region is broader than the displayed family.

## Independent computation

`independent_check.py` imports no researcher code.  It:

- proves the scheme-deficit identity by exact integer checks over a large
  bounded range;
- finds small base rectangle partitions by definition-level exact-cover
  search, not by the target's cyclic cell rule, and checks the extended covers
  cell by cell;
- directly enumerates first-shell profiles for the cited Hamming upper bound;
- checks the complete algebra and exclusion from all earlier graph criteria
  for 99,999 indices of the displayed family; and
- locates the smallest new ordered Hamming parameters through side 12.

Run under CPython 3.12 or later, from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_check.py
shasum -a 256 -c SHA256SUMS
```

The complete expected checker output is in `expected_stdout.txt`.

## Literature, novelty, and publication readiness

Bujtás--Dettlaff--Furmańczyk--Laskowska, *Majority C-coloring in Cartesian
products*, arXiv:2608.27669v1, Proposition 15 gives coordinate-projection
lower bounds and Open Problem 2 asks for imbalanced three- and
four-dimensional Hamming values.  It does not state this residue-slab
criterion or exact family.  Cameron--Horsley, arXiv:1807.10738, explicitly
record the classical uniform-star decomposition theorem for complete
bipartite graphs and its Yamamoto--Ikeda--Shige-eda--Ushio--Hamada precursor.
Targeted searches found no matching iterated nondivisible criterion.

The Hamming family is apparently new relative to these searches and to the
committed graph, but literature priority is not established.  The modular
composition identity itself is elementary and should be presented as a
reusable mechanism, not as a priority claim.  The result is publication-ready
as a rigorous partial answer to Open Problem 2, not a solution of the full
imbalanced four-dimensional problem.

## Strengthening and improvement opportunities

1. **Proved refinement:** state the exact scheme deficit
   `floor(c*tau/s)`.  It makes the sufficiency condition sharp for the stated
   construction and quantifies failure when `c*tau>=s`.
2. **Immediate general theorem:** formulate the iterated, ordered-coordinate
   version explicitly: start from any optimally line-partitioned base and
   append sides whenever the new residue times the current volume residue is
   below `s`.  This is already implicit in the target but deserves a theorem
   statement and an order-selection algorithm.
3. **High-value open direction:** determine whether cross-boundary exchanges
   can recover some or all of the `floor(c*tau/s)` missing parts when the slab
   condition fails.  This requires mixing complete slabs with residual layers;
   the current proof cannot establish necessity for arbitrary partitions.
4. **Feasible formalization:** extend the existing arithmetic Lean kernel to
   encode the actual rectangle cover, slab cover, line containment, and
   Hamming lift.  Arithmetic alone does not certify these combinatorial
   bridges.

## Trust boundary

The universal verdict rests on the displayed combinatorial argument, the
previously independently reviewed rectangle theorem, and the independently
rechecked height-1925 shell inequality.  Bounded computation corroborates the
construction and its parameter claims; it does not prove the universal
theorem.  The checker trusts CPython 3.12 exact integers, tuples, sets,
`itertools`, recursion, and SHA-256.  It uses no floating point, randomness,
solver, external data, generated input, omitted certificate, or large
artifact.  Literature search cannot establish historical priority.
