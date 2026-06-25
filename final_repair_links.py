import os
import re

FILES = [
    'index.html',
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

def final_repair(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the "href=" missing error in all files
    # It seems some links look like: <a ... /index.html#... data-zh="...">
    # We want to restore href="/index.html#..."
    
    anchors = ['markets', 'solutions', 'technology', 'services', 'contact', 'products']
    for anchor in anchors:
        # Pattern to catch the missing href= part
        # Matches space followed by /index.html#anchor followed by space or data-
        content = re.sub(
            r' (?P<path>/index\.html#' + anchor + r')(?= | data-)',
            r' href="\1"',
            content
        )
        # Also catch just #products on index.html
        if file_path == 'index.html':
            content = re.sub(
                r' (?P<path>#products)(?= | data-)',
                r' href="\1"',
                content
            )

    # 2. Specific fix for the "Products" link which might have been mangled differently
    if file_path == 'index.html':
        # Ensure nav Products is href="#products"
        content = re.sub(
            r'href="/index\.html#products"',
            r'href="#products"',
            content
        )
    
    # 3. Clean up any href="href="...""
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    
    # 4. Final verification of the specific line 244 in index.html
    if file_path == 'index.html':
        content = re.sub(
            r'href="/products/index\.html"([^>]*?data-i18n="nav_products")',
            r'href="#products"\1',
            content
        )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Repaired: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        final_repair(f)
