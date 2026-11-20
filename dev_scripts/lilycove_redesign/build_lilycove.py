#!/usr/bin/env python3
"""Rebuilds data/layouts/LilycoveCity/map.bin from layout.py and renders a preview.

Usage: python3 dev_scripts/lilycove_redesign/build_lilycove.py [--preview out.png]
The map is composed from stamps of the original Lilycove (lilycove_original.bin)
plus general/lilycove metatiles. Edit layout.py and re-run.
"""
import os, sys, struct
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from compose import M, W, H, REPO
exec(open(os.path.join(HERE, 'layout.py')).read())
out = os.path.join(REPO, 'data/layouts/LilycoveCity/map.bin')
open(out, 'wb').write(b''.join(struct.pack('<H', v) for r in M for v in r))
print('wrote', out, W, 'x', H)
if '--preview' in sys.argv:
    import render
    render.render(out, W, sys.argv[sys.argv.index('--preview') + 1])
