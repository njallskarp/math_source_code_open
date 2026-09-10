# Mixed index/conjugation symmetry at length 64

All subscripts are cyclic. A quaternary Legendre pair (QLP) consists of two
length-64 rows over \(\{1,i,-1,-i\}\) such that
\[
C_A(k)+C_B(k)=-2\quad(1\leq k<64),\qquad
C_X(k)=\sum_j X_j\overline{X_{j+k}}.
\]

## 1. Statement and normalization

**Computer-assisted theorem.** There is no normalized QLP of length 64 with
\[
\sum A=0,\quad\sum B=1+i,\qquad
A_{hj}=\overline{A_j},\quad B_{hj}=B_j,
\qquad h\in\{31,63\}.
\]
The computation excludes a complete set of necessary half-compressions,
already at length 32. It does not enumerate or rely on an imported list of
length-64 candidates.

Summing the QLP equations over all lags gives
\(|\sum A|^2+|\sum B|^2=2\). Each row has even length, so the real and imaginary
parts of its Gaussian sum have the same parity. Thus one sum is zero and
the other has norm 2. Interchanging the rows and multiplying the nonzero-sum
row by a fourth root of unity gives the stated normalization. These operations,
and independent cyclic shifts, preserve the QLP equations.

Use the bijective Gray representation
\[
G(x,y)=\frac{x+y}{2}+i\frac{x-y}{2},\qquad x,y\in\{\pm1\}^{64}.
\]
Conjugation interchanges its two binary rows. Therefore
\(A=G(x,x_h)\), where \((x_h)_j=x_{hj}\) and \(\sum x=0\).
Write \(B=G(s,r)\), where \(\sum s=2\), \(\sum r=0\) and
both binary rows are fixed by \(h\).

## 2. Why the mixed row must have real autocorrelation

Since \(h^2=1\pmod {64}\), changing the summation index gives
\[
C_A(hk)=\overline{C_A(k)},\qquad C_B(hk)=C_B(k).
\]
Comparing the QLP equation at \(k\) and \(hk\) proves that \(C_A(k)\) is
real. Consequently \(C_B(k)\) is real as well. This includes the zero lag.
No assumption that conjugating just one row preserves arbitrary QLPs is used.

For \(d\in\{4,8,16,32\}\), define the integer half-compression of a binary row
by \(v^{(d)}_j=\tfrac12\sum_{t=0}^{64/d-1}v_{j+td}\).
It is integral because the number of summands is even. Write \(p,r,s\) for
the half-compressions of \(x,r,s\), respectively, at the current length.
Since both 31 and 63 reduce to \(-1\) modulo every such \(d\), the compressed
Gray rows are \(2G(p,p^*)\) and \(2G(s,r)\), with
\(p^*_j=p_{-j}\), \(r=r^*\), \(s=s^*\).

Compression sums autocorrelations over congruent lags; in particular it
preserves the assertion that all autocorrelations are real. Put
\(P(z)=\sum_{j=0}^{d-1}p_jz^j\). A direct expansion gives
\[
\operatorname{Im} C_{G(p,p^*)}(k)
=\frac12\left(\sum_jp_jp_{k-j}-\sum_jp_jp_{-k-j}\right).
\]
Hence every compressed \(p\) has the **axes property**
\[
P(z)^2=P(z^{-1})^2\pmod{z^d-1}.\tag{1}
\]
Equivalently, at every \(d\)-th root of unity \(\zeta\), \(P(\zeta)\) is real
or purely imaginary. This follows from real coefficients and
\(P(\zeta^{-1})=\overline{P(\zeta)}\).

## 3. Complete necessary compressed system

Set \(M=32/d\). The entries of all three rows are integers in \([-M,M]\),
with sums \(0,0,1\) for \(p,r,s\). The last two are symmetric under reversal.
Their endpoint parities are
\[
r_0\equiv r_{d/2}\equiv M\pmod2,\qquad
s_0\equiv M+1,\quad s_{d/2}\equiv M\pmod2.\tag{2}
\]
To see this, the only fixed indices of either full multiplier 31 or 63 are
0 and 32. The residue class \(d/2\) contains no fixed index and is partitioned
into pairs of equal binary entries. Its half-compression is a sum of \(M\)
signs. Reversal and the row sum then determine the parity at residue 0.
There is no endpoint parity condition on \(p\).

The real part of the Gray autocorrelation is half the sum of its binary
autocorrelations. Compressing the binary total gives the necessary equations
\[
2C_p(k)+C_r(k)+C_s(k)=T_d(k),\qquad
T_d(0)=65-64/d,\quad T_d(k)=-64/d\ (k\ne0).\tag{3}
\]
Here \(C\) is the integer periodic autocorrelation. One can also obtain (3)
by compressing the original QLP equations and dividing the resulting real
Gray identity by 2. All these autocorrelations are even functions of the lag,
so checking \(0\leq k\leq d/2\) checks every lag. In particular (3) bounds
the row energies by \(\|p\|^2\leq\lfloor T_d(0)/2\rfloor\) and
\(\|r\|^2,\|s\|^2\leq T_d(0)\). These are necessary, not additional
empirical pruning rules.

