# Primitive Fourier collision rigidity for the QLP-42 local alphabet

## Binary theorem

Let \(p\ne q\) be primes, let \(G=C_p\times C_q\), and let
\(f,g:G\to\{0,1\}\). Suppose that \(f\) and \(g\) have equal weight and

\[
\widehat f(\chi)=\widehat g(\chi)
\]

for every character \(\chi\) that is nontrivial on both factors.
Equivalently, after identifying \(G\cong C_{pq}\), the two words have equal
Fourier values at every primitive order-\(pq\) character.

Then \(d=g-f\) is constant on all \(C_q\)-fibers or constant on all
\(C_p\)-fibers. More explicitly, at least one of the following holds:

1. \(d(r,c)=u(r)\) for a balanced function
   \(u:C_p\to\{-1,0,1\}\);
2. \(d(r,c)=v(c)\) for a balanced function
   \(v:C_q\to\{-1,0,1\}\).

Their intersection is the trivial collision \(d=0\), so a nonzero collision
has exactly one of these forms. Thus two equal-weight
binary words with the same primitive Fourier block can differ only by swaps
of complete subgroup fibers. There is no genuinely mixed row-column trade.

## Multicolor strengthening

Let \(\mathcal A\) be any finite alphabet, and let
\(F,G:C_p\times C_q\to\mathcal A\) be two colorings. Suppose that every
color has the same multiplicity in \(F\) and \(G\), and that the primitive
Fourier coefficients of every color indicator agree. Then exactly one of
the following occurs:

1. \(F=G\);
2. every changed \(C_q\)-fiber is monochromatic in both colorings, and
   \(G\) is obtained by relabeling complete \(C_q\)-fibers;
3. every changed \(C_p\)-fiber is monochromatic in both colorings, and
   \(G\) is obtained by relabeling complete \(C_p\)-fibers.

In particular, nontrivial row and column recolorings cannot occur together.

For \(C_{21}\cong C_7\times C_3\), apply this to the sixteen colors
\((x_j,y_j)\in\mu_4^2\) in the coupled QLP transform. If two local-state
words have the same state counts and the same primitive order-\(21\)
Fourier value for every state indicator, then the entire coloring changes
only by complete three-cell fiber swaps or only by complete seven-cell
fiber swaps. The primitive indicator block therefore retains positional
information absent from the aggregate local-character image.

## Sparse-minority QLP corollary

Across both QLP families, the \(q=5\) branch has exactly five quarter cells,
whereas the \(q=37\) branch has exactly five nonquarter cells. Thus each
family has at most five cells in the branch's minority category.

A nontrivial seven-cell fiber recoloring that changes quarter support would
make a complete seven-cell fiber belong to the minority category in either
the old or the new coloring. This is impossible. Hence a seven-cell
primitive collision can relabel local states only within the quarter class
or within the nonquarter class, and it leaves the quarter-support word
unchanged.

Likewise, if one family contains at most two minority cells, a three-cell
fiber recoloring cannot cross the quarter/nonquarter boundary. For that
family, its state multiplicities and primitive state-indicator block
determine its quarter support uniquely. Since the two family minority counts
sum to five, at least one of the two families always satisfies this
support-rigidity condition.

## Sharpness: the second family need not be rigid

The fixed-invariant strengthening suggested after the theorem is false.
Even after fixing the sixteen state multiplicities separately in each
family, both exact \(S/H\) sums, the global \(q\) and \(\sigma\), and every
primitive order-\(21\) Fourier coefficient of every state indicator, the
quarter support of the other family need not be determined.

The file `fiber_trade_counterexample.json` gives an exact case-\(0\)
counterexample at

\[
(q,\sigma)=(5,3).
\]

