# Eleven transition-closed `a=2` safe cores for BHR `{1,2,11}`

## Result

For `s=1,...,11`, let `(B_s,C_s)` be the safe-seed pair in the table.

| `s` | source counts | source cuts `(1,2,11)` | modes applied | safe seed `(2,B_s,C_s)` | safe cuts `(1,2,11)` |
|---:|---:|---:|---:|---:|---:|
| 1 | `(1,9,12)` | `(0,1,11)` | `1,2,11` | `(2,11,23)` | `(0,2,14)` |
| 2 | `(2,7,13)` | `(1,2,11)` | `2,11` | `(2,9,24)` | `(1,2,13)` |
| 3 | `(2,7,14)` | `(19,20,10)` | `2,11` | `(2,9,25)` | `(30,31,10)` |
| 4 | `(2,7,15)` | `(21,22,11)` | `2,11` | `(2,9,26)` | `(32,33,11)` |
| 5 | `(2,7,16)` | `(19,20,10)` | `2,11` | `(2,9,27)` | `(30,31,10)` |
| 6 | `(2,7,17)` | `(19,20,10)` | `2,11` | `(2,9,28)` | `(30,31,10)` |
| 7 | `(2,7,18)` | `(21,22,10)` | `2,11` | `(2,9,29)` | `(32,33,10)` |
| 8 | `(2,7,19)` | `(20,21,10)` | `2,11` | `(2,9,30)` | `(31,32,10)` |
| 9 | `(2,11,9)` | `(0,1,10)` | `2,11` | `(2,13,20)` | `(0,1,12)` |
| 10 | `(1,11,10)` | `(21,1,11)` | `1,2,11` | `(2,13,21)` | `(34,1,13)` |
| 11 | `(2,9,11)` | `(19,20,10)` | `2,11` | `(2,11,22)` | `(30,31,10)` |

Every seed in the last two columns is simultaneously 1-, 2-, and
11-growable.  Consequently, for all `p,q,r>=0`, the multiset

\[
  \{1^{2+p},2^{B_s+2q},11^{C_s+11r}\}
\]

has a Hamiltonian-path realization.  The `C_s` are the consecutive integers
20 through 30, one in every residue class modulo 11, and `max_s B_s=13`.
Thus a uniform corollary is

\[
  a\geq2,\qquad b\geq13\text{ odd},\qquad c\geq20.
\]

## What is new and what is not

The earlier complete cap-orthant theorem already implies these existence
instances, in fact with stronger residue-dependent boundary values.  This
result therefore claims no new residual-coverage gain and is not presented as
a new existence frontier.

The structural refinement is a lower, uniform transition-closed core.  The
previous tri-modal certificate used safe seeds with `a=3` in nine of these
eleven residue classes.  Here, applying only modes 2 and 11 to the nine
available `a=2` cap witnesses preserves the transported mode-1 cut as well.
The resulting order-36--42 endpoints are already tri-modal safe at `a=2`.
Applying mode 1 once to each of those nine endpoints gives exactly, path and
cuts, the corresponding stored `a=3` seed.  The two remaining `a=2` endpoints
(`s=1,10`) are rederived from all six 1/2/11 orders and exactly match their
stored safe seeds.  Hence all eleven old safe cores now have checked `a=2`
predecessors or endpoints in one pinned certificate.

## Pinned finite derivation

All eleven source paths are copied from the Chand--Ollis certificate whose
SHA-256 is
`e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c`.
Every source realization and every displayed 1/2/11 growth incidence is
recomputed directly.

For the nine `a=2` sources, the two orders `(2,11)` and `(11,2)` are checked
while all three cuts are transported and reverified at each intermediate
state.  For `s=1,10`, all six permutations of `(1,2,11)` are checked.  All
endpoints agree within each row.  This gives 72 low-order derivation steps:
`9*2*2 + 2*6*3`.  No cross-mode preservation theorem is used before the safe
endpoint and no solver is involved.

The pinned trimodal certificate has SHA-256
`532470ffe31ff3e5acb4da51a78c15f172d2d00db6816dd43d5dc44a243bc059`.
External provenance replay verifies the two exact endpoint matches and the
nine exact mode-1 successor links described above.

The new compact certificate is
[`a2_mantle_certificate.json`](a2_mantle_certificate.json), SHA-256
`601a48ad69abef99c6279c8420492c16c9000120069affad74686388d4ccca4e`.
Its canonical eleven-seed digest is
`004f25da6b57aef196ce74d743b1b2680893fe47f4633eafb007c0bdd5e5989c`.

## Infinite transition closure

Every endpoint has maximum cyclic edge length `D=11` and order at least 36.
For all three pairs of distinct growth modes, the largest pair sum is 13, so

\[
  2D+\max\{1+2,1+11,2+11\}=35\leq36.
\]

The finite-mode safe-margin theorem in
[`TRIMODAL_SAFE_CORES.md`](TRIMODAL_SAFE_CORES.md) therefore preserves all
three transported cuts and makes every pair of refinements commute.  New
edges have length 1, 2, or 11, so `D` does not increase, while path order does.
Induction proves all `p,q,r>=0`.  The finite grids below test the implementation
but are not the proof of the universal quantifiers.

## Reproduction

With CPython 3.12.12 and no third-party package, run:

```bash
python3 independent_a2_mantle_check.py a2_mantle_certificate.json --grid 3
python3 -m unittest -v test_a2_mantle.py
```

The independent checker reports 11 residue classes, nine two-mode sources,
two rederived existing residues, 72 derivation steps, 1,375 family paths,
2,112 coordinate transitions, 2,112 commuting squares, and record SHA-256
`a52077728ea22b3e2ab4d8868b659a4174408745a284381d1cc403548ca8fc40`,
then `VERIFIED`.

For byte-level provenance checking, set `BHR_SOURCE_CERTIFICATE` to the pinned
external certificate and run:

```bash
python3 verify_a2_mantle.py a2_mantle_certificate.json --grid 3 \
  --source "$BHR_SOURCE_CERTIFICATE" --trimodal trimodal_certificate.json
python3 build_a2_mantle_certificate.py "$BHR_SOURCE_CERTIFICATE" \
  trimodal_certificate.json /tmp/a2-mantle.json
cmp /tmp/a2-mantle.json a2_mantle_certificate.json
```

The first command additionally reports `external_provenance_checked=true` and
`trimodal_successor_links_checked=11`; the builder reproduces identical bytes.

## Trust and novelty boundaries

The theorem trusts the explicit embedded paths, exact integer cyclic-length
and incidence calculations, the written finite-mode safe-margin proof,
ordinary induction, CPython, and either checker.  It does not trust a solver,
floating point, network data, the source certificate's coverage predicate, or
a finite grid as an infinite proof.  Provenance replay additionally trusts the
two pinned external files solely to establish the claimed source identities
and successor links.

Primary-source calibration used Chand--Ollis, *The Buratti--Horak--Rosa
Conjecture Holds for Some Underlying Sets of Size Three*
(<https://arxiv.org/abs/2202.07733>) and Ağırseven--Ollis, *Grid-based graphs,
linear realizations and the Buratti--Horak--Rosa conjecture*
(<https://arxiv.org/abs/2402.08736>).  The latter retains `a in {1,2}` for odd
third length as its possible exception.  Live exact-parameter searches on
2026-09-03 found no external statement of these eleven `a=2` safe cores.
Within Discovery Net, the existence ranges specialize the cap-orthant result;
the new graph value is explicitly limited to the nine lowered tri-modal cores,
the retained mode-1 cuts, and the pinned eleven-link certificate.  No priority
claim is made.
