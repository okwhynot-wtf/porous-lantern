# Porous Lantern

A cleaner join, with exact miniature Lanterns continuing within.

![The preferred trimmed join, with gold and teal pieces meeting on a mirror plane](site/assets/joins/pair-trimmed.png)

**[Website](https://okwhynot-wtf.github.io/porous-lantern/)** ·
**[Gallery](https://okwhynot-wtf.github.io/porous-lantern/gallery.html)** ·
**[Trimmed join study](docs/joins.md)** ·
**[Definition](docs/definition.md)** · **[Results](docs/results.md)**

Porous Lantern is a documented spatial fractal study by **okwhynot-wtf**.
The preferred visual direction is now the **trimmed join**: one neighbouring
pair cut back to its shared mirror plane. The traces match exactly and complete
original miniature Lanterns survive, including all their finer descendants.
The cut changes the whole object's original eight-map equation; a replacement
rule reproducing the edited whole has not been established. This is a local
join experiment, not a completed redesign of all eight joins.

The original L3-30 construction remains preserved: eight contracting
similarities, a scale ratio of `sqrt(2) - 1`, and a 30-degree roll.
Its eightfold symmetry, smaller repeated copies and passages are explored
through a solid-looking copper-and-teal rendering derived from the Sixfold project.

The original v1.0.0 release includes six lossless stills, a 48-second silent hero film,
a TouchDesigner studio, reproducible mathematical checks, and a literature review.
The exact fractal has zero volume; the visible surface is a finite rendering
envelope. Those original release assets keep their fixed geometry; the new
join images and certificates are separately identified.

## Explore or reproduce

| Purpose | Start here |
| --- | --- |
| Explore the preferred trimmed join and what survives | [Join study](docs/joins.md) |
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
python research/join-study/source/certify_interface.py
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
