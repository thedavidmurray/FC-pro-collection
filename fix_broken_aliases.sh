#!/bin/bash

# Script to fix broken symbolic links in the fc-pro-collection layers directory

echo "Finding and removing broken symbolic links in layers directory..."

# Change to the layers directory
cd /Users/djm/claude-projects/github-repos/fc-pro-collection/layers

# Find all broken symbolic links and count them
broken_count=$(find . -type l ! -exec test -e {} \; -print | wc -l)
echo "Found $broken_count broken symbolic links"

# List them first
echo "Broken links to be removed:"
find . -type l ! -exec test -e {} \; -print

# Ask for confirmation
read -p "Do you want to remove all broken symbolic links? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Remove all broken symbolic links
    find . -type l ! -exec test -e {} \; -delete
    echo "Removed all broken symbolic links"
    
    # Count remaining files
    remaining=$(find . -name "*.png" -type f | wc -l)
    echo "Remaining actual PNG files: $remaining"
else
    echo "Operation cancelled"
fi