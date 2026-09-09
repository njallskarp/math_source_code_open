# Exact reproduction of seven published quaternary Legendre pairs

The literal pairs in Nikita Lebedev, [arXiv:2609.04589v1, Theorem 1](https://arxiv.org/html/2609.04589v1#S2), satisfy every defining equation at lengths
\[
42,46,52,58,66,72,80.
\]
This is an independent verification of published witnesses, not a claim of new constructions or a reproduction of the author's searches. In particular, length 42 has a positive existence certificate and should no longer be treated as an open existence target.

For \(X\in\{1,i,-1,-i\}^n\), write
\[
C_X(k)=\sum_{j=0}^{n-1}X_j\overline{X_{j+k}},
\]
with indices modulo \(n\). Each pair here satisfies \(C_A(k)+C_B(k)=-2\) at all \(1\le k<n\), and has sums \(0\) and \(1+i\). The file `pairs.json` transcribes the paper's decimal words, with digits 0,1,2,3 representing \(1,i,-1,-i\). Its only inputs are these short literal certificates.

## Reproduction

Tested with CPython 3.12.12 on macOS; no packages are required. From the repository root:

```sh
python3 qlp_2026_seven_lengths_reproduction/verify.py
```

The exact output is `expected.json`: `status` is `PASS`, all seven pairs pass, and 42 deliberately malformed or mutated controls are rejected. The midpoint PSD pairs are respectively
\[
(4,82),(68,26),(16,90),(20,98),(4,130),(64,82),(32,130).
\]
The per-pair SHA-256 convention is ASCII `A + "\n" + B + "\n"`. For length 42 it is `b9d438020f96f35a8b4b55481262e681a33bf972e241331275f5348e9af42e5f`. Hashes identify inputs; they do not establish the mathematical equations.

## Two verification routes

`gaussian_check` computes all shifts directly, storing each Gaussian integer as a pair of unbounded Python integers. It checks the zero-shift norm and the normalization as well as the required nonzero shifts.

`difference_family_check` separately decodes each word into two negative-position sets of binary Gray rows. For \(A=(p+q)/2+i(p-q)/2\), the negative positions of \(p\) are digits 2 and 3; those of \(q\) are digits 1 and 2. Likewise decode \(B\) into \(r,s\). It verifies that every set is invariant under negation, the four sizes are \(n/2,n/2,n/2-1,n/2\), and the total number of ordered differences of each nonzero residue is \(n-2\).

Here is why this second check suffices. A binary row with negative set \(D\) has
\[
C_x(k)=n-4|D|+4|D\cap(D-k)|.
\]
The four size and difference identities therefore make the four binary autocorrelations sum to \(-4\). Reflection symmetry gives \(C_{x,y}(k)=C_{y,x}(k)\) by the substitution \(j\mapsto-j-k\), so the imaginary Gray cross terms vanish. The two quaternary autocorrelations consequently sum to \(-2\).

The checkers share input words but use different representations and identities. They were written for this reproduction without importing the author's code. This is not independent peer review of this verifier.

## Scope and provenance

No solver status, floating point, search completeness, queue coverage, or external database is trusted. The trust boundary is the displayed finite identities, literal input transcription, the supplied Python code, CPython integer/set semantics, and the operating system/hardware. The tests reject one single-symbol mutation, one truncation and one invalid symbol per pair per checker. No unrestricted nonexistence or search-exhaustion claim is made at lengths 64, 70 or 76.

Lebedev's seven witnesses are attributed to that paper, whose arXiv version is distributed under CC BY 4.0. The mathematical context and original even-length normalization come from Kotsireas–Winterhof, [Quaternary Legendre Pairs](https://arxiv.org/abs/2212.10953); the earlier finite frontier and general constructions are in [Kotsireas–Koutschan–Winterhof](https://arxiv.org/abs/2408.16318) and [Jedwab–Pender](https://arxiv.org/abs/2408.08472). This reproduction does not assert novelty for the induced Hadamard matrix orders.
