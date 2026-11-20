# Images, film and TouchDesigner

## The preferred trimmed join

The new [join study](joins.md) presents the preferred trimmed interface,
comparisons with the original and reassigned geometry, an annotated anatomy,
and horizontal sections. The [trimmed PNG](../site/assets/joins/pair-trimmed.png)
is a computed 1100 × 880 image with two spatial samples per pixel. It uses the
same solid rendering style and frozen field as the original Lantern, with a
separate halfspace cut applied to the selected pair.

These are finite envelopes of the exact sets. Planar cut surfaces in the
rendering do not establish smooth surfaces of the infinite fractal. Only this
join has been studied: there is no new all-joins film or TouchDesigner release.
The film and studio below still show the preserved original geometry.

The reproducible [study renderer](../research/join-study/source/render_join.py)
and [shader](../research/join-study/source/join.glsl) read the original texture
without altering it. From the repository root:

```sh
python -m pip install -r visual-requirements.txt
python research/join-study/source/render_join.py
```

Output is written under `.build/join-study`, alongside a receipt recording the
shader and original texture hashes.

## The original release

The six stills and the silent hero film show the same fixed Porous Lantern.
Copper, teal and steel distinguish regions of its repeated structure. Lighting,
surface shading and the distance-atlas technique derive from Sixfold.

## The original visual edition

The [gallery](https://okwhynot-wtf.github.io/porous-lantern/gallery.html) contains
the hero composition, an axial view, a low side view, the underside, and two
successively closer views. Lossless PNG masters are in
[media/stills](https://github.com/okwhynot-wtf/porous-lantern/tree/main/media/stills).
The hero is 1920 × 1080; the other five masters are 1920 × 1440. These are
native renders with four spatial samples per pixel, not enlarged thumbnails.

**Porous Lantern — A closer look** is a 48-second, silent, looping film at
1280 × 720 and 24 frames per second. It uses two spatial samples per pixel.
A slow changing view first reveals the whole object. The camera then approaches
one lobe through three generations and returns along the same path. There are
no cuts, crossfades or replacements of the object during the descent.

The [web film](https://okwhynot-wtf.github.io/porous-lantern/assets/porous-lantern-hero.mp4)
uses a smaller encode for playback. The
[higher-quality master](https://github.com/okwhynot-wtf/porous-lantern/releases/download/v1.0.0/Porous-Lantern-A-Closer-Look.mp4)
is a separate release download.
It is a native 720p export, with no audio track or resolution upscaling.

## The visible surface

The exact attractor has zero three-dimensional volume. A finite surface
envelope gives it a solid appearance, so a pixel is not evidence that an exact
passage is blocked or that two mathematical pieces have merged.

The renderer traces six explicit address levels and a depth-seven distance
atlas at each leaf. The atlas is a quantized 96-cubed field, packed into a
1152 × 768 texture. Its smooth envelope, interpolation, finite tracing and
pixel sampling limit the detail that can be shown. Surface thickness follows
the view scale within documented bounds. Address colours also change with
zoom depth to keep the smaller copies legible. Neither change alters the eight
similarity maps.

The camera follows the continuous fractional power of the first similarity.
At integer depths its position and orientation correspond to the same view
inside that address copy. Other copies remain in the scene and may occlude
parts of it. Intermediate camera poses are a smooth motion design, not new
members of the fractal family. See [results](results.md) for the actual
passage certificates and the limits of their scope.

## TouchDesigner

Open `touchdesigner/Porous-Lantern.toe`. The studio contains the fixed shader
and embedded field texture. Motion controls select the hero journey, an orbit,
or a still composition; Live and Scrub control playback. Still controls set
depth and view angles without changing the fractal. See the
[studio instructions](../touchdesigner/README.md).

[Download the standalone project](https://github.com/okwhynot-wtf/porous-lantern/releases/download/v1.0.0/Porous-Lantern.toe)
for viewing, or download the repository for the export source and dependencies.
The release was tested in TouchDesigner 2025.33230. Native preview, still saving,
and both a short test export and the full hero export succeeded. A fresh process
opened the `.toe` from an isolated directory without its source texture.
The [studio verification record](../touchdesigner/verification.json) records
those checks and the native/export image comparison.

The studio renders the scene live with a GLSL TOP. Its movie export uses the
same GLSL source in the included offscreen renderer and encodes through FFmpeg,
following Sixfold's export approach. This produces every requested frame even
when live playback cannot maintain 24 fps. It is not a screen recording.
The native 1280 × 720 project fits TouchDesigner Non-Commercial's resolution
limit. Export dependencies are separate from the embedded live preview.

## Render from source

From the repository root:

```sh
python -m pip install -r visual-requirements.txt
python visuals/render.py .build/hero.mp4 --seconds 48 --fps 24 --samples 2
python visuals/render.py .build/still.png --mode 2 --width 1920 --height 1440 --samples 4 --depth 1
```

The fixed shader is [lantern.glsl](../visuals/lantern.glsl). Still composition
parameters and hashes are in [manifest.json](../media/stills/manifest.json).
The [film receipt](../media/film-master.json) records its frame count, renderer
and shader hash. [Media verification](../media/verification.json) records a full
decode of the web encode, and [camera comparisons](../media/camera-validation.json)
check integer zoom views against the original anatomy renderer.
To rebuild the visual field from the frozen decimal maps, install SciPy and run:

```sh
python -m pip install scipy
python visuals/build_atlas.py
```

The complete mathematical verification is independent of this visual field.
