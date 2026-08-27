#!/usr/bin/env python3
"""
Build one SANDARC-VEC-Manual PDF per language from the MkDocs site.

Pipeline, repeated for each locale in the i18n plugin's `languages` list:
  1. `mkdocs build` against a generated config that pins the i18n plugin to
     a single locale, so that locale builds at the site root and the
     print-site plugin produces a print page for it. (A normal multi-locale
     build only ever emits one print page, for the default language.)
  2. Relative links in that page are rewritten to absolute site URLs, so
     they survive being printed from a file:// URL.
  3. Playwright's headless Chromium prints that page to PDF. Page size,
     margins, and the running footer ("SANDARC VEC Manual" / "Page N of M")
     come from the @page rules in docs/stylesheets/print-site.css, and the
     heading structure becomes the PDF outline (bookmarks).
  4. pypdf sets the PDF title/author metadata.

The default locale keeps the bare SANDARC-VEC-Manual.pdf name so existing
links to it stay valid; every other locale is suffixed, e.g.
SANDARC-VEC-Manual-es.pdf. The names must match extra.pdf_downloads in
mkdocs.yml, which is what the site's download buttons link to.

Usage (from the repo root):
  .venv/bin/python scripts/build-pdf.py [output_dir] [--locale es]

One-time setup: .venv/bin/playwright install chromium --only-shell
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urljoin

import yaml
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

REPO_ROOT = Path(__file__).resolve().parent.parent
MKDOCS_CONFIG = REPO_ROOT / "mkdocs.yml"
# Generated per locale next to mkdocs.yml, because MkDocs resolves
# docs_dir, custom_dir and hooks relative to the config file's directory.
GENERATED_CONFIG = REPO_ROOT / ".mkdocs-pdf.yml"
PDF_STEM = "SANDARC-VEC-Manual"

TITLE = "SANDARC VEC Manual"
AUTHOR = "San Diego County Amateur Radio Council"

ANCHOR_TAG_RE = re.compile(r"<a\b[^>]*>", re.IGNORECASE)
HREF_RE = re.compile(r'(href=")([^"]*)(")', re.IGNORECASE)
# Fragments and anything already carrying a scheme are left alone.
ALREADY_RESOLVED = ("#", "//", "http://", "https://", "mailto:", "tel:", "data:")


def load_config() -> dict:
    """Parse mkdocs.yml, tolerating the custom tags MkDocs registers."""
    # SafeLoader chokes on !ENV / !relative; the PDF build only reads plain
    # scalars, so unknown tags can be ignored rather than resolved.
    loader = yaml.SafeLoader
    loader.add_multi_constructor("!", lambda l, s, n: None)
    return yaml.load(MKDOCS_CONFIG.read_text(encoding="utf-8"), Loader=loader)


def i18n_languages(config: dict) -> list[dict]:
    """Return the i18n plugin's buildable languages, default locale first.

    Raises KeyError if the i18n plugin is absent, since a silent fallback to
    an English-only PDF would quietly stop publishing the translated ones.
    """
    for plugin in config.get("plugins", []):
        if isinstance(plugin, dict) and "i18n" in plugin:
            languages = plugin["i18n"]["languages"]
            buildable = [lang for lang in languages if lang.get("build", True)]
            return sorted(buildable, key=lambda lang: not lang.get("default", False))
    raise KeyError("No 'i18n' plugin found in mkdocs.yml")


def locale_site_url(config: dict, language: dict) -> str:
    """Public URL of a locale's site — the default locale sits at the root."""
    site_url = config["site_url"]
    if language.get("default", False):
        return site_url
    return urljoin(site_url, f"{language['locale']}/")


def output_name(language: dict) -> str:
    """PDF filename for a locale, matching extra.pdf_downloads in mkdocs.yml."""
    if language.get("default", False):
        return f"{PDF_STEM}.pdf"
    return f"{PDF_STEM}-{language['locale']}.pdf"


