# Exact bichromatic matching-cover normal form at \(m=10,\rho=21\)

## Result type

**Symbolic support-classification theorem with exact survivor certificates.**
Start from the exceptional \(m=10,\rho=21\) global blue-clause kernel
\((D,S)\). The 20 selected red \(K_4\)'s avoiding the singular vertex are
exactly a demand-constrained cover of the 41 edge occurrences of \(D\) by
20 distinct four-edge matchings. There are precisely two possible demand
vectors, according to whether the unique non-pivot vertex of selected red
degree three lies in the distinguished red triangle \(A\).

This is the first exact normal form in this lane that carries both colors at
once. It encodes all selected red supports, all selected blue supports,
bichromatic coverage, and every opposite-color support-intersection
constraint. Exact covers are exhibited for both published \(q=0,1\) blue
kernels and both demand cases. In all four witnesses, neither color's
selected supports force a \(K_5\). Consequently these joint selected-support
conditions still do not exclude the exceptional \(\rho=21\) stratum.

## Setup

The exceptional incidence profile has 21 selected red clauses and 23
selected blue clauses. Let \(w\) be the first singular vertex. Up to color
exchange its selected degrees are

\[
(d_R(w),d_B(w))=(1,10),\qquad
(d_R(u),d_B(u))=(3,2),                                    \tag{1}
\]

for one vertex \(u\ne w\), while every other vertex has selected degree
\((2,2)\). The unique selected red clause through \(w\) is

\[
R_0=\{w,a_1,a_2,a_3\}=\{w\}\cup A.                        \tag{2}
\]

The 23 selected blue clauses form the nodes of the already established
loopless multigraph \(D\). Each vertex \(x\ne w\) is represented by the
edge occurrence \(e_x\) joining its two selected blue clauses. The marked
ten-node set \(S\) consists of the blue clauses through \(w\).

## Matching translation

### Lemma 1: red clauses are matchings

For a four-set \(C\subseteq V(G)\setminus\{w\}\),

\[
|C\cap B|\le1\quad\text{for every selected blue clause }B
\quad\Longleftrightarrow\quad
\{e_x:x\in C\}\text{ is a four-edge matching in }D.       \tag{3}
\]

Indeed, a blue clause node is incident to both \(e_x\) and \(e_y\) exactly
when that selected blue clause contains both \(x\) and \(y\). Thus two of
the four edge occurrences share an endpoint exactly when \(C\) meets some
selected blue support twice.

Applying the same observation to \(A\), and remembering that \(R_0\) and a
side blue clause already share \(w\), gives

\[
\{e_{a_1},e_{a_2},e_{a_3}\}
\text{ is a three-edge matching and }
e_{a_j}\cap S=\varnothing\quad(j=1,2,3).                  \tag{4}
\]

Equation (4) is both necessary and sufficient for \(R_0\) to meet every
selected blue clause in at most one vertex.

### Lemma 2: the exact two demand vectors

For each edge occurrence \(e_x\), let \(r_x\) be the number of the 20 red
clauses avoiding \(w\) that contain \(x\). If \(u\in A\), then

\[
r_u=2,\qquad r_x=1\ (x\in A\setminus\{u\}),\qquad
r_x=2\ (x\notin A).                                      \tag{5a}
\]

If \(u\notin A\), then

\[
r_x=1\ (x\in A),\qquad r_u=3,\qquad
r_x=2\ (x\notin A\cup\{u\}).                           \tag{5b}
\]

These alternatives are forced directly by (1)--(2), since
\(r_x=d_R(x)-\mathbf 1_{x\in A}\). Conversely they recover the complete
selected-red degree profile. Both sum to

\[
\sum_{x\ne w}r_x=80=20\cdot4.                            \tag{6}
\]

## Bichromatic matching-cover theorem

### Theorem

Fix a valid marked blue kernel \((D,S)\), a three-edge matching
\(A_D=\{e_{a_1},e_{a_2},e_{a_3}\}\) avoiding \(S\), and one of the demand
vectors (5a)--(5b). A family of selected red supports realizing the
exceptional profile and meeting every selected blue support in at most one
vertex exists if and only if there are 20 **distinct** four-edge matchings

\[
M_1,\ldots,M_{20}\subseteq E(D)                           \tag{7}
\]

such that every edge occurrence has its prescribed multiplicity:

\[
|\{j:e_x\in M_j\}|=r_x\qquad(x\ne w).                    \tag{8}
\]

Equivalently, there is a binary matrix
\(Z\in\{0,1\}^{41\times20}\) satisfying

\[
\begin{aligned}
\sum_{j=1}^{20}Z_{xj}&=r_x &&(x\ne w),\\
\sum_{x\ne w}Z_{xj}&=4 &&(1\le j\le20),\\
\sum_{x:e_x\ni v}Z_{xj}&\le1
    &&(v\in V(D),\ 1\le j\le20),                        \tag{9}
\end{aligned}
\]

with pairwise distinct columns.

### Proof

Given selected red clauses, remove \(R_0\). Lemma 1 turns each of the
remaining 20 clauses into a four-edge matching. Clause-set semantics makes
the matchings distinct, and Lemma 2 gives (8). This proves necessity.

