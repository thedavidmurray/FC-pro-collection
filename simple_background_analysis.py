#!/usr/bin/env python3
"""
Simple background similarity analysis using file names and basic checks
"""

from pathlib import Path
from collections import defaultdict
import json

BACKGROUNDS_DIR = Path(
    "/Users/djm/claude-projects/github-repos/fc-pro-collection/layers/Backgrounds"
)


def analyze_backgrounds():
    """Analyze backgrounds based on naming patterns"""
    print("=== Background Similarity Analysis (Name-Based) ===\n")

    # Get all background files
    backgrounds = list(BACKGROUNDS_DIR.glob("*.png"))
    print(f"Found {len(backgrounds)} background files\n")

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

    print(f"Found {len(base_groups)} unique base backgrounds\n")

    # Analyze variation distribution
    variation_types = defaultdict(int)
    for bg in backgrounds:
        name = bg.stem
        if "_gold" in name:
            variation_types["gold"] += 1
        elif "_purple" in name:
            variation_types["purple"] += 1
        elif "_green" in name:
            variation_types["green"] += 1
        elif "_blue" in name:
            variation_types["blue"] += 1
        elif "_warm" in name:
            variation_types["warm"] += 1
        elif "_cool" in name:
            variation_types["cool"] += 1
        elif "_blur" in name:
            variation_types["blur"] += 1
        elif "_noise" in name:
            variation_types["noise"] += 1
        elif "_gradient" in name:
            variation_types["gradient"] += 1
        elif "#" in name and "_" not in name:
            variation_types["base"] += 1
        else:
            variation_types["other"] += 1

    print("=== Variation Type Distribution ===")
    for vtype, count in sorted(variation_types.items()):
        print(f"  {vtype:12s}: {count:3d} files")

    print("\n=== Background Families ===")

    # Sort by number of variants
    sorted_groups = sorted(base_groups.items(), key=lambda x: len(x[1]), reverse=True)

    # Show top backgrounds with most variants
    print("\nTop 10 backgrounds with most variants:")
    for base_name, variants in sorted_groups[:10]:
        print(f"  {base_name:30s}: {len(variants):2d} variants")

        # Check what variations exist
        has_gold = any("_gold" in v.stem for v in variants)
        has_purple = any("_purple" in v.stem for v in variants)
        has_effects = any(
            any(eff in v.stem for eff in ["_blur", "_noise", "_gradient"])
            for v in variants
        )

        status = []
        if has_gold:
            status.append("✓gold")
        if has_purple:
            status.append("✓purple")
        if has_effects:
            status.append("✓effects")

        if status:
            print(f"    [{', '.join(status)}]")

    print("\n=== Potential Issues ===")

    # Find backgrounds with duplicate color variations
    issues = []

    for base_name, variants in base_groups.items():
        variant_names = [v.stem for v in variants]

        # Check for multiple golds/purples of same type
        gold1_count = sum(1 for n in variant_names if "_gold1" in n)
        gold2_count = sum(1 for n in variant_names if "_gold2" in n)
        purple1_count = sum(1 for n in variant_names if "_purple1" in n)
        purple2_count = sum(1 for n in variant_names if "_purple2" in n)

        if gold1_count > 1 or gold2_count > 1:
            issues.append(f"{base_name} has duplicate gold variations")
        if purple1_count > 1 or purple2_count > 1:
            issues.append(f"{base_name} has duplicate purple variations")

    if issues:
        print("🔴 Found potential duplicates:")
        for issue in issues[:10]:
            print(f"  - {issue}")
    else:
        print("✅ No obvious duplicates found based on naming")

    # Check for similarly named backgrounds
    print("\n=== Similarly Named Backgrounds ===")
    base_names = list(base_groups.keys())
    similar_pairs = []

    for i in range(len(base_names)):
        for j in range(i + 1, len(base_names)):
            name1, name2 = base_names[i].lower(), base_names[j].lower()

            # Check if names are very similar
            if (name1 in name2 or name2 in name1) and name1 != name2:
                similar_pairs.append((base_names[i], base_names[j]))
            elif len(name1) > 5 and len(name2) > 5:
                # Check for common prefixes
                common_len = 0
                for k in range(min(len(name1), len(name2))):
                    if name1[k] == name2[k]:
                        common_len += 1
                    else:
                        break

                if common_len >= min(len(name1), len(name2)) * 0.7:
                    similar_pairs.append((base_names[i], base_names[j]))

    if similar_pairs:
        print("These backgrounds have similar names and might be visually similar:")
        for pair in similar_pairs[:10]:
            print(f"  - {pair[0]} <-> {pair[1]}")

    # Statistical analysis
    print("\n=== Statistical Analysis ===")

    variant_counts = [len(variants) for variants in base_groups.values()]
    avg_variants = sum(variant_counts) / len(variant_counts)
    max_variants = max(variant_counts)
    min_variants = min(variant_counts)

    print(f"  Average variants per background: {avg_variants:.1f}")
    print(f"  Maximum variants: {max_variants}")
    print(f"  Minimum variants: {min_variants}")

    # Find backgrounds with too few or too many variants
    print("\n  Backgrounds with only 1 file (no variants):")
    singles = [name for name, variants in base_groups.items() if len(variants) == 1]
    if singles:
        for s in singles[:5]:
            print(f"    - {s}")
        if len(singles) > 5:
            print(f"    ... and {len(singles) - 5} more")

    print(f"\n  Backgrounds with 10+ variants:")
    many = [(name, len(vars)) for name, vars in base_groups.items() if len(vars) >= 10]
    if many:
        for name, count in sorted(many, key=lambda x: x[1], reverse=True)[:5]:
            print(f"    - {name}: {count} variants")

    # Recommendations
    print("\n=== RECOMMENDATIONS ===\n")

    if variation_types.get("gold", 0) < len(base_groups) * 2:
        print(
            f"⚠️  Missing gold variations: Expected ~{len(base_groups)*2}, found {variation_types.get('gold', 0)}"
        )

    if variation_types.get("purple", 0) < len(base_groups) * 2:
        print(
            f"⚠️  Missing purple variations: Expected ~{len(base_groups)*2}, found {variation_types.get('purple', 0)}"
        )

    if singles:
        print(
            f"🔴 {len(singles)} backgrounds have no variations - consider generating variations for them"
        )

    if many and max_variants > avg_variants * 2:
        print(
            f"🟡 Some backgrounds have significantly more variants than average ({avg_variants:.1f})"
        )
        print(
            "   This might skew the distribution. Consider removing some redundant variations."
        )

    print(f"\n✅ Analysis complete!")

    return {
        "total_files": len(backgrounds),
        "base_backgrounds": len(base_groups),
        "variation_distribution": dict(variation_types),
        "avg_variants_per_background": avg_variants,
        "similar_named_pairs": similar_pairs,
    }


if __name__ == "__main__":
    analyze_backgrounds()
