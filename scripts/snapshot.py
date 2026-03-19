"""Render Sphinx HTML output to PDF snapshots (light, dark, mobile).

Install:

    1. Create and activate a Python venv, e.g. `python -m venv venv && venv\Scripts\activate`
    2. Install dependencies with `pip install -r requirements.txt`
    3. Run `playright install chromium` to install the browser engine

How to use:

    1. Build the docs with `make build`.
    2. Run this script with `python snapshot.py` to generate PDFs for all configs
       (Desktop-light, Desktop-dark, Mobile-light, Mobile-dark).
       Or specify a subset of configs with `--snapshots`, e.g. `--snapshots 1 4` for just Desktop-light and Mobile-dark.
    3. Find the generated PDFs in `snapshots/{timestamp}/`.
"""

import argparse
import asyncio
import img2pdf
import json
import shutil
import sys
import threading
from dataclasses import dataclass
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from playwright.async_api import BrowserContext, async_playwright
from pypdf import PdfReader, PdfWriter
from tqdm import tqdm

ROOT = Path(__file__).parent.parent
BUILD_DIR = ROOT / "docs" / "_build"
SNAPSHOT_DIR = ROOT / "snapshots"

HOST = "127.0.0.1"
PORT = 8765
CONCURRENCY = 8
VIEWPORT_HEIGHT = 900
JPEG_QUALITY = 85     # 0–100. 75 matches streaming-platform quality; raise to 90 for print.
SCREENSHOT_SCALE = 0.70  # Scales render width before capture. 0.75 cuts pixel area ~44%.

SKIP_STEMS = frozenset({"search", "genindex", "py-modindex"})

# Maps a page's relative path → content fragment injected into #protected-content.
# Fragment files are excluded from the page list automatically.
GATED_PAGES: dict[str, Path] = {
    "help/downloads/index.html": BUILD_DIR / "section-content-downloads.html",
}

_CLEANUP_JS = """() => {
    document.querySelectorAll(
        '.skip-link, [class*="skip-to"], a[href="#main-content"]'
    ).forEach(el => el.style.display = 'none');
}"""


@dataclass(frozen=True)
class Config:
    label: str
    theme: str
    width: int
    color: str


CONFIGS = [
    Config("Desktop-light", "light", 1440, "#b75a19"),
    Config("Desktop-dark",  "dark",  1440, "#bf5252"),
    Config("Mobile-light",  "light",  390,  "#a919b7"),
    Config("Mobile-dark",   "dark",   390,  "#b719a9"),
]


def _parse_args(configs: list[Config]) -> list[Config]:
    """Parse CLI arguments and return the selected subset of configs."""
    choices = "  ".join(f"{i + 1}: {cfg.label}" for i, cfg in enumerate(configs))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--snapshots",
        nargs="+",
        type=int,
        metavar="ID",
        help=f"IDs of configs to run (default: all).  Available — {choices}",
    )
    args = parser.parse_args()

    if not args.snapshots:
        return configs

    by_id = {i + 1: cfg for i, cfg in enumerate(configs)}
    invalid = [x for x in args.snapshots if x not in by_id]
    if invalid:
        parser.error(f"invalid snapshot ID(s): {invalid}  —  available: {list(by_id)}")

    return [by_id[x] for x in args.snapshots]


