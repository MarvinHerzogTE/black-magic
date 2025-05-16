#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from collections.abc import Sequence
from pathlib import Path


# Regex thatatches only magic commands
# - (starts with optional whitespace then % or %%)
# - immediately followed by a character (ignores legitimate python such as modulo operator)
MAGIC_RE = re.compile(rb'^\s*%%?[a-zA-Z]')
PLACEHOLDER = b'# MAGIC_PLACEHOLDER: '

def sanitize_file(filename: str) -> None:
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
        with path.open('wb') as f:
            f.writelines(new_lines)
        print(f'Sanitized {filename}')

def restore_file(path: Path) -> None:
    with path.open('rb') as f:
        lines = f.readlines()

    changed = False
    restored_lines = []

    for line in lines:
        if line.lstrip().startswith(PLACEHOLDER):
            # Replace only the matching placeholder lines
            restored_line = line.replace(PLACEHOLDER, b'', 1)
            restored_lines.append(restored_line)
            changed = True
        else:
            restored_lines.append(line)

    if changed:
        with path.open('wb') as f:
            f.writelines(restored_lines)
        print(f'Restored {path}')


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Comment or restore IPython magic lines')
    parser.add_argument('--restore', action='store_true', help='Restore original files from .magic.bak backups')
    parser.add_argument('filenames', nargs='*', help='Files to process')
    args = parser.parse_args(argv)

  
    for filename in args.filenames:
        if args.restore:
            restore_file(filename)
        else:
            sanitize_file(filename)
       
    # not a quality check, always pass
    return 0 

if __name__ == '__main__':
    raise SystemExit(main())
