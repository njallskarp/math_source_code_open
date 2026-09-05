# Complete classification at the first-carry equality boundary

This note closes the equality case left open by
`GLOBAL_NONLINEAR_CLASS_BOUND.md`.  It concerns partitions of the minor
three-dimensional Hamming box into legal colour classes.  It does not claim
that every majority colouring of the associated four-dimensional graph is a
major-coordinate lift.

## Setting

Fix integers

\[
s\ge 3,\qquad m,n\ge s,\qquad 2\le p<s.
\]

Write

\[
m\equiv r\pmod s,\qquad n\equiv u\pmod s,
\qquad 1\le r,u<s,
\]

and assume \(ru<s\).  A part of

\[
B=[m]\times[n]\times[p]
\]

is **legal** when its induced Hamming subgraph has minimum degree at least
\(s-1\).  We work at the equality boundary

\[
rup=2s-2. \tag{1}
\]

Put \(Q=p\lfloor mn/s\rfloor\).  The sharp thin-coordinate theorem says
that \(Q\) is the largest possible number of coordinate-line legal parts.
Equation (1) gives

\[
mnp=sQ+2s-2,
\qquad
\left\lfloor\frac{mnp}{s}\right\rfloor=Q+1. \tag{2}
\]

## Classification theorem

The box \(B\) has a partition into the quotient-optimal \(Q+1\) legal parts
if and only if

\[
\boxed{
  (p=2\ \text{and}\ ru=s-1)
  \quad\text{or}\quad
  (p=s-1\ \text{and}\ ru=2).
} \tag{3}
\]

Every optimal partition has exactly one nonlinear part.  It is a
\(K_{s-1}\mathbin\square K_2\); every other part is a coordinate-line
\(K_s\).  In the first case of (3), the two-point factor of the prism uses
the thin coordinate.  In the second case, its \((s-1)\)-point factor uses
the thin coordinate.  For \(s=3\), the two descriptions coincide because
both prism factors have order two.

Thus the arithmetic conditions in (3) are not merely sufficient templates:
they are forced by the geometry of the unique nonlinear part.

## Necessity: layer divisibility forces the orientation

The global nonlinear-class theorem says that every nonlinear legal part has
at least \(2s-2\) vertices, with equality only for
\(K_{s-1}\mathbin\square K_2\).  Comparing part sizes with (2) therefore
shows that an optimal partition has exactly one such prism \(P\), and that
all its other parts are line \(K_s\)'s.

Because \(p<s\), no line \(K_s\) can vary in the \(p\)-coordinate.  Hence
all line parts lie inside individual \([m]\times[n]\) layers.  After the
intersection with \(P\) is removed, the number of remaining vertices in
each layer must consequently be divisible by \(s\).

The equality classification embeds \(P\) along two ambient coordinate
directions.  There are only three cases.

1. **The prism is fixed in the thin coordinate.**  Since \(p\ge2\), some
   layer is untouched.  That layer would require \(s\mid mn\), contrary to
   \(mn\equiv ru\not\equiv0\pmod s\).

2. **The two-point prism factor uses the thin coordinate.**  The prism meets
   two layers in \(s-1\) vertices each.  An untouched layer would give the
   same contradiction, so \(p=2\).  Divisibility in either touched layer is

   \[
   s\mid mn-(s-1),
   \]

   and \(0<ru<s\) forces \(ru=s-1\).

3. **The \((s-1)\)-point prism factor uses the thin coordinate.**  Its
   embedding requires \(p\ge s-1\).  Since \(p<s\), necessarily
   \(p=s-1\), so the prism meets every layer in two vertices.  Layer
   divisibility gives

   \[
   s\mid mn-2,
   \]

   whence \(ru=2\).

These cases prove the necessity of (3).

## Sufficiency I: \(p=2\) and \(ru=s-1\)

Write \(m=as+r\) and \(n=bs+u\), with \(a,b\ge1\).  First remove the
obvious line \(K_s\)'s outside a terminal

\[
(s+r)\times(s+u)\times2
\]

core: strip \((a-1)s\) whole first-coordinate symbols, then strip
\((b-1)s\) whole second-coordinate symbols over the remaining core
columns.  It remains to partition each copy of the rectangle
\([s+r]\times[s+u]\) after deleting the same \((s-1)\)-set.

