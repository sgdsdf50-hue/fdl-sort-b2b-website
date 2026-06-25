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

SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']

def standardized_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Physical Product Detail Entrances (Cards and Related items)
    for slug in SLUGS:
        # Matches /products/xxx/, products/xxx/, or absolute domain versions
        pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # Step 2: Global Navigation Standardization (Header, Footer, Mobile Panel)
    
    # 2a. Home & Logo
    # Target Home/Logo links and ensure they point to /index.html
    # We identify them by their typical names in data-zh/en or content
    content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|' + re.escape(BASE_URL) + r'/?)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{ROOT_HOME}"', content)
    
    # 2b. Section Anchors
    for anchor in ANCHORS:
        if anchor == 'products':
            # "Products" or "Equipment Center" menu item should go to the catalog index
            content = re.sub(r'href="[^"]*?#products"', f'href="{ROOT_CATALOG}"', content)
        else:
            # Anchor links for homepage sections
            pattern = r'href="[^"]*?#' + anchor + r'"'
            content = re.sub(pattern, f'href="{ROOT_HOME}#{anchor}"', content)

    # Step 3: Specific Navigation and Breadcrumb Fixes
    
    # 3a. Breadcrumbs or direct links to /products/ catalog
    content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|' + re.escape(BASE_URL) + r'/products/index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', f'href="{ROOT_CATALOG}"', content)
    
    # 3b. Catch-all for simple root-relative catalog links
    content = re.sub(r'href="/products/"', f'href="{ROOT_CATALOG}"', content)

    # Step 4: Sub-page Stability
    # Ensure all "/" links in sub-pages are physical
    if file_path != 'index.html':
        content = re.sub(r'href="/"', f'href="{ROOT_HOME}"', content)

    # Step 5: Homepage Smooth Scroll Preservation
    if file_path == 'index.html':
        for anchor in ['markets', 'solutions', 'technology', 'services', 'contact']:
             content = content.replace(f'href="{ROOT_HOME}#{anchor}"', f'href="#{anchor}"')

    # Step 6: Final Integrity Cleanup
    
    # Remove nested hrefs (href="href=...")
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Correct double slashes
    content = content.replace('href="//', 'href="/')
    # Remove any stray control chars
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Standardized: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        standardized_fix(f)
