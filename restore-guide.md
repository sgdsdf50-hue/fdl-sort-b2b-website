# FDL SORT 独立站一键恢复指南 (Restore & Rollback Guide)

本指南说明如何在发生任何紧急故障、误修改、线上排版破坏或逻辑冲突时，100% 物理级恢复至当前无暇运行的稳定状态。

---

## 方案 A：从 Git Tag 物理还原（最高优先级，推荐）

此方案能利用本地 Git 元数据一键擦除所有不满意改动，重置代码到本完美时点。

### 1. 检出恢复分支
打开终端（Windows PowerShell 或 Git Bash），进入网站代码根目录，运行：
```bash
# 获取远程最新的标签数据
git fetch --all --tags

# 基于黄金恢复 Tag 建立并切换到一个新分支
git checkout tags/restore-point-current-site-20260626-0930 -b restore-action-branch
```

### 2. 强制覆盖主分支并上线
确认当前分支代码正常后，强制将 main 主分支覆盖并推送到 GitHub 远程仓库（触发 Vercel 自动重构上线）：
```bash
# 将 main 分支强制重置到该 Tag 的状态
git branch -f main restore-action-branch

# 切换回 main 分支
git checkout main

# 强制推送覆盖远程 GitHub（请先确认本地代理正常，10808）
$env:HTTP_PROXY="http://127.0.0.1:10808"
$env:HTTPS_PROXY="http://127.0.0.1:10808"
git push origin main --force
```

---

## 方案 B：使用 Vercel CLI 手动一键发布

如果您直接在 Vercel 进行了错误的设置，可以通过控制台或 CLI 进行还原。

### 1. Vercel 控制台 Promote
1. 登录您的 Vercel 控制台。
2. 找到与最新 Commit ID `5add23d7e19eaa55627cfb156cbda3ff76a284dc` 绑定的 Deployment（部署）。
3. 点击右侧的三个小点，选择 **"Promote to Production"**。
4. 线上环境将在 10 秒内瞬间回滚至该正确时点。

### 2. Vercel CLI 一键发布
如果本地拥有 Vercel CLI 权限，直接在根目录运行以下命令重新生成线上 Production：
```bash
# 全量打包并强制覆盖到线上正式域名
vercel --prod
```

---

## 方案 C：从 ZIP 备份包纯物理覆盖恢复

如果由于 Git 元数据冲突或仓库被意外删除导致无法回退：
1. 彻底清空当前工作区下的除 `.git` 外的所有文件。
2. 解压备份包 `fdlsorterai-current-site-backup-20260626-0930.zip`，将解压后的所有物理文件（`index.html`，`products/`，`about/`等）拷贝粘贴进工作区中。
3. 执行提交并推送：
   ```bash
   git add .
   git commit -m "Emergency Rollback: Manual file overwrite restore from ZIP"
   git push origin main --force
   ```

---

## 方案 D：恢复后的核心功能核对项 (Checklist)

恢复成功后，请对照此清单逐页核对以下功能：
1. **首页 (`index.html`)**：
   - 检查电脑端顶栏导航（Markets, Solutions, etc.）是否平滑滚动，无遮挡。
   - 检查手机端顶栏，右侧 ☰（三横线）按钮是否能够点击弹出，且在点击锚点后能**自动收起面板并平滑定位**。
   - 检查第 6 个产品卡片（Complete Sorting Line）点击后能顺利加载二级页。
2. **产品中心 (`products/index.html`)**：
   - 确认 6 个产品详情卡片均能正常点击进入物理文件页面。
3. **二级详情页 (`products/*/index.html`)**：
   - 页面顶部的大标题显示为 **“核心优势 / Core Advantages”**，且无任何“手册内容整理”等残留小字。
   - 顶部导航支持多端点击（Home, Markets）并顺滑跳回首页各板块。
   - 底部 **“相关设备 (Related Products)”** 推荐大卡片点击后，能正常互相跳转到对应的详情页，不再跳回首页 root。
    4. **关于我们 (`about/index.html`)**：
       - 确认大标题正常。
       - 检查视频播放器是否能正常、零卡顿播放 Cloudflare R2 宣传片。
       - 检查证书画廊是否显示 19 张精美的白底悬停放大 PNG 证书，底部官方名称展示正常。
       - **检查 Meta Pixel & CAPI 联调状态**：打开浏览器开发者工具 (F12) 控制台或 Meta Pixel Helper，确认无 JS 报错且 PageView/Lead 事件已顺利发送。

