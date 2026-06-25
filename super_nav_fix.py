import os
import re

BASE_URL = "https://www.fdlsorterai.com"
ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']

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

# Mapping of machine slugs to names for precision if needed, 
# but regex on the path is safer.
PRODUCT_SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

def fix_content(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. Fix Product Card Entrance (index.html and products/index.html) ---
    # Convert any /products/xxx/ to /products/xxx/index.html
    # We use a non-capturing group to catch variations like href="products/xxx/"
    content = re.sub(r'href="(?:\.\./|/)?products/([^"/]+)/"', r'href="/products/\1/index.html"', content)
    
    # In products/index.html, some cards point to "/" incorrectly. Fix them.
    if file_path == 'products/index.html':
        # This is a bit manual but necessary for precision
        content = content.replace('alt="AI Optical Sorter"><h3 class="i18n" data-zh="AI 智能视觉光选色选机"', 'alt="AI Optical Sorter"><h3 class="i18n" data-zh="AI 智能视觉光选色选机"')
        # We'll use a more generic approach: if a product-card href is just BASE_URL or "/", fix it based on the image name.
        for slug in PRODUCT_SLUGS:
            content = re.sub(
                r'href="(?:https://www\.fdlsorterai\.com/|/)"([^>]*><img src="[^"]*'+slug+r'\.jpg")', 
                r'href="/products/'+slug+'/index.html"\1', 
                content
            )

    # --- 2. Fix Global Navigation (Header, Footer, Mobile) ---
    # Apply to all files in products/
    if file_path.startswith('products/'):
        # Fix Logo and Home links to absolute main domain
        content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top)"', f'href="{BASE_URL}/"', content)
        
        # Fix Anchors to absolute main domain
        for anchor in ANCHORS:
            # Match href="#anchor", href="/#anchor", href="../../index.html#anchor"
            # Use negative lookbehind to avoid fixing things that are already correct absolute URLs
            pattern = r'href="(?!http)[^"]*#' + anchor + r'"'
            content = re.sub(pattern, f'href="{BASE_URL}/#{anchor}"', content)
            
            # Match path-style links /anchor
            path_pattern = r'href="/' + anchor + r'"'
            content = re.sub(path_pattern, f'href="{BASE_URL}/#{anchor}"', content)

        # Fix "Back to Product Center" buttons
        # These usually have the text "返回设备中心" or "Back to Product Center"
        content = re.sub(r'href="(?:(?:\.\./)*index\.html|/products/)"([^>]*?(?:返回设备中心|Product Center))', f'href="{BASE_URL}/products/index.html"\1', content)

    # --- 3. Related Products in Detail Pages ---
    # Ensure they point to absolute index.html files
    for slug in PRODUCT_SLUGS:
        content = re.sub(r'href="(?:/products/|(?:\.\./)+products/|https://www\.fdlsorterai\.com/products/)'+slug+r'/(?:index\.html)?"', f'href="{BASE_URL}/products/{slug}/index.html"', content)

    # --- 4. Final Cleanup ---
    # Ensure no nested hrefs
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Ensure no double slashes in BASE_URL transitions
    content = content.replace(f'{BASE_URL}//', f'{BASE_URL}/')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Final Fix Applied: {file_path}")

for f in FILES:
    fix_content(f)
