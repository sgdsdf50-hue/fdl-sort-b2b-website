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

PRODUCT_SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

def fix_related_products(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match product cards in the related products section
    # Usually: <a class="product-card" href="..."><img src="...slug.jpg" ...>
    for slug in PRODUCT_SLUGS:
        # Regex to find a link followed by an image that contains the slug
        # We look for the pattern where href is currently the domain or root
        pattern = r'href="(?:https?://www\.fdlsorterai\.com/?|/)"(?=[^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Related products fixed in: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_related_products(f)
