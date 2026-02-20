#!/usr/bin/env python3
"""
generate_all.py
Runner script: imports and executes all gen_*.py visualization scripts.

Creates the ../images/ directory if needed, runs each script in sequence,
reports success/failure for each, and prints a summary at the end.

Usage:
    cd slides/lecture-08/python && python generate_all.py
"""

import os
import sys
import importlib
import traceback

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, '..', 'images')

# All gen_* modules in order. Each must define a main() function.
SCRIPTS = [
    'gen_01_konigsberg',
    'gen_02_konigsberg_graph',
    'gen_03_euler_path',
    'gen_04_cayley_trees',
    'gen_05_parse_tree',
    'gen_06_random_graph',
    'gen_07_small_world',
    'gen_08_six_degrees',
    'gen_09_pagerank',
    'gen_10_pagerank_surfer',
    'gen_11_nn_architectures',
    'gen_12_attention',
    'gen_13_knowledge_graph',
    'gen_14_rag_pipeline',
    'gen_15_gnn_message',
    'gen_16_molecule',
    'gen_17_timeline',
    'gen_18_milgram_letters',
    'gen_19_graphrag_concept',
]


def run_script(module_name: str) -> bool:
    """Import and run a gen_* script. Returns True on success."""
    try:
        mod = importlib.import_module(module_name)
        if hasattr(mod, 'main'):
            mod.main()
        else:
            # Some scripts (e.g. gen_01) run at module level on import.
            # If already executed on import, nothing more to do.
            pass
        return True
    except Exception:
        traceback.print_exc()
        return False


def main():
    # Ensure images directory exists
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Add script directory to sys.path so imports resolve
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)

    total = len(SCRIPTS)
    successes = 0
    failures = []

    print(f'{"=" * 60}')
    print(f'  Generating {total} lecture-08 visualizations')
    print(f'  Output directory: {os.path.abspath(IMAGES_DIR)}')
    print(f'{"=" * 60}\n')

    for i, script_name in enumerate(SCRIPTS, 1):
        print(f'[{i}/{total}] Generating {script_name} ...')
        ok = run_script(script_name)
        if ok:
            print(f'        Done.\n')
            successes += 1
        else:
            print(f'        FAILED.\n')
            failures.append(script_name)

    # Summary
    print(f'{"=" * 60}')
    print(f'  Generated {successes}/{total} images successfully')
    if failures:
        print(f'  Failed: {", ".join(failures)}')
    print(f'{"=" * 60}')

    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
