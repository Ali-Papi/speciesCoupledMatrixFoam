#!/usr/bin/env python3
"""
generate_dox_indexes.py

This script recursively generates `.dox` index files for use with Doxygen
based on a given test directory structure. The goal is to automatically
build navigable index pages that reflect the folder hierarchy of test cases.

Behavior:
- For each directory that contains subdirectories but does NOT have a README.md,
  a `.dox` file is created listing its children as Doxygen subpages.
- This makes it easy to build hierarchical documentation without requiring manual
  index maintenance.

Usage:
    python3 generate_dox_indexes.py <tests_dir> <output_dir>

Arguments:
    tests_dir    Path to the root test directory to scan.
    output_dir   Path where the `.dox` index files should be generated.

Example:
    python3 generate_dox_indexes.py ./tests ./generated_dox_indexes

Author:
    [Hélio Ribeiro Neto] — [2025/04/14]
"""

import os
import sys

def clean_id(path):
    """
    Clean and normalize a directory path to be used as a valid Doxygen page ID.

    Converts a relative path like '../tests/case A' to 'tests_case_A'.

    Args:
        path (str): The original file system path.

    Returns:
        str: A normalized string suitable as a Doxygen \page or \subpage ID.
    """
    return path.replace("../", "").strip("/").replace("/", "_").replace(" ", "_")


def generate_dox_recursive(current_dir, rel_path, output_dir, parent_page=None):
    """
    Recursively traverse a directory tree and generate Doxygen .dox index pages
    for directories that contain subdirectories but no README.md.

    Args:
        current_dir (str): The full path of the current directory being processed.
        rel_path (str): The relative path from the root directory (for titles).
        output_dir (str): Directory where the generated .dox files will be stored.
        parent_page (str): Optional parent page ID (not currently used).
    """
    # Get sorted list of all items in the directory
    entries = sorted(os.listdir(current_dir))

    # Identify subdirectories (excluding hidden ones)
    subdirs = [d for d in entries if os.path.isdir(os.path.join(current_dir, d))]
    has_readme = 'README.md' in entries

    # Generate a page ID and output filename based on directory path
    page_id = clean_id(current_dir)
    dox_filename = os.path.join(output_dir, f"{page_id}.dox")

    # Only generate a .dox file if:
    # - The directory contains subdirectories (so there’s something to index)
    # - The directory does NOT contain a README.md (which would be the actual page)
    if subdirs and not has_readme:
        with open(dox_filename, 'w', encoding='utf-8') as f:
            page_title = rel_path.replace("/", " / ") if rel_path else "Tests"

            f.write(f"/** \\page {page_id} {page_title}\n")
            f.write(" * \\brief Auto-generated index page\n *\n")
            f.write(" * List of subpages:\n *\n")

            for subdir in subdirs:
                if not subdir.startswith('.'):
                    sub_path = os.path.join(current_dir, subdir)
                    sub_page_id = clean_id(sub_path)
                    f.write(f" * - \\subpage {sub_page_id}\n")

            f.write(" */\n")

    # Recursively process subdirectories (only if README.md is not present)
    if not has_readme:
        for subdir in subdirs:
            generate_dox_recursive(
                current_dir=os.path.join(current_dir, subdir),
                rel_path=f"{rel_path}/{subdir}" if rel_path else subdir,
                output_dir=output_dir,
                parent_page=page_id
            )


if __name__ == "__main__":
    # Validate CLI arguments
    if len(sys.argv) != 3:
        print("Usage: generate_dox_indexes.py <tests_dir> <output_dir>")
        sys.exit(1)

    tests_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # Start recursive generation
    generate_dox_recursive(tests_dir, rel_path="", output_dir=output_dir)
