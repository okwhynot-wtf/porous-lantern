"""Build and check the GitHub Pages site from the canonical Markdown documents."""

import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
from urllib.parse import quote, unquote, urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"
REPOSITORY = "https://github.com/okwhynot-wtf/porous-lantern"
SITE_URL = "https://okwhynot-wtf.github.io/porous-lantern/"
PAGES = [
    ("definition", "Definition"),
    ("results", "Results & evidence"),
    ("related", "Published relatives"),
    ("reproduce", "Reproduce"),
    ("media", "Images & film"),
    ("provenance", "Credits & AI"),
]


def substitute(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", str(value))
    if re.search(r"\{\{[a-z_]+\}\}", template):
        raise ValueError("Unfilled page template field")
    return template


def rewrite_links(content, source):
    def replace(match):
        attribute, value = match.groups()
        url = urlsplit(html.unescape(value))
        if url.scheme or url.netloc or not url.path:
            return match.group(0)
        path = (source.parent / unquote(url.path)).resolve()
        if not path.is_relative_to(ROOT) or not path.exists():
            raise ValueError(f"Broken source link in {source.name}: {value}")
        if path.parent == ROOT / "docs" and path.stem in dict(PAGES):
            destination = path.stem + ".html"
        elif path.is_relative_to(ROOT / "site/assets"):
            destination = "assets/" + quote(path.relative_to(ROOT / "site/assets").as_posix())
        else:
            kind = "tree" if path.is_dir() else "blob"
            destination = f"{REPOSITORY}/{kind}/main/" + quote(path.relative_to(ROOT).as_posix())
        if url.query:
            destination += "?" + url.query
        if url.fragment:
            destination += "#" + url.fragment
        return f'{attribute}="{html.escape(destination, quote=True)}"'

    return re.sub(r'(href|src)="([^"]+)"', replace, content)


def render_page(filename, title, description, content, document=False):
    template = (ROOT / "site/templates/layout.html").read_text(encoding="utf-8")
    math_scripts = ""
    if document:
        math_scripts = ('<script src="assets/math.js"></script>'
                        '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"></script>')
    return substitute(template, {
        "title": html.escape(title),
        "description": html.escape(description, quote=True),
        "canonical": SITE_URL + ("" if filename == "index.html" else filename),
        "body_class": "document" if document else "home",
        "content": content,
        "math": math_scripts,
    })


def film_markup(film):
    url = urlsplit(film["url"])
    if url.scheme and (url.scheme != "https" or not url.netloc):
        raise ValueError("The film URL must be relative or HTTPS")
    if not url.scheme:
        source = (ROOT / "site" / unquote(url.path)).resolve()
        if not source.is_relative_to(ROOT / "site/assets") or not source.is_file() or not source.stat().st_size:
            raise ValueError(f"Missing or empty local film: {film['url']}")
    return (
        '<video id="hero-film" controls muted loop playsinline preload="none" '
        'aria-label="Porous Lantern, a silent fractal film" '
        f'poster="{html.escape(film["poster"], quote=True)}" width="1280" height="720">'
        f'<source src="{html.escape(film["url"], quote=True)}" type="video/mp4">'
        'Your browser does not support this video. '
        f'<a href="{html.escape(film["url"], quote=True)}">Download the film</a>.'
        '</video>'
    )


def still_markup(still, preview=False):
    slug = still["slug"]
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        raise ValueError(f"Invalid asset name: {slug}")
    image = f"assets/{slug}.jpg"
    image_source = ROOT / "site" / image
    if not image_source.is_file() or not image_source.stat().st_size:
        raise ValueError(f"Missing or empty gallery image: {image}")
    title = html.escape(still["title"])
    alt = html.escape(still["alt"], quote=True)
    width, height = int(still.get("width", 1920)), int(still.get("height", 1440))
    destination = f"gallery.html#{slug}" if preview else image
    details = f'<h3>{title}</h3>'
    if not preview:
        master = ROOT / "media/stills" / (slug + ".png")
        if not master.is_file() or not master.stat().st_size:
            raise ValueError(f"Missing PNG master: {master.relative_to(ROOT)}")
        master_url = REPOSITORY + "/raw/refs/heads/main/media/stills/" + slug + ".png"
        details += (
            f'<p>{html.escape(still["caption"])}</p>'
            f'<div class="image-downloads"><a href="{image}" download>Download JPEG</a>'
            f'<a href="{master_url}">PNG master</a></div>'
        )
    return (
        f'<figure id="{slug}"><a class="still-image" href="{destination}" aria-label="View {title}">'
        f'<img src="{image}" alt="{alt}" width="{width}" height="{height}" loading="lazy"></a>'
        f'<figcaption>{details}</figcaption></figure>'
    )


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data:
            if data["id"] in self.ids:
                raise ValueError(f"Duplicate HTML id: {data['id']}")
            self.ids.add(data["id"])
        for attr in ("href", "src", "poster"):
            if attr in data:
                self.links.append(data[attr])


def check_output():
    pages = {}
    for path in OUTPUT.rglob("*.html"):
        parser = PageLinks()
        parser.feed(path.read_text(encoding="utf-8"))
        pages[path.resolve()] = parser
    for source, parser in pages.items():
        for value in parser.links:
            url = urlsplit(value)
            if url.scheme or url.netloc:
                continue
            target = (source.parent / unquote(url.path)).resolve() if url.path else source
            if not target.is_relative_to(OUTPUT.resolve()) or not target.is_file():
                raise ValueError(f"Broken site link in {source.name}: {value}")
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                raise ValueError(f"Broken anchor in {source.name}: {value}")
    return len(pages)


def main():
    OUTPUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "site/assets", OUTPUT / "assets", dirs_exist_ok=True)
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    media = json.loads((ROOT / "site/media.json").read_text(encoding="utf-8"))
    if len(media["stills"]) != 6:
        raise ValueError("This edition has six stills")
    film_url = html.escape(media["film"].get("download_url", media["film"]["url"]), quote=True)
    home = substitute((ROOT / "site/templates/home.html").read_text(encoding="utf-8"), {
        "hero_film": film_markup(media["film"]),
        "hero_caption": html.escape(media["film"]["caption"]),
        "film_url": film_url,
        "preview_stills": "".join(still_markup(still, preview=True) for still in media["stills"][1:4]),
    })
    (OUTPUT / "index.html").write_text(render_page(
        "index.html", "Porous Lantern — an eightfold spatial fractal",
        "Explore Porous Lantern: an eightfold self-similar spatial fractal, seen through copper-and-teal images, a silent film and reproducible mathematics.",
        home), encoding="utf-8")
    gallery = substitute((ROOT / "site/templates/gallery.html").read_text(encoding="utf-8"), {
        "gallery_stills": "".join(still_markup(still) for still in media["stills"]),
        "film_url": film_url,
    })
    (OUTPUT / "gallery.html").write_text(render_page(
        "gallery.html", "Gallery — Porous Lantern",
        "Six views of the original Porous Lantern fractal, with JPEG images, lossless PNG masters and a silent film.",
        gallery), encoding="utf-8")
    for slug, label in PAGES:
        source = ROOT / "docs" / f"{slug}.md"
        content = markdown.markdown(
            source.read_text(encoding="utf-8"),
            extensions=["tables", "fenced_code", "toc", "pymdownx.arithmatex", "pymdownx.tasklist"],
            extension_configs={"pymdownx.arithmatex": {"generic": True}},
        )
        content = rewrite_links(content, source)
        navigation = "".join(
            f'<a href="{name}.html"' + (' aria-current="page"' if name == slug else '')
            + f'>{html.escape(text)}</a>' for name, text in PAGES
        )
        source_url = REPOSITORY + f"/blob/main/docs/{slug}.md"
        body = (
            '<main id="main" class="document-shell wrap">'
            f'<aside class="sidebar"><nav aria-label="Research pages">{navigation}</nav></aside>'
            f'<article class="article"><div class="source-link"><a href="{source_url}">'
            f'Read or suggest a correction on GitHub</a></div>{content}</article></main>'
        )
        (OUTPUT / f"{slug}.html").write_text(render_page(
            f"{slug}.html", f"{label} — Porous Lantern", f"Porous Lantern. {label}.",
            body, document=True), encoding="utf-8")
    count = check_output()
    print(f"Built and checked {count} pages in {OUTPUT}.")
    print("All local links, anchors, media references and documentation source links resolve.")


if __name__ == "__main__":
    main()
