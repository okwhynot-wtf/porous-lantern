# Porous Lantern Studio

The studio renders the mirrored set D: two recursive pieces retained on opposite sides of their shared plane. Camera and exposure controls change its presentation; the geometry stays fixed.

## Open and view

Open [Porous-Lantern.toe](Porous-Lantern.toe), or import [Porous-Lantern.tox](Porous-Lantern.tox) into a TouchDesigner project. Select the `PorousLanternRelease` component and choose **View → Open studio** for the preview and controls.

**Composition** offers Hero, Film, Mirror, Profile, Reverse, Interface and Within. **Play camera** selects Film and advances its 24-second camera cycle. To inspect a precise film view, turn Play camera off, select Film and adjust **Film phase** between 0 and 1. **Exposure** defaults to 1.3.

The native preview is 640 × 360. The shader, actions and locked `reference_field` texture are embedded in the saved component. Leave that texture locked for portable viewing.

The film follows a slow arc and a closer view of the central interface. The Within preset looks into retained recursive detail; it does not demonstrate a whole-D replacement rule.

## Export

1. Under **Export**, choose a **Save folder**. An absolute path makes the destination explicit; the default `../exports` is resolved from TouchDesigner's working directory.
2. For movies, set **FFmpeg executable**, or make `ffmpeg` available on PATH. PNG export does not require FFmpeg.
3. Set the composition, phase and exposure, then use **Save still** or **Render 24 second loop**.

| Output | Settings |
| --- | --- |
| Save still | Current composition and phase; lossless 1920 × 1080 PNG; two spatial samples per pixel. |
| Render 24 second loop | Film camera from phase zero; 576 frames at 24 fps; 1280 × 720; silent H.264; two spatial samples per pixel. |

Movie export uses its own fixed frame sequence, regardless of the selected preview composition or phase. Leave Exposure unchanged while exporting, because it is read as frames render. Export speed does not change the movie's duration.

Every frame is rendered by the native GLSL TOP in tiles no larger than **320 × 180**. The rendered RGB tiles are read to the CPU and assembled into the frame. FFmpeg encodes those completed frames into the movie.

**Status** reports progress and completion. **Cancel export** takes effect at the next frame boundary and can leave a partial file. A completed export has a neighbouring `.json` receipt; movies also have a `.log` file. Failures produce an `.error.txt` file.

The standard movie name is `Porous-Lantern-Mirrored-Form.mp4`. If that name exists, the studio chooses a timestamped name. Stills are timestamped PNGs. Export returns to the preview when complete.

## Gallery-size stills

The published hero master is 1920 × 1080; the other five gallery masters are 1920 × 1440. The Save still button uses 1920 × 1080. To request a 1920 × 1440 native export, choose the composition and run inside TouchDesigner:

```python
studio = op('/project1/PorousLanternRelease')
studio.op('actions').module.begin(
    'C:/exports/Porous-Lantern.png', kind='still',
    width=1920, height=1440, samples=2)
```

Adjust the component path if it was renamed or imported elsewhere, and choose the desired output path. Finish or cancel an active export before starting another.

## Rebuild from source

In a TouchDesigner Text DAT or Textport, set the repository location:

```python
from pathlib import Path
LANTERN_DIR = Path('C:/path/to/porous-lantern')
exec((LANTERN_DIR / 'touchdesigner' / 'install.py').read_text(encoding='utf-8'))
```

The installer creates or updates `/project1/PorousLanternRelease` and resets its custom controls to their defaults. Finish or cancel an export before reinstalling. A locked field texture remains embedded; to rebuild it from a changed `visuals/field.png`, unlock `reference_field` before running the installer. Wait for the preview to appear, then save the component or project.

## Verification scope

The native export was verified as a 24-second, 576-frame, 1280 × 720 movie at 24 fps with two spatial samples. The saved TOX passed a portable reload test with its embedded assets. The TOE was packaged from a clean project using that component; a separate fresh-process reopening of the TOE has not yet been tested.

The [film receipt](../media/film-master.json) records the delivered movie. Mathematical claims about the displayed set and the limits of its finite envelope are documented in [results](../docs/results.md).
