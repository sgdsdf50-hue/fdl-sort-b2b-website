import os
import re

FILES = [
    'index.html',
    'about/index.html',
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

def update_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update i18n dictionary
    content = content.replace('nav_contact: "Contact"', 'nav_contact: "Contact",\n        nav_about: "About Us"')
    content = content.replace('nav_contact: "联系我们"', 'nav_contact: "联系我们",\n        nav_about: "关于我们"')

    # 2. Update Header Navigation
    nav_pattern = r'(<a href="#services" data-i18n="nav_services">Services</a>)'
    content = re.sub(nav_pattern, r'\1\n          <a href="/about/index.html" data-i18n="nav_about">About Us</a>', content)

    # 3. Update Footer
    footer_pattern = r'(<h4 data-i18n="footer_col2_title">Product series</h4>)'
    content = re.sub(footer_pattern, r'<h4 data-i18n="nav_about">About Us</h4>\n          <a href="/about/index.html" data-i18n="nav_about">About Us</a>\n          \1', content)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated index.html")

def update_subpages():
    subpages = [f for f in FILES if f != 'index.html']
    
    for file_path in subpages:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Update Header Navigation (PC)
        # Services link usually: <a class="i18n" href="/index.html#services" data-zh="售后服务" data-en="Service">售后服务</a>
        header_nav_pattern = r'(<a class="i18n" href="/index\.html#services" data-zh="售后服务" data-en="Service">售后服务</a>)'
        new_header_link = '<a class="i18n" href="/about/index.html" data-zh="关于我们" data-en="About Us">关于我们</a>'
        if new_header_link not in content:
            content = re.sub(header_nav_pattern, r'\1' + new_header_link, content)

        # 2. Update Mobile Panel
        # Equipment center: <a class="i18n" href="/products/index.html" data-zh="设备中心" data-en="Products">设备中心</a>
        mobile_nav_pattern = r'(<a class="i18n" href="/products/index\.html" data-zh="设备中心" data-en="Products">设备中心</a>)'
        new_mobile_link = '<a class="i18n" href="/about/index.html" data-zh="关于我们" data-en="About Us">关于我们</a>'
        if new_mobile_link not in content:
            content = re.sub(mobile_nav_pattern, r'\1' + new_mobile_link, content)

        # 3. Update Footer
        # Column 1 header usually: <h4 class="i18n" data-zh="产品系列" data-en="Products">产品系列</h4>
        footer_nav_pattern = r'(<h4 class="i18n" data-zh="产品系列" data-en="Products">产品系列</h4>)'
        new_footer_link = '<h4 class="i18n" data-zh="关于我们" data-en="About Us">关于我们</h4><a class="i18n" href="/about/index.html" data-zh="关于我们" data-en="About Us">关于我们</a>'
        if new_footer_link not in content:
            content = re.sub(footer_nav_pattern, r'\1' + new_footer_link, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path}")

if __name__ == "__main__":
    update_index_html()
    update_subpages()
