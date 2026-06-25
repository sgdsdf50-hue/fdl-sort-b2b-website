import os
import re

BASE_URL = "https://www.fdlsorterai.com"
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

PRODUCT_DATA = {
    'ai-optical-sorter': 'AI Optical Sorter',
    'film-flexible-sorter': 'AI Flexible Film Sorter',
    'hyperspectral-material-sorter': 'AI Hyperspectral Material Sorter',
    'parallel-robot-sorter': 'AI Parallel Robot Sorter',
    'solid-waste-line': 'Solid Waste Sorting Line',
    'textile-sorter': 'AI Textile Sorter'
}

def repair_navigation(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. Homepage Specific Fixes ---
    if file_path == 'index.html':
        # Header Nav: Products -> #products
        content = re.sub(
            r'href="/products/index\.html"([^>]*?data-i18n="nav_products")',
            r'href="#products"\1',
            content
        )
        # Product Cards: /products/xxx/ -> /products/xxx/index.html
        for slug in PRODUCT_DATA:
            content = re.sub(
                r'href="/products/' + slug + r'/"',
                f'href="/products/{slug}/index.html"',
                content
            )

    # --- 2. Sub-page Specific Fixes (products/ directory) ---
    else:
        # Logo & Home -> /index.html
        content = re.sub(
            r'href="(?:https?://www\.fdlsorterai\.com/?|/|(?:\.\./)+index\.html|index\.html|#top)"(?=[^>]*?(?:logo|brand|Home|首页))',
            'href="/index.html"',
            content
        )

        # Main Nav & Mobile Panel: 
        # Markets -> /index.html#markets, etc.
        anchors = ['markets', 'solutions', 'technology', 'services', 'contact']
        for anchor in anchors:
            pattern = r'href="(?!http)[^"]*#' + anchor + r'"'
            content = re.sub(pattern, f'/index.html#{anchor}', content)
        
        # Equipment Center / Products -> /index.html#products
        content = re.sub(
            r'href="(?:/products/index\.html|https?://www\.fdlsorterai\.com/?|#products|/products/)"(?=[^>]*?(?:Equipment Center|设备中心|Products))',
            'href="/index.html#products"',
            content
        )

        # "Back to Product Center" button -> /products/index.html
        content = re.sub(
            r'href="(?:https?://www\.fdlsorterai\.com/?|/|\.\./index\.html)"(?=[^>]*?(?:返回设备中心|Back to Product Center))',
            'href="/products/index.html"',
            content
        )

        # Related Product Cards: Fix links pointing to root to point to correct sub-page
        for slug in PRODUCT_DATA:
            # Match card link followed by machine-specific image
            pattern = r'href="(?:https?://www\.fdlsorterai\.com/?|/)"(?=[^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
            content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)
            
            # Match simple folder links in related products
            pattern2 = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
            content = re.sub(pattern2, f'href="/products/{slug}/index.html"', content)

    # --- 3. Global Sanitization ---
    # Fix double slashes
    content = content.replace('href="//', 'href="/')
    # Prevent nested hrefs (href="href=...")
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Repaired: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        repair_navigation(f)