Every actual pair therefore produces a triple satisfying (1)--(3) at every
proper compression length. Folding from length \(2d\) to length \(d\) is
simply \(v_j=u_j+u_{j+d}\). It preserves all the stated necessary conditions.

## 4. Complete row lifting

### Axes row

Let \(v\) be an axes row of length \(d\), with \(d\) a power of two, and let
\(u\) be a child of length \(2d\) that folds to \(v\). Define
\(D_j=u_j-u_{j+d}=2u_j-v_j\), \(0\leq j<d\).
At roots whose order divides \(d\), the child polynomial equals the parent
polynomial. It already has the axes property there. The remaining roots have
order exactly \(2d\), and the child polynomial equals
\(D(z)=\sum_{j<d}D_jz^j\) at these roots.

For a primitive root \(\zeta\) of order \(2d\), (1) for the child requires
\((D(\zeta)-\overline{D(\zeta)})(D(\zeta)+\overline{D(\zeta)})=0\).
The cyclotomic field is a field and its minimal polynomial is
\(z^d+1\), of degree \(d\). Thus either of the following coefficient systems
holds, and conversely either one gives the axes property at every primitive
root:
\[
\begin{array}{ll}
\text{real branch:}&D_j=-D_{d-j}\ (1\leq j<d),\quad D_{d/2}=0;\ D_0\text{ free},\\
\text{imaginary branch:}&D_j=D_{d-j}\ (1\leq j<d),\quad D_0=0;\ D_{d/2}\text{ free}.
\end{array}\tag{4}
\]
Indeed, modulo \(z^d+1\), conjugating \(D(\zeta)\) replaces the coefficient
of \(z^j\), for \(j>0\), by \(-D_{d-j}\), while leaving \(D_0\) unchanged.
Irreducibility makes the coefficient comparison exact; there is no freedom
to choose different branches independently at conjugate primitive roots.

`mixed_lifts` enumerates the free endpoint and entries \(u_1,\ldots,u_{d/2-1}\)
in the entire child bound. The forced endpoint is \(v_j/2\); (4) determines
the other first-half entries, and folding determines the second half.
It rejects only nonintegral entries, entries outside the bound and excessive
energy. An exact set removes duplicate children appearing in both branches.
This enumerates every axes child above the given parent.

### Symmetric rows

For a symmetric child, \(u_j=u_{2d-j}\) and folding imply
\(u_{d/2}=u_{3d/2}=v_{d/2}/2\). Require only that this forced value be
integral and bounded. Enumerate \(u_0,u_1,\ldots,u_{d/2-1}\) in the full
child bound. Then \(u_d=v_0-u_0\), and for \(1\leq j<d/2\),
\[
u_{2d-j}=u_j,\qquad u_{d-j}=u_{d+j}=v_j-u_j.
\]
Apply (2) at the child's actual endpoints 0 and \(d\), together with bounds
and the energy cap. These formulas give every symmetric child exactly once.
**No endpoint parity is imposed on the forced quarter entries.** This is the
corrected distinction documented in the earlier parity correction.

## 5. Exhaustion and independent coverage checks

At length 4, `root_rows` enumerates all bounded \(p=(a,b,c,-a-b-c)\) and all
bounded symmetric rows \((a,b,c,b)\), then applies the exact predicates above.
`match` stores every \(p\) supplying a key \(T_d-2C_p\), loops over every
\((r,s)\), and returns every matching triple. At each doubling it repeats
this match on every parent's complete row fibers. Only identical triples are
deduplicated. There is no sign, permutation, decimation, or other quotient.
Induction on the folding map therefore proves that every actual mixed QLP
would appear as a triple in the final necessary cover.

The reproduced counts at lengths 4, 8, 16 and 32 are **8, 116, 1,312 and 0**.
The final compact JSON is exactly `[]` followed by a newline; its SHA-256 is
`37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`.
The empty length-32 cover proves the theorem. The expected file records all
intermediate hashes and counters; a hash alone is not a completeness proof.

The bounded Python audit directly enumerates the full length-4 boxes, checks
the root triple set using all lags, and checks all 6,561 ternary length-8 rows
using Gaussian arithmetic independent of (1). It includes empty parent fibers.
For the actual production parents at every stage:

- `axis_oracle.cpp` enumerates every bounded folding choice, without using
  (4), and directly checks integer cyclic convolution and energy. At length
  32 it checks 235,271,304 folding choices over all 184 distinct parents,
  including 96 empty fibers, and agrees on exactly 196,408 children.
- `symmetric_oracle.cpp` enumerates all bounded symmetric rows, checks their
  sum, energy and endpoint parities, and only then folds and looks up their
  parents. At length 32 its 14,348,907 interior assignments yield 10,476,351
  globally eligible rows and exactly 19,860 children over the 74 input parents.

Both oracles remove each accepted row from the supplied production set and
require it to become empty. They reject duplicates, omitted rows, extra rows
and trailing input. The runner derives the parent sets from every triple in
the complete preceding level, including parents with no successful triple
extension. This directly challenges omissions, not just emitted candidates.

