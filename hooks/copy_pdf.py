"""
Ship the generated PDF manual with every build — no external dependencies.

scripts/build-pdf.py writes SANDARC-VEC-Manual.pdf to the repo root. The
site's "Download PDF" buttons (hero, sidebar, footer) link to that file at
the site root, but `mkdocs build` wipes and rebuilds site/ without it —
so a plain build + deploy shipped a site whose PDF links 404'd. This hook
copies the most recent PDF into the build output after every build,
covering `mkdocs build`, `mkdocs serve`, and scripts/build-pdf.py alike.

    hooks:
      - hooks/copy_pdf.py

If no PDF has been generated yet, the build still succeeds; a warning
notes that the download links will 404 until scripts/build-pdf.py runs.
"""

import logging
import shutil
from pathlib import Path

logger = logging.getLogger("mkdocs.hooks.copy_pdf")

PDF_NAME = "SANDARC-VEC-Manual.pdf"
REPO_ROOT = Path(__file__).resolve().parent.parent


def on_post_build(config, **kwargs):
    pdf = REPO_ROOT / PDF_NAME
    if not pdf.exists():
        logger.warning(
            f"{PDF_NAME} not found at the repo root; the site's Download PDF "
            "links will 404. Run scripts/build-pdf.py to generate it."
        )
        return
    shutil.copy2(pdf, Path(config["site_dir"]) / PDF_NAME)
    logger.info(f"Copied {PDF_NAME} into the site output.")
