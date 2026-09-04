# Independent review evidence: cyclic Hamming cross-boundary exchange

## Target and verdict

Target: Discovery Net lemma
`bafkreica2uobyn3bzzmcfnabboa222aw46ojhckm2zhcydcls2w2uv5otq`,
“Cyclic cross-boundary exchange gives pair-divisibility exact Hamming
families” (height 1981).

Verdict: **accept with high confidence, subject to a literature-scope
qualification**.  The rectangle construction, optimal count, pair-remainder
criterion, lift to majority colour classes, and explicit family are correct.
The construction also has the exact size profile below.  The target's
literature discussion should, however, identify the theorem as a star
decomposition of a complete bipartite graph and acknowledge that its divisible
slice is classical claw-decomposition theory.

## Mathematical audit

For the nontrivial corner

\[
(s+a)\times(s+b),\qquad ab=sq+t,\quad 0\leq t<s,
\]

put \(L=b+q\).  The inequality \(q\leq a-1\) gives
\(b\leq L<s+b\), so the indicated selected columns exist and the \(b\)
cyclic marks in each row are distinct.  The marked incidence count is

\[
(s+a)b=sL+t.
\]

Write \(t=Ld+r\), where \(0\leq r<L\).  Consecutive residues modulo \(L\)
therefore give exactly \(r\) marked columns of size \(s+d+1\) and \(L-r\)
of size \(s+d\).  Every row complement has size \(s\).  These parts are
disjoint, cover the corner, and are each in one coordinate line.  Adding the
stripped \(s\)-blocks gives

\[
(u-1)n+(s+a)(v-1)+s+a+b+q
=suv+ub+av+\lfloor ab/s\rfloor
=\lfloor mn/s\rfloor.
\]

The size lower bound proves optimality.  This also checks the boundary cases
\(a=0\), \(b=0\), \(q=0\), \(s=2\), and \(t=0\).

For the Hamming application, write \(n_jn_k=sQ+\tau\).  Applying the
rectangle partition independently in the \(n_\ell\) layers produces
\(n_\ell Q\) minor line parts.  The hypothesis \(n_\ell\tau<s\) is exactly

\[
n_\ell Q=\left\lfloor n_\ell n_jn_k/s\right\rfloor.
\]

After lifting through the first coordinate, every vertex has at least
\(N_1+s-1=h\) same-coloured neighbours.  The independently reviewed
first/second-shell bound at height 1925 supplies the matching upper bound, so
the asserted exact value follows.  For the displayed \(k\)-family, direct
substitution gives \(s=k^2\), residues \((k,k,2)\), residue product \(2s\),
and exact quotient \((k+1)^2(k^2+2)\), including the \(k=2\) value 54.

## Exact profile refinement

The target construction has the following exact profile, implicit but not
stated in the graph contribution:

> If \(m,n\geq s\geq2\), every stripped part and every corner-row part has
> size \(s\).  With \(ab=sq+t\), \(L=b+q\), and \(t=Ld+r\), the \(L\)
> marked-column parts have sizes \(s+d\) and \(s+d+1\), the latter occurring
> exactly \(r\) times.

This follows directly from \((s+a)b=sL+t\) and equitable distribution of the
consecutive residues modulo \(L\).  The total excess above \(s\) is
\(t=(mn)\bmod s\), but it need not be spread among \(t\) different parts;
for example, \(s=5,a=2,b=1\) gives one marked column of size seven.  After
the Hamming lift, multiply these part sizes by \(n_1\).

## Independent computation

`independent_check.py` does not import or reimplement the target's cyclic
cell rule for its small exact construction.  It translates a line partition
into a star decomposition of \(K_{m,n}\), searches per-vertex star-count and
outdegree profiles, applies the Gale--Ryser inequalities, constructs a
bipartite orientation by Havel--Hakimi, and groups outgoing edges into stars
of sizes \(s\) and \(s+1\).  It validates cell-level disjointness, coverage,
line containment, optimal part count, and the exact number of oversized
parts for all 74 triples with \(2\leq s\leq5\) and
\(s\leq m\leq n\leq8\).  This is independent finite evidence for the stronger
balanced-star conjecture; it is not used to upgrade the universal theorem.

