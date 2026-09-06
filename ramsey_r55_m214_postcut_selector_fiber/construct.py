#!/usr/bin/env python3
"""Construct five rational four-vertex probability tables by Walsh inversion."""
import argparse
from fractions import Fraction as F
import itertools as it
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent


def require(ok,message):
    if not ok:raise ValueError(message)


def construct(parameters):
    require(set(parameters)=={'u','v','t1','t2'},'four free parameters')
    u,v,t1,t2=(F(parameters[k]) for k in ('u','v','t1','t2'))
    a,b,c=F(20,39),F(6,13),F(15,29)
    # A wedge is indexed by center class and number of exceptional leaves.
    wedge={(1,2):(19*a-30*u)/11,(1,1):u,(1,0):(19*b-12*u)/29,
           (0,2):(20*b-29*v)/12,(0,1):v,(0,0):(20*c-13*v)/28}
    triangle={1:t1,2:t2,3:(93-360*t2-435*t1)/66,
              0:(100-78*t2-377*t1)/406}
    pairs=tuple(it.combinations(range(4),2));result=[]
    for q in range(5):
        exceptional=tuple(int(i<q) for i in range(4))
        def edge(pair):return (c,b,a)[sum(exceptional[i] for i in pair)]
        coefficients={0:F(1)}
        for j,pair in enumerate(pairs):coefficients[1<<j]=1-2*edge(pair)
        for j,k in it.combinations(range(6),2):
            common=set(pairs[j])&set(pairs[k])
            if len(common)!=1:continue
            h=next(iter(common));leaves=(set(pairs[j])|set(pairs[k]))-{h}
            joint=wedge[exceptional[h],sum(exceptional[i] for i in leaves)]
            coefficients[(1<<j)|(1<<k)]=1-2*edge(pairs[j])-2*edge(pairs[k])+4*joint
        for triple in it.combinations(range(4),3):
            indices=[pairs.index(pair) for pair in it.combinations(triple,2)]
            joints=sum(wedge[exceptional[h],sum(exceptional[i] for i in triple if i!=h)] for h in triple)
            coefficients[sum(1<<i for i in indices)]=1-2*sum(edge(pairs[i]) for i in indices)+4*joints-8*triangle[sum(exceptional[i] for i in triple)]
        require(len(coefficients)==23,'Fourier support')
        # All other coefficients, including those of disjoint edge pairs,
        # are zero. Nonnegativity is checked; it is not assumed for inversion.
        atoms=[sum(value*(-1)**((mask&subset).bit_count()) for subset,value in coefficients.items())/64 for mask in range(64)]
        require(min(atoms)>0 and sum(atoms)==1,'four-vertex probability')
        result.append(atoms)
    D=math.lcm(*(x.denominator for atoms in result for x in atoms))
    return {'denominator':D,'four_vertex_atoms':[{'exceptional_count':q,'numerators':[int(x*D) for x in atoms]} for q,atoms in enumerate(result)]}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--parameters',type=Path,default=HERE/'parameters.json');parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.write_text(json.dumps(construct(json.loads(args.parameters.read_text())),indent=2)+'\n')

if __name__=='__main__':main()
