#!/usr/bin/env python3
"""Known exact Gram matrices and adversarial controls for both global proofs."""
from itertools import combinations
import json
import global_psd
import independent_global


def require(ok,message):
    if not ok:raise ValueError(message)


def cells_from_sizes(sizes):
    cells=[];start=0
    for size in sizes:cells.append(list(range(start,start+size)));start+=size
    return cells


def main():
    cases=entries=images=rejected=0
    def reject(call):
        nonlocal rejected
        try:call()
        except ValueError:rejected+=1
        else:raise ValueError('bad global evidence accepted')
    sizes_list=((1,),(2,),(3,),(4,),(1,2,3),(2,2),(3,4),(1,2,4))
    for sizes in sizes_list:
        cells=cells_from_sizes(sizes);nv=sum(sizes);edges=[()]+list(combinations(range(nv),2));lookup={e:i for i,e in enumerate(edges)};n=len(edges)
        cls={v:i for i,c in enumerate(cells) for v in c};literal=[1]+[int((cls[u]+cls[v])%2==0) for u,v in edges[1:]]
        matrices=[([[0]*n for _ in range(n)],0),([[int(i==j) for j in range(n)] for i in range(n)],n),
                  ([[x*y for y in literal] for x in literal],1),
                  ([[4 if i==j==0 else 2 if i==0 or j==0 or i==j else 1 for j in range(n)] for i in range(n)],n)]
        for matrix,rank in matrices:
            a=global_psd.decompose(cells,edges,lookup,matrix);b=independent_global.check_basis(cells,edges,matrix)
            require(a['global_matrix_rank']==b['rank']==rank,'known global Gram rank')
            cases+=1;entries+=a['global_physical_entries'];images+=b['basis_image_coordinates']
        bad=[[int(i==j) for j in range(n)] for i in range(n)];bad[0][0]=-1
        reject(lambda:global_psd.decompose(cells,edges,lookup,bad));reject(lambda:independent_global.check_basis(cells,edges,bad))
        if n>1:
            bad=[[0]*n for _ in range(n)];bad[0][1]=bad[1][0]=1
            reject(lambda:global_psd.decompose(cells,edges,lookup,bad));reject(lambda:independent_global.check_basis(cells,edges,bad))
            bad=[[int(i==j) for j in range(n)] for i in range(n)];bad[0][1]=1
            reject(lambda:global_psd.decompose(cells,edges,lookup,bad));reject(lambda:independent_global.check_basis(cells,edges,bad))
            reject(lambda:global_psd.decompose(cells,edges[:-1],lookup,bad));reject(lambda:independent_global.check_basis(cells,edges[:-1],bad))
    # The complete dimension-904 identity verifies the projector resolution
    # and the independent spanning-basis construction on the actual cells.
    cells=cells_from_sizes((1,1,6,6,1,12,2,2,12));edges=[()]+list(combinations(range(43),2));lookup={e:i for i,e in enumerate(edges)}
    identity=[[int(i==j) for j in range(904)] for i in range(904)]
    a=global_psd.decompose(cells,edges,lookup,identity);b=independent_global.check_basis(cells,edges,identity)
    require(a['global_matrix_rank']==b['rank']==904,'full identity rank and coverage')
    cases+=1;entries+=a['global_physical_entries'];images+=b['basis_image_coordinates']
    require((cases,rejected)==(33,58),'global control coverage')
    print(json.dumps({'status':'GLOBAL_PSD_CONTROLS_PASS','known_gram_matrices':cases,'damaged_inputs_rejected':rejected,
                     'exact_reconstructed_entries':entries,'exact_basis_image_coordinates':images,'full_identity_rank':904,
                     'boundary_cell_sizes':[list(s) for s in sizes_list]},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