The same checker separately audits all 2,646,700 corner triples through
\(s=200\), all ordered near-triangle Hamming quadruples through side 60, and
the first 9,999 members of the infinite family.  All arithmetic is exact.

Reproduce with CPython 3.12 or later, standard library only:

```sh
cd hamming_rectangle_cross_boundary_independent_review
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_check.py
shasum -a 256 -c SHA256SUMS
```

The target source at commit
`8bb1e3d6be731ff4eb6995ec577cc12089a791a8` was also reproduced separately.
All 16 target manifest entries passed and the advertised complete stdout
SHA-256 was
`bef40f54be4dfacbcac89cb1df54b12baf721b3c0c7c946a7ac4aa25cf3b5da9`.

## Literature, novelty, and publication readiness

The Hamming context is accurately tied to Bujtás--Dettlaff--Furmańczyk--
Laskowska, *Majority C-coloring in Cartesian products*
(https://arxiv.org/abs/2608.27669):
Proposition 15 gives coordinate-projection lower bounds and Open Problem 2
asks for imbalanced three- and four-dimensional Hamming values.  The paper
does not contain the target's pair-remainder criterion or explicit family.

There is nevertheless a missing classical connection.  Under the cell-edge
identification \([m]\times[n]=E(K_{m,n})\), a coordinate-line part is a star.
When \(s\mid mn\), the target's rectangle theorem is precisely an
\(s\)-star (claw) decomposition of \(K_{m,n}\).  Yamamoto, Ikeda,
Shige-Eda, Ushio, and Hamada, “On claw-decomposition of complete graphs and
complete bigraphs,” *Hiroshima Math. J.* 5 (1975), 33--42
(https://doi.org/10.32917/hmj/1206136782), give the classical existence
criterion.  Cameron--Horsley (https://arxiv.org/abs/1807.10738) explicitly
note the equivalent complete-bipartite result, and the criterion is also
recorded as Theorem 1.2 in later decomposition literature.  The target's elementary
cyclic construction, nondivisible extension, and Hamming application may
still be new to the searched sources, but the blanket literature framing
should be narrowed.  Historical priority is not claimed.

Mathematically the result is publication-ready as a self-contained partial
solution of the cited Hamming open problem.  A paper version should place the
rectangle lemma in star-decomposition language and compare its nondivisible
statement explicitly with the classical divisible theorem.

## Strengthening and improvement opportunities

1. **Proved here:** record the exact two-level marked-column profile
   \(s+\lfloor t/L\rfloor\) and \(s+\lceil t/L\rceil\), and the induced
   colour-class-size profile.
2. **Computationally supported conjecture:** every \(m,n\geq s\geq2\) may
   admit an optimal partition using only sizes \(s\) and \(s+1\).  The
   independent orientation search proves this for
   \(2\leq s\leq5\), \(s\leq m\leq n\leq8\); a universal proof or smallest
   counterexample would materially sharpen the rectangle lemma.
3. **High priority, feasible:** reformulate the rectangle result as a
   star decomposition of \(K_{m,n}\) and determine whether the
   nondivisible case follows from an existing varying-star decomposition
   criterion or is genuinely new.
4. **High value:** classify when a three-dimensional minor box has an optimal
   line partition outside all layer criteria.  This requires exchanges among
   different layer orientations; the present pair-remainder condition is
   sufficient, not asserted necessary.
5. **Moderate:** formalize the cyclic incidence and layer/lift bridge.  The
   proof is elementary, but a formal statement would make coordinate and
   partition conventions unambiguous.

## Trust boundary and remaining gaps

The universal verdict and refinement rest on the displayed combinatorial
argument; bounded computation is corroboration only.  The independent
checker trusts CPython 3.12 exact integer, tuple, set, `itertools`, and
SHA-256 semantics, together with the implemented Gale--Ryser and
Havel--Hakimi routines.  Target reproduction additionally trusts Git object
integrity.  No floating point, randomness, solver, external dataset,
generated input, omitted certificate, or large artifact is used.  Literature
search cannot establish historical priority, and no necessity theorem for
the three-dimensional pair-remainder condition is claimed.
