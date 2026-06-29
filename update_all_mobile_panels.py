import os
import re

FILES = [
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html',
    'about/index.html'
]

NEW_MOBILE_PANEL = """<div id="mobilePanel" class="mobile-panel">
      <a class="i18n" href="/index.html" data-zh="首页" data-en="Home">首页</a>
      <a class="i18n" href="/index.html#markets" data-zh="服务市场" data-en="Markets">服务市场</a>
      <a class="i18n" href="/index.html#solutions" data-zh="分选方案" data-en="Solutions">分选方案</a>
      <a class="i18n" href="/index.html#products" data-zh="设备中心" data-en="Products">设备中心</a>
      <a class="i18n" href="/index.html#technology" data-zh="核心技术" data-en="Technology">核心技术</a>
      <a class="i18n" href="/index.html#services" data-zh="售后服务" data-en="Service">售后服务</a>
      <a class="i18n" href="/about/index.html" data-zh="关于我们" data-en="About Us">关于我们</a>
      <a class="i18n" href="/index.html#contact" data-zh="联系我们" data-en="Contact">联系我们</a>
    </div>"""

def update_mobile_panel(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the <div id="mobilePanel" class="mobile-panel">...</div> block
    # Matches <div id="mobilePanel" class="mobile-panel"> up to the next </div>
    # Using non-greedy match to find the closing div of mobilePanel
    pattern = r'<div id="mobilePanel" class="mobile-panel">.*?</div>'
    
    # Check if we can find it
    matches = re.findall(pattern, content, flags=re.DOTALL)
    if not matches:
        print(f"Could not find mobilePanel block in {file_path}")
        return
        
    # Replace the block with the new one
    new_content = re.sub(pattern, NEW_MOBILE_PANEL, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated mobile panel in {file_path}")

if __name__ == "__main__":
    for f in FILES:
        update_mobile_panel(f)
