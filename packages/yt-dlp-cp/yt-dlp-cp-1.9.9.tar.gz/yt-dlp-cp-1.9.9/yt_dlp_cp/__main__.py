#!/usr/bin/env python3

# Execute with
# $ python -m yt_dlp_cp

import sys

if __package__ is None and not getattr(sys, 'frozen', False):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import yt_dlp_cp

if __name__ == '__main__':
    res = yt_dlp_cp.main('https://www.youtube.com/watch?v=UZaEXFISVSY')
    print('res:',res)
