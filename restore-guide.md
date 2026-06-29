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
