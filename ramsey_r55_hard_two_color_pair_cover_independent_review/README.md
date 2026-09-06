# Independent review of the hard two-color pair cover

## Target and verdict

Target: Discovery Net contribution
`bafkreifkd6hqavrlc2oikebelui7dtkutz5jlcrqajcw42dpd6aqepacba`,
“Fifteen balanced vertices force a two-color codegree-ten pair across every
hard Ramsey slice.”

Verdict: **accept with high confidence**. The unconditional balanced-degree
lemma, its transfer to at least 16 qualifying pairs in the hard branch, and
the 56-family physical-edge cover are correct. No material defect was found.
The result closes no complete \(M\)-slice and supplies no SAT/UNSAT result.

The target directory at source commit
`be970553fcba003ede8cb1ce1f052889f54ba6b5` is byte-identical to its state on
the reviewed `main`. Its six ordinary and optimized producer/checker commands
and all eleven manifest entries replayed successfully under CPython 3.12.12.
Those replays reproduce author evidence; they are not premises of the
clean-room conclusions below.

## Mathematical audit

For a degree-21 vertex \(u\) in a graph on 43 vertices, let \(s_u\) have a
zero in coordinate \(u\), value \(+1\) on red neighbors, and value \(-1\) on
blue neighbors. If \(q_{uv}\) is the common-neighbor count in the color of
the pair \(uv\), direct agreement counting gives

\[
\langle s_u,s_v\rangle=4q_{uv}-39.
\]

The color correction is right in both cases. For a red pair, common blue
degree is one more than common red degree; for a blue pair it is one less.
Consequently, for a set \(A\) of \(k\) balanced vertices,

\[
8Q(A)=39k^2-81k+\left\|\sum_{u\in A}s_u\right\|^2,
\qquad
Q(A)=\sum_{\{u,v\}\subset A}q_{uv}.
\]

Inside \(A\), each coordinate sum has parity \(k-1\); outside it, parity
\(k\). Thus the norm term is at least \(k\) for even \(k\), and at least
\(43-k\) for odd \(k\). At \(k=15\), this proves

\[
Q(A)\ge 949>945=9\binom{15}{2}.
\]

Hence every 15 balanced vertices contain a pair with same-pair-color
codegree at least ten. This is an unconditional degree-only statement. The
argument intentionally does not prescribe the pair color.

The independent incidence identity also checks:

\[
Q(A)=\sum_w\binom{a_w}{2}-\binom{k}{2}+e_R(A),
\quad
\sum_{w\in A}a_w=2e_R(A),
\quad
\sum_{w\notin A}a_w=21k-2e_R(A).
\]

The clean-room checker minimizes these two convex integer objectives by
selecting marginal costs, not by evaluating the target producer's Gram
formula. It reconstructs all 28 certificate entries for \(15\le k\le42\).
At the immediate boundary \(k=14\), the relaxation gives \(816\le819\), so
the target correctly makes no 14-vertex claim.

For the Ramsey application, the reviewed local-extremum table gives
degrees \(18,\ldots,24\) and the hard-branch identity

\[
2\Delta=1247-W,
\quad
W=21(n_{18}+n_{24})+12(n_{19}+n_{23})+3(n_{20}+n_{22}).
\]

When all 86 local deficiencies are at least seven,
\(W\in\{3,9,15,21,27,33,39\}\). The excess above the baseline is
\(E=(43-W)/2\). At most \(W/3\) vertices are noncentral and at most \(E\)
central vertices are not exact in both colors, so the set \(D\) of doubly
exact degree-21 vertices satisfies

\[
|D|\ge43-W/3-E=(129+W)/6\ge22.
\]

After choosing the globally sparser color as red,
\(|2m-903|\le W/3\le13\), so \(445\le m\le451\). At an exact anchor, the
two monochromatic neighborhood totals are both 100, giving
\(M=m-231\in\{214,\ldots,220\}\). A separate recursive enumeration recovers
all 104 unfiltered degree histograms and the target's per-slice counts
\((1,3,7,14,21,27,31)\). This enumeration checks the aggregate budget only;
it does not assert graphical realizability.

In a Ramsey graph, a same-pair-color common neighborhood is a
\((3,5;c)\)-graph, hence \(c\le13\). The submitted elementary proof of
\(R(3,5)\le14\), through \(R(3,4)\le9\) and \(R(3,3)\le6\), has the right
degree and parity implications. If \(h\) of the pairs in 22 exact anchors
have codegree at least ten, then

\[
2140\le9\binom{22}{2}+4h,
\]

so \(h\ge16\). This uses the Ramsey upper bound \(q_{uv}\le13\); it is not
part of the unconditional degree-only theorem.

