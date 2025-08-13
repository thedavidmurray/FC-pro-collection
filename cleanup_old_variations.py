#!/usr/bin/env python3
"""
Clean up old background variations to prepare for new generation
"""

import os
from pathlib import Path
import shutil

LAYERS_DIR = Path("/Users/djm/claude-projects/github-repos/fc-pro-collection/layers")
BACKGROUNDS_DIR = LAYERS_DIR / "Backgrounds"
BACKUP_DIR = LAYERS_DIR / "Backgrounds_backup_old"

# Patterns to identify variations (not base files)
VARIATION_PATTERNS = ["_blur_", "_grad_", "_hue_", "_sat_", "_temp_", "_noise"]


def main():
    print("=== Cleaning Old Background Variations ===")

    # Create backup of current state
    if not BACKUP_DIR.exists():
        print(f"Creating backup at {BACKUP_DIR}")
        shutil.copytree(BACKGROUNDS_DIR, BACKUP_DIR)
        print("Backup created successfully")
    else:
        print(f"Backup already exists at {BACKUP_DIR}")

    # Find all variation files
    all_files = list(BACKGROUNDS_DIR.glob("*.png"))
    variation_files = []
    base_files = []

    for file in all_files:
        is_variation = any(pattern in file.stem for pattern in VARIATION_PATTERNS)
        if is_variation:
            variation_files.append(file)
        else:
            base_files.append(file)

    print(f"\nFound {len(base_files)} base backgrounds")
    print(f"Found {len(variation_files)} variation files to remove")

    # Confirm before deletion
    if variation_files:
        print(f"\nRemoving {len(variation_files)} old variation files...")
        for i, file in enumerate(variation_files):
            file.unlink()
            if i < 10 or i % 100 == 0:  # Show first 10 and every 100th
                print(f"  Removed: {file.name}")
        print(f"\n✓ Removed {len(variation_files)} variation files")

    # Final count
    remaining_files = len(list(BACKGROUNDS_DIR.glob("*.png")))
    print(f"\nRemaining files in Backgrounds: {remaining_files}")
    print("Ready for new variation generation!")


if __name__ == "__main__":
    main()
