# Order-3/order-7 specialization image for the QLP-42 group ring

## Theorem

Let `R = Z[i]`, let

```text
Phi3(x) = x^2 + x + 1,
Phi7(x) = x^6 + x^5 + x^4 + x^3 + x^2 + x + 1,
```

and choose the canonical representatives of

```text
a in R[x]/(Phi3),   deg(a) < 2,
b in R[x]/(Phi7),   deg(b) < 6.
```

For `s in R`, there is a polynomial `f in R[x]` of degree less than 21 such
that

```text
f(1) = s,   f mod Phi3 = a,   f mod Phi7 = b                 (1)
```

if and only if

```text
a(1) = s (mod 3),   b(1) = s (mod 7).                       (2)
```

Thus, after the global sum has been fixed, primitive order-3 and primitive
order-7 specializations of an unrestricted Gaussian length-21 group-ring
element have no additional mixed compatibility condition.  In particular,
any QLP-42 obstruction combining these specializations must use information
not present in the unrestricted group ring: the 16-state pointwise `H/S`
coupling, the restricted coefficient alphabet and support, or the primitive
order-21 component.

This is a classification of the specialization map, not a QLP construction.
The interpolating polynomial need not have coefficients in the QLP local-state
alphabet.

## Proof

The two cyclotomic polynomials satisfy the integral Bezout identity

```text
Phi7(x) - (x^4+x) Phi3(x) = 1.                               (3)
```

Consequently `(Phi3)` and `(Phi7)` are comaximal in `R[x]`.  Given `a,b`, put

```text
f0 = a Phi7 + b(1-Phi7).
```

Equation (3) gives

```text
f0 mod Phi3 = a,   f0 mod Phi7 = b,
f0(1) = 7a(1)-6b(1).                                        (4)
```

If (2) holds, then `s-f0(1)` is divisible by both 3 and 7 in `Z[i]`.
The ideals `(3)` and `(7)` are comaximal, so it is divisible by 21.  Set

```text
c = (s-f0(1))/21 in R,
f = f0 + c Phi3 Phi7.                                       (5)
```

The correction vanishes in both cyclotomic quotients and changes the value at
one by `21c`, proving (1).  The construction has degree at most 11, hence in
particular less than 21.

Conversely, if `f=a+q Phi3`, then evaluation at one gives
`f(1)-a(1)=3q(1)`.  The corresponding division by `Phi7` gives
`f(1)-b(1)=7q'(1)`.  Therefore (1) implies (2).

## Consequence for the q=5/q=37 pivot

Represent any of the four coupled length-21 words by its polynomial in
`R[C_21]`.  Its primitive order-3 and order-7 Fourier data are exactly its
residue classes modulo `Phi3` and `Phi7`; its exact Gaussian sum is `f(1)`.
The theorem applies independently to all four words and all six canonical sum
cases.  It rules out a coefficient-free resultant, congruence, or
interpolation obstruction between those two specializations across the whole
216-cell frontier.

This does **not** say that the two specializations are independent after the
16-state local coupling is imposed.  It identifies that coupling (or the
primitive order-21 component) as an indispensable ingredient of any future
family-level theorem.  No `(1+i)`-adic layer, cellwise SAT sweep, or support
orbit census is used here.

## Exact reproduction

The standard-library checker verifies the Bezout identity, the necessity
congruences on all 21 monomial basis elements, and the constructive
sufficiency formula on a nine-parameter universal linear basis.  Because the
identities are integral-linear, the check extends coefficientwise from `Z`
to `Z[i]`.

```bash
python3 verify_specialization_image.py
python3 derive_with_sympy.py
```

The recorded environment is CPython 3.12.12 and SymPy 1.14.0.  Expected
output is in `expected_output.txt`.

## Dependencies and trust boundary

The mathematical proof uses only polynomial division, (3), evaluation at
one, and comaximality of `(3)` and `(7)` in `Z[i]`.  The scripts are redundant
exact checks of the displayed identities; they are not substitutes for the
proof.  The QLP interpretation imports the established canonical norm-32
shell and coupled half-sum/half-difference transform, but the algebraic
specialization theorem itself is independent of those reductions.

The conclusion rules out one proposed *coefficient-unrestricted mechanism*;
it does not exclude a single q=5/q=37 cell, prove a local-state lift, or settle
QLP-42.  Standard interpreter, SymPy, operating-system, and hardware trust
apply only to the reproductions.  There is no floating point, randomness,
solver status, timeout, or exhaustive frontier enumeration.
