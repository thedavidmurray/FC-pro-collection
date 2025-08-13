#!/usr/bin/env python3
"""
Create background variations with randomized RGB filters
Generates gold, purple, green, and other color variations with subtle randomization
"""

import os
import random
import subprocess
from pathlib import Path
import shutil

# Configuration
LAYERS_DIR = Path("/Users/djm/claude-projects/github-repos/fc-pro-collection/layers")
BACKGROUNDS_DIR = LAYERS_DIR / "Backgrounds"
BACKUP_DIR = LAYERS_DIR / "Backgrounds_backup"

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
        print(
            f"  Created {color_name} variation: {output_file.name} (RGB: {r},{g},{b}, opacity: {opacity}%)"
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR creating {color_name} variation: {e}")
        return False


def create_effect_variations(input_file, base_name, rarity):
    """Create non-color effect variations"""
    variations = []

    # Blur variation
    blur_file = BACKGROUNDS_DIR / f"{base_name}_blur#{rarity}.png"
    cmd = ["magick", str(input_file), "-blur", "0x8", str(blur_file)]
    if run_command(cmd):
        variations.append(blur_file)
        print(f"  Created blur variation")

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
    if run_command(cmd):
        variations.append(noise_file)
        print(f"  Created noise variation")

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
    if run_command(cmd):
        variations.append(grad_file)
        print(f"  Created gradient variation")

    return variations


def run_command(cmd):
    """Run a command and return success status"""
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Command failed: {' '.join(cmd)}")
        print(f"  Error: {e.stderr.decode() if e.stderr else 'Unknown error'}")
        return False


def process_background(background_file):
    """Process a single background file and create all variations"""
    # Extract base name and rarity
    filename = background_file.stem
    if "#" in filename:
        base_name, rarity = filename.rsplit("#", 1)
    else:
        base_name = filename
        rarity = "10"

    print(f"\nProcessing: {base_name}")

    # Create color variations
    created_files = []

    for color_name, config in COLOR_FILTERS.items():
        for i in range(config["variations"]):
            # Create unique suffix for multiple variations of same color
            suffix = (
                f"_{color_name}{i+1}" if config["variations"] > 1 else f"_{color_name}"
            )
            output_file = BACKGROUNDS_DIR / f"{base_name}{suffix}#{rarity}.png"

            if create_color_variation(background_file, output_file, color_name, config):
                created_files.append(output_file)

    # Create effect variations
    effect_files = create_effect_variations(background_file, base_name, rarity)
    created_files.extend(effect_files)

    return created_files


def get_best_backgrounds():
    """Get list of best backgrounds that make protardios POP"""
    # These are curated backgrounds that work well
    best_backgrounds = [
        "farcasterOG",
        "farcaster_sun",
        "higher horse",
        "AOL",
        "SuperAnon",
        "energy_zora",
        "destroyer",
        "gmfc",
        "degen_farcat",
        "Rainbro",
        "Lenny",
        "Background%AI",
        "DevBruv",
        "EggHole",
        "Farcats",
        "aethernet_mountain",
        "compass",
        "gold check",
        "Degen Golden Ticket",
        "chicago mentioned",
        "art",
        "cruising horse",
        "dat boi",
    ]

    return best_backgrounds


def main():
    print("=== Background Variation Generator ===")
    print(f"Working directory: {BACKGROUNDS_DIR}")

    # Create backup
    if not BACKUP_DIR.exists():
        print(f"Creating backup at {BACKUP_DIR}")
        shutil.copytree(BACKGROUNDS_DIR, BACKUP_DIR)

    # Get base background files (without variations)
    all_files = list(BACKGROUNDS_DIR.glob("*.png"))
    base_files = [
        f
        for f in all_files
        if not any(
            tag in f.stem
            for tag in [
                "_blur",
                "_noise",
                "_gradient",
                "_gold",
                "_purple",
                "_green",
                "_blue",
                "_warm",
                "_cool",
                "_hue",
                "_sat",
                "_temp",
                "_grad",
            ]
        )
    ]

    print(f"Found {len(base_files)} base backgrounds")

    # Get best backgrounds
    best_names = get_best_backgrounds()
    best_files = []

    for base_file in base_files:
        base_name = base_file.stem.split("#")[0].lower()
        if any(
            best.lower() in base_name or base_name in best.lower()
            for best in best_names
        ):
            best_files.append(base_file)

    print(f"Identified {len(best_files)} best backgrounds for variations")

    # Process best backgrounds first
    print("\n=== Processing Best Backgrounds ===")
    for bg_file in best_files:
        process_background(bg_file)

    # Process remaining backgrounds
    remaining = [f for f in base_files if f not in best_files]
    if remaining:
        print(f"\n=== Processing {len(remaining)} Remaining Backgrounds ===")
        for bg_file in remaining:
            process_background(bg_file)

    print("\n=== Complete ===")
    total_files = len(list(BACKGROUNDS_DIR.glob("*.png")))
    print(f"Total background files: {total_files}")


if __name__ == "__main__":
    main()
