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

def fix_products_jump(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if file_path == 'index.html':
        # Homepage Nav link: Products -> #products
        # Target: <a href="/products/index.html" data-i18n="nav_products">Products</a>
        content = re.sub(
            r'href="/products/index\.html"([^>]*?data-i18n="nav_products")',
            r'href="#products"\1',
            content
        )
    else:
        # Sub-pages: Navigation "Equipment Center" -> /index.html#products
        # We target links with data-zh="设备中心" or data-en="Products" in the nav/mobile areas
        
        # PC Nav & Mobile Panel
        content = re.sub(
            r'href="(?:/products/index\.html|https://www\.fdlsorterai\.com/|/index\.html)"([^>]*?data-(?:zh|en)="(?:设备中心|Products)")',
            r'href="/index.html#products"\1',
            content
        )

    # Final cleanup of any potential href="href=..." artifacts
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Jump fixed in: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_products_jump(f)
