import os
import re

# Physical root-relative paths
ROOT_HOME = "/index.html"
ROOT_CATALOG = "/products/index.html"
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

PRODUCT_SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']

def final_precise_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Related Product Cards in detail pages (catch ones pointing to root domain)
    # Proximity fix: find link followed by image matching a slug
    for slug in PRODUCT_SLUGS:
        # Match href="/" or absolute URL followed by card contents and machine-specific image
        pattern = r'href="(?:/|' + re.escape(BASE_URL) + r'/?)"(?=[^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)
        
        # Also direct folder links should include index.html
        pattern2 = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern2, f'href="/products/{slug}/index.html"', content)

    # 2. Global Navigation Standardization (Header, Mobile, Footer)
    # Home & Logo -> /index.html
    content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|' + re.escape(BASE_URL) + r'/?)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{ROOT_HOME}"', content)
    
    # Anchors -> /index.html#anchor
    for anchor in ANCHORS:
        if anchor == 'products':
            # Equipment Center menu item -> /products/index.html
            content = re.sub(r'href="[^"]*?#products"', f'href="{ROOT_CATALOG}"', content)
        else:
            pattern = r'href="[^"]*?#' + anchor + r'"'
            content = re.sub(pattern, f'href="{ROOT_HOME}#{anchor}"', content)

    # 3. Product Center / Equipment Center buttons
    content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|' + re.escape(BASE_URL) + r'/products/index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', f'href="{ROOT_CATALOG}"', content)
    
    # 4. Homepage Smooth Scroll (Re-fix local anchors on index.html)
    if file_path == 'index.html':
        for anchor in ['markets', 'solutions', 'technology', 'services', 'contact']:
             content = content.replace(f'href="{ROOT_HOME}#{anchor}"', f'href="#{anchor}"')

    # Final Sanitization
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    content = content.replace('href="//', 'href="/')
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Final Fix Applied: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        final_precise_fix(f)
