#!/usr/bin/env python3
"""Spot-check rasters for broken-image alt text (Chrome shows alt when src fails)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STREAMS = [
    "01-agenda",
    "02-earth-observatory",
    "03-datalab",
    "04-datathon",
    "05-air4u-demo",
]
CHANNELS = [
    "linkedin",
    "facebook",
    "instagram",
    "story",
    "x",
    "whatsapp",
    "email",
    "web",
    "linkedin-carousel",
    "instagram-carousel",
]
# Alt strings used before embed fix — should not appear as dominant raster text.
BAD_SNIPPETS = ("CleantechHUB", "Datalab", "[img]", "broken", "alt=")


def sample_file(channel_dir: Path) -> Path | None:
    for sub in ("png", "jpg"):
        d = channel_dir / sub
        if not d.is_dir():
            continue
        files = sorted(d.glob("*.png" if sub == "png" else "*.jpg"))
        if files:
            return files[0]
    if (channel_dir / "carousel.pdf").is_file():
        return channel_dir / "carousel.pdf"
    return None


def check_png_jpg(path: Path) -> list[str]:
    issues: list[str] = []
    if path.suffix.lower() == ".pdf":
        data = path.read_bytes()
        if len(data) < 5000:
            issues.append("pdf too small")
        return issues
    try:
        from PIL import Image
        import io
    except ImportError:
        return ["PIL missing"]
    im = Image.open(path).convert("RGB")
    if max(im.size) < 100:
        issues.append("dimensions too small")
    # Heuristic: broken-image alt text often renders as flat color bands + text;
    # compare file size to a sane minimum for branded layouts.
    if path.stat().st_size < 8000:
        issues.append("file suspiciously small")
    raw = path.read_bytes()
    for snippet in BAD_SNIPPETS:
        if snippet.encode() in raw:
            issues.append(f"binary contains {snippet!r}")
    return issues


def main() -> int:
    checked: list[str] = []
    failures: list[str] = []
    for stream in STREAMS:
        for channel in CHANNELS:
            ch = ROOT / stream / channel
            if not ch.is_dir():
                continue
            sample = sample_file(ch)
            if not sample:
                failures.append(f"{stream}/{channel}: no raster")
                continue
            rel = sample.relative_to(ROOT)
            checked.append(str(rel))
            issues = check_png_jpg(sample)
            if issues:
                failures.append(f"{rel}: {', '.join(issues)}")
    print("CHECKED_FILES")
    for c in checked:
        print(c)
    if failures:
        print("FAILURES", file=sys.stderr)
        for f in failures:
            print(f, file=sys.stderr)
        return 1
    print(f"OK {len(checked)} samples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
