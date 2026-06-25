# 域名 DNS 解析与 Cloudflare R2 CDN 配置指南

本指南旨在指导如何完成域名 `fdlsorterai.com` 在 Namecheap 上的 DNS 配置，将其绑定至 Vercel 部署项目；同时详细介绍如何配置 Cloudflare R2 存储桶、上传本地产品图片，并配置自定义 CDN 子域名（`cdn.fdlsorterai.com`）以替换 `index.html` 中的内联 Base64 图片。

通过此优化，您将实现：
- **首屏加载性能（FCP/LCP）飞跃**：HTML 大小从 **1.5MB+** 缩减至 **50KB** 以内，页面解析速度提升数倍。
- **完美的 B2B SEO 友好度**：图片拥有独立 URL 且带有语义化文件名（如 `ai_optical.jpg`），易于被 Google 等搜索引擎收录。
- **几乎为零的 Vercel 流量消耗**：利用 Cloudflare R2 的 **0 流量流出费 (Zero Egress Fees)** 特性，分发高分辨率图片，避免 Vercel 免费额度（100GB）迅速耗尽。
- **高效的浏览器缓存**：图片和静态资源可被浏览器持久缓存，二次访问近乎瞬时加载。

---

## 1. Namecheap DNS 绑定 Vercel

要将新购买的域名 `fdlsorterai.com` 绑定到您在 Vercel 上的 B2B 独立站项目，请按照以下步骤在 Namecheap 中配置 DNS 解析。

### DNS 配置规则表
请将下表中的两条记录添加至您的 Namecheap DNS 管理后台：

| 主机名 (Host) | 记录类型 (Type) | 记录值 (Value) | TTL | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `@` | **A** | `76.76.21.21` | Automatic | 将主域名 `fdlsorterai.com` 指向 Vercel 边缘服务器 |
| `www` | **CNAME** | `cname.vercel-dns.com` | Automatic | 将 `www.fdlsorterai.com` 子域名指向 Vercel 的 DNS 系统 |

