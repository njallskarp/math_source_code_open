# No 29-entry maximal partial Latin cube of order four

**Computer-assisted theorem.** There is no independent dominating set of size 29 in the Hamming graph \(H(4,4)\). Equivalently,
\[
29\notin ML(3,4).
\]
Combining this exclusion with the previously established spectrum and the checked 28- and 30-entry witnesses gives
\[
ML(3,4)=\{28\}\cup\{30,31,\ldots,61\}\cup\{64\}.
\]
The new exclusion has no dependency on an imported minimum-size theorem. The spectrum corollary additionally uses the prior results cited below.

## 1. Objects and the complete smallest-layer reduction

A word in \(\{0,1,2,3\}^4\) specifies a cell and symbol of an order-four partial Latin cube. Two entries are compatible exactly when their Hamming distance is at least two. A compatible set is maximal exactly when every ambient word is at distance at most one from a selected word: an undominated word would be an addable entry. Thus the requested objects are precisely independent dominating sets in \(H(4,4)\).

There are sixteen coordinate slices, obtained by fixing one coordinate to one of its four values. Suppose a 29-word code exists, and let \(k\) be its smallest slice size. Within any fixed slice, an entry in that slice covers ten positions: itself and nine one-coordinate changes. Each entry outside it covers at most one position in the slice. Consequently
\[
64\le10k+(29-k)=29+9k,
\]
so \(k\ge4\). The four slices in any one coordinate partition the 29 entries, whence the global minimum is at most seven. Therefore
\[
4\le k\le7.
\]

Permute coordinates and their symbols to make a smallest slice the first-coordinate-zero slice. Let its projection be \(A\subseteq W=\{0,1,2,3\}^3\). It is an independent set in \(H(3,4)\) of size \(k\). The three remaining coordinates and their symbol names can still be permuted freely. We enumerate every such \(A\), modulo exactly this action \(S_4\wr S_3\), of order \(24^3\cdot6=82944\). No assumption of a nontrivial automorphism of the full code is made.

## 2. Orbit coverage, with a separate completeness audit

`orbits.c` generates all independent-set orbits of sizes zero through seven. Starting with the empty set, it adds every vertex outside the closed neighborhood of each preceding representative. Every independent set has an independent one-entry deletion. Mapping that deletion to a representative also maps the omitted entry to one of the explicitly tested extensions. Induction therefore proves coverage; retaining one representative per exact canonical code removes only equivalent sets.

The canonical code uses only finite permutations. For each ordering of the \(k\) entries, rename symbols separately in each of the three coordinate columns in first-occurrence order. Encode each column in base four, sort the three columns, and take the lexicographically least triple over all \(k!\) entry orderings. The C implementation packs this triple into at most 42 bits.

Equality of these codes is equivalent to orbit equivalence. An allowed coordinate/symbol permutation preserves a normalized triple after an appropriate reordering of entries. Conversely, equal normalized triples specify an entry bijection, a permutation of the three columns, and bijections between the used symbols in matching columns. Extend each used-symbol bijection arbitrarily to all four symbols. This gives an actual allowed automorphism mapping one set to the other. The argument includes unused symbols and repeated normalized columns.

The resulting orbit counts and independently counted labeled populations are:

| Slice size | Orbits | Labeled independent sets |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 1 | 64 |
| 2 | 2 | 1728 |
| 3 | 5 | 25,920 |
| 4 | 18 | 239,760 |
| 5 | 39 | 1,437,696 |
| 6 | 121 | 5,728,896 |
| 7 | 253 | 15,326,208 |

`audit.py` independently validates orbit coverage by orbit–stabilizer accounting. It uses arbitrary-precision Python integers and entry permutations, checks independence and distinct canonical codes, and computes each stabilizer as follows. Let \(t\) be the number of entry orderings attaining the minimum normalized triple. Let \(u_j\) be the number of symbols used in column \(j\), and let the multiplicities of identical normalized columns be \(m_1,m_2,\ldots\). Then
\[
|\operatorname{Stab}(A)|
=t\prod_j(4-u_j)!\prod_h m_h!.
\]
To see this, fix one entry ordering attaining the minimum. For each other such ordering, matching identical normalized columns gives \(\prod_hm_h!\) coordinate bijections. The symbols used in a matched column have their images forced, while unused symbols admit \((4-u_j)!\) extensions. These choices correspond bijectively to stabilizing automorphisms. For the empty set the stabilizer is the entire group.

