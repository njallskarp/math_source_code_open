"""Corruption tests at the graph and forcing-certificate trust boundaries."""
from copy import deepcopy
import json
import verify


def rejects(fn):
    try:
        fn()
    except (ValueError,TypeError,IndexError):
        return
    raise RuntimeError('corruption was accepted')


def main():
    data=json.loads((verify.HERE/'WITNESS.json').read_text())
    red=verify.construct(data)
    damaged=red-{(0,3)}
    rejects(lambda:verify.audit(damaged,data))
    malformed=deepcopy(data)
    malformed['cross_rows'][0]='2'+malformed['cross_rows'][0][1:]
    rejects(lambda:verify.construct(malformed))
    wrong_hole=deepcopy(data)
    wrong_hole['forced_diagonal_edge']=[5,26]
    rejects(lambda:verify.audit(red,wrong_hole))
    wrong_set=deepcopy(data)
    wrong_set['red_five_minus_edge']=[5,25,28,34,40]
    rejects(lambda:verify.audit(red,wrong_set))
    rejects(lambda:verify.decode_graph6('fg=='))
    print('PASS rejected missing root edge and nonbinary incidence')
    print('PASS rejected incorrect forcing hole and incorrect forcing five-set')
    print('PASS rejected truncated graph6')


if __name__=='__main__':
    main()