### 详细配置步骤
1. **登录 Namecheap**：访问 [Namecheap 官网](https://www.namecheap.com/) 并登录您的账户。
2. **进入域名管理**：在左侧菜单中选择 **Domain List**，找到您的域名 `fdlsorterai.com`，点击右侧的 **Manage** 按钮。
3. **切换到高级 DNS**：在域名管理页顶部导航栏中，点击 **Advanced DNS** 选项卡。
4. **清理旧记录**：在 **Host Records** 下，如果存在默认的 CNAME 或 URL Redirect 记录（例如指向 Namecheap 停放页面的记录），请先点击右侧的垃圾桶图标删除它们。
5. **添加主域名 A 记录**：
   - 点击 **Add New Record** 按钮。
   - **Type** 选择 `A Record`。
   - **Host** 输入 `@`。
   - **Value** 输入 `76.76.21.21`。
   - **TTL** 选择 `Automatic`。
   - 点击绿色的打勾按钮（Save Changes）保存。
6. **添加 www 子域名 CNAME 记录**：
   - 点击 **Add New Record** 按钮。
   - **Type** 选择 `CNAME Record`。
   - **Host** 输入 `www`。
   - **Value** 输入 `cname.vercel-dns.com`。
   - **TTL** 选择 `Automatic`。
   - 点击绿色的打勾按钮保存。

*注：DNS 变更在全球生效可能需要 10 分钟至 48 小时不等，您可以在 Vercel 项目的 Settings -> Domains 页面中点击 "Refresh" 按钮验证绑定状态。*

---

## 2. Cloudflare R2 存储桶创建与资产上传

Cloudflare R2 是兼容 S3 协议的对象存储服务，最大的优势是 **免收外网流量流出费（Zero Egress Fees）**，是搭建高保真图片 CDN 的最佳选择。

### 2.1 创建 R2 存储桶 (Bucket)
1. **登录 Cloudflare**：进入 [Cloudflare 控制台](https://dash.cloudflare.com/)。
2. **进入 R2 页面**：在左侧导航栏中，点击 **R2 Object Storage**。
3. **启用 R2 订阅**：如果是首次使用，根据提示绑定一张信用卡（R2 包含非常宽裕的每月免费额度：10GB 存储，1000 万次 A 类操作，1 亿次 B 类操作，超出部分费率也极低，正常 B2B 独立站基本能保持**完全免费**）。
4. **创建 Bucket**：
   - 点击 **Create bucket** 按钮。
   - **Bucket Name** 填入：`fdlsorter-assets`（可自定义，建议使用小写字母和连字符）。
   - **Location / Region**：选择 **Automatic**（Cloudflare 会根据上传用户的物理位置自动选择最近的存储节点，一般为北美或西欧，可实现全球极速分发）。
   - 点击 **Create bucket** 完成创建。

### 2.2 上传本地静态资产
您的本地项目中，`assets/` 目录下共有以下 11 张高分辨率产品图片：
1. `ai_optical.jpg` (AI 智能色选机视觉图)
2. `eu.jpg` (欧洲市场/标准证书示意图)
3. `film.jpg` (胶片/薄膜材质分选细节图)
4. `hero.jpg` (网站首屏 Banner 核心视觉大图)
5. `hsi3.jpg` (高光谱成像产品模型图 3)
6. `hsi5.jpg` (高光谱成像产品模型图 5)
7. `na.jpg` (北美市场/标准证书示意图)
8. `robot.jpg` (智能机器人/自动化分选臂图)
9. `sea.jpg` (海产品/海带分选应用场景图)
10. `series.jpg` (全系列色选机大合集图)
11. `textile.jpg` (纺织品/无纺布分选应用场景图)

为了保证网站替换后图片能够被正确加载，建议将这些图片上传至 R2 存储桶中，并保留 `assets/` 这个目录层级前缀。

#### 方法一：通过 Cloudflare 网页控制台直接上传（最直观）
1. 在 Cloudflare 中打开刚才创建的 `fdlsorter-assets` 存储桶。
2. 进入 **Objects** 选项卡。
3. 点击 **Upload** 按钮并选择 **Folder**（上传文件夹），或者直接将本地的 `assets` 文件夹拖拽到浏览器窗口中。
4. 确认所有 11 张图片都被选中，路径形式为 `assets/filename.jpg`（例如 `assets/hero.jpg`）。
5. 点击开始上传，等待 11 张图片全部显示为上传成功。

#### 方法二：通过命令行工具 (Wrangler/Rclone) 上传（开发流提效）
如果您习惯使用 CLI 开发工具，可以在本地项目根目录下配置 Cloudflare Wrangler 快速同步：
```bash
# 1. 登录 Cloudflare 账号
npx wrangler login

# 2. 将本地 assets 目录同步上传至 R2 存储桶 fdlsorter-assets 对应的路径下
# 也可使用 rclone 或 aws-cli 等标准 S3 命令行工具进行同步，保持目录结构
# 示例：rclone sync ./assets r2:fdlsorter-assets/assets --progress
```

---

## 3. Cloudflare R2 绑定 CDN 自定义域名

上传完资源后，默认的 R2 临时域名不适合作为生产环境的 CDN 地址。我们需要绑定自定义域名 `cdn.fdlsorterai.com`，并开启 Cloudflare 的免费 SSL 证书保障访问安全。

### 详细绑定步骤
1. **进入存储桶设置**：在 Cloudflare 控制台的 R2 存储桶列表中，点击进入 `fdlsorter-assets`。
2. **切换至 Settings 选项卡**：点击上方的 **Settings**。
3. **绑定自定义域名**：
   - 往下滚动找到 **Public Access**（公共访问）区域。
   - 在 **Custom Domains**（自定义域名）一栏中，点击 **Connect Domain**。
   - 输入您要绑定的子域名：`cdn.fdlsorterai.com`。
   - 点击 **Continue**。
4. **解析与证书配置**：
   - **若您的域名 fdlsorterai.com DNS 已托管在 Cloudflare**：
     Cloudflare 会直接在 DNS 记录里自动帮您添加一条指向 R2 存储桶的 CNAME 记录，您只需确认并点击 **Connect Domain** 即可。
   - **若您的域名 DNS 仍在 Namecheap 管理**：
     Cloudflare 会提示您添加一条验证域名的 CNAME 记录。您需要回到 **Namecheap 的 Advanced DNS** 后台，添加一条新的 **CNAME** 记录：
     - **Host**: `cdn`
     - **Value**: 指向 Cloudflare 提供的 R2 目标地址（例如 `fdlsorter-assets.r2.cloudflarestorage.com` 或 Cloudflare 提示的特定地址）。
     - 保存后，回到 Cloudflare 页面点击 **Verify Domain** 验证。
5. **免费 SSL 证书配置**：
   一旦域名绑定并验证成功，Cloudflare 将自动为 `cdn.fdlsorterai.com` 申请并下发免费的 **Universal SSL (万能 SSL 证书)**，实现全站 `https` 加密传输，全程无需手动续期。
6. **验证访问**：
   在浏览器中输入 `https://cdn.fdlsorterai.com/assets/hero.jpg`，若能正常且飞速地打开首屏主图，说明 CDN 域名绑定及图片上传已全部配置成功！

---

## 4. 替换 index.html 中的 Base64 引用（性能飞跃方案）

目前，您的独立站首屏和产品图采用的是 inline Base64 编码方式。这种方式虽然减少了初期的 HTTP 请求，但由于代码体积庞大（1.5MB+），给网站带来致命的性能和 SEO 缺陷。

### 4.1 代码替换对比示例

#### **优化前：Base64 内联格式（导致 HTML 异常臃肿，超过 1.5MB）**
在原 `index.html` 中，大图是以巨长的 Base64 字符串形式内嵌：
```html
<!-- index.html (以 hero-card 结构下的图片为例) -->
<div class="hero-card">
    <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUEBAQEAwUEBAQGBQUGCA0ICAcHCBALDAkNExAUExIQEhIUFx0ZFBYcFhISGiMaHB4fISEhFBkkJyQgJh0gISD/2wBDAQUGBggHCA8ICA8... (此处省略数十万字符，总长度超过数万行) ..." alt="FDL Optical Sorter banner image">
</div>
```

#### **优化后：CDN 图片链接加载（极简、高可读性、支持缓存）**
替换为基于 Cloudflare R2 托管的自定义 CDN 链接：
```html
<!-- 优化后的 index.html -->
<div class="hero-card">
    <img src="https://cdn.fdlsorterai.com/assets/hero.jpg" alt="FDL Optical Sorter banner image">
</div>
```

### 4.2 性能提升与 SEO 优势深度解析

通过这一重构，网站的底层架构将获得质的提升，特别是在面向海外 B2B 客户的场景下：

1. **页面首屏加载时间 (FCP/LCP) 提升 300%**：
   - 浏览器在加载网页时，必须先将整个 HTML 文档下载完毕，然后才能解析 CSS、JS 并渲染首屏。
   - 原本 1.5MB 的 HTML 在中东、南美、东南亚等 B2B 客户网络较慢的地区，下载需要 3-5 秒甚至更久，导致白屏时间极长。
   - 优化后，HTML 大小骤降至 30KB - 50KB 左右，下载仅需几毫秒，网页核心框架瞬间呈现。
2. **极佳的 B2B SEO 索引效果（提升 Google 排名）**：
   - 搜索引擎蜘蛛（如 Googlebot）抓取网页的单页大小存在预算和物理上限（通常超过 500KB 就会被截断或降低抓取频次）。
   - Base64 的无意义乱码极易干扰 HTML 的文本解析，导致 SEO 核心内容（如关键词、描述、H1 标签）无法被蜘蛛正常索引。
   - 替换为 CDN 链接后，图片具有了语义化的物理文件名（如 `ai_optical.jpg`、`textile.jpg`），蜘蛛可以轻松抓取、索引图片并将其收录在 **Google Images (图片搜索)** 中，为 B2B 独立站带来极高价值的行业精准询盘流量。
3. **大幅降低 Vercel 流量开销，避免超出免费额度**：
   - Vercel 免费版（Hobby Tier）的每月流量额度为 **100GB**。
   - 每次访问臃肿的 HTML（1.5MB），仅需 **6.6 万次访问**就会彻底耗尽额度，从而面临项目被关停或强制升级至高额付费版的风险。
   - 图片迁移到 Cloudflare R2 后，最消耗流量的静态资源全部由 R2 免费分发，Vercel 仅负责输出不到 50KB 的纯文本，即便月访问量达到 **200万次** 也无需支付一分钱流量费。
4. **实现强大的浏览器本地缓存**：
   - 内联 Base64 图片无法被浏览器单独缓存，每次刷新页面都必须重新下载整页代码。
   - 使用 CDN 子域名后，Cloudflare 会在响应头中自动注入强大的缓存策略（例如 `Cache-Control: public, max-age=31536000`）。用户二次访问独立站时，图片直接从其本地设备内存中读取，加载时间缩短至 **0 毫秒**。

---

## 5. 项目持续维护与快速更新建议

为在今后的开发中更方便地管理图片，您可以将此模式固化到工作流中：
- **图片命名规范**：所有新设计的产品、证书、案例图，在上传 R2 之前使用小写英文字母和下划线命名（例如 `certificate_iso9001.jpg`）。
- **图片预压缩**：在上传 Cloudflare R2 之前，建议先在本地或通过 TinyPNG、Squoosh 等工具对 JPG 图片进行无损/有损压缩，确保单张图片控制在 `150KB` 以内，以进一步压榨加载速度极限。
