# Porous Lantern

Eight tilted copies of one shape, repeating around an open centre.

![Porous Lantern in copper, teal and steel](site/assets/lantern-hero.jpg)

**[Website](https://okwhynot-wtf.github.io/porous-lantern/)** ·
**[Gallery](https://okwhynot-wtf.github.io/porous-lantern/gallery.html)** ·
**[Definition](docs/definition.md)** · **[Results](docs/results.md)**

Porous Lantern is a documented spatial fractal study by **okwhynot-wtf**.
This edition fixes the original L3-30 construction: eight contracting
similarities, a scale ratio of `sqrt(2) - 1`, and a 30-degree roll.
Its eightfold symmetry, smaller repeated copies and passages are explored
through a solid-looking copper-and-teal rendering derived from the Sixfold project.

The release includes six lossless stills, a 48-second silent hero film,
a TouchDesigner studio, reproducible mathematical checks, and a literature review.
The exact fractal has zero volume; the visible surface is a finite rendering
envelope. The geometry stays fixed throughout the images and film.

## Explore or reproduce

| Purpose | Start here |
| --- | --- |
| Define the eight maps | [Exact construction](docs/definition.md) |
| Understand the established results and open questions | [Results and evidence](docs/results.md) |
| Compare published relatives | [Prior art](docs/related.md) |
| Generate points and verify certificates | [Reproduction](docs/reproduce.md) |
| Open the studio or render the film | [Media and TouchDesigner](docs/media.md) |
| Credit or reuse the work | [Provenance](docs/provenance.md) |

```sh
python -m pip install -r requirements.txt
python math/verify.py --receipt .build/verification.json
python math/generate.py --depth 5 --output .build/lantern.csv
```

Build the website from the same Markdown documents:

```sh
python -m pip install -r site-requirements.txt
python scripts/build_site.py
```

The public account distinguishes analytic arguments, interval-certified bounds,
numerical diagnostics and visual evidence. Independent mathematical review is
pending. The prior-art review identifies a close planar eight-gasket relative;
historical originality of the spatial recipe remains open.

Developed with substantial assistance from OpenAI GPT models through ChatGPT
and Codex. Code and original certificate data use [MIT](LICENSE); writing,
images and films use [CC BY 4.0](CONTENT-LICENSE.md).
