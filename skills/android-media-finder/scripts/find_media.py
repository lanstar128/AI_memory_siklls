#!/usr/bin/env python3
"""
Find recent screenshots or photos in Termux storage.
"""

import argparse
import os
from pathlib import Path
from typing import Iterable, List, Tuple


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}


def existing_dirs(paths: Iterable[Path]) -> List[Path]:
    return [p for p in paths if p.exists() and p.is_dir()]


def candidate_dirs(media_type: str) -> List[Path]:
    home = Path.home()
    base = [
        home / "storage" / "pictures" / "Screenshots",
        home / "storage" / "dcim" / "Camera",
        home / "storage" / "pictures",
        home / "storage" / "dcim",
        home / "storage" / "shared" / "Pictures" / "Screenshots",
        home / "storage" / "shared" / "DCIM" / "Camera",
        home / "storage" / "shared" / "Pictures",
    ]

    if media_type == "screenshot":
        paths = [
            home / "storage" / "pictures" / "Screenshots",
            home / "storage" / "shared" / "Pictures" / "Screenshots",
            home / "storage" / "pictures",
        ]
    elif media_type == "photo":
        paths = [
            home / "storage" / "dcim" / "Camera",
            home / "storage" / "shared" / "DCIM" / "Camera",
            home / "storage" / "dcim",
        ]
    else:
        paths = base

    return existing_dirs(paths)


def iter_files(paths: List[Path]) -> Iterable[Path]:
    for root in paths:
        for dirpath, _, filenames in os.walk(root):
            for name in filenames:
                path = Path(dirpath) / name
                if path.suffix.lower() in IMAGE_EXTS:
                    yield path


def newest_files(paths: List[Path], limit: int) -> List[Tuple[float, Path]]:
    items: List[Tuple[float, Path]] = []
    for path in iter_files(paths):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        items.append((mtime, path))
    items.sort(key=lambda x: x[0], reverse=True)
    return items[:limit]


def main() -> None:
    parser = argparse.ArgumentParser(description="Find recent screenshots or photos")
    parser.add_argument("--type", choices=["screenshot", "photo", "any"], default="any")
    parser.add_argument("--latest", action="store_true", help="Print only the latest file path")
    parser.add_argument("--limit", type=int, default=5, help="Limit results (default: 5)")
    args = parser.parse_args()

    dirs = candidate_dirs(args.type)
    if not dirs:
        raise SystemExit("No candidate directories found. Check Termux storage permissions.")

    limit = 1 if args.latest else max(1, args.limit)
    items = newest_files(dirs, limit=limit)
    if not items:
        raise SystemExit("No image files found in candidate directories.")

    for _, path in items:
        print(str(path))


if __name__ == "__main__":
    main()
