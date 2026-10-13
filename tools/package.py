#!/usr/bin/env python3
"""Produce a clean single-skill ZIP accepted by qq-dsh-bot's registry."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'distilly-qq'


def package(destination):
    selected = [ROOT / f for f in ('SKILL.md', 'LICENSE', 'UPSTREAM.md')]
    selected += [p for directory in ('references', 'tools') for p in (ROOT / directory).rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
    with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(selected):
            archive.write(path, 'distilly-qq/' + path.relative_to(ROOT).as_posix())
    return len(selected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(f'Packaged {package(args.output)} files')
