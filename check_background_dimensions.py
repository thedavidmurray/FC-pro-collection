#!/usr/bin/env python3
"""
Check dimensions of all background files
Ensure all are 600x600 pixels
"""

from pathlib import Path
from PIL import Image
from collections import defaultdict

BACKGROUNDS_DIR = Path(
    "/Users/djm/claude-projects/github-repos/fc-pro-collection/layers/Backgrounds"
)
EXPECTED_SIZE = (600, 600)


def check_dimensions():
    """Check all background file dimensions"""
    print("=== Background Dimension Check ===")
    print(f"Expected size: {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}")
    print(f"Directory: {BACKGROUNDS_DIR}\n")

    # Get all PNG files
    backgrounds = list(BACKGROUNDS_DIR.glob("*.png"))
    print(f"Total background files: {len(backgrounds)}\n")

    # Track dimensions
    dimension_groups = defaultdict(list)
    incorrect_files = []
    corrupted_files = []

    print("Checking dimensions...")
    for i, bg_file in enumerate(backgrounds):
        try:
            with Image.open(bg_file) as img:
                size = img.size
                dimension_groups[size].append(bg_file)

                if size != EXPECTED_SIZE:
                    incorrect_files.append((bg_file, size))

            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"  Checked {i + 1}/{len(backgrounds)} files...")

        except Exception as e:
            corrupted_files.append((bg_file, str(e)))

    print(f"\n=== Results ===")

    # Show dimension distribution
    print("\nDimension Distribution:")
    for size, files in sorted(
        dimension_groups.items(), key=lambda x: len(x[1]), reverse=True
    ):
        count = len(files)
        percentage = (count / len(backgrounds)) * 100
        status = "✅" if size == EXPECTED_SIZE else "❌"
        print(f"  {status} {size[0]}x{size[1]}: {count} files ({percentage:.1f}%)")

    # Report incorrect dimensions
    if incorrect_files:
        print(f"\n❌ Found {len(incorrect_files)} files with incorrect dimensions:")
        for file, size in incorrect_files[:10]:  # Show first 10
            print(f"  - {file.name}: {size[0]}x{size[1]}")
        if len(incorrect_files) > 10:
            print(f"  ... and {len(incorrect_files) - 10} more")
    else:
        print("\n✅ All files have correct dimensions (600x600)")

    # Report corrupted files
    if corrupted_files:
        print(f"\n⚠️ Found {len(corrupted_files)} corrupted/unreadable files:")
        for file, error in corrupted_files[:5]:
            print(f"  - {file.name}: {error}")

    # Generate fix script if needed
    if incorrect_files:
        print("\n=== Creating Fix Script ===")
        create_fix_script(incorrect_files)

    return len(incorrect_files) == 0 and len(corrupted_files) == 0


def create_fix_script(incorrect_files):
    """Create a script to resize incorrect files"""
    script_content = """#!/usr/bin/env python3
'''
Fix background dimensions to 600x600
'''
from PIL import Image
from pathlib import Path

files_to_fix = [
"""

    for file, size in incorrect_files:
        script_content += f'    ("{file.name}", {size}),\n'

    script_content += """
]

BACKGROUNDS_DIR = Path("/Users/djm/claude-projects/github-repos/fc-pro-collection/layers/Backgrounds")

print(f"Fixing {len(files_to_fix)} files...")

for filename, current_size in files_to_fix:
    file_path = BACKGROUNDS_DIR / filename
    if file_path.exists():
        try:
            # Open and resize
            img = Image.open(file_path)
            
            # Use high-quality resize
            resized = img.resize((600, 600), Image.Resampling.LANCZOS)
            
            # Save with same filename
            resized.save(file_path, "PNG")
            print(f"  ✓ Fixed {filename}: {current_size} -> (600, 600)")
        except Exception as e:
            print(f"  ✗ Failed to fix {filename}: {e}")
    else:
        print(f"  ⚠️ File not found: {filename}")

print("\\nDone!")
"""

    fix_script_path = Path("fix_background_dimensions.py")
    fix_script_path.write_text(script_content)
    print(f"Created fix script: {fix_script_path}")
    print("Run 'python3 fix_background_dimensions.py' to resize incorrect files")


def main():
    """Main function"""
    all_correct = check_dimensions()

    if all_correct:
        print("\n🎉 All backgrounds are properly sized at 600x600!")
    else:
        print("\n⚠️ Some backgrounds need to be resized to 600x600")
        print("Run the generated fix script to correct them.")


if __name__ == "__main__":
    main()
