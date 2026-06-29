FDL SORT 独立站移动端/电脑端多端截图核对指南

由于当前的沙盒编译环境缺少无头浏览器（Headless Browser，如 Chromium/Gecko）及底层的图形驱动支持，为了避免本地静默打包失败，我们已为您将全套“截图自动化核对脚本”编译完毕并保存在本目录中。

您只需要将备份 ZIP 压缩包下载到您的本地电脑，并执行以下 3 步，即可自动截取当前最完美的双端页面，存入本目录中进行物理校验：

---

### 1. 运行前准备 (环境支持)
确保您的电脑上已安装了 Node.js（推荐 18.x 以上版本）。

### 2. 安装截图引擎
在当前 `pc-mobile-screenshot-check` 目录下打开终端（PowerShell 或 CMD），运行以下命令安装轻量级 Puppeteer：
```bash
npm install puppeteer
```

### 3. 一键执行截图
安装完成后，直接运行我们的自动化脚本：
```bash
node capture_screenshots.js
```

### 4. 生成的图片清单
脚本执行完毕后，将在本目录下自动生成以下 6 张高保真 PNG 图片，供您对比核验：
- `1-homepage-pc.png` (首页 电脑端)
- `1-homepage-mobile.png` (首页 手机端)
- `2-ai-sorter-pc.png` (详情页 电脑端)
- `2-ai-sorter-mobile.png` (详情页 手机端)
- `3-about-pc.png` (关于我们页 电脑端)
- `3-about-mobile.png` (关于我们页 手机端)
