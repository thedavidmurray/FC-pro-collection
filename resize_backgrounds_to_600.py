#!/usr/bin/env python3

import os
from PIL import Image
import shutil

def resize_backgrounds_to_600x600():
    backgrounds_dir = "layers/Backgrounds"
    backup_dir = "layers/Backgrounds_backup_dimensions"
    
    # Create backup directory
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created backup directory: {backup_dir}")
    
    resized_count = 0
    already_correct = 0
    
    # Get all PNG files
    png_files = [f for f in os.listdir(backgrounds_dir) if f.endswith('.png')]
    
    print(f"Processing {len(png_files)} background images...\n")
    
    for filename in png_files:
        filepath = os.path.join(backgrounds_dir, filename)
        backup_path = os.path.join(backup_dir, filename)
        
        try:
            with Image.open(filepath) as img:
                width, height = img.size
                
                if width == 600 and height == 600:
                    already_correct += 1
                    continue
                
                # Backup original
                shutil.copy2(filepath, backup_path)
                
                # Create new 600x600 image
                new_img = Image.new('RGBA', (600, 600), (0, 0, 0, 0))
                
                # Calculate position to center the image
                if width <= 600 and height <= 600:
                    # Image fits, center it
                    x_offset = (600 - width) // 2
                    y_offset = (600 - height) // 2
                    new_img.paste(img, (x_offset, y_offset))
                else:
                    # Image is larger, resize to fit
                    img.thumbnail((600, 600), Image.Resampling.LANCZOS)
                    x_offset = (600 - img.width) // 2
                    y_offset = (600 - img.height) // 2
                    new_img.paste(img, (x_offset, y_offset))
                
                # Save resized image
                new_img.save(filepath, 'PNG')
                resized_count += 1
                print(f"Resized: {filename} ({width}x{height} → 600x600)")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"\nSummary:")
    print(f"========")
    print(f"Already 600x600: {already_correct}")
    print(f"Resized: {resized_count}")
    print(f"Total: {len(png_files)}")
    print(f"\nOriginals backed up to: {backup_dir}")

if __name__ == "__main__":
    response = input("This will resize all background images to 600x600. Originals will be backed up. Continue? (y/n): ")
    if response.lower() == 'y':
        resize_backgrounds_to_600x600()
    else:
        print("Operation cancelled.")