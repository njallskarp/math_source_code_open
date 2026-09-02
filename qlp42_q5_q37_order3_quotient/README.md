# Exact order-three quotient obstruction on the QLP-42 q=5/q=37 frontier

## Theorem

Let `(S_A,H_A,S_B,H_B)` be the coupled length-21 transform in the canonical
norm-32 QLP-42 shell.  For a length-21 Gaussian word `W`, define its factor-7
compression to `Z/3Z` by

```text
C_3(W)_r = sum_{j congruent to r (mod 3)} W_j,  r=0,1,2.
```

The compression identity sends the two exact length-21 target profiles to

```text
PAF(C_3(S_A)) + PAF(C_3(S_B)) = (43, 0, 0),
PAF(C_3(H_A)) + PAF(C_3(H_B)) = (29,-14,-14).       (1)
```

For each branch `q=5,37`, every one of the 18 oriented binary-shadow support
orbits, and every one of the six canonical exact-sum cases, there is a full
assignment from the 16-state local table satisfying simultaneously:

- the prescribed quarter-turn support;
- the exact energy type counts;
- all four exact Gaussian sums; and
- both exact compressed autocorrelation identities in (1).

Thus all **216** orbit/case cells survive the fully coupled exact order-three
quotient.  This proves a family-level obstruction to the proposed
cyclotomic shortcut: the factor-7/order-three quotient, even before reduction
modulo any Gaussian prime and even with the exact sums and pointwise `S/H`
coupling retained, has zero pruning power on the unresolved `q=5/q=37`
frontier.

This is not a QLP construction.  The certificate satisfies the quotient sums
of the length-21 autocorrelation equations, not the individual length-21
equations.

## Proof ingredients

For a local state, a quarter-turn contributes norm one to both `S` and `H`,
an opposite state contributes norm two only to `S`, and an equal state
contributes norm two only to `H`.  Consequently a branch with `q` quarter
states has exactly

```text
opposite states = (43-q)/2,
equal states    = (41-q)/2.
```

The C++ generator groups the seven positions in each residue class modulo
three only by these three local types.  It constructs the exact finite set of
attainable aggregate pairs `(sum S, sum H)` for each section and type count.
For a three-section word, its exact total sum and shift-zero energy determine
the real part of its shift-one autocorrelation; shift two is the conjugate.
The generator therefore joins the two families by the lossless five-integer
key

```text
(equal count, S energy, Im PAF_S(1), H energy, Im PAF_H(1)).
```

It emits one full 21-state word for each surviving cell.  The published TSV
is the theorem certificate.  The independent Python checker does not trust
the aggregate join: it reconstructs all 16 Gaussian states from the existing
coupled-transform definition, checks support and type counts, recomputes the
four exact sums, compresses the four words directly, and evaluates all three
autocorrelation coordinates from definitions.

## Reproduction

From this directory, with a C++20 compiler:

```bash
CXX=/opt/homebrew/bin/g++-16 ./verify_all.sh
```

The recorded run used Python 3.12.12 and GCC 16.2.0.  The constructive
enumeration takes roughly 2.5 minutes and about 270 MB on the recorded
Apple-arm64 host.  The definition-level certificate check is effectively
instantaneous.

Certificate SHA-256:

```text
edaf6d255ec1c2e76fe8e07288bea03c250711772aa2e0d2a82301db48ae3b70
```

## Trust boundary and scope

The positive theorem depends on the established coupled half-transform and
16-state bijection, the oriented 18+18 support manifest, the 216-row state
certificate, and the direct checker.  The C++ search order and frontier
packing are outside the certificate trust base because every emitted word is
rechecked from definitions.  Integer arithmetic only is used; there is no
floating point, SAT/SMT status, heuristic cutoff, randomization, timeout, or
cellwise residue assumption.

The result rules out the exact order-three quotient *as a pruning mechanism*;
it does not rule out cyclotomic methods.  The next falsifiable structural step
is a primitive-order-21 compatibility theorem coupling the order-three and
order-seven specializations, rather than another `(1+i)`-adic layer or a
cell-by-cell search.

## Literature and novelty calibration

Compression of complementary sequences is standard; see Djokovic--Kotsireas,
*Compression of Periodic Complementary Sequences and Applications*,
arXiv:1302.0571.  The QLP definition, decompression setting, and length-42
frontier are in Kotsireas--Winterhof, arXiv:2212.10953, and
Kotsireas--Koutschan--Winterhof, arXiv:2408.16318; see also Jedwab--Pender,
arXiv:2408.08472.  The theorem is presented only as a search-relative exact
specialization of those methods.  No claim of historical priority is made.
