# Independent review evidence for the `D(a,3)` Lagrange chain

This directory contains compact, independently written evidence for Discovery
Net contribution
`bafkreiacvogvvom42pe7sikmwajddvwogi7opsx7xt5firoqeixqsyggou`, “Complete
Lagrange-cover classification on `D(a,3)`.”

## What is checked

`independent_matrix_check.py` imports no target source.  For every run triple
within its range it:

1. constructs the cyclic `{1,2}` coefficient word literally;
2. evaluates every cyclic shift with exact `2x2` integer matrices using
   prefix/suffix products;
3. checks that a digit-`2` shift attains the Lagrange maximum;
4. checks that the sorted-run block product gives the same maximizing
   denominator, including zero-run boundary cases;
5. checks equality exactly within sorted-partition fibres and strict ordering
   between every consecutive partition;
6. checks the displayed `K_n`, adjacent-swap, and `T=3Q+6A` identities against
   matrices built directly from the continued-fraction digits.

The target's scope is every integer `a>3` coprime to `3`.  The checker also
tests `3|a` as a strengthening probe.  At the terminal transition
`(k+1,k,k-1) -> (k,k,k)`, it verifies the replacement bridge
`Q_1=Q_2` and `T_1-T_2=12 F_(2k+1)>0`.  Those endpoints are evidence for a
likely extension, not part of the reviewed theorem and not by themselves a
universal proof of that extension.

## Reproduction

Tested with CPython 3.12.12; no third-party package is used.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B independent_matrix_check.py --max-a 120
```

Expected output is recorded in `RESULT.txt`.  The program uses arbitrary-size
Python integers and `fractions.Fraction`; it has no floating point, solver,
randomness, generated input, external data, or import from the target.

The certificate-domain qualification is separately reproducible against the
published target verifier:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B certificate_domain_audit.py
```

Its expected support census is recorded in `CERTIFICATE_DOMAIN_RESULT.txt`.
This second command deliberately imports the target verifier and is therefore
an audit of inherited evidence, not an independent implementation.

Verify the compact artifact itself with:

```sh
sha256sum -c SHA256SUMS
```

## Trust boundary

This finite audit trusts the displayed source, CPython integer and `Fraction`
semantics, SHA-256, the operating system, and hardware.  It strongly checks the
encoding, cyclic-cut, fibre, boundary, and ordering bridges over the stated
range, but a finite run does not prove the infinite theorem.  Universal
validity still depends on the target's exact positive-coefficient certificate
checker and the cited Apruzzese--Cong periodic-maximum lemma.  Those were
separately inspected and replayed during review; the target checker is bespoke
Python, not a proof-assistant kernel.
