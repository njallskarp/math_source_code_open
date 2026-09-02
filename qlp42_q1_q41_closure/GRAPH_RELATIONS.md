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

## Required topological repair

1. Add the final `b=20` obstruction as a lemma, depending on the coupled
   transform and q=1 third-order partition, and attach an incoming
   `DEPENDS_ON` edge from the existing q=1 closure node.
2. Add the final `b=16` obstruction as a lemma, depending on its committed
   predecessor chain, the coupled transform, and the q=1 partition, and
   attach an incoming `DEPENDS_ON` edge from the existing q=1 closure node.
3. Add one consolidated extreme-branch corollary depending on the repaired
   q=1 closure and the q=41 all-weight closure, refining the defect-count
   restriction and pointing `ABOUT` the QLP-42 problem and area.

Every contribution and all known relations should be submitted atomically
through the isolated local RPC. Post-commit inclusion must be checked in the
committed ledger; CheckTx is not sufficient.

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