Conversely, make one red clause from the four original vertices represented
by each \(M_j\), and add \(R_0=\{w\}\cup A\). Matchingness in (7) gives
intersection at most one with every blue clause not containing \(w\).
Condition (4) handles \(R_0\) against non-side blue clauses and, because the
three \(A_D\)-edges avoid \(S\), against side clauses as well. Equations
(5)--(8) give red degrees \(1,3,2^{40}\); the blue kernel gives blue degrees
\(10,2^{41}\). Hence every vertex has bichromatic coverage with exactly the
exceptional signed-incidence profile. Distinctness in (7) prevents duplicate
red clauses. This proves sufficiency. \(\square\)

This converse is a decoding theorem: every solution of (9), together with
the marked \(A_D\), reconstructs the complete selected-support system without
an unrecorded combinatorial choice.

## Exact joint-color survivors

The compact certificate uses the two simple role-marked kernels already
published for

\[
q=|Q\cap A|\in\{0,1\}.                                    \tag{10}
\]

For each kernel it supplies one cover of type (5a) and one of type (5b), for
four certified joint-color systems in total. The definition-level checker
verifies:

1. every column is a four-edge matching and all 20 are distinct;
2. all 41 row sums equal the prescribed demand vector;
3. the marked \(A_D\) is a three-edge matching avoiding \(S\);
4. every red/blue selected-support intersection has size at most one;
5. the selected degrees are exactly (1); and
6. exhaustive five-subset inspection of the two support-union graphs finds
   no forced red or blue \(K_5\).

Run:

~~~bash
python3 ramsey_r55_symbolic_extension/verify_rho21_bichromatic_matching_cover.py \
  ramsey_r55_symbolic_extension/rho21-bichromatic-matching-cover-certificate.json
~~~

The checker uses only Python's standard library and exact finite operations.
It checks supplied witnesses; the written matching argument is the universal
classification proof.

## Consequence and next obstruction

Theorem (7)--(9) is a compact graph-sandwich projection that genuinely adds
the missing color information to the blue kernel. It supplies immediate
sound rejection rules: a candidate \((D,S,A_D,u)\) is impossible if it has
fewer than 20 distinct four-matchings or if its exact-demand system (9) has
no solution.

The four survivors show just as precisely what this layer cannot prove.
Even simultaneous red and blue selected supports, all cross-color
compatibility constraints, exact coverage, and the absence of a forced
monochromatic \(K_5\) do not by themselves eliminate \(\rho=21\). The next
obstruction must use at least one of:

- completion of the still-unspecified core edges to a two-coloring;
- the requirement that the completed red graph on \(N_R(w)\) is \(K_4\)-free
  and the completed blue graph on \(N_B(w)\) is \(K_4\)-free;
- completeness of the selected-clause set as the actual monochromatic
  \(K_4\)'s of that completion; or
- singular Davis--Putnam ancestry beyond the first fan.

This is therefore a certified survivor frontier, not an existence claim for
a Ramsey \((5,5,42)\) core or a 44-clause obstruction.

## Novelty assessment and literature position

Discovery Net was searched through indexed height 1187 for “matching cover,”
“edge multicoloring,” “red support,” “four-edge matching,” and “bicolored
incidence.” No contribution containing this bichromatic translation was
found. Fixed-size matching covers and edge multicoloring are established
graph-theoretic topics; for example, Wang, Song, Yuan, and Liu study fixed-size
matching coverings in *Discrete Mathematics* 309 (2009), 3311--3317,
[doi:10.1016/j.disc.2008.09.031](https://doi.org/10.1016/j.disc.2008.09.031).
No novelty is claimed for those general notions.

The apparently new Ramsey-specific content is the exact reduction of the
exceptional two-color support geometry to (4)--(9), including the two forced
demand vectors and the four exact joint-color survivors. This assessment is
limited to the targeted literature and graph searches; it is not a priority
claim.

## Scope and trust boundary

The theorem imports the exceptional \(m=10,\rho=21\) incidence profile and
the reviewed global blue-kernel construction. Its universal content is the
elementary incidence proof above. The certificate is exact evidence only for
the four explicit survivors. The checker neither enumerates all role-marked
kernels nor proves that every admissible kernel has a matching cover.

Most importantly, the partial support graph leaves many core edges
unspecified. Passing the checker does not provide a full two-coloring, show
that the selected clauses are all monochromatic \(K_4\)'s, or certify any
singular-DP history. No solver result, floating point, or exhaustive kernel
enumeration is promoted to a universal theorem.

## Public source and provenance

The reader-facing source is
[rho21-bichromatic-matching-cover-normal-form.md](https://github.com/njallskarp/math_source_code_open/blob/main/ramsey_r55_symbolic_extension/rho21-bichromatic-matching-cover-normal-form.md).

Immutable source commit: `SOURCE_COMMIT_PLACEHOLDER`.

- initial research-note SHA-256: `NOTE_SHA256_PLACEHOLDER`;
- exact-certificate SHA-256: `CERTIFICATE_SHA256_PLACEHOLDER`;
- checker SHA-256: `CHECKER_SHA256_PLACEHOLDER`.

Discovery Net publication status: pending independent prepublication review.
