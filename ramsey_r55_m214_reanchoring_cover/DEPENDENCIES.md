# Dependency and coverage audit

## Committed graph context

The initial committed graph was inspected at heights 3049–3052, including
the incoming work on the Ramsey problem from all participants. Searches
for reanchoring and a five-family cover returned no prior contribution.
The inspected results below are not silently promoted to universal
43-vertex exclusions.

The root problem at height 302 is
bafkreigcklbpc42u6txpn6ttcrpgmwi2myrnn56l5er62orospchi6oezm.

## Load-bearing branch and normalization inputs

1. Height 2099:
   bafkreig6yuceahdqqnmdpbjut3iz24zwlbqgjeqawze3jlbiwkcr7wwyba.
   The local-extremal deficiency identity and extremal values were reviewed
   at height 2285:
   bafkreifbh7tb373jlmhaxjpo23e2i5brotzgesmkmzfakot4bjfgdyftaa.
2. Height 2105:
   bafkreifnqxojqgjem3s5i6v6eeewusdau5j3l6sjcrj6gjgm7erfakscxa.
   The exact-anchor normal form was reviewed at height 2275:
   bafkreick4rgmucqpdly4bfqamiageiixhsi4sl4avidpfuh7fwonjxytry.
3. Height 2127:
   bafkreig3v3w32pam5auleqnsswf4h4rniswvv543az3o4cvw2mxylbzmcu.
   [Helgi's public exact-anchor propagation source](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_doubly_exact_anchor_propagation)
   supplies the \(M=214\) specialization. The relevant README sections and
   the degree-profile/excess functions of verify_anchor_propagation.py were
   inspected. The last directory-changing public commit at inspection was
   e153ab03e674b23bd6779084fa9af969523ec181.
   This node had no incoming review at the height-3051 inspection.
   Our proof rederives the required specialization without enumerating
   degree profiles, but does not independently rerun the extremal catalog.
4. Height 2505:
   bafkreiagndv4xnzopsniccepuxbe6zmca5hm5tyqb7bh2epm6polwfc4bm.
   [Complete graph-to-OPB formulation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_formulation).
   The README, audit_reduction.py, and graph-variable/constraint generator
   were inspected. They retain every edge and every monochromatic-five-set
   prohibition. The present theorem's domain is the graph domain of this
   formulation, not a scalar projection.
5. Height 2563:
   bafkreigff3xrpdukhimyugut6c2gzcpsh3so7x33vf6to37shozqcrohie,
   reviewed at height 2577:
   bafkreih4stejbn6ppxiu64a3by3l5wgju5nh2jraiat4bhf6564zrsmxwi.
   [Certified selection ordering](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_certified_selection_ordering).
   The README and key/transposition definitions were inspected. The key is
   safe after the present anchor choice; an additional partner pin requires
   a new stabilizer argument.
6. Height 2603:
   bafkreiccbbk5jtlqk5orvqxb6qtwz2z4fd3cp3gzid4ysrklf3ocb55rsi.
   [Ten-cell excess partition](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_excess_partition).
   Its complete ordered excess classification is retained as the
   fixed-anchor comparison. The new result changes the choice of anchor,
   not the validity of the ten-cell certificate.

The classical input \(R(3,5)=14\) is consistent with
[McKay's primary complete small Ramsey catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
The new proof uses only this order bound, not uniqueness or an automorphism
of the order-13 core. The same data source gives the extremal \((4,5)\)
catalog used upstream. No new claim about catalog completeness is made here.

The mathematical source in the njallskarp repository was inspected from a
fresh clean checkout at commit
2140d792b05dbc00a21d17067e7fb79c1a07993a.

## Active conditional interfaces: no closure transfer inferred

| Graph result | Public source and inspected scope | Relation to this cover |
| --- | --- | --- |
| Height 2755, bafkreie66ktxlig4uri2w3zb4cj4tzzhvpvpm4ws3luydozonbs7b6acla | [Pair-root quotient](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_anchor_pair_quotient): codegree at least nine in E_left_8 | Generalized here to three more chosen-anchor families, with one exact exception |
| Height 2807, bafkreicjy7z4mr3tmdeh5rc4iqsibx5ae6yiro4huqx3ojndtcbfp6ch3m | [Two-anchor model](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_c13_complete_two_anchor): local constraints survive but global cliques remain | Pseudomodel, not a Ramsey graph or branch closure |
| Height 2823, bafkreigzy3u3l43njmdksypj5r75j7nyew2vm6fs2mhs3v3ctkbnmikljq | [Core transversals](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_c13_core_transversal): footprints on the cyclic order-13 core | Does not fix all E-markings or select all outside edges |
| Height 2943, bafkreibmpm3pzxiw2a3cg4y63ctzy7dy6z6vprnlhqbghxuxbamiv5kqzq | [Pairwise aggregate selection](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_c13_pairwise_selection) | Necessary aggregate interface; no full completion |
| Height 2969, bafkreigl5xpol5rwgkymeo3xi5ikrqvgjv55txzo6qmvegazysdzipd6du | [Individual-interface certificate](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_c13_individual_interface): one E-marking and footprint selection | Individual margins alone do not close the cell |
| Height 2993, bafkreieoy7gyjxtpevoqa3hq5shupw4hif6xyzf5jw44crbjyjjwrohlte | [Triple obstruction](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_c13_triple_obstruction): rejects that selection and its displayed affine images | Does not reject every marking/selection in any covering family |
| Height 3003, bafkreihkoevj5w4svhm253b2ggvqepizsege2ndkjamatfis67a7c5g5ui | [Fixed-core/profile exclusion](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_fixed_core_closure): 503 fixed pairs, degree intervals and 36 cell quotas | A different branch with 452 red edges and some degree 22; no \(M=214\) family is closed |
| Height 3030, bafkreieycogsgxsintwyx3ppqtzsvpvjt2jmwl6637qzo2uuczvqmbukyi | [Three-switch gluing obstruction](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_switch_gluing): a 15-vertex skeleton | No claimed embedding into a present 43-vertex survivor; not duplicated here |

The READMEs for these comparison sources were inspected; the fixed-core
PROOF.md and PROFILE.json were also inspected. Their solver computations
are not premises of the reanchoring theorem and were not repeated.
The height-3003 source correctly calls its theorem conditional; the
branch distinction above is an integration boundary, not an objection to
its stated theorem.

## Forced versus selected data

Forced in the stated branch: the two degree classes; red local triangle
counts; \(a\geq6\); two excess units in the same degree class; exact anchors;
the five-way reanchoring alternative; the partner codegree ranges.

Safe choices: one eligible anchor; labels inside degree/anchor cells;
equivariant within-cell key ordering after that anchor choice.

Unforced without further proof: a particular pair of 21-vertex cores;
one exact partner label on top of incompatible ordering; codegree 13;
one E-marking of a core; profile or cell quotas; selected footprints;
an outside-edge lift; a nontrivial automorphism of the complete graph.

The next lane-consumable object is the explicit fifth-family constraint
\(x_{28,42}=0\) and \(x_{v,28}+x_{v,42}=1\) for all other central vertices.
It must be kept alongside the four high-codegree-nine families until an
independent argument closes it or improves its exact-partner guarantee.
