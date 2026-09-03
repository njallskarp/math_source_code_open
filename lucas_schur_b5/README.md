# Canonical width-five Lucas Schur positivity

Let `F_0=0`, `F_1=1`, `F_(n+1)=e1 F_n+e2 F_(n-1)`, and let
`{n choose r}_F` be the associated lucasnomial. This directory publishes the
unpacked proof source for every nontrivial canonical `b=5` ray:

| ray | normalized comparison | range | graph artifact |
|---|---|---:|---|
| `a=1` | `{k+5 choose 5}_F-F_(5k+1)` | `k>=5` | `bafkreid3syx42txanl5jeoc32mm64cwxsv7rxtx24rmv3f7w46pluidxyi`, height 1607 |
| `a=2` | `{5k+2 choose 2}_F-{2k+5 choose 5}_F` | `k>=3` | `bafkreigt43gkrgbxcfumuisrcank2sh75cghqtkqvvkhp42st6nvy4cu7u`, height 1575 |
| `a=3` | `{3k+5 choose 5}_F-{5k+3 choose 3}_F` | `k>=2` | `bafkreidxd3zjqe54g37rxm4jab7qtng5iq2xti36qcdih7lvpd4cjaqfrq`, height 1557 |
| `a=4` | `{5k+4 choose 4}_F-{4k+5 choose 5}_F` | `k>=2` | `bafkreietghhgglnr2vb6ke65cj4lsrattsszmawwvbf44phkkx2cuus7lq`, height 1537 |

[`a1/`](a1/) proves the stronger all-width theorem
`{b+c choose b}_F-F_(bc+1) in N[e1,e2]` for every `2<=b<=c`, using an
even-shift KOH transport. [`a2/`](a2/), [`a3/`](a3/), and [`a4/`](a4/)
prove the interior rays through exact restricted-partition layer formulas and
adjacent Schur-layer pairing. `verify_slice.py` is an independent finite
definition-level audit of the three interior rays.

The interior synthesis is graph artifact
`bafkreia7higbufees2ntkqacoshnmayfhkevtlv4t56dzr4ts3lbsxa5zq` at height
1589. Combining it with the `a=1` theorem resolves every canonical width-five
ray mathematically. The aggregate must nevertheless remain **provisional**:
the 72-cell `(2,5)` certificate has no independent review at indexed height
1628. The `(3,5)` and `(4,5)` certificates were independently accepted at
heights 1565 and 1547.

## Reproduction

Run from the repository root under CPython 3.12.12. SymPy is used only by the
three symbolic certificate producers.

```bash
python3 -m pip install -r lucas_schur_b5/requirements.txt

PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a1/verify_koh.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a1/verify_sparse.py

PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a2/verify_symbolic.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a2/verify_fraction.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a2/verify_layers.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a2/verify_sparse.py

PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a3/verify_symbolic.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a3/verify_fraction.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a3/verify_layers.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a3/verify_sparse.py

PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a4/verify_symbolic.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a4/verify_layers.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a4/verify_sparse.py

PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/verify_slice.py
(cd lucas_schur_b5 && sha256sum -c SHA256SUMS)
```

Compact expected certificate hashes:

- `a=1` KOH structural record:
  `2ed9293c891669589170bf172bbec8b54860bf69ef2d295be84d65c125566a94`.
- `a=2` SymPy/Fraction records:
  `73b29979e55d22ac28008c5b3f2f9298386623186a1972238b8c21bba3a57c64` /
  `212b4173408454f6c75298a484dad40abcab29aacd319644d8c1a5ea9cd5023d`.
- `a=3` SymPy/Fraction records:
  `b15738db8e9f1041b95d72eda84807d858d29ca5616b504e275f5d1d9f127b1b` /
  `30b60ee3c72ace0c5e95848d171f8602218bc9bfd10e7fdaa58afda14378bf20`.
- `a=4` SymPy record:
  `f5f0756fce46c6c69c319a5895369ed15fd5a1cd14c7e36a3052250c9a8a13a4`.
- Interior aggregate audit:
  `5a4dc7d8534fa8fa03b1a37ce14a7486b878029e64c761df0acd872d237a090e`.

## Trust boundary

The universal claims rest on the written identities and exact symbolic
certificates documented in the ray READMEs, not on their finite test cutoffs.
All computations use exact integers or rationals. There is no floating point,
randomness, solver status, modular reconstruction, interpolation, or external
generated proof data. No tar archive, cache, database, binary, ledger, key, or
private node state is included here.
