# Porous Lantern: one-join study

This directory contains the reproducible research behind [the public join study](../../docs/joins.md). It examines a local trim of the original L3-30 Lantern's pieces 0 and 1. The preferred trimmed pair is a design direction, not a new all-eight recipe.

The reference maps remain in [`math/exact.py`](../../math/exact.py) and [`math/model.py`](../../math/model.py). All paths resolve relative to this repository, so a clean clone contains the required inputs. No neighbouring workspace folder is needed.

| File | Purpose |
| --- | --- |
| [MATH.md](MATH.md) | Exact set construction, analytic argument and proof scope. |
| [source/certify_interface.py](source/certify_interface.py) | 60-digit outward-interval verification of all finite inequalities. |
| [data/interface-certificate.json](data/interface-certificate.json) | Complete covers, rational bounds, diagnostics and hashes. |
| [OVERLAP.md](OVERLAP.md) | Numerical anatomy and finite-render interpretation. |
| [source/analyze_overlap.py](source/analyze_overlap.py) | Optional floating-point convergence and contact-localization screen. |
| [data/overlap-screen.json](data/overlap-screen.json) | Small reproducible numerical summary. |
| [source/render_join.py](source/render_join.py) | Reproduction of the study's finite pair renders. |

From the repository root:

```sh
python -m pip install -r requirements.txt
python research/join-study/source/certify_interface.py
```

The optional numerical screen additionally needs SciPy. Its largest depth uses over two million points per piece and several hundred MB of working memory; it saves only a small JSON summary:

```sh
python -m pip install -r research/join-study/requirements.txt
python research/join-study/source/analyze_overlap.py
```

The render script uses `visual-requirements.txt`. Public figures live in [`site/assets/joins`](../../site/assets/joins/); large numerical clouds are not part of this research package. The exact verifier is independent of all images, graphics libraries and floating-point screens.

The certificate combines interval-checked inequalities with the analytic argument in `MATH.md`. It is reproducible research, not proof-assistant formalization or independent peer review. Its central result is precise: the local trim removes genuine geometry and changes the whole object's original IFS equation, while preserving complete smaller Lanterns and the original Hausdorff dimension within the trimmed pair.
