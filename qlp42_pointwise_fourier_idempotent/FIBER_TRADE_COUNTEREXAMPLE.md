# A three-fiber counterexample to full support rigidity

## Disproved lemma

Consider two pairs of length-\(21\) words in the sixteen-state QLP local
alphabet. Suppose that, separately in each family, the pairs have the same
state multiplicities and the same primitive order-\(21\) Fourier coefficient
for every state indicator. Also fix the canonical exact \(S/H\) sums and the
global values of \(q\) and \(\sigma\).

The proposed lemma asserted that these data determine both quarter-support
words. The certificate in this directory disproves that assertion.

## Exact instance

Use coordinates \((r,c)\in C_7\times C_3\), listed by rows of constant
\(r\). State numbers follow the order obtained by taking
\(x,y\in(1,i,-1,-i)\) with \(x\) outermost and setting

\[
S=\frac{x-y}{1+i},
\qquad
H=\frac{x+y}{1+i},
\qquad
\epsilon=-iS\overline H.
\]

The two family-\(A\) colorings are identical except in rows \(0\) and \(1\):

| \(r\) | first coloring | second coloring |
|---:|:---|:---|
| \(0\) | \(14,14,14\) | \(5,5,5\) |
| \(1\) | \(5,5,5\) | \(14,14,14\) |
| \(2\) | \(0,0,5\) | \(0,0,5\) |
| \(3\) | \(5,5,5\) | \(5,5,5\) |
| \(4\) | \(7,7,8\) | \(7,7,8\) |
| \(5\) | \(14,15,15\) | \(14,15,15\) |
| \(6\) | \(15,15,15\) | \(15,15,15\) |

State \(14\) is a quarter state with

\[
(S,H,\epsilon)=(-i,-1,1),
\]

whereas state \(5\) is a nonquarter state with

\[
(S,H,\epsilon)=(0,1+i,0).
\]

The common family-\(A\) multiplicity vector is

\[
(2,0,0,0,0,7,0,2,1,0,0,0,0,0,4,5).
\]

It gives

\[
\sum S_A=1-i,
\qquad
\sum H_A=0,
\qquad
(q_A,\sigma_A)=(4,4).
\]

Family \(B\) is unchanged between the two paired colorings. Its multiplicity
vector is

\[
(0,1,4,0,0,8,0,0,0,0,0,0,0,0,0,8),
\]

and it gives

\[
\sum S_B=4-5i,
\qquad
\sum H_B=1,
\qquad
(q_B,\sigma_B)=(1,-1).
\]

These are precisely the canonical case-\(0\) exact sums. Globally,

\[
(q,\sigma)=(5,3).
\]

## Primitive Fourier proof

For each state \(a\), let \(d_a\) be the difference between its indicator in
the second and first family-\(A\) words. Every \(d_a\) is constant on each
three-cell fiber. If a character is nontrivial on both factors, write it as

\[
\chi_{u,v}(r,c)=\omega_7^{ur}\omega_3^{vc},
\qquad
u\ne0,
\qquad
v\ne0.
\]

Then

\[
\widehat d_a(u,v)
=\sum_{r\in C_7}d_a(r)\omega_7^{ur}
 \sum_{c\in C_3}\omega_3^{vc}
=0.
\]

Thus all sixteen primitive indicator blocks agree. The multiplicity vectors
also agree, so all exact sums, \(q\), and \(\sigma\) agree. Nevertheless the
quarter supports differ on the two exchanged fibers: their symmetric
difference has six positions.

## Consequence and scope

The full primitive indicator block does retain genuine positional
information, as the collision-rigidity theorem proves. This example shows
that the theorem is sharp for the sparse-minority QLP application: when one
family contains a three-cell minority fiber, a cross-category monochromatic
fiber trade can survive every invariant in the proposed package.

This certificate is not a solution of the QLP equations. In particular, no
claim is made that either paired coloring satisfies the imported coupled
autocorrelation conditions. It proves only that state multiplicities, exact
sums, \(q\), \(\sigma\), and the full primitive indicator block cannot by
themselves determine both support words or exclude the corresponding
aggregate branch point.

## Reproduction

Run:

    ./verify.sh

The production checker works in \(\mathbb Z[z]/(\Phi_{21}(z))\). The
independent checker uses only the \(C_7\times C_3\) fiber decomposition and
the exact state table. Neither uses floating point, randomness, a solver, or
enumeration of support or frontier cells.
