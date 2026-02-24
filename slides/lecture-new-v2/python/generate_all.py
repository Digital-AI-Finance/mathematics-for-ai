#!/usr/bin/env python3
"""
generate_all.py
Runner script: imports and executes all gen_*.py visualization scripts.

Creates the ../images/ directory if needed, runs each script in sequence,
reports success/failure for each, and prints a summary at the end.

Usage:
    cd slides/lecture-new/python && python generate_all.py
"""

import os
import sys
import importlib
import traceback

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, '..', 'images')

# All gen_* modules in order. Each must define a main() function.
SCRIPTS = [
    'gen_01_five_pillars_overview',
    'gen_02_word_vectors',
    'gen_03_softmax',
    'gen_04_galton_board',
    'gen_05_gradient_descent',
    'gen_06_cross_entropy',
    'gen_07_shannon_diagram',
    'gen_08_optimizers',
    'gen_09_scaling_laws',
    'gen_10_convergence',
    'gen_11_timeline',
    'gen_12_embedding_space',
    'gen_13_loss_curve',
    'gen_14_attention_heatmap',
    'gen_15_hero_neural_net',
    'gen_16_token_pipeline',
    'gen_17_matrix_multiply',
    'gen_18_backprop_flow',
    'gen_19_radar_pillars',
    'gen_20_section_icons',
]


def run_script(module_name: str) -> bool:
    """Import and run a gen_* script. Returns True on success."""
    try:
        mod = importlib.import_module(module_name)
        if hasattr(mod, 'main'):
            mod.main()
        else:
            # Some scripts run at module level on import.
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
    print(f'  Generating {total} lecture-new visualizations')
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
