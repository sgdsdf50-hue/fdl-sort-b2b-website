import os

files = [
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

replacements = [
    ('href="../index.html"', 'href="/"'),
    ('href="../../index.html"', 'href="/"'),
    ('href="/markets"', 'href="/#markets"'),
    ('href="/solutions"', 'href="/#solutions"'),
    ('href="/products/"', 'href="/#products"'),
    ('href="../products/index.html"', 'href="/#products"'),
    ('href="/technology"', 'href="/#technology"'),
    ('href="/services"', 'href="/#services"'),
    ('href="/contact"', 'href="/#contact"'),
    ('href="#inquiry"', 'href="/#contact"'),
]

for file_path in files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")
