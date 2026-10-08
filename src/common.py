"""Small helpers shared by every module. Nothing here knows about any document type."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

NZ = ZoneInfo("Pacific/Auckland")
TS_FORMAT = "%Y-%m-%d %H:%M"

RAW_DIR = Path("data/raw")
MANIFEST = RAW_DIR / "manifest.csv"
OUTPUT_DIR = Path("output")
EXTRACTED = OUTPUT_DIR / "extracted.json"
REVIEW_QUEUE = OUTPUT_DIR / "review_queue.csv"
DB_PATH = OUTPUT_DIR / "intake.db"
CACHE_DIR = OUTPUT_DIR / "llm_cache"


def now_nz() -> str:
    return datetime.now(NZ).strftime(TS_FORMAT)


def mtime_nz(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, NZ).strftime(TS_FORMAT)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def squash(text: str | None) -> str:
    """Lower-case and collapse whitespace, for tolerant text comparison."""
    return re.sub(r"\s+", " ", text or "").strip().lower()


def load_records(path: Path = EXTRACTED) -> dict[str, dict]:
    if not Path(path).exists():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_records(records: dict[str, dict], path: Path = EXTRACTED) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    ordered = {key: records[key] for key in sorted(records)}
    Path(path).write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
