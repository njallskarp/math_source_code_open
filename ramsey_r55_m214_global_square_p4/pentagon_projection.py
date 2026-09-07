#!/usr/bin/env python3
"""Exact survivor of the stated M214 pentagon-count projection, not a graph."""
from copy import deepcopy
from math import comb
import json


def require(ok,message):
    if not ok:raise ValueError(message)


def verify(w):
    require(set(w)=={'N_red','N_blue','W_red','W_blue','P'},'schema')
    L=[0]*10+[2,4,7,12]
    correction=[L[q]-2*(q-9) for q in range(14)]
    total_F=0
    for color,edges,qsum in [('red',445,4209),('blue',458,4389)]:
        N=w['N_'+color];W=w['W_'+color]
        require(len(N)==14 and all(type(v)==int and v>=0 for v in N),'integer pair histogram')
        require(sum(N)==edges and sum(q*N[q] for q in range(14))==qsum,'color edge and triangle totals')
        require(type(W)==int and W>=0,'integer joined count')
        require(sum(L[q]*N[q] for q in range(14))<=W,'hereditary pentagon lower bounds')
        require(W<=sum(comb(q,5)*N[q] for q in range(5,14)),'trivial local upper bounds')
        require(W<=26*w['P'],'per-color homogeneous-anchor cap')
        total_F+=sum(correction[q]*N[q] for q in range(14))
    P=w['P'];W=w['W_red']+w['W_blue']
    require(type(P)==int and 18<=P<=comb(43,5),'integer pentagon count')
    require(903+3*13+total_F<=W<=52*P,'complete aggregate incidence bounds')
    require(W<=comb(43,7),'seven-set upper bound')
    return total_F


def main():
    # M214 gives 445 red/458 blue pairs, 1403 red/1463 blue triangles,
    # and sigma=13. Histogram entries are counts of same-color codegrees.
    w={'N_red':[0]*9+[241,204,0,0,0],
       'N_blue':[0]*9+[191,267,0,0,0],
       'W_red':408,'W_blue':534,'P':21}
    F=verify(w)
    # A dual-style scalar lower bound valid for every histogram in this
    # complete projection: W_blue>=2*4389-18*458=534 and W_blue<=26P.
    lower=2*4389-18*458
    require(lower==534 and (lower+25)//26==21,'sharp projected integer minimum')
    # Optional distribution over 21 abstract pentagon records respects
    # each of the two 26-edge caps and a 38-vertex disjoint-neighbor budget.
    slots=[(19,25,10,13)]*12+[(20,26,10,13)]*9
    require(sum(v[0] for v in slots)==408 and sum(v[1] for v in slots)==534,'slot incidence totals')
    require(all(r<=2*ur<=26 and b<=2*ub<=26 and ur+ub<=38 for r,b,ur,ub in slots),'slot capacities')
    rejected=0
    for mode in ('missing','histogram','fraction','lower','upper','P'):
        bad=deepcopy(w)
        if mode=='missing':bad['N_red'].pop()
        elif mode=='histogram':bad['N_blue'][9]+=1
        elif mode=='fraction':bad['N_red'][9]=241.0
        elif mode=='lower':bad['W_blue']=533
        elif mode=='upper':bad['W_blue']=547
        else:bad['P']=20
        try:verify(bad)
        except ValueError:rejected+=1
        else:raise ValueError('damaged aggregate accepted')
    require(rejected==6,'corruption coverage')
    print(json.dumps({'status':'EXACT_M214_PENTAGON_PROJECTION_SURVIVOR',
          'witness':w,'correction_F':F,'sigma':13,'total_joined_pentagons':942,
          'minimum_projected_integer_P':21,'corruptions_rejected':rejected,
          'scope':'Only the explicit count projection; no pentagon placements, shared vertices, physical realization, or extension of a P4 point is certified.'},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
