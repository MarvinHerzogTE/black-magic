#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from collections.abc import Sequence
from pathlib import Path

MAGIC_RE = re.compile(rb'^\s*%')
PLACEHOLDER = b'# MAGIC_PLACEHOLDER: '

def sanitize_file(filename: str) -> bool:
    path = Path(filename)
    with path.open('rb') as f:
        lines = f.readlines()

    changed = False
    new_lines = []
    for line in lines:
        if MAGIC_RE.match(line):
            new_lines.append(PLACEHOLDER + line)
            changed = True
        else:
            new_lines.append(line)

    if changed:
        backup = path.with_suffix(path.suffix + '.magic.bak')
        with backup.open('wb') as f:
            f.writelines(lines)
        with path.open('wb') as f:
            f.writelines(new_lines)
        print(f'Sanitized {filename}')
        return True
    return False

def restore_file(filename: str) -> bool:
    path = Path(filename)
    backup = path.with_suffix(path.suffix + '.magic.bak')
    if not backup.exists():
        return False
    with backup.open('rb') as f:
        original = f.read()
    with path.open('wb') as f:
        f.write(original)
    backup.unlink()
    print(f'Restored {filename}')
    return True

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Comment or restore IPython magic lines')
    parser.add_argument('--restore', action='store_true', help='Restore original files from .magic.bak backups')
    parser.add_argument('filenames', nargs='*', help='Files to process')
    args = parser.parse_args(argv)

    any_changed = False
    for filename in args.filenames:
        if args.restore:
            changed = restore_file(filename)
        else:
            changed = sanitize_file(filename)
        if changed:
            any_changed = True

    return 1 if any_changed else 0

if __name__ == '__main__':
    raise SystemExit(main())
