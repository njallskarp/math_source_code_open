# Coverage and the finite-exclusion interface

This document supplies the mathematical reduction for the corrected computation.
The finite searches, their complete input hash and their execution status are
reported separately. A compressed candidate is not a quaternary Legendre pair.

## Normalization and the real system

Use cyclic indices and
\[
C_X(k)=\sum_{j=0}^{63}X_j\overline{X_{j+k}}.
\]
A QLP satisfies \(C_A(k)+C_B(k)=-2\) for every nonzero lag. Summing over all
lags shows that the squared absolute values of the two Gaussian row sums add
to 2. An even-length fourth-root row has Gaussian coordinates of equal parity.
Consequently one sum is zero and the other is \(\pm1\pm i\). Exchange and
rotate the rows to normalize them to \(0,1+i\). These operations preserve any
common fixed index multiplier.

The standard Gray map is
\[
G(x,y)_j=(x_j+y_j)/2+i(x_j-y_j)/2,\qquad x_j,y_j\in\{-1,1\}.
\]
Write \(R_{x,y}(k)=\sum_jx_jy_{j+k}\) and
\(H_{x,y}=R_{x,y}-R_{y,x}\). Direct multiplication gives
\[
C_{G(x,y)}=(C_x+C_y)/2+iH_{x,y}/2.
\]
The four binary rows can therefore be ordered with sums \(0,0,0,2\).
Their combined real autocorrelation is 256 at zero and \(-4\) elsewhere.
For a suitable division into Gray pairs their skew correlations must cancel.
Both binary Gray rows inherit the fixed multiplier of their quaternary row.

## Every proper compression is in the stated domain

Suppose the common multiplier is \(h=31\) or \(h=63\). For
\(d\in\{4,8,16,32\}\), put
\[
z_j=\frac12\sum_{t=0}^{64/d-1}x_{j+td},\qquad M=32/d.
\]
Then \(z\) is integral, \(|z_j|\le M\), \(z_j=z_{-j}\), and its sum is
\(s=0\) or \(1\). Symmetry follows from \(h\equiv-1\pmod d\).

Each multiplier has just two fixed positions at length 64, namely 0 and 32;
all other orbits have size two. A sum-zero binary row has 32 negative signs,
so its two fixed signs agree. A sum-two row has 31 negative signs, so they
are opposite. In residue class zero the remaining orbits are pairs, while
residue class \(d/2\) contains only pairs. Counting their signs gives exactly
the necessary endpoint parities
\[
z_0\equiv M+s\pmod2,\qquad z_{d/2}\equiv M\pmod2.
\]
There is no corresponding condition on a quarter position.

The compression identity gives the combined periodic autocorrelations
\[
\sum_{r=1}^4 C_{z^{(r)}}(k)=
\begin{cases}65-64/d,&k=0,\\-64/d,&k\ne0.\end{cases}
\]
Indeed the unscaled compression collects all \(64/d\) original lags with
the same residue, and half-compression divides their sum by four. Each row's
squared norm is at most the combined zero-lag value, since the other squared
norms are nonnegative. This is the only individual correlation pruning used.

At length four, enumerate every \((a,b,c,b)\in[-8,8]^4\) with these conditions.
There are 27 sum-zero rows and 28 sum-one rows. Matching their full even
correlation vectors gives 72 labelled quadruples, or six after the sign and
permutation normalization described below. No external queue is imported.

## Exact doubling fibers

Let \(p\) be a symmetric parent of length \(d\), with child \(z\) of length
\(2d\) and bound \(b=64/(4d)\). Folding and symmetry force
\[
z_{d/2}=z_{3d/2}=p_{d/2}/2,\qquad z_d=p_0-z_0,
\]
and, for \(1\le j<d/2\),
\[
z_j=z_{2d-j},\qquad z_{d-j}=z_{d+j}=p_j-z_j.
\]
Thus every child is determined uniquely by \(z_0,\ldots,z_{d/2-1}\).
Conversely these equations construct a symmetric child folding to \(p\)
from every such choice. Its sum is automatically the parent's sum.

The first forced value must be integral and bounded. For each free position,
the exact interval
\[
\max(-b,p_j-b)\le z_j\le\min(b,p_j+b)
\]
is equivalent to bounding both entries of that folded pair. At position zero
also impose \(z_0\equiv b+s\pmod2\) and \(p_0-z_0\equiv b\pmod2\).
The remaining necessary test is the child's squared-norm bound.

These conditions are necessary and sufficient for the stated child domain.
In particular, parity is imposed on \(z_d\), not on \(z_{d/2}\). The historical
generator incorrectly imposed the latter condition and lost complete coverage.

`reference.py` chooses free coordinates throughout the whole box and checks
the constructed row. `match.cpp` uses the equivalent intersected intervals.
Independent box audits define complete symmetric rows first and then fold
them, without using these doubling equations to generate the oracle set.

## Matching and the quotient preserve coverage

At each stage the required combined correlation vector is known. Real
autocorrelation is even, so lags zero through half the child length specify
the entire vector. Match two row lists against the complementary sum of the
other two lists. Every equal complete key is retained. In the native matcher,
the table points into linked lists of **all** row pairs with that key; it
does not discard pairs merely because their correlations coincide.

Negating any of the three sum-zero rows and permuting those rows preserves
the real equations, bounds, endpoint conditions and folding. Canonicalization
chooses each row's smaller sign and sorts these three rows. It leaves the
sum-one row alone. Although this can change a Gray pairing, the final search
restores the three possible pairings and the relative skew signs.

