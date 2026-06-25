import os
import re

# Standard physical root-relative paths
ROOT_INDEX = "/index.html"
PROD_CATALOG = "/products/index.html"

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

SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']

def fix_file(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Clean control characters if any (prevent decoding issues)
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')

    # Step 2: Global Navigation Fix (Header, Footer, Mobile Panel)
    
    # 2a. Standardize Home/Logo (must point to /index.html)
    # Target elements that serve as home links
    content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|https://www\.fdlsorterai\.com/)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{ROOT_INDEX}"', content)
    
    # 2b. Standardize Anchors to point to /index.html#anchor
    for anchor in ANCHORS:
        if anchor == 'products':
            # "Products" or "Equipment Center" menu item should go to the catalog
            content = re.sub(r'href="[^"]*?#products"', f'href="{PROD_CATALOG}"', content)
        else:
            # Standard sections on the homepage
            pattern = r'href="[^"]*?#' + anchor + r'"'
            content = re.sub(pattern, f'href="{ROOT_INDEX}#{anchor}"', content)

    # Step 3: Product Detail Entrances (Cards and Related items)
    for slug in SLUGS:
        # Standardize any link containing the slug to point to the physical index.html
        pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # Step 4: Page Specific Fixes
    
    # 4a. Back to Product Center button
    content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|https://www\.fdlsorterai\.com/products/index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', f'href="{PROD_CATALOG}"', content)
    
    # 4b. Sub-page links to "/" should point to /index.html
    if file_path != 'index.html':
        content = re.sub(r'href="/"', f'href="{ROOT_INDEX}"', content)

    # Step 5: Final Integrity Cleanup
    
    # Remove nested hrefs (href="href=...")
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Correct double slashes
    content = content.replace('href="//', 'href="/')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Repaired: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_file(f)
