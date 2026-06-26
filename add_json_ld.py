import os
import re

BASE_DIR = 'products'
PRODUCTS = [
    {
        'dir': 'ai-optical-sorter',
        'name': 'AI Optical Sorter',
        'description': 'Industrial RGB vision AI optical sorter for plastic bottle recycling.'
    },
    {
        'dir': 'hyperspectral-material-sorter',
        'name': 'AI Hyperspectral Material Sorter',
        'description': 'NIR hyperspectral sensing for same-color different-material plastic separation.'
    },
    {
        'dir': 'film-flexible-sorter',
        'name': 'AI Flexible Film Sorter',
        'description': 'Specialized AI optical sorting for flexible plastic films and packaging.'
    },
    {
        'dir': 'parallel-robot-sorter',
        'name': 'AI Parallel Robot Sorter',
        'description': 'High-speed robotic picking and sorting system driven by AI vision.'
    },
    {
        'dir': 'textile-sorter',
        'name': 'AI Textile Sorter',
        'description': 'Automated garment and textile classification by fiber type and color using AI.'
    },
    {
        'dir': 'solid-waste-line',
        'name': 'Solid Waste Sorting Line',
        'description': 'Complete turnkey AI-powered sorting solutions for municipal and industrial solid waste.'
    }
]

for p in PRODUCTS:
    file_path = os.path.join(BASE_DIR, p['dir'], 'index.html')
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    schema = f'''  <!-- JSON-LD Product Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "{p['name']}",
    "brand": {{ "@type": "Brand", "name": "FDL SORT" }},
    "description": "{p['description']}",
    "category": "Industrial Sorting Equipment"
  }}
  </script>'''
    
    # Insert before </head>
    if '</head>' in content:
        new_content = content.replace('</head>', f'{schema}\n</head>')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated JSON-LD in {file_path}")
    else:
        print(f"Could not find </head> in {file_path}")
