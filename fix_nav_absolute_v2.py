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

# Mapping patterns to absolute URLs
replacements = [
    # Home and Logo
    (r'href="(https://www\.fdlsorterai\.com/)?(index\.html|/|#top)"', 'href="https://www.fdlsorterai.com/"'),
    (r'href="(\.\./)+index\.html"', 'href="https://www.fdlsorterai.com/"'),
    
    # Anchors
    (r'href="([^"]*)#markets"', 'href="https://www.fdlsorterai.com/#markets"'),
    (r'href="([^"]*)#solutions"', 'href="https://www.fdlsorterai.com/#solutions"'),
    (r'href="([^"]*)#products"', 'href="https://www.fdlsorterai.com/#products"'),
    (r'href="([^"]*)#technology"', 'href="https://www.fdlsorterai.com/#technology"'),
    (r'href="([^"]*)#services?"', 'href="https://www.fdlsorterai.com/#services"'),
    (r'href="([^"]*)#contact"', 'href="https://www.fdlsorterai.com/#contact"'),
    (r'href="([^"]*)#inquiry"', 'href="https://www.fdlsorterai.com/#contact"'),
    
    # Special: Back to equipment center button in detail pages
    (r'href="(\.\./)?(products/)?index\.html"', 'href="https://www.fdlsorterai.com/products/index.html"'),
]

# Special catch for specific links that might be tricky
final_cleanup = [
    ('href="/#markets"', 'href="https://www.fdlsorterai.com/#markets"'),
    ('href="/#solutions"', 'href="https://www.fdlsorterai.com/#solutions"'),
    ('href="/#products"', 'href="https://www.fdlsorterai.com/#products"'),
    ('href="/#technology"', 'href="https://www.fdlsorterai.com/#technology"'),
    ('href="/#services"', 'href="https://www.fdlsorterai.com/#services"'),
    ('href="/#contact"', 'href="https://www.fdlsorterai.com/#contact"'),
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pattern, sub in replacements:
        content = re.sub(pattern, sub, content)
    
    for old, new in final_cleanup:
        content = content.replace(old, new)
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed navigation in: {file_path}")
