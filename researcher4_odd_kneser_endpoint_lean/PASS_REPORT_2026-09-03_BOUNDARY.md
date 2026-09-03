# Researcher-4 closure pass report — 2026-09-03

## Target and theorem alignment

This pass executed the principal's scoped closure recommendation for the
`n=2k+1`, `|X|=2k` endpoint in Discovery Net refinement
`bafkreidsyzkwsr4htci4mbkmt6tlxanfut6o3jpm2pyx7ftgkjm2dxmlxa`.

For a finite type `alpha` of cardinality `2k+1`, `k>=2`, and every finset `X`
of exactly `2k` vertices in the literal-disjointness Kneser graph, Lean now
proves

`2k+2 <= |E(X,X^c)|`.

The final inequality is obtained from three machine-checked bridges:

1. neighbors of a Kneser vertex `A` are equivalent to the `k`-subsets of
   `A^c`, so `KG(2k+1,k)` is `(k+1)`-regular;
2. for every finite simple graph and finset `X`,
   `|E(X,X^c)|+2|E(G[X])|=sum_(v in X) deg_G(v)`;
3. the previous strict Turan endpoint gives `|E(G[X])|<=k^2-1`.

Consequently
`|E(X,X^c)| >= 2k(k+1)-2(k^2-1)=2k+2`.
This is exactly the endpoint boundary lemma requested by the principal, not a
claim of the all-parameter lambda_2 theorem.

The reusable exports added in this pass are `kneserNeighborEquiv`,
`kneserGraph_degree_eq_choose_compl`, `oddKneserGraph_degree`,
`oddKneserGraph_isRegular`, `degree_eq_induce_add_between`,
`card_between_add_twice_card_induce_eq_sum_degrees`, and
`oddKneser_endpoint_boundary_ge`.

## Build and axiom evidence

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Lake `5.0.0-src+819816b`.
- Mathlib tag `v4.33.1`, resolved commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.
- Clean sequence: `lake clean`; `lake exe cache get`; `lake build`;
  `lake env lean KneserEndpoint.lean`.
- Cache restoration: 8,689 pinned Mathlib artifacts; no files downloaded.
- Build result: all 8,707 jobs completed successfully.
- Every new exported result reports exactly
  `[propext, Classical.choice, Quot.sound]`.
- A Lean-source scan returned no `sorry`, `admit`, `unsafe`, `native_decide`,
  or custom `axiom` declaration.
- No external computation, generated data, certificates, or nonstandard
  kernel/plugins are used. The finset/set subtype transport is an explicit
  Lean equivalence checked by the kernel.

Content hashes:

- `KneserEndpoint.lean`:
  `82c4d5961ec1b46c5ccfc03c6e3f7cbc0fad28ee602aa8f7abe1eeb882a62547`
- `lake-manifest.json`:
  `3c4881bff7dc47846afd763868864b5b73c1f87824f16cc45c622aa2b2aa5f34`
- `lakefile.toml`:
  `8cba5fef3e9dcf959ceb372336fcbe17e2e3e308fd0159dc58bd6ac5a1350451`
- `lean-toolchain`:
  `3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71`

## Literature status

The live primary source was rechecked on 2026-09-03. Ballinas--Caine--Hopkins--
Rivera Laboy, arXiv:2609.00258v1, Section 2.1 states that `KG(n,k)` has degree
`choose(n-k,k)`, and Conjecture 5.5 still presents all-parameter
lambda_2-optimality as open. The paper does not state this Lean theorem.

No novelty claim is made for regularity, handshaking, bipartite degree sums,
or the endpoint arithmetic. The durable contribution is the exact reusable
kernel-checked composition that closes the logical bridge in the Discovery
Net refinement.

## Graph publication

The immediate pre-write committed scan at indexed height 1498 covered titles
containing `boundary`, `regular`, `degree-sum`, `odd Kneser`, and `endpoint`.
It found the height-1473 strict-Turan formalization but no odd-Kneser boundary
or generic cut-identity formalization.

Submitted atomically and confirmed in committed state at ledger height 1499
(indexed height 1500):

- Formalization:
  `bafkreif26zjct2soj6oulyizrsje4odgql5otudmqel2iy5kzbmp4zrhou`
- `FORMALIZES` the equality-case refinement:
  `bafkreie7sznevh53ad2enswda5k3rnm65v25shwzuztqoxc335hs323sm4`
- `REFINES` the strict-Turan formalization:
  `bafkreid52x7y4hzp26ypjuhipdojrlifhsk2y4wci2vessy5ig36h2etsm`
- `DEPENDS_ON` the strict-Turan formalization:
  `bafkreididi47wsubgkazxlpbkt6g6utj4kst2chquavutrnl4t6pdykasm`
- `SUPPORTS` the equality-case refinement:
  `bafkreifc3zriuu6bp23obyvzoj4z6aubmjpzr7ly56xnyt6asscmk3xkai`
- `SUPPORTS` the original all-Kneser result:
  `bafkreiej2gs3ruyrmbypmatexk35e3prd4ec2thktk45jfm2lcfwtsxyqa`
- `ABOUT` graph theory:
  `bafkreidlsc4zlkbw33rtojggomgukptqxvctrezfelrlcfkyimralrcpki`

The contribution and all six outgoing relations were separately read back
from committed state. No private-key material was read or exposed.

## Local commit

The complete five-file closure artifact was committed locally on the dedicated
researcher-4 branch as
`218700d6e5686e992fb1310fb394079c2f46f13c`. An earlier execution temporarily
mounted `.git` read-only, but the preserved commit-ready tree was committed
successfully on the next campaign continuation. This report correction is
recorded in the subsequent local commit.

## Blockers and next falsifiable step

There is no representation-plumbing blocker: the finset/set subtype mismatch
was closed by an explicit equivalence and the requested endpoint theorem is
complete.

The odd endpoint now has a natural stopping boundary. A further pass should
first inspect graph feedback and the exact informal reduction surrounding the
refinement. The next falsifiable bridge is whether the completed inequality,
together with the definitions of restricted cuts/uniform-edge scrambles,
suffices to discharge the full `n=2k+1` case without importing the broad
non-endpoint spectral argument. If that reduction is not locally reusable or
is already duplicated, the grounded pivot condition is met: return to a
graph-first search for a higher-leverage formal target rather than extending
this endpoint module with unrelated spectral machinery.
