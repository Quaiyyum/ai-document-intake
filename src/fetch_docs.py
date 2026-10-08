"""Checks (and optionally downloads) every real document listed in data/sources.md.

    python -m src.fetch_docs              # verify the files are present, write the manifest
    python -m src.fetch_docs --download   # also download any missing file from its URL
    python -m src.fetch_docs --print      # or print each missing web page to PDF with headless Chrome

Downloaded documents are third-party material and are never committed (data/raw/ is gitignored).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

from .common import RAW_DIR, sha256_file
from .manifest import load_manifest, make_row, save_manifest

SOURCES = Path("data/sources.md")
USER_AGENT = "ai-document-intake portfolio project (polite, 1 request per 2s)"
DELAY_SECONDS = 2
CHROME = os.getenv("CHROME_PATH") or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def print_to_pdf(url: str, target: Path) -> None:
    """Save a public web page as a PDF, the same as File > Print > Save as PDF."""
    if not Path(CHROME).exists():
        raise SystemExit(f"Chrome not found at {CHROME}; set CHROME_PATH to your Chrome or Chromium binary")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
         f"--print-to-pdf={target.resolve()}", url],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
    )


def parse_sources(path: Path = SOURCES) -> list[dict]:
    """Read the markdown table whose header row starts with doc_id."""
    rows, header = [], None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if header is None:
            if cells and cells[0] == "doc_id":
                header = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--print", dest="print_pdf", action="store_true")
    parser.add_argument("--folder", default="tender", help="sub-folder of data/raw the files live in")
    args = parser.parse_args(argv)

    manifest = {row["doc_id"]: row for row in load_manifest()}
    missing, mismatched = [], []
    for source in parse_sources():
        target = RAW_DIR / args.folder / source["file_name"]
        if not target.exists() and args.download:
            target.parent.mkdir(parents=True, exist_ok=True)
            response = requests.get(source["url"], headers={"User-Agent": USER_AGENT}, timeout=60)
            response.raise_for_status()
            target.write_bytes(response.content)
            print(f"downloaded {target}")
            time.sleep(DELAY_SECONDS)
        if not target.exists() and args.print_pdf:
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                print_to_pdf(source["url"], target)
                print(f"printed {target}")
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
                print(f"FAILED {source['url']}: {error}", file=sys.stderr)
            time.sleep(DELAY_SECONDS)
        if not target.exists():
            missing.append(target.as_posix())
            continue
        expected = (source.get("sha256") or "").strip()
        if expected and expected != sha256_file(target):
            mismatched.append(target.as_posix())
        if source["doc_id"] not in manifest:  # received_at is recorded once and never rewritten
            manifest[source["doc_id"]] = make_row(source["doc_id"], target)
    save_manifest(list(manifest.values()))
    print(f"manifest: {len(manifest)} rows")
    for name in missing:
        print(f"MISSING  {name}", file=sys.stderr)
    for name in mismatched:
        print(f"SHA256 DIFFERS FROM sources.md  {name}", file=sys.stderr)
    return 1 if missing or mismatched else 0


if __name__ == "__main__":
    sys.exit(main())
