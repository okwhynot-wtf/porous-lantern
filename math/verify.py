"""Verify the fixed Lantern's finite interval certificate and recipe export.

Run from any directory: python /path/to/repository/math/verify.py
The analytic implications of these finite inequalities are in docs/results.md.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import mpmath as mp
from exact import (ROOT, I, ONE, ZERO, iv, r, radius, sqrt2, qs, ts, q0, t0,
                   gp, vertices, add, sub, mul, mv, mm, tr, norm, norm2, cross,
                   word, point, gt, require, contains_zero, complete_prefixes,
                   diagnostic, ident)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, default=ROOT/'data/verification.json')
    args = parser.parse_args()
    data = json.loads((ROOT/'data/covers.json').read_text(encoding='utf-8'))
    reference = json.loads((ROOT/'data/reference.json').read_text(encoding='utf-8-sig'))
    require(reference['id'] == 'L3-30' and reference['family'] == 'lantern', 'Wrong recipe')
    require((reference['height'], reference['chord'], reference['twist']) == (0, 3, 30),
            'Reference parameters changed')
    require(len(data['passages']) == 7 and {x['word'] for x in data['passages']} ==
            {'', '0', '00', '01', '02', '05', '000'}, 'Required passage certificates missing')
    require(len(data['separations']) == 3 and {x['separation'] for x in data['separations']} ==
            {2, 3, 4}, 'Required separation certificates missing')
    require(len(data['intrusions']) == 4 and {x['axis_word'] for x in data['intrusions']} ==
            {'03', '04', '06', '07'}, 'Required intrusion certificates missing')

    gt(ONE, r)
    gt(r, ZERO)
    gt(ONE, 8*r**3)
    margins = [radius-norm(t)-r*radius for t in ts]
    for margin in margins:
        gt(margin, ZERO)
    gt(radius, ONE)

    # Independent radical construction versus the original decimal export.
    # This is a float compatibility check; it is not an exact-identity proof.
    errors = [abs(float(r.a)-reference['r']), abs(float(r.b)-reference['r'])]
    factor = reference['normalization']
    require(factor > 0, 'Invalid display normalization')
    require(len(reference['Q']) == len(reference['T']) == len(reference['vertices']) == 8,
            'Wrong number of display maps or vertices')
    for k in range(8):
        for i in range(3):
            for j in range(3):
                exact = qs[k][i][j]
                displayed = reference['Q'][k][i][j]
                errors.extend(abs(float(x)-displayed) for x in (exact.a, exact.b))
            for exact, displayed in ((ts[k][i], reference['T'][k][i]/factor),
                                     (vertices[k][i], reference['vertices'][k][i]/factor)):
                errors.extend(abs(float(x)-displayed) for x in (exact.a, exact.b))
    require(max(errors) < 1e-13, 'Display recipe differs from the radical construction')

    # Residuals support implementation review. Their exact identities follow
    # analytically from orthonormal frames and endpoint alignment.
    for k in range(8):
        orthogonal = mm(qs[k], tr(qs[k]))
        for i in range(3):
            for j in range(3):
                contains_zero(orthogonal[i][j]-I(int(i == j)))
        for target, source in ((k, k), ((k+1) % 8, (k+3) % 8)):
            for residual in sub(point(str(k), source), vertices[target]):
                contains_zero(residual)
    nonplanar_witness = point('0', 1)
    gt(-nonplanar_witness[2], I(1)/100)

    h = [[sqrt2/2, sqrt2/2, ZERO], [sqrt2/2, -sqrt2/2, ZERO], [ZERO, ZERO, ONE]]
    hin = mm(gp[2], h)
    lhs, rhs = mm(h, q0), mm(q0, hin)
    for i in range(3):
        for j in range(3):
            contains_zero(lhs[i][j]-rhs[i][j])
    for residual in sub(mv(h, t0), t0):
        contains_zero(residual)

    passages = []
    for entry in data['passages']:
        w = entry['word']
        origin, q, s = word(w)
        direction = [row[2] for row in q]
        delta = I(11)/50*r**len(w)
        complete_prefixes([tuple(map(int, x)) for x in entry['leaves']], 8)
        margins = []
        for p in entry['leaves']:
            c, _, scale = word(p)
            margin = norm2(cross(sub(c, origin), direction))-(scale*radius+delta)**2
            gt(margin, ZERO)
            margins.append(float(margin.a))
        passages.append(dict(word=w or 'root', radius_formula='(11/50)*(sqrt(2)-1)^'+str(len(w)),
                             radius_diagnostic=diagnostic(delta), cover_leaves=len(entry['leaves']),
                             maximum_cover_depth=max(map(len, entry['leaves'])),
                             minimum_squared_margin_diagnostic=min(margins)))
        print('PASS: whole-attractor tube', w or 'root', flush=True)

    separations = []
    for entry in data['separations']:
        sep = entry['separation']
        suffixes = []
        for aa, bb in entry['leaves']:
            require(aa and bb and aa[0] == '0' and bb[0] == str(sep) and len(aa) == len(bb),
                    'Wrong pair cover')
            suffixes.append(tuple(8*int(i)+int(j) for i, j in zip(aa[1:], bb[1:])))
        complete_prefixes(suffixes, 64)
        margins = []
        for aa, bb in entry['leaves']:
            ca, _, sa = word(aa)
            cb, _, sb = word(bb)
            margin = norm2(sub(ca, cb))-((sa+sb)*radius+I(1)/100)**2
            gt(margin, ZERO)
            margins.append(float(margin.a))
        separations.append(dict(separation=sep, gap_lower_bound='1/100',
                                cover_leaves=len(suffixes),
                                minimum_squared_margin_diagnostic=min(margins)))
        print('PASS: non-neighbour separation', sep, flush=True)

    c, q, s = word('04')
    xm, xp = point('04', 5), point('04', 1)
    sm, sp = (xm[0]-xm[1])/sqrt2, (xp[0]-xp[1])/sqrt2
    gt(-sm, I(14)/100)
    gt(sp, I(18)/100)
    join_margin = norm2(sub(c, vertices[1]))-(s*radius+I(18)/100)**2
    gt(join_margin, ZERO)
    crossing = dict(word='04', negative_vertex=5, positive_vertex=1,
                    negative_signed_distance_diagnostic=diagnostic(sm),
                    positive_signed_distance_diagnostic=diagnostic(sp),
                    distance_from_prescribed_join_lower_bound='18/100',
                    squared_join_margin_diagnostic=diagnostic(join_margin))
    print('PASS: additional adjacent contact via connected mirror-plane crossing', flush=True)

    intrusions = []
    for witness in data['intrusions']:
        require(witness['point_word'][0] != witness['axis_word'][0], 'Witness is not from another root piece')
        origin, q, s = word(witness['axis_word'])
        direction = [row[2] for row in q]
        p = point(witness['point_word'], witness['vertex'])
        delta = I(11)/50*s
        distance2 = norm2(cross(sub(p, origin), direction))
        gt(delta**2, distance2)
        intrusions.append(dict(**witness, distance_diagnostic=diagnostic(iv.sqrt(distance2)),
                               nominal_radius_diagnostic=diagnostic(delta)))
    print('PASS: four explicit points inside nominal descendant tubes', flush=True)

    # The connected set contains a unit-octagon edge's endpoints, giving dim>=1;
    # the standard similarity-cover argument gives the upper bound below.
    exponent = iv.ln(I(8))/iv.ln(ONE/r)
    tracked = ['exact.py', 'verify.py', 'data/reference.json', 'data/covers.json']
    receipt = dict(recipe='L3-30', status='passed', precision_decimal_digits=iv.dps,
                   python=platform.python_version(), mpmath=mp.__version__,
                   units='unit circumradius of the retained regular octagon',
                   invariant_ball_radius='27/20',
                   invariant_ball_margin_diagnostic=min(float((radius-norm(t)-r*radius).a) for t in ts),
                   nonplanar_witness=dict(word='0', vertex=1, z_diagnostic=diagnostic(nonplanar_witness[2])),
                   volume_cover_ratio_diagnostic=diagnostic(8*r**3),
                   Hausdorff_dimension_lower_bound=1,
                   Hausdorff_dimension_upper_bound_formula='log(8)/log(1+sqrt(2))',
                   Hausdorff_dimension_upper_bound_diagnostic=diagnostic(exponent),
                   passages=passages, separated_pairs=separations, additional_contact=crossing,
                   nominal_tube_intrusions=intrusions,
                   maximum_display_export_error=max(errors),
                   inputs_sha256={name: digest(ROOT/name) for name in tracked},
                   scope='Finite interval inequalities and complete covers checked. The analytic connectedness, symmetry, contact and winding arguments are in docs/results.md. Diagnostic decimal floats are not interval endpoints. Not proof-assistant verification or independent peer review.')
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print('Receipt:', args.receipt)


if __name__ == '__main__':
    main()
