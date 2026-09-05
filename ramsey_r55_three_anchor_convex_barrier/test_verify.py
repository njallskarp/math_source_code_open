"""Small decoding controls and rejection of malformed primal inputs."""
import base64
from copy import deepcopy
import json
from pathlib import Path
from seed import construct, graph6, require


def reject(function, argument):
    try:
        function(argument)
    except (ValueError, KeyError, TypeError):
        return
    raise RuntimeError("malformed input accepted")


require(graph6(base64.b64encode(b"B?").decode()) == (3,set()), "empty three-graph")
require(graph6(base64.b64encode(b"Bw").decode()) == (3,{(0,1),(0,2),(1,2)}), "complete three-graph")
for raw in (b"Bx", b"B", b"B\x7f"):
    reject(graph6,base64.b64encode(raw).decode())
source = json.loads((Path(__file__).resolve().parent / "SEED.json").read_text())
bad = deepcopy(source)
bad["red_core_delete_edges"][1] = bad["red_core_delete_edges"][0]
reject(construct,bad)
bad = deepcopy(source)
bad["cross_rows"][0] = "2" + bad["cross_rows"][0][1:]
reject(construct,bad)
bad = deepcopy(source)
bad["cross_rows"].pop()
reject(construct,bad)
bad = deepcopy(source)
bad["anchors"] = [0,9,3]
reject(construct,bad)
print("PASS 2 known graphs and 7 malformed-input controls")
