#!/usr/bin/env python3
"""
Fix missing variations for backgrounds that have none
This addresses the statistical spread issue by ensuring all backgrounds have proper variations
"""

import os
import random
import subprocess
from pathlib import Path
import json

# Configuration
LAYERS_DIR = Path("/Users/djm/claude-projects/github-repos/fc-pro-collection/layers")
BACKGROUNDS_DIR = LAYERS_DIR / "Backgrounds"

# Color definitions with RGB direction vectors and ranges
COLOR_FILTERS = {
    "gold": {
        "base_rgb": (255, 215, 0),  # Gold base color
        "variance": 30,  # How much to vary each channel
        "opacity_range": (60, 80),  # Opacity range for the filter
        "variations": 2,  # Number of gold variations
    },
    "purple": {
        "base_rgb": (147, 0, 211),  # Purple base color
        "variance": 40,
        "opacity_range": (50, 70),
        "variations": 2,
    },
    "green": {
        "base_rgb": (0, 255, 0),  # Green base color
        "variance": 50,
        "opacity_range": (40, 60),
        "variations": 1,
    },
    "blue": {
        "base_rgb": (0, 100, 255),  # Blue base color
        "variance": 40,
        "opacity_range": (45, 65),
        "variations": 1,
    },
    "warm": {
        "base_rgb": (255, 150, 50),  # Warm orange
        "variance": 35,
        "opacity_range": (50, 70),
        "variations": 1,
    },
    "cool": {
        "base_rgb": (50, 150, 255),  # Cool blue
        "variance": 35,
        "opacity_range": (50, 70),
        "variations": 1,
    },
}


def generate_random_color_filter(base_rgb, variance):
    """Generate a randomized RGB value in the direction of the base color"""
    r, g, b = base_rgb

    # Add random variance to each channel
    r = max(0, min(255, r + random.randint(-variance, variance)))
    g = max(0, min(255, g + random.randint(-variance, variance)))
    b = max(0, min(255, b + random.randint(-variance, variance)))

    return (r, g, b)