def write_locale_config(config: dict, locale: str, site_dir: Path) -> None:
    """Write a one-locale copy of mkdocs.yml for MkDocs to build from."""
    for plugin in config["plugins"]:
        if isinstance(plugin, dict) and "i18n" in plugin:
            # build_only_locale flips this locale to default+build and every
            # other locale off, so it lands at the site root with a print page.
            plugin["i18n"]["build_only_locale"] = locale
    config["site_dir"] = str(site_dir)
    GENERATED_CONFIG.write_text(
        yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def build_site(site_dir: Path) -> Path:
    """Run mkdocs against the generated config and return its print page."""
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "-f", str(GENERATED_CONFIG)],
        cwd=REPO_ROOT,
        check=True,
    )
    # The offline plugin sets use_directory_urls: false, flattening the print
    # page to print_page.html; without it the page lands in print_page/.
    for candidate in (
        site_dir / "print_page.html",
        site_dir / "print_page" / "index.html",
    ):
        if candidate.exists():
            return candidate
    sys.exit("Print page not found in the build — is the print-site plugin enabled?")


def absolutize_anchor_links(print_page: Path, site_url: str) -> int:
    """Rewrite the print page's relative links to absolute site URLs.

    Chromium prints from a file:// URL, so a relative href would otherwise be
    baked into the PDF as a path on the build machine and be dead for every
    reader. Only <a> tags are touched: stylesheets, fonts and images must stay
    relative so they keep resolving out of the local site directory.

    Returns the number of links rewritten.
    """
    # Hrefs are relative to the print page's own directory, which is the site
    # root only when use_directory_urls flattened it to print_page.html.
    subdir = "print_page/" if print_page.parent.name == "print_page" else ""
    base = urljoin(site_url, subdir)

    rewritten = 0

    def resolve(match: re.Match) -> str:
        nonlocal rewritten
        prefix, url, suffix = match.groups()
        if not url or url.startswith(ALREADY_RESOLVED):
            return match.group(0)
        rewritten += 1
        return f"{prefix}{urljoin(base, url)}{suffix}"

    html = ANCHOR_TAG_RE.sub(
        lambda tag: HREF_RE.sub(resolve, tag.group(0)),
        print_page.read_text(encoding="utf-8"),
    )
    print_page.write_text(html, encoding="utf-8")
    return rewritten


def print_to_pdf(print_page: Path, raw_pdf: Path) -> None:
    """Print the assembled print page to PDF with headless Chromium."""
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
            tagged=True,  # Chromium only emits the outline for tagged PDFs
            outline=True,  # PDF bookmarks from the heading structure
        )
        browser.close()


def add_metadata(raw_pdf: Path, output: Path, language: dict) -> int:
    """Stamp title/author metadata onto the printed PDF and save it."""
    title = TITLE
    if not language.get("default", False):
        title = f"{TITLE} ({language['name']})"
    writer = PdfWriter(clone_from=PdfReader(raw_pdf))  # clone keeps the outline
    writer.add_metadata(
        {
            "/Title": title,
            "/Author": AUTHOR,
            "/Subject": "Volunteer Examiner Manual",
            "/Creator": "mkdocs-print-site-plugin + headless Chromium",
        }
    )
    with open(output, "wb") as f:
        writer.write(f)
    return len(writer.pages)


def build_locale_pdf(config: dict, language: dict, output_dir: Path) -> Path:
    """Build, print and stamp the PDF for one locale; return its path."""
    locale = language["locale"]
    output = output_dir / output_name(language)
    print(f"==> {locale}: mkdocs build")
    with tempfile.TemporaryDirectory() as tmp:
        site_dir = Path(tmp) / "site"
        write_locale_config(config, locale, site_dir)
        print_page = build_site(site_dir)
        links = absolutize_anchor_links(print_page, locale_site_url(config, language))
        print(f"==> {locale}: absolutized {links} relative links")
        raw_pdf = Path(tmp) / "raw.pdf"
        print_to_pdf(print_page, raw_pdf)
        pages = add_metadata(raw_pdf, output, language)
    print(f"==> wrote {output} ({pages} pages)")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=REPO_ROOT,
        type=Path,
        help="directory to write the PDFs into (default: repo root)",
    )
    parser.add_argument(
        "--locale",
        help="build only this locale instead of every configured language",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    config = load_config()
    languages = i18n_languages(config)
    if args.locale:
        languages = [lang for lang in languages if lang["locale"] == args.locale]
        if not languages:
            sys.exit(
                f"Locale {args.locale!r} is not a buildable language in mkdocs.yml"
            )

    try:
        for language in languages:
            # Re-parsed per locale: write_locale_config mutates the plugin dict.
            build_locale_pdf(load_config(), language, output_dir)
    finally:
        GENERATED_CONFIG.unlink(missing_ok=True)

    print(f"==> {len(languages)} PDF(s) in {output_dir}")


if __name__ == "__main__":
    main()
