# Porous Lantern in TouchDesigner

This studio uses the original **L3-30** object: eight fixed similarities, a contraction ratio of `sqrt(2)-1`, and a 30-degree chord-frame roll. Its controls change the view and exposure. The camera never changes the recipe.

The installer creates `/project1/PorousLantern`. Its `view` TOP is the finished 1280 × 720 image, and **Motion → Open studio** opens a preview beside the controls. Save the project as `touchdesigner/Porous-Lantern.toe` so the default relative export paths match the repository layout.

## Viewing

- **Lantern · hero** runs the 48-second camera composition: a whole-object reveal, a controlled descent through three generations, and the return to the opening view.
- **Sculpture orbit** moves around the entire object.
- **Manual still** enables the Still page's depth, azimuth, elevation and field controls.
- **Clock → Scrub** enables Phase for a fixed position in either animated camera. Live advances according to Loop seconds. Phase 0 and 1 represent the loop boundary.
- **Exposure** defaults to 1.15.

The shader, atlas and callbacks are embedded when installed and remain in the saved `.toe`. Viewing a saved project does not require Python packages, the original file paths, or access to this repository. The atlas TOP is locked and treats its PNG as data, without a colour-space conversion. Do not unlock it unless rebuilding from the source files.

The preview uses one sample per pixel. Rendering performance depends on the GPU; the heavy raymarcher is not guaranteed to play at the movie frame rate. The exported film advances by frame number, so slow rendering does not alter its timing.

## Stills and movies

**Still → Save current still** writes the current native TOP image to a lossless PNG. It works with any camera. Scrub first if you want an exact animation phase.

**Export → Render one loop** launches the repository's standalone OpenGL renderer and FFmpeg in the background. It uses the same shader and atlas as the TouchDesigner scene, with two subpixel samples, 1280 × 720 pixels, 24 fps and silent H.264 output. The default hero duration is 48 seconds. Live exports start at phase zero; Scrub exports start at the selected phase and complete one cycle. Choose the hero or orbit camera to enable movie export.

The default hero filename is `Porous-Lantern-A-Closer-Look.mp4`. The orbit filename is `Porous-Lantern-Sculpture-Orbit.mp4`. If that file already exists, a timestamp is added to preserve the earlier export.

This is the same source-sharing export approach used in Sixfold. The MP4 is rendered by the external renderer, rather than captured from the TouchDesigner viewer or a Movie File Out TOP. There is no output upscaling.

The default **Save folder** is `../exports`, relative to the saved project. **Repository folder** defaults to `..`; it must contain `visuals/render.py`, `visuals/lantern.glsl` and `visuals/field.png`. The exporter checks that the source shader and atlas match the embedded versions before rendering. After editing either asset, reinstall and save the project to refresh its embedded copy.

Install [uv](https://docs.astral.sh/uv/) for automatic preparation of the export environment. It may download Python and dependencies on its first run. An external `python` on PATH is also supported if it already has `numpy`, `pillow`, `moderngl` and `imageio-ffmpeg`. TouchDesigner's bundled interpreter alone is not the export environment.

Status displays progress. **Cancel render** requests cancellation after the current frame. Settings and logs remain in the save folder's `logs` directory, and **Last movie**, **Last still** and **Export log** identify the outputs. Export settings are snapshotted at launch; later control changes do not affect a running movie.

## Rebuild the component

Run the installer from a TouchDesigner Text DAT or Textport, setting the repository's absolute location:

```python
from pathlib import Path
LANTERN_DIR = Path("C:/path/to/porous-lantern")
exec((LANTERN_DIR / "touchdesigner" / "install.py").read_text(encoding="utf-8"))
```

Alternatively, load the file into a DAT and call its module's `install(repository_folder)` function. Defining `LANTERN_DIR` when executing the file invokes installation automatically; importing it without that variable does not install anything.

Reinstallation updates this named component and preserves existing custom-parameter values. It does not delete other project components. Finish or cancel an active export before reinstalling. Check the `sculpture` GLSL TOP for compile errors, confirm that the preview shows the Lantern, and save the project through TouchDesigner.

The installer follows the existing Sixfold studio's node and parameter conventions. Native still saving uses the documented [TOP `save()` method](https://derivative.ca/UserGuide/TOP%20Class). A saved project and live TouchDesigner verification are separate from the Python source checks; consult the release's media record for which checks were completed.