---

## 方案 E：Meta 营销追踪联合环境变量配置指南

Conversions API (CAPI) 的密钥安全级别极高，决不能暴露在客户端代码中。请确保在对应的托管或独立服务器控制台中，配置了以下三个环境变量。

### 1. Vercel 生产部署环境变量配置（当前正式站使用）
1. 登录 [Vercel 仪表盘](https://vercel.com/) 并进入您的项目 `fdl-sort-b2b-website`。
2. 依次点击顶部的 **"Settings"** -> 左侧导航栏 **"Environment Variables"**。
3. 依次添加以下三个变量（设置为 **Production**、**Preview** 两个环境生效）：
   - 键名：`META_PIXEL_ID`
     值：`1032808262617579`
   - 键名：`META_CAPI_TOKEN`
     值：`EAASZBCEBPClUBR05bUc7cwUYjnqgBwtLwo9p3R5ppU8dYvvZAuJptdxY2RxmdsZBNvp6w8RM5s5MPxqTTCCzv8lXlKrUCZCZAZCSYE4mqwl95aD9nTwtx2mBYYR9eeonZBjGiRdwGPkjZBZCGn0SZBE5V59jHxMJz3ZB8hdtQlz8nEtvNXPBqaSTL3ZAXygWdYcS6HAYBAZDZD`
   - 键名：`META_TEST_EVENT_CODE`（可选，测试完毕后请从后台将其删除，以使生产上报完美对齐）
     值：`TTEST89156`
4. 点击 **"Save"**。
5. **重要**：添加环境变量后，必须触发一次新的 Deployment 构建部署，新配置才会正式生效上屏。

### 2. Cloudflare Worker 密钥配置
如果未来您选择将中转代理 API 迁移部署至 Cloudflare Workers 中，请通过以下方式将 Token 存入 CF 的加密安全存储（Secrets）中：
1. 本地打开终端，运行：
   ```bash
   # 为 Worker 注入加密 CAPI 令牌 (不公开可见)
   wrangler secret put META_CAPI_TOKEN
   # 终端将提示您输入密码，直接粘入您的 EAASZBCE... 令牌后回车
   
   # 注入 Pixel ID
   wrangler secret put META_PIXEL_ID
   # 输入 1032808262617579 后回车
   ```
2. 您也可以登录 [Cloudflare 控制台](https://dash.cloudflare.com/)，在 Workers & Pages 中选择您的服务，进入 **"Settings"** -> **"Variables"**，并在 **"Environment Variables"** 处以加密加密的形式添加对应的键值对。

### 3. 独立 Node.js / Linux 物理服务器配置
如果将站点与 Node.js 代理接口部署于独立的私有云服务器中：
- **Linux/Ubuntu/Docker 启动时导出**：
  在启动或守护进程脚本中进行导出注入：
  ```bash
  export META_PIXEL_ID="1032808262617579"
  export META_CAPI_TOKEN="EAASZBCEBPClUBR05bUc..."
  export META_TEST_EVENT_CODE="TTEST89156"
  
  # 启动您的 Node.js 主服务
  node server.js
  ```
- **PM2 进程管理工具配置 (Ecosystem.config.js)**：
  如果您使用 PM2，可将环境变量配置在 `env` 标签下：
  ```json
  {
    "apps" : [{
      "name"   : "fdl-sort-capi-proxy",
      "script" : "./server.js",
      "env": {
        "META_PIXEL_ID": "1032808262617579",
        "META_CAPI_TOKEN": "EAASZBCEBPClUBR05bUc...",
        "META_TEST_EVENT_CODE": "TTEST89156"
      }
    }]
  }
  ```