def create_color_variation(input_file, output_file, color_name, filter_config):
    """Create a color variation using ImageMagick"""
    r, g, b = generate_random_color_filter(
        filter_config["base_rgb"], filter_config["variance"]
    )
    opacity = random.randint(*filter_config["opacity_range"])

    # Convert RGB to hex for ImageMagick
    hex_color = f"#{r:02x}{g:02x}{b:02x}"

    # Build ImageMagick command to create colored overlay
    cmd = [
        "magick",
        str(input_file),
        "(",
        str(input_file),
        "-fill",
        hex_color,
        "-colorize",
        f"{opacity}%",
        ")",
        "-compose",
        "overlay",
        "-composite",
        str(output_file),
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR creating {color_name} variation: {e}")
        return False


def create_effect_variations(input_file, base_name, rarity):
    """Create non-color effect variations"""
    variations_created = 0

    # Blur variation
    blur_file = BACKGROUNDS_DIR / f"{base_name}_blur#{rarity}.png"
    cmd = ["magick", str(input_file), "-blur", "0x8", str(blur_file)]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        variations_created += 1
    except:
        pass

    # Noise variation
    noise_file = BACKGROUNDS_DIR / f"{base_name}_noise#{rarity}.png"
    cmd = [
        "magick",
        str(input_file),
        "-attenuate",
        "0.5",
        "+noise",
        "gaussian",
        str(noise_file),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        variations_created += 1
    except:
        pass

    # Gradient diagonal overlay
    grad_file = BACKGROUNDS_DIR / f"{base_name}_gradient#{rarity}.png"
    cmd = [
        "magick",
        str(input_file),
        "(",
        "-size",
        "600x600",
        "gradient:black-white",
        "-rotate",
        "45",
        ")",
        "-compose",
        "overlay",
        "-composite",
        "-modulate",
        "100,100,100",
        str(grad_file),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        variations_created += 1
    except:
        pass

    return variations_created


def find_backgrounds_without_variations():
    """Find backgrounds that have no variations"""
    from collections import defaultdict

    # Get all background files
    backgrounds = list(BACKGROUNDS_DIR.glob("*.png"))

    # Group backgrounds by base name
    base_groups = defaultdict(list)
    for bg in backgrounds:
        # Extract base name (before underscore or just before #)
        name = bg.stem
        if "_" in name:
            base_name = name.split("_")[0]
        elif "#" in name:
            base_name = name.split("#")[0]
        else:
            base_name = name
        base_groups[base_name].append(bg)

    # Find singles (no variations)
    singles = []
    for base_name, variants in base_groups.items():
        if len(variants) == 1:
            singles.append(variants[0])

    return singles


def process_background(background_file):
    """Process a single background file and create all variations"""
    # Extract base name and rarity
    filename = background_file.stem
    if "#" in filename:
        base_name, rarity = filename.rsplit("#", 1)
    else:
        base_name = filename
        rarity = "10"

    variations_created = 0

    # Create color variations
    for color_name, config in COLOR_FILTERS.items():
        for i in range(config["variations"]):
            # Create unique suffix for multiple variations of same color
            suffix = (
                f"_{color_name}{i+1}" if config["variations"] > 1 else f"_{color_name}"
            )
            output_file = BACKGROUNDS_DIR / f"{base_name}{suffix}#{rarity}.png"

            # Skip if already exists
            if output_file.exists():
                continue

            if create_color_variation(background_file, output_file, color_name, config):
                variations_created += 1

    # Create effect variations
    variations_created += create_effect_variations(background_file, base_name, rarity)

    return variations_created


def main():
    print("=== Fixing Missing Background Variations ===")
    print(f"Working directory: {BACKGROUNDS_DIR}")

    # Find backgrounds without variations
    singles = find_backgrounds_without_variations()
    print(f"\nFound {len(singles)} backgrounds without variations")

    if not singles:
        print("All backgrounds already have variations!")
        return

    # Process each background
    total_variations_created = 0
    successful_backgrounds = 0

    print("\nGenerating variations for backgrounds without any...")
    for i, bg_file in enumerate(singles):
        base_name = bg_file.stem.split("#")[0]
        print(f"\n[{i+1}/{len(singles)}] Processing: {base_name}")

        variations = process_background(bg_file)
        if variations > 0:
            successful_backgrounds += 1
            total_variations_created += variations
            print(f"  ✓ Created {variations} variations")
        else:
            print(f"  ✗ Failed to create variations")

    # Final statistics
    print("\n=== Summary ===")
    print(f"Processed {len(singles)} backgrounds")
    print(f"Successfully created variations for {successful_backgrounds} backgrounds")
    print(f"Total new variations created: {total_variations_created}")

    # Re-analyze to show new distribution
    all_files = list(BACKGROUNDS_DIR.glob("*.png"))
    from collections import defaultdict

    base_groups = defaultdict(list)
    for bg in all_files:
        name = bg.stem
        if "_" in name:
            base_name = name.split("_")[0]
        elif "#" in name:
            base_name = name.split("#")[0]
        else:
            base_name = name
        base_groups[base_name].append(bg)

    variation_counts = [len(variants) for variants in base_groups.values()]
    avg_variants = (
        sum(variation_counts) / len(variation_counts) if variation_counts else 0
    )

    # Count gold and purple
    gold_count = sum(1 for f in all_files if "_gold" in f.stem)
    purple_count = sum(1 for f in all_files if "_purple" in f.stem)

    print(f"\n=== New Distribution ===")
    print(f"Total files: {len(all_files)}")
    print(f"Base backgrounds: {len(base_groups)}")
    print(f"Average variations per background: {avg_variants:.1f}")
    print(f"Gold variations: {gold_count} (expected ~{len(base_groups)*2})")
    print(f"Purple variations: {purple_count} (expected ~{len(base_groups)*2})")

    # Check if any still have no variations
    new_singles = [name for name, variants in base_groups.items() if len(variants) == 1]
    if new_singles:
        print(f"\n⚠️  Still {len(new_singles)} backgrounds without variations")
        for s in new_singles[:5]:
            print(f"  - {s}")
    else:
        print(f"\n✅ All backgrounds now have variations!")


if __name__ == "__main__":
    main()
