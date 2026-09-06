# Albertson 27 and 28: one proof and its publication audit

[MANUSCRIPT.md](MANUSCRIPT.md) gives a joint proof of
\[
\chi(G)\ge r\ \Longrightarrow\ \operatorname{cr}(G)\ge\operatorname{cr}(K_r),
\qquad r\in\{27,28\}.
\]
It consolidates independently reviewed Discovery Net terminal arguments.
The new contribution is a complete common order/complement bridge using
refereed external inputs, with an exact certificate. The consolidated
manuscript and new bridge await independent review. Publication here is
source delivery, not a claim of journal acceptance or historical priority.

A critical counterexample would have connected complement and one of
\[
(r,n,m)=(27,53,713),\ (28,55,768),\ (28,55,769).
\]
The certificate covers all 132 integer orders between the published small-
and large-order cutoffs. The marked join calculation explicitly forces
complement connectivity. The joint terminal argument uses complete-graph
seeds only through \(K_{12}\) and has minimum margin six above the target.
No recent Cranston or Sadhu frontier theorem, Kostochka--Yancey edge bound,
or earlier Albertson case is a premise of this route.

## Reproduction

Clone the whole repository; three reviewed modules in sibling directories
are required and checked against hard-coded SHA-256 hashes. Tested with
CPython 3.12.12, standard library only. No network, solver or Lean build is
needed for this command.

~~~sh
cd albertson_r27_r28_publication
PYTHONDONTWRITEBYTECODE=1 python3 reproduce.py > actual.txt
diff -u EXPECTED_OUTPUT.txt actual.txt
shasum -a 256 -c SHA256SUMS
~~~

Expected: empty diff; every manifest entry OK; output ends with

~~~text
result_sha256=7b7e2e7668e02a33b3b8229c621d21c5670f24f3de63fceb47011cc2b4740f30
VERIFIED
~~~

The normal run regenerates both certificates in memory and compares every
byte. To deliberately regenerate the compact source tables:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 reproduce.py --write-certificates
~~~

[ORDER_CERTIFICATE.tsv](ORDER_CERTIFICATE.tsv) has 132 rows;
[COMPONENT_CERTIFICATE.tsv](COMPONENT_CERTIFICATE.tsv) has 108 rows
(34 for \(r=27\), 37 for each \(r=28\) edge total).
[EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt) records the six recursive
thresholds, four join minima, three component frontiers and ten terminal
split minima. These are relaxed numerical configurations; their survival
does not assert graph realizability.

## Scope and evidence

[PUBLICATION_AUDIT.md](PUBLICATION_AUDIT.md) distinguishes prior research,
independent reviews, this new bridge, source replay, and human/formal
interfaces. The program consumes reviewed implementations; it is not a
new independent review of those implementations. Execution does not prove
the external graph-theoretic or topological theorems. No theorem about
\(r=29\) is included.
