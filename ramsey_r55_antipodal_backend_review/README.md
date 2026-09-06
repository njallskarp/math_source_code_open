# Independent pointwise review of the fixed H92 backend

## Verdict

The complete CNF at Discovery Net height 3272 is accepted as an exact
auxiliary encoding of the previously reviewed fixed H92 mixed system.
The independent certificate proves the following pointwise statement,
which is stronger than merely observing equal satisfiability statuses.

Let \(x\in\{0,1\}^{523}\) be a retained-edge assignment, let
\(\mathcal P(x)\) denote the complete fixed mixed specification below,
and let \(C(x,y,z)\) be the emitted CNF, where \(y\) contains 208 margin
bits and \(z\) contains 10,074 arithmetic bits. Then

\[
\#\{(y,z):C(x,y,z)\}=
\begin{cases}
1,&\mathcal P(x),\\
0,&\neg\mathcal P(x).
\end{cases}
\]

This is an independent review of the author's encoding, not a new
Ramsey theorem or general counting method. No solver was run. The author's
bounded UNKNOWN remains UNKNOWN. There is no claim that a full graph
completion is unique, that the fixed family covers every hypothetical
Ramsey graph, or that any family is eliminated.

Target:
bafkreih4cbsb6brwvjze6vnzwhxwexrtyqip3ykxoh5tswqlba4derngbu,
height 3272.
[Author source](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_antipodal_degree_backend),
commit 7f25e7786bbb850b2979a9d877543f1dc44ec5df.
The public merge commit was b70010d38d00c0e47fc74dfc382429453b0e5ef8.

## Exact graph and mixed-system domain

Use vertices \(0,\ldots,42\). On \(H=\{0,\ldots,19\}\), fix H92.json,
whose red-edge count is 92 and SHA-256 is
926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466.
Write

\[
W=\{2,\ldots,9\},\quad D_0=\{10,\ldots,13\},\quad
D_1=\{14,\ldots,17\},\quad D_{01}=\{18,19\},
\]

\[
X=\{20,\ldots,28\},\quad Y=\{29,\ldots,37\},\quad Z=\{39,\ldots,42\}.
\]

The fixed red stars are

\[
N_R(0)=D_0\cup D_{01}\cup Y\cup Z\cup\{38\},\quad
N_R(1)=D_1\cup D_{01}\cup X\cup Z\cup\{38\},\quad N_R(38)=H.
\]

Other root edges are blue. Require red degrees 20 at \(0,1,38\)
and 21 elsewhere. Each red root neighborhood has no red \(K_4\) or
blue \(K_5\); each blue root neighborhood has no blue \(K_4\) or
red \(K_5\). The blue neighborhoods of 0 and 1 each have 124 red edges.
No other global \(K_5\) predicates, symmetry, quotas, or opposite-core
choices are imposed.

There are 276 fixed pairs and 627 free pairs. The 104 free pairs in
\(Z\times W,D_0\times X,D_1\times Y\) occur only in degree equations
of this subsystem. The 523 other free pairs, in lexicographic order,
are variables \(x_1,\ldots,x_{523}\).

Put

\[
r(v)=d^*(v)-d_{\mathrm{fixed},R}(v)
      -\sum_{\substack{e\text{ retained}\\v\in e}}x_e.
\]

The specification \(\mathcal P(x)\) keeps every neighborhood clause and
both densities, requires \(r(v)=0\) at \(0,1,18,19,38\), and imposes
the following on each of the three blocks \(L\times R\):

\[
0\leq r(i)\leq|R|\ (i\in L),\qquad
0\leq r(j)\leq|L|\ (j\in R),\qquad
\sum_{i\in L}r(i)=\sum_{j\in R}r(j),
\]

\[
\sum_{i\in S}r(i)\leq\sum_{j\in R}\min\{r(j),|S|\}
\quad(\varnothing\ne S\subseteq L).
\]

All margins are integers since \(x\) is Boolean. The prior projection
theorem says that \(\mathcal P(x)\) holds exactly when \(x\) extends
to the original fixed subsystem. That theorem and its physical interface
are explicit dependencies:

- Height 3256,
  bafkreidufm26hzufnaopoyiorhpdgiwei7pk6uuv56cpewvjlqrofir6fq,
  [projection source](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_antipodal_degree_projection),
  commit 40a6cd7ffbe45892bd52e3dfcdbb086f1b5afbfd.
- Height 3266,
  bafkreihowil3ijiqegbezgvnvpror7gbgxjrkwp7l5poqg3qhtxcugdshe,
  [independent physical review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_antipodal_projection_review),
  commit 31e969ac6b6d78f9dc0f50ab53242ea863496ea3.

This pass checks the full imported descriptor and physical clause stream
by their previously reviewed byte identities, rather than repeating that
graph audit. No supplementary margin census, fixture statistic, or
solver result is imported.

## Unary margins and unique extensions

A block vertex \(v\) has residual upper bound \(U_v\in\{4,8,9\}\).
Use \(U_v\) Boolean bits \(y(v,t)\) with
\(y(v,t+1)\Rightarrow y(v,t)\). These 170 implications force precisely
the prefixes of ones. Thus the word uniquely represents its sum in
\([0,U_v]\), and

\[
\min\{r(v),k\}=\sum_{t=1}^{k}y(v,t)
\]

for every required \(k\leq4\).

The 43 degree equations force each unary sum to equal the specified
residual. For fixed \(x\), either no such word exists or it is unique.
The two densities, three balances, and all 45 labeled subset comparisons
give exactly 93 high-level conditions. The three trivial root equations
and the redundant full-subset cuts are retained.

Each full adder has three earlier Boolean literals \(a,b,c\) and
two fresh outputs \(s,t\). Its complete actual CNF block is equivalent to

\[
s+2t=a+b+c.
\]

This relation has exactly one Boolean output pair for every input
assignment. Freshness and acyclicity therefore give exactly one
assignment to every arithmetic auxiliary once \(x,y\) are fixed.

The remaining audit establishes that the terminal assertions are
precisely the 93 required arithmetic conditions. This proves the
pointwise zero-or-one statement in both directions. Combining it with
the prior projection theorem gives existential equivalence with the
fixed graph subsystem, but not a bijection of its 104-edge lifts.

## Different certificate: affine conservation, not tree replay

The author checker reconstructs balanced count trees and ripple wiring.
The new checker instead treats the actual gate blocks as local exact
identities and proves the meaning of each terminal word algebraically.
It imports no author generator or checker modules.

Represent a word \(b_0,\ldots,b_{w-1}\) by the affine integer expression
\(\sum_i2^i b_i\). A negative literal is interpreted as \(1-x\);
Boolean constants have their exact integer values.

Starting at the last gate and proceeding backwards, suppose an
expression has coefficients \(k\) and \(2k\) on a gate's outputs
\(s,t\). Replace those terms by \(k(a+b+c)\). Reject any unmatched
output coefficient. Every replacement is a justified integer multiple
of the checked local identity and introduces only earlier variables.
The resulting expression uses only physical and margin bits.

For each of the 100 count outputs, this reduction yields exactly its
input sum. The input sum used by each degree, density, balance, or cut
is separately reconstructed from the pinned mathematical descriptor.
Equality is checked as an exact coefficient dictionary, not merely by
an aggregate value or a digest.

For every comparison, let \(A,B\) be the certified count words,
zero-padded to the same width \(w\). The entire \(w+1\)-bit comparator
output reduces to

\[
2^w+B-A.
\]

Both \(A\) and \(B\) lie in \([0,2^w-1]\), since they are unsigned
\(w\)-bit words. Consequently the high output bit is one exactly when
\(A\leq B\). The lower \(w\) output bits are retained, not discarded
as an unchecked carry assumption. This proves comparison correctness
for all assignments, without a bounded table of word pairs.

The checker verifies every local gate truth table with its actual
constants, repeated literals, and clause simplifications. It also checks
fresh ordered output ownership, complete physical and unary prefixes,
all terminal clause blocks, and a disjoint partition of the complete
clause stream. There is no extra clause that could silently strengthen
the system and no undefined auxiliary that could break uniqueness.