Family \(A\) has \((q_A,\sigma_A)=(4,4)\). One three-cell fiber is
monochromatic in quarter state \(14\), while a second is monochromatic in
nonquarter state \(5\). Exchanging the two fiber labels moves three quarter
positions. Family \(B\) is unchanged and has
\((q_B,\sigma_B)=(1,-1)\). The state counts, and therefore all aggregate
linear invariants, remain fixed. Each changed indicator difference is a
linear combination of complete three-cell fiber indicators, so all of its
primitive order-\(21\) Fourier coefficients vanish.

This is a counterexample to the proposed invariant package, not a QLP-42
witness. The paired words satisfy the local sixteen-state alphabet and the
canonical case-\(0\) exact sums, but the certificate does not assert the
remaining QLP autocorrelation equations. See
`FIBER_TRADE_COUNTEREXAMPLE.md` for the precise statement and proof.

## Fourier idempotent lift

For a coloring \(F:C_n\to\mathcal A\), let \(n_a(j)\) be the indicator of
color \(a\), and use the unnormalized Fourier transform

\[
N_a(k)=\sum_{j\in C_n}n_a(j)\zeta_n^{jk}.
\]

The one-hot pointwise identities are equivalent to

\[
\sum_{\ell\in C_n}N_a(\ell)N_b(k-\ell)
=n\delta_{a,b}N_a(k)
\]

for every \(a,b,k\), together with

\[
\sum_{a\in\mathcal A}N_a(k)=n\delta_{k,0}.
\]

The forward implication is the Fourier product-convolution identity.
Conversely, Fourier inversion turns these equations into
\(n_a(j)n_b(j)=\delta_{a,b}n_a(j)\) and
\(\sum_a n_a(j)=1\). Over characteristic zero, each \(n_a(j)\) is an
idempotent scalar and hence lies in \(\{0,1\}\); orthogonality and the sum
condition give exactly one color at each position. This is an exact
equivalence, not a relaxation through moments or autocorrelations.

## Proof of the binary theorem

Put \(d=g-f\in\{-1,0,1\}^{p\times q}\). Vanishing of every Fourier
coefficient on

\[
\mathbf 1_p^\perp\otimes\mathbf 1_q^\perp
\]

places \(d\) in the orthogonal complement

\[
(\mathbf 1_p^\perp\otimes\mathbf 1_q^\perp)^\perp
=\mathbb C^p\otimes\mathbf 1_q
+\mathbf 1_p\otimes\mathbb C^q.
\]

Hence

\[
d(r,c)=u(r)+v(c).
\]

