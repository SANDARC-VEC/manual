#!/usr/bin/env python3
"""
Build SANDARC-VEC-Manual.pdf from the MkDocs site.

Pipeline:
  1. `mkdocs build` — the print-site plugin assembles every page (in nav
     order) into a single print page with a cover page and TOC.
  2. Playwright's headless Chromium prints that page to PDF. Page size,
     margins, and the running footer ("SANDARC VEC Manual" / "Page N of M")
     come from the @page rules in docs/stylesheets/print-site.css, and the
     heading structure becomes the PDF outline (bookmarks).
  3. pypdf sets the PDF title/author metadata.

Usage (from the repo root):
  .venv/bin/python scripts/build-pdf.py [output.pdf]

One-time setup: .venv/bin/playwright install chromium --only-shell
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

REPO_ROOT = Path(__file__).resolve().parent.parent
# The offline plugin sets use_directory_urls: false, flattening the print
# page to print_page.html; without it the page lands in print_page/.
PRINT_PAGE_CANDIDATES = [
    REPO_ROOT / "site" / "print_page.html",
    REPO_ROOT / "site" / "print_page" / "index.html",
]
DEFAULT_OUTPUT = REPO_ROOT / "SANDARC-VEC-Manual.pdf"

TITLE = "SANDARC VEC Manual"
AUTHOR = "San Diego County Amateur Radio Council"


def build_site() -> Path:
    print("==> mkdocs build")
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build"],
        cwd=REPO_ROOT,
        check=True,
    )
    for candidate in PRINT_PAGE_CANDIDATES:
        if candidate.exists():
            return candidate
    sys.exit("Print page not found in site/ — is the print-site plugin enabled?")


def print_to_pdf(print_page: Path, raw_pdf: Path) -> None:
    print("==> printing with Playwright Chromium")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(print_page.as_uri(), wait_until="networkidle", timeout=60_000)
        # Make sure the Google-hosted webfonts (IBM Plex, Exo 2) are in
        # before printing, or the PDF falls back to system fonts.
        page.evaluate("document.fonts.ready")
        page.emulate_media(media="print")
        page.pdf(
            path=str(raw_pdf),
            prefer_css_page_size=True,  # honor the @page size in print-site.css
            print_background=True,
            display_header_footer=False,
            tagged=True,   # Chromium only emits the outline for tagged PDFs
            outline=True,  # PDF bookmarks from the heading structure
        )
        browser.close()


def add_metadata(raw_pdf: Path, output: Path) -> int:
    writer = PdfWriter(clone_from=PdfReader(raw_pdf))  # clone keeps the outline
    writer.add_metadata({
        "/Title": TITLE,
        "/Author": AUTHOR,
        "/Subject": "Volunteer Examiner Manual",
        "/Creator": "mkdocs-print-site-plugin + headless Chromium",
    })
    with open(output, "wb") as f:
        writer.write(f)
    return len(writer.pages)


def main() -> None:
    output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    print_page = build_site()
    with tempfile.TemporaryDirectory() as tmp:
        raw_pdf = Path(tmp) / "raw.pdf"
        print_to_pdf(print_page, raw_pdf)
        pages = add_metadata(raw_pdf, output)
    print(f"==> wrote {output} ({pages} pages)")

    # The site's "Download PDF" links (hero, sidebar, footer) point at
    # /SANDARC-VEC-Manual.pdf, so ship the PDF with the built site.
    site_copy = REPO_ROOT / "site" / DEFAULT_OUTPUT.name
    shutil.copy2(output, site_copy)
    print(f"==> copied into {site_copy}")


if __name__ == "__main__":
    main()
