---
name: android-media-finder
description: "在 Termux/Codex 环境中查找最近的 Android 照片或截图。用于用户要求定位、打开或分析手机截图/照片，或需要获取最新图片的文件路径时。"
---

# Android Media Finder

## Overview

Locate the newest screenshot or camera photo on Android (Termux storage) and return a concrete file path that can be opened or analyzed.

## Workflow

1. Identify the target type: `screenshot`, `photo`, or `any`.
2. Run the finder script to get the newest file path.
3. If the user wants analysis, open the file with the image viewer tool.

## Quick commands

Find the newest screenshot:
```bash
python3 ~/.codex/skills/android-media-finder/scripts/find_media.py --type screenshot --latest
```

Find the newest camera photo:
```bash
python3 ~/.codex/skills/android-media-finder/scripts/find_media.py --type photo --latest
```

List the 5 newest images of any type:
```bash
python3 ~/.codex/skills/android-media-finder/scripts/find_media.py --type any --limit 5
```

## Common paths this skill checks

- `~/storage/pictures/Screenshots`
- `~/storage/dcim/Camera`
- `~/storage/pictures`
- `~/storage/dcim`
- `~/storage/shared/DCIM/Camera`
- `~/storage/shared/Pictures/Screenshots`
- `~/storage/shared/Pictures`

## Notes

- If no images are found, ask the user where they saved the file.
- Prefer returning a single path so the user can confirm before analysis.

## Resources

### scripts/

- `scripts/find_media.py`: Locate newest screenshot/photo with stable paths for Codex tooling.
