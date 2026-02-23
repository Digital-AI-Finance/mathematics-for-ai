#!/usr/bin/env python3
"""
download_portraits.py
Downloads 8 public domain portraits from Wikimedia Commons for the
Five Pillars presentation.

Usage:
    cd slides/lecture-new/python && python download_portraits.py
"""

import os
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PORTRAITS_DIR = os.path.join(SCRIPT_DIR, '..', 'images', 'portraits')

# Portrait definitions: (filename, url, description)
PORTRAITS = [
    (
        'grassmann-1860.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Hermann_Grassmann.jpg/440px-Hermann_Grassmann.jpg',
        'Hermann Grassmann portrait',
    ),
    (
        'pascal-1663.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Blaise_Pascal_Versailles.JPG/440px-Blaise_Pascal_Versailles.JPG',
        'Blaise Pascal (Versailles portrait by Quesnel)',
    ),
    (
        'newton-1689.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/GodfreyKneller-IsaacNewton-1689.jpg/440px-GodfreyKneller-IsaacNewton-1689.jpg',
        'Isaac Newton (Kneller 1689)',
    ),
    (
        'leibniz-1695.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Gottfried_Wilhelm_von_Leibniz.jpg/440px-Gottfried_Wilhelm_von_Leibniz.jpg',
        'Gottfried Leibniz (Francke portrait)',
    ),
    (
        'shannon-1963.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/ClaudeShannon_MFO3807.jpg/440px-ClaudeShannon_MFO3807.jpg',
        'Claude Shannon at Bell Labs',
    ),
    (
        'hinton-2024.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Geoffrey_Hinton_Royal_Society.jpg/440px-Geoffrey_Hinton_Royal_Society.jpg',
        'Geoffrey Hinton (Nobel laureate)',
    ),
    (
        'cayley-1883.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Arthur_Cayley.jpg/440px-Arthur_Cayley.jpg',
        'Arthur Cayley engraving',
    ),
    (
        'bayes.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Thomas_Bayes.gif/440px-Thomas_Bayes.gif',
        'Thomas Bayes (disputed portrait)',
    ),
]


def download_portrait(filename: str, url: str, description: str, dest_dir: str) -> bool:
    """Download a single portrait. Returns True on success."""
    dest_path = os.path.join(dest_dir, filename)
    try:
        print(f'  Downloading {filename} ({description}) ...')
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        with open(dest_path, 'wb') as f:
            f.write(data)
        size_kb = len(data) / 1024
        print(f'    Saved {filename} ({size_kb:.1f} KB)')
        return True
    except Exception as exc:
        print(f'    WARNING: Failed to download {filename}: {exc}')
        print(f'    Manual download: {url}')
        print(f'    Save to: {dest_path}')
        return False


def main():
    os.makedirs(PORTRAITS_DIR, exist_ok=True)

    total = len(PORTRAITS)
    successes = 0
    failures = []

    print(f'{"=" * 60}')
    print(f'  Downloading {total} portraits')
    print(f'  Output directory: {os.path.abspath(PORTRAITS_DIR)}')
    print(f'{"=" * 60}\n')

    for filename, url, description in PORTRAITS:
        ok = download_portrait(filename, url, description, PORTRAITS_DIR)
        if ok:
            successes += 1
        else:
            failures.append(filename)
        print()

    print(f'{"=" * 60}')
    print(f'  Downloaded {successes}/{total} portraits successfully')
    if failures:
        print(f'  Failed: {", ".join(failures)}')
        print(f'  See warnings above for manual download instructions.')
    print(f'{"=" * 60}')

    return 0 if not failures else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
