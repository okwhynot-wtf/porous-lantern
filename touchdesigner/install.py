"""Build Porous Lantern inside TouchDesigner; folder is the repository root.

Call install(folder), or execute this DAT with LANTERN_DIR defined. The shader,
data texture and callbacks are embedded in the component before it is saved.
"""
from pathlib import Path
import hashlib
import json


def install(folder):
    folder = Path(folder).expanduser().resolve()
    source = folder / "visuals" / "lantern.glsl"
    atlas_file = folder / "visuals" / "field.png"
    actions_file = folder / "touchdesigner" / "actions.py"
    shader_text = source.read_text(encoding="utf-8")
    actions_text = actions_file.read_text(encoding="utf-8")
    atlas_bytes = atlas_file.read_bytes()
    if "uniform float uWeight;" not in shader_text:
        raise ValueError("Expected the Lantern shader's uWeight declaration.")
    manifest = {
        "recipe": "L3-30; eight fixed maps; ratio sqrt(2)-1; roll 30 degrees",
        "shader_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "atlas_sha256": hashlib.sha256(atlas_bytes).hexdigest(),
        "preview_pixels": [1280, 720],
        "movie_defaults": {"seconds": 48, "fps": 24, "samples": 2},
    }

    root = op("/project1")
    if root is None:
        raise RuntimeError("Create /project1 before installing Porous Lantern.")
    base = root.op("PorousLantern") or root.create(baseCOMP, "PorousLantern")
    if base.fetch("lanternJob", None, search=False):
        raise RuntimeError("Finish or cancel the current export before reinstalling.")
    base.nodeX, base.nodeY = 320, 60

    def node(kind, name, parent=base):
        return parent.op(name) or parent.create(kind, name)

    pages = {page.name: page for page in base.customPages}
    motion = pages.get("Motion") or base.appendCustomPage("Motion")
    still = pages.get("Still") or base.appendCustomPage("Still")
    export = pages.get("Export") or base.appendCustomPage("Export")

    def menu(page, name, label, names, labels, default):
        existing = bool(base.pars(name))
        par = getattr(base.par, name) if existing else page.appendMenu(name, label=label)[0]
        selected = par.eval() if existing else default
        par.menuNames, par.menuLabels = names, labels
        par.default = default
        par.val = selected if selected in names else default
        return par

    def number(page, name, label, default, low, high):
        if not base.pars(name):
            par = page.appendFloat(name, label=label)[0]
            par.default = par.val = default
            par.min, par.max = low, high
            par.clampMin, par.clampMax = True, True
        return getattr(base.par, name)

    def pulse(page, name, label):
        if not base.pars(name):
            page.appendPulse(name, label=label)

    def text_parameter(page, name, label, default="", kind="Str", readonly=False):
        if not base.pars(name):
            par = getattr(page, "append" + kind)(name, label=label)[0]
            par.default = par.val = default
            par.readOnly = readonly
        return getattr(base.par, name)

    menu(motion, "Camera", "Camera", ["hero", "orbit", "still"],
         ["Lantern · hero", "Sculpture orbit", "Manual still"], "hero")
    menu(motion, "Clock", "Clock", ["live", "manual"], ["Live", "Scrub"], "live")
    number(motion, "Phase", "Phase", 0., 0., 1.)
    number(motion, "Seconds", "Loop seconds", 48., 5., 120.)
    number(motion, "Exposure", "Exposure", 1.15, .2, 3.)
    pulse(motion, "Openstudio", "Open studio")
    number(still, "Depth", "Zoom generations", 0., 0., 3.)
    number(still, "Azimuth", "Azimuth", -58., -360., 360.)
    number(still, "Elevation", "Elevation", 34., -90., 90.)
    number(still, "Frame", "Vertical field", 4.65, .5, 12.)
    pulse(still, "Savestill", "Save current still")
    text_parameter(export, "Destination", "Save folder", "../exports", "Folder")
    text_parameter(export, "Sourcefolder", "Repository folder", "..", "Folder")
    text_parameter(export, "Format", "Movie format", "1280 × 720 · 24 fps · 2 samples", readonly=True)
    pulse(export, "Renderloop", "Render one loop")
    pulse(export, "Cancelrender", "Cancel render")
    text_parameter(export, "Exportstatus", "Status", "Ready", readonly=True)
    text_parameter(export, "Laststill", "Last still", kind="File", readonly=True)
    text_parameter(export, "Lastmovie", "Last movie", kind="File", readonly=True)
    text_parameter(export, "Lastlog", "Export log", kind="File", readonly=True)
    pulse(export, "Showfolder", "Open save folder")
    base.sortCustomPages("Motion", "Still", "Export")

    atlas = node(moviefileinTOP, "reference_field")
    atlas.lock = False
    atlas.par.file = atlas_file.as_posix()
    atlas.par.inputcolorspace = "passthrough"
    atlas.par.play = False
    atlas.par.reloadpulse.pulse()
    atlas.cook(force=True)
    if (atlas.width, atlas.height) != (1152, 768):
        raise RuntimeError("Lantern field.png must be 1152 × 768.")
    # A locked TOP stores its cooked data in the .toe. Its filename is then only
    # a relative source hint; playback never needs the external PNG.
    atlas.lock = True
    atlas.par.file = "../visuals/field.png"

    shader = node(glslTOP, "sculpture")
    pixel = shader.par.pixeldat.eval()
    # Movie File In uploads PNG rows with the image convention. The standalone
    # data texture uploads raw atlas rows. Adapt only that coordinate convention.
    td_source = shader_text.replace("uniform float uWeight;", "const float uWeight = 1.;", 1)
    for address in ("a", "b"):
        coordinate = f"({address}+uv)/atlas"
        td_source = td_source.replace(
            f"textureLod(FIELD, {coordinate}, 0.)",
            f"textureLod(FIELD, vec2(({coordinate}).x, 1.-({coordinate}).y), 0.)")
    pixel.text = (
        "#define FIELD sTD2DInputs[0]\n"
        + td_source
        + "\nlayout(location=0) out vec4 fragColor;\n"
        + "void main(){fragColor=TDOutputSwizzle(vec4(render(vUV.st),1.));}\n"
    )
    shader.inputConnectors[0].connect(atlas)
    shader.par.outputresolution = "custom"
    shader.par.resolutionw, shader.par.resolutionh = 1280, 720
    shader.par.inputfiltertype = "linear"
    shader.seq.vec.numBlocks = 2
    shader.seq.vec[0].par.name = "uView"
    shader.seq.vec[0].par.valuex.expr = (
        "parent().par.Phase if parent().par.Clock == 'manual' "
        "else absTime.seconds / parent().par.Seconds"
    )
    shader.seq.vec[0].par.valuey.expr = "parent().par.Camera.menuIndex"
    shader.seq.vec[0].par.valuez.expr = "parent().par.Exposure"
    shader.seq.vec[0].par.valuew.expr = "me.par.resolutionw / me.par.resolutionh"
    shader.seq.vec[1].par.name = "uStill"
    for channel, parameter in zip("xyzw", ("Depth", "Azimuth", "Elevation", "Frame")):
        getattr(shader.seq.vec[1].par, "value" + channel).expr = "parent().par." + parameter

    output = node(nullTOP, "view")
    output.inputConnectors[0].connect(shader)
    base.par.opviewer = output
    output.viewer = base.viewer = True
    manifest_dat = node(textDAT, "asset_manifest")
    manifest_dat.text = json.dumps(manifest, indent=2)
    actions = node(textDAT, "actions")
    actions.text = actions_text

    studio = node(containerCOMP, "studio")
    studio.par.w, studio.par.h = 1200, 600
    preview = node(containerCOMP, "preview", studio)
    preview.par.w, preview.par.h, preview.par.top = 800, 600, output
    preview.par.topfill, preview.par.bgalpha = "best", 1.
    settings = node(parameterCOMP, "settings", studio)
    settings.par.x, settings.par.w, settings.par.h = 800, 400, 600
    settings.par.op, settings.par.builtin, settings.par.custom = base, False, True
    settings.par.header, settings.par.pagenames, settings.par.allowexpand = False, True, False
    settings.par.pagescope, settings.par.syncpage = "Motion Still Export", True
    window = node(windowCOMP, "studio_window")
    window.par.winop, window.par.title = studio, "Porous Lantern Studio"
    window.par.justifyh, window.par.justifyv, window.par.borders = "center", "center", True
    window.par.cursorvisible = "alwaysvisible"

    events = node(parameterexecuteDAT, "events")
    events.par.op = base
    events.par.pars = "Camera Clock Openstudio Savestill Renderloop Cancelrender Showfolder"
    events.par.valuechange, events.par.onpulse = True, True
    events.text = '''def onValueChange(par, prev):
    if par.name in ('Camera', 'Clock'):
        parent().op('actions').module.update_controls()

def onPulse(par):
    actions = parent().op('actions').module
    callbacks = {'Openstudio': actions.open_studio, 'Savestill': actions.save_still,
                 'Renderloop': actions.start, 'Cancelrender': actions.cancel,
                 'Showfolder': actions.show_folder}
    if par.name in callbacks:
        callbacks[par.name]()
'''
    startup = node(executeDAT, "startup")
    startup.par.start = True
    startup.text = '''def onStart():
    run("op(args[0]).module.on_start()", parent().op('actions').path, delayFrames=3)
'''
    atlas.nodeX, atlas.nodeY = -240, 80
    shader.nodeX, shader.nodeY = 0, 80
    pixel.nodeX, pixel.nodeY = 0, -70
    output.nodeX, output.nodeY = 230, 80
    for i, item in enumerate((studio, window, actions, events, startup, manifest_dat)):
        item.nodeX, item.nodeY = -240 + 160 * (i % 3), -240 - 120 * (i // 3)
    base.currentPage = "Motion"
    base.store("lanternJob", None)
    base.storeStartupValue("lanternJob", None)
    actions.module.set_state("Ready", False)
    actions.module.update_controls()
    shader.cook(force=True)
    return base


if "LANTERN_DIR" in globals():
    install(LANTERN_DIR)
