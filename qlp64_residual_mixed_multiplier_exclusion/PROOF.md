# Residual mixed multiplier 33: proof and complete coverage

## Statement

For a cyclic row, put \(C_X(k)=\sum_jX_j\overline{X_{j+k}}\).
A quaternary Legendre pair (QLP) of length 64 has entries in
\(\{1,i,-1,-i\}\) and \(C_A(k)+C_B(k)=-2\) for every nonzero lag.

**Computer-assisted theorem.** No such pair satisfies
\[
\sum A=0,\quad\sum B=1+i,\qquad
A_{33j}=\overline{A_j},\quad B_{33j}=B_j.\tag{1}
\]
The proof excludes a complete necessary system at compressed length 32.
It has no length-64 candidate queue as an input and makes no assertion of
unrestricted nonexistence.

**Conditional corollary.** Combining this theorem with the corrected ordinary
exclusion and the mixed 31/63 exclusion, a QLP of length 64 has no nonidentity
common affine index permutation fixing its members, even if independent
global fourth-root phases and optional alphabet conjugations accompany that
permutation. Allowing row interchange adds no stabilizing index permutation.
The two earlier exclusions are separate computational dependencies, not
replayed by this package. See Section 7 for their exact provenance and scope.

## 1. Necessary compressed equations

Summing all QLP equations gives
\(|\sum A|^2+|\sum B|^2=2\). In even length, a Gaussian row sum has real
and imaginary coordinates of the same parity. Consequently one row sum is
zero and the other has norm 2; row interchange and a fourth-root rotation
of the latter give the normalization in (1).

Since \(33^2=1\pmod {64}\), changing summation indices in (1) gives
\[
C_A(33k)=\overline{C_A(k)},\qquad C_B(33k)=C_B(k).
\]
The QLP equations at \(k\) and \(33k\) therefore force both individual
autocorrelations to be real.

Use the standard bijective binary Gray map
\[
G(x,y)=\frac{x+y}{2}+i\frac{x-y}{2}.
\]
Write \(A=G(x,y)\), with binary row sums zero, and \(B=G(s,r)\), with
binary row sums 2 and zero. For \(d\in\{2,4,8,16,32\}\), half-compress a
binary row by
\[
v^{(d)}_j=\frac12\sum_{t=0}^{64/d-1}v_{j+td}.
\]
These entries are integral and bounded in absolute value by \(M=32/d\).
The actual unscaled complex compression of \(A\) is real: 33 is congruent
to 1 modulo \(d\), so (1) makes that compression equal to its conjugate.
Its two binary half-compressions thus coincide; call the resulting row
\(p\). Denote those of \(B\) by \(s,r\) again.

At full length, 33 fixes the even indices and interchanges \(j,j+32\) at
odd indices. For every odd compressed coordinate, the binary terms of
\(B\) are paired equal signs. Its half-compression is a sum of \(M\)
signs, hence has parity \(M\). There is no imposed parity at even coordinates
of \(r,s\), or at any coordinate of \(p\).

Every actual pair produces a triple satisfying all of
\[
\begin{gathered}
p,r,s\in\mathbb Z^d,\quad |p_j|,|r_j|,|s_j|\le M,\qquad
\sum p=\sum r=0,\quad\sum s=1,\\
r_j\equiv s_j\equiv M\pmod2\quad(j\text{ odd}),\tag{2}\\
2C_p(k)+C_r(k)+C_s(k)=T_d(k),\qquad
T_d(0)=65-64/d,\quad T_d(k)=-64/d\quad(k\ne0),\tag{3}\\
\sum_jr_js_{j+k}=\sum_js_jr_{j+k}\quad\text{for every }k.\tag{4}
\end{gathered}
\]
Here the autocorrelations are of real integer rows. The real Gray identity
and compression of the full binary correlation total give (3). The actual
complex compressions are \(2p\) and \(2G(s,r)\); expanding the imaginary
part of the latter's autocorrelation gives (4). Compression sums full
autocorrelations over congruent lags, so the already proved reality justifies
this condition. No assumption of independent conjugation as a global QLP
equivalence is required.

At zero lag, (3) bounds the energies by
\(\|p\|^2\le\lfloor T_d(0)/2\rfloor\) and
\(\|r\|^2,\|s\|^2\le T_d(0)\). Autocorrelation of real rows is even in
the lag, and the difference in (4) is odd; checking lags up to the midpoint
therefore checks all lags. Neither \(r\) nor \(s\) is assumed reversible.
The polynomial-square condition from the earlier 31/63 family is not used.

