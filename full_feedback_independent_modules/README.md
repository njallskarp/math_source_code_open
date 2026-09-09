# One-probe independent substitutions and exact cube duration

If a vertex \(p\) resolves a connected quotient graph \(G\) in one round,
then replacing its vertices by arbitrary nonempty independent modules
preserves one-probe full-feedback directional localization. For module
sizes \(m_v\) and \(M=\max_v m_v\), the constructive strategy takes at
most \(m_p+M-1\) rounds.

The one-probe optimal worst-case duration on
\(Q_3[\overline K_m]\) is exactly \(2m-1\), for every \(m\ge1\).
The proof uses a response invariant supported on antipodal module pairs.
The elementary complete-bipartite family also attains the general uniform
bound; no first-sharpness priority claim is made.

[THEOREM.md](THEOREM.md) supplies the strategy, its handling of extra robber
moves and singleton modules, and the exact-duration lower bound. It does
not prove preservation for an arbitrary adaptive one-probe quotient, and
it does not answer the greater-than-two open question.

## Reproduction

Python 3.10 or later; no extra packages or inputs. From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
shasum -a 256 -c SHA256SUMS
```

The first command must match `EXPECTED_OUTPUT.txt`, ending with:

```text
result_sha256=8ef82f3275f92f8ff755c5707428e72f1feeabf49f98466ec623b233ac94b506
VERIFIED
```

The checker explores all response branches of the constructive policy for
4,716 instances: every labelled connected quotient of orders two through
four with a one-round resolver, every resolver in it, and every module
size vector in \(\{1,2,3\}^{V(G)}\). It directly checks every antipodal
core and probe obligation through \(m=5\), and independently solves the
complete reachable belief games through \(m=4\). Their exact initial
ranks are 1, 3, 5, 7. The invariant audit searches actual response classes;
it does not encode the proof's chosen responses or distance-case split.

Validation used CPython 3.12.12. A second execution with `python3 -B -O`
matched the expected output, taking 1.026 seconds with 23,855,104 bytes peak
child RSS. These host measurements are not mathematical outputs.

## Scope and trust

Universal claims rest on the written proofs. Finite audits validate game
semantics, policy branches, and the invariant; they are not extrapolated
into a theorem. The remaining trust boundary is the written mathematics,
Python, and hardware. There is no solver, floating point, downloaded data,
external graph catalogue, or proof-assistant formalization. Exploratory
censuses and incomplete searches are excluded from the publication.

The results are apparently new relative to the committed graph and primary
sources searched on 2026-09-09, with no historical-priority assertion. They
have not received independent peer review at publication. The adaptive
one-probe preservation question remains the next research milestone.
