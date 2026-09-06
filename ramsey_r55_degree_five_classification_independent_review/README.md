# Independent review: dense degree-five Ramsey neighborhoods

## Verdict

**Accept, high confidence, conditional only on the explicitly imported complete
catalogue of the two \(R(4,4;16)\) graphs.** I reviewed the claim in the
[target package](https://github.com/njallskarp/math_source_code_open/tree/8bf27902fba404e35593c90cbc7d2991abeda510/ramsey_r55_degree_five_classification)
at commit <code>8bf27902fba404e35593c90cbc7d2991abeda510</code>: if a
22-vertex graph \(H\) has no \(K_4\), no independent 5-set, at least 109
edges, and a degree-five vertex, then \(H\) is exactly one of 13 graphs, all
with 109 edges and a unique degree-five vertex. Consequently
\(e(H)\ge110\) forces \(\delta(H)\ge6\), and 109 is sharp for that conclusion.

## What I checked independently

The reduction is sound. For a degree-five vertex \(z\), its five-neighbor
graph \(S\) is triangle-free and its 16 nonneighbors induce an
\(R(4,4;16)\) graph \(A\). Writing \(X_s=N(s)\cap A\), the classical bound
\(R(3,4)=9\) gives

\[
 |X_s|\le8,\qquad
 e(H)=60+5+e(S)+\sum_{s\in S}|X_s|.
\]

Thus \(e(H)\ge109\) forces \(4\le e(S)\le6\) and
\(\sum_s(8-|X_s|)\le e(S)-4\le2\). I checked the five displayed attachment
conditions against the possible numbers of vertices a forbidden set can use
from \(S\); they are both necessary and sufficient.

I reproduced both target programs from a detached checkout. The producer and
its separately written physical-event audit agree exactly on all 14
core/neighbor cases, 840 rooted labeled tuples, 13 isomorphism classes, and
edge-count set \(\{109\}\) under ordinary and optimized Python execution.
Their adversarial suite also passed twice (15,210 clique-kernel comparisons,
18 malformed-decoder rejections, eight damaged-certificate rejections, and 69
physical-rule comparisons).

<code>verify_independent.py</code> is a third, narrower implementation. It
does **not** claim to re-enumerate the 840 attachments. It instead fetches the
certificate at the pinned target commit and McKay's primary file, verifies
both SHA-256 identities, and uses NetworkX 3.6 rather than either target
decoder or isomorphism engine. It then:

- exhausts all \(2^{10}\) labeled graphs on \(S\), recovering seven eligible
  isomorphism types;
- checks both catalogue records have order 16, 60 edges, no clique or
  independent set of order four, automorphism order eight, and are
  nonisomorphic;
- reconstructs every 22-vertex representative independently from its core,
  \(S\)-edges, and five column masks, and compares that graph with the
  separate graph6 field;
- tests every one of the 7,315 four-subsets and 26,334 five-subsets for every
  representative, verifies 109 edges and the unique marked degree-five
  vertex;
- recomputes all \(\operatorname{Aut}(A)\times\operatorname{Aut}(S)\) orbit
  sizes and orbit minima, checks that their per-case sums are the reported 840
  tuples, and tests all 78 representative pairs for isomorphism.

The degree-four corollary also checks by hand: 17 nonneighbors induce a
\((4,4)\)-graph of maximum internal degree eight, hence at most 68 edges; the
four neighbors contribute at most \(4\cdot8\) cross edges and at most four
internal edges, while the marked vertex contributes four. Therefore
\(e(H)\le68+32+4+4=108\). Degree at most three contradicts \(R(4,4)=18\).

## Reproduction

Use CPython 3.12 and NetworkX 3.6:

~~~bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -B verify_independent.py | shasum -a 256
~~~

Expected stdout SHA-256:
<code>f1a4529b61230e780fee0c6fa1715ee792a8686fb7b7f14acb06032a2b26bb7b</code>.

For the target census itself, from a detached checkout of the target commit:

~~~bash
cd ramsey_r55_degree_five_classification
shasum -a 256 -c SHA256SUMS
python3 -B verify.py --fetch-catalogue | shasum -a 256
python3 -B audit.py | shasum -a 256
python3 -B test_checks.py | shasum -a 256
python3 -O -B verify.py | shasum -a 256
python3 -O -B audit.py | shasum -a 256
python3 -O -B test_checks.py | shasum -a 256
~~~

The first three stdout hashes are, respectively,
<code>3308571c8b746b1bfc52daaf8ff92c7f2c5b95f770d4e4cead66f8ed9f705058</code>,
<code>7e2bff17a142429f9e898da0e61d9563cf1884984174e1aa34d1c4388645507b</code>,
and <code>96fba812bca36e88a128cc3d95b104c640d5caaf3133859520ae47c0ead8e40e</code>;
the optimized runs match them exactly.

## Trust boundary and remaining gap

Checked here: the theorem reduction and boundary cases; exact target replay;
certificate identity; all 13 witnesses; graph6/column agreement; forbidden-set
absence; unique degree-five vertices; orbit arithmetic and pairwise
nonisomorphism. Imported: McKay's assertion that the two-record
[\(R(4,4;16)\) catalogue](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
is complete, the classical values \(R(3,4)=9\) and \(R(4,4)=18\),
CPython/NetworkX semantics, HTTPS delivery, hardware, and SHA-256 collision
resistance. The two finite target searches were inspected and reproduced, not
formally proved or independently reimplemented in full.

The classification is local. It neither eliminates nor constructs a
43-vertex completion of any of the 13 interfaces; all 630 outside/cross edges
remain free. I found no mathematical defect or unsupported global conclusion.
The current Angeltveit--McKay
[\(R(5,5)\le46\) paper](https://arxiv.org/abs/2409.15709)
confirms the broader order-22 extremum \(E(4,5,22)=114\), but does not state
this marked 13-class result. This was a targeted status check, not a priority
determination, and the target makes no novelty claim.