## 2. Roots and exhaustive lifting

`cover.py` generates every bounded length-4 row by choosing its first three
entries and setting its last to the required sum. It applies (2) and the
energy bounds, giving 249 choices for \(p\), 171 for \(r\) and 190 for
\(s\). Exact matching of (3), followed by (4), gives **224 labelled triples**.
The independent root audit enumerates the entire four-dimensional boxes and
their Cartesian triple product, checking all-lag Gaussian arithmetic.

The optional length-2 calculation is a useful explanation, not an imported
root restriction. Put \(p=(a,-a)\), \(r=(b,-b)\), \(s=(c,1-c)\).
Then \(b\) is even, \(c\) is odd, and
\[
2a^2+b^2+c^2-c=16.
\]
The four possibilities are \((a,b,c)=(0,\pm2,-3),(0,\pm4,1)\).
Thus \(A\) must balance separately on even and odd indices. At length 4,
let \(R=r_0-r_2\), \(V=r_1-r_3\), \(S=s_0-s_2\), \(T=s_1-s_3\).
Equation (4) says \(RT=SV\). Here \(R\) is even, \(S\) odd, and \(T\)
divisible by 4. Therefore \(V\) is divisible by 8, excluding \(b=\pm2\),
for which \(V\equiv2\pmod4\). In particular any pair in (1) would have
\(A(-1)=0\) and \(B(-1)\in\{9-7i,-7+9i\}\).
The complete 224-root calculation imposes the original equations directly.

Folding a child of length \(2d\) to its parent is
\(v_j=u_j+u_{j+d}\). It preserves (2)--(4): sums and parity follow by
addition, while autocorrelations and cross-correlations sum over congruent
lags. For \(d=4,8,16\), the indices \(j\) and \(j+d\) have the same parity.

For every parent row, enumerate each first-half child entry \(u_j\) in its
entire bounded range and set \(u_{j+d}=v_j-u_j\). Reject only out-of-bounds
entries, the required odd-coordinate parities for \(r,s\), and excessive
energy. Every child has exactly one such first half. `lift_match.cpp` uses
recursive enumeration with early nonnegative-energy pruning. The independent
Python oracle enumerates the full Cartesian product and tests energy at the
leaf; it compares complete encoded row sets, not just counts.

At each stage every supplying row is retained for each correlation key.
Matching all eligible row pairs therefore returns every triple satisfying
(3)--(4) above each input parent. Hash collisions are resolved by exact keys.

## 3. The compressed symmetry quotient

The following are automorphisms of the **necessary system (2)--(4)**:

- On \(p\) independently: any cyclic shift, reversal and sign change.
- On \((r,s)\) together: any even cyclic shift and reversal; also an
  independent sign change of \(r\).
- On all three rows together: index multiplication by any odd unit modulo
  the compressed length.

Independent row shifts preserve autocorrelations. The simultaneous shifts
of \(r,s\) preserve their cross-correlations, their simultaneous reversal
negates the cross-correlation difference, and changing the sign of \(r\)
also negates that difference. Even shifts and odd units preserve the parity
of indices. Simultaneous decimation permutes the lag equations, whose target
is constant off zero. Every listed action is invertible.

Odd units normalize the translation/reversal actions, and signs commute
with them. `quotient.py` minimizes lexicographically over the common unit,
then independently over the indicated actions on \(p\) and \((r,s)\).
Every selected representative is related by an explicitly allowed action.
The audit checks such a relation for every generated tuple, rather than
assuming that equal summary statistics imply equivalence.

Crucially, these actions lift to the next compressed length and commute with
folding: a parent shift lifts to the same shift, an even shift stays even,
and a parent odd unit has an odd-unit lift. Thus every child above an omitted
parent is mapped into a child above the chosen parent representative. Induction
proves complete coverage of the necessary system at every later stage.

An odd shift of \(p\) is **not asserted to be an equivalence of full mixed
QLPs**. The quotient is used to prove emptiness of the larger compressed
necessary system. Invertibility and closure of that system, together with
commutation with folding, suffice. No full length-64 reconstruction from a
quotient representative is used. Treating these compressed representatives
as full QLP isomorphism classes would be incorrect.