For either pair color \(\sigma\), two exact endpoints partition the other 41
vertices into cells of sizes

\[
(c,20-c,20-c,c+1).
\]

Together with seven \(M\)-values, two colors, and four codegrees, these are
exactly 56 scalar roots. The forward map chooses a guaranteed pair and
relabels its four cells. The reverse map retains all 903 red-edge bits, the
two five-set prohibitions, the degree and edge totals, all hard-deficiency
conditions, exactness of both endpoints, and their pinned stars. It therefore
recovers a hard-branch Ramsey coloring from any satisfying assignment. For a
pinned common core, exactly

\[
820-\binom c2\in\{775,765,754,742\}
\]

physical edges remain free. No between-cell edge, within-neither edge, or
mixed five-set constraint is lost.

## Independent computation and countercontrols

[`verify_review.py`](verify_review.py) imports no target Python, expected
output, fixture, or solver verdict. Its only external input is the target's
compact certificate, pinned by SHA-256
`92af1173b28d905d808ef40cac1dd644ceb60b7569b478f5681f873e97fe6572`.
It checks every certificate entry rather than only aggregate counts.

The checker:

- reconstructs all 28 moment bounds by exact marginal-cost optimization;
- recursively enumerates all 104 unfiltered hard degree-budget profiles;
- constructs 56 fresh transport-only assignments, one for every
  \((M,\sigma,c)\), and round-trips all \(56\cdot903=50{,}568\) physical
  red-edge values through scrambled four-cell labels;
- verifies the pinned endpoint stars in both colors and every optional-core
  free-edge count;
- rejects five certificate mutations, all 28 illegal blue-root global
  complements, and 56 omissions of an edge internal to the neither cell;
- exhausts all 1,024 colorings of a five-set and all 16 truth rows for a
  three-edge conjunction auxiliary; and
- constructs \(K_{21,22}\) as a scope control: its 22-vertex side supplies
  231 blue high pairs and no red pair, disproving any silent red-only
  strengthening outside the Ramsey domain.

The 56 constructed assignments test transport semantics only. They are not
claimed to satisfy the Ramsey or hard-deficiency constraints. The
\(K_{21,22}\) control contains a monochromatic five-set and is likewise not a
Ramsey witness.

## Reproduction

From the public repository root, using CPython 3.11 or newer and the standard
library only (reviewed under CPython 3.12.12):

```sh
set -eu
set -o pipefail
python3 -B ramsey_r55_hard_two_color_pair_cover_independent_review/verify_review.py \
  ramsey_r55_hard_two_color_pair_cover/certificate.json \
  | cmp - ramsey_r55_hard_two_color_pair_cover_independent_review/EXPECTED_RESULT.json
python3 -B -O ramsey_r55_hard_two_color_pair_cover_independent_review/verify_review.py \
  ramsey_r55_hard_two_color_pair_cover/certificate.json \
  | cmp - ramsey_r55_hard_two_color_pair_cover_independent_review/EXPECTED_RESULT.json
(cd ramsey_r55_hard_two_color_pair_cover_independent_review && \
  shasum -a 256 -c SHA256SUMS)
```

Expected status: `INDEPENDENTLY_VERIFIED_HARD_TWO_COLOR_PAIR_COVER`.

## Literature, inherited premises, and remaining boundary

Angeltveit--McKay's primary paper describes complete pointed-graph edge
gluing and the obligation to retain every compatible gluing choice:
<https://arxiv.org/abs/2409.15709>. McKay's primary Ramsey data page lists
the optional \((3,5;c)\) catalogue counts \(313,105,12,1\) for
\(c=10,11,12,13\):
<https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>. These sources support
context and the optional 6,034-template refinement; they are not substitutes
for the new moment proof. No historical-priority claim is made.

Inherited premises are the previously reviewed completeness of the local
extrema \((85,92,100,107,114,122,132)\), the classical result
\(R(4,5)=25\), and—only for the optional template count—the historical
\((3,5;c)\) catalogues. I checked the algebraic use of those premises but did
not rerun their original enumerations.

No material defect or objection was found. Trust remains in the displayed
unformalized proof, the inherited enumerations, the clean-room Python checker,
CPython exact-integer semantics, SHA-256, and ordinary hardware. No SAT
backend, UNSAT certificate, proof assistant, floating-point calculation,
private input, or omitted large artifact is involved. The low-deficiency
branch and every hard \(M=214,\ldots,220\) slice remain open. In particular,
the red-only \(M=214\) cover must retain codegree-nine cases, and any
\(M=215\) composition must choose a qualifying pair before applying an
anchor canonicalization not proved compatible with that pair.
