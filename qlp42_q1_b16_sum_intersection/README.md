# Exact-sum intersection for the QLP-42 `q=1`, `b=16` fourth-order survivors

## Theorem

Continue the coupled norm-32 QLP-42 shell in the `q=1`, `b=16` branch.
The exact mod-7 compression and complete fourth-order Gaussian filter leave

```text
18 reflected B masks, 672 labeled A/B type pairs,
32 A-rotation orbits.
```

Intersect those fourth-order phase systems with all four exact Gaussian sum
equations in each canonical order-two compression case. Cases 0 through 4
retain all 32 orbits. In case 5, whose representative is

```text
(p,q,x,y) = (4,1,2,-1),
```

exactly four full A-rotation orbits, containing 84 labeled pairs, are
inconsistent. Thus case 5 leaves

```text
18 B masks, 588 labeled pairs, 28 A-rotation orbits.       (1)
```

The two affected B masks each retain other orbits, so this intersection does
not eliminate a B mask or the entire case-5 branch. It is a strict
case-specific reduction. Because every excluded type survives at least one
of cases 0 through 4, it does not lower the union-of-cases type count.

The complete per-case counts are in `case_table.tsv`; the four excluded
orbits are in `excluded_case5_orbits.tsv`.

## Exact finite reduction

Put `pi=1+i`. For a fixed fourth-order survivor, the preceding certificate
writes the 20 fourth-order residues as an affine binary map. Its first ten
coordinates involve only the `S` phase variables and its last ten involve
only the `H` variables. The exact sum equations likewise separate as

```text
sum(S_A) = (p+q) + (q-p)i,
sum(S_B) = (x+y-1) + (y-x)i,
sum(H_A) = 0,
sum(H_B) = 1.                                      (2)
```

For either component, let `r_0` be its ten-bit baseline residual. Every
active A cell has four choices `pi*u`, with `u` a Gaussian unit. Every active
reflected B pair has eight choices: the XOR of its two unit axes is fixed by
the third-order theorem, while the common axis and two signs are free. The
exceptional B center has its two oriented sign choices. These local groups
partition all phase variables of the component.

For `X` in `{A,B}`, the verifier computes the finite set

```text
D_X(t) = {delta in F_2^10 :
          an exact local phase assignment has sum t
          and fourth-order residue change delta}.
```

It uses the exhaustive recurrence

```text
D_(j+1)(t+v)  contains  delta xor d
```

for every state `(t,delta)` after `j` local groups and every local option
with Gaussian contribution `v` and residue change `d`. Therefore a component
has the prescribed A- and B-sums exactly when

```text
r_0 in D_A(target_A) xor D_B(target_B).             (3)
```

The `S` and `H` phase variables are disjoint, including the two independent
exceptional signs, so both component tests are simultaneously sufficient for
the full fourth-order-plus-sums relaxation.

Independent rotation of A preserves its Gaussian sums and periodic
autocorrelations. Each tested representative therefore certifies its entire
21-element rotation orbit.

## Reproduction and trust boundary

Run:

```bash
python3 verify_b16_sum_intersection.py
```

The standard-library verifier:

- pins the preceding fourth-order verifier to SHA-256
  `a5f616a19e241bcdced0962a2843631d1bb13a30de41cfbc05a2c0999e74bacf`;
- reconstructs all 32 fourth-order survivor orbits from the preceding mod-7
  and fourth-order certificates;
- performs 5,376 direct exact-autocorrelation checks, covering every local
  phase option in every orbit and confirming its recorded residue change;
- builds 128 exhaustive Gaussian-sum/residue reachability tables;
- verifies every displayed case count and each excluded orbit against the
  checked-in TSV files.

All arithmetic is exact in `Z[i]` and `F_2`. No floating point, random
search, SAT/SMT status, or heuristic pruning enters the certificate. The
new reachability layer has one implementation; its recurrence and all local
phase-to-residue mappings are exhaustively audited, but an independent
reimplementation would further reduce implementation risk.

This theorem applies only to the exact sums intersected with the
fourth-order congruence. It does not impose the full integral autocorrelation
equations and does not settle QLP-42. The strongest next step is a complete
fifth-order lift of the 28 case-5 survivors, while using the exact-sum dynamic
program as a side constraint.

Primary context: Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs
II*, <https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Kotsireas--Koutschan--Winterhof,
*On properties of Legendre pairs under compression*,
<https://doi.org/10.1145/3747199.3747549>. A targeted primary-source and
committed-graph search found no matching case-5 exact-sum/fourth-order
classification; apparent novelty is relative to that search, not a
historical-priority claim.
