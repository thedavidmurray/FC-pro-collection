#!/usr/bin/env python3
"""
Process remaining backgrounds in smaller batches
"""

import subprocess
from pathlib import Path
from collections import defaultdict
import time

BACKGROUNDS_DIR = Path("layers/Backgrounds")


def find_singles():
    """Find backgrounds without variations"""
    backgrounds = list(BACKGROUNDS_DIR.glob("*.png"))
    base_groups = defaultdict(list)

    for bg in backgrounds:
        name = bg.stem
        if "_" in name:
            base_name = name.split("_")[0]
        elif "#" in name:
            base_name = name.split("#")[0]
        else:
            base_name = name
        base_groups[base_name].append(bg)

    return [
        variants[0] for base_name, variants in base_groups.items() if len(variants) == 1
    ]


def create_minimal_variations(bg_file):
    """Create just gold and purple variations for a background"""
    filename = bg_file.stem
    if "#" in filename:
        base_name, rarity = filename.rsplit("#", 1)
    else:
        base_name = filename
        rarity = "10"

    created = 0

    # Create 2 gold variations
    for i in [1, 2]:
        output = BACKGROUNDS_DIR / f"{base_name}_gold{i}#{rarity}.png"
        if not output.exists():
            cmd = [
                "magick",
                str(bg_file),
                "(",
                str(bg_file),
                "-fill",
                "#FFD700",
                "-colorize",
                "65%",
                ")",
                "-compose",
                "overlay",
                "-composite",
                str(output),
            ]
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=5)
                created += 1
            except:
                pass

    # Create 2 purple variations
    for i in [1, 2]:
        output = BACKGROUNDS_DIR / f"{base_name}_purple{i}#{rarity}.png"
        if not output.exists():
            cmd = [
                "magick",
                str(bg_file),
                "(",
                str(bg_file),
                "-fill",
                "#9400D3",
                "-colorize",
                "60%",
                ")",
                "-compose",
                "overlay",
                "-composite",
                str(output),
            ]
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=5)
                created += 1
            except:
                pass

    return created


def main():
    print("=== Processing Remaining Backgrounds ===")

    singles = find_singles()
    print(f"Found {len(singles)} backgrounds without variations")

    if not singles:
        print("All backgrounds have variations!")
        return

    # Process in batches of 10
    batch_size = 10
    total_created = 0

    for i in range(0, len(singles), batch_size):
        batch = singles[i : i + batch_size]
        print(f"\nBatch {i//batch_size + 1}: Processing {len(batch)} backgrounds")

        for bg in batch:
            base_name = bg.stem.split("#")[0]
            created = create_minimal_variations(bg)
            if created > 0:
                print(f"  ✓ {base_name}: created {created} variations")
                total_created += created
            else:
                print(f"  ✗ {base_name}: failed")

        # Brief pause between batches
        time.sleep(1)

    print(f"\n=== Summary ===")
    print(f"Total variations created: {total_created}")

    # Final count
    all_files = list(BACKGROUNDS_DIR.glob("*.png"))
    gold_count = sum(1 for f in all_files if "_gold" in f.stem)
    purple_count = sum(1 for f in all_files if "_purple" in f.stem)

    print(f"\nFinal counts:")
    print(f"  Total files: {len(all_files)}")
    print(f"  Gold variations: {gold_count}")
    print(f"  Purple variations: {purple_count}")


if __name__ == "__main__":
    main()
