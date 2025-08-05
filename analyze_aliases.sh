#!/bin/bash

# Script to analyze the alias situation in fc-pro-collection

echo "=== FC Pro Collection Alias Analysis ==="
echo

cd /Users/djm/claude-projects/github-repos/fc-pro-collection/layers

# Count files by type
echo "File type summary:"
echo "=================="
total_dirs=$(find . -type d | wc -l)
total_files=$(find . -type f -name "*.png" | wc -l)
total_symlinks=$(find . -type l | wc -l)
broken_symlinks=$(find . -type l ! -exec test -e {} \; -print | wc -l)
working_symlinks=$((total_symlinks - broken_symlinks))

echo "Directories: $total_dirs"
echo "Real PNG files: $total_files"
echo "Total symbolic links: $total_symlinks"
echo "  - Working: $working_symlinks"
echo "  - Broken: $broken_symlinks"
echo

# Check where broken symlinks point to
echo "Broken symlinks target analysis:"
echo "================================"
echo "First 10 broken symlinks and their targets:"
find . -type l ! -exec test -e {} \; -print | head -10 | while read link; do
    target=$(readlink "$link")
    echo "$link -> $target"
done
echo

# Count by layer
echo "Broken symlinks by layer:"
echo "========================"
for dir in */; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -type l ! -exec test -e {} \; -print 2>/dev/null | wc -l)
        if [ $count -gt 0 ]; then
            printf "%-20s %d broken links\n" "$dir" "$count"
        fi
    fi
done
echo

# Check file patterns
echo "File patterns with broken links:"
echo "================================"
echo "Filter patterns found:"
find . -type l ! -exec test -e {} \; -print | grep -E "_orig#|_hue#|_blur#|_sepia#" | wc -l | xargs echo "  Filtered versions (_orig, _hue, _blur, _sepia):"
find . -type l ! -exec test -e {} \; -print | grep -v -E "_orig#|_hue#|_blur#|_sepia#" | wc -l | xargs echo "  Regular files:"