Differences of two rows show that all \(u(r)-u(r')\) are integers; similarly
all differences of \(v\) are integers. After moving one constant between
\(u\) and \(v\), both may be taken integer-valued. Because every entry of
\(d\) lies in \(\{-1,0,1\}\),

\[
\operatorname{osc}(u)+\operatorname{osc}(v)\le 2.
\]

If both functions are nonconstant, each oscillation is \(1\). Normalize so
that \(u\in\{0,1\}\) and \(v\in\{-1,0\}\). Let \(a\) be the number of rows
where \(u=1\), and let \(b\) be the number of columns where \(v=0\). The
\(+1\) support has size \(ab\), whereas the \(-1\) support has size
\((p-a)(q-b)\). Equal weight gives

\[
ab=(p-a)(q-b),
\]

or

\[
qa+pb=pq.
\]

Reducing modulo \(p\) forces \(a\equiv0\pmod p\), impossible for
\(0<a<p\), because \(p\ne q\). Thus one of \(u,v\) is constant. Absorbing
that constant into the other proves the theorem. The converse is immediate:
a function of one factor has zero Fourier coefficient at every character
nontrivial on the other factor.

## Proof of the multicolor strengthening

Apply the binary theorem to every color-indicator difference \(d_a\).
Each nonzero \(d_a\) is row-type or column-type. Partition the nonzero
colors accordingly, and write the total difference vector at a cell as

\[
U(r)+V(c).
\]

Pointwise one-hotness gives

\[
\sum_a U_a(r)+\sum_a V_a(c)=0
\]

for every \(r,c\), so the two sums are opposite constants. Preservation of
each color count gives \(\sum_r U_a(r)=0\) for every row-type color and
\(\sum_c V_a(c)=0\) for every column-type color. Averaging the displayed
identity over either factor shows that both constants are zero. Thus
\(U(r)\) and \(V(c)\) each have coordinate sum zero. A nonzero integral
vector with coordinate sum zero has
\(\ell_1\)-norm at least \(2\). If some \(U(r)\ne0\) and some \(V(c)\ne0\),
their color supports are disjoint, so the difference of the two one-hot
state vectors at \((r,c)\) would have \(\ell_1\)-norm at least \(4\). But
the difference of two one-hot vectors has norm at most \(2\). Therefore
only one direction can change.

In that direction, the difference vector is constant along each fiber. A
nonzero constant difference of one-hot vectors forces the old fiber and the
new fiber to be monochromatic. Equal color multiplicities say exactly that
the multiset of monochromatic fiber labels is preserved.

## Exact certificate for \(C_{21}\)

The production derivation constructs the integer matrix for

\[
\mathbb Q[C_{21}]\longrightarrow\mathbb Q(\zeta_{21})
\]

by reducing \(1,z,\ldots,z^{20}\) modulo \(\Phi_{21}(z)\). Its rank is
\(12\), so the primitive kernel has dimension \(9\). The seven indicators
of residue fibers modulo \(7\) and three indicators of residue fibers modulo
\(3\) lie in this kernel and span a \(9\)-dimensional space. They therefore
equal the complete primitive kernel.

The independent checker reconstructs the evaluation matrix through a
separate recurrence for \(\Phi_{21}\), proves ranks over independent finite
fields, checks every fiber generator by exact integer multiplication, and
checks the mixed-balance equation for all interior size pairs. It also
reconstructs the sixteen QLP local states from \(\mu_4^2\), and exhaustively
checks the multicolor theorem on \(C_2\times C_3\) with three colors.

Run under CPython \(3.12\) or later:

    ./verify.sh

The expected compact output is in the file expected_output.txt.

## Scope and trust boundary

This is a positional representation-theoretic theorem. It uses neither
autocorrelations nor traces, moments, Gram matrices, positive
semidefiniteness, Gaussian residue layers, SAT searches, support orbits, nor
frontier-cell enumeration. It does not itself eliminate another QLP fiber
or prove existence or nonexistence of a QLP-42 pair. Instead it classifies
the exact collision modes left after retaining the full primitive
order-\(21\) state-indicator block.

The theorem is human-checkable for all distinct primes and every finite
alphabet. The code certifies the \(p=7,q=3\) instance and its link to the
sixteen-state transform. The computational trust boundary consists of
CPython, the operating system, and hardware; no third-party package,
floating point, randomness, solver, or timeout is used.

The sharpness counterexample is checked twice. The production derivation
reduces all indicator differences modulo \(\Phi_{21}\) over
\(\mathbb Z[z]\). The independent checker instead verifies the tensor-fiber
factorization directly on \(C_7\times C_3\), so it does not share the
cyclotomic reduction routine. Both use exact integer arithmetic.

## Translation obstruction to a fiber-norm detector

A proposed repair was to add the two compressed group-ring norms on
\(C_7\). The universal detector is false. For any two local states \(a,b\),
the compressed words

\[
(a,b,b,b,b,b,b)
\qquad\text{and}\qquad
(b,a,b,b,b,b,b)
\]

are cyclic translates. Their \(S\)- and \(H\)-norms therefore agree. If
\(a\) and \(b\) lie in opposite quarter classes, lifting each compressed
coordinate to a monochromatic three-cell fiber gives a cross-category
fiber exchange that moves six support positions while preserving all
primitive indicator coefficients.

This refutes a universal translation-invariant compressed-norm detector. It
does not provide a canonical-case QLP witness and does not rule out a more
specialized invariant that uses additional QLP structure. See
`FIBER_NORM_TRANSLATION_OBSTRUCTION.md`.
