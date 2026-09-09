# No nontrivial common fixed multiplier for a quaternary Legendre pair of length 64

**Computer-assisted result, externally unreviewed (2026-09-09).** There is no
quaternary Legendre pair \((A,B)\) of length 64 for which
\(A_{hj}=A_j\) and \(B_{hj}=B_j\) for a nonidentity unit
\(h\in(\mathbb Z/64\mathbb Z)^\times\). Indices are cyclic throughout.
The finite computations below exclude \(h=31,63\); an elementary argument
excludes \(h=33\) and reduces all other units to these three cases.

The result also applies after separate cyclic shifts of the two members.
It implies that a hypothetical pair has trivial common affine index stabilizer
when each member is fixed individually. It does **not** settle unrestricted
length-64 existence. Symmetries involving alphabet conjugation or phase factors
are outside the assertion.

## Literature and contribution

[Kotsireas–Winterhof](https://arxiv.org/abs/2212.10953) introduced these pairs;
[Kotsireas–Koutschan–Winterhof](https://arxiv.org/abs/2408.16318) and
[Jedwab–Pender](https://arxiv.org/abs/2408.08472) developed further searches and
constructions. The binary Gray representation and its amicability equation
are established tools; see also Pender's 2026 thesis, Chapter II,
[§2.19, equations (2.33)–(2.35)](https://theses.lib.sfu.ca/file/thesis/etd24298-thomasthomasscott-pender-pender-thesis-pdfa.pdf).
They are not claimed as new here.

[Lebedev, arXiv:2609.04589v1](https://arxiv.org/abs/2609.04589) gives seven new
even lengths and reports exhaustion of a particular reversible search queue
at 64, while explicitly withholding a proof that the queue covers every
reversible object. This contribution provides its own complete cover, generated
from integer constraints without importing that queue, and additionally excludes
the distinct multiplier-31 family. Targeted primary-source and Discovery Net
searches found no matching complete fixed-multiplier exclusion; priority remains
unestablished. The earlier
[half-period obstruction](https://github.com/njallskarp/math_source_code_open/tree/main/qlp_power_two_multiplier_obstruction)
is restated below to make the mathematical dependency explicit.

## Reproduce

Python 3.10 or later, a C++20 compiler and its standard library are sufficient.
No third-party Python packages, external datasets, search queues or floating-point
libraries are used. From this directory:

```sh
python3 run.py --workdir /tmp/qlp64-fixed-multiplier-check
```

The command regenerates all compressed parents, compiles `lift64.cpp`, runs the
independent row/key audit, exhausts both families, and compares every summary
with `expected.json`. Generated input and executables stay in the chosen work
directory. `--cxx` and `--cxxflags` can select another compiler or flags. On macOS,
the runner obtains the local SDK with `xcrun` and supplies its headers explicitly.

Expected final output:

```json
{"input_sha256": "26ed05773c9fc2d46bbabaac93ae61d8a17e14b718c2a21124b6305853d8957a", "multipliers": [31, 63], "parents": 1472, "verified": true, "witnesses": [0, 0]}
```

For the separate, slower comparison with unreduced compressed enumerations:

```sh
python3 compress.py --audit-reduction
```

It compares the actual candidate sets through compressed length 16 and reports
2,796 labelled / 72 reduced candidates at length 8 and 223,680 labelled / 4,740
reduced candidates at length 16. These are counts of necessary-condition tuples,
not counts of quaternary Legendre pairs or of their equivalence classes.

## Complete coverage argument

Write
\[
C_X(k)=\sum_{j=0}^{63}X_j\overline{X_{j+k}}.
\]
A quaternary Legendre pair has entries in \(\{1,i,-1,-i\}\) and
\(C_A(k)+C_B(k)=-2\) for every nonzero \(k\).
Summing over all shifts gives
\(\lvert\sum A_j\rvert^2+\lvert\sum B_j\rvert^2=2\).
For an even-length fourth-root sequence, the real and imaginary parts of its sum
have equal parity. Therefore one sum is zero and the other is one of
\(\pm1\pm i\). Exchange the members if necessary and rotate the nonzero sum
by a fourth root to normalize \(\sum A_j=0\), \(\sum B_j=1+i\).
These operations preserve a common fixed index multiplier.

### 1. Four binary rows

Use the bijection
\[
G(x,y)_j=\frac{x_j+y_j}{2}+i\frac{x_j-y_j}{2},
\qquad x_j,y_j\in\{-1,1\}.
\]
Put \(R_{x,y}(k)=\sum_jx_jy_{j+k}\) and
\(H_{x,y}(k)=R_{x,y}(k)-R_{y,x}(k)\). Direct multiplication gives
\[
C_{G(x,y)}(k)=\frac{C_x(k)+C_y(k)}2+\frac{iH_{x,y}(k)}2.
\]
The four binary rows have sums \(0,0,0,2\), after putting the special row last.
Their real autocorrelations must sum to 256 at zero and to \(-4\) elsewhere.
The two chosen Gray pairs must also have cancelling \(H\)-vectors.
Fixed multiplier invariance of a quaternary row is equivalent to invariance
of both of its binary Gray rows.

### 2. Necessary compressed constraints, with all roots generated

For \(d\in\{4,8,16,32\}\), define the half-compression of a binary row by
\[
z_j=\frac12\sum_{t=0}^{64/d-1}x_{j+td},\qquad 0\le j<d,
\qquad M=\frac{32}{d}.
\]
For both \(h=31\) and \(h=63\), multiplication reduces to reversal modulo
\(d\). Thus \(z_j=z_{-j}\), \(z_j\in[-M,M]\cap\mathbb Z\), and
\(\sum_jz_j=s\), where \(s=0\) for three rows and \(s=1\) for the last.

At length 64 both multipliers have exactly the fixed indices 0 and 32.
A zero-sum binary row has 32 negative entries, so these two fixed entries
are equal; a sum-2 row has 31 negative entries, so they are opposite.
In compressed residue class 0 all other multiplier orbits have size two;
in class \(d/2\) every orbit has size two. Consequently
\[
z_0\equiv M+s\pmod2,\qquad z_{d/2}\equiv M\pmod2.
\]
The compression identity for autocorrelations gives
\[
\sum_{r=1}^4C_{z^{(r)}}(k)=
\begin{cases}65-64/d,&k=0,\\-64/d,&k\ne0.\end{cases}
\]
Each row therefore has squared norm at most \(65-64/d\).

At \(d=4\), `root_rows` enumerates every \((a,b,c,b)\) in the box
\([-8,8]^4\), subject only to its sum, endpoint parities and this norm bound.
There are 27 eligible zero-sum rows and 28 eligible sum-1 rows. Exact matching
of the three independent correlation entries gives 72 labelled quadruples.
No pre-existing queue or spectral cutoff is an input.

### 3. Every doubling lift is present

Let \(p\) have length \(d\), and let its symmetric child \(z\) have length
\(2d\), with bound \(M=64/(4d)\). The equations
\(p_j=z_j+z_{j+d}\) force
\[
z_{d/2}=z_{3d/2}=p_{d/2}/2,\qquad z_d=p_0-z_0,
\]
and, for \(1\le j<d/2\),
\[
z_j=z_{2d-j},\qquad z_{d-j}=z_{d+j}=p_j-z_j.
\]
Thus choosing \(z_0,z_1,\ldots,z_{d/2-1}\) throughout \([-M,M]\)
enumerates every symmetric child. `lifts` implements exactly these equations,
checking bounds, endpoint parity, sum and the necessary norm bound. `match`
retains every quadruple whose complete correlation vector has the required sum.
Real autocorrelation is even in the lag, so checking lags 0 through \(d/2\)
is sufficient at each compressed length.

After each stage the three zero-sum rows are independently negated to their
lexicographically smaller sign and sorted. These transformations preserve the
real system and commute with compression and lifting. Therefore every full
solution has a representative above a retained parent at every stage. They need
not preserve a particular Gray pairing; the final step explicitly restores all
three pairings and both relative signs.

The resulting canonical tuple counts at lengths 4, 8, 16 and 32 are
6, 72, 4,740 and 11,776. At length 32, simultaneous index multiplication by all
odd units, followed by the same canonicalization, gives 1,472 representatives.
Every such unit lifts to an odd unit modulo 64 and commutes with both fixed
multipliers. Thus this last quotient also preserves coverage. The canonical
lists and the final input have deterministic SHA-256 values in `expected.json`.

### 4. Every full binary lift is present

Now \(z\) has length 32 and entries in \(\{-1,0,1\}\).
If \(z_j=\pm1\), then \(x_j=x_{j+32}=z_j\).
If \(z_j=0\), then \(x_{j+32}=-x_j\).
The entry \(z_{16}\) is nonzero. A zero at \(z_0\), present only in the special
row, supplies one free antipodal sign. For each \(1\le j<16\) with
\(z_j=z_{32-j}=0\), choose \(x_j\) freely and set
\[
x_{32-j}=\begin{cases}
x_j,&h=31\text{ and }j\text{ odd},\\
-x_j,&h=63\text{ or }j\text{ even}.
\end{cases}
\]
All remaining entries follow. This parametrization is both necessary and
sufficient for the prescribed compression and multiplier invariance.
`lift64.cpp` enumerates all choices. `audit.py` independently solves the signed
equality components on 64 positions and compares the entire resulting word set
for every one of the 966 distinct compressed rows, for each multiplier.

### 5. The exact final keys are sufficient

For a full binary row with half-compression \(z\),
\[
C_x(k)+C_x(k+32)=4C_z(k),\qquad
C_x(32)=4\sum_jz_j^2-64.
\]
At lag 16, evenness gives \(C_x(16)=2C_z(16)\).
For either multiplier, the compressed equations therefore settle the lag-32
condition and reduce the remaining real conditions to lags 1 through 15.

For \(h=63\), all cross-correlations of two invariant binary rows are even,
so \(H_{x,y}=0\). Matching the 15 real entries for any one division into two
pairs is necessary and sufficient.

For \(h=31\), multiplier invariance gives \(C_x(k)=C_x(31k)\).
When \(k\) is odd, \(31k\equiv32-k\), so the compressed equations already
settle the real conditions at odd lags. Only the seven even lags
\(2,4,\ldots,14\) remain. Likewise \(R_{x,y}(31k)=R_{x,y}(k)\);
\(H_{x,y}\) vanishes at even lags, is antisymmetric under negation, and is
unchanged under \(k\mapsto32-k\) at odd lags. Its eight entries at
\(1,3,\ldots,15\) determine it completely.

For each choice of the zero-sum row paired with the special row, the program
matches keys consisting of seven real pair-correlation entries and eight
\(H\)-entries. It divides each by four, which is exact for binary rows.
The imaginary vector is canonicalized up to its overall sign. A match is
therefore equivalent to \(H_{x,y}=\pm H_{z,w}\). Negating one zero-sum row
realizes the required sign without changing any real autocorrelation.
This restores every sign/permutation choice discarded in Step 3. Reversing the
order of a Gray pair also just changes that sign.

Hash tables compare the complete 15-entry integer key. Retaining one row pair
per equal key is safe here because there are no remaining constraints depending
on the individual pair. Any match is independently checked at all 63 nonzero
lags before being reported. Both full searches report zero matches:

| Fixed multiplier | Parents | Enumerated row pairs | Distinct stored keys, summed over tables | Witnesses |
| --- | ---: | ---: | ---: | ---: |
| 31 | 1,472 | 1,698,693,120 | 26,736,800 | 0 |
| 63 | 1,472 | 494,690,304 | 18,059,427 | 0 |

These are deterministic implementation counters, not counts of mathematical
isomorphism classes.

### 6. All nonidentity units and common affine maps

For a unit-modulus row fixed by \(h=33\), odd indices satisfy
\(X_{j+32}=X_j\). Splitting the half-period correlation into even and odd
antipodal pairs gives
\[
C_X(32)=\sum_{\substack{0\le j<32\\j\text{ even}}}
             |X_j+X_{j+32}|^2\ge0.
\]
Two such rows cannot have correlation sum \(-2\).

The unit group modulo 64 has order 32. Every nonidentity cyclic subgroup
therefore contains an element of order two. The three nonidentity solutions
of \(h^2\equiv1\pmod{64}\) are 31, 33 and 63. A pair fixed by any nonidentity
unit would be fixed by one of these three, all excluded above.

Finally consider a common affine map \(j\mapsto hj+b\) fixing both members.
The affine group has order \(64\cdot32=2048\), so all cycles of the map have
power-of-two lengths. If the map had no fixed point, its invariant quaternary
row sums would have both Gaussian coordinates even, contradicting the normalized
sum \(1+i\). A fixed point permits a common change of origin reducing the map
to \(j\mapsto hj\). The only remaining possibility is the identity. Separate
shifts of the two sequences also preserve all Legendre equations, giving the
stated extension whenever they put the sequences into common fixed-multiplier
form.

## Evidence and trust boundary

The proof above supplies coverage; the negative finite result depends on the
published Python and C++ programs and their execution. This is a computer-assisted
exclusion, not a proof checked by a formal proof assistant or an independently
reviewed theorem. Hashes establish reproducibility of generated data, not
mathematical completeness by themselves.

The packaged audit compares 343,104 full words per multiplier, grouped into 966
complete lift sets, against a separate signed-component implementation. It checks
720 deterministic pair-key samples per multiplier by direct array arithmetic.
At lengths 8 and 16 it compares the component method with exhaustive binary
multiplier-orbit enumeration: respectively 12 and 140 normalized full rows per
multiplier. The optional reduction audit compares entire labelled/reduced
compressed sets through length 16. Local sanitizer runs cover representative
final searches; the full optimized searches are repeated by `run.py`.

Python integers are unbounded. C++ sequence words are unsigned 64-bit values;
rotations use `std::rotr`. Correlations lie between \(-64\) and 64, pair sums
and skew-correlations between \(-128\) and 128. The scaled key coordinates lie
between \(-32\) and 32; real complements lie between \(-33\) and 31, within
`int8_t`. Accumulations use `int`, counters use `uint64_t`, and hash overflow is
intentional unsigned modular arithmetic. Hash collisions cannot remove a match
because complete keys are compared. No numerical tolerance, heuristic stopping
rule, external queue or unrecorded search parameter affects acceptance.

The small expected summaries are published; intermediate candidate lists,
binaries and verbose logs are generated locally and are not repository inputs.
