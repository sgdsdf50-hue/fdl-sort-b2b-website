# Vercel 网页端一键导入与部署指南

由于本地环境未配置 Vercel 命令行工具（CLI），我们已为您将部署所需的配置文件 `vercel.json` 推送至 GitHub 仓库。您可以通过 Vercel 网页端，以最简单、点击即用的方式完成网站的部署。

---

## 🚀 方式一：一键点击部署（最推荐）

我们已经为您生成了专属的 **Vercel 一键克隆与部署链接**。点击下方链接即可直接进入 Vercel 的导入与部署流程：

👉 [**点击一键部署到 Vercel**](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fsgdsdf50-hue%2Ffdl-sort-b2b-website)

### 一键部署步骤：
1. **点击链接**：点击上方的部署链接。
2. **选择 Git 账户**：在跳转的 Vercel 页面中，选择您的 GitHub 账号（若未登录，请先登录/注册 Vercel 账号）。
3. **创建新仓库**：Vercel 会要求您输入一个新的仓库名称（Vercel 会将该模板复制到您的 GitHub 下）。
4. **点击 Create**：点击 **Create** 按钮，Vercel 将自动完成代码拉取、构建和部署。
5. **获取链接**：部署完成后，Vercel 会提供一个 `*.vercel.app` 后缀的免费二级域名。

---

## 📦 方式二：手动导入已有 GitHub 仓库

如果您希望直接关联您已有的 GitHub 仓库 `sgdsdf50-hue/fdl-sort-b2b-website`，请按照以下步骤操作：

### 1. 登录 Vercel
访问 [Vercel 官网 (vercel.com)](https://vercel.com/) 并点击右上角的 **Log In**。推荐使用 **Continue with GitHub** 进行登录，这样可以直接读取您的代码库。

### 2. 新建项目
在 Vercel 控制台主页（Dashboard），点击右上角的 **Add New...** 按钮，并在下拉菜单中选择 **Project**。

### 3. 导入 GitHub 仓库
1. 在 **Import Git Repository** 区域中，您会看到已关联的 GitHub 账号下的仓库列表。
2. 找到 `fdl-sort-b2b-website` 仓库（如果未找到，可使用搜索框搜索，或点击 "Configure GitHub App" 授予 Vercel 访问该仓库的权限）。
3. 点击仓库右侧的 **Import** 按钮。

### 4. 项目配置（零配置 / Zero Config）
由于我们已经在项目根目录下编写并推送了 `vercel.json`，Vercel 会自动识别并应用所有静态缓存与优化配置。
* **Framework Preset**：选择 **Other**（默认会自动识别为 Other）。
* **Root Directory**：保持 `./` 默认。
* **Build and Output Settings**：无需修改，保持默认（静态 HTML 项目不需要构建命令）。

### 5. 开始部署
点击最下方的 **Deploy** 按钮。
Vercel 将在 5~10 秒内完成部署。部署完成后，您会看到满天飞舞的五彩纸屑 🎉，并获得自动分配的预览地址。

---

## 🛠️ 关于配置文件 `vercel.json`

我们在项目根目录中为您配置了专为 B2B 静态网站优化的 `vercel.json`：
- **静态资源强缓存**：`assets/` 目录下的图片、样式、脚本等资源将被设置为长达 1 年的强缓存（`Cache-Control: public, max-age=31536000, immutable`），极大地提升了二次加载速度。
- **美化 URL**：启用了 `cleanUrls: true`。
- **安全响应头**：为整站添加了安全头，包括 `X-Content-Type-Options: nosniff`、`X-Frame-Options: DENY` 以及 `X-XSS-Protection`，提升了网站安全防护等级。
