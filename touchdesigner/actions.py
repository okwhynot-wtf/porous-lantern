"""Callbacks embedded in Porous Lantern's actions Text DAT.

Only primitive state is stored in the COMP. Process objects remain in this
runtime module and are never serialized into the public TouchDesigner project.
"""
from datetime import datetime
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess

job = None


def owner():
    return me.parent()


def resolve_setting(name):
    value = Path(tdu.expandPath(getattr(owner().par, name).eval())).expanduser()
    return (Path(project.folder) / value).resolve()


def folder():
    return resolve_setting("Destination")


def source_folder():
    candidates = [resolve_setting("Sourcefolder"), Path(project.folder), Path(project.folder).parent]
    for candidate in candidates:
        candidate = candidate.resolve()
        if (candidate / "visuals" / "render.py").is_file():
            manifest = json.loads(owner().op("asset_manifest").text)
            for filename, key in (("lantern.glsl", "shader_sha256"), ("field.png", "atlas_sha256")):
                path = candidate / "visuals" / filename
                if hashlib.sha256(path.read_bytes()).hexdigest() != manifest[key]:
                    raise ValueError("The source assets differ from this project. Reinstall to refresh the embedded assets.")
            return candidate
    raise FileNotFoundError("Set Repository folder to the checkout containing visuals/render.py.")


def set_state(message, busy):
    b = owner()
    b.par.Exportstatus.val = message
    b.par.Renderloop.enable = not busy and b.par.Camera.eval() != "still"
    b.par.Cancelrender.enable = busy


def update_controls():
    b = owner()
    manual = b.par.Camera.eval() == "still"
    b.par.Clock.enable = not manual
    b.par.Phase.enable = not manual and b.par.Clock.eval() == "manual"
    b.par.Renderloop.enable = not manual and job is None
    for name in ("Depth", "Azimuth", "Elevation", "Frame"):
        getattr(b.par, name).enable = manual


def open_studio():
    owner().op("studio_window").par.winopen.pulse()


def show_folder():
    destination = folder()
    destination.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        os.startfile(str(destination))
    else:
        subprocess.Popen(["open", str(destination)], stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def save_still():
    b = owner()
    try:
        destination = folder()
        destination.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        target = destination / f"Porous-Lantern-{b.par.Camera.eval()}-{stamp}.png"
        output = b.op("view")
        output.cook(force=True)
        output.save(target.as_posix(), asynchronous=False)
        if not target.is_file() or not target.stat().st_size:
            raise RuntimeError("TouchDesigner did not produce the still image.")
        b.par.Laststill.val = target.as_posix()
        if job is None:
            set_state(f"Saved · {target.name}", False)
    except Exception as exc:
        set_state(f"Still failed · {exc}", job is not None)


def python_command():
    uv = shutil.which("uv")
    if not uv:
        candidate = Path.home() / ".local" / "bin" / ("uv.exe" if os.name == "nt" else "uv")
        if candidate.is_file():
            uv = str(candidate)
    if uv:
        return [uv, "run", "--python", "3.12", "--with", "numpy", "--with", "pillow",
                "--with", "moderngl", "--with", "imageio-ffmpeg", "python"]
    python = shutil.which("python") or shutil.which("python3")
    if python:
        return [python]
    raise FileNotFoundError("Install uv, or add Python with the visual dependencies to PATH.")


def start():
    global job
    b = owner()
    if job is not None or b.fetch("lanternJob", None, search=False):
        return
    if b.par.Camera.eval() == "still":
        set_state("Choose the hero or orbit camera to export a movie.", False)
        return
    try:
        source = source_folder()
        destination = folder()
        destination.mkdir(parents=True, exist_ok=True)
        logs = destination / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        name = f"Porous-Lantern-{b.par.Camera.eval()}-{stamp}"
        title = "Porous-Lantern-A-Closer-Look" if b.par.Camera.eval() == "hero" else "Porous-Lantern-Sculpture-Orbit"
        target = destination / (title + ".mp4")
        if target.exists():
            target = destination / f"{title}-{stamp}.mp4"
        log = logs / (name + ".log")
        cancel_file, settings_file = logs / (name + ".cancel"), logs / (name + ".json")
        snapshot = {
            "mode": b.par.Camera.menuIndex,
            "phase": float(b.par.Phase.eval()) if b.par.Clock.eval() == "manual" else 0.,
            "seconds": float(b.par.Seconds.eval()),
            "fps": 24, "samples": 2, "width": 1280, "height": 720,
            "exposure": float(b.par.Exposure.eval()),
            "depth": float(b.par.Depth.eval()),
            "az": float(b.par.Azimuth.eval()),
            "elev": float(b.par.Elevation.eval()),
            "frame": float(b.par.Frame.eval()),
        }
        settings_file.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
        command = python_command() + [str(source / "visuals" / "render.py"), str(target)]
        for key, value in snapshot.items():
            command.extend(["--" + key, str(value)])
        command.extend(["--cancel-file", str(cancel_file)])
        options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
        with log.open("wb") as stream:
            process = subprocess.Popen(command, cwd=source, stdin=subprocess.DEVNULL,
                                       stdout=stream, stderr=subprocess.STDOUT, **options)
        job = {"process": process, "target": target, "log": log, "cancel": cancel_file}
        b.store("lanternJob", process.pid)
        b.storeStartupValue("lanternJob", None)
        b.par.Lastlog.val = log.as_posix()
        set_state("Starting export…", True)
        poll()
    except Exception as exc:
        set_state(f"Export failed · {exc}", False)


def poll():
    global job
    if job is None:
        return
    b = owner()
    code = job["process"].poll()
    with job["log"].open("rb") as stream:
        stream.seek(max(0, job["log"].stat().st_size - 8192))
        lines = stream.read().decode("utf-8", errors="replace").splitlines()
    if code is None:
        if job["cancel"].exists():
            set_state("Cancelling after the current frame…", True)
        else:
            for line in reversed(lines):
                match = re.match(r"^(\d+)/(\d+)(?:\s|$)", line)
                if match:
                    current, total = map(int, match.groups())
                    if total:
                        set_state(f"Rendering {100 * current / total:.0f}% · {current}/{total} frames", True)
                    break
        run("op(args[0]).module.poll()", me.path, delayMilliSeconds=500, wallTime=True)
        return
    target = job["target"]
    if code == 0 and target.is_file() and target.stat().st_size:
        b.par.Lastmovie.val = target.as_posix()
        message = f"Saved · {target.name}"
    elif code == 2 and job["cancel"].exists():
        message = "Export cancelled"
    else:
        detail = next((line for line in reversed(lines) if line.strip()), f"exit code {code}")
        message = "Export failed · " + detail[-220:]
    if job["cancel"].exists():
        job["cancel"].unlink()
    b.unstore("lanternJob")
    job = None
    set_state(message, False)


def cancel():
    if job is not None:
        job["cancel"].touch()
        set_state("Cancelling after the current frame…", True)


def on_start():
    owner().store("lanternJob", None)
    set_state("Ready", False)
    update_controls()
    open_studio()
