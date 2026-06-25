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

    # --- Step 1: Standardize Related Product Cards in Detail Pages ---
    # Find links pointing to root domain that are immediately followed by a machine-specific image
    for slug in PRODUCT_SLUGS:
        # Regex explanation: Match href pointing to domain or root followed by card contents and machine-specific image
        pattern = r'href="(?:/|' + re.escape(BASE_URL) + r'/?)"(?=[^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)
        
        # Also fix direct folder links to include index.html
        pattern2 = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern2, f'href="/products/{slug}/index.html"', content)

    # --- Step 2: Global Navigation Standardization (Header, Footer, Mobile) ---
    # Home & Logo text links -> physical /index.html
    # This regex targets Home, 首页 or brand/logo related tags
    home_pattern = r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|' + re.escape(BASE_URL) + r'/?)"(?=[^>]*?(?:logo|brand|Home|首页))'
    content = re.sub(home_pattern, f'href="{ROOT_HOME}"', content)
    
    # Standardize Navigation Anchors to /index.html#anchor
    for anchor in ANCHORS:
        if anchor == 'products':
            # Equipment Center menu item -> Catalog Index
            content = re.sub(r'href="[^"]*?#products"', f'href="{ROOT_CATALOG}"', content)
        else:
            pattern = r'href="[^"]*?#' + anchor + r'"'
            content = re.sub(pattern, f'href="{ROOT_HOME}#{anchor}"', content)

    # --- Step 3: Specific Buttons and Breadcrumbs ---
    # "Back to Product Center" or direct catalog links
    content = re.sub(r'href="(?:https?://www\.fdlsorterai\.com)?(?:/products/|(?:\.\./)*index\.html|index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', f'href="{ROOT_CATALOG}"', content)
    
    # Catch any remaining root-relative catalog links
    content = re.sub(r'href="/products/"', f'href="{ROOT_CATALOG}"', content)

    # --- Step 4: Homepage Local Anchor Fix ---
    # Links within index.html to its own sections should remain simple anchors for smooth scroll
    if file_path == 'index.html':
        for anchor in ['markets', 'solutions', 'technology', 'services', 'contact']:
             content = content.replace(f'href="{ROOT_HOME}#{anchor}"', f'href="#{anchor}"')
        # Home links on homepage should point to root or #top
        content = content.replace(f'href="{ROOT_HOME}"', 'href="/"')

    # --- Final Sanitization ---
    # Fix any double leading slashes
    content = content.replace('href="//', 'href="/')
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    # Ensure no nested hrefs
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Standardized: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        final_precise_fix(f)
