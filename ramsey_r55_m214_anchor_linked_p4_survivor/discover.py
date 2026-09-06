#!/usr/bin/env python3
"""Optional rational discovery restriction for root 278; full checking is separate."""
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction as F
import itertools as it,functools,json,math,sys,time,importlib.util
HERE=Path(__file__).resolve().parent;REPO=HERE.parent
import hashlib
parent=REPO/'ramsey_r55_m214_postcut_selector_fiber/check.py'
if hashlib.sha256(parent.read_bytes()).hexdigest()!='25d24c17f139d6dc9d1c1c05056808e995c0571595821c83e4c1032ab0abf1e4':raise ValueError('changed geometry source')
spec=importlib.util.spec_from_file_location('priorcheck',parent);prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
E=prior.E
def require(ok,message):
 if not ok:raise ValueError(message)

class Model:
 def __init__(self,c=12,k=0):
  self.c,self.k=c,k;self.edge,self.triangle,self.roots,self.missed,self.q=prior.geometry()
  self.active=[r for r,(key,*_) in enumerate(self.roots) if key[1:3]==(c,k)];require(278 in self.active,'root278 anchor pattern');self.active=[278]
  self.y={r:F(int(r in self.active),len(self.active)) for r in range(389)}
  self.units=self.roots[self.active[0]][3];require(all(self.roots[r][3]==self.units for r in self.active),'common anchor pattern')
  buckets=defaultdict(list)
  for v in range(43):
   key=(v,) if v<2 else (int(v in E),self.units[0,v],self.units[1,v])
   buckets[key].append(v)
  self.cells=sorted(buckets.values(),key=lambda vs:vs[0]);self.types={v:j for j,vs in enumerate(self.cells) for v in vs};self.sizes=list(map(len,self.cells))
  self.n=0;self.tables={};self.reps={};self.rows=[];self.rowset=set()
  for size in (2,3,4):
   for ts in it.combinations_with_replacement(range(len(self.cells)),size):
    counts=Counter(ts)
    if any(counts[t]>self.sizes[t] for t in counts):continue
    tally=Counter();vs=[]
    for t in ts:vs.append(self.cells[t][tally[t]]);tally[t]+=1
    vs=tuple(vs);pairs=list(it.combinations(range(size),2));self.reps[ts]=vs
    perms=[perm for perm in it.permutations(range(size)) if tuple(ts[i] for i in perm)==ts]
    transports=[[pairs.index(tuple(sorted((perm[a],perm[b])))) for a,b in pairs] for perm in perms]
    table={};orbits={}
    for mask in range(1<<len(pairs)):
     if any((vs[a],vs[b]) in self.units and (mask>>j&1)!=self.units[vs[a],vs[b]] for j,(a,b) in enumerate(pairs)):continue
     orbit=min(sum((mask>>bit&1)<<j for j,bit in enumerate(bits)) for bits in transports)
     if orbit not in orbits:orbits[orbit]=self.n;self.n+=1
     table[mask]=orbits[orbit]
    self.tables[ts]=table
    self.add(Counter(table.values()),'=',1)
  # Every local marginal, including different placements inside a cell.
  for ts,table in self.tables.items():
   size=len(ts)
   if size==2:continue
   pairs=list(it.combinations(range(size),2))
   for pos in it.combinations(range(size),size-1):
    target=tuple(ts[i] for i in pos);sub=self.tables[target];bits=[pairs.index(p) for p in it.combinations(pos,2)]
    for state in range(1<<len(bits)):
     row=Counter(table[m] for m in table if sum((m>>b&1)<<j for j,b in enumerate(bits))==state)
     if state in sub:row[sub[state]]-=1
     self.add(row,'=',0)
  self.coords={}
  for pair,index in self.edge.items():self.coords[index]=self.event(pair,red=[pair])
  for vs,index in self.triangle.items():self.coords[index]=self.event(vs,red=list(it.combinations(vs,2)))
  for (a,b,h),index in self.missed.items():self.coords[index]=self.event((a,b,h),blue=[(a,h),(b,h)])
  for (a,b,i,j),index in self.q.items():self.coords[index]=self.event((a,b,i,j),red=[(i,j)],blue=[(a,i),(b,i),(a,j),(b,j)])
 def add(self,row,rel,rhs):
  key=(tuple(sorted((i,int(v)) for i,v in row.items() if v)),rel,F(rhs))
  if not key[0]:
   require(0==rhs if rel=='=' else 0>=rhs,'constant contradiction '+str(rhs))
   return
  if key not in self.rowset:self.rowset.add(key);self.rows.append(key)
 def event(self,vs,red=(),blue=()):
  order=sorted(vs,key=lambda v:(self.types[v],v));ts=tuple(self.types[v] for v in order);pairs=list(it.combinations(range(len(order)),2))
  def bit(e):return pairs.index(tuple(sorted(order.index(v) for v in e)))
  rr=[bit(e) for e in red];bb=[bit(e) for e in blue]
  return Counter(index for mask,index in self.tables[ts].items() if all(mask>>j&1 for j in rr) and not any(mask>>j&1 for j in bb))
 def addparts(self,parts,rel,rhs):
  row=Counter()
  for c,expr in parts:
   for i,a in expr.items():row[i]+=c*a
  self.add(row,rel,rhs)
 def initial(self):
  for cell in self.cells:
   h=cell[0];others=[v for v in range(43) if v!=h];degree=20 if h in E else 21
   self.addparts([(1,self.coords[self.edge[tuple(sorted((h,v)))]] ) for v in others],'=',degree)
   self.addparts([(1,self.coords[self.triangle[tuple(sorted((h,a,b)))]] ) for a,b in it.combinations(others,2)],'=',93 if h in E else 100)
   self.addparts([(1,self.coords[self.edge[tuple(sorted((h,v)))]] ) for v in E if v!=h],'>=',6)
   for ts,vs in self.reps.items():
    if len(ts)!=2 or self.types[h] not in ts:continue
    a=next((v for v in vs if v!=h),None)
    if a is None:continue
    for color in (0,1):
     parts=[(1,self.event((h,a,b),**{'red' if color else 'blue':[(h,a),(h,b)]})) for b in others if b!=a]
     parts.append((-(degree-1 if color else 41-degree),self.event((h,a),**{'red' if color else 'blue':[(h,a)]})))
     self.addparts(parts,'=',0)
  for ts,vs in self.reps.items():
   if len(ts)!=2:continue
   a,b=vs
   for color in (0,1):
    parts=[(1,self.event((a,b,h),**{'red' if color else 'blue':list(it.combinations((a,b,h),2))})) for h in range(43) if h not in (a,b)]
    parts.append((-13,self.event((a,b),**{'red' if color else 'blue':[(a,b)]})))
    self.addparts([(-c,e) for c,e in parts],'>=',0)
  # All five-set clauses, quotienting only this candidate's cell symmetry.
  for ts in it.combinations_with_replacement(range(len(self.cells)),5):
   counts=Counter(ts)
   if any(counts[t]>self.sizes[t] for t in counts):continue
   tally=Counter();vs=[]
   for t in ts:vs.append(self.cells[t][tally[t]]);tally[t]+=1
   parts=[(1,self.coords[self.edge[tuple(sorted(pair))]]) for pair in it.combinations(vs,2)]
   self.addparts(parts,'>=',1);self.addparts([(-c,e) for c,e in parts],'>=',-9)
 def base(self,path):
  start=time.time()
  with path.open() as f:
   next(f)
   for num,line in enumerate(f,1):
    fields=line.split();rhs=F(fields[-2]);parts=[]
    for j in range(0,len(fields)-3,2):
     c=int(fields[j]);idx=int(fields[j+1][1:])
     if 13245<=idx<=13633:rhs-=c*self.y[idx-13245]
     else:parts.append((c,self.coords[idx]))
    self.addparts(parts,fields[-3],rhs)
    if num%500000==0:print('base',num,'unique',len(self.rows),'sec',round(time.time()-start,1),flush=True)
 def write(self,path):
  with path.open('w') as f:
   f.write('Minimize\n obj: 0 p0\nSubject To\n')
   for n,(row,rel,rhs) in enumerate(self.rows):f.write(' r'+str(n)+': '+ ' '.join(f'{c:+d} p{i}' for i,c in row)+f' {rel} {rhs}\n')
   f.write('Bounds\n');f.writelines(f' 0 <= p{i} <= 1\n' for i in range(self.n));f.write('End\n')
  print('LP',self.n,len(self.rows),'templates',len(self.tables),'cells',self.cells,'active',self.active,flush=True)
 def read(self,path):
  values=[F(0)]*self.n;seen=set()
  for line in path.read_text().splitlines():
   if line.startswith('p'):
    name,v=line.split();index=int(name[1:]);require(0<=index<self.n and index not in seen,'solution coordinate');seen.add(index);values[index]=F(v)
  require(seen and min(values)>=0 and max(values)<=1,'exact solution bounds')
  for i,(row,rel,rhs) in enumerate(self.rows):
   val=sum(c*values[j] for j,c in row)
   require(val==rhs if rel=='=' else val>=rhs,'exact discovery row '+str(i))
  return values
 def certificate(self,values,path):
  D=math.lcm(*(v.denominator for v in values));tables=[];pairs=list(it.combinations(range(4),2))
  for ts,table in self.tables.items():
   if len(ts)!=4:continue
   perms=[perm for perm in it.permutations(range(4)) if tuple(ts[j] for j in perm)==ts];orbits={}
   for mask,idx in table.items():
    if not values[idx]:continue
    canonical=min(sum((mask>>pairs.index(tuple(sorted((perm[a],perm[b]))))&1)<<j for j,(a,b) in enumerate(pairs)) for perm in perms)
    mass=int(values[idx]*D)
    require(canonical not in orbits or orbits[canonical]==mass,'state orbit invariance');orbits[canonical]=mass
   tables.append({'types':ts,'orbits':{str(k):v for k,v in sorted(orbits.items())}})
  path.write_text(json.dumps({'denominator':D,'cells':self.cells,'active_selectors':self.active,'four_tables':tables,'format':'class-state-orbits-v1'},separators=(',',':'))+'\n')
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--c',type=int,default=12);p.add_argument('--k',type=int,default=0);p.add_argument('--base',type=Path);p.add_argument('--lp',type=Path);p.add_argument('--solution',type=Path);p.add_argument('--certificate',type=Path);a=p.parse_args()
 require(a.lp is not None or (a.solution is not None and a.certificate is not None),'request an LP or solution conversion')
 m=Model(a.c,a.k);m.initial()
 if a.base:m.base(a.base)
 if a.lp:m.write(a.lp)
 if a.solution:m.certificate(m.read(a.solution),a.certificate)
