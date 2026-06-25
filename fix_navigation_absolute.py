import os
import re

files = [
    'index.html',
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

# Patterns to match any existing variations of these links
replacements = [
    # 1. Logo and Home links
    (r'href="([^"]*/)?index\.html"', 'href="/"'),
    (r'href="https://www\.fdlsorterai\.com/"', 'href="/"'),
    
    # 2. Main Navigation Anchors (Targeting sub-pages)
    (r'href="[^"]*#markets"', 'href="/#markets"'),
    (r'href="[^"]*#solutions"', 'href="/#solutions"'),
    (r'href="[^"]*#products"', 'href="/#products"'),
    (r'href="[^"]*#technology"', 'href="/#technology"'),
    (r'href="[^"]*#services"', 'href="/#services"'),
    (r'href="[^"]*#contact"', 'href="/#contact"'),
    (r'href="[^"]*#inquiry"', 'href="/#contact"'),
    
    # 3. Special: "Back to Product Center" buttons in detail pages
    (r'href="(\.\./)?index\.html" (data-zh="返回设备中心"|data-en="Back to Product Center")', 'href="/products/index.html" \\2'),
]

# Final specific polish for index.html (ensure smooth scroll within page)
index_polish = [
    ('href="/#markets"', 'href="#markets"'),
    ('href="/#solutions"', 'href="#solutions"'),
    ('href="/#products"', 'href="#products"'),
    ('href="/#technology"', 'href="#technology"'),
    ('href="/#services"', 'href="#services"'),
    ('href="/#contact"', 'href="#contact"'),
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply global replacements
    for pattern, sub in replacements:
        content = re.sub(pattern, sub, content)
        
    # Apply smooth scroll polish for homepage only
    if file_path == 'index.html':
        for old, new in index_polish:
            content = content.replace(old, new)
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {file_path}")
