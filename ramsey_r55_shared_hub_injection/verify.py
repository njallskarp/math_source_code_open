"""Independent literal verifier: no extractor, Ramsey fact, or catalogue import."""
import json
import sys


def verify(data, certificate):
    if not isinstance(data, dict) or not isinstance(data.get('rows'), list):
        raise ValueError('Missing matrix')
    matrix = data['rows']
    if len(matrix) != 43:
        raise ValueError('Wrong order')
    for i, row in enumerate(matrix):
        if not isinstance(row, str) or len(row) != 43:
            raise ValueError('Wrong row')
        for j, entry in enumerate(row):
            if entry not in '01' or (i == j and entry != '0'):
                raise ValueError('Bad matrix entry')
    for i in range(43):
        for j in range(43):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError('Not symmetric')
    if not isinstance(certificate, dict) or set(certificate) != {'color', 'vertices'}:
        raise ValueError('Bad certificate schema')
    color, vs = certificate['color'], certificate['vertices']
    if type(color) is not int or color not in (0, 1):
        raise ValueError('Bad color')
    if not isinstance(vs, list) or len(vs) != 5 or any(type(v) is not int or not 0 <= v < 43 for v in vs) or len(set(vs)) != 5:
        raise ValueError('Expected five distinct physical vertices')
    for i in range(5):
        for j in range(i):
            if matrix[vs[i]][vs[j]] != str(color):
                raise ValueError('Five-set is not monochromatic')
    return 'VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE'


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python3 -B verify.py graph.json certificate.json')
    try:
        with open(sys.argv[1], encoding='utf-8') as stream:
            data = json.load(stream)
        with open(sys.argv[2], encoding='utf-8') as stream:
            cert = json.load(stream)
        print(verify(data, cert))
    except ValueError as error:
        raise SystemExit(str(error))
