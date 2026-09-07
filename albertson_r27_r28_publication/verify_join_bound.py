#!/usr/bin/env python3
"""Check the marked-join polynomial certificate for r=27,28, exactly.

Author verification, not independent review. No imported source or packages.
The manuscript proves the graph-to-variables map and the nonnegative identity.
This program checks every polynomial coefficient for all relevant part counts,
the scalar substitutions, and the four tight relaxed integer bounds.
"""
from hashlib import sha256
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {m: c for m, c in result.items() if c}


def scale(coefficient, polynomial):
    return {m: coefficient*c for m, c in polynomial.items() if coefficient*c}


def multiply(a, b):
    result = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            monomial = tuple(sorted(ma+mb))
            result[monomial] = result.get(monomial, 0) + ca*cb
    return {m: c for m, c in result.items() if c}


def variable(index):
    return {(index,): 1}


def square(polynomial):
    return multiply(polynomial, polynomial)


def shift_marked(polynomial):
    """Substitute u_1=3+z_1, preserving variable index 0 for z_1."""
    result = {}
    for monomial, coefficient in polynomial.items():
        term = {(): coefficient}
        for index in monomial:
            factor = add({(): 3}, variable(0)) if index == 0 else variable(index)
            term = multiply(term, factor)
        result = add(result, term)
    return result


def verify_identity(t):
    u = [variable(i) for i in range(t)]
    s = [variable(t+i) for i in range(t)]
    total_u, total_s = add(*u), add(*s)
    q = add(scale(2, add(*(square(x) for x in u))),
            scale(3, add(*(multiply(x,y) for x,y in zip(u,s)))),
            add(*(square(x) for x in s)), scale(-2, u[0]))
    q_star = add(scale(2, square(total_u)),
                 scale(3, multiply(total_u,total_s)), square(total_s),
                 scale(-2,total_u))
    difference = add(q_star, scale(-1,q))
    positive_form = add(
        *(multiply(add(scale(4,u[0]), {(): -2}), u[i]) for i in range(1,t)),
        *(scale(4,multiply(u[i],u[j])) for i in range(1,t) for j in range(i+1,t)),
        *(scale(3,multiply(u[i],s[j])) for i in range(t) for j in range(t) if i != j),
        *(scale(2,multiply(s[i],s[j])) for i in range(t) for j in range(i+1,t)))
    require(difference == positive_form, 'Polynomial identity failed')
    shifted = shift_marked(positive_form)
    require(shifted and all(c > 0 for c in shifted.values()),
            'Nonnegative coefficient certificate failed')
    # Two deliberate corruption controls, checked without assertions.
    require(add(difference,{(): 1}) != positive_form,
            'Changed identity was accepted')
    damaged = dict(shifted)
    damaged[next(iter(damaged))] = -1
    require(not all(c > 0 for c in damaged.values()),
            'Negative coefficient was accepted')
    return [[list(m),c] for m,c in sorted(shifted.items())]


def ceil_half(value):
    return -((-value)//2)


def main():
    identities = {t: verify_identity(t) for t in range(2,26)}
    substitutions = 0
    rows = []
    expected = {(27,52):712,(27,53):725,(28,54):766,(28,55):780}
    for r in (27,28):
        for epsilon in (2,1):
            n = 2*r-epsilon
            base = r*(n+1)-8
            for t in range(2,r-2):
                total_u, total_s = r-t,t-epsilon
                require(total_u >= 3 and total_s >= 0, 'Invalid part domain')
                q_star = 2*total_u**2+3*total_u*total_s+total_s**2-2*total_u
                lower = n*n-3*r+2*epsilon-4-q_star
                surplus = (t-2)*(r-epsilon-2)
                require(lower == base+surplus, 'Scalar identity failed')
                require(surplus >= 0, 'Part-count surplus has wrong sign')
                require(t in identities, 'Part-count identity missing')
                substitutions += 1
            lower = ceil_half(base)
            # A singleton and the marked (r-1,n-1) part attain the relaxed
            # edge expression, including its parity rounding; no graph is claimed.
            witness = (n-1)+ceil_half((r-2)*(n-1)+2*(r-1)-6)
            require(lower == witness == expected[r,n], 'Endpoint mismatch')
            rows.append({'r':r,'n':n,'twice_unrounded_floor':base,
                         'integer_floor':lower,'relaxed_witness_edges':witness})
    encoded = json.dumps(identities, sort_keys=True,separators=(',',':')).encode()
    result = {'scope':'Albertson r=27,28 marked-join bound; author algebraic verification',
              'polynomial_identities':len(identities),
              'scalar_substitutions':substitutions,
              'corruption_controls':2*len(identities),
              'nonnegative_polynomial_sha256':sha256(encoded).hexdigest(),
              'rows':rows}
    canonical = json.dumps(result,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps(result,indent=2,sort_keys=True))
    print('result_sha256='+sha256(canonical).hexdigest())
    print('VERIFIED')


if __name__ == '__main__':
    main()
