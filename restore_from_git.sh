#!/bin/bash

# Script to restore PNG files that were converted to symlinks

echo "=== Restoring Original PNG Files from Git ==="
echo

cd /Users/djm/claude-projects/github-repos/fc-pro-collection

# Find all broken symlinks and restore them from git
echo "Finding and restoring broken symlinks..."

restored_count=0
failed_count=0

# Process each broken symlink
find layers -type l ! -exec test -e {} \; -print | while read symlink; do
    echo -n "Restoring $symlink... "
    
    # Remove the broken symlink
    rm "$symlink"
    
    # Restore the file from the commit before symlinks were created
    if git checkout 350ee63386b57ff252753b86d0caf07f47b5a7ed -- "$symlink" 2>/dev/null; then
        echo "✓"
        ((restored_count++))
    else
        echo "✗ (file may be new)"
        ((failed_count++))
    fi
done

echo
echo "Restoration complete!"
echo "Files restored: Check git status"
echo

# Show what was restored
echo "Restored files summary:"
git status --porcelain | grep "^M " | wc -l | xargs echo "Modified files:"
git status --porcelain | grep "^?? " | wc -l | xargs echo "Untracked files:"