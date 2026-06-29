import os

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

PIXEL_CODE = """
  <!-- Meta Pixel & CAPI Code -->
  <script>
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    
    const META_PIXEL_ID = '1032808262617579';
    fbq('init', META_PIXEL_ID);
    
    // 浏览器端和服务器端去重 EventID 生成器
    function generateMetaEventId() {
      return 'evt_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }
    
    // 1. 浏览器端 PageView 上报
    const pageViewId = generateMetaEventId();
    fbq('track', 'PageView', {}, { eventID: pageViewId });
    
    // 2. 服务端 CAPI PageView 上报代理
    fetch('/api/meta-capi', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        eventName: 'PageView',
        eventID: pageViewId
      })
    }).catch(err => console.error('Meta CAPI PageView Error:', err));
    
    // 浏览器端高安全 SHA-256 哈希辅助函数
    function hashMetaValue(value) {
      if (!value) return Promise.resolve(null);
      return crypto.subtle.digest('SHA-256', new TextEncoder().encode(value.trim().toLowerCase()))
        .then(hashBuffer => {
          const hashArray = Array.from(new Uint8Array(hashBuffer));
          return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        });
    }
  </script>
  <!-- End Meta Pixel Code -->
"""

for file_path in FILES:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if already injected to avoid duplicate injects
    if "Meta Pixel & CAPI Code" in content:
        print(f"Already injected in {file_path}")
        continue
        
    if "</head>" in content:
        new_content = content.replace("</head>", PIXEL_CODE + "</head>")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully injected tracking into {file_path}")
    else:
        print(f"ERROR: No </head> tag found in {file_path}")
