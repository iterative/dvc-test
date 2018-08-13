import os
import sys
import json

assert len(sys.argv) == 2

with open(sys.argv[1], 'w+') as fd:
    d = dict(os.environ)
    if 'SHLVL' in d:
        del d['SHLVL']
    json.dump(d, fd, sort_keys=True)
