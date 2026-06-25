import os
import re

BASE_URL = "https://www.fdlsorterai.com"
ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']
PRODUCT_SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

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

def apply_standardized_links(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Step 1: Fix Product Card Links in index.html and products/index.html ---
    # They should point to /products/xxx/index.html
    for slug in PRODUCT_SLUGS:
        # Match href="/products/xxx/" or "products/xxx/" or "../../products/xxx/"
        # Ensuring we don't accidentally match something that is already correct or an anchor
        pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # --- Step 2: Fix Global Navigation (Header, Footer, Mobile) ---
    # Mapping for sub-pages to go back to homepage anchors
    if file_path != 'index.html':
        # 1. Logo & Home
        content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{BASE_URL}/index.html"', content)
        
        # 2. Main Nav Anchors
        for anchor in ANCHORS:
            # Pattern matches any href that ends with #anchor but isn't already the correct absolute path
            # This covers href="#markets", href="/#markets", href="../../index.html#markets"
            pattern = r'href="[^"]*?#' + anchor + r'"'
            content = re.sub(pattern, f'href="{BASE_URL}/index.html#{anchor}"', content)

    # --- Step 3: Specific Page Link Fixes ---
    # "Back to Product Center" buttons
    content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html)"(?=[^>]*?(?:Equipment Center|设备中心|返回设备中心|Product Center))', f'href="{BASE_URL}/products/index.html"', content)

    # --- Step 4: Homepage Local Anchors (Ensure Smooth Scroll) ---
    if file_path == 'index.html':
        # On homepage, we prefer #anchor for smooth scrolling, but product cards need filenames
        # (Step 1 already handled product cards)
        pass

    # --- Final Polish & Safety ---
    # Ensure no nested hrefs
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    # Fix double slashes in URLs
    content = content.replace(f'{BASE_URL}//', f'{BASE_URL}/')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Final Fix Applied: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        apply_standardized_links(f)
