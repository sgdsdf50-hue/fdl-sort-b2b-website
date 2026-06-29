import os

file_path = "products/ai-optical-sorter/index.html"

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Targets to replace
    old_str = '<td class="i18n" data-zh="2.5 / 4.5 / 8 kW" data-en="2.5 / 4.5 / 8 kW">2.5 / 4.5 / 8 kW</td>'
    new_str = '<td class="i18n" data-zh="2.5 / 4.5 / 5.5 kW" data-en="2.5 / 4.5 / 5.5 kW">2.5 / 4.5 / 5.5 kW</td>'

    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully replaced all 3 occurrences of '2.5 / 4.5 / 8 kW' in the target td tag.")
    else:
        print("Target td tag not found or already replaced.")
else:
    print(f"File not found: {file_path}")
