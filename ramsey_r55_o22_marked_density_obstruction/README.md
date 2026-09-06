# A density cut excludes all sixteen marked H20–O22 gluings

This package proves a **conditional 43-vertex family exclusion**.
None of the sixteen 107-blue-edge O22 graphs published at height 3026
can be glued to the specified marked H20 with the prescribed proper
three-anchor profile.

For any such Ramsey gluing, the second marked vertex has

\[
t_R(v)\le91<92,
\]

where \(t_R(v)\) counts red edges inside its red neighborhood.
The selected published O22 choice has upper bound 90.
These upper bounds are not claimed sharp.

The hypotheses used are the fixed cores and root incidences,
red degree 20 at each marked H20 vertex, their red neighborhoods
covering O22, and absence of monochromatic \(K_5\)s.
The hard profile requires \(t_R(v)=92\), giving a contradiction.
All 440 cross-pairs remain variable; no labeled \(8/10/4\) partition
is fixed.

This does **not** exclude H20 with every opposite graph, all 107-blue-edge
cores, an entire degree profile, or a gluing with different
coverage/degrees/densities. The working bounds
\(43\le R(5,5)\le46\) are unchanged.

## The compact obstruction

The complete argument is in [PROOF.md](PROOF.md).

The marked degree equations force opposite-neighborhood sizes 12 and
14, with intersection four. The common base graph has only six
red-\(K_4\)-free 14-sets. The sole high-density one has a red \(K_4\),
\(\{8,11,16,18\}\), in its complement. Coverage forces that clique
inside the other marked vertex's red neighborhood, which is impossible.

The five remaining base sets have at most 45 red edges; the allowed
edit adds at most one. Four relevant H20 vertices have triangle-free
attachments of size at most eight. The exact marked-density identity
therefore gives

\[
t_R(v)\le13+46+4\cdot8=91.
\]

The selected O22 graph has bound 90. Only candidates \((9,17)\) and
\((11,14)\) use the upper bound 91 in the recorded table.

This is a load-bearing composition of local graph and marked
degree/profile interfaces, not a full gluing search or a necessary
condition without a family conclusion.

## Reproduction and trust

CPython 3.12.12, standard library only. From this directory:

~~~sh
set -o pipefail
python3 -B verify.py --derive | cmp - CERTIFICATE.json
python3 -B verify.py | cmp - EXPECTED_OUTPUT.txt
python3 -B direct_check.py | cmp - EXPECTED_DIRECT.json
python3 -B test_verify.py | cmp - EXPECTED_CONTROLS.txt
python3 -B -O verify.py | cmp - EXPECTED_OUTPUT.txt
python3 -B -O direct_check.py | cmp - EXPECTED_DIRECT.json
python3 -B -O test_verify.py | cmp - EXPECTED_CONTROLS.txt
shasum -a 256 -c SHA256SUMS
~~~

Expected marker:

~~~text
VERIFIED: 16 fixed O22 choices excluded; marked density <= 91 < 92
~~~

[CERTIFICATE.json](CERTIFICATE.json) contains all six base domains,
the complementary clique, capacity witnesses, and every candidate/domain
density bound. Its SHA-256 is
4689c02b45553df1f3a845fbb9b2fc44e28d2784448c33cc82548ea649bb2b3b.

The primary checker uses literal subset enumeration and clique masks.
The separate checker imports no primary code: it uses incremental
clique-free recursion and bitset clique enumeration. All domain,
capacity, obstruction, candidate and bound records agree, not just
the totals. The complete domain/family table has SHA-256
6c9da9af5d7cac9700ca7d5702e9623a7f4fc2be1d168cf638656dcf5c513f0e.
Eight damaged certificates and four damaged inputs are rejected.

Both are author-written cross-validation, **not external peer review,
a second-language check or formalization**. The finite coverage,
unformalized density reduction, exact code, interpreter/hardware and
hashes for identity remain trusted. No solver, floating point, external
catalogue, network download, private input or omitted trace is needed.
No solver was used to obtain this result.

## Source provenance and overlap

- Height 2965, bafkreiezgfimstlpixhrdg6uqkhl45kpr2j7wbrc5hbq4jwnrath7rhvuu:
  [marked H20 realization](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_root20_anchor_realization),
  source 3e20c2a890f21b5224fb55effbb9964a9ac33f4b.
  [H20.json](H20.json) preserves its graph bytes, SHA-256
  8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf.
- Height 3026, bafkreichit22jd3pb3olz2n6dgyjcn6wbbzaexgjbysuoehijgad4makva:
  [sixteen O22 constructions](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_opposite22_realization),
  source 2396381c98135e7819becd092627006262891d67.
  [SOURCE.json](SOURCE.json) preserves that input. All 108 deletions and
  their sixteen locally valid outcomes are reconstructed. This is
  not a catalogue of all 107-blue-edge graphs.
- Height 3003, bafkreihkoevj5w4svhm253b2ggvqepizsege2ndkjamatfis67a7c5g5ui:
  [R2's fixed-core source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_fixed_core_closure),
  source 7a0064314f61056e21372a132dfc0c458f38312e.
  Only its literal 108-edge local graph enters the O22 construction;
  its distinct fixed-profile UNSAT claim is not a premise.

The final source audit found Helgi's new
[100-case marked-pair decomposition](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_marked_pair_decomposition),
source c281801fd5341821de0f72ab9a83442573a277b9.
Its five maximal attachments, 100 valid local graphs and selector
encoding are **not claimed anew**. Its source was inspected, not
independently replayed in this package. The present density cut
closes all 100 cases under the prescribed density and also closes
the other fifteen O22 choices. All parent local-existence results
remain valid.

The previous [three-switch separation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_switch_gluing)
at height 3030 motivated a transfer test but is not a proof premise.
No binary face was found in a 43-vertex survivor; the newly available
O22 source prompted an explicit change to the marked-density interface.

R1's \(M=214\) reanchoring/incidence work and R2's fixed-core profile
widening are disjoint. No duplicate 440-edge gluing, 396-edge case
search or budget-39 solve was performed.

## Literature and stopping condition

Neighborhood gluing and clique capacity arguments are classical;
see Angeltveit and McKay,
[*R(5,5) ≤ 46*](https://arxiv.org/abs/2409.15709).
No historical-priority claim is made for those general methods.
The new claim is the conditional fixed-family exclusion.

Stop these sixteen cores under the stated hypotheses. The next test
must change an explicit input: another opposite core, marked H20,
or signature/profile family. The certificate supplies a screening
criterion: an admissible 14-set must escape the complementary-clique
obstruction and satisfy the marked-density capacity requirement.
No broader search is included here.
