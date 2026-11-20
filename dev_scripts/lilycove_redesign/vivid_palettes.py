#!/usr/bin/env python3
"""Boosts saturation/brightness of the outdoor palettes used by Lilycove and Route 121.
Idempotent: reads the untouched copies in base_tileset/pal_*/ and rewrites the repo palettes.
Usage: vivid_palettes.py [saturation=1.22] [value=1.04]"""
import os, sys, colorsys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
SAT = float(sys.argv[1]) if len(sys.argv) > 1 else 1.22
VAL = float(sys.argv[2]) if len(sys.argv) > 2 else 1.04
JOBS = [('pal_general', 'data/tilesets/primary/general/palettes'),
        ('pal_lilycove', 'data/tilesets/secondary/lilycove/palettes')]
def q(v): return max(0, min(248, int(round(v / 8.0)) * 8))
for src, dst in JOBS:
    for f in sorted(glob.glob(os.path.join(HERE, 'base_tileset', src, '*.pal'))):
        lines = open(f).read().split('\n')
        out = lines[:3]
        for l in lines[3:19]:
            r, g, b = (int(x) / 255 for x in l.split())
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            if s > 0.08:                      # leave greys/whites alone
                s = min(1.0, s * SAT); v = min(1.0, v * VAL)
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            out.append('%d %d %d' % (q(r * 255), q(g * 255), q(b * 255)))
        with open(os.path.join(REPO, dst, os.path.basename(f)), 'w', newline='\r\n') as o:
            o.write('\n'.join(out) + '\n')
print('palettes updated (sat x%.2f, val x%.2f)' % (SAT, VAL))
