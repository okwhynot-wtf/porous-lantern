"""L3-30 reconstructed from rational constants and radicals, using intervals.

The decimal display export is not an input to this construction. See
docs/definition.md for the exact chord-frame formula.
"""
from functools import lru_cache
from pathlib import Path
import mpmath as mp

ROOT = Path(__file__).resolve().parent
iv = mp.iv
iv.dps = 60
I = iv.mpf
ZERO, ONE = I(0), I(1)


def add(a, b): return [x + y for x, y in zip(a, b)]
def sub(a, b): return [x - y for x, y in zip(a, b)]
def mul(s, a): return [s * x for x in a]
def dot(a, b): return sum((x * y for x, y in zip(a, b)), ZERO)
def norm2(a): return sum((x ** 2 for x in a), ZERO)
def norm(a): return iv.sqrt(norm2(a))
def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def tr(a): return [list(c) for c in zip(*a)]
def mm(a, b): return [[dot(row, col) for col in tr(b)] for row in a]
def mv(a, x): return [dot(row, x) for row in a]
def ident(): return [[I(int(i == j)) for j in range(3)] for i in range(3)]


def frame(d):
    x = mul(ONE/norm(d), d)
    y = cross([ZERO, ZERO, ONE], x)
    y = mul(ONE/norm(y), y)
    return tr([x, y, cross(x, y)])


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def gt(a, b):
    """True only when the interval for a lies strictly above that for b."""
    require(bool(a > b), 'Strict interval inequality failed: '+str(a)+' > '+str(b))


def contains_zero(x):
    require(bool(x.a <= 0 and x.b >= 0), 'Identity residual does not contain zero: '+str(x))


def diagnostic(x):
    # Binary floats are readable diagnostics, not certified decimal endpoints.
    return [float(x.a), float(x.b)]


sqrt2, sqrt3 = iv.sqrt(I(2)), iv.sqrt(I(3))
r = sqrt2 - 1
g = [[sqrt2/2, -sqrt2/2, ZERO], [sqrt2/2, sqrt2/2, ZERO], [ZERO, ZERO, ONE]]
gp = [ident()]
for _ in range(7):
    gp.append(mm(gp[-1], g))
vertices = [mv(p, [ONE, ZERO, ZERO]) for p in gp]
a, b, u, v = vertices[0], vertices[3], vertices[0], vertices[1]
roll = [[ONE, ZERO, ZERO], [ZERO, sqrt3/2, -ONE/2], [ZERO, ONE/2, sqrt3/2]]
q0 = mm(mm(frame(sub(v, u)), roll), tr(frame(sub(b, a))))
t0 = sub(mul(ONE/2, add(u, v)), mul(r, mv(q0, mul(ONE/2, add(a, b)))))
qs = [mm(mm(p, q0), tr(p)) for p in gp]
ts = [mv(p, t0) for p in gp]
radius = I(27)/20


@lru_cache(None)
def word(w):
    """Return c,Q,s for f_w(x)=c+s Qx; first digit is outermost."""
    require(isinstance(w, str) and set(w) <= set('01234567'), 'Invalid address')
    if not w:
        return [ZERO, ZERO, ZERO], ident(), ONE
    c, q, s = word(w[:-1])
    j = int(w[-1])
    return add(c, mul(s, mv(q, ts[j]))), mm(q, qs[j]), s*r


def point(w, vertex):
    require(0 <= vertex < 8, 'Invalid retained vertex')
    c, q, s = word(w)
    return add(c, mul(s, mv(q, vertices[vertex])))


def complete_prefixes(words, alphabet):
    """Check that finite words partition every infinite address in a trie."""
    trie = {}
    for w in words:
        node = trie
        for k in w:
            require(None not in node, 'Cover is not prefix-free')
            node = node.setdefault(k, {})
        require(not node, 'Duplicate or non-prefix-free leaf')
        node[None] = True

    def walk(node):
        if None in node:
            require(len(node) == 1, 'Leaf has descendants')
            return
        require(set(node) == set(range(alphabet)), 'Incomplete cover')
        for child in node.values():
            walk(child)
    walk(trie)