All 38,400 length-8 triples are generated before taking their 87
representatives. Complete lifting above these gives 4,352 length-16 triples,
which yield 190 representatives. The 4,352 count is over the selected
length-8 parents, not the entire unreduced length-16 domain. The 190
representatives nevertheless cover the complete necessary length-16 system
up to the proved actions. The audit also checks the generators against
folding on all 87 length-8 representatives, for 609 exact checks.

## 4. Half-period energy budget

At final compressed length 32 all entries are ternary; \(r,s\) have
\(\pm1\) at each odd position. For a length-16 parent triple \((p,r,s)\),
define
\[
L_p=\sum_j|p_j|,\qquad
L_r=16+\sum_{j\text{ even}}|r_j|,\qquad
L_s=16+\sum_{j\text{ even}}|s_j|.
\]
These are exact individual minimum child energies. For a ternary child,
the energy equals its number of nonzero entries. Folding a pair to \(v\)
requires at least \(|v|\) such entries; that minimum is attained for
\(v\in\{-2,-1,0,1,2\}\). At the odd positions of \(r,s\), all 16 child
entries must instead be nonzero. The parent parity permits all these minima.

Since the required weighted energy is 63, every final child must satisfy
\[
2L_p+L_r+L_s\le63,\qquad
\|p'\|^2\le\left\lfloor\frac{63-L_r-L_s}{2}\right\rfloor,
\quad\|r'\|^2\le63-2L_p-L_s,
\quad\|s'\|^2\le63-2L_p-L_r.\tag{5}
\]
The first inequality excludes 158 of the 190 parent representatives.
For the other 32, the individual caps preserve every possible triple.
The independent audit enumerates each coordinate's allowed pairs and its
minimum energy for **all 190 parents**, agreeing with these closed formulas,
including the 158 excluded cases. The test is also invariant under the
compressed quotient, since that quotient preserves total absolute value
and preserves even positions of \(r,s\).

