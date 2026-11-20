"""Certify a local opposite-halfspace join for the unchanged L3-30 Lantern.

Run from any directory. Reads the original exact radical implementation;
writes only this study's data/interface-certificate.json. No original model,
reference export, render or publication file is changed.

Interval inequalities establish numerical premises. Analytic conclusions
(symmetry, retained vertices, attractor uniqueness and dimension monotonicity)
are explained in ../MATH.md. This is not proof-assistant formalization.
"""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

import mpmath as mp

STUDY = Path(__file__).resolve().parents[1]
REPOSITORY = STUDY.parents[1]
ORIGINAL_MATH = REPOSITORY / 'math'
spec = importlib.util.spec_from_file_location('lantern_original_exact', ORIGINAL_MATH / 'exact.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)
e.iv.dps = 60


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def signed(x):
    """Unit signed distance to x=y; positive on A's nominal side."""
    return (x[0] - x[1]) / e.sqrt2


def vector_diagnostic(x):
    return [e.diagnostic(a) for a in x]


def exclusion_cover(p, root, gap, max_depth=10):
    """Build and then recheck a complete rigorous ball cover of f_root(K)."""
    leaves, pending = [], [str(root)]
    while pending:
        w = pending.pop()
        c, _, scale = e.word(w)
        margin = e.norm2(e.sub(p, c)) - (scale * e.radius + gap) ** 2
        if bool(margin > e.ZERO):
            leaves.append(w)
        else:
            e.require(len(w) < max_depth, 'Cover depth limit reached at ' + w)
            pending.extend(w + str(j) for j in reversed(range(8)))
    leaves.sort()
    # Stripping root leaves a complete partition of this copy's address space.
    e.complete_prefixes([tuple(map(int, w[1:])) for w in leaves], 8)
    margins = []
    for w in leaves:
        e.require(w[0] == str(root), 'Wrong cover root')
        c, _, scale = e.word(w)
        margin = e.norm2(e.sub(p, c)) - (scale * e.radius + gap) ** 2
        e.gt(margin, e.ZERO)
        margins.append(float(margin.a))
    return dict(root=str(root), leaves=leaves, leaf_count=len(leaves),
                maximum_depth=max(map(len, leaves)),
                minimum_squared_margin_diagnostic=min(margins))


def main():
    original_paths = [ORIGINAL_MATH / p for p in
                      ('exact.py', 'model.py', 'data/reference.json', 'data/covers.json')]
    original_hashes = {p.relative_to(REPOSITORY).as_posix(): sha256(p) for p in original_paths}
    e.gt(e.r, e.ZERO)
    e.gt(e.ONE, e.r)
    e.gt(e.radius, e.ONE)
    invariant_margins = [e.radius - e.norm(t) - e.r * e.radius for t in e.ts]
    for margin in invariant_margins:
        e.gt(margin, e.ZERO)

    # Implementation checks only; exactness follows from chord-frame algebra.
    for j in range(8):
        for residual in e.sub(e.point(str(j), j), e.vertices[j]):
            e.contains_zero(residual)
    h = [[e.sqrt2/2, e.sqrt2/2, e.ZERO],
         [e.sqrt2/2, -e.sqrt2/2, e.ZERO], [e.ZERO, e.ZERO, e.ONE]]
    hin = e.mm(e.gp[2], h)
    lhs, rhs = e.mm(h, e.q0), e.mm(e.q0, hin)
    for row_a, row_b in zip(lhs, rhs):
        for a, b in zip(row_a, row_b):
            e.contains_zero(a-b)
    for residual in e.sub(e.mv(h, e.t0), e.t0):
        e.contains_zero(residual)
    swap = [[e.ZERO, e.ONE, e.ZERO], [e.ONE, e.ZERO, e.ZERO],
            [e.ZERO, e.ZERO, e.ONE]]
    for row_a, row_b in zip(e.mm(e.gp[1], h), swap):
        for a, b in zip(row_a, row_b):
            e.contains_zero(a-b)

    # An exact attractor point on the side removed from A.
    p = e.point('04', 5)
    ell = signed(p)
    e.gt(-ell, e.I(7)/50)  # > 0.14 below the plane
    gap = e.I(3)/50      # > 0.06 from every other first-level piece
    covers = [exclusion_cover(p, j, gap) for j in range(1, 8)]
    print('PASS: p=f_04(v5) lies below plane and >0.06 from all other root pieces', flush=True)

    # A complete copy remains intact in the retained side of A.
    retained_word = '00'
    c, _, scale = e.word(retained_word)
    retained_margin = signed(c) - scale * e.radius
    e.gt(retained_margin, e.I(9)/25)  # > 0.36
    print('PASS: all of f_00(K) remains >0.36 inside A retained halfspace', flush=True)

    # f_5 fixes v5. Every point of f_04555(K) lies within
    # r^5 (27/20 + |v5|) of p = f_04(v5), so a WHOLE copy is removed.
    removed_word = '04555'
    removed_radius = e.r ** len(removed_word) * (e.radius + e.ONE)
    e.gt(e.I(3)/100, removed_radius)
    e.gt(-ell - removed_radius, e.I(11)/100)
    e.gt(gap - removed_radius, e.I(3)/100)
    # Also check the composition/fixed-point relation numerically by intervals.
    for residual in e.sub(e.point(removed_word, 5), p):
        e.contains_zero(residual)
    print('PASS: entire f_04555(K) is removed; >0.03 from every other root piece', flush=True)

    # Existing connected-crossing argument, reproduced for the local seam.
    q = e.point('04', 1)
    e.gt(signed(q), e.I(9)/50)
    c04, _, s04 = e.word('04')
    crossing_join_margin = e.norm2(e.sub(c04, e.vertices[1])) - (s04*e.radius + e.I(9)/50)**2
    e.gt(crossing_join_margin, e.ZERO)
    print('PASS: connected f_04(K) crosses common seam >0.18 from planned join v1', flush=True)

    for path in original_paths:
        e.require(sha256(path) == original_hashes[path.relative_to(REPOSITORY).as_posix()],
                  'An original input changed during this run')

    receipt = dict(
        status='passed', recipe='L3-30, unchanged',
        created_utc=datetime.now(timezone.utc).isoformat(),
        python=platform.python_version(), mpmath=mp.__version__,
        interval_precision_decimal_digits=e.iv.dps,
        units='unit circumradius of retained regular octagon; before display normalization',
        diagnostics_warning='Float endpoints are readable diagnostics, not certified decimal bounds. Rational bounds and interval checks carry the certificate.',
        original_inputs_sha256=original_hashes,
        verifier_sha256=sha256(Path(__file__)),
        invariant_ball=dict(radius='27/20',
                            minimum_margin_diagnostic=min(float(x.a) for x in invariant_margins)),
        construction=dict(A='f_0(K)', B='f_1(K)', plane='x=y',
                          signed_distance='ell(x,y,z)=(x-y)/sqrt(2)',
                          A_kept='A intersect {ell >= 0}', B_kept='B intersect {ell <= 0}',
                          full_variant='C=(A intersect H+) union (B intersect H-) union f_2(K) union ... union f_7(K)'),
        removed_witness=dict(word='04', vertex=5,
                             coordinates_diagnostic=vector_diagnostic(p),
                             signed_distance_diagnostic=e.diagnostic(ell),
                             signed_distance_strict_upper_bound='-7/50',
                             distance_from_each_other_root_piece_strict_lower_bound='3/50',
                             complete_exclusion_covers=covers),
        retained_whole_copy=dict(word=retained_word,
                                 centre_diagnostic=vector_diagnostic(c),
                                 radius_diagnostic=e.diagnostic(scale*e.radius),
                                 minimum_signed_distance_strict_lower_bound='9/25',
                                 plane_margin_diagnostic=e.diagnostic(retained_margin)),
        removed_whole_copy=dict(word=removed_word, centre_witness='f_04(v5)',
                                radius_about_witness_formula='(47/20)*(sqrt(2)-1)^5',
                                radius_about_witness_diagnostic=e.diagnostic(removed_radius),
                                radius_strict_upper_bound='3/100',
                                signed_distance_strict_upper_bound='-11/100',
                                distance_from_each_other_root_piece_strict_lower_bound='3/100'),
        genuine_seam_crossing=dict(word='04', negative_vertex=5, positive_vertex=1,
                                   positive_signed_distance_diagnostic=e.diagnostic(signed(q)),
                                   distance_from_v1_strict_lower_bound='9/50',
                                   squared_margin_diagnostic=e.diagnostic(crossing_join_margin)),
        analytic_conclusions=[
            'S(x,y,z)=(y,x,z) exchanges A and B, so A intersect P = B intersect P.',
            'The clipped pair meets exactly at A intersect P and is disjoint away from P.',
            'The full variant C is a proper subset of K, so cannot satisfy the original eight-map fixed-point equation.',
            'Both C and the clipped pair contain f_00(K), hence have the same Hausdorff dimension as K.',
            'K minus C contains f_04555(K), so removed geometry also contains an exact whole Lantern copy.',
            'No claim is made that C lacks some other IFS, that its seam is smooth, or that clipping preserves connectedness.'
        ])
    target = STUDY / 'data' / 'interface-certificate.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print('WROTE:', target, flush=True)


if __name__ == '__main__':
    main()
