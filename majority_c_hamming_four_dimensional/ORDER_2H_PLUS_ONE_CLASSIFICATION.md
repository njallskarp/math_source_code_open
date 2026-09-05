# Classification of Hamming cores one vertex past equality

The global nonlinear-class bound and the three-coordinate dimension gap leave
one natural small-order case: classify the nonlinear Hamming $h$-cores on
exactly $2h+1$ vertices.  There are only two uniform shapes and one sporadic
shape.

## Theorem

Let

\[
H=K_{n_1}\mathbin\square\cdots\mathbin\square K_{n_d},
\qquad h\ge2,
\]

and let $C\subseteq V(H)$ have

\[
|C|=2h+1,\qquad \delta(H[C])\ge h.
\]

If $C$ is not contained in a coordinate line, then, after permuting
coordinates and symbols, exactly one of the following holds.

1. **Nested parallel lines.**  For sets $Z\subset Y$ with
   $|Y|=h+1$ and $|Z|=h$,

   \[
   C=(\{x_0\}\times Y)\mathbin\cup(\{x_1\}\times Z).
   \tag{P}
   \]

2. **Perpendicular lines.**  For $|X|=|Y|=h+1$, with
   $x_0\in X$ and $y_0\in Y$,

   \[
   C=(\{x_0\}\times Y)\mathbin\cup(X\times\{y_0\}).
   \tag{X}
   \]

3. **Sporadic grid.**  Here $h=4$ and

   \[
   C=X\times Y,\qquad |X|=|Y|=3.
   \tag{G}
   \]

Conversely, every set in (P), (X), or (G) has the stated order and minimum
degree.  If the line case is included, the list is completed by an arbitrary
$(2h+1)$-point coordinate line.

The three nonlinear forms are distinguished intrinsically.  Form (P) has two
parallel maximal lines of sizes $h+1,h$; form (X) has two perpendicular
maximal lines of size $h+1$; and (G) is $4$-regular with six maximal
three-point lines.

## Bipartite translation

By the three-coordinate gap theorem, every such $C$ is contained in a
coordinate two-flat.  Regard its selected cells as the edges of a bipartite
graph $B$, whose bipartition consists of the used row and column symbols.
Two cells are adjacent in the Hamming graph exactly when the corresponding
edges of $B$ share an endpoint.  Thus a selected cell $xy$ has induced
degree

\[
d_B(x)+d_B(y)-2,
\]

and the core condition is the endpoint-degree inequality

