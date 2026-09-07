"""Exact PSD via cell contrasts and group-sum Gram matrices.

Every physical entry is checked before this decomposition is used. No
floating-point eigenvalue calculation or producer import occurs here.
"""
from fractions import Fraction as F


def require(ok,message):
    if not ok:raise ValueError(message)


def psd_rank(matrix):
    """Exact Schur elimination, including singular zero-pivot conditions."""
    n=len(matrix);a=[[F(x) for x in row] for row in matrix];rank=0
    require(all(len(row)==n for row in a),'square matrix')
    require(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)),'symmetric matrix')
    for k in range(n):
        pivot=a[k][k]
        require(pivot>=0,'negative exact PSD pivot '+str(k))
        if pivot==0:
            require(all(a[k][j]==0 for j in range(k+1,n)),'nonzero row at zero PSD pivot')
            continue
        rank+=1
        for i in range(k+1,n):
            for j in range(i,n):
                a[i][j]-=a[i][k]*a[k][j]/pivot;a[j][i]=a[i][j]
    return rank


def physical_matrix(point,h):
    vertices=[u for u in range(43) if u!=h]
    means={u:point.V[point.edge[tuple(sorted((h,u)))]] for u in vertices}
    matrix=[[point.D]+[means[u] for u in vertices]]
    for u in vertices:
        row=[means[u]]
        for v in vertices:
            row.append(means[u] if u==v else sum(m for s,m in enumerate(point.triples[point.types((h,u,v))]) if s&3==3))
        matrix.append(row)
    return vertices,matrix


def decompose(matrix,groups):
    """groups contain matrix indices 1..42; retain index zero separately."""
    require(all(len(row)==len(matrix) for row in matrix),'square physical matrix')
    require(all(matrix[i][j]==matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix))),'symmetric physical matrix')
    require(sorted(sum(groups,[]))==list(range(1,len(matrix))),'complete matrix partition')
    sizes=list(map(len,groups));indices=[[0]]+groups
    block=[[sum(matrix[i][j] for i in g for j in f) for f in indices] for g in indices]
    contrasts=[]
    for t,g in enumerate(groups):
        lam=matrix[g[0]][g[0]]-matrix[g[0]][g[1]] if len(g)>1 else 0
        require(lam>=0,'negative within-cell contrast');contrasts.append(lam)
        for i in g:
            require(matrix[0][i]*len(g)==block[0][t+1] and matrix[i][0]==matrix[0][i],'physical constant entry')
            for s,f in enumerate(groups):
                for j in f:
                    if t!=s:expected=block[t+1][s+1];scale=len(g)*len(f)
                    else:
                        scale=len(g)**2
                        expected=block[t+1][t+1]+lam*len(g)*((len(g) if i==j else 0)-1)
                    require(matrix[i][j]*scale==expected,'physical contrast decomposition entry')
    return block,contrasts,sizes


def incident_matrices(point):
    blocks={};records=[];contrast_min=None;entries=0
    for h in range(43):
        vertices,matrix=physical_matrix(point,h);position={u:j+1 for j,u in enumerate(vertices)}
        groups=[[position[u] for u in cell if u!=h] for cell in point.cells];groups=[g for g in groups if g]
        block,contrasts,sizes=decompose(matrix,groups)
        key=tuple(map(tuple,block))
        if key not in blocks:blocks[key]=psd_rank(block)
        rank=blocks[key]+sum((size-1) for lam,size in zip(contrasts,sizes) if lam>0)
        records.append({'center':h,'block_order':len(block),'block_rank':blocks[key],'matrix_rank':rank})
        eligible=[lam for lam,size in zip(contrasts,sizes) if size>1]
        if eligible:contrast_min=min(eligible) if contrast_min is None else min(contrast_min,*eligible)
        entries+=len(matrix)**2
    require(entries==43**3,'all 43 physical matrices')
    return {'incident_matrix_count':43,'incident_matrix_order':43,'incident_physical_entries':entries,
            'incident_unique_blocks':len(blocks),'incident_blocks':records,
            'incident_minimum_contrast':str(F(contrast_min,point.D)),
            'incident_psd_status':'EXACT_ALL_43_PSD','total_psd_constraints':44}
