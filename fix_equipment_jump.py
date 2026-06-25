import os
import re

# Target files
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

def fix_navigation(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if file_path == 'index.html':
        # 1. index.html (Home)
        # Find: <a href="/products/index.html" data-i18n="nav_products">Products</a>
        # Replace with: <a href="#products" data-i18n="nav_products">Products</a>
        content = re.sub(
            r'href="/products/index\.html"([^>]*?data-i18n="nav_products")',
            r'href="#products"\1',
            content
        )
    else:
        # 2. Sub-pages (products/ folder)
        # Find Header and Mobile Panel "Products"/"设备中心" links
        # Patterns to catch:
        # href="/products/index.html" data-zh="设备中心"
        # href="https://www.fdlsorterai.com/" data-zh="设备中心"
        
        # We target specific data attributes to ensure we only hit the navigation links
        patterns = [
            (r'href="(?:/products/index\.html|https://www\.fdlsorterai\.com/)"([^>]*?data-(?:zh|en)="(?:设备中心|Products)")', r'href="/index.html#products"\1'),
        ]
        
        for old, new in patterns:
            content = re.sub(old, new, content)

    # Safety check: Remove any accidental double hrefs if they were introduced previously (just in case)
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_navigation(f)
