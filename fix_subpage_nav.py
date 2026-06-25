import os
import re

files = [
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

# Redirect script to inject
redirect_script = """
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      document.querySelectorAll('.nav-links a, .mobile-panel a, .logo, .btn').forEach(function(link) {
        link.addEventListener('click', function(e) {
          const href = this.getAttribute('href');
          if (href && href.startsWith('/index.html#')) {
            e.preventDefault();
            window.location.href = href;
          }
        });
      });
    });
  </script>
"""

# Link mapping
replacements = [
    (r'href="(?:/|index\.html|(?:\.\./)+index\.html)"', 'href="/index.html"'),
    (r'href="(?:/#markets|#markets|(?:\.\./)+index\.html#markets)"', 'href="/index.html#markets"'),
    (r'href="(?:/#solutions|#solutions|(?:\.\./)+index\.html#solutions)"', 'href="/index.html#solutions"'),
    (r'href="(?:/products/|#products|(?:\.\./)+index\.html#products)"', 'href="/index.html#products"'),
    (r'href="(?:/#technology|#technology|(?:\.\./)+index\.html#technology)"', 'href="/index.html#technology"'),
    (r'href="(?:/#services|#services|(?:\.\./)+index\.html#services)"', 'href="/index.html#services"'),
    (r'href="(?:/#contact|#contact|#inquiry|(?:\.\./)+index\.html#contact)"', 'href="/index.html#contact"'),
]

for file_path in files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Inject script into <head>
    if '</head>' in content and '<script>' not in content[:content.find('</head>')]:
        content = content.replace('</head>', redirect_script + '</head>')
    
    # 2. Update href attributes
    for pattern, new_href in replacements:
        # Use regex to find href in tags, avoid double matching
        # Specifically targeting navigation related sections
        content = re.sub(pattern, f'href="{new_href}"', content)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed navigation and injected script in: {file_path}")