For perspective, (3) at final length gives \(\|p'\|^2\le14\): each other
row has at least 16 nonzeros, \(s'\) has odd energy and hence at least 17,
and a sum-zero ternary \(p'\) has even energy. This is a restriction from
the pair equations, not positivity of the conjugated row's half-period
autocorrelation. The source supplies a length-16 single-row counterexample
with mixed multiplier 9, real autocorrelations, sum zero, and \(C_A(8)=-8\).
Thus the ordinary half-period positivity lemma cannot be transferred to
conjugation.

## 5. Final exhaustion and independent reproduction

For the final stage, put the larger of the two \(r,s\) row fibers into an
exact-key table and enumerate \(p\) with the smaller fiber. Every table
supplier remains available. This changes the matching order, not its domain.
There are 466,944 stored row occurrences and **11,362,432 pair operations**.
Exactly **1,280 triples** satisfy the complete real equations; none satisfies
(4). The independent Python replay checks their original compressed Gaussian
coordinates \(2p\) and \((s+r)+i(s-r)\) directly. The first nonzero imaginary
lag is 1 in 960 cases and 2 in 320 cases. All real lag equations are checked
on every candidate up to its rejection.

The final proper cover is therefore empty, proving (1). Its compact JSON is
`[]` followed by a newline, with SHA-256
`37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`.
The canonical list of all 1,280 intermediate real matches has SHA-256
`9d841032d1e1fbee2340d317172e5cba87f72c2b7e3ffb8658e2b8344cb5d056`.
These hashes bind outputs; the coverage arguments establish the domain.

The complete checks supplied by the reproduction command are:

- Full-box, all-lag root enumeration, and explicit orbit/folding checks.
- Complete Python/native agreement on all 38,400 length-8 triples.
- Complete row-set equality for 47 length-8, 88 length-16 and 57 length-32
  fibers, with respectively 28,589, 1,515,997 and 453,134 children. The direct
  box totals are 81,525, 1,951,213 and 22,471,254. Additional empty and nonempty
  controls challenge energy-bound edge cases.
- A separate length-16 matcher on the audited rows. It uses a direct indexed
  bucket array, full-key comparisons, and Gaussian imaginary parts, importing
  no production matching code. It visits all 5,276,583,504 row pairs and
  reproduces all 4,352 triples, entry for entry.
- A complete Python final replay on the audited row sets, including every
  real match and its direct Gaussian rejection.

The row-export executable invokes the production lifting function under test;
the independent product-box oracle validates its entire output. The separate
matching replays use these **audited** rows. This is an explicit shared-data
interface, not an imported unverified candidate queue.

## 6. Arithmetic and trust boundary

Python integers are unbounded. Native child lengths are at most 32, entry
bounds at most 4, and unpruned quadratic sums have magnitude at most 512.
All decisions fit comfortably in signed `int`. Native row indices fit in
signed 32 bits: even the unpruned first-half boxes have at most \(5^8\)
rows at length 16 and \(3^{16}\) at length 32; the special binary odd entries
give a smaller bound for the other two rows. Pair and operation counters
are unsigned 64-bit values on the recorded finite inputs.

The alternate length-16 bucket uses energy and two correlation coordinates.
The stored energy is between 1 and 61; each other stored coordinate is in
\([-64,56]\). Queried energies at least 64 cannot match and are rejected;
queried correlation coordinates lie in \([-122,122]\). Eight bits per
signed shifted coordinate and a \(2^{22}\)-entry bucket array therefore
suffice, with checked indices. The remaining coordinates are compared exactly.

Row encodings use bases 9, 5 and 3 at lengths 8, 16 and 32, respectively.
They are injective and below \(2^{64}\). Hash arithmetic intentionally wraps
unsigned integers and never substitutes for full-key equality. There is no
floating-point cutoff, solver, external candidate catalogue or proof assistant.
Trust remains in the written reductions, source, interpreter/compiler and
standard libraries, and execution hardware. Algorithmic independence here
means author-run independent implementations; it is not fresh external review.

## 7. Affine consequence and precise dependencies

The corrected ordinary theorem is at
[source directory](../qlp64_corrected_multiplier_exclusion), commit
`159c7e41b4c57a160d6338cde7346beebb774799`, graph height 4283,
`bafkreiemfckauq3e6zmztzyklhsmjxkmrf6i25gwwpa63p2ffgdontaate`.
The mixed 31/63 theorem and its affine reduction are at
[source directory](../qlp64_mixed_multiplier_exclusion), commit
`f2116a07b537ed8864525b528d2b5250784c6ee1`, graph height 4295,
`bafkreiag36hkck6t3jb62ouzvl7ys2skikxbn3dghprwyeivylhed7gvjm`.
The historical defective ordinary computation and its withdrawal are not
premises. Neither earlier complete exclusion is rerun by this package.

For completeness, the reduction is as follows. Suppose
\(\phi(j)=hj+b\), with \(h\) odd, fixes a normalized pair through
\[
A_{\phi(j)}=\alpha\operatorname{conj}^{\epsilon}(A_j),\qquad
B_{\phi(j)}=\beta\operatorname{conj}^{\delta}(B_j),
\quad\alpha,\beta\in\{1,i,-1,-i\},\quad\epsilon,\delta\in\{0,1\}.
\]
Summing the second equation forces either \(\delta=0,\beta=1\), or
\(\delta=1,\beta=i\). In the latter case the alphabet permutation
\(z\mapsto i\bar z\) forces counts \((u,u,v,v)\), with \(u-v=1\),
and thus length 2 modulo 4. That case is impossible here.

The affine group modulo 64 has order 2048. All cycles of its elements have
power-of-two length. If \(\phi\) had no fixed point, \(B_{\phi(j)}=B_j\)
would make both coordinates of \(\sum B\) even. Hence \(\phi\) has a fixed
point \(t\). If \(\epsilon=0\), evaluation there forces \(\alpha=1\),
and the ordinary theorem excludes a nonidentity map. Otherwise
\(\alpha=A_t^2\in\{1,-1\}\); rotating \(A\) by 1 or \(i\) sets it to 1.
The square \(\phi^2\) fixes both members ordinarily, so the ordinary theorem
makes that square the identity. Centering at \(t\) leaves one of the three
nonidentity unit involutions 31, 33, 63. The two mixed theorems exclude all
three. Equivalently, this new result removes both residual maps \(33j\) and
\(33j+32\), which differ by shifting the common origin by an odd index.

Row interchange cannot stabilize the normalized pair because zero and
\(\sqrt2\) are different Gaussian sum magnitudes. Global alphabet operations
accompanying the identity index map are outside the asserted triviality of
the **index** stabilizer. Index-dependent phases and different affine index
maps on the two members are also outside this corollary.
