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

PRODUCT_SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

ANCHOR_MAP = {
    'markets': '/index.html#markets',
    'solutions': '/index.html#solutions',
    'technology': '/index.html#technology',
    'services': '/index.html#services',
    'service': '/index.html#services',
    'contact': '/index.html#contact',
    'inquiry': '/index.html#contact'
}

def surgical_repair(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. Homepage index.html Specifics ---
    if file_path == 'index.html':
        # Header Nav: Equipment Center -> #products
        content = re.sub(
            r'href="(?:/products/index\.html|/products/)"([^>]*?data-i18n="nav_products")',
            r'href="#products"\1',
            content
        )
        # Product Cards: /products/xxx/ -> /products/xxx/index.html
        for slug in PRODUCT_SLUGS:
            content = re.sub(
                r'href="/products/' + slug + r'/"',
                f'href="/products/{slug}/index.html"',
                content
            )

    # --- 2. Sub-page specifics (All files in products/ folder) ---
    else:
        # Home & Logo -> /index.html
        content = re.sub(
            r'href="(?:https?://www\.fdlsorterai\.com/?|/|(?:\.\./)+index\.html|index\.html|#top)"(?=[^>]*?(?:logo|brand|Home|首页))',
            'href="/index.html"',
            content
        )

        # Standard Navigation Anchors (Markets, Solutions, etc.) -> /index.html#anchor
        for anchor, target in ANCHOR_MAP.items():
            # If it's a link to an anchor on the homepage
            pattern = r'href="(?!http)[^"]*#' + anchor + r'"'
            content = re.sub(pattern, f'href="{target}"', content)
            
            # If it's a path-style link like /markets
            path_pattern = r'href="/' + anchor + r'"'
            content = re.sub(path_pattern, f'href="{target}"', content)

        # Equipment Center / Products link in nav -> /index.html#products
        # Target based on text/i18n attributes
        content = re.sub(
            r'href="(?:/products/index\.html|https?://www\.fdlsorterai\.com/|/index\.html|#products|/products/)"([^>]*?data-(?:zh|en)="(?:设备中心|Products)")',
            r'href="/index.html#products"\1',
            content
        )

        # Related Products / Product Cards in sub-pages
        for slug in PRODUCT_SLUGS:
            # Proximity fix: find link followed by machine-specific image
            pattern = r'href="(?:https?://www\.fdlsorterai\.com/?|/|/index\.html)"([^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
            content = re.sub(pattern, f'href="/products/{slug}/index.html"\\1', content)
            
            # Direct slug links
            pattern2 = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
            content = re.sub(pattern2, f'href="/products/{slug}/index.html"', content)

        # "Back to Product Center" button -> /products/index.html
        content = re.sub(
            r'href="(?:https?://www\.fdlsorterai\.com/?|/|(?:\.\./)*index\.html)"(?=[^>]*?(?:返回设备中心|Back to Product Center))',
            'href="/products/index.html"',
            content
        )

    # --- 3. Global Sanitization ---
    # Fix double slashes
    content = content.replace('href="//', 'href="/')
    # Prevent nested hrefs
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Repaired: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        surgical_repair(f)
