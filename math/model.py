"""Floating-point access to the unchanged L3-30 display export.

Mathematical coordinates have unit octagon radius. Display normalization is
explicit and never used by the rigorous interval verifier.
"""
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parent
REFERENCE = json.loads((ROOT/'data/reference.json').read_text(encoding='utf-8-sig'))
FACTOR = float(REFERENCE['normalization'])
R = float(REFERENCE['r'])
Q = np.array(REFERENCE['Q'])
T = np.array(REFERENCE['T']) / FACTOR
V = np.array(REFERENCE['vertices']) / FACTOR


def word_map(word):
    q, c, s = np.eye(3), np.zeros(3), 1.
    for digit in word:
        i = int(digit)
        if i < 0 or i > 7:
            raise ValueError('Addresses use digits 0 through 7')
        c += s*q@T[i]
        q = q@Q[i]
        s *= R
    return c, q, s


def points(depth):
    """8**depth actual attractor points, starting at retained vertex v0.

    Float arithmetic approximates their exact locations. The Hausdorff error
    is at most (27/20 + 1)*r**depth in the unit-octagon coordinates.
    """
    if depth < 0:
        raise ValueError('Depth must be nonnegative')
    p = V[:1].copy()
    for _ in range(depth):
        p = np.concatenate([R*p@qi.T+ti for qi, ti in zip(Q, T)])
    return p
