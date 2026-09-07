"""Exact entrywise PSD certificate for the complete edge-moment matrix.

Cell-sum blocks, standard-cell blocks and explicit orthogonal residual
projectors reconstruct every entry. Positive semidefiniteness of their
coefficient blocks is checked with exact rational arithmetic.
"""
import hashlib
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement
from incident import psd_rank


def require(ok,message):
    if not ok:raise ValueError(message)


def physical_global(point):
    edges=[()]+list(combinations(range(43),2));lookup={e:i for i,e in enumerate(edges)};cache={}
    def moment(e,f):
        if not e and not f:return point.D
        if not e:return point.V[point.edge[f]]
        if not f or e==f:return point.V[point.edge[e]]
        vs=tuple(sorted(set(e+f)));pairs=list(combinations(vs,2));mask=sum(1<<pairs.index(z) for z in (e,f));types=point.types(vs);key=(types,mask)
        if key not in cache:
            dist=point.triples[types] if len(vs)==3 else point.four[types]
            cache[key]=sum(m for s,m in enumerate(dist) if s&mask==mask)
        return cache[key]
    matrix=[[moment(e,f) for f in edges] for e in edges]
    require(len(matrix)==904,'complete edge moment order')
    return edges,lookup,matrix


def decompose(cells,edges,lookup,matrix,check_psd=True):
    flat=sum(cells,[]);require(sorted(flat)==list(range(len(flat))) and all(cells),'complete cell partition')
    require(edges==[()]+list(combinations(range(len(flat)),2)),'complete physical edge roster')
    classes={v:i for i,cell in enumerate(cells) for v in cell};n=len(matrix)
    require(len(edges)==n and all(len(row)==n for row in matrix),'square global matrix')
    orbit=[tuple(sorted(classes[v] for v in e)) for e in edges]
    groups={}
    for i,o in enumerate(orbit):groups.setdefault(o,[]).append(i)
    keys=list(groups);group_index={o:i for i,o in enumerate(keys)};sizes={o:len(g) for o,g in groups.items()}
    B=[[sum(matrix[a][b] for a in groups[o] for b in groups[p]) for p in keys] for o in keys]
    trivial_rank=psd_rank(B) if check_psd else None
    standards={};standard_records=[]
    for i,cell in enumerate(cells):
        ni=len(cell)
        if ni<2:continue
        a,b=cell[:2];labels=[];scales={};vectors={}
        for j,other in enumerate(cells):
            if j==i and ni<3:continue
            d=ni-2 if j==i else len(other);v=Counter()
            for u,sign in ((a,1),(b,-1)):
                for w in other:
                    if u!=w:v[lookup[tuple(sorted((u,w)))]]+=sign
            labels.append(j);scales[j]=d;vectors[j]={e:c for e,c in v.items() if c}
        block={}
        for j in labels:
            for k in labels:
                value=sum(c*d*matrix[e][f] for e,c in vectors[j].items() for f,d in vectors[k].items())
                require(value%2==0,'exact standard normalization');block[j,k]=value//2
        rank=psd_rank([[block[j,k] for k in labels] for j in labels]) if check_psd else None
        standards[i]=(labels,scales,block)
        standard_records.append({'cell':i,'order':len(labels),'multiplicity':ni-1,'rank':rank})
    internal={};tensors={}
    for i,cell in enumerate(cells):
        if len(cell)<4:continue
        a,b,c,d=cell[:4];e=lookup[tuple(sorted((a,b)))];f=lookup[tuple(sorted((a,c)))];g=lookup[tuple(sorted((c,d)))]
        internal[i]=matrix[e][e]-2*matrix[e][f]+matrix[e][g]
    for i,j in combinations(range(len(cells)),2):
        if min(len(cells[i]),len(cells[j]))<2:continue
        a,b=cells[i][:2];c,d=cells[j][:2]
        e=lookup[tuple(sorted((a,c)))];f=lookup[tuple(sorted((a,d)))];g=lookup[tuple(sorted((b,c)))];h=lookup[tuple(sorted((b,d)))]
        tensors[i,j]=matrix[e][e]-matrix[e][f]-matrix[e][g]+matrix[e][h]
    if check_psd:require(min([0]+list(internal.values())+list(tensors.values()))>=0,'nonnegative residual projector coefficients')
    # Reconstruct every physical entry, caching only equal orbit/intersection
    # patterns. Equality to this explicit PSD sum is the final certificate.
    predictions={};checked=0
    for a,e in enumerate(edges):
        o=orbit[a];oc=Counter(o)
        for b,f in enumerate(edges):
            p=orbit[b];common=tuple(sorted(classes[v] for v in set(e)&set(f)));key=(o,p,common)
            if key not in predictions:
                pc=Counter(p);value=F(B[group_index[o]][group_index[p]],sizes[o]*sizes[p])
                for i in set(o)&set(p):
                    if i not in standards:continue
                    labels,scales,block=standards[i]
                    j=o[1] if o[0]==i else o[0];k=p[1] if p[0]==i else p[0]
                    if j not in labels or k not in labels:continue
                    inner=F(common.count(i))-F(oc[i]*pc[i],len(cells[i]))
                    value+=F(block[j,k],scales[j]*scales[k])*inner
                if o==p and o:
                    i,j=o
                    if i==j and i in internal:
                        ni=len(cells[i]);projector=F(int(e==f))-F(1,sizes[o])-F(F(len(common))-F(4,ni),ni-2)
                        value+=internal[i]*projector
                    elif (i,j) in tensors:
                        projector=(F(common.count(i))-F(1,len(cells[i])))*(F(common.count(j))-F(1,len(cells[j])))
                        value+=tensors[i,j]*projector
                predictions[key]=value
            require(matrix[a][b]==matrix[b][a],'physical global symmetry')
            require(matrix[a][b]==predictions[key],'physical global decomposition '+str((a,b)))
            checked+=1
    dimension=len(B)+sum(r['order']*r['multiplicity'] for r in standard_records)
    dimension+=sum(len(cells[i])*(len(cells[i])-3)//2 for i in internal)
    dimension+=sum((len(cells[i])-1)*(len(cells[j])-1) for i,j in tensors)
    require(dimension==n,'orthogonal decomposition dimension')
    rank=None
    if check_psd:
        rank=trivial_rank+sum(r['rank']*r['multiplicity'] for r in standard_records)
        rank+=sum(len(cells[i])*(len(cells[i])-3)//2 for i,lam in internal.items() if lam>0)
        rank+=sum((len(cells[i])-1)*(len(cells[j])-1) for (i,j),lam in tensors.items() if lam>0)
    return {'global_matrix_order':n,'global_physical_entries':checked,'global_entry_patterns':len(predictions),
            'global_trivial_block_order':len(B),'global_trivial_block_rank':trivial_rank,
            'global_standard_blocks':standard_records,'global_internal_components':len(internal),
            'global_tensor_components':len(tensors),'global_orthogonal_dimension':dimension,'global_matrix_rank':rank,
            'global_minimum_residual_coefficient':min(list(internal.values())+list(tensors.values()) or [0])}


def global_edge_matrix(point):
    edges,lookup,matrix=physical_global(point);result=decompose(point.cells,edges,lookup,matrix)
    result['global_minimum_residual_coefficient']=str(F(result['global_minimum_residual_coefficient'],point.D))
    digest=hashlib.sha256(f'904 {point.D}\n'.encode())
    for row in matrix:digest.update((' '.join(map(str,row))+'\n').encode())
    result.update(global_psd_status='EXACT_FULL_904_PSD',total_psd_constraints=45,global_matrix_sha256=digest.hexdigest())
    return result
