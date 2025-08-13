#!/usr/bin/env python3
"""
Analyze background similarity to identify duplicates or near-duplicates
Uses perceptual hashing and color histogram comparison
"""

import os
from pathlib import Path
from PIL import Image
import numpy as np
from collections import defaultdict
import imagehash
import json

BACKGROUNDS_DIR = Path(
    "/Users/djm/claude-projects/github-repos/fc-pro-collection/layers/Backgrounds"
)


def get_image_hash(image_path):
    """Get perceptual hash of an image"""
    try:
        img = Image.open(image_path)
        # Use multiple hash types for better comparison
        dhash = imagehash.dhash(img, hash_size=16)
        phash = imagehash.phash(img, hash_size=16)
        ahash = imagehash.average_hash(img, hash_size=16)
        return {
            "dhash": str(dhash),
            "phash": str(phash),
            "ahash": str(ahash),
            "combined": f"{dhash}{phash}{ahash}",
        }
    except Exception as e:
        print(f"Error hashing {image_path}: {e}")
        return None


def get_color_histogram(image_path, bins=64):
    """Get color histogram for an image"""
    try:
        img = Image.open(image_path).convert("RGB")
        # Reduce size for faster processing
        img.thumbnail((200, 200))

        # Get histogram for each channel
        hist_r = np.histogram(np.array(img)[:, :, 0], bins=bins, range=(0, 256))[0]
        hist_g = np.histogram(np.array(img)[:, :, 1], bins=bins, range=(0, 256))[0]
        hist_b = np.histogram(np.array(img)[:, :, 2], bins=bins, range=(0, 256))[0]

        # Normalize
        hist_r = hist_r / hist_r.sum()
        hist_g = hist_g / hist_g.sum()
        hist_b = hist_b / hist_b.sum()

        return np.concatenate([hist_r, hist_g, hist_b])
    except Exception as e:
        print(f"Error getting histogram for {image_path}: {e}")
        return None


def histogram_similarity(hist1, hist2):
    """Calculate similarity between two histograms using correlation"""
    if hist1 is None or hist2 is None:
        return 0
    return np.corrcoef(hist1, hist2)[0, 1]


