#!/usr/bin/env python3
"""Small deletion-free reverse-unit-propagation checker; no solver imports."""
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def rup(clauses,clause):
    assignment={}
    for literal in clause:
        variable=abs(literal);value=literal<0
        if variable in assignment and assignment[variable]!=value:return True
        assignment[variable]=value
    while True:
        changed=False
        for row in clauses:
            free=[];satisfied=False
            for literal in row:
                value=assignment.get(abs(literal))
                if value is None:free.append(literal)
                elif value==(literal>0):satisfied=True;break
            if satisfied:continue
            if not free:return True
            if len(free)==1:
                literal=free[0];assignment[abs(literal)]=literal>0;changed=True
        if not changed:return False


def verify(clauses,path,variables):
    rows=[tuple(row) for row in clauses];count=0;closed=False
    for line in Path(path).read_text(encoding='ascii').splitlines():
        require(not closed,'proof after empty clause')
        fields=line.split();require(fields and fields[-1]=='0','proof row syntax')
        row=tuple(map(int,fields[:-1]));require(all(1<=abs(x)<=variables for x in row),'proof variable range')
        require(len(set(row))==len(row),'duplicate literal')
        require(rup(rows,row),f'non-RUP proof row {count+1}')
        rows.append(row);count+=1;closed=not row
    require(closed,'missing terminal empty clause')
    return count
