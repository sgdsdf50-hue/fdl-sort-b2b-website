import os
import re

# Goal: Precise physical links for stability across all environments
# All cross-directory jumps must point to physical /index.html + anchor
# 1. Homepage Entrance Fix
# 2. Sub-page Nav/Mobile/Footer Fix
# 3. Sub-page Related/Back Button Fix

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

# Physical base targets
MAIN_HOME = "/index.html"
MAIN_CATALOG = "/products/index.html"

def fix_all_links(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Step 1: Product Entrance Fix (index.html and any related cards) ---
    for slug in SLUGS:
        # Standardize products/slug/ to /products/slug/index.html
        # Catch absolute domain versions or relative ones
        pattern = r'href="(?:https?://www\.fdlsorterai\.com)?(?:/|\.\./)*products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # --- Step 2: Global Navigation Standardization (Header, Footer, Mobile) ---
    if file_path != 'index.html':
        # 2a. Standardize Home/Logo links to physical root
        # Identify by content/tags typically used for Home/Brand
        content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|https?://www\.fdlsorterai\.com/?)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{MAIN_HOME}"', content)
        
        # 2b. Standardize Anchor Navigation to jump back to homepage physical sections
        anchors = ['markets', 'solutions', 'technology', 'services', 'contact']
        for anchor in anchors:
            pattern = r'href="[^"]*?#' + anchor + r'"'
            content = re.sub(pattern, f'href="{MAIN_HOME}#{anchor}"', content)
            
        # 2c. Equipment Center menu item specifically
        content = re.sub(r'href="[^"]*?#products"', f'href="{MAIN_CATALOG}"', content)

    # --- Step 3: Product Center / Equipment Center buttons in sub-pages ---
    # Fix buttons like "Back to Product Center"
    content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|https?://www\.fdlsorterai\.com/products/index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', f'href="{MAIN_CATALOG}"', content)
    
    # Simple links to /products/
    content = re.sub(r'href="/products/"', f'href="{MAIN_CATALOG}"', content)

    # --- Step 4: Homepage Smooth Scroll Preservation ---
    if file_path == 'index.html':
        # On home, links within the page should stay simple anchors
        for anchor in ['markets', 'solutions', 'technology', 'services', 'contact']:
             content = content.replace(f'href="{MAIN_HOME}#{anchor}"', f'href="#{anchor}"')
        # Home links on home should point to top or root
        content = content.replace(f'href="{MAIN_HOME}"', 'href="/"')

    # --- Final Polish ---
    # Ensure no nested href artifacts
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Fix double slashes
    content = content.replace('href="//', 'href="/')
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_all_links(f)
