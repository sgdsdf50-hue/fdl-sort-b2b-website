import os
import re

# Goal: Standardized root-relative physical links
# Home: /index.html
# Home Anchors: /index.html#anchor
# Sub-pages: /products/slug/index.html
# Product Center: /products/index.html

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

def fix_all_links(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Fix Product Details (index.html, sub-pages, everything)
    for slug in SLUGS:
        # Match href="/products/slug/", href="products/slug/", or absolute versions
        # Ensuring we don't fix it if it's already /products/slug/index.html
        pattern = r'href="(?:https?://www\.fdlsorterai\.com)?(?:/|\.\./)*products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # Step 2: Global Navigation Standardization (Header, Footer, Mobile)
    
    # 2a. Home & Logo
    # Target Home/Logo links and ensure they point to /index.html
    # We match the domain, root, or relative indices
    home_pattern = r'href="(?:https?://www\.fdlsorterai\.com/?|/|(?:\.\./)+index\.html|index\.html|#top)"(?=[^>]*?(?:logo|brand|Home|首页))'
    content = re.sub(home_pattern, 'href="/index.html"', content)
    
    # 2b. Section Anchors
    for anchor in ANCHORS:
        # Special case for "Products" menu item in sub-pages -> Catalog Index
        if anchor == 'products':
             content = re.sub(r'href="[^"]*?#products"', 'href="/products/index.html"', content)
        else:
             # Standard anchors for sections on the homepage
             pattern = r'href="[^"]*?#' + anchor + r'"'
             content = re.sub(pattern, f'href="/index.html#{anchor}"', content)

    # Step 3: Specific Navigation and Breadcrumb Fixes
    
    # 3a. Breadcrumbs or direct links to /products/ catalog
    # Target: Equipment Center, Product Center, etc.
    content = re.sub(r'href="(?:https?://www\.fdlsorterai\.com)?(?:/products/|(?:\.\./)*index\.html|index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', 'href="/products/index.html"', content)
    
    # 3b. Related Product Cards that point to root domain (from turn 58 observation)
    for slug in SLUGS:
        # Find link followed by image matching a slug
        pattern = r'href="(?:https?://www\.fdlsorterai\.com/?|/)"(?=[^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # Step 4: Homepage Local Anchors (Ensure Smooth Scroll on index.html)
    if file_path == 'index.html':
        for anchor in ['markets', 'solutions', 'technology', 'services', 'contact']:
             content = content.replace(f'href="/index.html#{anchor}"', f'href="#{anchor}"')
        # Restore home links to simple anchors/root on homepage if preferred for smooth scroll
        content = content.replace('href="/index.html"', 'href="#top"')

    # Final Polish
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    # Correct double slashes
    content = content.replace('href="//', 'href="/')
    # Ensure no nested hrefs
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Standardized: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_all_links(f)