Simultaneous decimation by an odd unit also preserves the real equations.
Every odd unit at a proper power-of-two length lifts to an odd unit at length
64, and all these multiplications commute with both 31 and 63. Hence unit
normalization at length 16 is legitimate: transform a hypothetical child
using a lift of the unit taking its parent to the retained representative.
The transformed child lies in an enumerated fiber. Unit normalization at
length 32 is legitimate by the same argument.

The corrected computation gives 140 sign/permutation representatives at
length 8 and 23,872 at length 16; there are 6,095 unit representatives at
length 16. Lifting those representatives gives 64,464 sign/permutation
representatives over this selected parent set, and **32,232** representatives
after full unit normalization at length 32. The 64,464 count is not a census
over all unquotiented length-16 parents. The final 32,232-list covers every
admissible length-32 quadruple up to the stated sign/permutation/unit actions.

## Every full binary fiber is generated

At length 32, \(z_j\in\{-1,0,1\}\). If \(z_j=\pm1\), set
\(x_j=x_{j+32}=z_j\). If \(z_j=0\), the two signs are opposite.
The endpoint conditions ensure \(z_{16}\ne0\), and \(z_0=0\) occurs only
for the distinguished row, giving one free antipodal sign.

For every \(1\le j<16\) with \(z_j=0\), choose \(x_j\) freely and set
\[
x_{32-j}=\begin{cases}
x_j,&h=31\text{ and }j\text{ odd},\\
-x_j,&h=63\text{ or }j\text{ even}.
\end{cases}
\]
Antipodality determines the remaining signs. These rules are exactly the
multiplier-orbit equations, so they give every full binary lift once.
`audit_full.py` checks every resulting row set against a signed-component
constraint solver on the 64 individual positions, with no reliance on these
special-case orbit formulas.

## Reduced final keys are sufficient

For any full lift,
\[
C_x(k)+C_x(k+32)=4C_z(k),\qquad
C_x(32)=4\sum_jz_j^2-64.
\]
At lag 16, evenness gives \(C_x(16)=2C_z(16)\). Therefore the compressed
equations settle lags 16 and 32 and reduce the other real conditions to
lags 1 through 15.

For \(h=63\), every binary row is reversible. Changing index from \(j\) to
\(-j\) proves that each cross-correlation is even, and hence every
\(H_{x,y}\) vanishes. Matching the 15 remaining real lags for any one division
into two pairs is sufficient. Signs and all other pairings are redundant.

For \(h=31\), every cross-correlation obeys \(R(31k)=R(k)\). For odd \(k\),
\(31k\equiv32-k\pmod{64}\); evenness and compression therefore settle the
odd real lags. Only real lags \(2,4,\ldots,14\) remain. The skew correlation
is odd; for even \(k\), \(31k\equiv-k\), so it vanishes there. At odd lags
it is unchanged by \(k\mapsto32-k\). Its eight values at
\(1,3,\ldots,15\) determine it completely.

For each choice of the zero-sum row paired with the distinguished row, match
seven real coordinates and eight skew coordinates. Divide by four, which is
exact: binary autocorrelations and skew differences are multiples of four.
Canonicalize the skew vector by its overall sign. A match means that the
two skew vectors agree up to sign; negating one row of the all-zero-sum pair
realizes the required sign without changing its real autocorrelations or sum.
The code's final convention checks \(H_{x,y}=H_{z,w}\), corresponding to
\(A=G(x,y)\), \(B=G(w,z)\).

At this final stage retaining one pair per identical complete key is safe:
no untested condition depends on which representative supplied that key.
Every reported match is nevertheless checked at all 63 nonzero real and
skew lags, and against its sums and fixed multiplier, before being returned.

The additional reversible checker uses the reviewer's generic negative-count
equations on multiplier orbits. It computes all 32 real lags and retains every
distinct row autocorrelation vector. This last deduplication is exact because
all skew vectors vanish for reversible rows. It then matches all 32 lags,
providing a separate full-family check for 63 with a different lift generator
and without the reduced-lag interface. It does not check multiplier 31.

## Remaining units and affine consequence

This step is conditional on both finite exclusions succeeding on the complete
cover. It never follows from an incomplete or interrupted search.

For a unit-modulus row fixed by 33, odd antipodal entries agree. Splitting
the half-period correlation into even and odd antipodal pairs gives
\[
C_X(32)=\sum_{\substack{0\le j<32\\j\text{ even}}}|X_j+X_{j+32}|^2\ge0.
\]
Thus two such rows cannot have combined correlation \(-2\). This is the
independent, unaffected elementary result from the earlier contribution.

Every nonidentity cyclic subgroup of the unit group modulo 64 contains an
involution. The three nonidentity involutions are 31, 33 and 63. Excluding
these excludes every nonidentity common fixed multiplier. Separate cyclic
shifts preserve each row's autocorrelation, so the assertion also holds
whenever separate shifts put the members into common fixed-multiplier form.

The affine group modulo 64 has order \(64\cdot32=2048\). Every cycle of an
affine permutation has power-of-two length. If such a permutation has no
fixed point, an invariant fourth-root row has both Gaussian sum coordinates
even, contradicting the normalized sum \(1+i\). A fixed point permits a
change of origin reducing the affine map to a fixed multiplier. If the only
remaining multiplier is the identity, the affine map itself is the identity.
This gives the trivial common affine stabilizer, fixing each member individually.
Alphabet conjugation, phase twists and pair interchange are outside this claim.