As a direct independence control, the checker deletes all count-tree
addition annotations and all comparator wiring annotations except output
words, and obtains the same complete audit. Those annotations are not
trusted inputs of this proof.

These circuit methods are classical. See Eén and Sörensson,
[Translating Pseudo-Boolean Constraints into SAT](https://doi.org/10.3233/SAT190014),
especially the full-adder gates and adder-network discussion. No priority
or runtime claim is made for binary arithmetic or affine substitution.

## Reproduction and compact evidence

Use CPython 3.12.12 and its standard library. From the public repository:

~~~bash
set -o pipefail
python3 -B ramsey_r55_antipodal_backend_review/verify.py \
  | cmp - ramsey_r55_antipodal_backend_review/EXPECTED.json
python3 -O -B ramsey_r55_antipodal_backend_review/verify.py \
  | cmp - ramsey_r55_antipodal_backend_review/EXPECTED.json
cd ramsey_r55_antipodal_backend_review
shasum -a 256 -c SHA256SUMS
~~~

The script downloads five pinned input files and executes the author's
generator only with its emit-only flag. All source hashes are checked
before execution. Temporary inputs and generated files are removed on
normal exit. No solver binary is needed or called.

Offline use accepts a root containing the two source directories with
the exact files listed in verify.py. An already generated pair of files
may instead be checked directly:

~~~bash
python3 -B verify.py --upstream /absolute/path/to/pinned-source-root
python3 -B verify.py --work /absolute/path/to/emitted-model
~~~

The compact output records:

- 10,805 variables and all 125,119 clauses.
- 5,037 actual full adders and 116,432 local truth assignments.
- 100 count identities, 45 comparator identities, and 7,947 exact
  gate substitutions across those identities.
- All 93 physical high-level conditions and 170 unary implications.
- 784 unary words, covering the widths 4, 8, and 9.
- Eight rejected corruptions: unary direction, missing cut, wrong
  population count, lost carry, reused output, bad gate clause, reversed
  comparison, and appended unexamined clause.

The following identities agree with the producer:

| Artifact | SHA-256 |
| --- | --- |
| Full CNF | 9afab291586190b946e30b935970c0dc09f9fc36d906ec816d7c2f5bed5e306f |
| Arithmetic layout | 8cac48de646842543af5cd207b8c176b11492e750806b179aabf0edfa1274e9e |

The independently reconstructed physical-expression certificate has
SHA-256 36ed118d1e9c4a8fa956433901b3368d6da436efb2d37205d22dd5a991818b7d.
The digest identifies the compared expressions; the checker itself
compares the coefficient dictionaries entrywise. The source and compact
EXPECTED.json regenerate the evidence. No CNF, large layout, raw trace,
database, solver binary, downloaded source, or private state is published.

## Trust, coverage, and stopping point

The imported mixed-system theorem and physical index meanings remain
explicit dependencies. The current arithmetic bridge is independently
checked by the displayed unformalized proof plus exact Python; this is
not proof-assistant formalization. Hardware, interpreter semantics,
parsing, and file identities remain trusted.

The author's solver runner's SAT/UNSAT terminal paths and runtime
statistics are outside this review. No solver status was inferred from
the exact encoding audit. The working range remains
\(43\leq R(5,5)\leq46\); see the published
[Angeltveit–McKay upper bound](https://arxiv.org/abs/2409.15709).

Covered: the complete actual CNF has exactly the intended auxiliary
extensions for every retained assignment of the fixed mixed subsystem.
Uncovered: whether that subsystem is satisfiable, whether any of its
solutions admits a full-\(K_5\)-compatible lift, and whether the fixed
H92/stars/degrees/densities cover any entire \(M=214\) branch.

This review is separate from slots 1/2's search and enlargement, slot
5's composition, and Helgi's solver work. It closes the proposed
backend-equivalence review gate; it eliminates no graph family.
The next useful interface is a genuinely stronger full-\(K_5\) lifting
model or a complete branch-normalization theorem. Do not rerun this
UNKNOWN or repeat margin/circuit enumeration without a new objection.
