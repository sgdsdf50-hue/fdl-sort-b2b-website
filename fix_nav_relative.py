import os

detail_pages = [
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

center_page = 'products/index.html'

# Rules for 2-level deep pages
detail_replacements = [
    ('href="/"', 'href="../../index.html"'),
    ('href="/#markets"', 'href="../../index.html#markets"'),
    ('href="/#solutions"', 'href="../../index.html#solutions"'),
    ('href="/#products"', 'href="../../index.html#products"'),
    ('href="/#technology"', 'href="../../index.html#technology"'),
    ('href="/#services"', 'href="../../index.html#services"'),
    ('href="/#contact"', 'href="../../index.html#contact"'),
    ('href="../../index.html"', 'href="../../index.html"'), # Ensure logo is correct
]

# Rules for 1-level deep page
center_replacements = [
    ('href="/"', 'href="../index.html"'),
    ('href="/#markets"', 'href="../index.html#markets"'),
    ('href="/#solutions"', 'href="../index.html#solutions"'),
    ('href="/#products"', 'href="../index.html#products"'),
    ('href="/#technology"', 'href="../index.html#technology"'),
    ('href="/#services"', 'href="../index.html#services"'),
    ('href="/#contact"', 'href="../index.html#contact"'),
    ('href="../index.html"', 'href="../index.html"'), # Ensure logo is correct
]

def apply_fixes(file_path, replacements):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Specific fix for logo tag to avoid double relative path if already correct
    # But since we are targeting href="/", it's safer
    for old, new in replacements:
        content = content.replace(old, new)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed navigation in: {file_path}")

for p in detail_pages:
    apply_fixes(p, detail_replacements)

apply_fixes(center_page, center_replacements)
