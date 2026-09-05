# A cross-boundary repair of the thin `(2,2,2)` residue

The whole residue box `[2]^3` has induced degree only three, so the one-box
criterion at threshold `s=5` fails.  Nevertheless, mixing residue cells with
cells from an adjacent exact block produces one nonlinear part attaining the
height-1965 residue-box lower bound `2s-2=8` and repairs the unique modular
carry.

## The 19-part core

Work in

\[
B=[7]\times[7]\times[2]
\]

with coordinates \((x,y,z)\), where \(x,y\in\{0,\ldots,6\}\) and
\(z\in\{0,1\}\).  Define the nonlinear part

\[
D=\{0,1,2,3\}\times\{0\}\times\{0,1\}.
\tag{1}
\]

It induces \(K_4\square K_2\), so every vertex of \(D\) has degree
\(3+1=4\).

For each \(x\in[7]\), put

\[
e_x=
\begin{cases}
1,&x\in\{0,1\},\\
2,&x\in\{2,3\},\\
0,&x\in\{4,5,6\}.
\end{cases}
\]

For every layer \(z\in[2]\), take the seven column parts

\[
C_{x,z}=\{(x,y,z):y\in\{3,4,5,6,e_x\}\},
\qquad x\in[7],
\tag{2}
\]

and the two row parts

\[
\begin{aligned}
R_{1,z}&=\{(x,1,z):x\in\{2,3,4,5,6\}\},\\
R_{2,z}&=\{(x,2,z):x\in\{0,1,4,5,6\}\}.
\end{aligned}
\tag{3}
\]

Every part in (2)--(3) is a coordinate-line \(K_5\).  These eighteen line
parts and \(D\) are disjoint and cover \(B\): rows 3--6 occur entirely in
the column parts; the three cells of row 0 outside \(D\) use columns 4--6;
rows 1 and 2 split respectively as \(\{0,1\}\cup\{2,3,4,5,6\}\) and
\(\{2,3\}\cup\{0,1,4,5,6\}\).  Hence they give a partition into

\[
19=\left\lfloor\frac{7\cdot7\cdot2}{5}\right\rfloor
\]

parts of induced minimum degree at least four.

The sharp thin-coordinate theorem gives an exact line-only maximum of

\[
2\left\lfloor\frac{7\cdot7}{5}\right\rfloor=18.
\]

Thus one cross-boundary \(K_4\square K_2\) repairs precisely the missing
part.  This is the first top-carry case not covered by whole-tail absorption:
the standard residual `[2]^3` is itself illegal.

## Uniform box family

**Theorem 1.**  For all integers \(a,b\ge1\), the box

\[
B_{a,b}=[5a+2]\times[5b+2]\times[2]
\]

partitions into

\[
Q(a,b)=10ab+4a+4b+1
=\left\lfloor\frac{2(5a+2)(5b+2)}5\right\rfloor
\tag{4}
\]

parts, each inducing minimum degree at least four.  Every coordinate-line
partition has at most \(Q(a,b)-1\) parts.

### Proof

Strip \(a-1\) exact 5-blocks in the first coordinate, on every active
first-coordinate line.  This leaves a box of first side seven.  Within it,
strip \(b-1\) exact 5-blocks in the second coordinate, leaving a translated
copy of \([7]\times[7]\times[2]\).  Partition that core by (1)--(3).

The number of parts is

\[
2(a-1)(5b+2)+14(b-1)+19
=10ab+4a+4b+1,
\]

which is (4).  The residues of the first two sides modulo five are both two,
so their product has residue four.  The sharp thin theorem therefore gives

\[
L_5(5a+2,5b+2,2)
=2\left\lfloor\frac{(5a+2)(5b+2)}5\right\rfloor
=10ab+4a+4b=Q(a,b)-1.
\]

This proves both assertions uniformly, without a parameter search.

## Exact four-dimensional Hamming family

For \(a\ge b\ge2\), define

\[
\begin{aligned}
n_1&=5(a+b)-4,\\
n_2&=5a+2,\\
n_3&=5b+2,\\
n_4&=2.
\end{aligned}
\tag{5}
\]

The orders are nonincreasing because
\(n_1-n_2=5b-6\ge4\).  If \(N_i=n_i-1\), then

\[
\sum_iN_i=10a+10b-2,
\qquad
h=5a+5b-1,
\qquad
h-N_1+1=5.
\tag{6}
\]

Lift every part of Theorem 1 through the complete first coordinate.  Its
vertices have at least

\[
N_1+4=h
\]

same-coloured neighbours.  The near-triangle class-size bound supplies the
matching quotient upper bound.  Consequently:

**Theorem 2.**  For every \(a\ge b\ge2\),

\[
\boxed{
\overline\chi_{\ge}
\left(
K_{5(a+b)-4}\square K_{5a+2}\square K_{5b+2}\square K_2
\right)
=10ab+4a+4b+1.
}
\tag{7}
\]

Every coordinate-line lift has at most \(10ab+4a+4b\) colours.  The first
member is

\[
\overline\chi_{\ge}(K_{16}\square K_{12}\square K_{12}\square K_2)=57,
\]

versus line-lift ceiling 56.

## Scope and trust boundary

This construction refines the first-carry classification: it proves that the
whole-tail degree condition is not necessary for arbitrary quotient-sized
partitions.  It also answers the boundary left explicit by the multi-box
barrier, which obstructs pure residual completion but not mixing with stripped
blocks.

The primary problem source is Bujtás, Dettlaff, Furmańczyk, and Laskowska,
*Majority C-coloring in Cartesian products* (2026),
<https://arxiv.org/abs/2608.27669>, whose Open Problem 2 asks for imbalanced
three- and four-dimensional Hamming graphs.  The paper does not state
(1)--(7).  Targeted literature and committed-graph searches through
2026-09-05 found no matching `(2,2,2)` cross-boundary construction.  Novelty
is search-relative, not a priority claim.

The accompanying standard-library CPython checker constructs every part,
checks cell ownership and Hamming adjacency directly, audits the formulas and
Hamming thresholds, and rejects certificate mutations.  A separately written
Ruby owner-map audit reconstructs the 98-cell base certificate directly from
the coordinate predicates and checks the two counting identities on 250,000
parameter pairs.  Its scope is deliberately narrower than the Python checker:
it does not check the Hamming threshold or upper-bound prerequisites.  These
finite checks corroborate the explicit construction; the universal theorems
follow from the displayed stripping and lifting arguments together with the
cited sharp thin and near-triangle bounds.