Choose a row \(y_0\), a set \(X\) of \(s-1=ru\) columns, and split \(X\)
into \(u\) labelled blocks \(X_1,\ldots,X_u\), each of size \(r\).  Split
the rows into a set \(N\) of \(s\) rows containing \(y_0\), and \(u\)
additional rows \(y_1,\ldots,y_u\).

For each column \(x\notin X\), take the vertical line part

\[
\{x\}\times N.
\]

For \(x\in X_j\), take

\[
\{x\}\times\bigl((N\setminus\{y_0\})\cup\{y_j\}\bigr).
\]

Finally, in row \(y_j\), take the horizontal line part on all columns
except \(X_j\).  Its size is

\[
(s+r)-r=s.
\]

These line parts are disjoint and cover the core rectangle except for
\(X\times\{y_0\}\).  Apply the same construction in both thin layers and
join the two omitted copies into

\[
X\times\{y_0\}\times[2]
  \cong K_{s-1}\mathbin\square K_2.
\]

This gives one legal nonlinear part and \(Q\) line \(K_s\)'s, hence the
optimal \(Q+1\) parts.

## Sufficiency II: \(p=s-1\) and \(ru=2\)

Again write \(m=as+r\) and \(n=bs+u\).  In every thin layer, first
partition the first \(m-r\) columns into horizontal line \(K_s\)'s.  Over
the remaining \(r\) columns, partition the first \(n-u\) rows into vertical
line \(K_s\)'s.  The only uncovered vertices form

\[
[r]\times[u]\times[s-1].
\]

Since \(ru=2\), this is a
\(K_2\mathbin\square K_{s-1}\).  Adding it as the unique nonlinear part
again produces exactly \(Q+1\) legal parts.

The two constructions prove sufficiency and complete the classification.

## Consequences and examples

- The previously isolated \(s=5\), \((r,u,p)=(2,2,2)\) construction is one
  member of the entire first family.
- At \(s=7\), the residue pattern \((r,u,p)=(2,3,2)\) is repaired by a
  \(K_6\mathbin\square K_2\) crossing the two layers.
- Also at \(s=7\), \((r,u,p)=(1,2,6)\) is repaired by the residual
  \(K_2\mathbin\square K_6\) spanning every thin layer.
- Equality-boundary patterns such as \(s=7\), \((r,u,p)=(2,2,3)\) satisfy
  \(rup=2s-2\) but admit no quotient-optimal partition: every possible
  prism orientation leaves a layer whose remainder is nonzero modulo
  \(s\).

For the associated four-dimensional near-triangle graphs, either
construction can be lifted along the major coordinate exactly as in the
earlier results, yielding quotient-optimal majority colourings whenever the
same dominance normalization applies.

## Reproducibility and trust boundary

`verify_first_carry_equality_classification.py` directly constructs both
families, checks coverage, disjointness, part sizes, line/prism geometry,
minimum induced degrees, quotient counts, and the strict one-part line
deficit.  It also enumerates equality-boundary arithmetic patterns and all
six coordinate-role assignments of the forced prism, checking that a
layer-divisible orientation exists exactly in the two cases in (3).

Run with CPython 3.12 or later, standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_first_carry_equality_classification.py \
  | diff -u expected_first_carry_equality_classification_stdout.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_first_carry_equality_classification.py
shasum -a 256 -c SHA256SUMS
```

The default run checks 44,599 equality-boundary patterns through
\(s=1000\), classifying 9,046 as constructive and 35,553 as excluded.  It
directly validates 332 constructed boxes and 768,848 induced degrees.  The
canonical orientation and construction certificate hashes are respectively

```text
aa96281589be20d4effe1a10d99ad9e36f4a8b237909d5fd37850b6c8dc402e0
15e848d5197900791712d71ce8380fcabc33fd91447e10ca432929e3b989357d
```

The universal necessity proof rests on the committed global nonlinear-class
theorem, the sharp thin-coordinate line bound, and the layer-divisibility
argument above.  The program is finite exact corroboration and construction
verification; it is not a substitute for those universal arguments.  It
uses no solver, randomness, floating point, network input, external data, or
omitted certificate.

The originating open problem is Open Problem 2 of Bujtás, Dettlaff,
Furmańczyk, and Laskowska, *Majority C-coloring in Cartesian products*
(2026), <https://arxiv.org/abs/2608.27669>.  The exact classification (3)
was not found in the committed graph or targeted literature searches through
2026-09-05.  This is a search-relative novelty statement, not a priority
claim.
