# Porous Lantern

Two mirrored fractal pieces, an exact shared interface, and recursive detail within.

![Porous Lantern, a copper-and-teal mirrored fractal form](site/assets/lantern-hero.jpg)

**[Website](https://okwhynot-wtf.github.io/porous-lantern/)** · **[Gallery](https://okwhynot-wtf.github.io/porous-lantern/gallery.html)** · **[The interface](docs/joins.md)** · **[Definition](docs/definition.md)** · **[Results](docs/results.md)**

Porous Lantern is a spatial fractal artwork by **okwhynot-wtf**. Two recursively generated pieces meet at a mirror plane, with each retained on its own side. Their traces match exactly. Complete generating motifs and all their finer descendants remain inside the displayed form.

The mathematical set is

```text
D = (f_0(K) intersect {x >= y}) union (f_1(K) intersect {y >= x}).
```

K is an auxiliary motif defined by eight contracting similarities with ratio `sqrt(2)-1` and a 30-degree spatial roll. It supplies the detail in D; its IFS equation is not a whole-object replacement rule for D. Connectivity of D and a finite whole-object IFS description remain unresolved.

The exact set has zero three-dimensional volume. Six stills, a 24-second silent film and a TouchDesigner project show a finite metallic envelope of that geometry. The film is rendered from native TouchDesigner TOP frames.

## Explore and reproduce

| Purpose | Start here |
| --- | --- |
| Understand the mirrored interface | [Interface](docs/joins.md) |
| Define the displayed geometry and its generating maps | [Exact construction](docs/definition.md) |
| Read the established properties and limits | [Results and evidence](docs/results.md) |
| Explore mathematical precedents | [Related work](docs/related.md) |
| Run checks or sample the displayed set | [Reproduction](docs/reproduce.md) |
| View images, film and the native project | [Media](docs/media.md) |
| Credit or reuse the work | [Provenance](docs/provenance.md) |

```sh
python -m pip install -r requirements.txt
python math/verify.py --receipt .build/verification.json
python research/join-study/source/certify_interface.py
```

Build the website from the canonical documents and current media manifest:

```sh
python -m pip install -r site-requirements.txt
python scripts/build_site.py
```

Analytic arguments, interval bounds and rendering evidence are identified separately. Independent mathematical review is pending; historical priority is not claimed.

Developed with substantial assistance from OpenAI GPT models through ChatGPT and Codex. Code and certificate data use [MIT](LICENSE); writing, images and films use [CC BY 4.0](CONTENT-LICENSE.md).