\[
d_B(x)+d_B(y)\ge h+2\qquad(xy\in E(B)). \tag{1}

This translation is only notation; the proof below is given directly in
coordinate lines.

## Proof

Every connected component of $H[C]$ contains at least $h+1$ vertices.
Since $2(h+1)>2h+1$, the induced graph is connected.

Let $M$ be the largest number of selected cells on a coordinate line $L$.
If $M=2h+1$, then $C=L$, the excluded line case.  Suppose first that
$M\ge h+1$ and $C\ne L$.  Put $O=C\setminus L$.  A vertex outside $L$
has at most one neighbour on $L$, so its degree is at most

\[
1+(|O|-1)=|C|-M.
\]

The degree condition therefore gives $M\le h+1$.  Hence

\[
M=h+1,\qquad |O|=h. \tag{2}

Equality in the same degree count forces every vertex of $O$ to be adjacent
to all other vertices of $O$ and to one vertex of $L$.  A clique in a
Hamming graph lies on a coordinate line, so $O$ lies on a line $L'$.

The lines $L,L'$ either vary in the same coordinate or in different
coordinates.  In the first case, every vertex of $O$ must be aligned with a
distinct vertex of $L$; its $h$ symbols form a subset of the $h+1$
symbols on $L$.  This is (P).  In the second case, all vertices of $O$
meet the same selected intersection vertex of $L$, giving (X).

It remains to assume

\[
M\le h. \tag{3}

At a vertex $v$, let $a\ge b\ge1$ be its positive row and column
directional degrees.  Both are positive: otherwise degree at least $h$
would put at least $h+1$ selected vertices on one line, contrary to (3).
Also

\[
a+b\ge h,\qquad a,b\le h-1. \tag{4}

Each of the $a$ first-shell neighbours in one direction already has $a$
neighbours among $v$ and that line, so it needs at least $h-a$ neighbours
in the second shell.  Similarly the other direction contributes
$b(h-b)$ required incidences.  A second-shell cell is adjacent to at most
two first-shell cells.  Therefore

\[
2h+1\ge1+a+b+\frac{a(h-a)+b(h-b)}2. \tag{5}

Write $a+b=h+t$.  For fixed $t$, the quadratic penalty in (5) is minimized
at $a=h-1,b=t+1$, and (5) then requires

\[
t(h-t)\le2. \tag{6}

Consequently $t=0$, except that $h=3,t=1$ is possible.  When $t=0$,
(5) reduces to $ab\le h$ with $a+b=h$.  The complete list is

\[
\begin{array}{c|c}
h & (a,b)\\ \hline
2 &(1,1)\\
3 &(2,1),(2,2)\\
4 &(3,1),(2,2)\\
h\ge5 &(h-1,1).
\end{array} \tag{7}

For $h\ge5$, every vertex has profile $(h-1,1)$.  Its $h-1$ neighbours
in the large direction form, together with it, a unique selected $h$-point
line.  Every vertex on that line has the same unique large line.  These lines
partition $C$, forcing $h\mid(2h+1)$, impossible.

For $h=4$, the same partition argument applies unless some vertex has
profile $(2,2)$.  In that case (5) is an equality.  Its four first-shell
vertices require eight second-shell incidences, and the four remaining
vertices can supply at most two each.  All four rectangle completions must
therefore occur, giving exactly the $3$-by-$3$ grid (G).

For $h=3$, a vertex of profile $(2,2)$ again makes (5) an equality.  The
two remaining vertices must be rectangle completions forming a perfect
matching between the two pairs of first-shell vertices.  The completions are
not adjacent to each other and each has degree two, a contradiction.  Thus
every profile is $(2,1)$, and the unique three-point lines partition seven
vertices, also impossible.

Finally, for $h=2$, (7) makes the connected five-vertex core an induced
five-cycle.  At each cycle vertex the two incident cycle edges must change
different coordinates; otherwise its two neighbours lie on one coordinate
line and form a chord.  Row and column labels would therefore alternate
around an odd cycle, impossible.

This excludes (3) except for (G), and completes the classification.

## First-carry consequence

For majority-colouring applications put $h=s-1$.  Every nonlinear legal
class of size $2s-1$ is therefore one of two unions of coordinate lines:
two nested parallel lines of sizes $s,s-1$, or two perpendicular $s$-point
lines sharing one cell; when $s=5$, a $3$-by-$3$ grid is the sole extra
shape.  This turns the next residue-boundary question into three explicit
orientation tests.

This also corrects the phrase `order-2s+1` in the application paragraph of
the height-2765 graph contribution: the substitution $h=s-1$ gives
$2h+1=2s-1$.  The public source for that theorem already states $2s-1$.

## Reproducibility and trust boundary

`verify_order_2h_plus_one_classification.py` checks the endpoint-degree
identity, enumerates every candidate subset in 21 two-flat parameter jobs,
classifies every qualifying core, audits (5)--(7) through $h=300$, and
constructs every normal form through $h=100$.  Run with CPython 3.12 or
later, standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_order_2h_plus_one_classification.py \
  | diff -u expected_order_2h_plus_one_classification_stdout.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_order_2h_plus_one_classification.py
shasum -a 256 -c SHA256SUMS
```

Universal validity rests on the written dimension-gap dependency and the
line, shell-incidence, divisibility, and small-case arguments above.  The
finite computation corroborates the normal forms; it is not a proof of the
unbounded theorem.  No independent implementation or independent review is
claimed.  The checker uses no solver, floating point, randomness, network
input, external data, or omitted certificate.

The originating majority-colouring problem is Open Problem 2 of Bujtás,
Dettlaff, Furmańczyk, and Laskowska, *Majority C-coloring in Cartesian
products* (2026), <https://arxiv.org/abs/2608.27669>.  Targeted arXiv,
Crossref, OpenAlex, and graph searches found adjacent work on maximum degree
in large induced Hamming subgraphs, but no matching minimum-order
classification.  Novelty is search-relative, not a priority claim.
