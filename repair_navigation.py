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

# New fail-safe script
fail_safe_script = """
  <script>
    document.addEventListener('click', function(e) {
      const link = e.target.closest('a');
      if (link) {
        const href = link.getAttribute('href');
        if (href && href.includes('index.html#')) {
          const anchor = href.split('#')[1];
          e.preventDefault();
          window.location.href = '/index.html#' + anchor;
        }
      }
    });
  </script>
"""

def fix_content(content):
    # 1. Remove existing broken scripts (any script containing DOMContentLoaded and nav-links)
    content = re.sub(r'\s*<script>.*?DOMContentLoaded.*?nav-links.*?</script>', '', content, flags=re.DOTALL)
    
    # 2. Inject new fail-safe script before </head>
    if '</head>' in content:
        content = content.replace('</head>', fail_safe_script + '</head>')
    
    # 3. Clean up the massive href="href=..." syntax errors
    # This pattern matches href="href="something"" and extracts something
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    
    # 4. Standardize all navigation related links to explicit /index.html#id
    # We do a direct replacement for known anchors to be safe
    nav_fixes = [
        ('href="/index.html#markets"', '/index.html#markets'),
        ('href="/index.html#solutions"', '/index.html#solutions'),
        ('href="/index.html#products"', '/index.html#products'),
        ('href="/index.html#technology"', '/index.html#technology'),
        ('href="/index.html#services"', '/index.html#services'),
        ('href="/index.html#contact"', '/index.html#contact'),
        ('href="/index.html"', '/index.html'),
        ('href="/"', '/index.html'),
    ]
    
    for old_target, new_target in nav_fixes:
        # Match both standard href="target" and potential remaining corrupted ones
        content = re.sub(r'href="[^"]*?' + re.escape(old_target.split('/')[-1]) + r'[^"]*?"', f'href="{new_target}"', content)

    # 5. Specific fix for "Back to Product Center" if it was corrupted
    content = re.sub(r'href="[^"]*?products/index\.html[^"]*?"', 'href="/products/index.html"', content)
    
    return content

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = fix_content(content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Repaired and injected script in: {file_path}")
