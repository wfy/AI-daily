# 🌐 全球 AI 日报自动更新网站 (GitHub Pages 部署指南)

本项目可帮助您在 GitHub 上搭建一个**完全免费、每日早晨 07:30 自动更新**的个人全球 AI 日报网站。

---

## 🚀 3 步极速建站指南

### 第一步：创建 GitHub 仓库
1. 登录您的 [GitHub 账号](https://github.com/)。
2. 点击右上角 **`+`** -> **`New repository`**。
3. 仓库名称填写 `ai-daily`（或任意您喜欢的名字），设置为 **`Public`**（公开），点击 **`Create repository`**。

### 第二步：上传本项目的所有文件
1. 在新创建的仓库页面中，点击 **`uploading an existing file`**（上传现有文件）。
2. 将本项目文件夹中的所有文件（包括 `index.html`、`generate_report.py`、`README.md` 以及 `.github` 文件夹）拖拽上传到仓库中。
3. 提交提交信息，点击 **`Commit changes`**。

### 第三步：开启 GitHub Pages 网站服务
1. 在仓库顶部菜单点击 **`Settings`**（设置）。
2. 在左侧边栏找到 **`Pages`**。
3. 在 **`Build and deployment`** 下方的 **`Branch`** 中，选择 **`main`**（或 `master`），目录保持 **`/ (root)`**，点击 **`Save`**。
4. 等待 1-2 分钟，页面顶部即可看到您的专属网站链接：`https://您的用户名.github.io/ai-daily/`！

---

## ⏰ 自动更新说明
- **定时触发**：项目的 GitHub Actions (`.github/workflows/daily_update.yml`) 会在每天早晨 **07:30 (UTC+8)** 自动运行 Python 脚本，抓取最新的全球 AI 新闻并更新页面。
- **手动触发**：您也可以随时在 GitHub 仓库的 **`Actions`** 选项卡中点击 **`Run workflow`** 立即更新网站！
