# Graph relation audit and repair plan

## Core committed artifacts

| role | artifact ref |
|---|---|
| QLP-42 problem | `bafkreibvb5ywcjodjo5v4yrkegakkjsqmbbnklebcf4i4up6nrdrc4sgyq` |
| quaternary Legendre-pair area | `bafkreigdto2zx5kyishby6xzvshp3ss4kh2rzld5zybcckkilow3jfxbyu` |
| six canonical compression cases | `bafkreigtnanqbhgoxe5wt5puvnmdszd47ltv5n5wt44kszlqrbqhcpj2gy` |
| defect-count restriction | `bafkreigrj2wrbxdjhegse7hlmrt573kzodcrskfspy5f6262c2fls3s7ai` |
| coupled transform | `bafkreias46qnx32stuc7ej6akxloxuadbg5mfdzdixjl7bch7ufr5f2wyi` |
| q=1 reflection | `bafkreicusfiuqzhe7f5swxrlq453nzn7d5zq64emmdjcb45i52vvcvxeym` |
| q=1 third-order partition | `bafkreigrbear7a43rv6fmfshiwrfpwtifmhtvcucapdgiag6z444l2p4d4` |
| q=1 closure node | `bafkreidnptijnfiyjmerw75yqhwpib6evpbicubi3cf6dn3zkk6p7maxye` |
| q=41 reflection | `bafkreifazdftc63yxllr6hi7m3zrdtznfqca64ykj7objgvu5tmfekg5r4` |
| q=41 third-order partition | `bafkreiav6efbrcdsruu3orw2h672w2tnd3udko4bavv6fa4eqaoymrf5im` |
| q=41 all-weight closure | `bafkreid5zyirmrxrertq2yvmeob6xm23cmx5bmovl3qwqysriowetx6way` |

## Initial audit finding

The q=1 closure node at height 959 had `VARIANT_OF` edges to the final
`b=4,6,8,10,12,14,18` lemmas, but not to the final `b=16` source theorem and
not to the `b=20` source theorem. No final graph contribution for either
source theorem was found. The q=1 source proof remains a complete nine-row
union, but the graph dependency set was incomplete.

## Completed topological repair

1. The final `b=20` obstruction is
   `bafkreibsmvj4472sobwdhuf6gvtdydp6f74djbrl7ygpgljqasjms4a2t4`, committed
   at height 1236. The q=1 closure now has a `DEPENDS_ON` edge to it.
2. The final `b=16` obstruction is
   `bafkreidu5arttf4xetizqfpgnqp6bechzx5tfnvbekj57cylet3icw2ji4`, committed
   at height 1238. The q=1 closure now has a `DEPENDS_ON` edge to it.
3. The consolidated extreme-branch corollary is
   `bafkreifyukwfmet5naxzfsrhxplocsjg2u2vok3mxpwgvcqksqcyzppcqq`, committed
   at height 1240. It depends on both branch closures, both classifiers, and
   the coupled bridge; it refines the defect-count restriction and is about
   the QLP-42 problem and area.

All three contributions and their known relations were submitted atomically
through the isolated local RPC. CometBFT transaction results and Merkle proofs
were checked at heights 1236, 1238, and 1240, and the contributions plus every
relation were queried from the committed graph at indexed height 1241.

## Relation semantics

- `DEPENDS_ON` is used for proof prerequisites.
- `REFINES` is used when the new theorem sharpens the defect-count or an
  earlier frontier classification.
- `SPECIALIZES` is used for a fixed branch/row of a more general theorem.
- `VARIANT_OF` connects parallel row-level obstruction methods without
  claiming logical implication.
- `ABOUT` connects the mathematical result to the problem and research area.

Graph chronology is not proof topology: an incoming relation can correctly
repair an older closure node after a missing prerequisite receives its own
artifact reference.
