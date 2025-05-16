#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import re
from collections.abc import Sequence
from pathlib import Path

MAGIC_RE = re.compile(rb'^\s*%%?[a-zA-Z]')
PLACEHOLDER = b'# MAGIC_PLACEHOLDER: '

def run(cmd: list[str]) -> int:
    print(f'Running: {" ".join(cmd)}')
    return subprocess.run(cmd, check=False).returncode

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

def restore_file(filename: Path) -> None:
    path = Path(filename)
    with path.open('rb') as f:
        lines = f.readlines()

    changed = False
    restored_lines = []

    for line in lines:
        if line.lstrip().startswith(PLACEHOLDER):
            restored_lines.append(line.replace(PLACEHOLDER, b'', 1))
            changed = True
        else:
            restored_lines.append(line)

    if changed:
        with path.open('wb') as f:
            f.writelines(restored_lines)
        print(f'Restored {path}')

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Sanitize IPython magics, run Black, then restore magics',
        allow_abbrev=False,
    )
    parser.add_argument('filenames', nargs='*', help='Files to process')
    args, unknown_args = parser.parse_known_args(argv)

    if not args.filenames:
        return 0

    for filename in args.filenames:
        sanitize_file(filename)

    
    black_cmd = ["black", *args.filenames, *unknown_args]
    black_result = subprocess.run(black_cmd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("black output:", black_result.stdout)
 

    for filename in args.filenames:
        restore_file(Path(filename))

    return black_result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
