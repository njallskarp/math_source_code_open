"""Produce exact cut lower bounds for the complete coarse hard-cap envelope."""
from functools import lru_cache
from itertools import product
from math import comb
import hashlib
import json

CAPS = (78, 85, 93, 100, 107, 115, 125)

@lru_cache(None)
def edge_ceiling(order, cap_sum):
    allowed = []
    for edges in range(comb(order, 2) + 1):
        quotient, remainder = divmod(2 * edges, order)
        squares = (order-remainder)*quotient**2 + remainder*(quotient+1)**2
        if squares - order*edges <= cap_sum:
            allowed.append(edges)
    return max(allowed)

def profiles():
    answer = []
    for a,b,c,e,f,g in product(range(2), range(4), range(14),
                              range(14), range(4), range(2)):
        d = 43-a-b-c-e-f-g
        n = (a,b,c,d,e,f,g)
        weight = 21*(a+g)+12*(b+f)+3*(c+e)
        degree_sum = sum((18+i)*count for i,count in enumerate(n))
        if d >= 0 and weight <= 39 and degree_sum % 2 == 0 and degree_sum <= 902:
            answer.append(n)
    return sorted(answer)

def produce():
    ns = profiles()
    tables = {m: [[1000]*21 for _ in range(2)] for m in range(214,221)}
    census = {m:0 for m in tables}
    digest = hashlib.sha256()
    placements = 0
    for n in ns:
        m = sum((18+i)*count for i,count in enumerate(n))//2-231
        census[m] += 1
        for side in product(*(range(count+1) for count in n)):
            order = sum(side)
            if not 1 <= order <= 21:
                continue
            placements += 1
            digest.update((','.join(map(str,n))+';'+','.join(map(str,side))+'\n').encode())
            for color in range(2):
                degrees = sum((18+i if color == 0 else 24-i)*count
                              for i,count in enumerate(side))
                cap_sum = sum(CAPS[i if color == 0 else 6-i]*count
                              for i,count in enumerate(side))
                lower = degrees-2*edge_ceiling(order,cap_sum)
                tables[m][color][order-1] = min(tables[m][color][order-1],lower)
    universal = [min(tables[m][color][i] for m in tables for color in range(2))
                 for i in range(21)]
    old = [18*a-2*(3*a*a//8) for a in range(1,22)]
    return {'format':'r55-hard-cap-cut-bridge-v1','caps_18_to_24':list(CAPS),
            'profiles':[list(n) for n in ns], 'profile_counts_by_M':census,
            'side_placements':placements,'placement_sha256':digest.hexdigest(),
            'lower_bounds_by_M':tables,'universal_lower_bounds':universal,
            'uniform_two_side_bound':min(universal[1:]),
            'uniform_three_side_bound':min(universal[2:]),
            'old_full_q_bound':old,
            'sizes_where_this_bound_does_not_dominate_old_q':[
                a for a in range(1,22) if universal[a-1] < old[a-1]]}

if __name__ == '__main__':
    print(json.dumps(produce(),sort_keys=True,separators=(',',':')))
