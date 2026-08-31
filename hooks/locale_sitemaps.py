"""Write a per-locale sitemap.xml so the language selector can switch safely.

mkdocs-material's language selector fetches sitemap.xml from each alternate
language's base URL (e.g. /manual/es/sitemap.xml) to map the current page to
its translated counterpart. mkdocs-static-i18n only writes the one sitemap at
the site root, so those fetches 404 and Material falls back to navigating to
the locale base *without* a trailing slash (/manual/es). The trailing-slash
redirect upstream drops the /manual prefix, landing users on a 404 at /es/.
Publishing a sitemap per locale keeps Material on its happy path: switching
languages stays on the current page and never hits the redirect.
"""

import re
from pathlib import Path

# Matches one complete <url>...</url> entry in the root sitemap.
_URL_ENTRY = re.compile(r"<url>.*?</url>", re.DOTALL)


def on_post_build(config):
    """Split the root sitemap into one sitemap.xml per non-default locale."""
    site_dir = Path(config["site_dir"])
    root_sitemap = site_dir / "sitemap.xml"
    if not root_sitemap.exists():
        return

    text = root_sitemap.read_text(encoding="utf-8")
    entries = _URL_ENTRY.findall(text)
    header = text.split("<url>", 1)[0]
    site_url = config["site_url"].rstrip("/")

    for language in config["plugins"]["i18n"].config.languages:
        if language.default:
            continue
        locale_base = f"<loc>{site_url}/{language.locale}/"
        subset = [entry for entry in entries if locale_base in entry]
        if not subset:
            continue
        out = site_dir / language.locale / "sitemap.xml"
        out.write_text(header + "\n".join(subset) + "\n</urlset>", encoding="utf-8")
