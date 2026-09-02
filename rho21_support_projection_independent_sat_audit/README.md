# Independent satisfiability audit of the four rho=21 support witnesses

This is an independent direct audit of the four finite selected-support
witnesses recorded by
`ramsey_r55_symbolic_extension/rho21-bichromatic-matching-cover-certificate.json`.
It does not import or execute the producer's satisfiability checker or its
assignment certificate.

The audited producer source is immutable commit
`24d0ad83f16c61d77a7cfd44cdd69512be6c3de7`.  The two reconstruction inputs
have SHA-256 digests `01f6b874013d4a85e86b408dbedd04c56e9f03f87da34fff24d3e2b0972e9424`
and `6f30cd3cc288f6e58feeb57adc8b8f4122740b300c92795930639fbafc8fef87`.

The checker reads only the earlier public matching-cover and blue-kernel
certificates, whose SHA-256 digests are pinned in the source.  It reconstructs
the 23 selected blue K4s from the 41 edge occurrences of the clause kernel and
the ten side nodes containing pivot 41.  It reconstructs the 21 selected red
K4s from the distinguished support `{37,38,39,41}` and each survivor's twenty
four-edge matchings.

For a true-vertex set `T`, the signed-clause convention is checked directly:

- a selected red K4 `R` contributes `OR(not x_v for v in R)` and is false
  exactly when `R` is a subset of `T`;
- a selected blue K4 `B` contributes `OR(x_v for v in B)` and is false exactly
  when `B` is disjoint from `T`.

The assignments are independently transcribed as sets in `verify.py`.  For
both demand cases of the q=0 kernel the true set is
`{3,7,10,17,34,37,38,40,41}`.  For both demand cases of q=1 it is
`{3,7,10,17,36,38,39,40,41}`.

Run from the public repository root:

```bash
python3 rho21_support_projection_independent_sat_audit/verify.py
```

The output gives a canonical SHA-256 digest of each reconstructed colored
formula and confirms that every red clause has a false-assigned vertex and
every blue clause has a true-assigned vertex.

The four canonical colored-formula digests, in q=0/in, q=0/out, q=1/in,
q=1/out order, are:

```text
b81e9c05ded9d5174d20f9eff40797b20ceb52fcf8bd3bc7d431e19910741b9f
5cfbf978620f6f5ffbacada2df770e4ada16d70ea7dfe042e7843a3a8b2c6681
299fac4547ac5e81bcc58923d15ede453f38d982704866ff446cee68ecec078e
a54d21359ebc952486c9d7ce36ec709d3757e1a66f8846e4d1c69f61c3c83ddd
```

The conclusion is exact but narrow: these four displayed partial-support
systems are satisfiable and therefore are not minimally unsatisfiable, in
MU(2), or eligible as the assumed starting point of the singular-DP ancestry.
Nothing here shows that every matching-cover solution or every rho=21 system
is satisfiable, nor that these selected supports complete to a Ramsey core.