Separately, the audit counts **all labeled independent sets** by four distinguished row matchings. In a fixed row, entries form a matching between four columns and four symbols. There are
\[
\sum_{r=0}^4\binom4r^2r!=209
\]
such matchings, including the empty one. Row matchings in different rows must be disjoint as sets of column-symbol pairs. A dynamic program on the 16-bit union of used pairs appends each of the 209 possible row matchings when disjoint, retaining total sizes at most seven. Every labeled independent set occurs exactly once as its four ordered row matchings. The orbit-size sums \(\sum_A82944/|\operatorname{Stab}(A)|\) equal these independently obtained labeled counts at every size. Distinctness plus this mass equality supplies a second complete-coverage argument.

The initial graph-isomorphism-based discovery enumeration and the permutation-based C generator also agreed entry for entry on every representative. That exploratory comparison is not needed for public reproduction. No graph-isomorphism library or external catalogue is imported by the published verification.

## 3. Exact layer-extension interface

Fix a representative \(A\) of size \(k\). Write
\[
U=W\setminus N_{H(3,4)}[A],\qquad
P=W\setminus(A\cup U).
\]
The remaining three layers occupy some positions of \(W\setminus A\), with each occupied position colored by its layer, using colors \(0,1,2\).

At most one of these colors can occupy a position, because two entries with the same projected triple in different layers are adjacent in \(H(4,4)\). Adjacent positions in \(H(3,4)\) cannot receive the same color, because that would violate independence inside a layer. Every position in \(U\) must be occupied: otherwise its first-layer word would be undominated.

Every occupied projected position is already dominated in all four layers, by staying at that entry or changing its first coordinate. At an unoccupied projected position, each layer must instead supply a neighboring projected entry. The first layer supplies one precisely when the position is in \(P\); each of the other three layers must supply a neighbor of its own color. Thus the exact interface is:

1. Each position of \(U\) receives exactly one of three colors.
2. Each position of \(P\) receives at most one color.
3. Adjacent positions cannot have the same color.
4. Every unoccupied position of \(P\) has a neighbor of each color.
5. Exactly \(29-k-|U|\) positions of \(P\) are occupied.

These conditions are both necessary and sufficient for an independent dominating 29-word code extending \(A\). The proof above checks all positions, including those in \(A\), in \(U\), and in \(P\). A negative value of \(29-k-|U|\), or one exceeding \(|P|\), immediately excludes the extension.

Because the distinguished slice was globally smallest, all other coordinate slices must also have at least \(k\) entries. For each of the three remaining layers, impose this lower bound on its color count. For each of the twelve slices in the other three coordinates, subtract the known contribution from \(A\) and impose the residual lower bound on the corresponding colored positions. These constraints are necessary for a normalized counterexample; they do not assume that the four first-coordinate slice sizes alone are minimal.

One harmless color normalization is used. If \(U\ne\varnothing\), assign its first position color zero. If it has a neighbor in \(U\), assign the first such neighbor color one. Both positions are forced occupied and are adjacent, so they have distinct colors in every solution. Permuting the remaining three layers realizes this normalization without changing any condition. No normalization is imposed if the relevant positions do not exist.

## 4. CNF equivalence and cardinality gates

`model.py` assigns a Boolean variable \(x_{v,c}\) to each allowed position and color. Pairwise clauses forbid two colors at one position and equal colors at adjacent positions. Each \(v\in U\) has the clause \(x_{v,0}\vee x_{v,1}\vee x_{v,2}\). For \(v\in P\), an occupancy variable \(y_v\) is equivalent to that disjunction. Its three coverage clauses are
\[
y_v\vee\bigvee_{w\in N(v)\setminus A}x_{w,c},
\qquad c=0,1,2.
\]
The cardinality conditions are exactly those in Section 3. All these clauses directly express that interface, so a satisfying assignment decodes to a normalized counterexample, and every normalized counterexample extends to a satisfying assignment.

Cardinality gates are implemented in the published source, not imported from a solver library. For input literals \(z_1,\ldots,z_n\), the auxiliary variable \(s_{i,j}\) means that at least \(j\) of the first \(i\) inputs are true. Constants are \(s_{i,0}=\mathrm{true}\) and \(s_{i,j}=\mathrm{false}\) for \(j>i\). The exact recurrence is
\[
s_{i,j}\longleftrightarrow
s_{i-1,j}\vee(s_{i-1,j-1}\wedge z_i).
\]
For \(o\leftrightarrow a\vee(b\wedge z)\), the four clauses are
\[
(\neg a\vee o),\quad
(\neg b\vee\neg z\vee o),\quad
(\neg o\vee a\vee b),\quad
(\neg o\vee a\vee z).
\]
The acyclic recurrence forces unique correct values by induction. Setting \(s_{n,L}\) and, when needed, \(\neg s_{n,R+1}\) is equivalent to \(L\le\sum z_i\le R\). Only the necessary prefix columns are created. Boolean constant elimination, duplicate removal, and tautology removal preserve each clause's meaning.