def _serve(directory: Path, port: int) -> HTTPServer:
    """Start a static HTTP server in a daemon thread."""
    class _Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, *args):
            pass

    server = HTTPServer((HOST, port), _Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def _find_pages(build_dir: Path) -> list[Path]:
    """Walk the build directory and return renderable page paths in document order."""
    fragment_names = {p.name for p in GATED_PAGES.values()}
    pages = []
    for html in sorted(build_dir.rglob("*.html")):
        rel = html.relative_to(build_dir)
        if (
            any(p.startswith("_") for p in rel.parts)
            or rel.stem in SKIP_STEMS
            or html.name in fragment_names
        ):
            continue
        pages.append(rel)
    pages.sort(key=lambda p: (p.parent.parts, p.stem != "index", p.stem))
    return pages


async def _settle(page) -> None:
    """Await all async renderers so the page is in its final visual state."""
    await page.add_style_tag(content="""
        *, *::before, *::after {
            animation-duration: 0.001s !important;
            transition-duration: 0.001s !important;
        }
    """)
    await page.evaluate("""async () => {
        await document.fonts.ready;
        if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
    }""")
    await page.wait_for_timeout(200)


async def _pdf(page, path: Path) -> None:
    """Capture a full-page screenshot and embed it as a PDF page.

    Uses screenshot instead of page.pdf() to avoid Chromium's tiled PDF
    rendering, which silently drops content at tile boundaries on long pages.
    """
    await _settle(page)
    jpg = path.with_suffix(".jpg")
    await page.screenshot(path=str(jpg), full_page=True, type="jpeg", quality=JPEG_QUALITY)
    path.write_bytes(img2pdf.convert(str(jpg)))
    jpg.unlink()


async def _render_page(
    sem: asyncio.Semaphore,
    context: BrowserContext,
    cfg: Config,
    rel: Path,
    index: int,
    tmp_dir: Path,
    pbar: tqdm,
) -> list[Path]:
    """Load, theme, and export one page to PDF.

    Gated pages produce two PDFs: the locked view followed by the unlocked view.
    """
    async with sem:
        page = await context.new_page()
        await page.emulate_media(media="screen")
        try:
            await page.goto(
                f"http://{HOST}:{PORT}/{rel.as_posix()}",
                wait_until="networkidle",
                timeout=15_000,
            )
        except Exception as e:
            pbar.write(f"[warn] {rel}: {e}")
            await page.close()
            pbar.update(1)
            return []

        await page.evaluate(
            f"document.documentElement.setAttribute('data-theme', '{cfg.theme}')"
        )
        await page.evaluate(_CLEANUP_JS)

        out = tmp_dir / f"{index:04d}a.pdf"
        await _pdf(page, out)
        paths = [out]

        content_file = GATED_PAGES.get(rel.as_posix())
        if content_file and content_file.exists():
            html = json.dumps(content_file.read_text(encoding="utf-8"))
            await page.evaluate(f"""() => {{
                const gate = document.getElementById('password-gate-container');
                const content = document.getElementById('protected-content');
                if (gate && content) {{
                    content.innerHTML = {html};
                    content.style.display = 'block';
                    gate.style.display = 'none';
                }}
            }}""")
            await page.wait_for_timeout(400)
            out = tmp_dir / f"{index:04d}b.pdf"
            await _pdf(page, out)
            paths.append(out)

        await page.close()
        pbar.update(1)
        return paths


async def _render_config(cfg: Config, pages: list[Path], out_dir: Path) -> None:
    """Render all pages for a single config and merge into one PDF."""
    tmp = out_dir / f"_tmp_{cfg.label}"
    tmp.mkdir(parents=True, exist_ok=True)

    with tqdm(total=len(pages), desc=f"{cfg.label:14}", unit="pg", colour=cfg.color) as pbar:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            context = await browser.new_context(
                viewport={"width": cfg.width, "height": VIEWPORT_HEIGHT},
                device_scale_factor=SCREENSHOT_SCALE,
            )
            sem = asyncio.Semaphore(CONCURRENCY)
            results = await asyncio.gather(*[
                _render_page(sem, context, cfg, rel, i, tmp, pbar)
                for i, rel in enumerate(pages)
            ])
            await browser.close()

    writer = PdfWriter()
    for path in sorted(p for paths in results for p in paths):
        for pdf_page in PdfReader(str(path)).pages:
            writer.add_page(pdf_page)

    with open(out_dir / f"snapshot-{cfg.label.lower()}.pdf", "wb") as f:
        writer.write(f)

    shutil.rmtree(tmp)


async def main(configs: list[Config]) -> None:
    """Build PDFs for each selected config in parallel."""
    if not BUILD_DIR.exists():
        sys.exit("run 'make build' first")

    pages = _find_pages(BUILD_DIR)
    if not pages:
        sys.exit("no pages found in build directory")

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_dir = SNAPSHOT_DIR / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"{len(pages)} pages  read, writing to  snapshots/{ts}/")
    server = _serve(BUILD_DIR, PORT)
    try:
        await asyncio.gather(*[_render_config(cfg, pages, out_dir) for cfg in configs])
    finally:
        server.shutdown()
    print(f"Done: written to snapshots/{ts}/")


if __name__ == "__main__":
    asyncio.run(main(_parse_args(CONFIGS)))
