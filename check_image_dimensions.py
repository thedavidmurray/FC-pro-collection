#!/usr/bin/env python3

import os
from PIL import Image
from collections import defaultdict

def check_background_dimensions():
    backgrounds_dir = "layers/Backgrounds"
    dimension_counts = defaultdict(int)
    non_600x600_files = []
    
    # Get all PNG files
    png_files = [f for f in os.listdir(backgrounds_dir) if f.endswith('.png')]
    
    print(f"Checking {len(png_files)} background images...\n")
    
    for filename in png_files:
        filepath = os.path.join(backgrounds_dir, filename)
        try:
            with Image.open(filepath) as img:
                width, height = img.size
                dimension_counts[f"{width}x{height}"] += 1
                
                if width != 600 or height != 600:
                    non_600x600_files.append({
                        'file': filename,
                        'size': f"{width}x{height}"
                    })
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    
    # Print summary
    print("Dimension Summary:")
    print("==================")
    for dimensions, count in sorted(dimension_counts.items()):
        print(f"{dimensions}: {count} files")
    
    # Print non-600x600 files
    if non_600x600_files:
        print(f"\nFiles NOT 600x600 ({len(non_600x600_files)} total):")
        print("=" * 50)
        for item in sorted(non_600x600_files, key=lambda x: x['file']):
            print(f"{item['file']:<50} {item['size']}")
    else:
        print("\n✅ All files are 600x600!")
    
    return non_600x600_files

if __name__ == "__main__":
    non_standard = check_background_dimensions()
    
    if non_standard:
        print(f"\nTotal files with non-standard dimensions: {len(non_standard)}")