## 5. Complete proof computation and its trust boundary

There are \(18+39+121+253=431\) representative cases. All **431** generated CNFs have UNSAT certificates accepted by the independent DRAT-trim checker. The instance-manifest SHA-256 is

```text
4dcb262693cf41194511e287460e3cfe87971127e468c8136e0696018ad6d6f0
```

This digest covers the ordered case size, case index, representative mask, and exact DIMACS SHA-256 for every case. `run_proofs.py` regenerates the formulas and proofs, invokes the checker on each exact serialized formula, rejects non-UNSAT/unfinished solver results or rejected proofs, and checks the final manifest against `EXPECTED_RESULT.json`. A full invocation first performs the independent orbit and interface audits. A restricted invocation reports **PARTIAL** and cannot emit the complete theorem result.

Reproduction uses Python-SAT 1.8.dev24's Glucose 4.1 interface for proof generation and DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` for proof checking. The solver's negative verdict is not accepted by itself. The published encoding has explicit Boolean gates; no external cardinality encoder is trusted. Proof traces are regenerated locally and checked sequentially, with the current CNF and proof overwritten only after each completed check. Large traces and solver binaries are not published.

The additional exact audits check 7423 cardinality input/range assignments through seven inputs, every one of the 65,536 subsets of \(H(4,2)\) against the independent layer interface, and the actual known 28- and 30-entry witnesses. The binary audit obtains 24, 16, and 2 maximal sets of sizes 4, 5, and 8. The positive controls exercise every globally minimum slice orientation: two for the 28-word control and nine for the 30-word control, including the color normalizations and all counter gates. Their exact coverage histograms agree with the independently reviewed original witnesses. A duplicate-entry corruption is rejected for each control. These checks support the interfaces; the universal equivalences above are written proof obligations, not inferred from examples.

The C enumerator uses only unsigned 64-bit masks and canonical codes of at most 42 bits; shifts are at most 63 and occur on unsigned values. Its orbit-capacity bound is checked explicitly, and exceeding it terminates with an error. Normal and address/undefined-behavior-sanitized executions agree on every representative. The independent Python audit uses arbitrary-precision arithmetic.

The evidence is an exact computer-assisted theorem, not a proof-assistant formalization. Remaining trust is the written reduction and canonicalization arguments, the exact generators and independent audits, the DRAT-trim checker and proof-format semantics, Python/C execution, toolchains, and hardware. There is no floating point, random sampling, omitted search case, symmetry assumption about the full cube, or external graph catalogue in the proof.

## 6. Prior results, provenance, and scope

Britz, Cavenagh, and Sørensen, [*Maximal partial Latin cubes*, EJC 22(1), P1.81 (2015)](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v22i1p81/pdf/), Theorem 11 gives the order-four spectrum outside the possible sizes 28, 29, and 30. The current exclusion and the known positive witnesses therefore give the displayed complete spectrum.

The 28-membership and minimum 28 are classical coding results, recorded by Donovan, Grannell, and Yazıcı in [*On maximal partial Latin hypercubes*, DCC 92 (2024)](https://link.springer.com/article/10.1007/s10623-023-01314-5), citing Östergård, Quistorff, and Wassermann, [*New Results on Codes with Covering Radius 1 and Minimum Distance 2* (2005)](https://doi.org/10.1007/s10623-005-6404-3). The 2015 three-value open formulation overlooked that earlier equivalent-code result. We make no novelty claim for 28. The 2005 publisher endpoint was inspected, but its full text was not recovered in this pass.

`control28.json` and `control30.json` are the small mathematical witness lists from the [previous source contribution](https://github.com/helgithorskarp/math_results/tree/main/design_theory/maximal_partial_latin_cube_order4), originally published at commit `ec60305433f1d958d49ed60f0ed336d5b21a0d75`, independently accepted in graph review h1699. The 30-membership and its graph equivalence also have a [Lean formalization](https://github.com/njallskarp/math_source_code_open/tree/main/mplc_order4_30). Their use here is as credited controls and as the positive inputs to the spectrum corollary. The 29-exclusion does not depend on them.

Live searches in Latin-cube, spectrum, and equivalent covering-code terminology found no previous resolution of size 29 in the inspected primary sources or committed graph. Novelty is search-relative, not a historical-priority claim. Independent peer review of this new exclusion and its complete-spectrum corollary is pending.
