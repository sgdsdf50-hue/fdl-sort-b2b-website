import os
import re

FILES = [
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

PRODUCT_MAP = {
    'ai-optical-sorter': '/products/ai-optical-sorter/index.html',
    'film-flexible-sorter': '/products/film-flexible-sorter/index.html',
    'hyperspectral-material-sorter': '/products/hyperspectral-material-sorter/index.html',
    'parallel-robot-sorter': '/products/parallel-robot-sorter/index.html',
    'solid-waste-line': '/products/solid-waste-line/index.html',
    'textile-sorter': '/products/textile-sorter/index.html'
}

def final_precision_repair(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First, fix specific product cards based on proximity to unique images
    for slug, target in PRODUCT_MAP.items():
        # Match href="..." followed by machine-specific img src
        # This regex is more robust as it looks for the unique image filename
        content = re.sub(
            r'href="[^"]*?"(?=[^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")',
            f'href="{target}"',
            content
        )

    # 2. Fix the "Equipment Center" / "Back to Product Center" button
    # Target: <a ... href="..." data-zh="返回设备中心" ...>
    content = re.sub(
        r'href="[^"]*?"(?=[^>]*?data-zh="返回设备中心")',
        'href="/index.html#products"',
        content
    )
    
    # 3. Standardize Navigation Equipment Center link
    # Target: <a ... href="..." data-zh="设备中心" ...>
    content = re.sub(
        r'href="[^"]*?"(?=[^>]*?data-zh="设备中心")',
        'href="/index.html#products"',
        content
    )

    # 4. Standardize Home/Logo links (ONLY if they are still pointing to the old root)
    # Using negative lookahead to avoid breaking the product links we just fixed
    content = re.sub(
        r'href="https://www\.fdlsorterai\.com/?"(?![^>]*?src="[^"]*?(?:ai-optical|film|hyperspectral|parallel|solid|textile))',
        'href="/index.html"',
        content
    )

    # 5. Fix Homepage Nav Specific (Confirming index.html line 244)
    if file_path == 'index.html':
        content = re.sub(r'href="/products/index\.html"([^>]*?data-i18n="nav_products")', r'href="#products"\1', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    for f in FILES + ['index.html', 'products/index.html']:
        final_precision_repair(f)
