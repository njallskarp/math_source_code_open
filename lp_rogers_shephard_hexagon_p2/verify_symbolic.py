#!/usr/bin/env python3
"""Exact diagnostic checks for the normalized support-sector calculation.

All assertions are identities in the rational-function field Q(a,b,t), apart
from formal symbols for phi and pi in the final linear assembly.  Positivity,
angle branches, and the geometric support-area formula belong to the paper
proof and are intentionally not delegated to SymPy.
"""

from sympy import atan, diff, limit, oo, pi, simplify, symbols


a, b, t, phi = symbols("a b t phi", positive=True)
A = 1 + a
B = 1 + b

# In Sectors II and III write theta=pi/2+s and t=tan(s).  Common
# normalization factors are 1/sqrt(1+t^2).
q2_num = (B - a * t) ** 2 + t**2
hh2 = simplify(((B - a * t) * (-a - B * t) + t) / (1 + t**2))
assert simplify(hh2.subs(t, 0) + a * B) == 0
assert simplify(hh2.subs(t, b / a) + a) == 0

q3_num = 1 + (b - A * t) ** 2
hh3 = simplify((-t + (b - A * t) * (-A - b * t)) / (1 + t**2))
assert simplify(hh3.subs(t, b / a) - b) == 0
assert simplify(limit(hh3, t, oo) - b * A) == 0

# Curvature-term antiderivatives after dtheta=dt/(1+t^2).
F2 = B * atan(((a**2 + 1) * t - a * B) / B)
F3 = A * atan(A * t - b)
assert simplify(diff(F2, t) - B**2 / q2_num) == 0
assert simplify(diff(F3, t) - A**2 / q3_num) == 0

# The Sector-II transformed endpoint has the tangent required for a net
# angle phi=atan(b/a).  The paper proof supplies the branch information.
y1 = simplify(((a**2 + 1) * (b / a) - a * B) / B)
assert simplify((a + y1) / (1 - a * y1) - b / a) == 0

sector1 = 2 * A * B
sector2 = B * phi - a * b
sector3 = A * (pi / 2 - phi) - a * b
area = simplify(sector1 + sector2 + sector3)
expected_area = 2 * (1 + a + b) + B * phi + A * (pi / 2 - phi)
assert simplify(area - expected_area) == 0

deficit = simplify((pi / 2 + 2) * (1 + a + b) - area)
expected_deficit = a * phi + b * (pi / 2 - phi)
assert simplify(deficit - expected_deficit) == 0

print("exact sector endpoint identities: OK")
print("exact curvature antiderivatives: OK")
print("exact area assembly: OK")
print("exact deficit assembly: OK")