def analyze_backgrounds():
    """Analyze all backgrounds for similarity"""
    print("=== Background Similarity Analysis ===\n")

    # Get all background files
    backgrounds = list(BACKGROUNDS_DIR.glob("*.png"))
    print(f"Found {len(backgrounds)} background files\n")

    # Group backgrounds by base name
    base_groups = defaultdict(list)
    for bg in backgrounds:
        # Extract base name (before underscore or #)
        name = bg.stem
        if "_" in name:
            base_name = name.split("_")[0]
        elif "#" in name:
            base_name = name.split("#")[0]
        else:
            base_name = name
        base_groups[base_name].append(bg)

    print(f"Found {len(base_groups)} unique base backgrounds\n")

    # Analyze each group
    similarity_report = {}
    too_similar_pairs = []

    print("Analyzing similarity within each background family...")
    for base_name, variants in base_groups.items():
        if len(variants) > 1:
            print(f"\n{base_name}: {len(variants)} variants")

            # Calculate hashes and histograms
            variant_data = {}
            for v in variants:
                variant_name = v.stem
                variant_data[variant_name] = {
                    "path": v,
                    "hash": get_image_hash(v),
                    "histogram": get_color_histogram(v),
                }

            # Compare variants within the group
            variant_names = list(variant_data.keys())
            high_similarity = []

            for i in range(len(variant_names)):
                for j in range(i + 1, len(variant_names)):
                    name1, name2 = variant_names[i], variant_names[j]
                    data1, data2 = variant_data[name1], variant_data[name2]

                    # Calculate hash distance
                    if data1["hash"] and data2["hash"]:
                        dhash_dist = imagehash.hex_to_hash(
                            data1["hash"]["dhash"]
                        ) - imagehash.hex_to_hash(data2["hash"]["dhash"])
                        phash_dist = imagehash.hex_to_hash(
                            data1["hash"]["phash"]
                        ) - imagehash.hex_to_hash(data2["hash"]["phash"])

                        # Calculate histogram similarity
                        hist_sim = histogram_similarity(
                            data1["histogram"], data2["histogram"]
                        )

                        # Flag if too similar
                        if dhash_dist < 10 and phash_dist < 10 and hist_sim > 0.95:
                            high_similarity.append(
                                {
                                    "pair": (name1, name2),
                                    "dhash_dist": dhash_dist,
                                    "phash_dist": phash_dist,
                                    "histogram_similarity": hist_sim,
                                }
                            )
                            too_similar_pairs.append((name1, name2))
                            print(f"  ⚠️  {name1} <-> {name2}")
                            print(
                                f"      Hash distance: dhash={dhash_dist}, phash={phash_dist}"
                            )
                            print(f"      Color similarity: {hist_sim:.2%}")

            if high_similarity:
                similarity_report[base_name] = high_similarity

    # Analyze across different base backgrounds
    print("\n\n=== Cross-Background Similarity Check ===")
    print("Checking if different backgrounds are too similar...\n")

    base_representatives = {}
    for base_name, variants in base_groups.items():
        # Use the base file as representative
        base_file = [v for v in variants if "#" in v.stem and not "_" in v.stem]
        if base_file:
            base_representatives[base_name] = {
                "path": base_file[0],
                "hash": get_image_hash(base_file[0]),
                "histogram": get_color_histogram(base_file[0]),
            }

    cross_similar = []
    base_names = list(base_representatives.keys())

    for i in range(len(base_names)):
        for j in range(i + 1, len(base_names)):
            name1, name2 = base_names[i], base_names[j]
            data1 = base_representatives[name1]
            data2 = base_representatives[name2]

            if data1["hash"] and data2["hash"]:
                dhash_dist = imagehash.hex_to_hash(
                    data1["hash"]["dhash"]
                ) - imagehash.hex_to_hash(data2["hash"]["dhash"])
                phash_dist = imagehash.hex_to_hash(
                    data1["hash"]["phash"]
                ) - imagehash.hex_to_hash(data2["hash"]["phash"])
                hist_sim = histogram_similarity(data1["histogram"], data2["histogram"])

                if dhash_dist < 15 and phash_dist < 15 and hist_sim > 0.90:
                    cross_similar.append(
                        {
                            "pair": (name1, name2),
                            "dhash_dist": dhash_dist,
                            "phash_dist": phash_dist,
                            "histogram_similarity": hist_sim,
                        }
                    )
                    print(f"⚠️  {name1} is very similar to {name2}")
                    print(f"    Hash distance: dhash={dhash_dist}, phash={phash_dist}")
                    print(f"    Color similarity: {hist_sim:.2%}")

    # Generate recommendations
    print("\n\n=== RECOMMENDATIONS ===\n")

    if too_similar_pairs:
        print(
            "🔴 Critical: These variant pairs are nearly identical and should be reviewed:"
        )
        for pair in too_similar_pairs[:10]:  # Show top 10
            print(f"  - {pair[0]}")
            print(f"    {pair[1]}")

        if len(too_similar_pairs) > 10:
            print(f"  ... and {len(too_similar_pairs) - 10} more pairs")

    if cross_similar:
        print("\n🟡 Warning: These different backgrounds might be too similar:")
        for item in cross_similar:
            print(
                f"  - {item['pair'][0]} <-> {item['pair'][1]} (similarity: {item['histogram_similarity']:.2%})"
            )

    # Save detailed report
    report_data = {
        "total_files": len(backgrounds),
        "base_backgrounds": len(base_groups),
        "variant_similarity_issues": similarity_report,
        "cross_background_similarity": [
            {
                "backgrounds": item["pair"],
                "metrics": {
                    "dhash_distance": int(item["dhash_dist"]),
                    "phash_distance": int(item["phash_dist"]),
                    "color_similarity": float(item["histogram_similarity"]),
                },
            }
            for item in cross_similar
        ],
        "too_similar_count": len(too_similar_pairs),
    }

    with open("background_similarity_report.json", "w") as f:
        json.dump(report_data, f, indent=2)

    print(f"\n✅ Detailed report saved to background_similarity_report.json")
    print(f"\nSummary:")
    print(f"  - Total backgrounds: {len(backgrounds)}")
    print(f"  - Base backgrounds: {len(base_groups)}")
    print(f"  - Variants per background: ~{len(backgrounds) // len(base_groups)}")
    print(f"  - Too similar pairs: {len(too_similar_pairs)}")
    print(f"  - Cross-similar backgrounds: {len(cross_similar)}")

    return report_data


if __name__ == "__main__":
    # Check dependencies
    try:
        import imagehash
    except ImportError:
        print("Installing required package: imagehash")
        os.system("pip3 install imagehash")
        import imagehash

    try:
        from PIL import Image
    except ImportError:
        print("Installing required package: Pillow")
        os.system("pip3 install Pillow")
        from PIL import Image

    analyze_backgrounds()
