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

# Patterns for precise removal of the description <p> tags
PATTERNS = [
    r'<p class="i18n" data-zh="将手册中的.*?(?:提炼|转化)为采购方可理解的(?:网站内容|技术卖点).*?".*?<\/p>',
    r'<p class="i18n" data-zh="这里不再放整张手册截图，而是把手册中的产品定位、核心亮点、技术参数、应用场景和服务承诺拆成网页原生文字、表格和卡片，支持中英双语切换。".*?<\/p>',
    r'<p class="i18n" data-zh="参数由手册表格整理为网页原生表格，便于搜索引擎抓取和客户阅读。".*?<\/p>',
    r'<p class="i18n" data-zh="将手册中的售前、售中、售后服务内容整理为网页模块。".*?<\/p>'
]

def physical_delete(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    initial_content = content
    for pattern in PATTERNS:
        # Using DOTALL to ensure the entire tag including multiline content is removed
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    if content != initial_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Physically purified: {file_path}")
    else:
        print(f"Checked, no target tags found in: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        physical_delete(f)
