#!/usr/bin/env python3
"""
generate_doxygen_page_from_html.py

This script receives raw HTML content as a string via command line and
generates a `.dox` file suitable for Doxygen documentation.

What it does:
  1. Extracts the title from the first <h1> tag that starts with a 📌 marker.
  2. Updates all <img src="..."> tags to prepend a fixed relative path.
  3. Wraps the HTML content in a `\page` and `\htmlonly` block for Doxygen.
  4. Writes the result to a `.dox` output file with the specified page ID.

Usage:
    python3 generate_doxygen_page_from_html.py "<html_content>" output.dox page_id

Arguments:
    html_content   A string containing the raw HTML content (quoted if needed).
    output.dox     Path to the output file to be written.
    page_id        Doxygen page identifier used in the `\page` directive.

Example:
    python3 generate_doxygen_page_from_html.py "$(cat readme.html)" out.dox test_case_my_case

Note:
    The HTML content must include an <h1> tag like:
        <h1 id="...">📌 Title: My Test Case</h1>

Author:
    [Hélio Ribeiro Neto] — [2025/04/14]
"""

import sys
import re

def update_img_src(html_content):
    """
    Update all <img> tags to prepend a relative path to the 'src' attribute.

    Args:
        html_content (str): Raw HTML content.

    Returns:
        str: Modified HTML with updated image paths.
    """
    pattern = r'(<img\s+[^>]*?src=")([^"]+)(")'
    replacement = r'\1../../../tests/coreCase/\2\3'
    return re.sub(pattern, replacement, html_content)

# ▶️ Script entry point
if __name__ == "__main__":
    # ✅ Ensure correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: generate_doxygen_page_from_html.py '<html_content>' output.dox page_id")
        sys.exit(1)

    # 📥 Extract command-line arguments
    html_content = sys.argv[1]   # Raw HTML content as a single string
    output_path = sys.argv[2]    # Output file path (.dox)
    page_id = sys.argv[3]        # Doxygen page ID

    # 🔖 Extract title from the first <h1> tag containing 📌
    pattern = r'>📌.*?:\s*(.+?)</h1>'
    match = re.search(pattern, html_content)
    if not match:
        print("❌ Could not find a valid <h1> title with 📌 marker in the input HTML.")
        sys.exit(1)

    # 🛠 Update image paths in HTML
    html_content = update_img_src(html_content)

    # 🧱 Construct the .dox content
    dox_content = (
        "/**\n"
        f" * \\page {page_id} 📌 {match.group(1)}\n"
        " *\n"
        " * \\htmlonly\n"
        f"{html_content}\n"
        " * \\endhtmlonly\n"
        " */\n"
    )

    # 💾 Write to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dox_content)
    except Exception as e:
        print(f"❌ Failed to write output file: {e}")
        sys.exit(1)
