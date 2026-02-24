#!/usr/bin/env python3
"""
download_external.py
Downloads 4 external images (3 XKCD comics + 1 Wikimedia historical document)
for the Five Pillars presentation.

Usage:
    cd slides/lecture-new/python && python download_external.py
"""

import os
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXTERNAL_DIR = os.path.join(SCRIPT_DIR, '..', 'images', 'external')

EXTERNALS = [
    (
        'xkcd-machine-learning.png',
        'https://imgs.xkcd.com/comics/machine_learning.png',
        'XKCD #1838: Machine Learning (CC BY-NC 2.5)',
    ),
    (
        'xkcd-curve-fitting.png',
        'https://imgs.xkcd.com/comics/curve_fitting.png',
        'XKCD #2048: Curve-Fitting (CC BY-NC 2.5)',
    ),
    (
        'xkcd-frequentists-bayesians.png',
        'https://imgs.xkcd.com/comics/frequentists_vs_bayesians.png',
        'XKCD #1132: Frequentists vs Bayesians (CC BY-NC 2.5)',
    ),
    (
        'principia-title-page.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/e/e9/Principia_Mathematica_1713.JPG',
        'Newton Principia Mathematica title page (CC BY 4.0)',
    ),
]


def download_external(filename: str, url: str, description: str, dest_dir: str) -> bool:
    """Download a single external image. Returns True on success."""
    dest_path = os.path.join(dest_dir, filename)
    try:
        print(f'  Downloading {filename} ({description}) ...')
        req = urllib.request.Request(url, headers={'User-Agent': 'MathForAI-Slides/1.0 (educational presentation)'})
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
    os.makedirs(EXTERNAL_DIR, exist_ok=True)

    total = len(EXTERNALS)
    successes = 0
    failures = []

    print(f'{"=" * 60}')
    print(f'  Downloading {total} external images')
    print(f'  Output directory: {os.path.abspath(EXTERNAL_DIR)}')
    print(f'{"=" * 60}\n')

    for filename, url, description in EXTERNALS:
        ok = download_external(filename, url, description, EXTERNAL_DIR)
        if ok:
            successes += 1
        else:
            failures.append(filename)
        print()

    print(f'{"=" * 60}')
    print(f'  Downloaded {successes}/{total} external images successfully')
    if failures:
        print(f'  Failed: {", ".join(failures)}')
        print(f'  See warnings above for manual download instructions.')
    print(f'{"=" * 60}')

    return 0 if not failures else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