## 6. Conditional affine phase/conjugation corollary

Use additionally the [corrected ordinary multiplier exclusion](../qlp64_corrected_multiplier_exclusion)
at source commit `159c7e41b4c57a160d6338cde7346beebb774799`, graph height 4283:
no nonidentity common affine index permutation fixes both rows individually.
That result has a separate complete computation and is **not replayed** by
this directory's command. The mixed theorem above does not depend on it.

**Corollary.** For a normalized length-64 QLP, suppose an affine permutation
\(\phi(j)=hj+b\), with \(h\) odd, satisfies
\[
A_{\phi(j)}=\alpha\,\operatorname{conj}^{\epsilon}(A_j),\qquad
B_{\phi(j)}=\beta\,\operatorname{conj}^{\delta}(B_j),
\]
where \(\alpha,\beta\) are fourth roots of unity and
\(\epsilon,\delta\in\{0,1\}\). If \(\phi\) is nonidentity, then
\[
\phi(j)=33j\quad\text{or}\quad\phi(j)=33j+32\pmod {64}.
\]
In either case \(\delta=0,\beta=1,\epsilon=1\); a fourth-root rotation of
\(A\) makes \(\alpha=1\). These are residual possibilities, not existence
claims. Allowing interchange of the two rows adds no stabilizer: their sum
magnitudes, zero and \(\sqrt2\), differ.

Proof. If \(\delta=0\), summing the second equation gives \(\beta=1\).
If \(\delta=1\), it gives \(\beta=i\). The alphabet map \(z\mapsto i\bar z\)
interchanges \(1,i\) and interchanges \(-1,-i\). Invariance under any
permutation would force the respective counts to be \(u,u,v,v\), with
\(u-v=1\). The length would be \(2(u+v)\equiv2\pmod4\), contradicting 64.
Thus \(B\) is fixed without alphabet conjugation or phase.

The affine group modulo 64 has order \(64\cdot32=2048\), a power of two.
Every cycle of \(\phi\) therefore has power-of-two length. If there were no
fixed point, every cycle would have even length; \(B_{\phi(j)}=B_j\) would
make both coordinates of \(\sum B\) even. Hence \(\phi\) has a fixed point
\(t\). If \(\epsilon=0\), evaluation at \(t\) forces \(\alpha=1\), and the
ordinary exclusion makes \(\phi\) the identity. For a nonidentity map we
therefore have \(\epsilon=1\), and evaluation at \(t\) gives
\(\alpha=A_t^2\in\{1,-1\}\). Rotating \(A\) by 1 or \(i\) sets \(\alpha=1\).

Applying the symmetry twice shows that both rows are ordinarily fixed by
\(\phi^2\). The ordinary exclusion implies \(\phi^2=\mathrm{id}\).
Shifting the common origin to \(t\) turns \(\phi\) into multiplication by
\(h\). The nonidentity involutions of the unit group modulo 64 are
31, 33 and 63. The mixed theorem rules out 31 and 63. For 33, the fixed-point
equation \(32t+b=0\pmod {64}\) forces \(b=0\) or 32, as asserted.

The structural audit enumerates all 2,048 affine maps: 1,365 are fixed-point
free, 100 are involutions, and 67 involutions have fixed points. The latter
are the identity, 32 maps each with multipliers 31 and 63, and the two maps
listed above. This finite audit checks the group bookkeeping; the algebraic
argument and ordinary exclusion are still required premises.

Independent conjugation of one member is not claimed to preserve all QLPs.
The corollary concerns operations fixing a given pair, so it makes no claim
about an orbit of arbitrary QLPs under such operations.

## 7. A false simplification and arithmetic boundary

An axes binary row need not be reversible about any cyclic origin.
`structural.py` completely checks balanced rows at lengths 4, 8 and 16. At
length 16 there are 154 axes rows, of which 16 have no reflection symmetry.
For example,
\[
(-1,-1,-1,1,1,-1,-1,1,-1,-1,1,1,1,-1,1,1)
\]
has that property. Thus the mixed theorem is not justified merely by assuming
that its axes condition implies an ordinary reflection symmetry.

Python uses unbounded integers. In the native oracles, lengths are at most
32 and entry bounds are at most 4. Even unpruned norms and convolution sums
have absolute value at most \(32\cdot4^2=512\), well within `int`. Row codes
use bases 9, 5 and 3 at lengths 8, 16 and 32, respectively; parent codes use
bases 17, 9 and 5 at lengths 4, 8 and 16. All are injective and less than
\(2^{64}\). At most \(5^{16}\) final parent words could occur, and each has
at most \(3^{16}\) folding choices; their product is below \(2^{64}\).
Smaller-stage bounds are lower. Counters use unsigned 64-bit integers.
Hash-container collisions are resolved by exact integer equality.

The trust boundary comprises the written reductions and coverage proof,
source correctness, Python/C++ implementations and standard libraries,
compiler, and execution platform. There is no floating-point threshold,
external candidate queue, solver or formal proof assistant. Independent
algorithms are author-run checks, not a fresh external mathematical review.
