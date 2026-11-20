"""Reproducible floating-point screen of the unchanged Lantern's 0/1 join.

This is a numerical localization tool, not the interval proof. It never edits
the original recipe. All coordinates use the unit-octagon convention.
This publication version writes only the small JSON summary, not point clouds
or render-support arrays. It can require several hundred MB of working memory.
"""
from pathlib import Path
import hashlib
import json
import sys
import time

import numpy as np
from scipy.spatial import cKDTree

STUDY = Path(__file__).resolve().parents[1]
MATH = STUDY.parents[1] / "math"
sys.path.insert(0, str(MATH))
from model import R, Q, T, V, points, word_map  # noqa: E402

NORMAL = np.array([1., -1., 0.]) / np.sqrt(2.)
RADIAL = np.array([1., 1., 0.]) / np.sqrt(2.)
BALL_RADIUS = 1.35
DATA = STUDY / "data"


def centers(depth):
    p = np.zeros((1, 3))
    for _ in range(depth):
        p = np.concatenate([R * p @ qi.T + ti for qi, ti in zip(Q, T)])
    return p


def in_a(p):
    return R * p @ Q[0].T + T[0]


def reflect(p):
    return p[..., [1, 0, 2]]


def addr(index, depth):
    return "0" + format(int(index), "o").zfill(depth)


def main():
    start = time.monotonic()
    DATA.mkdir(exist_ok=True)
    c, q, s = word_map("04")
    vertices04 = c + s * V @ q.T
    witness = vertices04[5]
    focus = c - (c @ NORMAL) * NORMAL
    z_section = float(witness[2])
    rows = []
    covers = []

    for depth in (4, 5, 6, 7):
        a = in_a(points(depth))
        b = reflect(a)
        tree = cKDTree(b)
        error = (BALL_RADIUS + 1.) * R ** (depth + 1)
        vd, _ = tree.query(vertices04, workers=-1)
        signed = a @ NORMAL
        indices = np.flatnonzero(signed < 0.)
        d, _ = tree.query(a[indices], workers=-1)
        best = int(np.argmax(d))
        j = int(indices[best])
        rows.append({
            "child_depth": depth, "total_word_depth": depth + 1,
            "sample_count_per_piece": len(a),
            "sample_hausdorff_error_bound": float(error),
            "f04_vertices_nearest_B_samples": vd.tolist(),
            "witness_nearest_B_sample": float(vd[5]),
            "witness_distance_lower_screen": float(vd[5] - error),
            "A_wrong_halfspace_sample_fraction": float(len(indices) / len(a)),
            "furthest_wrong_side_sample": {
                "word": addr(j, depth), "seed_vertex": 0,
                "point": a[j].tolist(), "signed_plane_distance": float(signed[j]),
                "nearest_B_sample": float(d[best]),
                "distance_to_B_lower_screen": float(d[best] - error),
            },
        })

        ac = in_a(centers(depth))
        bc = reflect(ac)
        rad = BALL_RADIUS * R ** (depth + 1)
        dc, _ = cKDTree(bc).query(ac, workers=-1)
        keep = dc <= 2 * rad + 1e-11
        candidate = ac[keep]
        covers.append({
            "total_word_depth": depth + 1,
            "ball_radius": float(rad),
            "candidate_A_ball_count": int(keep.sum()),
            "total_A_ball_count": len(ac),
            "max_possible_abs_signed_plane_distance": float(np.max(np.abs(candidate @ NORMAL)) + rad),
            "candidate_cover_bounds_lower": (candidate.min(0) - rad).tolist(),
            "candidate_cover_bounds_upper": (candidate.max(0) + rad).tolist(),
        })
        print(json.dumps({"depth": depth + 1,
                          "witness_gap_lower_screen": float(vd[5] - error),
                          "possible_contact_balls": int(keep.sum())}), flush=True)

    error = (BALL_RADIUS + 1.) * R ** 8
    screen = {
        "purpose": "Numerical localization only; see the separate interval certificate for proof.",
        "original_reference_sha256": hashlib.sha256((MATH / "data/reference.json").read_bytes()).hexdigest(),
        "coordinates": "Unit octagon radius; original display normalization not applied.",
        "piece_A": "f0(K)", "piece_B": "f1(K)",
        "mirror": "S(x,y,z)=(y,x,z)",
        "plane": "x=y", "normal": NORMAL.tolist(),
        "focus": focus.tolist(), "f04_center": c.tolist(),
        "f04_enclosing_radius": float(BALL_RADIUS * s),
        "witness": {"address": "f04(v5)", "point": witness.tolist(),
                    "signed_plane_distance": float(witness @ NORMAL)},
        "sample_convergence": rows,
        "possible_contact_outer_screens": covers,
        "render_support_arrays_included": False,
        "original_visual_section_specification": {"z": z_section,
                    "u_definition": "(x+y)/sqrt(2)",
                    "w_definition": "(x-y)/sqrt(2)",
                    "u_range": [0.36, 1.0],
                    "w_range": [-0.24, 0.24],
                    "sampling_error": float(error),
                    "interpretation": "Distance-to-sample maps. Infinite-set distance is between max(0,d-error) and d; finite thickness masks are envelopes, not proofs of fractal intersection."},
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    (DATA / "overlap-screen.json").write_text(json.dumps(screen, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
